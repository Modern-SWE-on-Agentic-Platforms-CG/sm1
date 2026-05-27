from __future__ import annotations
from typing import Any
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from app.models.candidate import CandidateDetail, CandidateComments
from app.models.interview import RecruiterCalendar
from app.models.feedback import OverallFeedback, InterviewerFeedbackFormDetails, FeedbackFormTemplate, FeedbackParameter
from app.models.master_data import TechnologyMaster


def offer_approve_candidates(db: Session, page: int = 1, page_size: int = 20, bu: str | None = None) -> dict:
    query = db.query(CandidateDetail).filter(
        CandidateDetail.overall_status.in_(["Offer Approved", "Offer Released", "Offer_Accepted"])
    )
    if bu:
        query = query.filter(CandidateDetail.bu_id == bu)
    total = query.count()
    rows = query.order_by(CandidateDetail.candidate_detail_id.desc()).offset((page - 1) * page_size).limit(page_size).all()
    items = [
        {
            "id": r.candidate_detail_id,
            "candidate_name": r.candidate_name,
            "email_id": r.email_id,
            "bu_id": r.bu_id,
            "overall_status": r.overall_status,
            "offer_ctc": r.offer_ctc,
            "doj": str(r.doj) if r.doj else None,
            "technology": None,
        }
        for r in rows
    ]
    return {"items": items, "total": total, "page": page, "page_size": page_size}


def feedback_form_report(db: Session, page: int = 1, page_size: int = 20, bu: str | None = None) -> dict:
    query = (
        db.query(
            RecruiterCalendar.recruiter_calendar_id,
            RecruiterCalendar.candidate_detail_id,
            RecruiterCalendar.interview_date,
            CandidateDetail.candidate_name,
            TechnologyMaster.tech_name.label("technology"),
            OverallFeedback.rating.label("recommendation"),
            OverallFeedback.remarks.label("overall_score"),
        )
        .join(CandidateDetail, RecruiterCalendar.candidate_detail_id == CandidateDetail.candidate_detail_id, isouter=True)
        .join(TechnologyMaster, CandidateDetail.skill_id == TechnologyMaster.id, isouter=True)
        .join(OverallFeedback, OverallFeedback.recruiter_calendar_id == RecruiterCalendar.recruiter_calendar_id, isouter=True)
    )
    if bu:
        query = query.filter(CandidateDetail.bu_id == bu)
    total = query.count()
    rows = query.order_by(RecruiterCalendar.recruiter_calendar_id.desc()).offset((page - 1) * page_size).limit(page_size).all()
    items = [
        {
            "booking_id": r.recruiter_calendar_id,
            "candidate_id": r.candidate_detail_id,
            "interview_date": str(r.interview_date) if r.interview_date else None,
            "candidate_name": r.candidate_name,
            "technology": r.technology,
            "recommendation": r.recommendation,
            "overall_score": r.overall_score,
        }
        for r in rows
    ]
    return {"items": items, "total": total, "page": page, "page_size": page_size}
