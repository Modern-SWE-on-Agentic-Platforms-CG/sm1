from __future__ import annotations
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.supply import DemandBatch, DemandData, BenchBatch, BenchData


def create_demand_batch(name: str, created_by: str, db: Session) -> DemandBatch:
    # Current model stores uploader metadata only.
    batch = DemandBatch(uploaded_by=created_by)
    db.add(batch)
    db.commit()
    db.refresh(batch)
    return batch


def list_demand_batches(db: Session) -> list:
    return db.query(DemandBatch).order_by(DemandBatch.id.desc()).all()


def list_demand_data(db: Session, batch_id: int | None = None, page: int = 1, page_size: int = 20) -> dict:
    query = db.query(DemandData)
    if batch_id:
        query = query.filter(DemandData.batch_id == batch_id)
    total = query.count()
    items = query.order_by(DemandData.id.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return {"items": items, "total": total, "page": page, "page_size": page_size}


def create_demand_record(payload: dict, db: Session) -> DemandData:
    # Accept legacy/front-end payload keys and map to current ORM fields.
    mapped = {
        "batch_id": payload.get("batch_id"),
        "jr_id": payload.get("jr_id") or payload.get("role_name"),
        "skill": payload.get("skill") or payload.get("technology"),
        "account": payload.get("account"),
        "bu": payload.get("bu"),
        "demand_date": payload.get("demand_date") or payload.get("target_date"),
        "pipeline_count": payload.get("pipeline_count") or payload.get("headcount") or 0,
    }
    # Remove optional Nones to keep SQLAlchemy defaults intact.
    clean_mapped = {k: v for k, v in mapped.items() if v is not None}
    record = DemandData(**clean_mapped)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def list_bench_data(db: Session, batch_id: int | None = None, page: int = 1, page_size: int = 20) -> dict:
    query = db.query(BenchData)
    if batch_id:
        query = query.filter(BenchData.batch_id == batch_id)
    total = query.count()
    items = query.order_by(BenchData.id.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return {"items": items, "total": total, "page": page, "page_size": page_size}


def create_bench_record(payload: dict, db: Session) -> BenchData:
    mapped = {
        "batch_id": payload.get("batch_id"),
        "emp_name": payload.get("emp_name"),
        "emp_email": payload.get("emp_email"),
        "skill": payload.get("skill") or payload.get("technology"),
        "location": payload.get("location"),
        "bu": payload.get("bu"),
    }
    clean_mapped = {k: v for k, v in mapped.items() if v is not None}
    record = BenchData(**clean_mapped)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_summary(db: Session) -> dict:
    # Use model-native fields: demand approximated by sourced + pipeline counts.
    total_demand = (
        db.query(func.sum(DemandData.sourced_count + DemandData.pipeline_count)).scalar() or 0
    )
    total_bench = db.query(func.count(BenchData.id)).scalar() or 0
    demand_techs = {
        r.skill for r in db.query(DemandData.skill).filter(DemandData.skill.isnot(None)).all()
    }
    bench_matching = (
        db.query(func.count(BenchData.id)).filter(BenchData.skill.in_(demand_techs)).scalar() or 0
    )
    return {
        "total_demand": int(total_demand),
        "total_bench": int(total_bench),
        "matched": int(bench_matching),
        "gap": max(0, int(total_demand) - int(bench_matching)),
    }
