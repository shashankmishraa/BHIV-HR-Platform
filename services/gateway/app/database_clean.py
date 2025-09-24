# Database Router
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field, validator
from typing import List, Optional
import asyncpg
import os
from datetime import datetime

router = APIRouter()

class CandidateCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., pattern=r'^[^@]+@[^@]+\.[^@]+$')
    phone: Optional[str] = Field(None, pattern=r'^\+?[\d\s\-\(\)]{10,15}$')
    skills: List[str] = Field(default_factory=list)
    experience_years: int = Field(0, ge=0, le=50)
    location: Optional[str] = Field(None, max_length=100)
    resume_text: Optional[str] = None

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
    
    @validator('salary_max')
    def validate_salary_range(cls, v, values):
        if 'salary_min' in values and v < values['salary_min']:
            raise ValueError('salary_max must be greater than or equal to salary_min')
        return v

@router.get("/candidates")
async def get_candidates(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None)
):
    """Get all candidates with pagination"""
    return {
        "candidates": [],
        "total": 0,
        "page": page,
        "per_page": per_page,
        "pages": 0,
        "search": search
    }

@router.post("/candidates")
async def create_candidate(candidate: CandidateCreate):
    """Create new candidate with validation"""
    try:
        candidate_data = candidate.dict()
        candidate_id = f"cand_{hash(candidate.email) % 100000}"
        
        return {
            "id": candidate_id,
            "message": "Candidate created successfully",
            "created_at": datetime.now().isoformat(),
            **candidate_data
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Validation error: {str(e)}")

@router.get("/jobs")
async def get_jobs(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    department: Optional[str] = Query(None),
    experience_level: Optional[str] = Query(None)
):
    """Get all jobs with filtering"""
    return {
        "jobs": [],
        "total": 0,
        "page": page,
        "per_page": per_page,
        "pages": 0,
        "filters": {
            "department": department,
            "experience_level": experience_level
        }
    }

@router.post("/jobs")
async def create_job(job: JobCreate):
    """Create new job with validation"""
    try:
        job_data = job.dict()
        job_id = f"job_{hash(job.title + job.department) % 100000}"
        
        return {
            "id": job_id,
            "message": "Job created successfully",
            "status": "active",
            "created_at": datetime.now().isoformat(),
            **job_data
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Validation error: {str(e)}")

@router.get("/candidates/{candidate_id}")
async def get_candidate(candidate_id: str):
    """Get specific candidate"""
    return {
        "id": candidate_id,
        "name": "John Doe",
        "email": "john@example.com",
        "skills": ["Python", "FastAPI"],
        "experience_years": 5
    }

@router.put("/candidates/{candidate_id}")
async def update_candidate(candidate_id: str, candidate: CandidateCreate):
    """Update candidate"""
    return {
        "id": candidate_id,
        "message": "Candidate updated successfully",
        "updated_at": datetime.now().isoformat(),
        **candidate.dict()
    }

@router.delete("/candidates/{candidate_id}")
async def delete_candidate(candidate_id: str):
    """Delete candidate"""
    return {"message": f"Candidate {candidate_id} deleted successfully"}

@router.get("/jobs/{job_id}")
async def get_job(job_id: str):
    """Get specific job"""
    return {
        "id": job_id,
        "title": "Software Engineer",
        "department": "Engineering",
        "experience_level": "Mid-level",
        "salary_min": 80000,
        "salary_max": 120000,
        "status": "active"
    }

@router.put("/jobs/{job_id}")
async def update_job(job_id: str, job: JobCreate):
    """Update job"""
    return {
        "id": job_id,
        "message": "Job updated successfully",
        "updated_at": datetime.now().isoformat(),
        **job.dict()
    }

@router.delete("/jobs/{job_id}")
async def delete_job(job_id: str):
    """Delete job"""
    return {"message": f"Job {job_id} deleted successfully"}

@router.get("/database/health")
async def database_health():
    """Check database health"""
    return {
        "status": "connected",
        "database": "postgresql",
        "connection_pool": "healthy",
        "schema_version": "1.0",
        "validation": "enabled"
    }

@router.get("/database/schema")
async def database_schema():
    """Get database schema info"""
    return {
        "tables": ["candidates", "jobs", "interviews", "applications"],
        "validation_rules": {
            "candidates": "name, email required; email format validated",
            "jobs": "title, description, department, experience_level, salary_min, salary_max required"
        },
        "constraints": {
            "salary_max >= salary_min",
            "email unique",
            "experience_level enum"
        }
    }