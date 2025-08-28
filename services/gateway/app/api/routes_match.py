from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.base import SessionLocal
from ..services.ai_agent_client import get_top_candidates

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{job_id}/top")
async def get_shortlist(job_id: int, db: Session = Depends(get_db)):
    try:
        candidates = await get_top_candidates(job_id)
        return candidates
    except Exception as e:
        return {"error": str(e), "job_id": job_id, "top_candidates": []}
