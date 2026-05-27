from __future__ import annotations
from datetime import datetime

from sqlalchemy import (
    BigInteger, Integer, String, Boolean, DateTime,
    ForeignKey, UniqueConstraint, func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ReferralTechnologyMaster(Base):
    __tablename__ = "referral_technology_master"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tech_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # Relationships
    candidate_skills: Mapped[list[ReferralCandidateSkill]] = relationship(
        "ReferralCandidateSkill", back_populates="technology"
    )


class ReferralNoticePeriodMaster(Base):
    __tablename__ = "referral_notice_period_master"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    period_label: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)


class ReferralLocationMaster(Base):
    __tablename__ = "referral_location_master"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    location_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)


class ReferralCandidateInfo(Base):
    __tablename__ = "referral_candidate_info"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    referee_emp_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("employee_master.emp_id"), nullable=True
    )
    candidate_name: Mapped[str] = mapped_column(String(200), nullable=False)
    candidate_email: Mapped[str] = mapped_column(String(255), nullable=False)
    candidate_phone: Mapped[str | None] = mapped_column(String(20))
    certifications: Mapped[str | None] = mapped_column(String(500))
    notice_period: Mapped[str | None] = mapped_column(String(50))
    location: Mapped[str | None] = mapped_column(String(100))
    resume_path: Mapped[str | None] = mapped_column(String(500))
    image_path: Mapped[str | None] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="Pending")
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    skills: Mapped[list[ReferralCandidateSkill]] = relationship(
        "ReferralCandidateSkill", back_populates="referral", cascade="all, delete-orphan"
    )


class ReferralCandidateSkill(Base):
    __tablename__ = "referral_candidate_skills"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    referral_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("referral_candidate_info.id"), nullable=False
    )
    tech_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("referral_technology_master.id"), nullable=False
    )

    __table_args__ = (UniqueConstraint("referral_id", "tech_id"),)

    # Relationships
    referral: Mapped[ReferralCandidateInfo] = relationship("ReferralCandidateInfo", back_populates="skills")
    technology: Mapped[ReferralTechnologyMaster] = relationship(
        "ReferralTechnologyMaster", back_populates="candidate_skills"
    )
