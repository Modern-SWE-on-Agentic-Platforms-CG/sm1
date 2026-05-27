from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, EmailStr


class EmployeeCreate(BaseModel):
    emp_name: str
    email_id: EmailStr
    password: str
    location: str | None = None
    grade: str | None = None
    bu: str | None = None
    practice: str | None = None
    market_unit: str | None = None
    account: str | None = None
    organisation: str | None = None
    role_ids: list[int] = []
    technology_ids: list[int] = []
    tower_names: list[str] = []


class EmployeeUpdate(BaseModel):
    emp_name: str | None = None
    location: str | None = None
    grade: str | None = None
    bu: str | None = None
    practice: str | None = None
    market_unit: str | None = None
    account: str | None = None
    organisation: str | None = None
    role_ids: list[int] | None = None
    technology_ids: list[int] | None = None
    tower_names: list[str] | None = None
    is_active: bool | None = None


class EmployeeOut(BaseModel):
    emp_id: int
    emp_name: str
    email_id: str
    location: str | None
    grade: str | None
    bu: str | None
    practice: str | None
    market_unit: str | None
    account: str | None
    organisation: str | None
    is_active: bool
    created_at: datetime
    roles: list[str] = []
    technologies: list[str] = []
    tower_names: list[str] = []

    model_config = {"from_attributes": True}


class EmployeeListResponse(BaseModel):
    items: list[EmployeeOut]
    total: int
    page: int
    page_size: int
