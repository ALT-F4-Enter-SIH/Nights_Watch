"""Behavioral analysis schemas."""
from pydantic import BaseModel
from typing import Optional


class HourlyActivity(BaseModel):
    hour: int
    posts: int
    percentage: float


class BehavioralProfile(BaseModel):
    identity_id: str
    username: str
    active_hours: list[int]
    categories: list[str]
    languages: list[str]
    post_frequency_daily: float
    typical_session_length_minutes: int
    platform_switch_frequency: str
    response_latency_pattern: str
    hourly_distribution: list[HourlyActivity]
    behavioral_indicators: list[str]
    risk_assessment: str  # "low", "medium", "high"


class BehavioralComparison(BaseModel):
    identity_a: str
    identity_b: str
    hour_overlap_score: float
    category_overlap_score: float
    language_overlap_score: float
    combined_behavioral_score: float
    shared_hours: list[int]
    shared_categories: list[str]
    behavioral_indicators: list[str]
