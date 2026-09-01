"""Router registry."""
from fastapi import APIRouter

from routers import correlation, dashboard, graph, identities, investigations

api_router = APIRouter()
api_router.include_router(dashboard.router)
api_router.include_router(investigations.router)
api_router.include_router(identities.router)
api_router.include_router(graph.router)
api_router.include_router(correlation.router)

__all__ = ["api_router"]
