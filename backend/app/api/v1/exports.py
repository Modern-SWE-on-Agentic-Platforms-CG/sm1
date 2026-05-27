from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_role
from app.models.employee import EmployeeMaster
from app.schemas.common import success_response
from app.services import document_service

router = APIRouter(prefix="/api/v1/exports", tags=["exports"])


@router.get("/history")
def list_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: EmployeeMaster = Depends(
        require_role("Recruiter", "PMO", "Admin", "RecruiterLead")
    ),
):
    result = document_service.list_export_history(current_user.email_id, db, page, page_size)
    return success_response(result)


@router.delete("/history/{export_id}")
def delete_history(
    export_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(require_role("Recruiter", "PMO", "Admin")),
):
    document_service.delete_export(export_id, db)
    return success_response({"message": "Export deleted"})


@router.get("/{export_id}/download")
def download_export(
    export_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(require_role("Recruiter", "PMO", "Admin", "RecruiterLead")),
):
    return document_service.download_export(export_id, db)
