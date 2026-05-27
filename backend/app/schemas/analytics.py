from pydantic import BaseModel
from typing import Any


class PieChartItem(BaseModel):
    name: str
    value: int


class LineChartItem(BaseModel):
    date: str
    count: int


class TrendChartItem(BaseModel):
    month: str
    hired: int
    pipeline: int


class RejectChartItem(BaseModel):
    reason: str
    count: int


class ArcDeviationItem(BaseModel):
    candidate_id: int
    candidate_name: str | None
    ctc_offered: float | None
    ctc_arc: float | None
    deviation_pct: float | None


class AnalyticsSummary(BaseModel):
    total_candidates: int
    total_offers: int
    total_joinings: int
    pending_feedback: int
