# Database Models and Schemas
from pydantic import BaseModel, EmailStr, validator, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class ExperienceLevel(str, Enum):
    ENTRY = "Entry-level"
    MID = "Mid-level" 
    SENIOR = "Senior"
    LEAD = "Lead"
    EXECUTIVE = "Executive"

class JobType(str, Enum):
    FULL_TIME = "Full-time"
    PART_TIME = "Part-time"
    CONTRACT = "Contract"
    INTERNSHIP = "Internship"
    FREELANCE = "Freelance"

class JobStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    CLOSED = "closed"
    DRAFT = "draft"

# Candidate Models
class CandidateBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., regex=r'^[^@]+@[^@]+\.[^@]+$')
    phone: Optional[str] = Field(None, regex=r'^\+?[\d\s\-\(\)]{10,15}$')
    location: Optional[str] = Field(None, max_length=100)
    experience_years: int = Field(0, ge=0, le=50)
    skills: List[str] = Field(default_factory=list)
    resume_text: Optional[str] = None
    
class CandidateCreate(CandidateBase):
    pass

class CandidateUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[str] = Field(None, regex=r'^[^@]+@[^@]+\.[^@]+$')
    phone: Optional[str] = Field(None, regex=r'^\+?[\d\s\-\(\)]{10,15}$')
    location: Optional[str] = Field(None, max_length=100)
    experience_years: Optional[int] = Field(None, ge=0, le=50)
    skills: Optional[List[str]] = None

class CandidateResponse(CandidateBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

# Job Models
class JobBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=20, max_length=5000)
    requirements: List[str] = Field(..., min_items=1)
    location: str = Field(..., min_length=2, max_length=100)
    department: str = Field(..., min_length=2, max_length=100)
    experience_level: ExperienceLevel
    salary_min: int = Field(..., ge=0, le=10000000)
    salary_max: int = Field(..., ge=0, le=10000000)
    job_type: JobType = JobType.FULL_TIME
    company_id: str = Field(default="default")
    
    @validator('salary_max')
    def validate_salary_range(cls, v, values):
        if 'salary_min' in values and v < values['salary_min']:
            raise ValueError('salary_max must be greater than or equal to salary_min')
        return v

class JobCreate(JobBase):
    pass

class JobUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=5, max_length=200)
    description: Optional[str] = Field(None, min_length=20, max_length=5000)
    requirements: Optional[List[str]] = Field(None, min_items=1)
    location: Optional[str] = Field(None, min_length=2, max_length=100)
    department: Optional[str] = Field(None, min_length=2, max_length=100)
    experience_level: Optional[ExperienceLevel] = None
    salary_min: Optional[int] = Field(None, ge=0, le=10000000)
    salary_max: Optional[int] = Field(None, ge=0, le=10000000)
    job_type: Optional[JobType] = None
    status: Optional[JobStatus] = None

class JobResponse(JobBase):
    id: str
    status: JobStatus = JobStatus.ACTIVE
    created_at: datetime
    updated_at: Optional[datetime] = None
    applications_count: int = 0

# Interview Models
class InterviewBase(BaseModel):
    candidate_id: str = Field(..., min_length=1)
    job_id: str = Field(..., min_length=1)
    interviewer: str = Field(..., min_length=2, max_length=100)
    scheduled_time: datetime
    interview_type: str = Field(default="technical", max_length=50)
    notes: Optional[str] = Field(None, max_length=2000)

class InterviewCreate(InterviewBase):
    pass

class InterviewUpdate(BaseModel):
    interviewer: Optional[str] = Field(None, min_length=2, max_length=100)
    scheduled_time: Optional[datetime] = None
    interview_type: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = Field(None, max_length=2000)
    status: Optional[str] = Field(None, max_length=20)

class InterviewResponse(InterviewBase):
    id: str
    status: str = "scheduled"
    created_at: datetime
    updated_at: Optional[datetime] = None

# Response Models
class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int = 1
    per_page: int = 10
    pages: int

class ErrorResponse(BaseModel):
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None

class SuccessResponse(BaseModel):
    message: str
    data: Optional[Dict[str, Any]] = None