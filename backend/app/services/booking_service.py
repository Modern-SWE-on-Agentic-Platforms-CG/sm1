import uuid
import logging
from datetime import date, datetime, timezone
from pathlib import Path

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.interview import RecruiterCalendar, InterviewerCalendar
from app.models.candidate import CandidateDetail
from app.schemas.booking import BookingCreate, DirectBookingCreate, RescheduleRequest
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


def _write_email_log(subject: str, to_email: str, body: str) -> None:
    log_path = Path("backend/logs/email.log")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    entry = (
        f"[{datetime.now(timezone.utc).isoformat()}] "
        f"TO={to_email} SUBJECT={subject}\n{body}\n---\n"
    )
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(entry)

    if settings.SMTP_ENABLED:
        import smtplib
        from email.message import EmailMessage
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = settings.SMTP_FROM
        msg["To"] = to_email
        msg.set_content(body)
        try:
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as s:
                s.send_message(msg)
        except Exception as exc:
            logger.warning(f"SMTP send failed: {exc}")


def search_available_slots(
    skill_id: int | None,
    interview_date: date | None,
    db: Session,
) -> list[InterviewerCalendar]:
    query = db.query(InterviewerCalendar).filter(
        InterviewerCalendar.slot_status == "Available"
    )
    if skill_id:
        query = query.filter(InterviewerCalendar.skill_id == skill_id)
    if interview_date:
        query = query.filter(InterviewerCalendar.slot_date == interview_date)
    return query.all()


def book_slot(data: BookingCreate, booked_by: str, db: Session) -> RecruiterCalendar:
    slot = db.query(InterviewerCalendar).filter(
        InterviewerCalendar.interviewer_calendar_id == data.interviewer_calendar_id
    ).first()
    if not slot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Slot not found")
    if slot.slot_status != "Available":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Slot is not available")

    candidate = db.query(CandidateDetail).filter(
        CandidateDetail.candidate_detail_id == data.candidate_detail_id
    ).first()
    if not candidate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found")

    meeting_link = f"https://meet.smartrecruit.local/{uuid.uuid4()}"

    booking = RecruiterCalendar(
        candidate_detail_id=data.candidate_detail_id,
        interviewer_calendar_id=data.interviewer_calendar_id,
        interview_date=slot.slot_date,
        from_time=slot.from_time,
        to_time=slot.to_time,
        meeting_link=meeting_link,
        is_direct_booked=False,
        booked_by=booked_by,
    )
    db.add(booking)
    slot.slot_status = "Booked"
    db.commit()
    db.refresh(booking)

    _write_email_log(
        subject=f"Interview Booked — {candidate.candidate_name}",
        to_email=booked_by,
        body=f"Interview scheduled on {slot.slot_date}. Meeting: {meeting_link}",
    )
    return booking


def direct_book(data: DirectBookingCreate, booked_by: str, db: Session) -> RecruiterCalendar:
    candidate = db.query(CandidateDetail).filter(
        CandidateDetail.candidate_detail_id == data.candidate_detail_id
    ).first()
    if not candidate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found")

    meeting_link = f"https://meet.smartrecruit.local/{uuid.uuid4()}"
    booking = RecruiterCalendar(
        candidate_detail_id=data.candidate_detail_id,
        interviewer_calendar_id=None,
        interview_date=data.interview_date,
        from_time=data.from_time,
        to_time=data.to_time,
        meeting_link=meeting_link,
        is_direct_booked=True,
        booked_by=booked_by,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)

    _write_email_log(
        subject=f"Direct Interview Booked — {candidate.candidate_name}",
        to_email=booked_by,
        body=f"Direct booking on {data.interview_date}. Meeting: {meeting_link}",
    )
    return booking


def reschedule_booking(booking_id: int, req: RescheduleRequest, db: Session) -> RecruiterCalendar:
    booking = db.query(RecruiterCalendar).filter(
        RecruiterCalendar.recruiter_calendar_id == booking_id
    ).first()
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

    if req.new_interviewer_calendar_id:
        new_slot = db.query(InterviewerCalendar).filter(
            InterviewerCalendar.interviewer_calendar_id == req.new_interviewer_calendar_id
        ).first()
        if not new_slot or new_slot.slot_status != "Available":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="New slot not available")

        # Release old slot
        if booking.interviewer_calendar_id:
            old_slot = db.query(InterviewerCalendar).filter(
                InterviewerCalendar.interviewer_calendar_id == booking.interviewer_calendar_id
            ).first()
            if old_slot:
                old_slot.slot_status = "Available"

        booking.interviewer_calendar_id = req.new_interviewer_calendar_id
        booking.interview_date = new_slot.slot_date
        booking.from_time = new_slot.from_time
        booking.to_time = new_slot.to_time
        new_slot.slot_status = "Booked"

    if req.new_interview_date:
        booking.interview_date = req.new_interview_date
    if req.new_from_time:
        booking.from_time = req.new_from_time
    if req.new_to_time:
        booking.to_time = req.new_to_time

    db.commit()
    db.refresh(booking)
    return booking


def cancel_booking(booking_id: int, db: Session) -> None:
    booking = db.query(RecruiterCalendar).filter(
        RecruiterCalendar.recruiter_calendar_id == booking_id
    ).first()
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

    if booking.interviewer_calendar_id:
        slot = db.query(InterviewerCalendar).filter(
            InterviewerCalendar.interviewer_calendar_id == booking.interviewer_calendar_id
        ).first()
        if slot:
            slot.slot_status = "Available"

    db.delete(booking)
    db.commit()


def get_todo_list(emp_email: str, db: Session) -> dict:
    today = date.today()
    today_interviews = (
        db.query(RecruiterCalendar)
        .filter(RecruiterCalendar.booked_by == emp_email, RecruiterCalendar.interview_date == today)
        .all()
    )
    pending_feedbacks = (
        db.query(RecruiterCalendar)
        .filter(
            RecruiterCalendar.booked_by == emp_email,
            RecruiterCalendar.feedback_submitted == False,  # noqa: E712
            RecruiterCalendar.interview_date < today,
        )
        .all()
    )
    return {"today_interviews": today_interviews, "pending_feedback": pending_feedbacks}


def get_weekly_view(emp_email: str, db: Session) -> list[RecruiterCalendar]:
    from datetime import timedelta
    today = date.today()
    week_end = today + timedelta(days=7)
    return (
        db.query(RecruiterCalendar)
        .filter(
            RecruiterCalendar.booked_by == emp_email,
            RecruiterCalendar.interview_date >= today,
            RecruiterCalendar.interview_date <= week_end,
        )
        .all()
    )


def get_pending_feedbacks(emp_email: str, db: Session) -> list[RecruiterCalendar]:
    today = date.today()
    return (
        db.query(RecruiterCalendar)
        .filter(
            RecruiterCalendar.booked_by == emp_email,
            RecruiterCalendar.feedback_submitted == False,  # noqa: E712
            RecruiterCalendar.interview_date < today,
        )
        .all()
    )
