from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_role
from app.schemas.booking import BookingCreate, DirectBookingCreate, RescheduleRequest
from app.schemas.common import success_response
from app.services import booking_service
from app.models.employee import EmployeeMaster

router = APIRouter(prefix="/api/v1/bookings", tags=["bookings"])


@router.get("/available-slots")
def get_available_slots(
    skill_id: int | None = None,
    interview_date: date | None = None,
    db: Session = Depends(get_db),
    _: object = Depends(require_role("Recruiter", "PMO", "Admin")),
):
    slots = booking_service.search_available_slots(skill_id, interview_date, db)
    return success_response({"items": slots, "total": len(slots)})


@router.post("", status_code=201)
def book_slot(
    body: BookingCreate,
    db: Session = Depends(get_db),
    current_user: EmployeeMaster = Depends(require_role("Recruiter", "PMO", "Admin")),
):
    booking = booking_service.book_slot(body, current_user.email_id, db)
    return success_response(booking)


@router.post("/direct", status_code=201)
def direct_book(
    body: DirectBookingCreate,
    db: Session = Depends(get_db),
    current_user: EmployeeMaster = Depends(require_role("Recruiter", "PMO", "Admin")),
):
    booking = booking_service.direct_book(body, current_user.email_id, db)
    return success_response(booking)


@router.put("/{booking_id}/reschedule")
def reschedule(
    booking_id: int,
    body: RescheduleRequest,
    db: Session = Depends(get_db),
    _: object = Depends(require_role("Recruiter", "PMO", "Admin")),
):
    booking = booking_service.reschedule_booking(booking_id, body, db)
    return success_response(booking)


@router.delete("/{booking_id}", status_code=204)
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(require_role("Recruiter", "PMO", "Admin")),
):
    booking_service.cancel_booking(booking_id, db)


@router.get("/todo")
def get_todo(
    db: Session = Depends(get_db),
    current_user: EmployeeMaster = Depends(require_role("Recruiter", "PMO", "Interviewer")),
):
    result = booking_service.get_todo_list(current_user.email_id, db)
    return success_response(result)


@router.get("/weekly")
def get_weekly(
    db: Session = Depends(get_db),
    current_user: EmployeeMaster = Depends(require_role("Recruiter", "PMO", "Interviewer")),
):
    bookings = booking_service.get_weekly_view(current_user.email_id, db)
    return success_response({"items": bookings, "total": len(bookings)})


@router.get("/pending-feedback")
def get_pending_feedback(
    db: Session = Depends(get_db),
    current_user: EmployeeMaster = Depends(require_role("Recruiter", "PMO", "Interviewer")),
):
    bookings = booking_service.get_pending_feedbacks(current_user.email_id, db)
    return success_response({"items": bookings, "total": len(bookings)})
