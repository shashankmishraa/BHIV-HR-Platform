from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from ..db.base import SessionLocal
from typing import List
from pydantic import BaseModel

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class CandidateCreate(BaseModel):
    name: str
    email: str = ""
    cv_url: str = ""
    phone: str = ""
    experience_years: int = 0
    status: str = "applied"
    job_id: int
    location: str = ""
    education_level: str = ""
    technical_skills: str = ""
    seniority_level: str = ""

class BulkCandidatesRequest(BaseModel):
    candidates: List[CandidateCreate]

@router.post("/bulk")
async def upload_candidates_bulk(request: BulkCandidatesRequest, db: Session = Depends(get_db)):
    try:
        inserted_count = 0
        for candidate in request.candidates:
            # Insert candidate into database
            # Create enhanced candidates table if not exists
            db.execute(text("""
                CREATE TABLE IF NOT EXISTS candidates (
                    id SERIAL PRIMARY KEY,
                    job_id INTEGER,
                    name VARCHAR(255),
                    email VARCHAR(255),
                    phone VARCHAR(50),
                    location VARCHAR(255),
                    cv_url TEXT,
                    experience_years INTEGER DEFAULT 0,
                    education_level VARCHAR(100),
                    technical_skills TEXT,
                    seniority_level VARCHAR(50),
                    status VARCHAR(50) DEFAULT 'applied',
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """))
            
            query = text("""
                INSERT INTO candidates (job_id, name, email, phone, location, cv_url, 
                                      experience_years, education_level, technical_skills, 
                                      seniority_level, status, created_at)
                VALUES (:job_id, :name, :email, :phone, :location, :cv_url, 
                        :experience_years, :education_level, :technical_skills, 
                        :seniority_level, :status, NOW())
            """)
            db.execute(query, {
                "job_id": candidate.job_id,
                "name": candidate.name,
                "email": candidate.email,
                "phone": candidate.phone,
                "location": candidate.location,
                "cv_url": candidate.cv_url,
                "experience_years": candidate.experience_years,
                "education_level": candidate.education_level,
                "technical_skills": candidate.technical_skills,
                "seniority_level": candidate.seniority_level,
                "status": candidate.status
            })
            inserted_count += 1
        
        db.commit()
        return {
            "message": f"Successfully uploaded {inserted_count} candidates",
            "count": inserted_count,
            "status": "success"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to upload candidates: {str(e)}")

@router.get("/job/{job_id}")
async def get_candidates_by_job(job_id: int, db: Session = Depends(get_db)):
    try:
        query = text("""
            SELECT id, name, email, phone, location, cv_url, experience_years, 
                   education_level, technical_skills, seniority_level, status, created_at
            FROM candidates 
            WHERE job_id = :job_id
            ORDER BY created_at DESC
        """)
        result = db.execute(query, {"job_id": job_id})
        candidates = []
        for row in result:
            candidates.append({
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "phone": row[3],
                "location": row[4],
                "cv_url": row[5],
                "experience_years": row[6],
                "education_level": row[7],
                "technical_skills": row[8],
                "seniority_level": row[9],
                "status": row[10],
                "created_at": str(row[11])
            })
        
        return {
            "job_id": job_id,
            "candidates": candidates,
            "count": len(candidates)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get candidates: {str(e)}")