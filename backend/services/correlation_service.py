"""
Correlation service — orchestrates identity-pair correlations using real synthetic data.
"""
from __future__ import annotations

import time
import uuid
from itertools import combinations
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from models.identity import Identity
from models.relation import Relation
from services.correlation_engine import (
    behavioral_pattern_match,
    crypto_wallet_match,
    exact_username_match,
    fuzzy_alias_match,
    pgp_match,
    metadata_match,
    temporal_match,
    category_match,
    graph_match,
)

# Default weights (sum to 1.0)
DEFAULT_WEIGHTS = {
    "username": 0.20,
    "alias": 0.15,
    "pgp": 0.20,
    "wallet": 0.15,
    "behavioral": 0.10,
    "stylometry": 0.25,
    "metadata": 0.10,
    "temporal": 0.10,
    "category": 0.05,
    "graph": 0.05,
}

# Default correlation methods to use
DEFAULT_METHODS = [
    "username",
    "alias",
    "pgp",
    "wallet",
    "behavioral",
    "stylometry",
    "metadata",
    "temporal",
    "category",
    "graph",
    "infrastructure"
]


def _iter_pairs(identities: List[dict]) -> List[tuple[dict, dict]]:
    return list(combinations(identities, 2))


def _identity_payload(identity: Identity) -> dict:
    meta = identity.extra_metadata or {}
    return {
        "id": identity.id,
        "username": identity.username,
        "aliases": identity.aliases or [],
        "email": identity.email,
        "pgp_fingerprint": identity.pgp_fingerprint,
        "crypto_wallets": identity.crypto_wallets or [],
        "posting_hours": identity.posting_hours or [],
        "categories": identity.categories or [],
        "writing_samples": identity.writing_samples or [],
        "languages": meta.get("languages", []),
        "infrastructure_metadata": meta.get("infrastructure_metadata", {}),
        "writing_style_signature": meta.get("writing_style_signature", {}),
    }


def _alias_overlap(a: dict, b: dict) -> tuple[bool, float, str]:
    match, score, explanation = fuzzy_alias_match(a, b)
    return match, score, explanation


def _stylometry_match(a: dict, b: dict) -> tuple[bool, float, str]:
    from ml.stylometry import stylometry_similarity

    a_text = " ".join(a.get("writing_samples", []))
    b_text = " ".join(b.get("writing_samples", []))
    if not a_text or not b_text:
        return False, 0.0, "Insufficient writing samples"
    _, _, score, _, _, _ = stylometry_similarity(a_text, b_text)
    if score < 0.3:
        return False, score, ""
    return True, score, f"Stylometry similarity: {round(score * 100, 1)}%"


def _infrastructure_match(a: dict, b: dict) -> tuple[bool, float, str]:
    a_infra = a.get("infrastructure_metadata", {}) or {}
    b_infra = b.get("infrastructure_metadata", {}) or {}
    shared = []
    score = 0.0
    if a_infra.get("origin_ip_range") and a_infra.get("origin_ip_range") == b_infra.get("origin_ip_range"):
        shared.append("shared_origin_ip_range")
        score += 0.4
    if a_infra.get("connection_type") and a_infra.get("connection_type") == b_infra.get("connection_type"):
        shared.append("shared_connection_type")
        score += 0.2
    if a_infra.get("user_agent") and a_infra.get("user_agent") == b_infra.get("user_agent"):
        shared.append("shared_user_agent")
        score += 0.4
    if not shared:
        return False, 0.0, ""
    return True, min(1.0, score), f"Infrastructure signals: {', '.join(shared)}"


METHOD_MAP = {
    "username": lambda a, b: exact_username_match(a, b),
    "alias": lambda a, b: fuzzy_alias_match(a, b),
    "pgp": lambda a, b: pgp_match(a, b),
    "wallet": lambda a, b: crypto_wallet_match(a, b),
    "behavioral": lambda a, b: behavioral_pattern_match(a, b),
    "stylometry": lambda a, b: _stylometry_match(a, b),
    "metadata": lambda a, b: metadata_match(a, b),
    "temporal": lambda a, b: temporal_match(a, b),
    "category": lambda a, b: category_match(a, b),
    "graph": lambda a, b: graph_match(a, b),
    "infrastructure": lambda a, b: _infrastructure_match(a, b),
}


def _load_dataset() -> tuple[list[dict], list[dict]]:
    from pathlib import Path
    import json
    DATASET_PATH = Path(__file__).parent.parent.parent / "data" / "shadowlink_synthetic_dataset.json"
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["identities"], data["relationships"]


_IDENTITIES, _RELATIONSHIPS = _load_dataset()


def graph_match(a: dict, b: dict) -> tuple[bool, float, str]:
    for rel in _RELATIONSHIPS:
        if (rel["source_identity_id"] == a["id"] and rel["target_identity_id"] == b["id"]) or \
           (rel["source_identity_id"] == b["id"] and rel["target_identity_id"] == a["id"]):
            return True, rel["confidence_score"], f"Direct relation exists with confidence {rel['confidence_score']:.2f}"
    return False, 0.0, "No direct relationship found"


def correlate(
    db: Session,
    identity_ids: List[str],
    methods: Optional[List[str]] = None,
    min_confidence: float = 0.0,
    persist: bool = True,
) -> dict:
    started = time.perf_counter()
    methods = methods or DEFAULT_METHODS
    invalid = [m for m in methods if m not in METHOD_MAP]
    if invalid:
        raise ValueError(f"Unknown correlation methods: {invalid}")

    rows = (
        db.query(Identity)
        .filter(Identity.id.in_(identity_ids))
        .all()
    )
    if len(rows) < 2:
        raise ValueError("At least two identities are required for correlation")

    found_ids = {r.id for r in rows}
    missing = [i for i in identity_ids if i not in found_ids]
    if missing:
        raise ValueError(f"Unknown identity ids: {missing}")

    identities = [_identity_payload(r) for r in rows]
    pairs = _iter_pairs(identities)

    correlations = []
    for a, b in pairs:
        matches: List[dict] = []
        for method in methods:
            fn = METHOD_MAP[method]
            ok, score, explanation = fn(a, b)
            if ok and score >= min_confidence:
                matches.append(
                    {
                        "source_id": a["id"],
                        "target_id": b["id"],
                        "correlation_type": method,
                        "confidence_score": round(score, 4),
                        "evidence": {"method": method},
                        "explanation": explanation,
                    }
                )
        if not matches:
            continue
        from ml.confidence import aggregate

        combined = aggregate(matches)
        if combined < min_confidence:
            continue
        correlations.append(
            {
                "pair": (a["id"], b["id"]),
                "match_signals": matches,
                "combined_confidence": combined,
            }
        )

    # Persist combined correlations for downstream endpoints.
    if persist:
        for c in correlations:
            for match in c["match_signals"]:
                exists = (
                    db.query(Relation)
                    .filter(
                        Relation.source_identity_id == match["source_id"],
                        Relation.target_identity_id == match["target_id"],
                        Relation.correlation_type == match["correlation_type"],
                    )
                    .first()
                )
                if exists:
                    continue
                db.add(
                    Relation(
                        id=str(uuid.uuid4()),
                        source_identity_id=match["source_id"],
                        target_identity_id=match["target_id"],
                        correlation_type=match["correlation_type"],
                        confidence_score=match["confidence_score"],
                        evidence=match["evidence"],
                        explanation=match["explanation"],
                    )
                )
        db.commit()

    # Flatten match list for response.
    flat: List[dict] = []
    for c in correlations:
        for m in c["match_signals"]:
            flat.append(m)

    duration_ms = round((time.perf_counter() - started) * 1000, 2)
    return {
        "pair_count": len(pairs),
        "identities_analyzed": len(identities),
        "correlations_found": len(flat),
        "correlations": flat,
        "analysis_methods_used": methods,
        "duration_ms": duration_ms,
    }


def classify(score: float) -> str:
    if score >= 0.85:
        return "high"
    if score >= 0.55:
        return "medium"
    if score >= 0.25:
        return "low"
    return "minimal"


def compute_overall_confidence(
    matches: List[dict], weights: Optional[Dict[str, float]] = None
) -> float:
    if not matches:
        return 0.0
    total_weight = sum(weights.values()) if weights else sum(DEFAULT_WEIGHTS.values())
    weighted_sum = 0.0
    for m in matches:
        ctype = m.get("correlation_type", "")
        weight = weights.get(ctype) if weights else DEFAULT_WEIGHTS.get(ctype, 0.0)
        if ctype == "behavioral":
            score = m["confidence_score"] / 0.8 if m["confidence_score"] > 0 else 0.0
        else:
            score = m["confidence_score"]
        weighted_sum += score * weight
    if total_weight == 0:
        return 0.0
    return min(1.0, weighted_sum / total_weight)


def analyze_two_identities(
    id_a: str,
    id_b: str,
    methods: Optional[List[str]] = None,
    min_confidence: float = 0.0,
    weights: Optional[Dict[str, float]] = None,
) -> dict:
    # Load identities
    identity_a = next((i for i in _IDENTITIES if i["id"] == id_a), None)
    identity_b = next((i for i in _IDENTITIES if i["id"] == id_b), None)
    if not identity_a or not identity_b:
        raise ValueError("Identity not found")
    payload_a = _identity_payload(identity_a)
    payload_b = _identity_payload(identity_b)

    matches = []
    for method in methods or DEFAULT_METHODS:
        fn = METHOD_MAP[method]
        ok, score, explanation = fn(payload_a, payload_b)
        if ok and score >= min_confidence:
            matches.append(
                {
                    "source_id": payload_a["id"],
                    "target_id": payload_b["id"],
                    "correlation_type": method,
                    "confidence_score": score,
                    "evidence": {"method": method},
                    "explanation": explanation,
                }
            )

    overall_confidence = compute_overall_confidence(matches, weights)
    risk_level = (
        "LOW"
        if overall_confidence <= 0.25
        else "MEDIUM"
        if overall_confidence <= 0.5
        else "HIGH"
        if overall_confidence <= 0.75
        else "CRITICAL"
    )

    signals = {
        "stylometry": 0,
        "behavior": 0,
        "pgp": 0,
        "wallet": 0,
        "metadata": 0,
        "temporal": 0,
        "category": 0,
        "graph": 0,
    }
    for m in matches:
        key = m["correlation_type"]
        if key == "stylometry":
            signals["stylometry"] = int(m["confidence_score"] * 100)
        elif key == "behavioral":
            signals["behavior"] = int(m["confidence_score"] * 100)
        elif key == "pgp":
            signals["pgp"] = int(m["confidence_score"] * 100)
        elif key == "wallet":
            signals["wallet"] = int(m["confidence_score"] * 100)
        elif key == "metadata":
            signals["metadata"] = int(m["confidence_score"] * 100)
        elif key == "temporal":
            signals["temporal"] = int(m["confidence_score"] * 100)
        elif key == "category":
            signals["category"] = int(m["confidence_score"] * 100)
        elif key == "graph":
            signals["graph"] = int(m["confidence_score"] * 100)

    evidence = [m["explanation"] for m in matches]
    explanation = (
        "Correlation analysis performed using a weighted scoring model. "
        "Each signal contributes based on its individual confidence and assigned weight. "
        "Overall confidence reflects the combined similarity across all signals."
    )

    return {
        "identity_a": payload_a["username"],
        "identity_b": payload_b["username"],
        "correlation_confidence": int(overall_confidence * 100),
        "risk_level": risk_level,
        "signals": signals,
        "evidence": evidence,
        "explanation": explanation,
    }