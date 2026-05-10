from pathlib import Path
from fastapi import UploadFile

BASE = Path("storage")
BASE.mkdir(exist_ok=True)
DB: dict[str, dict] = {}


async def save_upload(file: UploadFile, file_id: str) -> Path:
    out_dir = BASE / file_id
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / file.filename
    with dest.open("wb") as f:
        f.write(await file.read())
    return dest


def register_file_record(file_id: str, path: Path):
    DB[file_id] = {
        "input_path": str(path),
        "output_dir": str(path.parent),
        "status": "uploaded",
    }


def get_record(file_id: str):
    return DB.get(file_id)


def update_record(file_id: str, patch: dict):
    if file_id in DB:
        DB[file_id].update(patch)
