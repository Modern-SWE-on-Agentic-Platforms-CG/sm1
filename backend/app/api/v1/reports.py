from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_role
from app.schemas.common import success_response
from app.services import reports_service, analytics_service

router = APIRouter(prefix="/api/v1/reports", tags=["reports"])


@router.get("/offer-approve-candidates")
def offer_approve_candidates(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    bu: str | None = Query(None),
    db: Session = Depends(get_db),
    _: object = Depends(require_role("PMO", "Admin", "RecruiterLead")),
):
    result = reports_service.offer_approve_candidates(db, page, page_size, bu)
    return success_response(result)


@router.get("/feedback-form-report")
def feedback_form_report(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    bu: str | None = Query(None),
    db: Session = Depends(get_db),
    _: object = Depends(require_role("PMO", "Admin", "RecruiterLead", "Interviewer")),
):
    result = reports_service.feedback_form_report(db, page, page_size, bu)
    return success_response(result)


# ── Analytics endpoints ──────────────────────────────────────────────────────

@router.get("/analytics/summary")
def analytics_summary(bu: str | None = None, db: Session = Depends(get_db),
                       _: object = Depends(require_role("Admin", "RecruiterLead", "PMO"))):
    return success_response(analytics_service.get_summary(db, bu))


@router.get("/analytics/status-pie")
def status_pie(bu: str | None = None, db: Session = Depends(get_db),
               _: object = Depends(require_role("Admin", "RecruiterLead", "PMO"))):
    return success_response(analytics_service.get_status_pie(db, bu))


@router.get("/analytics/source-pie")
def source_pie(bu: str | None = None, db: Session = Depends(get_db),
               _: object = Depends(require_role("Admin", "RecruiterLead", "PMO"))):
    return success_response(analytics_service.get_source_pie(db, bu))


@router.get("/analytics/channel-pie")
def channel_pie(bu: str | None = None, db: Session = Depends(get_db),
                _: object = Depends(require_role("Admin", "RecruiterLead", "PMO"))):
    return success_response(analytics_service.get_channel_pie(db, bu))


@router.get("/analytics/interview-line")
def interview_line(days: int = 30, bu: str | None = None, db: Session = Depends(get_db),
                   _: object = Depends(require_role("Admin", "RecruiterLead", "PMO"))):
    return success_response(analytics_service.get_interview_line(db, days, bu))


@router.get("/analytics/trend")
def trend_chart(months: int = 6, bu: str | None = None, db: Session = Depends(get_db),
                _: object = Depends(require_role("Admin", "RecruiterLead", "PMO"))):
    return success_response(analytics_service.get_trend_chart(db, months, bu))


@router.get("/analytics/rejection-reasons")
def rejection_reasons(bu: str | None = None, db: Session = Depends(get_db),
                      _: object = Depends(require_role("Admin", "RecruiterLead", "PMO"))):
    return success_response(analytics_service.get_rejection_reasons(db, bu))


@router.get("/analytics/arc-deviations")
def arc_deviations(threshold: float = 15.0, db: Session = Depends(get_db),
                   _: object = Depends(require_role("Admin", "RecruiterLead"))):
    return success_response(analytics_service.get_arc_deviations(db, threshold))


@router.get("/analytics/interview-data")
def interview_data(page: int = 1, page_size: int = 20, bu: str | None = None,
                   db: Session = Depends(get_db),
                   _: object = Depends(require_role("Admin", "RecruiterLead", "PMO", "Interviewer"))):
    result = analytics_service.get_interview_data(db, page, page_size, bu)
    return success_response(result)

