from __future__ import annotations
from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, extract, case

from app.models.candidate import CandidateDetail
from app.models.interview import RecruiterCalendar
from app.models.feedback import OverallFeedback
from app.models.workflow import OfferWorkflow


def get_status_pie(db: Session, bu: str | None = None) -> list[dict]:
    query = db.query(CandidateDetail.overall_status, func.count().label('count')).group_by(CandidateDetail.overall_status)
    if bu:
        query = query.filter(CandidateDetail.bu_id == bu)
    rows = query.all()
    return [{"name": r.overall_status or "Unknown", "value": r.count} for r in rows]


def get_source_pie(db: Session, bu: str | None = None) -> list[dict]:
    query = db.query(CandidateDetail.source, func.count().label('count')).group_by(CandidateDetail.source)
    if bu:
        query = query.filter(CandidateDetail.bu_id == bu)
    rows = query.filter(CandidateDetail.source.isnot(None)).all()
    return [{"name": r.source, "value": r.count} for r in rows]


def get_channel_pie(db: Session, bu: str | None = None) -> list[dict]:
    # Use 'source' as channel proxy since there's no dedicated channel column
    query = db.query(CandidateDetail.source, func.count().label('count')).group_by(CandidateDetail.source)
    if bu:
        query = query.filter(CandidateDetail.bu_id == bu)
    rows = query.filter(CandidateDetail.source.isnot(None)).all()
    return [{"name": r.source, "value": r.count} for r in rows]


def get_interview_line(db: Session, days: int = 30, bu: str | None = None) -> list[dict]:
    since = date.today() - timedelta(days=days)
    query = db.query(RecruiterCalendar.interview_date, func.count().label('count')).filter(
        RecruiterCalendar.interview_date >= since
    ).group_by(RecruiterCalendar.interview_date).order_by(RecruiterCalendar.interview_date)
    rows = query.all()
    return [{"date": str(r.interview_date), "count": r.count} for r in rows]


def get_trend_chart(db: Session, months: int = 6, bu: str | None = None) -> list[dict]:
    query = db.query(
        extract('year', CandidateDetail.created_at).label('yr'),
        extract('month', CandidateDetail.created_at).label('mo'),
        func.count().label('pipeline'),
        func.sum(
            case(
                (CandidateDetail.overall_status.in_(["Offer Accepted", "Joined"]), 1),
                else_=0
            )
        ).label('hired'),
    )
    if bu:
        query = query.filter(CandidateDetail.bu_id == bu)
    rows = query.group_by('yr', 'mo').order_by('yr', 'mo').limit(months).all()
    result = []
    for r in rows:
        result.append({"month": f"{int(r.yr)}-{int(r.mo):02d}", "pipeline": r.pipeline, "hired": int(r.hired or 0)})
    return result


def get_rejection_reasons(db: Session, bu: str | None = None) -> list[dict]:
    # Use dashboard_status as proxy since there's no dedicated reject_reason column
    query = db.query(CandidateDetail.dashboard_status, func.count().label('count')).filter(
        CandidateDetail.dashboard_status.isnot(None),
        CandidateDetail.overall_status.in_(["Rejected", "L1 Rejected", "L2 Rejected"])
    ).group_by(CandidateDetail.dashboard_status)
    if bu:
        query = query.filter(CandidateDetail.bu_id == bu)
    rows = query.all()
    return [{"reason": r.dashboard_status, "count": r.count} for r in rows]


def get_arc_deviations(db: Session, threshold_pct: float = 15.0) -> list[dict]:
    # OfferWorkflow does not store CTC fields; return empty until data is available
    return []


def get_interview_data(db: Session, page: int = 1, page_size: int = 20, bu: str | None = None) -> dict:
    query = (
        db.query(RecruiterCalendar)
        .join(CandidateDetail, RecruiterCalendar.candidate_detail_id == CandidateDetail.candidate_detail_id, isouter=True)
    )
    if bu:
        query = query.filter(CandidateDetail.bu_id == bu)
    total = query.count()
    rows = query.order_by(RecruiterCalendar.interview_date.desc()).offset((page - 1) * page_size).limit(page_size).all()
    items = [
        {
            "recruiter_calendar_id": r.recruiter_calendar_id,
            "candidate_detail_id": r.candidate_detail_id,
            "interview_date": str(r.interview_date) if r.interview_date else None,
            "interview_from_time": r.from_time.isoformat() if r.from_time else None,
            "interview_to_time": r.to_time.isoformat() if r.to_time else None,
            "interview_type": r.interview_type,
            "feedback_submitted": r.feedback_submitted,
        }
        for r in rows
    ]
    return {"items": items, "total": total, "page": page, "page_size": page_size}


def get_summary(db: Session, bu: str | None = None) -> dict:
    q = db.query(CandidateDetail)
    if bu:
        q = q.filter(CandidateDetail.bu_id == bu)
    total = q.count()
    offers = q.filter(CandidateDetail.overall_status.in_(["Offer Approved", "Offer Released", "Offer Accepted"])).count()
    joinings = q.filter(CandidateDetail.overall_status == "Joined").count()
    pending_fb = db.query(RecruiterCalendar).filter(
        ~RecruiterCalendar.recruiter_calendar_id.in_(
            db.query(OverallFeedback.recruiter_calendar_id)
        )
    ).count()
    return {"total_candidates": total, "total_offers": offers, "total_joinings": joinings, "pending_feedback": pending_fb}
