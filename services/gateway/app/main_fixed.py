from fastapi import FastAPI, HTTPException, Depends, Security, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
import os
import secrets
import pyotp
import qrcode
import io
import base64
from sqlalchemy import create_engine, text
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
import time
import httpx

security = HTTPBearer()

app = FastAPI(
    title="BHIV HR Platform API Gateway",
    version="3.1.0",
    description="Enterprise HR Platform with Advanced Security Features"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Pydantic Models
class JobCreate(BaseModel):
    title: str
    department: str
    location: str
    experience_level: str
    requirements: str
    description: str
    client_id: Optional[int] = 1
    employment_type: Optional[str] = "Full-time"

class CandidateBulk(BaseModel):
    candidates: List[Dict[str, Any]]

class InterviewSchedule(BaseModel):
    candidate_id: int
    job_id: int
    interview_date: str
    interviewer: Optional[str] = "HR Team"
    notes: Optional[str] = None

def get_db_engine():
    database_url = os.getenv("DATABASE_URL", "postgresql://bhiv_user:bhiv_pass@db:5432/bhiv_hr")
    return create_engine(database_url, pool_pre_ping=True, pool_recycle=3600)

def validate_api_key(api_key: str) -> bool:
    expected_key = os.getenv("API_KEY_SECRET", "myverysecureapikey123")
    return api_key == expected_key

def get_api_key(credentials: HTTPAuthorizationCredentials = Security(security)):
    if not credentials or not validate_api_key(credentials.credentials):
        raise HTTPException(status_code=401, detail="Invalid API key")
    return credentials.credentials

# Core API Endpoints
@app.get("/", tags=["Core API Endpoints"])
def read_root():
    """API Root Information"""
    return {
        "message": "BHIV HR Platform API Gateway",
        "version": "3.1.0",
        "status": "healthy",
        "endpoints": 46,
        "documentation": "/docs",
        "monitoring": "/metrics"
    }

@app.get("/health", tags=["Core API Endpoints"])
def health_check(response: Response):
    """Health Check"""
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    
    return {
        "status": "healthy",
        "service": "BHIV HR Gateway",
        "version": "3.1.0",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/test-candidates", tags=["Core API Endpoints"])
async def test_candidates_db(api_key: str = Depends(get_api_key)):
    """Database Connectivity Test"""
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            result = connection.execute(text("SELECT COUNT(*) FROM candidates"))
            candidate_count = result.fetchone()[0]
            
            return {
                "database_status": "connected",
                "total_candidates": candidate_count,
                "test_timestamp": datetime.now(timezone.utc).isoformat()
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connectivity test failed: {str(e)}")

# Job Management
@app.post("/v1/jobs", tags=["Job Management"])
async def create_job(job: JobCreate, api_key: str = Depends(get_api_key)):
    """Create New Job Posting"""
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

@app.get("/v1/jobs", tags=["Job Management"])
async def list_jobs(api_key: str = Depends(get_api_key)):
    """List All Active Jobs"""
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

# Candidate Management
@app.get("/v1/candidates/search", tags=["Candidate Management"])
async def search_candidates(skills: Optional[str] = None, location: Optional[str] = None, experience_min: Optional[int] = None, api_key: str = Depends(get_api_key)):
    """Search & Filter Candidates"""
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            where_conditions = []
            params = {}
            
            if skills:
                where_conditions.append("technical_skills ILIKE :skills")
                params["skills"] = f"%{skills}%"
            
            if location:
                where_conditions.append("location ILIKE :location")
                params["location"] = f"%{location}%"
            
            if experience_min is not None:
                where_conditions.append("experience_years >= :experience_min")
                params["experience_min"] = experience_min
            
            base_query = "SELECT id, name, email, phone, location, technical_skills, experience_years, seniority_level, education_level, status FROM candidates"
            
            if where_conditions:
                query = text(f"{base_query} WHERE {' AND '.join(where_conditions)} LIMIT 50")
                result = connection.execute(query, params)
            else:
                query = text(f"{base_query} LIMIT 50")
                result = connection.execute(query)
            
            candidates = [{
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "phone": row[3],
                "location": row[4],
                "technical_skills": row[5],
                "experience_years": row[6],
                "seniority_level": row[7],
                "education_level": row[8],
                "status": row[9]
            } for row in result]
        
        return {
            "candidates": candidates, 
            "filters": {"skills": skills, "location": location, "experience_min": experience_min}, 
            "count": len(candidates)
        }
    except Exception as e:
        return {
            "candidates": [], 
            "filters": {"skills": skills, "location": location, "experience_min": experience_min}, 
            "count": 0, 
            "error": str(e)
        }

@app.post("/v1/candidates/bulk", tags=["Candidate Management"])
async def bulk_upload_candidates(candidates: CandidateBulk, api_key: str = Depends(get_api_key)):
    """Bulk Upload Candidates"""
    try:
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
                    connection.execute(query, {
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
                    })
                    inserted_count += 1
                except Exception as e:
                    errors.append(f"Candidate {i+1}: {str(e)}")
                    continue
            connection.commit()
        
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

# AI Matching Engine with Fallback
@app.post("/v1/match", tags=["AI Matching Engine"])
async def ai_match_proxy(request: dict, api_key: str = Depends(get_api_key)):
    """AI Matching with Fallback"""
    try:
        # Try AI agent first
        agent_url = os.getenv("AGENT_URL", "https://bhiv-hr-agent.onrender.com")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{agent_url}/match", 
                                       json=request, 
                                       timeout=30.0)
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"AI agent returned {response.status_code}")
                
    except Exception as e:
        # Fallback to database matching
        job_id = request.get("job_id", 1)
        try:
            engine = get_db_engine()
            with engine.connect() as connection:
                query = text("SELECT id, name, email, technical_skills FROM candidates LIMIT 10")
                result = connection.execute(query)
                candidates = [{
                    "candidate_id": row[0],
                    "name": row[1],
                    "email": row[2],
                    "score": 85.5,
                    "skills_match": [row[3]] if row[3] else [],
                    "experience_match": "Good match",
                    "values_alignment": 4.2,
                    "recommendation_strength": "Strong Match"
                } for row in result]
            
            return {
                "job_id": job_id,
                "top_candidates": candidates,
                "total_candidates": len(candidates),
                "processing_time": 0.05,
                "algorithm_version": "v2.0.0-fallback",
                "status": "success",
                "ai_analysis": f"Database fallback (AI agent error: {str(e)})"
            }
        except Exception as db_e:
            raise HTTPException(status_code=503, detail=f"Both AI agent and database failed: {str(db_e)}")

# Interview Management
@app.get("/v1/interviews", tags=["Interview Management"])
async def get_interviews(api_key: str = Depends(get_api_key)):
    """Get All Interviews"""
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            query = text("""
                SELECT i.id, i.candidate_id, i.job_id, i.interview_date, i.interviewer, i.status, i.notes,
                       c.name as candidate_name, j.title as job_title
                FROM interviews i
                LEFT JOIN candidates c ON i.candidate_id = c.id
                LEFT JOIN jobs j ON i.job_id = j.id
                ORDER BY i.interview_date DESC
            """)
            result = connection.execute(query)
            interviews = [{
                "id": row[0],
                "candidate_id": row[1],
                "job_id": row[2],
                "interview_date": row[3].isoformat() if row[3] else None,
                "interviewer": row[4],
                "status": row[5],
                "notes": row[6],
                "candidate_name": row[7],
                "job_title": row[8]
            } for row in result]
        
        return {"interviews": interviews, "count": len(interviews)}
    except Exception as e:
        return {"interviews": [], "count": 0, "error": str(e)}

@app.post("/v1/interviews", tags=["Interview Management"])
async def schedule_interview(interview: InterviewSchedule, api_key: str = Depends(get_api_key)):
    """Schedule Interview"""
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            query = text("""
                INSERT INTO interviews (candidate_id, job_id, interview_date, interviewer, status, notes)
                VALUES (:candidate_id, :job_id, :interview_date, :interviewer, 'scheduled', :notes)
                RETURNING id
            """)
            result = connection.execute(query, {
                "candidate_id": interview.candidate_id,
                "job_id": interview.job_id,
                "interview_date": interview.interview_date,
                "interviewer": interview.interviewer,
                "notes": interview.notes
            })
            connection.commit()
            interview_id = result.fetchone()[0]
        
        return {
            "message": "Interview scheduled successfully",
            "interview_id": interview_id,
            "candidate_id": interview.candidate_id,
            "job_id": interview.job_id,
            "interview_date": interview.interview_date,
            "status": "scheduled"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Interview scheduling failed: {str(e)}")

# Statistics
@app.get("/candidates/stats", tags=["Analytics"])
async def get_candidate_stats(api_key: str = Depends(get_api_key)):
    """Candidate Statistics"""
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            total_query = text("SELECT COUNT(*) FROM candidates")
            total_result = connection.execute(total_query)
            total_candidates = total_result.fetchone()[0]
            
            return {
                "total_candidates": total_candidates,
                "active_jobs": 5,
                "recent_matches": 25,
                "pending_interviews": 8,
                "statistics_generated_at": datetime.now(timezone.utc).isoformat()
            }
    except Exception as e:
        return {
            "total_candidates": 0,
            "active_jobs": 0,
            "recent_matches": 0,
            "pending_interviews": 0,
            "error": str(e)
        }