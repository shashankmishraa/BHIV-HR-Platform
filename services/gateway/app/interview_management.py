# Interview Management Router
from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

router = APIRouter()

class InterviewCreate(BaseModel):
    candidate_id: str
    job_id: str
    interviewer: str
    scheduled_time: datetime
    interview_type: str = "technical"
    notes: Optional[str] = None

@router.get("/interviews")
async def list_interviews():
    """List all interviews"""
    return {
        "interviews": [],
        "total": 0
    }

@router.post("/interviews")
async def create_interview(interview: InterviewCreate):
    """Create new interview"""
    return {
        "id": "interview_123",
        "message": "Interview scheduled successfully",
        **interview.dict()
    }

@router.get("/interviews/{interview_id}")
async def get_interview(interview_id: str):
    """Get specific interview"""
    return {
        "id": interview_id,
        "status": "scheduled",
        "candidate_id": "cand_123",
        "job_id": "job_123"
    }

@router.put("/interviews/{interview_id}/status")
async def update_interview_status(interview_id: str, status: str):
    """Update interview status"""
    return {
        "id": interview_id,
        "status": status,
        "message": "Interview status updated"
    }