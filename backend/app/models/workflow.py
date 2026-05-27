from __future__ import annotations
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger, String, Text, DateTime, Numeric,
    ForeignKey, CheckConstraint, func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class OfferWorkflow(Base):
    __tablename__ = "offer_workflow"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    candidate_detail_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("candidate_detail.candidate_detail_id"), nullable=False
    )
    current_level: Mapped[str] = mapped_column(String(100), nullable=False, default="TowerLead")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="Pending")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    comments: Mapped[list[WorkflowComments]] = relationship(
        "WorkflowComments", back_populates="workflow", cascade="all, delete-orphan",
        order_by="WorkflowComments.created_at"
    )


class WorkflowComments(Base):
    __tablename__ = "workflow_comments"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    workflow_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("offer_workflow.id"), nullable=False)
    commenter_email: Mapped[str] = mapped_column(String(255), nullable=False)
    comment_text: Mapped[str | None] = mapped_column(Text)
    action: Mapped[str] = mapped_column(
        String(20),
        CheckConstraint("action IN ('Approved','Rejected','Comment')", name="ck_workflow_action"),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    workflow: Mapped[OfferWorkflow] = relationship("OfferWorkflow", back_populates="comments")


class CTCHistory(Base):
    __tablename__ = "ctc_history"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    candidate_detail_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("candidate_detail.candidate_detail_id"), nullable=False
    )
    ctc_value: Mapped[str] = mapped_column(String(50), nullable=False)
    changed_by: Mapped[str | None] = mapped_column(String(255))
    changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class JoiningBonus(Base):
    __tablename__ = "joining_bonus"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    candidate_detail_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("candidate_detail.candidate_detail_id"), nullable=False
    )
    bonus_amount: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="Pending")
    dl_email: Mapped[str | None] = mapped_column(String(255))
    updated_by: Mapped[str | None] = mapped_column(String(255))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
