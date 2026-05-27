from __future__ import annotations
from datetime import datetime, timedelta, timezone
from pathlib import Path

from fastapi import HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.models.candidate import CandidateDetail, CandidateComments
from app.models.master_data import ExportHistory
from app.core.logging import get_logger

logger = get_logger(__name__)


def download_resume(candidate_id: int, db: Session) -> FileResponse:
    candidate = db.query(CandidateDetail).filter(
        CandidateDetail.candidate_detail_id == candidate_id
    ).first()
    if not candidate or not candidate.resume_path:
        raise HTTPException(status_code=404, detail="Resume not found")
    path = Path(candidate.resume_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Resume file missing from storage")
    return FileResponse(
        str(path),
        media_type="application/octet-stream",
        filename=path.name,
        headers={"Content-Disposition": f'attachment; filename="{path.name}"'},
    )


def download_attachment(candidate_id: int, comment_id: int, db: Session) -> FileResponse:
    comment = db.query(CandidateComments).filter(
        CandidateComments.id == comment_id,
        CandidateComments.candidate_detail_id == candidate_id,
    ).first()
    if not comment or not comment.attachment_path:
        raise HTTPException(status_code=404, detail="Attachment not found")
    path = Path(comment.attachment_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Attachment file missing from storage")
    filename = comment.attachment_filename or path.name
    return FileResponse(
        str(path),
        media_type="application/octet-stream",
        filename=filename,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


def list_export_history(created_by: str, db: Session, page: int = 1, page_size: int = 20) -> dict:
    query = db.query(ExportHistory).filter(
        ExportHistory.created_by == created_by,
        ExportHistory.is_deleted == False,
    ).order_by(ExportHistory.created_at.desc())
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return {"items": items, "total": total, "page": page, "page_size": page_size}


def delete_export(export_id: int, db: Session) -> None:
    record = db.query(ExportHistory).filter(ExportHistory.id == export_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Export not found")
    record.is_deleted = True
    db.commit()


def download_export(export_id: int, db: Session) -> FileResponse:
    record = db.query(ExportHistory).filter(ExportHistory.id == export_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Export not found")
    if record.is_deleted:
        raise HTTPException(status_code=404, detail="Export not found or deleted")
    path = Path(record.file_path)
    if not path.exists():
        raise HTTPException(status_code=410, detail="Export file has been deleted from storage")
    return FileResponse(
        str(path),
        media_type="application/octet-stream",
        filename=path.name,
        headers={"Content-Disposition": f'attachment; filename="{path.name}"'},
    )


def cleanup_old_exports(db: Session) -> int:
    """Delete export records and files older than 7 days."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    old_records = db.query(ExportHistory).filter(
        ExportHistory.created_at < cutoff,
        ExportHistory.is_deleted == False,
    ).all()
    count = 0
    for record in old_records:
        try:
            path = Path(record.file_path)
            if path.exists():
                path.unlink()
        except Exception as exc:
            logger.warning(f"Could not delete export file {record.file_path}: {exc}")
        record.is_deleted = True
        count += 1
    if count > 0:
        db.commit()
        logger.info(f"Cleaned up {count} old export records")
    return count
