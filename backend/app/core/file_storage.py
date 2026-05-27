import os
import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException

from app.core.config import settings

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


def _safe_subdir(subfolder: str) -> Path:
    """Resolve upload subdirectory and guard against path traversal."""
    base = Path(settings.UPLOAD_DIR).resolve()
    target = (base / subfolder).resolve()
    if not str(target).startswith(str(base)):
        raise HTTPException(status_code=400, detail="Invalid upload path")
    target.mkdir(parents=True, exist_ok=True)
    return target


async def save_file(file: UploadFile, subfolder: str) -> str:
    """Save an uploaded file; enforce 5 MB limit. Returns stored filename."""
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum allowed size is {MAX_FILE_SIZE // (1024*1024)} MB.",
        )
    target_dir = _safe_subdir(subfolder)
    ext = Path(file.filename or "file").suffix
    stored_name = f"{uuid.uuid4()}{ext}"
    target_path = target_dir / stored_name
    target_path.write_bytes(content)
    return stored_name


def get_file_path(subfolder: str, filename: str) -> Path:
    """Return absolute path for a stored file; guard against traversal."""
    base = Path(settings.UPLOAD_DIR).resolve()
    target = (base / subfolder / filename).resolve()
    if not str(target).startswith(str(base)):
        raise HTTPException(status_code=400, detail="Invalid file path")
    if not target.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return target


def generate_export_path(report_type: str) -> Path:
    """Return a timestamped path for a generated export file."""
    import datetime
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
    filename = f"{report_type}_{timestamp}.xlsx"
    target_dir = _safe_subdir("exports")
    return target_dir / filename
