"""
Роуты для списка, загрузки и скачивания файлов.
"""
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, Query, UploadFile
from fastapi.responses import FileResponse

from config import UPLOAD_DIR
from app.services.storage import get_file_path, list_files, save_upload

router = APIRouter(prefix="", tags=["files"])


@router.get("/files")
def get_files(limit: int | None = Query(None, ge=1)):
    """Список файлов в хранилище."""
    return list_files(UPLOAD_DIR, limit=limit)


@router.get("/download/{filename}")
def download_file(filename: str):
    """Скачать файл по имени."""
    file_path = get_file_path(UPLOAD_DIR, filename)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(
        path=file_path,
        filename=file_path.name,
        media_type="application/octet-stream",
    )


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Загрузить файл. 409 если файл с таким именем уже есть."""
    safe_name = Path(file.filename).name
    if not safe_name:
        raise HTTPException(status_code=400, detail="Filename required")
    try:
        path = save_upload(UPLOAD_DIR, safe_name, file.file)
        return {"filename": safe_name, "saved_to": str(path)}
    except FileExistsError:
        raise HTTPException(
            status_code=409,
            detail=f"File '{safe_name}' already exists",
        )
