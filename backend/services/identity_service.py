"""
Identity service — read-side access against the synthetic dataset.
"""
from __future__ import annotations

from typing import List, Optional

from sqlalchemy.orm import Session

from models.identity import Identity


def _to_dict(identity: Identity) -> dict:
    meta = identity.extra_metadata or {}
    return {
        "id": identity.id,
        "username": identity.username,
        "aliases": identity.aliases or [],
        "email": identity.email,
        "pgp_fingerprint": identity.pgp_fingerprint,
        "crypto_wallets": identity.crypto_wallets or [],
        "platform": identity.platform,
        "bio": identity.bio,
        "writing_samples": identity.writing_samples or [],
        "posting_hours": identity.posting_hours or [],
        "categories": identity.categories or [],
        "languages": meta.get("languages", []),
        "risk_score": meta.get("risk_score", 0.0),
        "writing_style_signature": meta.get("writing_style_signature", {}),
        "behavioral_profile": meta.get("behavioral_profile", {}),
        "infrastructure_metadata": meta.get("infrastructure_metadata", {}),
        "posting_timestamps": meta.get("posting_timestamps", []),
        "source_id": identity.source_id,
        "created_at": identity.created_at,
        "updated_at": identity.updated_at,
    }


def list_identities(
    db: Session,
    *,
    page: int = 1,
    page_size: int = 25,
    search: Optional[str] = None,
    platform: Optional[str] = None,
    min_risk: Optional[float] = None,
) -> tuple[List[dict], int]:
    query = db.query(Identity)
    if search:
        like = f"%{search.lower()}%"
        from sqlalchemy import func, or_

        query = query.filter(
            or_(
                func.lower(Identity.username).like(like),
                func.lower(Identity.email).like(like),
            )
        )
    if platform:
        query = query.filter(Identity.platform == platform)

    total = query.count()
    rows = query.order_by(Identity.username.asc()).offset((page - 1) * page_size).limit(page_size).all()
    identities = [_to_dict(row) for row in rows]

    if min_risk is not None:
        identities = [i for i in identities if i["risk_score"] >= min_risk]
    return identities, total


def get_identity(db: Session, identity_id: str) -> Optional[dict]:
    row = db.query(Identity).filter(Identity.id == identity_id).first()
    return _to_dict(row) if row else None


def get_identity_by_username(db: Session, username: str) -> Optional[dict]:
    row = db.query(Identity).filter(Identity.username == username).first()
    return _to_dict(row) if row else None
