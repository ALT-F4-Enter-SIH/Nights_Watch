"""Report generation schemas."""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CorrelationEntry(BaseModel):
    identity_a: str
    identity_b: str
    confidence_score: float
    correlation_type: str
    explanation: str


class ClusterSummary(BaseModel):
    name: str
    member_count: int
    members: list[str]
    shared_signals: list[str]
    avg_confidence: float


class ReportSection(BaseModel):
    title: str
    content: str


class ReportResponse(BaseModel):
    report_id: str
    investigation_id: Optional[str] = None
    title: str
    generated_at: datetime
    summary: str
    sections: list[ReportSection]
    clusters: list[ClusterSummary]
    correlations: list[CorrelationEntry]
    total_identities_analyzed: int
    total_correlations_found: int
    methodology: str
