from __future__ import annotations
from datetime import datetime, date
from pydantic import BaseModel


class BookingCreate(BaseModel):
    candidate_detail_id: int
    interviewer_calendar_id: int


class DirectBookingCreate(BaseModel):
    candidate_detail_id: int
    interview_date: date
    from_time: datetime
    to_time: datetime
    panel_email: str | None = None
    skill_id: int | None = None


class BookingOut(BaseModel):
    recruiter_calendar_id: int
    candidate_detail_id: int
    interviewer_calendar_id: int | None
    interview_date: date | None
    meeting_link: str | None
    is_direct_booked: bool
    feedback_submitted: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class RescheduleRequest(BaseModel):
    new_interviewer_calendar_id: int | None = None
    new_interview_date: date | None = None
    new_from_time: datetime | None = None
    new_to_time: datetime | None = None


class TodoListResponse(BaseModel):
    today_interviews: list[BookingOut]
    pending_feedback: list[BookingOut]
