from __future__ import annotations
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class WorkflowCommentOut(BaseModel):
    id: int
    commenter_email: str
    comment_text: str | None
    action: str
    created_at: datetime

    model_config = {"from_attributes": True}


class WorkflowOut(BaseModel):
    id: int
    candidate_detail_id: int
    current_level: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class WorkflowAction(BaseModel):
    action: str  # Approved / Rejected / Comment
    comment: str | None = None


class CTCHistoryOut(BaseModel):
    id: int
    ctc_value: str
    changed_by: str | None
    changed_at: datetime

    model_config = {"from_attributes": True}


class ThresholdOut(BaseModel):
    arc_threshold_percent: float
    description: str


class ApproverDLOut(BaseModel):
    id: int
    tower_id: int | None
    dl_email: str
    dl_title: str | None
    level: str

    model_config = {"from_attributes": True}


class ApproverDLUpdate(BaseModel):
    id: int
    dl_email: str
    dl_title: str | None = None
