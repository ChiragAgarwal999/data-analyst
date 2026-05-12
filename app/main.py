from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from app.api.upload import router as upload_router
from app.api.analysis import router as analysis_router

app = FastAPI(title="AI Data Analyst SaaS", version="2.0.0")
app.mount("/assets", StaticFiles(directory="app/static"), name="assets")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(upload_router)
app.include_router(analysis_router)


@app.get("/")
def root():
    return FileResponse("app/static/index.html")


@app.get("/favicon.ico")
def favicon():
    return JSONResponse(status_code=204, content=None)


@app.get("/health")
def health():
    return {"status": "ok"}
