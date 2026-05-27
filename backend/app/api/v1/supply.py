from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.core.database import get_db
from app.core.security import require_role
from app.schemas.common import success_response
from app.schemas.supply import DemandDataCreate, BenchDataCreate
from app.services import supply_service

router = APIRouter(prefix="/api/v1/supply", tags=["supply"])


@router.get("/demand")
def list_demand(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    batch_id: Optional[int] = None,
    db: Session = Depends(get_db),
    _: object = Depends(require_role("PMO", "Admin", "RecruiterLead")),
):
    return success_response(supply_service.list_demand_data(db, batch_id, page, page_size))


@router.post("/demand", status_code=201)
def create_demand(
    body: DemandDataCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_role("PMO", "Admin")),
):
    return success_response(supply_service.create_demand_record(body.model_dump(exclude_none=True), db))


@router.get("/bench")
def list_bench(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    batch_id: Optional[int] = None,
    db: Session = Depends(get_db),
    _: object = Depends(require_role("PMO", "Admin", "RecruiterLead")),
):
    return success_response(supply_service.list_bench_data(db, batch_id, page, page_size))


@router.post("/bench", status_code=201)
def create_bench(
    body: BenchDataCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_role("PMO", "Admin")),
):
    return success_response(supply_service.create_bench_record(body.model_dump(exclude_none=True), db))


@router.get("/summary")
def supply_summary(
    db: Session = Depends(get_db),
    _: object = Depends(require_role("PMO", "Admin", "RecruiterLead")),
):
    return success_response(supply_service.get_summary(db))


@router.get("/demand-batches")
def list_demand_batches(
    db: Session = Depends(get_db),
    _: object = Depends(require_role("PMO", "Admin", "RecruiterLead")),
):
    return success_response(supply_service.list_demand_batches(db))
