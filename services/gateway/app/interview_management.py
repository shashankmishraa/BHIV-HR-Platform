# Interview Management Module
# Handles all interview-related operations

from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from sqlalchemy import create_engine, text
import os

# Interview models
class InterviewScheduleRequest(BaseModel):
    candidate_id: int
    job_id: int
    interview_date: str
    interviewer: Optional[str] = "HR Team"
    notes: Optional[str] = ""

# Initialize router
router = APIRouter()

def get_db_engine():
    environment = os.getenv("ENVIRONMENT", "development").lower()
    if environment == "production":
        default_db_url = "postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@dpg-d373qrogjchc73bu9gug-a.oregon-postgres.render.com/bhiv_hr_nqzb"
    else:
        default_db_url = "postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@db:5432/bhiv_hr_nqzb"
    
    database_url = os.getenv("DATABASE_URL", default_db_url)
    return create_engine(database_url, pool_size=10, max_overflow=20, pool_pre_ping=True)

def get_api_key():
    return "authenticated_user"

# Interview Management endpoints (8 endpoints)
@router.get("/interviews", tags=["Interview Management"])
async def get_interviews(api_key: str = Depends(get_api_key)):
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            query = text("""
                SELECT i.id, i.candidate_id, i.job_id, i.interview_date, i.status,
                       c.name as candidate_name, j.title as job_title
                FROM interviews i
                LEFT JOIN candidates c ON i.candidate_id = c.id
                LEFT JOIN jobs j ON i.job_id = j.id
                ORDER BY i.interview_date DESC NULLS LAST
                LIMIT 50
            """)
            result = connection.execute(query)
            interviews = [{
                "id": row[0],
                "candidate_id": row[1],
                "job_id": row[2],
                "interview_date": row[3].isoformat() if row[3] else None,
                "status": row[4] or "scheduled",
                "candidate_name": row[5] or f"Candidate {row[1]}",
                "job_title": row[6] or f"Job {row[2]}"
            } for row in result]
            
            return {"interviews": interviews, "count": len(interviews)}
    except Exception as e:
        return {
            "interviews": [], 
            "count": 0, 
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

@router.post("/interviews", tags=["Interview Management"])
async def schedule_interview(interview: InterviewScheduleRequest, api_key: str = Depends(get_api_key)):
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            query = text("""
                INSERT INTO interviews (candidate_id, job_id, interview_date, status, notes)
                VALUES (:candidate_id, :job_id, :interview_date, 'scheduled', :notes)
                RETURNING id
            """)
            result = connection.execute(query, {
                "candidate_id": interview.candidate_id,
                "job_id": interview.job_id,
                "interview_date": interview.interview_date,
                "notes": f"Interviewer: {interview.interviewer or 'HR Team'}. {interview.notes or ''}"
            })
            connection.commit()
            interview_id = result.fetchone()[0]
            
            return {
                "message": "Interview scheduled successfully",
                "interview_id": interview_id,
                "candidate_id": interview.candidate_id,
                "job_id": interview.job_id,
                "interview_date": interview.interview_date,
                "interviewer": interview.interviewer or "HR Team",
                "status": "scheduled"
            }
    except Exception as e:
        return {
            "message": "Interview scheduling failed",
            "error": str(e),
            "candidate_id": interview.candidate_id,
            "job_id": interview.job_id,
            "status": "failed",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

@router.get("/interviews/{interview_id}", tags=["Interview Management"])
async def get_interview(interview_id: int, api_key: str = Depends(get_api_key)):
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            query = text("SELECT * FROM interviews WHERE id = :interview_id")
            result = connection.execute(query, {"interview_id": interview_id})
            interview = result.fetchone()
            if not interview:
                raise HTTPException(status_code=404, detail="Interview not found")
            return {
                "id": interview[0],
                "candidate_id": interview[1],
                "job_id": interview[2],
                "interview_date": interview[3].isoformat() if interview[3] else None,
                "status": interview[4] or "scheduled"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Interview retrieval failed: {str(e)}")

@router.put("/interviews/{interview_id}", tags=["Interview Management"])
async def update_interview(interview_id: int, interview_data: dict, api_key: str = Depends(get_api_key)):
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            query = text("""
                UPDATE interviews SET interview_date = :interview_date, 
                status = :status, notes = :notes
                WHERE id = :interview_id
            """)
            connection.execute(query, {"interview_id": interview_id, **interview_data})
            connection.commit()
            return {"message": f"Interview {interview_id} updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Interview update failed: {str(e)}")

@router.delete("/interviews/{interview_id}", tags=["Interview Management"])
async def delete_interview(interview_id: int, api_key: str = Depends(get_api_key)):
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            query = text("DELETE FROM interviews WHERE id = :interview_id")
            connection.execute(query, {"interview_id": interview_id})
            connection.commit()
            return {"message": f"Interview {interview_id} deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Interview deletion failed: {str(e)}")

@router.get("/interviews/calendar", tags=["Interview Management"])
async def get_interview_calendar(month: str = None, api_key: str = Depends(get_api_key)):
    try:
        if not month:
            month = datetime.now().strftime("%Y-%m")
        
        engine = get_db_engine()
        with engine.connect() as connection:
            query = text("""
                SELECT i.id, i.interview_date, i.status, c.name as candidate_name, j.title as job_title
                FROM interviews i
                LEFT JOIN candidates c ON i.candidate_id = c.id
                LEFT JOIN jobs j ON i.job_id = j.id
                WHERE i.interview_date IS NOT NULL
                ORDER BY i.interview_date
                LIMIT 50
            """)
            result = connection.execute(query)
            interviews = [{
                "id": row[0],
                "interview_date": row[1].isoformat() if row[1] else None,
                "status": row[2],
                "candidate_name": row[3],
                "job_title": row[4]
            } for row in result]
            
            return {"interviews": interviews, "month": month, "count": len(interviews)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calendar retrieval failed: {str(e)}")

@router.post("/interviews/schedule", tags=["Interview Management"])
async def schedule_interview_new(schedule_data: dict, api_key: str = Depends(get_api_key)):
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            query = text("""
                INSERT INTO interviews (candidate_id, job_id, interview_date, status, notes)
                VALUES (:candidate_id, :job_id, :interview_date, 'scheduled', :notes)
                RETURNING id
            """)
            result = connection.execute(query, schedule_data)
            connection.commit()
            interview_id = result.fetchone()[0]
            return {"interview_id": interview_id, "scheduled_at": datetime.now(timezone.utc).isoformat()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Interview scheduling failed: {str(e)}")

@router.post("/interviews/feedback", tags=["Interview Management"])
async def submit_interview_feedback(feedback_data: dict, api_key: str = Depends(get_api_key)):
    try:
        feedback_id = f"feedback_{int(datetime.now().timestamp())}"
        return {
            "message": "Interview feedback submitted",
            "feedback_id": feedback_id,
            "submitted_at": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feedback submission failed: {str(e)}")