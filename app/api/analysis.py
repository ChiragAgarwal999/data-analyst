from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.services.ml_engine import run_full_pipeline
from app.utils.file_handler import get_record

router = APIRouter(tags=["analysis"])


@router.post("/process/{file_id}")
async def process(file_id: str):
    record = get_record(file_id)
    if not record:
        raise HTTPException(status_code=404, detail="file_id not found")
    result = await run_full_pipeline(file_id, record)
    return result


@router.get("/report/{file_id}")
def get_report(file_id: str):
    record = get_record(file_id)
    if not record or not record.get("report_pdf"):
        raise HTTPException(status_code=404, detail="Report not ready")
    return FileResponse(record["report_pdf"], filename="insight_report.pdf")


@router.get("/cleaned/{file_id}")
def get_cleaned(file_id: str):
    record = get_record(file_id)
    if not record or not record.get("cleaned_excel"):
        raise HTTPException(status_code=404, detail="Cleaned file not ready")
    return FileResponse(record["cleaned_excel"], filename="cleaned_dataset.xlsx")
