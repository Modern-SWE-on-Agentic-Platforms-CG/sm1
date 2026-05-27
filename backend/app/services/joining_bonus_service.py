from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.workflow import JoiningBonus
from app.models.candidate import CandidateDetail
from app.models.master_data import ApproverDLMapping
from app.schemas.joining_bonus import JoiningBonusUpdate
from app.core.logging import get_logger

logger = get_logger(__name__)


def list_jb_candidates(db: Session, status: str | None = None, page: int = 1, page_size: int = 20) -> dict:
    query = db.query(JoiningBonus, CandidateDetail).join(
        CandidateDetail,
        JoiningBonus.candidate_detail_id == CandidateDetail.candidate_detail_id,
    )
    if status:
        query = query.filter(JoiningBonus.status == status)
    total = query.count()
    rows = query.offset((page - 1) * page_size).limit(page_size).all()
    items = []
    for jb, cand in rows:
        items.append({
            "id": jb.id,
            "candidate_detail_id": jb.candidate_detail_id,
            "candidate_name": cand.candidate_name,
            "bonus_amount": jb.bonus_amount,
            "status": jb.status,
            "dl_email": jb.dl_email,
            "updated_by": jb.updated_by,
            "updated_at": jb.updated_at,
        })
    return {"items": items, "total": total, "page": page, "page_size": page_size}


def list_jb_by_bu(bu: str | None, db: Session, page: int = 1, page_size: int = 20) -> dict:
    query = db.query(JoiningBonus, CandidateDetail).join(
        CandidateDetail,
        JoiningBonus.candidate_detail_id == CandidateDetail.candidate_detail_id,
    )
    if bu:
        from sqlalchemy import cast
        query = query.filter(CandidateDetail.tower == bu)
    total = query.count()
    rows = query.offset((page - 1) * page_size).limit(page_size).all()
    items = []
    for jb, cand in rows:
        items.append({
            "id": jb.id,
            "candidate_detail_id": jb.candidate_detail_id,
            "candidate_name": cand.candidate_name,
            "bonus_amount": jb.bonus_amount,
            "status": jb.status,
            "dl_email": jb.dl_email,
        })
    return {"items": items, "total": total, "page": page, "page_size": page_size}


def update_jb_status(jb_id: int, data: JoiningBonusUpdate, updated_by: str, db: Session) -> JoiningBonus:
    jb = db.query(JoiningBonus).filter(JoiningBonus.id == jb_id).first()
    if not jb:
        raise HTTPException(status_code=404, detail="Joining bonus record not found")
    jb.status = data.status
    if data.dl_email is not None:
        jb.dl_email = data.dl_email
    jb.updated_by = updated_by
    db.commit()
    db.refresh(jb)
    return jb


def get_dl_options(db: Session) -> list:
    return db.query(ApproverDLMapping).all()
