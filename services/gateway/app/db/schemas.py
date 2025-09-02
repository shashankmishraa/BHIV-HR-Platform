from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime

class JobCreate(BaseModel):
    title: str = Field(..., example="Senior Python Developer")
    description: str = Field(..., example="Looking for experienced Python developer with AI/ML skills")
    client_id: int = Field(..., example=1)
    department: Optional[str] = Field(None, example="Engineering")
    location: Optional[str] = Field(None, example="Remote")
    experience_level: Optional[str] = Field(None, example="Senior")
    employment_type: Optional[str] = Field(None, example="Full-time")
    requirements: Optional[str] = Field(None, example="5+ years Python experience")
    status: Optional[str] = Field("active", example="active")

class FeedbackCreate(BaseModel):
    candidate_id: int
    reviewer: Optional[str] = Field(None, example="HR Manager")
    feedback_text: Optional[str] = Field(None, example="Excellent candidate with strong technical skills")
    values_scores: Optional[Dict[str, int]] = Field(None, example={
        "integrity": 5, "honesty": 4, "discipline": 5, "hard_work": 5, "gratitude": 4
    })

class InterviewCreate(BaseModel):
    job_id: int = Field(..., example=1)
    candidate_id: int = Field(..., example=2)
    interview_date: datetime = Field(..., example="2025-02-01T10:00:00Z")
    interviewer: Optional[str] = Field(None, example="Tech Lead")

class OfferCreate(BaseModel):
    job_id: int = Field(..., example=1)
    candidate_id: int = Field(..., example=2)
    salary: Optional[int] = Field(None, example=120000)
    status: str = Field(..., example="sent")

class CandidateCreate(BaseModel):
    name: str
    email: str = ""
    cv_url: str = ""
    phone: str = ""
    experience_years: int = 0
    status: str = "applied"
    location: str = ""
    education_level: str = ""
    technical_skills: str = ""
    seniority_level: str = ""

class BulkCandidatesRequest(BaseModel):
    candidates: list[CandidateCreate]