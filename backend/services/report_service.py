"""
Report service — synthesises a structured report from the synthetic dataset.
"""
from __future__ import annotations

import hashlib
import time
from collections import defaultdict
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy.orm import Session

from models.investigation import Investigation
from models.relation import Relation
from services.identity_service import get_identity


def _username_by_id(db: Session) -> dict:
    from models.identity import Identity

    return {row.id: row.username for row in db.query(Identity).all()}


def _cluster_summaries(db: Session) -> List[dict]:
    relations = db.query(Relation).all()
    usernames = _username_by_id(db)
    clusters: dict[str, list[Relation]] = defaultdict(list)
    for r in relations:
        if r.correlation_type == "hidden_cluster":
            evidence = r.evidence or {}
            cluster = evidence.get("cluster", "unknown")
            clusters[cluster].append(r)

    summaries: List[dict] = []
    for name, items in clusters.items():
        members = set()
        for item in items:
            members.add(usernames.get(item.source_identity_id, ""))
            members.add(usernames.get(item.target_identity_id, ""))
        members.discard("")
        signals = set()
        for item in items:
            evidence = item.evidence or {}
            signals.update(evidence.keys())
        signals.discard("method")
        avg_conf = round(sum(i.confidence_score for i in items) / max(1, len(items)), 3)
        summaries.append(
            {
                "name": name,
                "member_count": len(members),
                "members": sorted(members),
                "shared_signals": sorted(signals),
                "avg_confidence": avg_conf,
            }
        )
    return summaries


def _correlations(db: Session) -> List[dict]:
    usernames = _username_by_id(db)
    relations = db.query(Relation).all()
    return [
        {
            "identity_a": usernames.get(r.source_identity_id, "unknown"),
            "identity_b": usernames.get(r.target_identity_id, "unknown"),
            "confidence_score": r.confidence_score,
            "correlation_type": r.correlation_type,
            "explanation": r.explanation or "",
        }
        for r in relations
    ]


def _sections(db: Session, investigation: Optional[Investigation], clusters: List[dict], correlations: List[dict]) -> List[dict]:
    section_input = (
        f"Investigation: {investigation.title}\n"
        f"Description: {investigation.description or 'N/A'}\n"
        f"Status: {investigation.status}\n"
        f"Priority: {investigation.priority}"
    ) if investigation else "Synthetic dataset overview — no specific investigation scoped."

    return [
        {
            "title": "Executive Summary",
            "content": (
                f"Detected {len(clusters)} hidden identity clusters and "
                f"{len(correlations)} total correlations across the synthetic dataset. "
                "All signals are derived from mock telemetry and authorized research artifacts."
            ),
        },
        {
            "title": "Investigation Scope",
            "content": section_input,
        },
        {
            "title": "Cluster Findings",
            "content": "\n".join(
                f"- {c['name']}: {c['member_count']} members ({', '.join(c['members'])}) "
                f"avg confidence {c['avg_confidence']}"
                for c in clusters
            ) or "No hidden clusters detected.",
        },
        {
            "title": "Methodology",
            "content": (
                "Correlations combine username, alias, PGP, wallet, behavioral, stylometry, "
                "and infrastructure signals. Confidence is the weighted aggregate of all signals."
            ),
        },
    ]


def generate(db: Session, report_id: str) -> dict:
    # report_id currently is interpreted as an investigation id, or as a free-form report key.
    investigation = (
        db.query(Investigation).filter(Investigation.id == report_id).first()
    )
    clusters = _cluster_summaries(db)
    correlations = _correlations(db)
    sections = _sections(db, investigation, clusters, correlations)

    digest = hashlib.sha256(
        f"{report_id}-{time.time()}".encode()
    ).hexdigest()[:12]

    return {
        "report_id": f"rpt_{digest}",
        "investigation_id": investigation.id if investigation else None,
        "title": f"ShadowLink Synthetic Report — {investigation.title if investigation else 'Overview'}",
        "generated_at": datetime.now(timezone.utc),
        "summary": (
            f"Reviewed {len(clusters)} clusters and {len(correlations)} correlation entries."
        ),
        "sections": sections,
        "clusters": clusters,
        "correlations": correlations,
        "total_identities_analyzed": len(_username_by_id(db)),
        "total_correlations_found": len(correlations),
        "methodology": (
            "Weighted correlation across username, alias, PGP, wallet, behavioral, "
            "stylometry, and infrastructure signals. Synthetic mock dataset only."
        ),
    }
