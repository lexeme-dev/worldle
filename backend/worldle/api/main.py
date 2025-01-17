import uuid
from collections.abc import Generator
from typing import Annotated

import rl.utils.io
from diskcache import Cache
from fastapi import Depends, FastAPI, Header, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, select
from sqlalchemy.orm import Session, defer

from worldle.api.interfaces import (
    CountryItem,
    CountryRead,
    GameCreate,
    GameRead,
    GameStatus,
    GuessCreate,
    GuessRead,
    UserClientRead,
)
from worldle.db.models import Country, Game, Guess, UserClient
from worldle.db.session import get_session
from worldle.utils.game import MAX_GUESSES
from worldle.utils.stats import UserStats, get_user_stats

_COUNTRIES_CACHE = Cache(rl.utils.io.get_cache_dir("countries"))

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# region Dependencies


def get_db() -> Generator[Session, None, None]:
    session = get_session()
    try:
        yield session
    finally:
        session.close()


def get_country(db: Annotated[Session, Depends(get_db)], country_id: int) -> Country:
    country = db.get(Country, country_id)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return country


def get_user_client(
    db: Annotated[Session, Depends(get_db)], user_client_uuid: str
) -> UserClient:
    user_client = db.scalar(
        select(UserClient).where(UserClient.uuid == user_client_uuid)
    )
    if not user_client:
        raise HTTPException(status_code=404, detail="User client not found")
    return user_client


def get_authed_user_client(
    db: Annotated[Session, Depends(get_db)],
    x_worldle_user_client_uuid: str | None = Header(None),
) -> UserClient:
    if not x_worldle_user_client_uuid:
        raise HTTPException(
            status_code=401, detail="X-Worldle-User-Client-Uuid header is required"
        )

    user_client = db.scalar(
        select(UserClient).where(UserClient.uuid == x_worldle_user_client_uuid)
    )
    if not user_client:
        raise HTTPException(status_code=404, detail="User client not found")
    return user_client


# endregion


@app.get(
    "/countries",
    response_model=list[CountryItem],
    operation_id="listCountries",
)
def list_countries(response: Response, db: Annotated[Session, Depends(get_db)]):
    response.headers["Cache-Control"] = "public, max-age=86400"  # Cache for 24 hours

    cache_key = "__all_countries"
    if cache_key in _COUNTRIES_CACHE:
        return _COUNTRIES_CACHE[cache_key]

    countries = db.scalars(
        select(Country)
        .options(defer(Country.geometry), defer(Country.geo_point))
        .order_by(Country.name.asc())
    ).all()
    _COUNTRIES_CACHE[cache_key] = [CountryItem.model_validate(c) for c in countries]
    return _COUNTRIES_CACHE[cache_key]


@app.get(
    "/countries/{country_id}",
    response_model=CountryRead,
    operation_id="readCountry",
)
def read_country(
    response: Response,
    country: Annotated[Country, Depends(get_country)],
):
    response.headers["Cache-Control"] = "public, max-age=86400"  # Cache for 24 hours

    cache_key = f"__country_{country.id}"
    if cache_key in _COUNTRIES_CACHE:
        return _COUNTRIES_CACHE[cache_key]

    _COUNTRIES_CACHE[cache_key] = CountryRead.model_validate(country)
    return _COUNTRIES_CACHE[cache_key]


@app.post(
    "/user_clients",
    response_model=UserClientRead,
    operation_id="createUserClient",
)
def create_user_client(db: Annotated[Session, Depends(get_db)]):
    client = UserClient(uuid=str(uuid.uuid4()))
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


@app.get(
    "/user_clients/{user_client_uuid}",
    response_model=UserClientRead,
    operation_id="readUserClient",
)
def read_user_client(
    user_client: Annotated[UserClient, Depends(get_user_client)],
):
    return user_client


@app.get(
    "/user_clients/{user_client_uuid}/current_game",
    response_model=GameRead | None,
    operation_id="readCurrentGame",
)
def read_current_game(
    db: Annotated[Session, Depends(get_db)],
    user_client: Annotated[UserClient, Depends(get_user_client)],
):
    return db.scalar(
        select(Game)
        .where(Game.user_client_id == user_client.id)
        .where(Game.status == GameStatus.IN_PROGRESS)
        .order_by(Game.created_at.desc())
        .limit(1)
    )


@app.get(
    "/user_clients/{user_client_uuid}/stats",
    response_model=UserStats,
    operation_id="readUserStats",
)
def read_user_stats(
    db: Annotated[Session, Depends(get_db)],
    user_client: Annotated[UserClient, Depends(get_user_client)],
):
    return get_user_stats(user_client.id, db)


@app.post(
    "/games",
    response_model=GameRead,
    operation_id="createGame",
)
def create_game(
    db: Annotated[Session, Depends(get_db)],
    user_client: Annotated[UserClient, Depends(get_authed_user_client)],
    game_create: GameCreate,
):
    active_game = db.scalar(
        select(Game)
        .where(Game.user_client_id == user_client.id)
        .where(Game.status == GameStatus.IN_PROGRESS)
    )
    if active_game:
        # TODO: Should we do this here or require a separate API call first?
        active_game.status = GameStatus.ABANDONED

    # Get random country for answer
    answer_country = db.scalar(
        select(Country)
        .where(Country.svg_bucket_path.isnot(None))
        .order_by(func.random())
        .limit(1)
    )

    game = Game(
        user_client=user_client,
        answer_country=answer_country,
        status=GameStatus.IN_PROGRESS,
    )
    db.add(game)
    db.commit()
    db.refresh(game)
    return game


@app.get(
    "/games/{game_id}",
    response_model=GameRead,
    operation_id="readGame",
)
def read_game(
    db: Annotated[Session, Depends(get_db)],
    user_client: Annotated[UserClient, Depends(get_authed_user_client)],
    game_id: int,
):
    game = db.get(Game, game_id)
    if not game or game.user_client_id != user_client.id:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


@app.post(
    "/games/{game_id}/guesses",
    response_model=GuessRead,
    operation_id="createGuess",
)
def create_guess(
    db: Annotated[Session, Depends(get_db)],
    user_client: Annotated[UserClient, Depends(get_authed_user_client)],
    game_id: int,
    guess_create: GuessCreate,
):
    game = db.get(Game, game_id)
    if not game or game.user_client_id != user_client.id:
        raise HTTPException(status_code=404, detail="Game not found")

    if game.status != GameStatus.IN_PROGRESS:
        raise HTTPException(status_code=400, detail="Game is already complete")

    guess_count = len(game.guesses)
    if guess_count >= MAX_GUESSES:
        raise HTTPException(status_code=400, detail="Maximum guesses reached")

    guessed_country = db.get(Country, guess_create.guessed_country_id)
    if not guessed_country:
        raise HTTPException(status_code=404, detail="Country not found")

    guess = Guess(game=game, guessed_country=guessed_country, index=guess_count)
    db.add(guess)

    # Update game status
    if guessed_country.id == game.answer_country_id:
        game.status = GameStatus.WON
    elif guess_count == MAX_GUESSES - 1:  # This is the last guess
        game.status = GameStatus.LOST

    db.commit()
    db.refresh(guess)
    return guess
