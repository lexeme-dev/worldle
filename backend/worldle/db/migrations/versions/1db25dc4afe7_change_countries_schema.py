"""Change countries schema

Revision ID: 1db25dc4afe7
Revises: 5069297c64c1
Create Date: 2025-01-03 21:36:27.366046

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from geoalchemy2 import Geometry

# revision identifiers, used by Alembic.
revision: str = "1db25dc4afe7"
down_revision: str | None = "5069297c64c1"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "countries", sa.Column("iso_3166_1_alpha_2_codes", sa.String(), nullable=False)
    )
    op.add_column("countries", sa.Column("iso3", sa.String(), nullable=False))
    op.add_column("countries", sa.Column("status", sa.String(), nullable=False))
    op.add_column("countries", sa.Column("continent", sa.String(), nullable=False))
    op.add_column("countries", sa.Column("region", sa.String(), nullable=False))
    op.add_column("countries", sa.Column("color_code", sa.String(), nullable=True))
    op.add_geospatial_column(
        "countries",
        sa.Column(
            "geo_point",
            Geometry(
                geometry_type="POINT",
                srid=4326,
                spatial_index=False,
                from_text="ST_GeomFromEWKT",
                name="geometry",
                nullable=False,
            ),
            nullable=False,
        ),
    )
    op.create_geospatial_index(
        "idx_countries_geo_point",
        "countries",
        ["geo_point"],
        unique=False,
        postgresql_using="gist",
        postgresql_ops={},
    )
    op.drop_column("countries", "is_island")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "countries",
        sa.Column("is_island", sa.BOOLEAN(), autoincrement=False, nullable=True),
    )
    op.drop_geospatial_index(
        "idx_countries_geo_point",
        table_name="countries",
        postgresql_using="gist",
        column_name="geo_point",
    )
    op.drop_geospatial_column("countries", "geo_point")
    op.drop_column("countries", "color_code")
    op.drop_column("countries", "region")
    op.drop_column("countries", "continent")
    op.drop_column("countries", "status")
    op.drop_column("countries", "iso3")
    op.drop_column("countries", "iso_3166_1_alpha_2_codes")
    # ### end Alembic commands ###
