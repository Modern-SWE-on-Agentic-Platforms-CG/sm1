from __future__ import annotations
from datetime import datetime, date

from sqlalchemy import (
    BigInteger, String, Boolean, Integer, Date, DateTime, Text,
    ForeignKey, UniqueConstraint, Index, func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class StatusIntermediateMapping(Base):
    __tablename__ = "status_intermediate_mapping"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    from_status: Mapped[str] = mapped_column(String(100), nullable=False)
    to_status: Mapped[str] = mapped_column(String(100), nullable=False)

    __table_args__ = (UniqueConstraint("from_status", "to_status"),)


class CandidateDetail(Base):
    __tablename__ = "candidate_detail"

    candidate_detail_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    candidate_name: Mapped[str] = mapped_column(String(200), nullable=False)
    email_id: Mapped[str] = mapped_column(String(255), nullable=False)
    contact_number: Mapped[str | None] = mapped_column(String(20))
    gender: Mapped[str | None] = mapped_column(String(20))
    total_exp: Mapped[str | None] = mapped_column(String(10))
    rel_exp: Mapped[str | None] = mapped_column(String(10))
    current_company: Mapped[str | None] = mapped_column(String(200))
    current_location: Mapped[str | None] = mapped_column(String(100))
    preferred_location: Mapped[str | None] = mapped_column(String(100))
    notice_period: Mapped[str | None] = mapped_column(String(50))
    current_ctc: Mapped[str | None] = mapped_column(String(50))
    exp_ctc: Mapped[str | None] = mapped_column(String(50))
    offer_ctc: Mapped[str | None] = mapped_column(String(50))
    skill_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("technology_master.id"))
    tower: Mapped[str | None] = mapped_column(String(100))
    skill_group: Mapped[str | None] = mapped_column(String(100))
    source: Mapped[str | None] = mapped_column(String(100))
    referred_vendor: Mapped[str | None] = mapped_column(String(100))
    college: Mapped[str | None] = mapped_column(String(200))
    level_based_on_exp: Mapped[str | None] = mapped_column(String(50))
    overall_status: Mapped[str] = mapped_column(String(100), nullable=False, default="Profile Received")
    dashboard_status: Mapped[str | None] = mapped_column(String(100))
    is_referral: Mapped[bool] = mapped_column(Boolean, default=False)
    is_rehire: Mapped[bool] = mapped_column(Boolean, default=False)
    bu_id: Mapped[int | None] = mapped_column(Integer)
    practice_id: Mapped[int | None] = mapped_column(Integer)
    account_name: Mapped[str | None] = mapped_column(String(200))
    region: Mapped[str | None] = mapped_column(String(100))
    pmo_coordinator: Mapped[str | None] = mapped_column(String(200))
    pmo_coordinator_email: Mapped[str | None] = mapped_column(String(255))
    hr_coordinator: Mapped[str | None] = mapped_column(String(200))
    jr_id: Mapped[str | None] = mapped_column(String(100))
    doj: Mapped[date | None] = mapped_column(Date)
    resume_path: Mapped[str | None] = mapped_column(String(500))
    created_by: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    recvd_date: Mapped[date | None] = mapped_column(Date)

    __table_args__ = (
        Index("ix_candidate_email_id", "email_id"),
        Index("ix_candidate_overall_status", "overall_status"),
        Index("ix_candidate_skill_id", "skill_id"),
        Index("ix_candidate_created_by", "created_by"),
        Index("ix_candidate_bu_status", "bu_id", "overall_status"),
    )

    # Relationships
    status_history: Mapped[list[CandidateStatusHistory]] = relationship(
        "CandidateStatusHistory", back_populates="candidate", cascade="all, delete-orphan"
    )
    comments: Mapped[list[CandidateComments]] = relationship(
        "CandidateComments", back_populates="candidate", cascade="all, delete-orphan"
    )
    bookings: Mapped[list["RecruiterCalendar"]] = relationship(  # type: ignore[name-defined]
        "RecruiterCalendar", back_populates="candidate"
    )


class CandidateStatusHistory(Base):
    __tablename__ = "candidate_status_history"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    candidate_detail_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("candidate_detail.candidate_detail_id"), nullable=False
    )
    from_status: Mapped[str | None] = mapped_column(String(100))
    to_status: Mapped[str] = mapped_column(String(100), nullable=False)
    changed_by: Mapped[str | None] = mapped_column(String(255))
    changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    notes: Mapped[str | None] = mapped_column(Text)

    candidate: Mapped[CandidateDetail] = relationship(
        "CandidateDetail", back_populates="status_history"
    )


class CandidateComments(Base):
    __tablename__ = "candidate_comments"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    candidate_detail_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("candidate_detail.candidate_detail_id"), nullable=False
    )
    comment_text: Mapped[str | None] = mapped_column(Text)
    attachment_path: Mapped[str | None] = mapped_column(String(500))
    attachment_filename: Mapped[str | None] = mapped_column(String(255))
    created_by: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    candidate: Mapped[CandidateDetail] = relationship(
        "CandidateDetail", back_populates="comments"
    )
