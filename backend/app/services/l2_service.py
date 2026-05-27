from __future__ import annotations
from datetime import date
from sqlalchemy.orm import Session

from app.models.l2 import L2SelectData
from app.models.candidate import CandidateDetail
from fastapi import HTTPException


def list_l2_candidates(db: Session, page: int = 1, page_size: int = 20, status: str | None = None) -> dict:
    query = db.query(L2SelectData)
    if status:
        query = query.filter(L2SelectData.l2_status == status)
    total = query.count()
    items = query.order_by(L2SelectData.l2_select_id.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return {"items": items, "total": total, "page": page, "page_size": page_size}


def upsert_l2_data(candidate_id: int, payload: dict, db: Session) -> L2SelectData:
    record = db.query(L2SelectData).filter(L2SelectData.candidate_detail_id == candidate_id).first()
    if not record:
        record = L2SelectData(candidate_detail_id=candidate_id)
        db.add(record)
    for k, v in payload.items():
        if hasattr(record, k) and v is not None:
            setattr(record, k, v)
    db.commit()
    db.refresh(record)
    return record


def get_l2_aging(db: Session) -> list[dict]:
    rows = db.query(L2SelectData, CandidateDetail).join(
        CandidateDetail, L2SelectData.candidate_detail_id == CandidateDetail.candidate_detail_id, isouter=True
    ).filter(L2SelectData.l2_status == "Pending").all()

    result = []
    today = date.today()
    for l2, cand in rows:
        interview_date = l2.l2_interview_date
        aging = (today - interview_date).days if interview_date else None
        result.append({
            "l2_select_id": l2.l2_select_id,
            "candidate_id": l2.candidate_detail_id,
            "candidate_name": cand.candidate_name if cand else None,
            "l2_interview_date": str(interview_date) if interview_date else None,
            "l2_status": l2.l2_status,
            "aging_days": aging,
        })
    return result
