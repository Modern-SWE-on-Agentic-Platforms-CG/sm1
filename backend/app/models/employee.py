from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger, String, Boolean, Integer, DateTime, ForeignKey,
    UniqueConstraint, func, Index
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.master_data import RoleMaster, TechnologyMaster


class EmployeeMaster(Base):
    __tablename__ = "employee_master"

    emp_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    emp_name: Mapped[str] = mapped_column(String(200), nullable=False)
    email_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str | None] = mapped_column(String(100))
    grade: Mapped[str | None] = mapped_column(String(50))
    bu: Mapped[str | None] = mapped_column(String(100))
    practice: Mapped[str | None] = mapped_column(String(100))
    market_unit: Mapped[str | None] = mapped_column(String(100))
    account: Mapped[str | None] = mapped_column(String(100))
    organisation: Mapped[str | None] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    __table_args__ = (
        Index("ix_employee_master_bu", "bu"),
        Index("ix_employee_master_is_active", "is_active"),
    )

    roles: Mapped[list[EmployeeRoleDetails]] = relationship(
        "EmployeeRoleDetails", back_populates="employee", cascade="all, delete-orphan"
    )
    technologies: Mapped[list[EmployeeTechnologyDetails]] = relationship(
        "EmployeeTechnologyDetails", back_populates="employee", cascade="all, delete-orphan"
    )
    towers: Mapped[list[EmployeeTowerDetails]] = relationship(
        "EmployeeTowerDetails", back_populates="employee", cascade="all, delete-orphan"
    )


class EmployeeRoleDetails(Base):
    __tablename__ = "employee_role_details"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    emp_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("employee_master.emp_id", ondelete="CASCADE"), nullable=False
    )
    role_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("role_master.id"), nullable=False
    )
    assigned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (UniqueConstraint("emp_id", "role_id"),)

    employee: Mapped[EmployeeMaster] = relationship("EmployeeMaster", back_populates="roles")
    role: Mapped[RoleMaster] = relationship("RoleMaster", back_populates="employee_roles")


class EmployeeTechnologyDetails(Base):
    __tablename__ = "employee_technology_details"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    emp_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("employee_master.emp_id", ondelete="CASCADE"), nullable=False
    )
    technology_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("technology_master.id"), nullable=False
    )
    added_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (UniqueConstraint("emp_id", "technology_id"),)

    employee: Mapped[EmployeeMaster] = relationship("EmployeeMaster", back_populates="technologies")
    technology: Mapped[TechnologyMaster] = relationship(
        "TechnologyMaster", back_populates="employee_technologies"
    )


class EmployeeTowerDetails(Base):
    __tablename__ = "employee_tower_details"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    emp_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("employee_master.emp_id", ondelete="CASCADE"), nullable=False
    )
    tower_name: Mapped[str] = mapped_column(String(100), nullable=False)

    employee: Mapped[EmployeeMaster] = relationship("EmployeeMaster", back_populates="towers")
