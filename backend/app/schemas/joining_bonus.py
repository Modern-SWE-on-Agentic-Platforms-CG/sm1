from __future__ import annotations
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class JoiningBonusOut(BaseModel):
    id: int
    candidate_detail_id: int
    bonus_amount: Decimal | None
    status: str
    dl_email: str | None
    updated_by: str | None
    updated_at: datetime

    model_config = {"from_attributes": True}


class JoiningBonusUpdate(BaseModel):
    status: str
    dl_email: str | None = None


class JBCandidateOut(BaseModel):
    id: int
    candidate_detail_id: int
    candidate_name: str | None = None
    bonus_amount: Decimal | None
    status: str
    dl_email: str | None

    model_config = {"from_attributes": True}
