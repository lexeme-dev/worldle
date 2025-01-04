import uuid
from collections.abc import Generator
from typing import Annotated

import rl.utils.io
from diskcache import Cache
from fastapi import Depends, FastAPI, HTTPException
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


# endregion


@app.get(
    "/countries",
    response_model=list[CountryItem],
    operation_id="listCountries",
)
def list_countries(db: Annotated[Session, Depends(get_db)]):
    cache_key = "__all_countries"
    if cache_key in _COUNTRIES_CACHE:
        return _COUNTRIES_CACHE[cache_key]

    countries = db.scalars(
        select(Country).options(defer(Country.geometry), defer(Country.geo_point))
    ).all()
    _COUNTRIES_CACHE[cache_key] = [CountryItem.model_validate(c) for c in countries]
    return _COUNTRIES_CACHE[cache_key]


@app.get(
    "/countries/{country_id}",
    response_model=CountryRead,
    operation_id="readCountry",
)
def read_country(
    country: Annotated[Country, Depends(get_country)],
):
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


@app.post(
    "/games",
    response_model=GameRead,
    operation_id="createGame",
)
def create_game(
    db: Annotated[Session, Depends(get_db)],
    game_create: GameCreate,
):
    user_client = db.scalar(
        select(UserClient).where(UserClient.uuid == game_create.user_client_uuid)
    )
    if not user_client:
        raise HTTPException(status_code=404, detail="User client not found")

    # Get random country for answer
    answer_country = db.scalar(select(Country).order_by(func.random()))

    game = Game(user_client=user_client, answer_country=answer_country)
    db.add(game)
    db.commit()
    return game


@app.get(
    "/games/{game_id}",
    response_model=GameRead,
    operation_id="readGame",
)
def read_game(
    db: Annotated[Session, Depends(get_db)],
    game_id: int,
):
    game = db.get(Game, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


@app.post(
    "/games/{game_id}/guesses",
    response_model=GuessRead,
    operation_id="createGuess",
)
def create_guess(
    db: Annotated[Session, Depends(get_db)],
    game_id: int,
    guess_create: GuessCreate,
):
    game = db.get(Game, game_id)
    if not game:
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
    return guess
