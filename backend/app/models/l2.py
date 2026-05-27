from __future__ import annotations
from datetime import date, datetime
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class L2SelectData(Base):
    __tablename__ = "l2_select_data"

    l2_select_id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_detail_id = Column(Integer, ForeignKey("candidate_detail.candidate_detail_id", ondelete="CASCADE"), nullable=False, index=True)
    l2_interviewer_id = Column(Integer, ForeignKey("employee_master.emp_id", ondelete="SET NULL"), nullable=True)
    l2_interview_date = Column(Date, nullable=True)
    l2_feedback = Column(Text, nullable=True)
    l2_recommendation = Column(String(50), nullable=True)
    l2_status = Column(String(50), nullable=True, default="Pending", index=True)
    aging_days = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
