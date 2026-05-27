from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.core.database import get_db
from app.core.security import require_role
from app.schemas.common import success_response
from app.schemas.referral import ReferralCandidateCreate
from app.services import referral_service

router = APIRouter(prefix="/api/v1/referral", tags=["referral"])


# ── Public endpoints (no auth — for external referral link) ─────────────────

@router.get("/technologies")
def list_technologies(db: Session = Depends(get_db)):
    return success_response(referral_service.list_technologies(db))


@router.get("/notice-periods")
def list_notice_periods(db: Session = Depends(get_db)):
    return success_response(referral_service.list_notice_periods(db))


@router.get("/locations")
def list_locations(db: Session = Depends(get_db)):
    return success_response(referral_service.list_locations(db))


@router.post("/submit", status_code=201)
def submit_referral(body: ReferralCandidateCreate, db: Session = Depends(get_db)):
    result = referral_service.submit_referral(body.model_dump(), db)
    return success_response(result)


# ── Protected endpoints ──────────────────────────────────────────────────────

@router.get("/candidates")
def list_referrals(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    bu: Optional[str] = None,
    account: Optional[str] = None,
    db: Session = Depends(get_db),
    _: object = Depends(require_role("Recruiter", "RecruiterLead", "Admin", "PMO")),
):
    result = referral_service.list_referrals(db, page, page_size, bu, account)
    return success_response(result)


@router.get("/candidates/{referral_id}")
def get_referral(
    referral_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(require_role("Recruiter", "RecruiterLead", "Admin", "PMO")),
):
    return success_response(referral_service.get_referral(referral_id, db))


@router.patch("/candidates/{referral_id}/status")
def update_status(
    referral_id: int,
    status: str,
    db: Session = Depends(get_db),
    _: object = Depends(require_role("Recruiter", "RecruiterLead", "Admin")),
):
    result = referral_service.update_referral_status(referral_id, status, db)
    return success_response(result)


@router.get("/reports/by-bu")
def report_by_bu(
    db: Session = Depends(get_db),
    _: object = Depends(require_role("Recruiter", "RecruiterLead", "Admin", "PMO")),
):
    return success_response(referral_service.reports_by_bu(db))


@router.get("/reports/by-account")
def report_by_account(
    db: Session = Depends(get_db),
    _: object = Depends(require_role("Recruiter", "RecruiterLead", "Admin", "PMO")),
):
    return success_response(referral_service.reports_by_account(db))
