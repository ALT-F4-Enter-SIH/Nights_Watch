"""
Relation service — read-side access to the synthetic relation table.
"""
from __future__ import annotations

from typing import List, Optional

from sqlalchemy.orm import Session

from models.identity import Identity
from models.relation import Relation


def _username(db: Session, identity_id: str) -> str:
    row = db.query(Identity).filter(Identity.id == identity_id).first()
    return row.username if row else "unknown"


def _to_dict(db: Session, rel: Relation) -> dict:
    return {
        "id": rel.id,
        "source_identity_id": rel.source_identity_id,
        "source_username": _username(db, rel.source_identity_id),
        "target_identity_id": rel.target_identity_id,
        "target_username": _username(db, rel.target_identity_id),
        "correlation_type": rel.correlation_type,
        "confidence_score": rel.confidence_score,
        "evidence": rel.evidence or {},
        "explanation": rel.explanation,
        "created_at": rel.created_at,
    }


def list_relations(
    db: Session,
    *,
    page: int = 1,
    page_size: int = 50,
    correlation_type: Optional[str] = None,
    min_confidence: float = 0.0,
    max_confidence: float = 1.0,
) -> tuple[List[dict], int]:
    query = db.query(Relation)
    if correlation_type:
        query = query.filter(Relation.correlation_type == correlation_type)
    query = query.filter(
        Relation.confidence_score >= min_confidence,
        Relation.confidence_score <= max_confidence,
    )
    total = query.count()
    rows = (
        query.order_by(Relation.confidence_score.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return [_to_dict(db, r) for r in rows], total


def get_relations_for_identity(db: Session, identity_id: str) -> List[dict]:
    rows = (
        db.query(Relation)
        .filter(
            (Relation.source_identity_id == identity_id)
            | (Relation.target_identity_id == identity_id)
        )
        .order_by(Relation.confidence_score.desc())
        .all()
    )
    return [_to_dict(db, r) for r in rows]


def relation_stats(db: Session) -> dict:
    from sqlalchemy import func

    rows = (
        db.query(Relation.correlation_type, func.count(Relation.id), func.avg(Relation.confidence_score))
        .group_by(Relation.correlation_type)
        .all()
    )
    return {
        ctype: {"count": count, "avg_confidence": round(float(avg or 0.0), 3)}
        for ctype, count, avg in rows
    }
