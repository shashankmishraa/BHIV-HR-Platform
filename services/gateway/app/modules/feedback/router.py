"""Feedback router"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/v1/feedback", tags=["Feedback"])

class FeedbackCreate(BaseModel):
    candidate_id: int
    job_id: int
    integrity: int
    honesty: int
    discipline: int
    hard_work: int
    gratitude: int
    comments: Optional[str] = None

@router.post("")
async def create_feedback(feedback: FeedbackCreate):
    """Submit values assessment feedback"""
    from app.shared.database import db_manager
    
    try:
        async with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO feedback (candidate_id, job_id, integrity, honesty, 
                                    discipline, hard_work, gratitude, comments)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (feedback.candidate_id, feedback.job_id, feedback.integrity,
                  feedback.honesty, feedback.discipline, feedback.hard_work,
                  feedback.gratitude, feedback.comments))
            
            feedback_id = cursor.fetchone()[0]
            conn.commit()
            
            # Calculate average score
            avg_score = (feedback.integrity + feedback.honesty + feedback.discipline + 
                        feedback.hard_work + feedback.gratitude) / 5
            
            return {
                "id": feedback_id,
                "message": "Values assessment submitted successfully",
                "average_score": round(avg_score, 2),
                "values": {
                    "integrity": feedback.integrity,
                    "honesty": feedback.honesty,
                    "discipline": feedback.discipline,
                    "hard_work": feedback.hard_work,
                    "gratitude": feedback.gratitude
                }
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("")
async def list_feedback():
    """List all feedback"""
    from app.shared.database import db_manager
    
    try:
        async with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT f.id, f.candidate_id, f.job_id, f.integrity, f.honesty,
                       f.discipline, f.hard_work, f.gratitude, f.comments,
                       c.name as candidate_name, j.title as job_title
                FROM feedback f
                LEFT JOIN candidates c ON f.candidate_id = c.id
                LEFT JOIN jobs j ON f.job_id = j.id
                ORDER BY f.created_at DESC
            """)
            
            feedback_list = []
            for row in cursor.fetchall():
                avg_score = (row[3] + row[4] + row[5] + row[6] + row[7]) / 5
                feedback_list.append({
                    "id": row[0],
                    "candidate_id": row[1],
                    "job_id": row[2],
                    "values": {
                        "integrity": row[3],
                        "honesty": row[4],
                        "discipline": row[5],
                        "hard_work": row[6],
                        "gratitude": row[7]
                    },
                    "average_score": round(avg_score, 2),
                    "comments": row[8],
                    "candidate_name": row[9],
                    "job_title": row[10]
                })
            
            return {"feedback": feedback_list, "total": len(feedback_list)}
    except Exception as e:
        return {"feedback": [], "total": 0, "error": str(e)}