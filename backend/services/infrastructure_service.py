"""
Infrastructure service — reads and analyzes infrastructure metadata for synthetic identities.
"""
from __future__ import annotations

import time
from itertools import combinations
from typing import List, Optional

from sqlalchemy.orm import Session

from models.identity import Identity


def _payload(identity: Identity) -> dict:
    meta = identity.extra_metadata or {}
    infra = meta.get("infrastructure_metadata", {}) or {}
    email_domain = identity.email.split("@", 1)[1] if identity.email and "@" in identity.email else None
    return {
        "id": identity.id,
        "username": identity.username,
        "origin_ip_range": infra.get("origin_ip_range"),
        "user_agent": infra.get("user_agent"),
        "connection_type": infra.get("connection_type"),
        "platform_tags": infra.get("platform_tags", []),
        "pgp_fingerprint": identity.pgp_fingerprint,
        "crypto_wallets": identity.crypto_wallets or [],
        "email_domain": email_domain,
    }


def profile_for(db: Session, identity_id: str) -> Optional[dict]:
    row = db.query(Identity).filter(Identity.id == identity_id).first()
    if not row:
        return None
    data = _payload(row)
    # Synthetic signal: cluster members share a PGP fingerprint -> high infrastructure score.
    score = 0.0
    if data["pgp_fingerprint"]:
        score += 0.3
    if data["origin_ip_range"]:
        score += 0.2
    if data["user_agent"]:
        score += 0.2
    if data["connection_type"]:
        score += 0.15
    if data["email_domain"]:
        score += 0.15
    return {
        **data,
        "infrastructure_score": round(min(1.0, score), 4),
    }


def analyze(db: Session, identity_ids: Optional[List[str]] = None) -> dict:
    started = time.perf_counter()
    if identity_ids is None:
        rows = db.query(Identity).all()
        profiles = [_payload(r) for r in rows]
    else:
        rows = db.query(Identity).filter(Identity.id.in_(identity_ids)).all()
        profiles = [_payload(r) for r in rows]

    links = []
    for a, b in combinations(profiles, 2):
        shared = []
        score = 0.0
        if a["pgp_fingerprint"] and a["pgp_fingerprint"] == b["pgp_fingerprint"]:
            shared.append("shared_pgp")
            score += 0.45
        if a["origin_ip_range"] and a["origin_ip_range"] == b["origin_ip_range"]:
            shared.append("shared_origin_ip_range")
            score += 0.2
        if a["user_agent"] and a["user_agent"] == b["user_agent"]:
            shared.append("shared_user_agent")
            score += 0.2
        if a["connection_type"] and a["connection_type"] == b["connection_type"]:
            shared.append("shared_connection_type")
            score += 0.1
        if a["crypto_wallets"] and b["crypto_wallets"]:
            if a["crypto_wallets"][0][:6] == b["crypto_wallets"][0][:6]:
                shared.append("shared_wallet_prefix")
                score += 0.25
        if not shared:
            continue
        confidence = round(min(1.0, score), 4)
        links.append(
            {
                "source_id": a["id"],
                "target_id": b["id"],
                "shared_ip_range": "shared_origin_ip_range" in shared,
                "shared_pgp": "shared_pgp" in shared,
                "shared_wallet_prefix": "shared_wallet_prefix" in shared,
                "shared_connection_type": "shared_connection_type" in shared,
                "shared_user_agent_pattern": "shared_user_agent" in shared,
                "infrastructure_confidence": confidence,
                "shared_signals": shared,
                "explanation": "Shared infrastructure signals: " + ", ".join(shared),
            }
        )

    duration_ms = round((time.perf_counter() - started) * 1000, 2)
    return {
        "analyzed_pairs": sum(1 for _ in combinations(profiles, 2)),
        "infrastructure_links_found": len(links),
        "links": links,
        "method": "metadata_fingerprint",
        "duration_ms": duration_ms,
    }
