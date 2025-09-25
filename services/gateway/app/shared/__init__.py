"""Shared utilities and models for BHIV HR Platform Gateway"""

from .models import (
    WorkflowStatus,
    WorkflowType,
    CandidateCreate,
    CandidateUpdate,
    JobCreate,
    JobUpdate,
    InterviewCreate,
    UserCreate,
    WorkflowStep,
    WorkflowCreate,
    APIResponse,
    ErrorResponse,
    HealthCheck,
)
from .database import DatabaseManager, db_manager, get_db_health, get_db_stats

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
