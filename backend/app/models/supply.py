from __future__ import annotations
from datetime import datetime, date

from sqlalchemy import (
    BigInteger, Integer, String, DateTime, Date,
    ForeignKey, func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class DemandBatch(Base):
    __tablename__ = "demand_batch"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    uploaded_by: Mapped[str | None] = mapped_column(String(255))
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    row_count: Mapped[int] = mapped_column(Integer, default=0)

    # Relationships
    demand_rows: Mapped[list[DemandData]] = relationship(
        "DemandData", back_populates="batch", cascade="all, delete-orphan"
    )


class DemandData(Base):
    __tablename__ = "demand_data"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    jr_id: Mapped[str | None] = mapped_column(String(100))
    skill: Mapped[str | None] = mapped_column(String(100))
    grade: Mapped[str | None] = mapped_column(String(50))
    account: Mapped[str | None] = mapped_column(String(200))
    bu: Mapped[str | None] = mapped_column(String(100))
    demand_status: Mapped[str] = mapped_column(String(50), nullable=False, default="Open")
    demand_date: Mapped[date | None] = mapped_column(Date)
    sourced_count: Mapped[int] = mapped_column(Integer, default=0)
    pipeline_count: Mapped[int] = mapped_column(Integer, default=0)
    batch_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("demand_batch.id"), nullable=False)

    # Relationships
    batch: Mapped[DemandBatch] = relationship("DemandBatch", back_populates="demand_rows")


class BenchBatch(Base):
    __tablename__ = "bench_batch"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    uploaded_by: Mapped[str | None] = mapped_column(String(255))
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    row_count: Mapped[int] = mapped_column(Integer, default=0)

    # Relationships
    bench_rows: Mapped[list[BenchData]] = relationship(
        "BenchData", back_populates="batch", cascade="all, delete-orphan"
    )


class BenchData(Base):
    __tablename__ = "bench_data"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    emp_name: Mapped[str | None] = mapped_column(String(200))
    emp_email: Mapped[str | None] = mapped_column(String(255))
    skill: Mapped[str | None] = mapped_column(String(100))
    grade: Mapped[str | None] = mapped_column(String(50))
    location: Mapped[str | None] = mapped_column(String(100))
    bu: Mapped[str | None] = mapped_column(String(100))
    bench_status: Mapped[str] = mapped_column(String(50), nullable=False, default="Available")
    batch_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("bench_batch.id"), nullable=False)

    # Relationships
    batch: Mapped[BenchBatch] = relationship("BenchBatch", back_populates="bench_rows")
