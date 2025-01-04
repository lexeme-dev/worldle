import hashlib
from pathlib import Path

import rl.utils.bucket as bucket_utils
import rl.utils.io
import s3fs

IMAGE_LOCAL_DIR = rl.utils.io.get_data_path("images")
IMAGES_BUCKET_BASE_PATH = "images"


def get_file_sha1(file_path: Path) -> str:
    return hashlib.sha1(file_path.read_bytes()).hexdigest()


def get_image_bucket_path(image_sha1: str) -> str:
    return f"{IMAGES_BUCKET_BASE_PATH}/{image_sha1[:2]}/{image_sha1[2:4]}/{image_sha1}"


def get_image_local_path(image_sha1: str) -> Path:
    return Path(IMAGE_LOCAL_DIR) / image_sha1[:2] / image_sha1


def get_existing_image_sha1s(fs: s3fs.S3FileSystem) -> set[str]:
    return {
        Path(p).name
        for p in bucket_utils.list_bucket_files(IMAGES_BUCKET_BASE_PATH, fs)
    }


def get_or_download_image(image_sha1: str, fs: s3fs.S3FileSystem) -> Path:
    local_path = get_image_local_path(image_sha1)
    if not local_path.exists():
        bucket_path = get_image_bucket_path(image_sha1)
        local_path.parent.mkdir(parents=True, exist_ok=True)
        local_path.write_bytes(bucket_utils.read_file(bucket_path, fs))
    return local_path
