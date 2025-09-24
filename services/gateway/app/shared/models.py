"""Shared Pydantic models for the BHIV HR Platform Gateway"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum

class WorkflowStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class WorkflowType(str, Enum):
    CANDIDATE_ONBOARDING = "candidate_onboarding"
    JOB_POSTING = "job_posting"
    INTERVIEW_PROCESS = "interview_process"
    HIRING_PIPELINE = "hiring_pipeline"
    BULK_OPERATIONS = "bulk_operations"
    SECURITY_AUDIT = "security_audit"

class CandidateCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., pattern=r'^[^@]+@[^@]+\.[^@]+$')
    phone: Optional[str] = Field(None, pattern=r'^\+?[\d\s\-\(\)]{10,15}$')
    skills: List[str] = Field(default_factory=list)
    experience_years: int = Field(0, ge=0, le=50)
    location: Optional[str] = Field(None, max_length=100)
    designation: Optional[str] = Field(None, max_length=100)
    education: Optional[str] = Field(None, max_length=100)

class CandidateUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[str] = Field(None, pattern=r'^[^@]+@[^@]+\.[^@]+$')
    phone: Optional[str] = Field(None, pattern=r'^\+?[\d\s\-\(\)]{10,15}$')
    skills: Optional[List[str]] = None
    experience_years: Optional[int] = Field(None, ge=0, le=50)
    location: Optional[str] = Field(None, max_length=100)
    designation: Optional[str] = Field(None, max_length=100)
    education: Optional[str] = Field(None, max_length=100)

class JobCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=20, max_length=5000)
    requirements: List[str] = Field(..., min_items=1)
    location: str = Field(..., min_length=2, max_length=100)
    department: str = Field(..., min_length=2, max_length=100)
    experience_level: str = Field(..., pattern=r'^(Entry-level|Mid-level|Senior|Lead|Executive)$')
    salary_min: int = Field(..., ge=0, le=10000000)
    salary_max: int = Field(..., ge=0, le=10000000)
    job_type: str = Field(default="Full-time")
    company_id: str = Field(default="default")

class JobUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=5, max_length=200)
    description: Optional[str] = Field(None, min_length=20, max_length=5000)
    requirements: Optional[List[str]] = Field(None, min_items=1)
    location: Optional[str] = Field(None, min_length=2, max_length=100)
    department: Optional[str] = Field(None, min_length=2, max_length=100)
    experience_level: Optional[str] = Field(None, pattern=r'^(Entry-level|Mid-level|Senior|Lead|Executive)$')
    salary_min: Optional[int] = Field(None, ge=0, le=10000000)
    salary_max: Optional[int] = Field(None, ge=0, le=10000000)
    job_type: Optional[str] = None

class InterviewCreate(BaseModel):
    candidate_id: str = Field(..., min_length=1)
    job_id: str = Field(..., min_length=1)
    interviewer: str = Field(..., min_length=2, max_length=100)
    scheduled_time: datetime
    interview_type: str = Field(default="technical", max_length=50)
    notes: Optional[str] = Field(None, max_length=2000)

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r'^[^@]+@[^@]+\.[^@]+$')
    password: str = Field(..., min_length=8)
    role: str = Field(default="user")

class WorkflowStep(BaseModel):
    step_id: str
    name: str
    status: WorkflowStatus = WorkflowStatus.PENDING
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    output: Optional[Dict[str, Any]] = None

class WorkflowCreate(BaseModel):
    workflow_type: WorkflowType
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

class APIResponse(BaseModel):
    success: bool = True
    message: str
    data: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    request_id: Optional[str] = None

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    request_id: Optional[str] = None

class HealthCheck(BaseModel):
    status: str
    service: str
    version: str
    timestamp: datetime
    components: Optional[Dict[str, str]] = None
    uptime: Optional[str] = None