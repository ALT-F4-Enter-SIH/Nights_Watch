"""Investigation router — list, detail, reports."""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from schemas.investigation import InvestigationResponse
from schemas.report import ReportResponse
from services import investigation_service, report_service

router = APIRouter(prefix="/api", tags=["investigations"])


@router.get("/investigations", response_model=list[InvestigationResponse])
def list_investigations(
    status: Optional[str] = Query(None, pattern="^(open|in_review|closed|suspended)$"),
    priority: Optional[str] = Query(None, pattern="^(low|medium|high|critical)$"),
    db: Session = Depends(get_db),
) -> list[InvestigationResponse]:
    return investigation_service.list_investigations(db, status=status, priority=priority)


@router.get("/investigations/{investigation_id}", response_model=InvestigationResponse)
def get_investigation(investigation_id: str, db: Session = Depends(get_db)) -> InvestigationResponse:
    investigation = investigation_service.get_investigation(db, investigation_id)
    if not investigation:
        raise HTTPException(status_code=404, detail=f"Investigation {investigation_id} not found")
    return investigation


@router.get("/reports/{report_id}", response_model=ReportResponse)
def get_report(report_id: str, db: Session = Depends(get_db)) -> ReportResponse:
    return report_service.generate(db, report_id)
