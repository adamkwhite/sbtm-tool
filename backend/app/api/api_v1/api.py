"""
API v1 router aggregation
"""

from fastapi import APIRouter

from app.api.api_v1.endpoints import sessions, projects, charters, testers

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
api_router.include_router(charters.router, prefix="/charters", tags=["charters"])
api_router.include_router(testers.router, prefix="/testers", tags=["testers"])