"""Weighted confidence aggregation for correlation results."""
from __future__ import annotations

from typing import Dict, List

WEIGHTS = {
    "username": 0.20,
    "alias": 0.15,
    "pgp": 0.20,
    "wallet": 0.20,
    "behavioral": 0.10,
    "stylometry": 0.10,
    "infrastructure": 0.05,
}


def aggregate(matches: List[Dict]) -> float:
    if not matches:
        return 0.0
    weighted = 0.0
    total_weight = 0.0
    for m in matches:
        ctype = m.get("correlation_type", "")
        weight = WEIGHTS.get(ctype, 0.05)
        weighted += weight * float(m.get("confidence_score", 0.0))
        total_weight += weight
    if total_weight == 0:
        return 0.0
    return round(min(1.0, weighted / total_weight), 4)


def classify(score: float) -> str:
    if score >= 0.85:
        return "high"
    if score >= 0.55:
        return "medium"
    if score >= 0.25:
        return "low"
    return "minimal"
