"""API v1 root router aggregation."""

from fastapi import APIRouter
from app.api.v1 import (
    health,
    sources,
    issues,
    stakeholders,
    opportunities,
    analytics,
)

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(sources.router)
api_router.include_router(issues.router)
api_router.include_router(stakeholders.router)
api_router.include_router(opportunities.router)
api_router.include_router(analytics.router)

__all__ = ["api_router"]
