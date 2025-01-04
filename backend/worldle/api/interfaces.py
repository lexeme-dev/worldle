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
                        shapely.wkb.loads(bytes(v.value.data))
                    ),
                    "properties": {},
                }
            elif isinstance(v.value, float) and (
                math.isnan(v.value) or math.isinf(v.value)
            ):
                output[k] = None
            else:
                output[k] = v.value

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
    parent_iso3: str | None


class CountryItem(CountryBase):
    pass


class CountryRead(CountryBase):
    geometry: GeoJsonGeometry
    geo_point: GeoJsonGeometry
