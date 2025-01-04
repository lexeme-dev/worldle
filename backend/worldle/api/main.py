from collections.abc import Generator
from typing import Annotated

import rl.utils.io
from diskcache import Cache
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session, defer

from worldle.api.interfaces import CountryItem, CountryRead
from worldle.db.models import Country
from worldle.db.session import get_session

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
