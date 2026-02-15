"""
Роуты для списка, загрузки и скачивания файлов.
"""
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, Query, UploadFile
from fastapi.responses import FileResponse

from config import UPLOAD_DIR
from app.services.storage import delete_files, get_file_path, list_files, save_upload

router = APIRouter(prefix="", tags=["files"])


@router.get("/files")
def get_files(limit: int | None = Query(None, ge=1)):
    """Список файлов в хранилище."""
    return list_files(UPLOAD_DIR, limit=limit)


def _media_type_for_preview(filename: str) -> str:
    ext = Path(filename).suffix.lower()
    if ext == ".pdf":
        return "application/pdf"
    if ext in (".jpg", ".jpeg"):
        return "image/jpeg"
    if ext == ".png":
        return "image/png"
    if ext == ".gif":
        return "image/gif"
    if ext == ".webp":
        return "image/webp"
    if ext == ".svg":
        return "image/svg+xml"
    if ext == ".bmp":
        return "image/bmp"
    return "application/octet-stream"


@router.get("/download/{filename}")
def download_file(
    filename: str,
    preview: bool = Query(False, description="Отдать файл для отображения в браузере (inline)"),
):
    """Скачать файл по имени. ?preview=1 — отображение в iframe/img без скачивания."""
    file_path = get_file_path(UPLOAD_DIR, filename)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    if preview:
        return FileResponse(
            path=file_path,
            filename=file_path.name,
            media_type=_media_type_for_preview(filename),
            content_disposition_type="inline",
        )
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


@router.delete("/files")
def delete_files_endpoint(names: str = Query(..., description="Имена файлов через запятую")):
    """Удалить файлы по именам (одно или несколько через запятую)."""
    name_list = [n.strip() for n in names.split(",") if n.strip()]
    if not name_list:
        raise HTTPException(status_code=400, detail="At least one filename required")
    deleted = delete_files(UPLOAD_DIR, name_list)
    return {"deleted": deleted}
