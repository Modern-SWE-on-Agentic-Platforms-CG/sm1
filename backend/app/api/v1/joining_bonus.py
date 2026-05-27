from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_role
from app.models.employee import EmployeeMaster
from app.schemas.common import success_response
from app.schemas.joining_bonus import JoiningBonusUpdate
from app.services import joining_bonus_service

router = APIRouter(prefix="/api/v1/joining-bonus", tags=["joining-bonus"])


@router.get("")
def list_jb(
    status: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: object = Depends(require_role("RecruiterLead", "Admin")),
):
    result = joining_bonus_service.list_jb_candidates(db, status, page, page_size)
    return success_response(result)


@router.get("/bu")
def list_jb_by_bu(
    bu: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: object = Depends(require_role("RecruiterLead", "Admin", "BUAdmin", "PracticeAdmin")),
):
    result = joining_bonus_service.list_jb_by_bu(bu, db, page, page_size)
    return success_response(result)


@router.put("/{jb_id}")
def update_jb(
    jb_id: int,
    body: JoiningBonusUpdate,
    db: Session = Depends(get_db),
    current_user: EmployeeMaster = Depends(require_role("RecruiterLead", "Admin", "BUAdmin")),
):
    jb = joining_bonus_service.update_jb_status(jb_id, body, current_user.email_id, db)
    return success_response({"id": jb.id, "status": jb.status, "updated_by": jb.updated_by})


@router.get("/dl-options")
def dl_options(
    db: Session = Depends(get_db),
    _: object = Depends(require_role("RecruiterLead", "Admin")),
):
    items = joining_bonus_service.get_dl_options(db)
    return success_response({"items": items})
