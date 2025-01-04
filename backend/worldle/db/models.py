from __future__ import annotations

import datetime

import geoalchemy2 as ga
import rl.utils.bucket as bucket_utils
from sqlalchemy import ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)

from worldle.utils.game import GameStatus


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

    svg_bucket_path: Mapped[str | None] = mapped_column()

    parent_id: Mapped[int | None] = mapped_column(ForeignKey("countries.id"))
    parent: Mapped[Country | None] = relationship(
        remote_side=[id], back_populates="children"
    )
    children: Mapped[list[Country]] = relationship(back_populates="parent")

    @property
    def svg_url(self) -> str:
        return bucket_utils.get_public_url(self.svg_bucket_path)


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

    answer_country: Mapped[Country] = relationship()
    user_client: Mapped[UserClient] = relationship()
    guesses: Mapped[list[Guess]] = relationship(back_populates="game", lazy="joined")


class Guess(TimestampMixin, Base):
    __tablename__ = "guesses"
    __table_args__ = (UniqueConstraint("game_id", "index", name="uq_guess_game_index"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))
    guessed_country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"))
    index: Mapped[int] = mapped_column()

    game: Mapped[Game] = relationship(back_populates="guesses")
    guessed_country: Mapped[Country] = relationship()
