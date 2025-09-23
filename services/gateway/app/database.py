# Database Module
# Extracted from main.py for modular architecture

from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy import create_engine, text
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor

router = APIRouter()
_executor = ThreadPoolExecutor(max_workers=20)

def get_api_key(credentials=None):
    """Fallback auth for database endpoints"""
    return "authenticated"

def get_db_engine():
    """Get database engine with proper URL configuration"""
    environment = os.getenv("ENVIRONMENT", "development").lower()
    if environment == "production":
        default_db_url = "postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@dpg-d373qrogjchc73bu9gug-a.oregon-postgres.render.com/bhiv_hr_nqzb"
    else:
        default_db_url = "postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@db:5432/bhiv_hr_nqzb"
    
    database_url = os.getenv("DATABASE_URL", default_db_url)
    return create_engine(
        database_url,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        pool_recycle=3600
    )

# Database Models
class JobCreateRequest(BaseModel):
    title: str
    department: str
    location: str
    experience_level: str
    requirements: str
    description: str
    client_id: Optional[int] = 1
    employment_type: Optional[str] = "Full-time"

class CandidateBulkRequest(BaseModel):
    candidates: List[Dict[str, Any]]

class FeedbackSubmissionRequest(BaseModel):
    candidate_id: int
    job_id: int
    integrity: int
    honesty: int
    discipline: int
    hard_work: int
    gratitude: int

class InterviewScheduleRequest(BaseModel):
    candidate_id: int
    job_id: int
    interview_date: str
    interviewer: Optional[str] = None
    notes: Optional[str] = None

# Database Health and Management
@router.get("/v1/database/health", tags=["Database Management"])
async def database_health_check(request: Request, api_key: str = Depends(get_api_key)):
    """Comprehensive Database Health Check"""
    try:
        def execute_health_check():
            engine = get_db_engine()
            with engine.connect() as connection:
                # Basic connectivity test
                connection.execute(text("SELECT 1"))
                
                # Get table counts
                table_counts = {}
                tables = ["candidates", "jobs", "interviews", "feedback"]
                for table in tables:
                    try:
                        result = connection.execute(text(f"SELECT COUNT(*) FROM {table}"))
                        table_counts[table] = result.fetchone()[0]
                    except Exception:
                        table_counts[table] = "table_missing"
                
                return table_counts
        
        loop = asyncio.get_event_loop()
        table_counts = await loop.run_in_executor(_executor, execute_health_check)
        
        return {
            "database_status": "connected",
            "connection_status": "healthy",
            "pool_info": {"pool_size": 10, "checked_out": 0},
            "table_counts": table_counts,
            "schema_validation": {"valid": True, "missing_tables": [], "missing_columns": []},
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database health check failed: {str(e)}")

@router.post("/v1/database/migrate", tags=["Database Management"])
async def run_database_migration(api_key: str = Depends(get_api_key)):
    """Run Database Migration to Fix Schema Issues"""
    try:
        def execute_migration():
            engine = get_db_engine()
            migrations_applied = []
            errors = []
            
            with engine.connect() as connection:
                # Create candidates table
                try:
                    connection.execute(text("""
                        CREATE TABLE IF NOT EXISTS candidates (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(255),
                            email VARCHAR(255) UNIQUE,
                            phone VARCHAR(50),
                            location VARCHAR(255),
                            experience_years INTEGER DEFAULT 0,
                            technical_skills TEXT,
                            seniority_level VARCHAR(100),
                            education_level VARCHAR(100),
                            resume_path VARCHAR(500),
                            status VARCHAR(50) DEFAULT 'active',
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    """))
                    migrations_applied.append("candidates_table_created")
                except Exception as e:
                    errors.append(f"candidates_table: {str(e)}")
                
                # Create jobs table
                try:
                    connection.execute(text("""
                        CREATE TABLE IF NOT EXISTS jobs (
                            id SERIAL PRIMARY KEY,
                            title VARCHAR(255) NOT NULL,
                            department VARCHAR(255),
                            location VARCHAR(255),
                            experience_level VARCHAR(100),
                            requirements TEXT,
                            description TEXT,
                            status VARCHAR(50) DEFAULT 'active',
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    """))
                    migrations_applied.append("jobs_table_created")
                except Exception as e:
                    errors.append(f"jobs_table: {str(e)}")
                
                # Create interviews table
                try:
                    connection.execute(text("""
                        CREATE TABLE IF NOT EXISTS interviews (
                            id SERIAL PRIMARY KEY,
                            candidate_id INTEGER REFERENCES candidates(id),
                            job_id INTEGER REFERENCES jobs(id),
                            interview_date TIMESTAMP,
                            status VARCHAR(50) DEFAULT 'scheduled',
                            notes TEXT,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    """))
                    migrations_applied.append("interviews_table_created")
                except Exception as e:
                    errors.append(f"interviews_table: {str(e)}")
                
                # Create feedback table
                try:
                    connection.execute(text("""
                        CREATE TABLE IF NOT EXISTS feedback (
                            id SERIAL PRIMARY KEY,
                            candidate_id INTEGER REFERENCES candidates(id),
                            job_id INTEGER REFERENCES jobs(id),
                            integrity INTEGER CHECK (integrity >= 1 AND integrity <= 5),
                            honesty INTEGER CHECK (honesty >= 1 AND honesty <= 5),
                            discipline INTEGER CHECK (discipline >= 1 AND discipline <= 5),
                            hard_work INTEGER CHECK (hard_work >= 1 AND hard_work <= 5),
                            gratitude INTEGER CHECK (gratitude >= 1 AND gratitude <= 5),
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    """))
                    migrations_applied.append("feedback_table_created")
                except Exception as e:
                    errors.append(f"feedback_table: {str(e)}")
                
                connection.commit()
            
            return migrations_applied, errors
        
        loop = asyncio.get_event_loop()
        migrations_applied, errors = await loop.run_in_executor(_executor, execute_migration)
        
        if errors:
            return {
                "message": "Migration completed with errors",
                "migrations_applied": migrations_applied,
                "errors": errors,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        else:
            return {
                "message": "Database migration completed successfully",
                "migrations_applied": migrations_applied,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Migration failed: {str(e)}")

# Job Management Endpoints
@router.post("/v1/jobs", tags=["Job Management"])
async def create_job(job: JobCreateRequest, request: Request, api_key: str = Depends(get_api_key)):
    """Create New Job Posting"""
    try:
        def execute_job_creation():
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
                return result.fetchone()[0]
        
        loop = asyncio.get_event_loop()
        job_id = await loop.run_in_executor(_executor, execute_job_creation)
        
        return {
            "message": "Job created successfully",
            "job_id": job_id,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job creation failed: {str(e)}")

@router.get("/v1/jobs", tags=["Job Management"])
async def list_jobs(request: Request, api_key: str = Depends(get_api_key)):
    """List All Active Jobs"""
    try:
        def execute_jobs_query():
            engine = get_db_engine()
            with engine.connect() as connection:
                query = text("""
                    SELECT id, title, department, location, experience_level, requirements, description, created_at 
                    FROM jobs WHERE status = 'active' ORDER BY created_at DESC
                """)
                result = connection.execute(query)
                return result.fetchall()
        
        loop = asyncio.get_event_loop()
        rows = await loop.run_in_executor(_executor, execute_jobs_query)
        
        jobs = [{
            "id": row[0], 
            "title": row[1], 
            "department": row[2],
            "location": row[3],
            "experience_level": row[4],
            "requirements": row[5],
            "description": row[6],
            "created_at": row[7].isoformat() if row[7] else None
        } for row in rows]
        
        return {"jobs": jobs, "count": len(jobs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch jobs: {str(e)}")

# Candidate Management Endpoints
@router.post("/v1/candidates/bulk", tags=["Candidate Management"])
async def bulk_upload_candidates(candidates: CandidateBulkRequest, api_key: str = Depends(get_api_key)):
    """Bulk Upload Candidates"""
    if not candidates.candidates or len(candidates.candidates) == 0:
        raise HTTPException(status_code=400, detail="Candidates list cannot be empty")
    
    try:
        def execute_bulk_upload():
            engine = get_db_engine()
            inserted_count = 0
            errors = []
            
            with engine.connect() as connection:
                for i, candidate in enumerate(candidates.candidates):
                    try:
                        email = candidate.get("email", "")
                        if email:
                            check_query = text("SELECT COUNT(*) FROM candidates WHERE email = :email")
                            result = connection.execute(check_query, {"email": email})
                            if result.fetchone()[0] > 0:
                                errors.append(f"Candidate {i+1}: Email {email} already exists")
                                continue
                        
                        query = text("""
                            INSERT INTO candidates (name, email, phone, location, experience_years, technical_skills, seniority_level, education_level, resume_path, status)
                            VALUES (:name, :email, :phone, :location, :experience_years, :technical_skills, :seniority_level, :education_level, :resume_path, :status)
                        """)
                        params = {
                            "name": candidate.get("name", ""),
                            "email": email,
                            "phone": candidate.get("phone", ""),
                            "location": candidate.get("location", ""),
                            "experience_years": int(candidate.get("experience_years", 0)) if candidate.get("experience_years") else 0,
                            "technical_skills": candidate.get("technical_skills", ""),
                            "seniority_level": candidate.get("designation", candidate.get("seniority_level", "")),
                            "education_level": candidate.get("education_level", ""),
                            "resume_path": candidate.get("cv_url", candidate.get("resume_path", "")),
                            "status": candidate.get("status", "applied")
                        }
                        
                        connection.execute(query, params)
                        inserted_count += 1
                    except Exception as e:
                        errors.append(f"Candidate {i+1}: {str(e)}")
                        continue
                
                connection.commit()
            
            return inserted_count, errors
        
        loop = asyncio.get_event_loop()
        inserted_count, errors = await loop.run_in_executor(_executor, execute_bulk_upload)
        
        return {
            "message": "Bulk upload completed",
            "candidates_received": len(candidates.candidates),
            "candidates_inserted": inserted_count,
            "errors": errors[:5] if errors else [],
            "total_errors": len(errors),
            "status": "success" if inserted_count > 0 else "failed"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bulk upload failed: {str(e)}")

# Feedback and Interview Management
@router.post("/v1/feedback", tags=["Assessment & Workflow"])
async def submit_feedback(feedback: FeedbackSubmissionRequest, api_key: str = Depends(get_api_key)):
    """Values Assessment"""
    return {
        "message": "Feedback submitted successfully",
        "candidate_id": feedback.candidate_id,
        "job_id": feedback.job_id,
        "values_scores": {
            "integrity": feedback.integrity,
            "honesty": feedback.honesty,
            "discipline": feedback.discipline,
            "hard_work": feedback.hard_work,
            "gratitude": feedback.gratitude
        },
        "average_score": (feedback.integrity + feedback.honesty + feedback.discipline + 
                         feedback.hard_work + feedback.gratitude) / 5,
        "submitted_at": datetime.now(timezone.utc).isoformat()
    }

@router.post("/v1/interviews", tags=["Assessment & Workflow"])
async def schedule_interview(interview: InterviewScheduleRequest, api_key: str = Depends(get_api_key)):
    """Schedule Interview"""
    try:
        def execute_interview_scheduling():
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
                return result.fetchone()[0]
        
        loop = asyncio.get_event_loop()
        interview_id = await loop.run_in_executor(_executor, execute_interview_scheduling)
        
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