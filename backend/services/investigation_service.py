"""
Investigation service — read access for investigations.
"""
from __future__ import annotations

from typing import List, Optional

from sqlalchemy.orm import Session

from models.investigation import Investigation


def list_investigations(
    db: Session,
    *,
    status: Optional[str] = None,
    priority: Optional[str] = None,
) -> List[dict]:
    query = db.query(Investigation)
    if status:
        query = query.filter(Investigation.status == status)
    if priority:
        query = query.filter(Investigation.priority == priority)
    rows = query.order_by(Investigation.created_at.desc()).all()
    return [_to_dict(r) for r in rows]


def get_investigation(db: Session, investigation_id: str) -> Optional[dict]:
    row = db.query(Investigation).filter(Investigation.id == investigation_id).first()
    return _to_dict(row) if row else None


def _to_dict(inv: Investigation) -> dict:
    return {
        "id": inv.id,
        "title": inv.title,
        "description": inv.description,
        "status": inv.status,
        "priority": inv.priority,
        "linked_identities": inv.linked_identities or [],
        "evidence_items": inv.evidence_items or [],
        "notes": inv.notes,
        "created_at": inv.created_at,
        "updated_at": inv.updated_at,
    }
