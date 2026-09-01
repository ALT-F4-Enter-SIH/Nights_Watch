"""Dashboard and analytics response schemas."""
from pydantic import BaseModel
from typing import Optional


class ConfidenceDistribution(BaseModel):
    bins: list[int]  # [0-10, 10-20, ..., 90-100] as percentages * 100
    counts: list[int]
    label: str = "Identities"


class TrendPoint(BaseModel):
    date: str
    identities: int
    relations: int


class CategoryCount(BaseModel):
    category: str
    count: int


class RiskBand(BaseModel):
    band: str  # "low", "medium", "high", "critical"
    count: int


class NetworkMetrics(BaseModel):
    total_nodes: int
    total_edges: int
    avg_clustering_coefficient: float
    density: float
    connected_components: int
    isolated_nodes: int


class DashboardOverview(BaseModel):
    total_identities: int
    total_relations: int
    total_investigations: int
    avg_confidence: float
    high_confidence_count: int
    medium_confidence_count: int
    low_confidence_count: int
    open_investigations: int
    closed_investigations: int
    avg_risk_score: float
    categories_present: list[str]
    languages_present: list[str]


class DashboardResponse(BaseModel):
    overview: DashboardOverview
    confidence_distribution: ConfidenceDistribution
    category_breakdown: list[CategoryCount]
    risk_bands: list[RiskBand]
    network_metrics: NetworkMetrics
    recent_trends: list[TrendPoint]
