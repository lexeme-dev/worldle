from __future__ import annotations

import datetime

import geoalchemy2 as ga
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )


class Country(TimestampMixin, Base):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    is_island: Mapped[bool | None]
    geometry: Mapped[ga.types.Geometry] = mapped_column(
        ga.Geometry(geometry_type="MULTIPOLYGON", srid=4326)
    )

    parent_id: Mapped[int | None] = mapped_column(ForeignKey("countries.id"))

    parent: Mapped[Country | None] = relationship(back_populates="children")
