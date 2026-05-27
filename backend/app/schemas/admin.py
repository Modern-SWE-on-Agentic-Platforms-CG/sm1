from __future__ import annotations

from pydantic import BaseModel


class TowerCreate(BaseModel):
    tower_name: str


class TowerOut(BaseModel):
    id: int
    tower_name: str
    is_active: bool

    model_config = {"from_attributes": True}


class SkillCreate(BaseModel):
    tech_name: str
    skill_group: str | None = None
    tower_id: int | None = None


class SkillUpdate(BaseModel):
    tech_name: str | None = None
    skill_group: str | None = None
    tower_id: int | None = None
    is_active: bool | None = None


class SkillOut(BaseModel):
    id: int
    tech_name: str
    skill_group: str | None
    tower_id: int | None
    is_active: bool

    model_config = {"from_attributes": True}


class SourceCreate(BaseModel):
    source_name: str


class SourceOut(BaseModel):
    id: int
    source_name: str
    is_active: bool

    model_config = {"from_attributes": True}


class VendorCreate(BaseModel):
    vendor_name: str
    source_id: int | None = None


class VendorOut(BaseModel):
    id: int
    vendor_name: str
    source_id: int | None
    is_active: bool

    model_config = {"from_attributes": True}


class SapCapabilityOut(BaseModel):
    id: int
    capability_name: str
    is_active: bool

    model_config = {"from_attributes": True}


class SapSkillOut(BaseModel):
    id: int
    skill_name: str
    capability_id: int | None
    is_active: bool

    model_config = {"from_attributes": True}


class ApproverDLCreate(BaseModel):
    tower_id: int | None = None
    dl_email: str
    dl_title: str | None = None
    level: str


class RoleCommentCreate(BaseModel):
    role_id: int
    comment_text: str


class RoleCommentOut(BaseModel):
    id: int
    role_id: int
    comment_text: str

    model_config = {"from_attributes": True}
