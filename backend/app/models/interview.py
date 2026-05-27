from __future__ import annotations
from datetime import datetime, date

from sqlalchemy import (
    BigInteger, String, Boolean, Integer, Date, DateTime,
    ForeignKey, CheckConstraint, Index, func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class InterviewerCalendar(Base):
    __tablename__ = "interviewer_calendar"

    interviewer_calendar_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    emp_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("employee_master.emp_id"), nullable=False
    )
    skill_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("technology_master.id"))
    slot_date: Mapped[date] = mapped_column(Date, nullable=False)
    from_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    to_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    slot_status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="Available"
    )
    is_weekend_drive: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_by: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    __table_args__ = (
        CheckConstraint(
            "slot_status IN ('Available','Booked','Interviewed','Pending')",
            name="ck_slot_status",
        ),
        Index("ix_interviewer_calendar_emp_date", "emp_id", "slot_date"),
        Index("ix_interviewer_calendar_emp_status", "emp_id", "slot_status"),
        Index("ix_interviewer_calendar_skill_id", "skill_id"),
    )

    # Relationships
    recruiter_calendars: Mapped[list[RecruiterCalendar]] = relationship(
        "RecruiterCalendar", back_populates="interviewer_slot"
    )


class RecruiterCalendar(Base):
    __tablename__ = "recruiter_calendar"

    recruiter_calendar_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    candidate_detail_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("candidate_detail.candidate_detail_id"), nullable=False
    )
    interviewer_calendar_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("interviewer_calendar.interviewer_calendar_id"), nullable=True
    )
    interview_type: Mapped[str | None] = mapped_column(String(10))
    skill_id: Mapped[int | None] = mapped_column(Integer)
    from_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    to_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    interview_date: Mapped[date | None] = mapped_column(Date)
    panel_email: Mapped[str | None] = mapped_column(String(255))
    meeting_link: Mapped[str | None] = mapped_column(String(255))
    is_direct_booked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    feedback_submitted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    booked_by: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    interviewer_slot: Mapped[InterviewerCalendar | None] = relationship(
        "InterviewerCalendar", back_populates="recruiter_calendars"
    )
    candidate: Mapped["CandidateDetail"] = relationship(  # type: ignore[name-defined]
        "CandidateDetail", back_populates="bookings"
    )
