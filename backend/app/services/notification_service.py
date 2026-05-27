"""Notification service — writes to backend/logs/email.log; sends via SMTP if enabled."""
from __future__ import annotations
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date, timedelta
from pathlib import Path

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import SessionLocal

logger = logging.getLogger("notifications")

_email_log_path = Path(__file__).resolve().parent.parent.parent / "logs" / "email.log"
_email_log_path.parent.mkdir(parents=True, exist_ok=True)

_email_file_handler = logging.FileHandler(str(_email_log_path))
_email_file_handler.setLevel(logging.INFO)
logger.addHandler(_email_file_handler)
logger.setLevel(logging.INFO)


def _log_email(to: str, subject: str, body: str) -> None:
    logger.info(f"TO={to} | SUBJECT={subject} | BODY={body[:200]}")


def _send_email(to: str, subject: str, body: str) -> None:
    _log_email(to, subject, body)
    if not getattr(settings, "SMTP_ENABLED", False):
        return
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = settings.SMTP_FROM
        msg["To"] = to
        msg.attach(MIMEText(body, "html"))
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10) as server:
            if getattr(settings, "SMTP_TLS", True):
                server.starttls()
            if settings.SMTP_USER and settings.SMTP_PASS:
                server.login(settings.SMTP_USER, settings.SMTP_PASS)
            server.sendmail(settings.SMTP_FROM, [to], msg.as_string())
    except Exception as exc:
        logger.error(f"SMTP send failed to {to}: {exc}")


# ── Scheduled Jobs ──────────────────────────────────────────────────────────

def notify_pending_feedback() -> None:
    """Notify interviewers who have pending feedback (older than 1 day)."""
    from app.models.interview import RecruiterCalendar
    from app.models.feedback import OverallFeedback
    from app.models.employee import EmployeeMaster

    db: Session = SessionLocal()
    try:
        yesterday = date.today() - timedelta(days=1)
        booked = db.query(RecruiterCalendar).filter(
            RecruiterCalendar.interview_date <= yesterday,
            ~RecruiterCalendar.recruiter_calendar_id.in_(
                db.query(OverallFeedback.recruiter_calendar_id)
            ),
        ).all()
        for booking in booked:
            # Find interviewer via interviewer slot
            slot = booking.interviewer_slot
            if not slot:
                continue
            emp = db.query(EmployeeMaster).filter(EmployeeMaster.emp_id == slot.emp_id).first()
            if emp and emp.email_id:
                _send_email(
                    emp.email_id,
                    "Pending Feedback Reminder",
                    f"<p>Please submit feedback for booking ID <b>{booking.recruiter_calendar_id}</b> "
                    f"(interview date: {booking.interview_date}).</p>",
                )
        logger.info(f"Pending feedback notifications sent: {len(booked)}")
    finally:
        db.close()


def notify_offer_expiry() -> None:
    """Notify recruiters of offer letters expiring in 3 days."""
    from app.models.workflow import OfferWorkflow
    from app.models.employee import EmployeeMaster

    db: Session = SessionLocal()
    try:
        target = date.today() + timedelta(days=3)
        offers = db.query(OfferWorkflow).filter(
            OfferWorkflow.offer_expiry_date == target,
            OfferWorkflow.status == "Offer Released",
        ).all()
        for offer in offers:
            emp = db.query(EmployeeMaster).filter(
                EmployeeMaster.emp_id == offer.created_by_emp_id
            ).first() if hasattr(offer, "created_by_emp_id") else None
            if emp and emp.email_id:
                _send_email(
                    emp.email_id,
                    "Offer Expiry Reminder",
                    f"<p>Offer for candidate {offer.candidate_detail_id} expires on {target}.</p>",
                )
        logger.info(f"Offer expiry notifications sent: {len(offers)}")
    finally:
        db.close()


def cleanup_export_files() -> None:
    """Remove export files older than 7 days."""
    from app.services.document_service import cleanup_old_exports
    db: Session = SessionLocal()
    try:
        count = cleanup_old_exports(db)
        logger.info(f"Export cleanup: removed {count} records")
    finally:
        db.close()


def notify_l2_aging() -> None:
    """Notify recruiters about L2 interviews pending for more than 7 days."""
    from app.services.l2_service import get_l2_aging
    from app.models.employee import EmployeeMaster

    db: Session = SessionLocal()
    try:
        aging = get_l2_aging(db)
        old = [r for r in aging if r["aging_days"] is not None and r["aging_days"] > 7]
        logger.info(f"L2 aging alerts: {len(old)} candidates pending > 7 days")
        # In a real scenario, resolve the recruiter for each candidate and email them
    finally:
        db.close()
