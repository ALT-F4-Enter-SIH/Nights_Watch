"""
Behavior service — assembles behavioral profiles from synthetic identity metadata.
"""
from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from models.identity import Identity


def _hourly_distribution(active_hours: list[int], total: int) -> list[dict]:
    if total == 0:
        return []
    distribution = []
    for hour in range(24):
        if hour in active_hours:
            posts = max(1, total // max(1, len(active_hours)))
        else:
            posts = 0
        distribution.append(
            {
                "hour": hour,
                "posts": posts,
                "percentage": round((posts / total) * 100, 2),
            }
        )
    return distribution


def _indicators(profile: dict) -> list[str]:
    indicators = []
    if profile["post_frequency_daily"] >= 3.0:
        indicators.append("High post frequency")
    if profile["platform_switch_frequency"] == "high":
        indicators.append("Frequent platform switching")
    if profile["response_latency_pattern"] == "fast":
        indicators.append("Rapid response latency")
    if 22 in profile["active_hours"] or 0 in profile["active_hours"] or 1 in profile["active_hours"]:
        indicators.append("Off-peak activity")
    if not indicators:
        indicators.append("Standard behavioral pattern")
    return indicators


def _risk_band(risk_score: float) -> str:
    if risk_score >= 0.75:
        return "high"
    if risk_score >= 0.45:
        return "medium"
    return "low"


def build_profile(db: Session, identity_id: str) -> Optional[dict]:
    row = db.query(Identity).filter(Identity.id == identity_id).first()
    if not row:
        return None
    meta = row.extra_metadata or {}
    behavioral = meta.get("behavioral_profile", {}) or {}
    active_hours = row.posting_hours or []
    total_posts = len(meta.get("posting_timestamps", [])) or 1
    profile = {
        "identity_id": row.id,
        "username": row.username,
        "active_hours": active_hours,
        "categories": row.categories or [],
        "languages": meta.get("languages", []),
        "post_frequency_daily": float(behavioral.get("post_frequency_daily", meta.get("post_frequency_daily", 0.0)) or 0.0),
        "typical_session_length_minutes": int(behavioral.get("typical_session_length_minutes", 30)),
        "platform_switch_frequency": behavioral.get("platform_switch_frequency", "medium"),
        "response_latency_pattern": behavioral.get("response_latency_pattern", "moderate"),
        "hourly_distribution": _hourly_distribution(active_hours, total_posts),
        "behavioral_indicators": _indicators(
            {
                "post_frequency_daily": float(behavioral.get("post_frequency_daily", 0.0) or 0.0),
                "platform_switch_frequency": behavioral.get("platform_switch_frequency", "medium"),
                "response_latency_pattern": behavioral.get("response_latency_pattern", "moderate"),
                "active_hours": active_hours,
            }
        ),
        "risk_assessment": _risk_band(float(meta.get("risk_score", 0.0) or 0.0)),
    }
    return profile


def compare(db: Session, identity_id_a: str, identity_id_b: str) -> Optional[dict]:
    profile_a = build_profile(db, identity_id_a)
    profile_b = build_profile(db, identity_id_b)
    if not profile_a or not profile_b:
        return None

    set_a_hours, set_b_hours = set(profile_a["active_hours"]), set(profile_b["active_hours"])
    shared_hours = sorted(set_a_hours & set_b_hours)
    hour_score = (len(shared_hours) / max(1, len(set_a_hours | set_b_hours))) if (set_a_hours or set_b_hours) else 0.0

    set_a_cats, set_b_cats = set(profile_a["categories"]), set(profile_b["categories"])
    shared_categories = sorted(set_a_cats & set_b_cats)
    cat_score = (len(shared_categories) / max(1, len(set_a_cats | set_b_cats))) if (set_a_cats or set_b_cats) else 0.0

    set_a_langs, set_b_langs = set(profile_a["languages"]), set(profile_b["languages"])
    lang_score = (len(set_a_langs & set_b_langs) / max(1, len(set_a_langs | set_b_langs))) if (set_a_langs or set_b_langs) else 0.0

    combined = round(0.45 * hour_score + 0.4 * cat_score + 0.15 * lang_score, 4)

    indicators = []
    if hour_score > 0.5:
        indicators.append("Strong hourly overlap")
    if cat_score > 0.5:
        indicators.append("Strong category overlap")
    if lang_score > 0.5:
        indicators.append("Shared primary language")
    if not indicators:
        indicators.append("Low behavioral overlap")

    return {
        "identity_a": identity_id_a,
        "identity_b": identity_id_b,
        "hour_overlap_score": round(hour_score, 4),
        "category_overlap_score": round(cat_score, 4),
        "language_overlap_score": round(lang_score, 4),
        "combined_behavioral_score": combined,
        "shared_hours": shared_hours,
        "shared_categories": shared_categories,
        "behavioral_indicators": indicators,
    }
