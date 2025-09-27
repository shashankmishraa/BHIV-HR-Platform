"""OpenAPI Schema definitions for BHIV HR Platform"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# Response Models
class CandidateResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    experience_years: int = 0
    technical_skills: Optional[str] = None
    seniority_level: Optional[str] = None
    education_level: Optional[str] = None
    status: str = "active"
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class JobResponse(BaseModel):
    id: int
    title: str
    department: str
    location: str
    experience_level: str
    requirements: str
    description: str
    status: str = "active"
    client_id: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class PaginatedCandidatesResponse(BaseModel):
    candidates: List[CandidateResponse]
    total: int
    page: int
    per_page: int
    pages: int
    filters: Dict[str, Any]
    error: Optional[str] = None

class PaginatedJobsResponse(BaseModel):
    jobs: List[JobResponse]
    total: int
    page: int
    per_page: int
    pages: int
    filters: Dict[str, Any]
    error: Optional[str] = None

class CandidateStatsResponse(BaseModel):
    total_candidates: int
    active_candidates: int
    by_experience: Dict[str, int]
    by_location: Dict[str, int]
    timestamp: str
    error: Optional[str] = None

class JobAnalyticsResponse(BaseModel):
    total_jobs: int
    active_jobs: int
    by_department: Dict[str, int]
    timestamp: str
    error: Optional[str] = None

class ErrorResponse(BaseModel):
    error: str
    timestamp: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

# AI Agent Response Models
class CandidateScore(BaseModel):
    candidate_id: int
    name: str
    email: str
    score: float = Field(..., ge=0, le=100)
    skills_match: List[str]
    experience_match: str
    location_match: bool
    reasoning: str

class MatchResponse(BaseModel):
    job_id: int
    top_candidates: List[CandidateScore]
    total_candidates: int
    processing_time: float
    algorithm_version: str
    status: str

class AnalyticsResponse(BaseModel):
    avg_match_time: str
    accuracy: str
    total_matches: int
    success_rate: str

class ModelStatus(BaseModel):
    name: str
    status: str
    version: str

class ModelsStatusResponse(BaseModel):
    models: List[ModelStatus]
    total: int

# Request Models
class MatchRequest(BaseModel):
    job_id: int = Field(..., gt=0)

class CandidateAnalysisResponse(BaseModel):
    candidate_id: int
    name: str
    email: str
    experience_years: int
    seniority_level: Optional[str] = None
    education_level: Optional[str] = None
    location: Optional[str] = None
    skills_analysis: Dict[str, List[str]]
    total_skills: int
    analysis_timestamp: str
    status: str
    error: Optional[str] = None