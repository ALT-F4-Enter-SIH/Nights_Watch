"""Correlation / ML routers — analyze, stylometry, behavior, infrastructure."""
import time

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from ml.stylometry import measure, stylometry_similarity
from schemas.behavior import BehavioralComparison, BehavioralProfile
from schemas.correlation import (
    CorrelationRequest,
    CorrelationResult,
    IdentityCorrelationResult,
    StylometryRequest,
    StylometryResult,
)
from schemas.infrastructure import InfrastructureAnalysisResult, InfrastructureProfile
from services import (
    behavior_service,
    correlation_service,
    infrastructure_service,
)

router = APIRouter(prefix="/api", tags=["analysis"])


@router.post("/correlation/analyze", response_model=CorrelationResult)
def analyze_correlation(request: CorrelationRequest, db: Session = Depends(get_db)) -> CorrelationResult:
    try:
        result = correlation_service.correlate(
            db,
            identity_ids=request.identity_ids,
            methods=request.methods,
            min_confidence=request.min_confidence,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return CorrelationResult(**result)


@router.post("/correlation/analyze-two", response_model=IdentityCorrelationResult)
def analyze_two_identities(
    identity_id_a: str,
    identity_id_b: str,
    methods: list[str] | None = None,
    min_confidence: float = 0.0,
    weights: dict[str, float] | None = None,
) -> IdentityCorrelationResult:
    try:
        result = correlation_service.analyze_two_identities(
            id_a=identity_id_a,
            id_b=identity_id_b,
            methods=methods,
            min_confidence=min_confidence,
            weights=weights,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return IdentityCorrelationResult(**result)


@router.post("/stylometry/compare", response_model=StylometryResult)
def stylometry_compare(request: StylometryRequest) -> StylometryResult:
    started = time.perf_counter()
    sig_a, sig_b, score, shared_ngrams, vocab_overlap, _ = stylometry_similarity(
        request.text_a, request.text_b
    )
    return StylometryResult(
        similarity_score=score,
        text_a_signature=sig_a,
        text_b_signature=sig_b,
        shared_ngrams=shared_ngrams,
        vocabulary_overlap=vocab_overlap,
        duration_ms=measure(started),
    )


@router.get("/behavior/{identity_id}", response_model=BehavioralProfile)
def get_behavior(identity_id: str, db: Session = Depends(get_db)) -> BehavioralProfile:
    profile = behavior_service.build_profile(db, identity_id)
    if not profile:
        raise HTTPException(status_code=404, detail=f"Identity {identity_id} not found")
    return profile


@router.get("/behavior/compare/{identity_id_a}/{identity_id_b}", response_model=BehavioralComparison)
def compare_behavior(
    identity_id_a: str,
    identity_id_b: str,
    db: Session = Depends(get_db),
) -> BehavioralComparison:
    result = behavior_service.compare(db, identity_id_a, identity_id_b)
    if not result:
        raise HTTPException(status_code=404, detail="One or both identities not found")
    return result


@router.post("/infrastructure/analyze", response_model=InfrastructureAnalysisResult)
def analyze_infrastructure(
    request: dict | None = None,
    db: Session = Depends(get_db),
) -> InfrastructureAnalysisResult:
    identity_ids = None
    if request and isinstance(request, dict):
        identity_ids = request.get("identity_ids")
    if identity_ids is not None and not isinstance(identity_ids, list):
        raise HTTPException(status_code=400, detail="identity_ids must be a list of identity ids")
    return InfrastructureAnalysisResult(**infrastructure_service.analyze(db, identity_ids))


@router.get("/infrastructure/{identity_id}", response_model=InfrastructureProfile)
def get_infrastructure(identity_id: str, db: Session = Depends(get_db)) -> InfrastructureProfile:
    profile = infrastructure_service.profile_for(db, identity_id)
    if not profile:
        raise HTTPException(status_code=404, detail=f"Identity {identity_id} not found")
    return profile
