"""Modules package for BHIV HR Platform Gateway"""

# Import all module routers for easy access
from app.modules.core import router as core_router
from app.modules.candidates import router as candidates_router
from app.modules.jobs import router as jobs_router
from app.modules.auth import router as auth_router
from app.modules.workflows import router as workflows_router
from app.modules.monitoring import router as monitoring_router

__all__ = [
    "core_router",
    "candidates_router", 
    "jobs_router",
    "auth_router",
    "workflows_router",
    "monitoring_router"
]