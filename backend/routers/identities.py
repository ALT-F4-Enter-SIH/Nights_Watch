"""Identity router — list + detail, with relations per identity."""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from schemas.common import PaginatedResponse
from schemas.identity import IdentityResponse
from services import identity_service, relation_service

router = APIRouter(prefix="/api", tags=["identities"])


def _to_response(payload: dict) -> IdentityResponse:
    return IdentityResponse(
        id=payload["id"],
        username=payload["username"],
        aliases=payload.get("aliases", []),
        email=payload.get("email"),
        pgp_fingerprint=payload.get("pgp_fingerprint"),
        crypto_wallets=payload.get("crypto_wallets", []),
        platform=payload.get("platform"),
        bio=payload.get("bio"),
        writing_samples=payload.get("writing_samples", []),
        posting_hours=payload.get("posting_hours", []),
        categories=payload.get("categories", []),
        metadata={
            **payload.get("metadata", {}),
            "languages": payload.get("languages", []),
            "risk_score": payload.get("risk_score", 0.0),
            "writing_style_signature": payload.get("writing_style_signature", {}),
            "behavioral_profile": payload.get("behavioral_profile", {}),
            "infrastructure_metadata": payload.get("infrastructure_metadata", {}),
        },
        source_id=payload.get("source_id"),
        created_at=payload["created_at"],
        updated_at=payload["updated_at"],
    )


@router.get("/identities", response_model=PaginatedResponse[IdentityResponse])
def list_identities(
    page: int = Query(1, ge=1, le=1000),
    page_size: int = Query(25, ge=1, le=200),
    search: Optional[str] = Query(None, max_length=200),
    platform: Optional[str] = Query(None, max_length=50),
    min_risk: Optional[float] = Query(None, ge=0.0, le=1.0),
    db: Session = Depends(get_db),
) -> PaginatedResponse[IdentityResponse]:
    items, total = identity_service.list_identities(
        db,
        page=page,
        page_size=page_size,
        search=search,
        platform=platform,
        min_risk=min_risk,
    )
    pages = (total + page_size - 1) // page_size if page_size else 1
    return PaginatedResponse[IdentityResponse](
        data=[_to_response(i) for i in items],
        total=total,
        page=page,
        page_size=page_size,
        pages=pages,
    )


@router.get("/identities/{identity_id}", response_model=IdentityResponse)
def get_identity(identity_id: str, db: Session = Depends(get_db)) -> IdentityResponse:
    identity = identity_service.get_identity(db, identity_id)
    if not identity:
        raise HTTPException(status_code=404, detail=f"Identity {identity_id} not found")
    return _to_response(identity)


@router.get("/identities/{identity_id}/relations")
def get_identity_relations(identity_id: str, db: Session = Depends(get_db)):
    return relation_service.get_relations_for_identity(db, identity_id)
