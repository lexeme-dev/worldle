from __future__ import annotations

import datetime
from math import atan2, cos, degrees, radians, sin

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
        lat1, lon1 = (
            radians(self.guessed_country.geo_point_shp.y),
            radians(self.guessed_country.geo_point_shp.x),
        )
        lat2, lon2 = (
            radians(self.game.answer_country.geo_point_shp.y),
            radians(self.game.answer_country.geo_point_shp.x),
        )

        d_lon = lon2 - lon1
        x = sin(d_lon) * cos(lat2)
        y = cos(lat1) * sin(lat2) - (sin(lat1) * cos(lat2) * cos(d_lon))
        initial_bearing = atan2(x, y)
        initial_bearing = degrees(initial_bearing)
        compass_bearing = (initial_bearing + 360) % 360
        return compass_bearing

    @property
    def compass_direction_to_answer(self) -> CompassDirection:
        bearing = self.bearing_to_answer
        directions = [
            (CompassDirection.NORTH, 0),
            (CompassDirection.NORTH_EAST, 45),
            (CompassDirection.EAST, 90),
            (CompassDirection.SOUTH_EAST, 135),
            (CompassDirection.SOUTH, 180),
            (CompassDirection.SOUTH_WEST, 225),
            (CompassDirection.WEST, 270),
            (CompassDirection.NORTH_WEST, 315),
        ]
        for direction, angle in directions:
            if (bearing >= angle - 22.5) and (bearing < angle + 22.5):
                return direction
        return CompassDirection.NORTH  # Default case

    @property
    def proximity_prop(self) -> float:
        normalized_distance = min(
            self.distance_to_answer_miles / EARTH_MAX_DISTANCE_MILES, 1
        )
        return 1 - normalized_distance
