from pathlib import Path

import rl.utils.bucket as bucket_utils
import rl.utils.click as click
import rl.utils.io
import s3fs
import shapely
import shapely.ops
import svgwrite
import tqdm
from pyproj import Transformer
from sqlalchemy import select
from tqdm.contrib.concurrent import thread_map

import worldle.utils.image as image_utils
from worldle.db.models import Country
from worldle.db.session import get_session

_DEFAULT_SVG_DIR = rl.utils.io.get_data_path("country_svgs")
_TARGET_SIZE = 256  # pixels for the longer dimension

# Create transformer from WGS84 (EPSG:4326) to Web Mercator (EPSG:3857)
_TRANSFORMER = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)


def _upload_svg(args: tuple[Path, str, s3fs.S3FileSystem]) -> None:
    svg_path, bucket_path, fs = args
    bucket_utils.write_file(svg_path, bucket_path, fs)


def _generate_svg(country: Country, output_dir: Path) -> tuple[Path, str]:
    geom = shapely.wkb.loads(bytes(country.geometry.data))
    # Project the geometry to Web Mercator
    projected_geom = shapely.ops.transform(
        lambda x, y: _TRANSFORMER.transform(x, y), geom
    )

    minx, miny, maxx, maxy = projected_geom.bounds
    width = maxx - minx
    height = maxy - miny

    dwg = svgwrite.Drawing(
        size=(f"{_TARGET_SIZE}px", f"{_TARGET_SIZE}px"),
        viewBox=f"{minx} {-maxy} {width} {height}",
    )

    path_data = ""
    for polygon in projected_geom.geoms:
        coords = list(polygon.exterior.coords)
        path_data += f"M {coords[0][0]},{-coords[0][1]} "
        path_data += " ".join(f"L {x},{-y}" for x, y in coords[1:])
        path_data += " Z "

    dwg.add(dwg.path(d=path_data, fill="black"))

    output_path = output_dir / f"{country.iso3}.svg"
    dwg.saveas(output_path)
    file_sha1 = image_utils.get_file_sha1(output_path)
    if file_sha1 is None:
        return output_path, None
    return output_path, file_sha1


@click.command()
@click.option(
    "-o",
    "--output-dir",
    type=click.Path(file_okay=False, path_type=Path),
    default=_DEFAULT_SVG_DIR,
    help="Directory to save SVG files",
)
def main(output_dir: Path) -> None:
    """Generate SVG files for each country's geometry."""
    output_dir.mkdir(parents=True, exist_ok=True)
    fs = bucket_utils.get_bucket_fs()
    upload_args = []
    existing_hashes = image_utils.get_existing_image_sha1s(fs)

    with get_session() as session:
        stmt = select(Country).where(Country.iso3.is_not(None))
        countries = session.execute(stmt).scalars().all()

        for country in tqdm.tqdm(countries, desc="Generating SVGs"):
            svg_path, sha1 = _generate_svg(country, output_dir)
            if sha1 is None:
                country.svg_bucket_path = None
                continue
            bucket_path = image_utils.get_image_bucket_path(sha1)
            if sha1 not in existing_hashes:
                upload_args.append((svg_path, bucket_path, fs))
            country.svg_bucket_path = bucket_path

        if upload_args:
            thread_map(_upload_svg, upload_args, desc="Uploading SVGs", max_workers=8)
        session.commit()


if __name__ == "__main__":
    main()
