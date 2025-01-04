from __future__ import annotations

import datetime
from math import atan2, degrees

import geoalchemy2 as ga
import rl.utils.bucket as bucket_utils
from geopy.distance import geodesic
from shapely import Point
from sqlalchemy import ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)

from worldle.utils.game import CompassDirection, GameStatus


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
        ga.Geometry(geometry_type="MULTIPOLYGON", srid=4326), deferred=True
    )
    geo_point: Mapped[ga.types.Geometry] = mapped_column(
        ga.Geometry(geometry_type="POINT", srid=4326), deferred=True
    )

    svg_bucket_path: Mapped[str | None] = mapped_column()

    parent_id: Mapped[int | None] = mapped_column(ForeignKey("countries.id"))
    parent: Mapped[Country | None] = relationship(
        remote_side=[id], back_populates="children"
    )
    children: Mapped[list[Country]] = relationship(back_populates="parent")

    @property
    def svg_url(self) -> str:
        return bucket_utils.get_public_url(self.svg_bucket_path)

    @property
    def geo_point_shp(self) -> Point:
        return ga.shape.to_shape(self.geo_point)


class UserClient(TimestampMixin, Base):
    __tablename__ = "user_clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(unique=True, index=True)


class Game(TimestampMixin, Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True)
    answer_country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"))
    user_client_id: Mapped[int] = mapped_column(ForeignKey("user_clients.id"))
    status: Mapped[GameStatus] = mapped_column(String(), default=GameStatus.IN_PROGRESS)

    answer_country: Mapped[Country] = relationship(lazy="joined")
    user_client: Mapped[UserClient] = relationship()
    guesses: Mapped[list[Guess]] = relationship(back_populates="game", lazy="joined")


EARTH_MAX_DISTANCE_MILES = 12_450  # Max distance between two points on Earth


class Guess(TimestampMixin, Base):
    __tablename__ = "guesses"
    __table_args__ = (UniqueConstraint("game_id", "index", name="uq_guess_game_index"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))
    guessed_country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"))
    index: Mapped[int] = mapped_column()

    game: Mapped[Game] = relationship(back_populates="guesses", lazy="joined")
    guessed_country: Mapped[Country] = relationship()

    @property
    def is_correct(self) -> bool:
        return self.guessed_country_id == self.game.answer_country_id

    @property
    def distance_to_answer_miles(self) -> float:
        guess_point = (
            self.guessed_country.geo_point_shp.y,
            self.guessed_country.geo_point_shp.x,
        )
        answer_point = (
            self.game.answer_country.geo_point_shp.y,
            self.game.answer_country.geo_point_shp.x,
        )
        return geodesic(guess_point, answer_point).miles

    @property
    def bearing_to_answer(self) -> float:
        guess = self.guessed_country.geo_point_shp
        answer = self.game.answer_country.geo_point_shp

        # Convert to Mercator-like coordinates (treating -180,-90 as origin)
        x1, y1 = guess.x + 180, guess.y + 90
        x2, y2 = answer.x + 180, answer.y + 90

        # Calculate angle in degrees
        angle = degrees(atan2(y2 - y1, x2 - x1))
        return angle % 360

    @property
    def compass_direction_to_answer(self) -> CompassDirection:
        angle = self.bearing_to_answer
        if 22.5 <= angle < 67.5:
            return CompassDirection.NORTH_EAST
        elif 67.5 <= angle < 112.5:
            return CompassDirection.NORTH
        elif 112.5 <= angle < 157.5:
            return CompassDirection.NORTH_WEST
        elif 157.5 <= angle < 202.5:
            return CompassDirection.WEST
        elif 202.5 <= angle < 247.5:
            return CompassDirection.SOUTH_WEST
        elif 247.5 <= angle < 292.5:
            return CompassDirection.SOUTH
        elif 292.5 <= angle < 337.5:
            return CompassDirection.SOUTH_EAST
        else:
            return CompassDirection.EAST

    @property
    def proximity_prop(self) -> float:
        normalized_distance = min(
            self.distance_to_answer_miles / EARTH_MAX_DISTANCE_MILES, 1
        )
        return 1 - normalized_distance
