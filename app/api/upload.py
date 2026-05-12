from fastapi import APIRouter, File, UploadFile, HTTPException
from pathlib import Path
import uuid

from app.utils.file_handler import save_upload, register_file_record

router = APIRouter(tags=["upload"])


@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    ext = Path(file.filename).suffix.lower()
    if ext not in {".xlsx", ".csv"}:
        raise HTTPException(status_code=400, detail="Supported formats: .xlsx, .csv")
    file_id = str(uuid.uuid4())
    path = await save_upload(file, file_id)
    register_file_record(file_id, path)
    return {"file_id": file_id, "filename": file.filename, "status": "uploaded"}
