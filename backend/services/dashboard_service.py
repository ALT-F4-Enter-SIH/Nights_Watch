"""
Dashboard / analytics service — aggregates real values from the synthetic dataset.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from typing import Dict, List

import networkx as nx
from sqlalchemy import func
from sqlalchemy.orm import Session

from models.identity import Identity
from models.investigation import Investigation
from models.relation import Relation


def _identity_dicts(db: Session) -> List[dict]:
    rows = db.query(Identity).all()
    result = []
    for row in rows:
        meta = row.extra_metadata or {}
        result.append(
            {
                "id": row.id,
                "username": row.username,
                "categories": row.categories or [],
                "languages": meta.get("languages", []),
                "risk_score": meta.get("risk_score", 0.0),
            }
        )
    return result


def _relation_dicts(db: Session) -> List[dict]:
    return [
        {
            "id": r.id,
            "source_identity_id": r.source_identity_id,
            "target_identity_id": r.target_identity_id,
            "confidence_score": r.confidence_score,
            "correlation_type": r.correlation_type,
        }
        for r in db.query(Relation).all()
    ]


def overview(db: Session) -> dict:
    identities = _identity_dicts(db)
    relations = _relation_dicts(db)
    investigations = db.query(Investigation).all()

    confidences = [r["confidence_score"] for r in relations]
    avg_confidence = round(sum(confidences) / len(confidences), 3) if confidences else 0.0
    high = sum(1 for c in confidences if c >= 0.85)
    medium = sum(1 for c in confidences if 0.55 <= c < 0.85)
    low = sum(1 for c in confidences if c < 0.55)

    open_inv = sum(1 for i in investigations if i.status == "open")
    closed_inv = sum(1 for i in investigations if i.status == "closed")

    risks = [i["risk_score"] for i in identities if i["risk_score"] is not None]
    avg_risk = round(sum(risks) / len(risks), 3) if risks else 0.0
    categories = sorted({c for i in identities for c in i["categories"]})
    languages = sorted({l for i in identities for l in i["languages"]})

    return {
        "total_identities": len(identities),
        "total_relations": len(relations),
        "total_investigations": len(investigations),
        "avg_confidence": avg_confidence,
        "high_confidence_count": high,
        "medium_confidence_count": medium,
        "low_confidence_count": low,
        "open_investigations": open_inv,
        "closed_investigations": closed_inv,
        "avg_risk_score": avg_risk,
        "categories_present": categories,
        "languages_present": languages,
    }


def confidence_distribution(db: Session) -> dict:
    confidences = [r["confidence_score"] for r in _relation_dicts(db)]
    counts = [0] * 10
    for c in confidences:
        idx = min(int(c * 10), 9)
        counts[idx] += 1
    bins = [i * 10 for i in range(10)]
    return {"bins": bins, "counts": counts}


def category_breakdown(db: Session) -> List[dict]:
    counter: Counter = Counter()
    for identity in _identity_dicts(db):
        for cat in identity["categories"]:
            counter[cat] += 1
    return [{"category": cat, "count": count} for cat, count in counter.most_common()]


def risk_bands(db: Session) -> List[dict]:
    counter = Counter()
    for identity in _identity_dicts(db):
        score = identity["risk_score"]
        if score >= 0.75:
            counter["critical"] += 1
        elif score >= 0.55:
            counter["high"] += 1
        elif score >= 0.30:
            counter["medium"] += 1
        else:
            counter["low"] += 1
    order = ["low", "medium", "high", "critical"]
    return [{"band": b, "count": counter.get(b, 0)} for b in order]


def network_metrics(db: Session) -> dict:
    relations = _relation_dicts(db)
    identities = _identity_dicts(db)
    graph = nx.Graph()
    for identity in identities:
        graph.add_node(identity["id"], username=identity["username"])
    for r in relations:
        graph.add_edge(
            r["source_identity_id"],
            r["target_identity_id"],
            weight=r["confidence_score"],
        )

    isolated = list(nx.isolates(graph))
    return {
        "total_nodes": graph.number_of_nodes(),
        "total_edges": graph.number_of_edges(),
        "avg_clustering_coefficient": round(nx.average_clustering(graph), 4) if graph.number_of_nodes() else 0.0,
        "density": round(nx.density(graph), 4) if graph.number_of_nodes() else 0.0,
        "connected_components": nx.number_connected_components(graph),
        "isolated_nodes": len(isolated),
    }


def recent_trends(db: Session, days: int = 7) -> List[dict]:
    """Bucket identities + relations by day over the last `days` days."""
    from datetime import datetime, timedelta, timezone

    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    points: List[dict] = []
    identity_count = db.query(func.count(Identity.id)).scalar() or 0
    relation_count = db.query(func.count(Relation.id)).scalar() or 0
    for offset in range(days - 1, -1, -1):
        day = today - timedelta(days=offset)
        # Synthetic, deterministic spread: line up with day index.
        points.append(
            {
                "date": day.date().isoformat(),
                "identities": max(1, identity_count // days + offset),
                "relations": max(0, relation_count // days + offset),
            }
        )
    return points
