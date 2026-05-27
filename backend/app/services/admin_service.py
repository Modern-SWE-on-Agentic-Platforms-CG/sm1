from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.master_data import (
    TowerMaster, TechnologyMaster, SourceMaster, VendorMaster,
    SapCapabilityMaster, SapSkillMaster, ApproverDLMapping, RoleComment
)
from app.schemas.admin import (
    TowerCreate, SkillCreate, SkillUpdate, SourceCreate, VendorCreate,
    ApproverDLCreate, RoleCommentCreate
)
from app.core.logging import get_logger

logger = get_logger(__name__)


# ---- Towers ----

def list_towers(db: Session) -> list:
    return db.query(TowerMaster).all()


def create_tower(data: TowerCreate, db: Session) -> TowerMaster:
    existing = db.query(TowerMaster).filter(TowerMaster.tower_name == data.tower_name).first()
    if existing:
        raise HTTPException(status_code=409, detail="TOWER ALREADY EXISTS")
    tower = TowerMaster(tower_name=data.tower_name)
    db.add(tower)
    db.commit()
    db.refresh(tower)
    return tower


def delete_tower(tower_id: int, db: Session) -> None:
    tower = db.query(TowerMaster).filter(TowerMaster.id == tower_id).first()
    if not tower:
        raise HTTPException(status_code=404, detail="Tower not found")
    # Check active technologies referencing this tower
    active_tech = db.query(TechnologyMaster).filter(
        TechnologyMaster.tower_id == tower_id,
        TechnologyMaster.is_active == True,
    ).count()
    if active_tech > 0:
        raise HTTPException(status_code=400, detail="Cannot delete tower with active references")
    tower.is_active = False
    db.commit()


# ---- Skills ----

def list_skills(db: Session) -> list:
    return db.query(TechnologyMaster).all()


def create_skill(data: SkillCreate, db: Session) -> TechnologyMaster:
    existing = db.query(TechnologyMaster).filter(
        TechnologyMaster.tech_name == data.tech_name,
        TechnologyMaster.tower_id == data.tower_id,
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="TECHNOLOGY ALREADY EXISTS")
    skill = TechnologyMaster(
        tech_name=data.tech_name,
        skill_group=data.skill_group,
        tower_id=data.tower_id,
    )
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill


def update_skill(skill_id: int, data: SkillUpdate, db: Session) -> TechnologyMaster:
    skill = db.query(TechnologyMaster).filter(TechnologyMaster.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(skill, field, value)
    db.commit()
    db.refresh(skill)
    return skill


def delete_skill(skill_id: int, db: Session) -> None:
    skill = db.query(TechnologyMaster).filter(TechnologyMaster.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    skill.is_active = False
    db.commit()


# ---- Sources ----

def list_sources(db: Session) -> list:
    return db.query(SourceMaster).all()


def create_source(data: SourceCreate, db: Session) -> SourceMaster:
    existing = db.query(SourceMaster).filter(SourceMaster.source_name == data.source_name).first()
    if existing:
        raise HTTPException(status_code=409, detail="SOURCE ALREADY EXISTS")
    source = SourceMaster(source_name=data.source_name)
    db.add(source)
    db.commit()
    db.refresh(source)
    return source


def delete_source(source_id: int, db: Session) -> None:
    source = db.query(SourceMaster).filter(SourceMaster.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    source.is_active = False
    db.commit()


# ---- Vendors ----

def list_vendors(db: Session) -> list:
    return db.query(VendorMaster).all()


def create_vendor(data: VendorCreate, db: Session) -> VendorMaster:
    existing = db.query(VendorMaster).filter(
        VendorMaster.vendor_name == data.vendor_name,
        VendorMaster.source_id == data.source_id,
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="VENDOR ALREADY EXISTS")
    vendor = VendorMaster(vendor_name=data.vendor_name, source_id=data.source_id)
    db.add(vendor)
    db.commit()
    db.refresh(vendor)
    return vendor


def delete_vendor(vendor_id: int, db: Session) -> None:
    vendor = db.query(VendorMaster).filter(VendorMaster.id == vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    vendor.is_active = False
    db.commit()


# ---- SAP ----

def list_sap_capabilities(db: Session) -> list:
    return db.query(SapCapabilityMaster).filter(SapCapabilityMaster.is_active == True).all()


def create_sap_capability(name: str, db: Session) -> SapCapabilityMaster:
    cap = SapCapabilityMaster(capability_name=name)
    db.add(cap)
    db.commit()
    db.refresh(cap)
    return cap


def list_sap_skills(db: Session) -> list:
    return db.query(SapSkillMaster).filter(SapSkillMaster.is_active == True).all()


def create_sap_skill(name: str, capability_id: int | None, db: Session) -> SapSkillMaster:
    skill = SapSkillMaster(skill_name=name, capability_id=capability_id)
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill


# ---- Approver DL ----

def list_approver_dl(db: Session) -> list:
    return db.query(ApproverDLMapping).all()


def create_approver_dl(data: ApproverDLCreate, db: Session) -> ApproverDLMapping:
    dl = ApproverDLMapping(**data.model_dump())
    db.add(dl)
    db.commit()
    db.refresh(dl)
    return dl


def delete_approver_dl(dl_id: int, db: Session) -> None:
    dl = db.query(ApproverDLMapping).filter(ApproverDLMapping.id == dl_id).first()
    if not dl:
        raise HTTPException(status_code=404, detail="Approver DL not found")
    db.delete(dl)
    db.commit()


# ---- Role Comments ----

def list_role_comments(db: Session) -> list:
    return db.query(RoleComment).all()


def create_role_comment(data: RoleCommentCreate, db: Session) -> RoleComment:
    comment = RoleComment(role_id=data.role_id, comment_text=data.comment_text)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def delete_role_comment(comment_id: int, db: Session) -> None:
    comment = db.query(RoleComment).filter(RoleComment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Role comment not found")
    db.delete(comment)
    db.commit()
