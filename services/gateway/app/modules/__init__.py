"""Modules package for BHIV HR Platform Gateway"""

# Import all module routers for easy access
from .auth import router as auth_router
from .candidates import router as candidates_router
from .core import router as core_router
from .jobs import router as jobs_router
from .monitoring import router as monitoring_router
from .workflows import router as workflows_router

__all__ = [
    "core_router",
    "candidates_router",
    "jobs_router",
    "auth_router",
    "workflows_router",
    "monitoring_router",
]
