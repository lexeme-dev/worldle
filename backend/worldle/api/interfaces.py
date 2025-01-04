from __future__ import annotations

import math
from enum import StrEnum
from typing import Any, Literal

import geoalchemy2 as ga
import shapely.wkb
import sqlalchemy as sa
from pydantic import BaseModel, ConfigDict, model_validator
from typing_extensions import TypedDict

from worldle.db.models import Base


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

    @model_validator(mode="before")
    def transform_wkb(cls, obj: Any, *args, **kwargs) -> Any:
        if not isinstance(obj, Base):
            return obj

        output = {}
        inspector = sa.inspect(obj)

        # Handle regular attributes
        for k, v in inspector.attrs.items():
            if isinstance(v.loaded_value, ga.elements.WKBElement):
                output[k] = {
                    "type": "Feature",
                    "geometry": shapely.geometry.mapping(
                        shapely.wkb.loads(bytes(v.loaded_value.data))
                    ),
                    "properties": {},
                }
            elif isinstance(v.loaded_value, float) and (
                math.isnan(v.loaded_value) or math.isinf(v.loaded_value)
            ):
                output[k] = None
            else:
                output[k] = v.loaded_value

        # Include @property methods
        for k in dir(obj.__class__):
            if isinstance(getattr(obj.__class__, k), property):
                output[k] = getattr(obj, k)

        return output


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


class UserClientBase(ApiModel):
    id: int
    uuid: str


class UserClientRead(UserClientBase):
    pass


class GuessBase(ApiModel):
    id: int
    guessed_country_id: int
    guessed_country: CountryItem
    index: int


class GuessCreate(BaseModel):
    guessed_country_id: int


class GuessRead(GuessBase):
    pass


class GameBase(ApiModel):
    id: int
    user_client_id: int
    answer_country_id: int


class GameCreate(BaseModel):
    user_client_uuid: str


class GameRead(GameBase):
    guesses: list[GuessRead]
