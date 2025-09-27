"""Interviews router"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/v1/interviews", tags=["Interviews"])

class InterviewCreate(BaseModel):
    candidate_id: int
    job_id: int
    interview_date: str
    interviewer: str = "HR Team"
    notes: Optional[str] = None

@router.post("")
async def create_interview(interview: InterviewCreate):
    """Create new interview"""
    from app.shared.database import db_manager
    
    try:
        async with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO interviews (candidate_id, job_id, interview_date, interviewer, notes)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            """, (interview.candidate_id, interview.job_id, interview.interview_date, 
                  interview.interviewer, interview.notes))
            
            interview_id = cursor.fetchone()[0]
            conn.commit()
            
            return {
                "id": interview_id,
                "message": "Interview scheduled successfully",
                "interview_date": interview.interview_date,
                "interviewer": interview.interviewer
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("")
async def list_interviews():
    """List all interviews"""
    from app.shared.database import db_manager
    
    try:
        async with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT i.id, i.candidate_id, i.job_id, i.interview_date, 
                       i.interviewer, i.status, i.notes,
                       c.name as candidate_name, j.title as job_title
                FROM interviews i
                LEFT JOIN candidates c ON i.candidate_id = c.id
                LEFT JOIN jobs j ON i.job_id = j.id
                ORDER BY i.interview_date DESC
            """)
            
            interviews = []
            for row in cursor.fetchall():
                interviews.append({
                    "id": row[0],
                    "candidate_id": row[1],
                    "job_id": row[2],
                    "interview_date": row[3].isoformat() if row[3] else None,
                    "interviewer": row[4],
                    "status": row[5],
                    "notes": row[6],
                    "candidate_name": row[7],
                    "job_title": row[8]
                })
            
            return {"interviews": interviews, "total": len(interviews)}
    except Exception as e:
        return {"interviews": [], "total": 0, "error": str(e)}