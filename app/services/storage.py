"""
Сервис работы с файловым хранилищем. Вся логика путей и FS вынесена сюда.
"""
import shutil
from datetime import datetime
from pathlib import Path


def list_files(upload_dir: Path, limit: int | None = None) -> list[dict]:
    """Список файлов в директории. limit — макс. количество записей."""
    files_data = []
    for f in upload_dir.iterdir():
        if f.is_file():
            stat = f.stat()
            files_data.append({
                "name": f.name,
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            })
    files_data.sort(key=lambda x: x["name"])
    if limit is not None:
        files_data = files_data[:limit]
    return files_data


def get_file_path(upload_dir: Path, filename: str) -> Path:
    """Безопасный путь к файлу (без path traversal)."""
    safe_name = Path(filename).name
    return upload_dir / safe_name


def save_upload(upload_dir: Path, filename: str, source) -> Path:
    """
    Сохраняет содержимое source в upload_dir/filename.
    Создаёт только если файл не существует (xb).
    Raises FileExistsError если файл уже есть.
    """
    path = get_file_path(upload_dir, filename)
    with path.open("xb") as buffer:
        shutil.copyfileobj(source, buffer)
    return path
