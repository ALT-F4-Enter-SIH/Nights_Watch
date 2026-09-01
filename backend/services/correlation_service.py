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
from services import identity_service
from services.correlation_engine import (
    behavioral_pattern_match,
    crypto_wallet_match,
    exact_username_match,
    fuzzy_alias_match,
    pgp_match,
)


DEFAULT_METHODS = ["username", "alias", "pgp", "wallet", "behavioral", "stylometry", "infrastructure"]


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
    "infrastructure": lambda a, b: _infrastructure_match(a, b),
}


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
                        "evidence": {"method": method, "identities": [a["username"], b["username"]]},
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
