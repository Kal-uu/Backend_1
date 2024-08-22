from pathlib import Path

from fastapi import UploadFile

MAKE_DIR = Path(__file__).parent / "media"


def save_file(file: UploadFile, subdir: str) -> str:
    file_dir = MAKE_DIR / subdir
    file_dir.mkdir(parents=True, exist_ok=True)
    file_path = file_dir/file.filename

    with open(file_path, "wb") as f:
        f.write(file.file.read())
        return str(file.filename)
