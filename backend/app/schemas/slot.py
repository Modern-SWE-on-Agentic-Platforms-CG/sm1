from __future__ import annotations
from datetime import datetime, date
from pydantic import BaseModel


class SlotCreate(BaseModel):
    skill_id: int | None = None
    slot_date: date
    from_time: datetime
    to_time: datetime
    is_weekend_drive: bool = False


class SlotOut(BaseModel):
    interviewer_calendar_id: int
    emp_id: int
    skill_id: int | None
    slot_date: date
    from_time: datetime
    to_time: datetime
    slot_status: str
    is_weekend_drive: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class SlotListResponse(BaseModel):
    items: list[SlotOut]
    total: int


class BulkSlotUploadResponse(BaseModel):
    created: int
    errors: int
    error_file_url: str | None = None
