from __future__ import annotations
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.supply import DemandBatch, DemandData, BenchBatch, BenchData


def create_demand_batch(name: str, created_by: str, db: Session) -> DemandBatch:
    batch = DemandBatch(batch_name=name, created_by=created_by)
    db.add(batch)
    db.commit()
    db.refresh(batch)
    return batch


def list_demand_batches(db: Session) -> list:
    return db.query(DemandBatch).order_by(DemandBatch.batch_id.desc()).all()


def list_demand_data(db: Session, batch_id: int | None = None, page: int = 1, page_size: int = 20) -> dict:
    query = db.query(DemandData)
    if batch_id:
        query = query.filter(DemandData.batch_id == batch_id)
    total = query.count()
    items = query.order_by(DemandData.demand_id.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return {"items": items, "total": total, "page": page, "page_size": page_size}


def create_demand_record(payload: dict, db: Session) -> DemandData:
    record = DemandData(**payload)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def list_bench_data(db: Session, batch_id: int | None = None, page: int = 1, page_size: int = 20) -> dict:
    query = db.query(BenchData)
    if batch_id:
        query = query.filter(BenchData.batch_id == batch_id)
    total = query.count()
    items = query.order_by(BenchData.bench_id.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return {"items": items, "total": total, "page": page, "page_size": page_size}


def create_bench_record(payload: dict, db: Session) -> BenchData:
    record = BenchData(**payload)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_summary(db: Session) -> dict:
    total_demand = db.query(func.sum(DemandData.headcount)).scalar() or 0
    total_bench = db.query(func.count(BenchData.bench_id)).scalar() or 0
    # Simple tech-based matching
    demand_techs = {r.technology for r in db.query(DemandData.technology).filter(DemandData.technology.isnot(None)).all()}
    bench_matching = db.query(func.count(BenchData.bench_id)).filter(BenchData.technology.in_(demand_techs)).scalar() or 0
    return {
        "total_demand": int(total_demand),
        "total_bench": int(total_bench),
        "matched": int(bench_matching),
        "gap": max(0, int(total_demand) - int(bench_matching)),
    }
