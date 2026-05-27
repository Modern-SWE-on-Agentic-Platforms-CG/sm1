from __future__ import annotations
from datetime import datetime
from typing import Any

from sqlalchemy import (
    BigInteger, Integer, String, Boolean, Text, DateTime,
    ForeignKey, CheckConstraint, func
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class FeedbackFormTemplate(Base):
    __tablename__ = "feedback_form_template"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tech_name: Mapped[str] = mapped_column(String(100), nullable=False)
    practice: Mapped[str | None] = mapped_column(String(100))
    form_title: Mapped[str] = mapped_column(String(200), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    parameters: Mapped[list[FeedbackParameter]] = relationship(
        "FeedbackParameter", back_populates="template", cascade="all, delete-orphan",
        order_by="FeedbackParameter.param_order"
    )
    feedback_forms: Mapped[list[InterviewerFeedbackFormDetails]] = relationship(
        "InterviewerFeedbackFormDetails", back_populates="template"
    )


class FeedbackParameter(Base):
    __tablename__ = "feedback_parameter"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    template_id: Mapped[int] = mapped_column(Integer, ForeignKey("feedback_form_template.id"), nullable=False)
    section_name: Mapped[str] = mapped_column(String(200), nullable=False)
    parameter_name: Mapped[str] = mapped_column(String(200), nullable=False)
    param_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    max_score: Mapped[int] = mapped_column(Integer, nullable=False, default=10)

    # Relationships
    template: Mapped[FeedbackFormTemplate] = relationship("FeedbackFormTemplate", back_populates="parameters")


class InterviewerFeedbackFormDetails(Base):
    __tablename__ = "interviewer_feedback_form_details"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    recruiter_calendar_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("recruiter_calendar.recruiter_calendar_id"), nullable=False
    )
    template_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("feedback_form_template.id"))
    parameter_scores: Mapped[Any | None] = mapped_column(JSONB)
    overall_rating: Mapped[str | None] = mapped_column(
        String(20),
        CheckConstraint("overall_rating IN ('Select','Hold','Reject')", name="ck_overall_rating"),
    )
    overall_remarks: Mapped[str | None] = mapped_column(Text)
    submitted_by: Mapped[str | None] = mapped_column(String(255))
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    pdf_path: Mapped[str | None] = mapped_column(String(500))

    # Relationships
    template: Mapped[FeedbackFormTemplate | None] = relationship(
        "FeedbackFormTemplate", back_populates="feedback_forms"
    )


class OverallFeedback(Base):
    __tablename__ = "overall_feedback"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    recruiter_calendar_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("recruiter_calendar.recruiter_calendar_id"), nullable=False
    )
    rating: Mapped[str | None] = mapped_column(String(20))
    remarks: Mapped[str | None] = mapped_column(Text)
    is_revisit: Mapped[bool] = mapped_column(Boolean, default=False)
