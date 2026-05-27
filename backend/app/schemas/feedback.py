from __future__ import annotations
from datetime import datetime
from typing import Any

from pydantic import BaseModel


class FeedbackParameterOut(BaseModel):
    id: int
    parameter_name: str
    max_score: int
    param_order: int

    model_config = {"from_attributes": True}


class FeedbackSectionOut(BaseModel):
    section_name: str
    parameters: list[FeedbackParameterOut]


class FeedbackTemplateOut(BaseModel):
    template_id: int
    form_title: str
    tech_name: str
    sections: list[FeedbackSectionOut]

    model_config = {"from_attributes": True}


class FeedbackSubmitRequest(BaseModel):
    parameter_scores: dict[str, int]
    overall_rating: str  # Select / Hold / Reject
    overall_remarks: str | None = None
    is_revisit: bool = False


class FeedbackOut(BaseModel):
    feedback_id: int
    pdf_path: str | None
    overall_rating: str | None

    model_config = {"from_attributes": True}


class PDFDownloadResponse(BaseModel):
    file_path: str
    booking_id: int


class FeedbackTemplateCreate(BaseModel):
    tech_name: str
    practice: str | None = None
    form_title: str
    parameters: list[dict[str, Any]]
