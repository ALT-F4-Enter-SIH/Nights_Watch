"""Dashboard router — aggregated analytics."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas.dashboard import (
    DashboardResponse,
)
from services import dashboard_service

router = APIRouter(prefix="/api", tags=["dashboard"])


@router.get("/dashboard", response_model=DashboardResponse)
def get_dashboard(db: Session = Depends(get_db)) -> DashboardResponse:
    return DashboardResponse(
        overview=dashboard_service.overview(db),
        confidence_distribution=dashboard_service.confidence_distribution(db),
        category_breakdown=dashboard_service.category_breakdown(db),
        risk_bands=dashboard_service.risk_bands(db),
        network_metrics=dashboard_service.network_metrics(db),
        recent_trends=dashboard_service.recent_trends(db),
    )
