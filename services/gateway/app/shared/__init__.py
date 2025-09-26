"""Shared utilities and models for BHIV HR Platform Gateway"""

from .database import DatabaseManager, db_manager, get_db_health, get_db_stats
from .models import (
    APIResponse,
    CandidateCreate,
    CandidateUpdate,
    ErrorResponse,
    HealthCheck,
    InterviewCreate,
    JobCreate,
    JobUpdate,
    UserCreate,
    WorkflowCreate,
    WorkflowStatus,
    WorkflowStep,
    WorkflowType,
)

__all__ = [
    "WorkflowStatus",
    "WorkflowType",
    "CandidateCreate",
    "CandidateUpdate",
    "JobCreate",
    "JobUpdate",
    "InterviewCreate",
    "UserCreate",
    "WorkflowStep",
    "WorkflowCreate",
    "APIResponse",
    "ErrorResponse",
    "HealthCheck",
    "DatabaseManager",
    "db_manager",
    "get_db_health",
    "get_db_stats",
]
