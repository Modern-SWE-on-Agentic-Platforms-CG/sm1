from __future__ import annotations
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import func

from app.models.referral import (
    ReferralCandidateInfo,
    ReferralCandidateSkill,
    ReferralTechnologyMaster,
    ReferralNoticePeriodMaster,
    ReferralLocationMaster,
)
from app.models.employee import EmployeeMaster


def _serialize_referral(candidate: ReferralCandidateInfo, db: Session) -> dict:
    referee = None
    if candidate.referee_emp_id:
        referee = db.query(EmployeeMaster).filter(EmployeeMaster.emp_id == candidate.referee_emp_id).first()

    return {
        "referral_candidate_id": candidate.id,
        "candidate_name": candidate.candidate_name,
        "email": candidate.candidate_email,
        "phone": candidate.candidate_phone,
        "experience_years": None,
        "current_company": None,
        "current_ctc": None,
        "expected_ctc": None,
        "status": candidate.status,
        "bu": getattr(referee, "bu", None),
        "account": getattr(referee, "account", None),
    }


def list_technologies(db: Session) -> list:
    rows = db.query(ReferralTechnologyMaster).filter(ReferralTechnologyMaster.is_active == True).all()
    return [{"id": r.id, "tech_name": r.tech_name} for r in rows]


def list_notice_periods(db: Session) -> list:
    rows = db.query(ReferralNoticePeriodMaster).all()
    return [{"id": r.id, "notice_period": r.period_label} for r in rows]


def list_locations(db: Session) -> list:
    rows = db.query(ReferralLocationMaster).all()
    return [{"id": r.id, "location_name": r.location_name} for r in rows]


def submit_referral(payload: dict, db: Session) -> ReferralCandidateInfo:
    # Check for duplicate email
    existing = db.query(ReferralCandidateInfo).filter(
        ReferralCandidateInfo.candidate_email == payload.get("email")
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Candidate with this email already referred")

    notice_period = None
    if payload.get("notice_period_id"):
        np = db.query(ReferralNoticePeriodMaster).filter(
            ReferralNoticePeriodMaster.id == payload.get("notice_period_id")
        ).first()
        notice_period = np.period_label if np else None

    location = None
    if payload.get("location_id"):
        loc = db.query(ReferralLocationMaster).filter(
            ReferralLocationMaster.id == payload.get("location_id")
        ).first()
        location = loc.location_name if loc else None

    candidate = ReferralCandidateInfo(
        referee_emp_id=payload.get("referred_by_emp_id"),
        candidate_name=payload.get("candidate_name"),
        candidate_email=payload.get("email"),
        candidate_phone=payload.get("phone"),
        certifications=payload.get("current_company"),
        notice_period=notice_period,
        location=location,
    )
    db.add(candidate)
    db.flush()

    technology_id = payload.get("technology_id")
    if technology_id:
        db.add(ReferralCandidateSkill(referral_id=candidate.id, tech_id=technology_id))

    db.commit()
    db.refresh(candidate)
    return _serialize_referral(candidate, db)


def list_referrals(db: Session, page: int = 1, page_size: int = 20, bu: str | None = None, account: str | None = None) -> dict:
    query = db.query(ReferralCandidateInfo, EmployeeMaster).outerjoin(
        EmployeeMaster, EmployeeMaster.emp_id == ReferralCandidateInfo.referee_emp_id
    )
    if bu:
        query = query.filter(EmployeeMaster.bu == bu)
    if account:
        query = query.filter(EmployeeMaster.account == account)
    total = query.count()
    rows = query.order_by(ReferralCandidateInfo.id.desc()).offset((page - 1) * page_size).limit(page_size).all()
    items = []
    for candidate, referee in rows:
        item = _serialize_referral(candidate, db)
        item["bu"] = getattr(referee, "bu", None)
        item["account"] = getattr(referee, "account", None)
        items.append(item)
    return {"items": items, "total": total, "page": page, "page_size": page_size}


def get_referral(referral_id: int, db: Session) -> ReferralCandidateInfo:
    record = db.query(ReferralCandidateInfo).filter(
        ReferralCandidateInfo.id == referral_id
    ).first()
    if not record:
        raise HTTPException(status_code=404, detail="Referral not found")
    return _serialize_referral(record, db)


def update_referral_status(referral_id: int, status: str, db: Session) -> ReferralCandidateInfo:
    record = get_referral(referral_id, db)

    db_record = db.query(ReferralCandidateInfo).filter(ReferralCandidateInfo.id == referral_id).first()
    if not db_record:
        raise HTTPException(status_code=404, detail="Referral not found")
    db_record.status = status
    db.commit()
    db.refresh(db_record)
    return _serialize_referral(db_record, db)


def reports_by_bu(db: Session) -> list[dict]:
    rows = (
        db.query(EmployeeMaster.bu.label("bu"), func.count(ReferralCandidateInfo.id).label("count"))
        .select_from(ReferralCandidateInfo)
        .outerjoin(EmployeeMaster, EmployeeMaster.emp_id == ReferralCandidateInfo.referee_emp_id)
        .group_by(EmployeeMaster.bu)
        .all()
    )
    return [{"bu": r.bu or "Unknown", "count": r.count} for r in rows]


def reports_by_account(db: Session) -> list[dict]:
    rows = (
        db.query(EmployeeMaster.account.label("account"), func.count(ReferralCandidateInfo.id).label("count"))
        .select_from(ReferralCandidateInfo)
        .outerjoin(EmployeeMaster, EmployeeMaster.emp_id == ReferralCandidateInfo.referee_emp_id)
        .group_by(EmployeeMaster.account)
        .all()
    )
    return [{"account": r.account or "Unknown", "count": r.count} for r in rows]
