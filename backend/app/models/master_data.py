from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, String, Boolean, Integer, DateTime, Text, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.employee import EmployeeRoleDetails, EmployeeTechnologyDetails


class RoleMaster(Base):
    __tablename__ = "role_master"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    role_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    employee_roles: Mapped[list[EmployeeRoleDetails]] = relationship(
        "EmployeeRoleDetails", back_populates="role"
    )


class TowerMaster(Base):
    __tablename__ = "tower_master"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tower_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    technologies: Mapped[list[TechnologyMaster]] = relationship(
        "TechnologyMaster", back_populates="tower"
    )


class TechnologyMaster(Base):
    __tablename__ = "technology_master"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tech_name: Mapped[str] = mapped_column(String(100), nullable=False)
    skill_group: Mapped[str | None] = mapped_column(String(100))
    tower_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("tower_master.id"), nullable=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    tower: Mapped[TowerMaster | None] = relationship("TowerMaster", back_populates="technologies")
    employee_technologies: Mapped[list[EmployeeTechnologyDetails]] = relationship(
        "EmployeeTechnologyDetails", back_populates="technology"
    )


# --- Extended Master Data (Phase 2) ---

class SourceMaster(Base):
    __tablename__ = "source_master"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    vendors: Mapped[list[VendorMaster]] = relationship("VendorMaster", back_populates="source")


class VendorMaster(Base):
    __tablename__ = "vendor_master"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    vendor_name: Mapped[str] = mapped_column(String(100), nullable=False)
    source_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("source_master.id"))
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (UniqueConstraint("vendor_name", "source_id"),)

    source: Mapped[SourceMaster | None] = relationship("SourceMaster", back_populates="vendors")


class ApproverDLMapping(Base):
    __tablename__ = "approver_dl_mapping"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tower_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("tower_master.id"))
    dl_email: Mapped[str] = mapped_column(String(255), nullable=False)
    dl_title: Mapped[str | None] = mapped_column(String(200))
    level: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class TowerSkillMapping(Base):
    __tablename__ = "tower_skill_mapping"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tower_id: Mapped[int] = mapped_column(Integer, ForeignKey("tower_master.id"), nullable=False)
    technology_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("technology_master.id"), nullable=False
    )

    __table_args__ = (UniqueConstraint("tower_id", "technology_id"),)


class SapCapabilityMaster(Base):
    __tablename__ = "sap_capability_master"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    capability_name: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    skills: Mapped[list[SapSkillMaster]] = relationship("SapSkillMaster", back_populates="capability")


class SapSkillMaster(Base):
    __tablename__ = "sap_skill_master"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    skill_name: Mapped[str] = mapped_column(String(200), nullable=False)
    capability_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("sap_capability_master.id"), nullable=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    capability: Mapped[SapCapabilityMaster | None] = relationship(
        "SapCapabilityMaster", back_populates="skills"
    )


class ExportHistory(Base):
    __tablename__ = "export_history"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    export_type: Mapped[str] = mapped_column(String(100), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    created_by: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


class RoleComment(Base):
    __tablename__ = "role_comment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("role_master.id"), nullable=False)
    comment_text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

