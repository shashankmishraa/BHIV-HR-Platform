from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime

class JobBase(BaseModel):
    title: str
    description: str

class JobCreate(JobBase):
    client_id: int

class Job(JobBase):
    id: int
    client_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class CandidateBase(BaseModel):
    name: str
    cv_url: str
    status: Optional[str] = "applied"
    metadata_json: Optional[Dict[str, Any]] = {}

class CandidateCreate(CandidateBase):
    job_id: int

class CandidateBulkCreate(BaseModel):
    candidates: List[CandidateCreate]

class Candidate(CandidateBase):
    id: int
    job_id: int
    
    model_config = ConfigDict(from_attributes=True)

class FeedbackBase(BaseModel):
    reviewer: str
    free_text: Optional[str] = None
    values_scores: Optional[Dict[str, int]] = {}

class FeedbackCreate(FeedbackBase):
    candidate_id: int

class Feedback(FeedbackBase):
    id: int
    candidate_id: int
    
    model_config = ConfigDict(from_attributes=True)

class InterviewCreate(BaseModel):
    job_id: int
    candidate_id: int
    datetime: datetime
    status: Optional[str] = "scheduled"

class OfferCreate(BaseModel):
    job_id: int
    candidate_id: int
    status: str
    date_offered: datetime
