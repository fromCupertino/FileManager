import shutil
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from config import UPLOAD_DIR, CORS_ORIGINS

app = FastAPI()


@app.on_event("startup")
def ensure_upload_dir():
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/files")
def get_files(limit: int | None = Query(None, ge=1)):
    files_data = []

    for f in Path(UPLOAD_DIR).iterdir():
        if f.is_file():
            stat = f.stat()
            files_data.append({
                "name": f.name,
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
            })

    files_data.sort(key=lambda x: x["name"])

    # Ограничиваем по limit, если передан
    if limit is not None:
        files_data = files_data[:limit]

    return files_data


@app.get("/download/{filename}")
def download_file(filename: str):
    safe_name = Path(filename).name
    file_path = UPLOAD_DIR / safe_name

    if not file_path.exists():
        return {"error": "File not found"}

    return FileResponse(
        path=file_path,
        filename=safe_name,
        media_type="application/octet-stream"
    )

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    safe_name = Path(file.filename).name
    file_path = UPLOAD_DIR / safe_name

    if file_path.exists():
        raise HTTPException(
            status_code=409,
            detail=f"File '{safe_name}' already exists"
        )

    try:
        with file_path.open("xb") as buffer:  # x = create only if not exists
            shutil.copyfileobj(file.file, buffer)

        return {
            "filename": safe_name,
            "saved_to": str(file_path)
        }

    except FileExistsError:
        # защита от race condition
        raise HTTPException(
            status_code=409,
            detail=f"File '{safe_name}' already exists"
        )
