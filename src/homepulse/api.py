from __future__ import annotations

import tempfile
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from .analytics import analyse, forecast_next_day
from .io import load_readings

app = FastAPI(title="HomePulse API", version="0.1.0")


@app.get("/")
def home() -> FileResponse:
    return FileResponse(Path(__file__).parent / "web" / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/analyse")
async def analyse_upload(upload: UploadFile = File(...)) -> dict[str, object]:
    if not (upload.filename or "").lower().endswith(".csv"):
        raise HTTPException(status_code=415, detail="Upload a CSV file")
    with tempfile.NamedTemporaryFile(suffix=".csv") as temporary:
        temporary.write(await upload.read())
        temporary.flush()
        readings = load_readings(temporary.name)
    return {"analysis": analyse(readings), "next_day_forecast": forecast_next_day(readings)}
