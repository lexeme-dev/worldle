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
    iso2: Mapped[str | None] = mapped_column()
    iso3: Mapped[str | None] = mapped_column()
    status: Mapped[str | None] = mapped_column()
    continent: Mapped[str | None] = mapped_column()
    region: Mapped[str | None] = mapped_column()
    parent_iso3: Mapped[str | None] = mapped_column()

    geometry: Mapped[ga.types.Geometry] = mapped_column(
        ga.Geometry(geometry_type="MULTIPOLYGON", srid=4326)
    )
    geo_point: Mapped[ga.types.Geometry] = mapped_column(
        ga.Geometry(geometry_type="POINT", srid=4326)
    )

    parent_id: Mapped[int | None] = mapped_column(ForeignKey("countries.id"))
    parent: Mapped[Country | None] = relationship(
        remote_side=[id], back_populates="children"
    )
    children: Mapped[list[Country]] = relationship(back_populates="parent")
