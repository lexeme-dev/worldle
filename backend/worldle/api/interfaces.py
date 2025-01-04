from __future__ import annotations

from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict
from typing_extensions import TypedDict

from worldle.utils.game import CompassDirection, GameStatus


class GeoJsonGeometryType(StrEnum):
    POINT = "Point"
    LINESTRING = "LineString"
    POLYGON = "Polygon"
    MULTIPOLYGON = "MultiPolygon"
    MULTILINESTRING = "MultiLineString"


class GeoJsonGeometry(TypedDict):
    type: GeoJsonGeometryType
    coordinates: list[Any]  # Type varies based on geometry type


class GeoJson(TypedDict):
    type: Literal["Feature"]
    geometry: GeoJsonGeometry
    properties: dict[str, Any] | None


class ApiModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class CountryBase(ApiModel):
    id: int
    name: str
    iso2: str | None
    iso3: str | None
    status: str | None
    continent: str | None
    region: str | None
    parent_id: int | None
    svg_url: str | None


class CountryItem(CountryBase):
    pass


class CountryRead(CountryBase):
    pass


class UserClientRead(ApiModel):
    uuid: str


class GuessBase(ApiModel):
    id: int
    guessed_country_id: int
    guessed_country: CountryItem
    index: int
    is_correct: bool
    distance_to_answer_miles: float
    distance_to_answer_km: float
    bearing_to_answer: float
    compass_direction_to_answer: CompassDirection
    proximity_prop: float


class GuessItem(GuessBase):
    pass


class GuessRead(GuessBase):
    game: GameRead


class GuessCreate(ApiModel):
    guessed_country_id: int


class GameBase(ApiModel):
    id: int
    user_client_id: int
    answer_country_id: int
    status: GameStatus

    answer_country: CountryItem


class GameCreate(ApiModel):
    user_client_uuid: str


class GameItem(GameBase):
    pass


class GameRead(GameBase):
    guesses: list[GuessItem]
