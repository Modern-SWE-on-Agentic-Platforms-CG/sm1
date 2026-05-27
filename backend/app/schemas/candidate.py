from __future__ import annotations
from datetime import datetime, date
from pydantic import BaseModel


class CandidateOut(BaseModel):
    candidate_detail_id: int
    candidate_name: str
    email_id: str
    contact_number: str | None
    gender: str | None
    total_exp: str | None
    rel_exp: str | None
    current_company: str | None
    current_location: str | None
    preferred_location: str | None
    notice_period: str | None
    current_ctc: str | None
    exp_ctc: str | None
    offer_ctc: str | None
    skill_id: int | None
    tower: str | None
    skill_group: str | None
    source: str | None
    referred_vendor: str | None
    overall_status: str
    is_referral: bool
    is_rehire: bool
    doj: date | None
    resume_path: str | None
    created_by: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class CandidateUpdate(BaseModel):
    candidate_name: str | None = None
    contact_number: str | None = None
    gender: str | None = None
    total_exp: str | None = None
    rel_exp: str | None = None
    current_company: str | None = None
    current_location: str | None = None
    preferred_location: str | None = None
    notice_period: str | None = None
    current_ctc: str | None = None
    exp_ctc: str | None = None
    offer_ctc: str | None = None
    skill_id: int | None = None
    tower: str | None = None
    source: str | None = None
    referred_vendor: str | None = None
    doj: date | None = None


class CommentCreate(BaseModel):
    comment_text: str | None = None


class CommentOut(BaseModel):
    id: int
    candidate_detail_id: int
    comment_text: str | None
    attachment_path: str | None
    attachment_filename: str | None
    created_by: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class StatusChangeRequest(BaseModel):
    to_status: str
    notes: str | None = None


class BulkUploadResponse(BaseModel):
    imported: int
    duplicates: int
    errors: int
    error_file_url: str | None = None
