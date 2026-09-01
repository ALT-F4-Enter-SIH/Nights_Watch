"""Graph router — returns the node/edge structure for the relations graph."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database import get_db
from services import graph_service

router = APIRouter(prefix="/api", tags=["graph"])


@router.get("/graph")
def get_graph(
    min_confidence: float = Query(0.0, ge=0.0, le=1.0),
    db: Session = Depends(get_db),
) -> dict:
    return graph_service.build_graph(db, min_confidence=min_confidence)
