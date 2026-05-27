from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.core.database import get_db
from app.core.security import require_role
from app.schemas.common import success_response
from app.services import l2_service

router = APIRouter(prefix="/api/v1/l2", tags=["l2"])


class L2UpdateRequest(BaseModel):
    l2_interview_date: Optional[str] = None
    l2_feedback: Optional[str] = None
    l2_recommendation: Optional[str] = None
    l2_status: Optional[str] = None


@router.get("/candidates")
def list_l2_candidates(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    _: object = Depends(require_role("Recruiter", "RecruiterLead", "Admin")),
):
    result = l2_service.list_l2_candidates(db, page, page_size, status)
    return success_response(result)


@router.put("/candidates/{candidate_id}")
def upsert_l2(
    candidate_id: int,
    body: L2UpdateRequest,
    db: Session = Depends(get_db),
    _: object = Depends(require_role("Recruiter", "RecruiterLead", "Admin")),
):
    result = l2_service.upsert_l2_data(candidate_id, body.model_dump(exclude_none=True), db)
    return success_response(result)


@router.get("/aging")
def l2_aging(
    db: Session = Depends(get_db),
    _: object = Depends(require_role("Recruiter", "RecruiterLead", "Admin")),
):
    return success_response(l2_service.get_l2_aging(db))
