import json
import re
from pathlib import Path

import geoalchemy2 as ga
import rl.utils.click as click
import rl.utils.io
import tqdm
from rl.utils import LOGGER
from shapely.geometry import MultiPolygon, Point, shape
from sqlalchemy.orm import Session

from worldle.db.models import Country
from worldle.db.session import get_session

_DEFAULT_COUNTRIES_PATH = rl.utils.io.get_data_path(
    "raw", "world_administrative_boundaries.json"
)
_COUNTRIES_URL = (
    "https://cdn.worldle.lexeme.dev/world_administrative_boundaries_opendatasoft.json"
)


def _ingest_countries(data: list[dict], session: Session) -> None:
    # First pass: create all countries
    country_map: dict[str, Country] = {}
    for record in tqdm.tqdm(data, desc="Creating countries"):
        geom = shape(record["geo_shape"]["geometry"])
        if not isinstance(geom, MultiPolygon):
            geom = MultiPolygon([geom])

        point_coords = record["geo_point_2d"]
        point = Point(point_coords["lon"], point_coords["lat"])

        iso3 = record["iso3"]
        parent_iso3 = record.get("color_code")
        if parent_iso3 == "XXX" or parent_iso3 == iso3:
            parent_iso3 = None

        name = re.sub(r"(.*)\s\((.*)\)", r"\1", record["name"])

        country = Country(
            name=name,
            iso2=record["iso_3166_1_alpha_2_codes"],
            iso3=record["iso3"],
            status=record["status"],
            continent=record["continent"],
            region=record["region"],
            parent_iso3=parent_iso3,
            geometry=ga.WKBElement(geom.wkb, srid=4326),
            geo_point=ga.WKBElement(point.wkb, srid=4326),
        )
        session.add(country)
        country_map[country.iso3] = country

    # Second pass: set parent relationships
    for country in tqdm.tqdm(country_map.values(), desc="Setting parent relationships"):
        if country.parent_iso3:
            country.parent = country_map[country.parent_iso3]

    session.commit()


@click.command()
@click.option(
    "-c",
    "--countries-path",
    type=click.Path(dir_okay=False, path_type=Path),
    default=_DEFAULT_COUNTRIES_PATH,
    help="Path to countries JSON file",
)
def main(countries_path: Path) -> None:
    """Ingest country geometries into database."""
    if not countries_path.exists():
        LOGGER.info("Downloading countries file...")
        countries_path.parent.mkdir(parents=True, exist_ok=True)
        rl.utils.io.download(_COUNTRIES_URL, countries_path)

    with countries_path.open() as f:
        data = json.load(f)

    with get_session() as session:
        LOGGER.info("Ingesting %d countries", len(data))
        _ingest_countries(data, session)


if __name__ == "__main__":
    main()
