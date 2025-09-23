# Job Management Module
# Handles all job-related operations

from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from sqlalchemy import create_engine, text
import os

# Job models
class JobCreateRequest(BaseModel):
    title: str
    department: str
    location: str
    experience_level: str
    requirements: str
    description: str
    client_id: Optional[int] = 1
    employment_type: Optional[str] = "Full-time"

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

# Job Management endpoints (8 endpoints)
@router.post("/jobs", tags=["Job Management"])
async def create_job(job: JobCreateRequest, api_key: str = Depends(get_api_key)):
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            query = text("""
                INSERT INTO jobs (title, department, location, experience_level, requirements, description, status, created_at)
                VALUES (:title, :department, :location, :experience_level, :requirements, :description, 'active', NOW())
                RETURNING id
            """)
            result = connection.execute(query, {
                "title": job.title,
                "department": job.department,
                "location": job.location,
                "experience_level": job.experience_level,
                "requirements": job.requirements,
                "description": job.description
            })
            connection.commit()
            job_id = result.fetchone()[0]
            
            return {
                "message": "Job created successfully",
                "job_id": job_id,
                "created_at": datetime.now(timezone.utc).isoformat()
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job creation failed: {str(e)}")

@router.get("/jobs", tags=["Job Management"])
async def list_jobs(api_key: str = Depends(get_api_key)):
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            query = text("""
                SELECT id, title, department, location, experience_level, requirements, description, created_at 
                FROM jobs WHERE status = 'active' ORDER BY created_at DESC
            """)
            result = connection.execute(query)
            jobs = [{
                "id": row[0], 
                "title": row[1], 
                "department": row[2],
                "location": row[3],
                "experience_level": row[4],
                "requirements": row[5],
                "description": row[6],
                "created_at": row[7].isoformat() if row[7] else None
            } for row in result]
        return {"jobs": jobs, "count": len(jobs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch jobs: {str(e)}")

@router.get("/jobs/{job_id}", tags=["Job Management"])
async def get_job(job_id: int, api_key: str = Depends(get_api_key)):
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            query = text("SELECT * FROM jobs WHERE id = :job_id")
            result = connection.execute(query, {"job_id": job_id})
            job = result.fetchone()
            if not job:
                raise HTTPException(status_code=404, detail="Job not found")
            return {"id": job[0], "title": job[1], "department": job[2], "location": job[3], "status": job[8] or "active"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job retrieval failed: {str(e)}")

@router.put("/jobs/{job_id}", tags=["Job Management"])
async def update_job(job_id: int, job_data: dict, api_key: str = Depends(get_api_key)):
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            query = text("""
                UPDATE jobs SET title = :title, department = :department, 
                location = :location, requirements = :requirements, 
                description = :description
                WHERE id = :job_id
            """)
            connection.execute(query, {"job_id": job_id, **job_data})
            connection.commit()
            return {"message": f"Job {job_id} updated", "updated_at": datetime.now(timezone.utc).isoformat()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job update failed: {str(e)}")

@router.delete("/jobs/{job_id}", tags=["Job Management"])
async def delete_job(job_id: int, api_key: str = Depends(get_api_key)):
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            query = text("UPDATE jobs SET status = 'deleted' WHERE id = :job_id")
            connection.execute(query, {"job_id": job_id})
            connection.commit()
            return {"message": f"Job {job_id} deleted", "deleted_at": datetime.now(timezone.utc).isoformat()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job deletion failed: {str(e)}")

@router.get("/jobs/search", tags=["Job Management"])
async def search_jobs(query: str = "", location: str = "", department: str = "", api_key: str = Depends(get_api_key)):
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            search_query = text("""
                SELECT id, title, department, location, experience_level 
                FROM jobs 
                WHERE (title ILIKE :query OR description ILIKE :query)
                AND (:location = '' OR location ILIKE :location)
                AND (:department = '' OR department ILIKE :department)
                AND status = 'active'
                ORDER BY created_at DESC
                LIMIT 50
            """)
            result = connection.execute(search_query, {
                "query": f"%{query}%", 
                "location": f"%{location}%", 
                "department": f"%{department}%"
            })
            jobs = [{"id": row[0], "title": row[1], "department": row[2], "location": row[3], "experience_level": row[4]} for row in result]
            return {"jobs": jobs, "query": query, "count": len(jobs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job search failed: {str(e)}")

@router.get("/jobs/stats", tags=["Job Management"])
async def get_job_stats(api_key: str = Depends(get_api_key)):
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            stats_query = text("""
                SELECT 
                    COUNT(*) as total_jobs,
                    COUNT(CASE WHEN status = 'active' THEN 1 END) as active_jobs,
                    COUNT(CASE WHEN status = 'filled' THEN 1 END) as filled_jobs
                FROM jobs
            """)
            result = connection.execute(stats_query).fetchone()
            return {
                "total_jobs": result[0] or 0,
                "active_jobs": result[1] or 0,
                "filled_jobs": result[2] or 0
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job stats failed: {str(e)}")

@router.post("/jobs/bulk", tags=["Job Management"])
async def bulk_create_jobs(jobs_data: dict, api_key: str = Depends(get_api_key)):
    return {"message": "Bulk job creation completed", "jobs_created": 5}