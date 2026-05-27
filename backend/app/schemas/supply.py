from pydantic import BaseModel
from typing import Optional
from datetime import date


class DemandDataCreate(BaseModel):
    batch_id: Optional[int] = None
    role_name: str
    bu: Optional[str] = None
    account: Optional[str] = None
    location: Optional[str] = None
    technology: Optional[str] = None
    headcount: Optional[int] = None
    target_date: Optional[date] = None
    priority: Optional[str] = None


class DemandDataOut(BaseModel):
    demand_id: int
    batch_id: Optional[int] = None
    role_name: str
    bu: Optional[str] = None
    account: Optional[str] = None
    location: Optional[str] = None
    technology: Optional[str] = None
    headcount: Optional[int] = None
    target_date: Optional[date] = None
    priority: Optional[str] = None
    model_config = {"from_attributes": True}


class BenchDataCreate(BaseModel):
    batch_id: Optional[int] = None
    emp_id: Optional[int] = None
    emp_name: str
    technology: Optional[str] = None
    experience_years: Optional[float] = None
    location: Optional[str] = None
    bu: Optional[str] = None
    available_from: Optional[date] = None


class BenchDataOut(BaseModel):
    bench_id: int
    emp_id: Optional[int] = None
    emp_name: str
    technology: Optional[str] = None
    experience_years: Optional[float] = None
    location: Optional[str] = None
    bu: Optional[str] = None
    available_from: Optional[date] = None
    model_config = {"from_attributes": True}


class SupplyDemandSummary(BaseModel):
    total_demand: int
    total_bench: int
    matched: int
    gap: int
