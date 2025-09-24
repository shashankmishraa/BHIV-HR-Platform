"""Shared Pydantic models for BHIV HR Platform Services"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class CandidateModel(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=2, max_length=255)
    email: str = Field(..., pattern=r'^[^@]+@[^@]+\.[^@]+$')
    phone: Optional[str] = Field(None, max_length=50)
    location: Optional[str] = Field(None, max_length=255)
    experience_years: int = Field(0, ge=0)
    technical_skills: Optional[str] = None
    seniority_level: Optional[str] = Field(None, max_length=100)
    education_level: Optional[str] = Field(None, max_length=255)
    status: str = Field(default="active", max_length=50)

class JobModel(BaseModel):
    id: Optional[int] = None
    title: str = Field(..., min_length=5, max_length=255)
    department: Optional[str] = Field(None, max_length=255)
    location: Optional[str] = Field(None, max_length=255)
    experience_level: Optional[str] = Field(None, max_length=100)
    requirements: Optional[str] = None
    description: Optional[str] = None
    status: str = Field(default="active", max_length=50)
    client_id: Optional[str] = Field(None, max_length=100)

class InterviewModel(BaseModel):
    id: Optional[int] = None
    candidate_id: int = Field(..., gt=0)
    job_id: int = Field(..., gt=0)
    interview_date: Optional[datetime] = None
    status: str = Field(default="scheduled", max_length=50)
    notes: Optional[str] = None
    interviewer: Optional[str] = Field(None, max_length=255)

class FeedbackModel(BaseModel):
    id: Optional[int] = None
    candidate_id: int = Field(..., gt=0)
    job_id: int = Field(..., gt=0)
    integrity: int = Field(..., ge=1, le=5)
    honesty: int = Field(..., ge=1, le=5)
    discipline: int = Field(..., ge=1, le=5)
    hard_work: int = Field(..., ge=1, le=5)
    gratitude: int = Field(..., ge=1, le=5)

class APIResponse(BaseModel):
    success: bool = True
    message: str
    data: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.now)

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.now)