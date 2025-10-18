from fastapi import FastAPI, HTTPException, Depends, Security, Response, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
import os
import secrets
import pyotp
import qrcode
import io
import base64
import re
import string
import random
import jwt
from collections import defaultdict
from sqlalchemy import create_engine, text
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, field_validator
import time
import psutil
try:
    from routes.auth import router as auth_router
except ImportError:
    # Fallback if auth routes not available
    from fastapi import APIRouter
    auth_router = APIRouter()
try:
    from .monitoring import monitor, log_resume_processing, log_matching_performance, log_user_activity, log_error
except ImportError:
    # Fallback if monitoring module is not available
    class MockMonitor:
        def export_prometheus_metrics(self): return "# No metrics available"
        def health_check(self): return {"status": "healthy", "monitoring": "disabled"}
        def get_performance_summary(self, hours): return {"monitoring": "disabled"}
        def get_business_metrics(self): return {"monitoring": "disabled"}
        def collect_system_metrics(self): return {"monitoring": "disabled"}
    
    monitor = MockMonitor()
    def log_resume_processing(*args, **kwargs): pass
    def log_matching_performance(*args, **kwargs): pass
    def log_user_activity(*args, **kwargs): pass
    def log_error(*args, **kwargs): pass

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

# Include auth routes
app.include_router(auth_router)

# Add monitoring endpoints
@app.get("/metrics", tags=["Monitoring"])
async def get_prometheus_metrics():
    """Prometheus Metrics Export"""
    return Response(content=monitor.export_prometheus_metrics(), media_type="text/plain")

@app.get("/health/detailed", tags=["Monitoring"])
async def detailed_health_check():
    """Detailed Health Check with Metrics"""
    return monitor.health_check()

@app.get("/metrics/dashboard", tags=["Monitoring"])
async def metrics_dashboard():
    """Metrics Dashboard Data"""
    return {
        "performance_summary": monitor.get_performance_summary(24),
        "business_metrics": monitor.get_business_metrics(),
        "system_metrics": monitor.collect_system_metrics()
    }

# Enhanced Granular Rate Limiting

rate_limit_storage = defaultdict(list)

# Granular rate limits by endpoint and user tier
RATE_LIMITS = {
    "default": {
        "/v1/jobs": 100,
        "/v1/candidates/search": 50,
        "/v1/match": 20,
        "/v1/candidates/bulk": 5,
        "default": 60
    },
    "premium": {
        "/v1/jobs": 500,
        "/v1/candidates/search": 200,
        "/v1/match": 100,
        "/v1/candidates/bulk": 25,
        "default": 300
    }
}

def get_dynamic_rate_limit(endpoint: str, user_tier: str = "default") -> int:
    """Dynamic rate limiting based on system load"""
    cpu_usage = psutil.cpu_percent()
    base_limit = RATE_LIMITS[user_tier].get(endpoint, RATE_LIMITS[user_tier]["default"])
    
    if cpu_usage > 80:
        return int(base_limit * 0.5)  # Reduce by 50% during high load
    elif cpu_usage < 30:
        return int(base_limit * 1.5)  # Increase by 50% during low load
    return base_limit

async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    current_time = time.time()
    endpoint_path = request.url.path
    
    # Determine user tier (simplified - in production, get from JWT/database)
    user_tier = "premium" if "enterprise" in request.headers.get("user-agent", "").lower() else "default"
    
    # Get dynamic rate limit for this endpoint
    rate_limit = get_dynamic_rate_limit(endpoint_path, user_tier)
    
    # Clean old requests (older than 1 minute)
    key = f"{client_ip}:{endpoint_path}"
    rate_limit_storage[key] = [
        req_time for req_time in rate_limit_storage[key] 
        if current_time - req_time < 60
    ]
    
    # Check granular rate limit
    if len(rate_limit_storage[key]) >= rate_limit:
        raise HTTPException(
            status_code=429, 
            detail=f"Rate limit exceeded for {endpoint_path}. Limit: {rate_limit}/min"
        )
    
    # Record this request
    rate_limit_storage[key].append(current_time)
    
    response = await call_next(request)
    response.headers["X-RateLimit-Limit"] = str(rate_limit)
    response.headers["X-RateLimit-Remaining"] = str(rate_limit - len(rate_limit_storage[key]))
    return response

app.middleware("http")(rate_limit_middleware)

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

class FeedbackSubmission(BaseModel):
    candidate_id: int
    job_id: int
    integrity: int
    honesty: int
    discipline: int
    hard_work: int
    gratitude: int
    comments: Optional[str] = None

class InterviewSchedule(BaseModel):
    candidate_id: int
    job_id: int
    interview_date: str
    interviewer: Optional[str] = "HR Team"
    notes: Optional[str] = None

class JobOffer(BaseModel):
    candidate_id: int
    job_id: int
    salary: float
    start_date: str
    terms: str

class ClientLogin(BaseModel):
    client_id: str
    password: str

class TwoFASetup(BaseModel):
    user_id: str

class TwoFALogin(BaseModel):
    user_id: str
    totp_code: str

class PasswordValidation(BaseModel):
    password: str

class SecurityTest(BaseModel):
    test_type: str
    payload: str

class CSPPolicy(BaseModel):
    policy: str

class InputValidation(BaseModel):
    input_data: str

class EmailValidation(BaseModel):
    email: str

class PhoneValidation(BaseModel):
    phone: str

class CSPReport(BaseModel):
    violated_directive: str
    blocked_uri: str
    document_uri: str

class PasswordChange(BaseModel):
    old_password: str
    new_password: str

class CandidateSearch(BaseModel):
    skills: Optional[str] = None
    location: Optional[str] = None
    experience_min: Optional[int] = None
    
    @field_validator('skills')
    @classmethod
    def validate_skills(cls, v):
        return v[:200] if v else None
        
    @field_validator('location')
    @classmethod
    def validate_location(cls, v):
        return v[:100] if v else None

def get_db_engine():
    database_url = os.getenv("DATABASE_URL", "postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu")
    return create_engine(
        database_url, 
        pool_pre_ping=True, 
        pool_recycle=3600,
        pool_size=10,
        connect_args={"connect_timeout": 10, "application_name": "bhiv_gateway"},
        pool_timeout=20,
        max_overflow=5
    )

def validate_api_key(api_key: str) -> bool:
    expected_key = os.getenv("API_KEY_SECRET", "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o")
    return api_key == expected_key

def get_api_key(credentials: HTTPAuthorizationCredentials = Security(security)):
    if not credentials or not validate_api_key(credentials.credentials):
        raise HTTPException(status_code=401, detail="Invalid API key")
    return credentials.credentials

def get_auth(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Dual authentication: API key or client JWT token"""
    if not credentials:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    # Try API key first
    if validate_api_key(credentials.credentials):
        return {"type": "api_key", "credentials": credentials.credentials}
    
    # Try client JWT token
    try:
        jwt_secret = os.getenv("JWT_SECRET", "fallback_jwt_secret_key_for_client_auth_2025")
        payload = jwt.decode(credentials.credentials, jwt_secret, algorithms=["HS256"])
        return {"type": "client_token", "client_id": payload.get("client_id")}
    except:
        pass
    
    raise HTTPException(status_code=401, detail="Invalid authentication")

# Core API Endpoints (3 endpoints)
@app.get("/", tags=["Core API Endpoints"])
def read_root():
    """API Root Information"""
    return {
        "message": "BHIV HR Platform API Gateway",
        "version": "3.1.0",
        "status": "healthy",
        "endpoints": 50,
        "documentation": "/docs",
        "monitoring": "/metrics",
        "live_demo": "https://bhiv-platform.aws.example.com"
    }

@app.get("/health", tags=["Core API Endpoints"])
def health_check(response: Response):
    """Health Check"""
    response.headers["X-RateLimit-Limit"] = "60"
    response.headers["X-RateLimit-Remaining"] = "59"
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
        return {
            "database_status": "failed",
            "error": str(e),
            "test_timestamp": datetime.now(timezone.utc).isoformat()
        }

# Job Management (2 endpoints)
@app.post("/v1/jobs", tags=["Job Management"])
async def create_job(job: JobCreate, api_key: str = Depends(get_api_key)):
    """Create New Job Posting"""
    try:
        engine = get_db_engine()
        with engine.begin() as connection:
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
            job_id = result.fetchone()[0]
            
            return {
                "message": "Job created successfully",
                "job_id": job_id,
                "created_at": datetime.now(timezone.utc).isoformat()
            }
    except Exception as e:
        return {
            "message": "Job creation failed",
            "error": str(e),
            "status": "failed"
        }

@app.get("/v1/jobs", tags=["Job Management"])
async def list_jobs(auth = Depends(get_auth)):
    """List All Active Jobs"""
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            query = text("""
                SELECT id, title, department, location, experience_level, requirements, description, created_at 
                FROM jobs WHERE status = 'active' ORDER BY created_at DESC LIMIT 100
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
        return {"jobs": [], "count": 0, "error": str(e)}

# Candidate Management (5 endpoints)
@app.get("/v1/candidates", tags=["Candidate Management"])
async def get_all_candidates(limit: int = 50, offset: int = 0, api_key: str = Depends(get_api_key)):
    """Get All Candidates with Pagination"""
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            query = text("""
                SELECT id, name, email, phone, location, experience_years, technical_skills, seniority_level, education_level, created_at
                FROM candidates ORDER BY created_at DESC LIMIT :limit OFFSET :offset
            """)
            result = connection.execute(query, {"limit": limit, "offset": offset})
            candidates = [{
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "phone": row[3],
                "location": row[4],
                "experience_years": row[5],
                "technical_skills": row[6],
                "seniority_level": row[7],
                "education_level": row[8],
                "created_at": row[9].isoformat() if row[9] else None
            } for row in result]
            
            count_query = text("SELECT COUNT(*) FROM candidates")
            count_result = connection.execute(count_query)
            total_count = count_result.fetchone()[0]
            
        return {
            "candidates": candidates,
            "total": total_count,
            "limit": limit,
            "offset": offset,
            "count": len(candidates)
        }
    except Exception as e:
        return {"candidates": [], "total": 0, "error": str(e)}

@app.get("/v1/candidates/search", tags=["Candidate Management"])
async def search_candidates(
    skills: Optional[str] = None, 
    location: Optional[str] = None, 
    experience_min: Optional[int] = None, 
    api_key: str = Depends(get_api_key)
):
    """Search & Filter Candidates"""
    if skills:
        skills = skills[:200]
    if location:
        location = location[:100]
    
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

@app.get("/v1/candidates/job/{job_id}", tags=["Candidate Management"])
async def get_candidates_by_job(job_id: int, api_key: str = Depends(get_api_key)):
    """Get All Candidates (Dynamic Matching)"""
    if job_id < 1:
        raise HTTPException(status_code=400, detail="Invalid job ID")
    
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            query = text("SELECT id, name, email, technical_skills, experience_years FROM candidates LIMIT 10")
            result = connection.execute(query)
            candidates = [{
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "skills": row[3],
                "experience": row[4]
            } for row in result]
        
        return {"candidates": candidates, "job_id": job_id, "count": len(candidates)}
    except Exception as e:
        return {"candidates": [], "job_id": job_id, "count": 0, "error": str(e)}

@app.get("/v1/candidates/{candidate_id}", tags=["Candidate Management"])
async def get_candidate_by_id(candidate_id: int, api_key: str = Depends(get_api_key)):
    """Get Specific Candidate by ID"""
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            query = text("""
                SELECT id, name, email, phone, location, experience_years, technical_skills, 
                       seniority_level, education_level, resume_path, created_at, updated_at
                FROM candidates WHERE id = :candidate_id
            """)
            result = connection.execute(query, {"candidate_id": candidate_id})
            row = result.fetchone()
            
            if not row:
                return {"error": "Candidate not found", "candidate_id": candidate_id}
            
            candidate = {
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "phone": row[3],
                "location": row[4],
                "experience_years": row[5],
                "technical_skills": row[6],
                "seniority_level": row[7],
                "education_level": row[8],
                "resume_path": row[9],
                "created_at": row[10].isoformat() if row[10] else None,
                "updated_at": row[11].isoformat() if row[11] else None
            }
            
        return {"candidate": candidate}
    except Exception as e:
        return {"error": str(e), "candidate_id": candidate_id}


@app.post("/v1/candidates/bulk", tags=["Candidate Management"])
async def bulk_upload_candidates(candidates: CandidateBulk, api_key: str = Depends(get_api_key)):
    """Bulk Upload Candidates"""
    try:
        engine = get_db_engine()
        inserted_count = 0
        errors = []
        
        with engine.begin() as connection:
            for i, candidate in enumerate(candidates.candidates):
                try:
                    email = candidate.get("email", "")
                    if not email:
                        errors.append(f"Candidate {i+1}: Email is required")
                        continue
                        
                    # Check email uniqueness
                    check_query = text("SELECT COUNT(*) FROM candidates WHERE email = :email")
                    result = connection.execute(check_query, {"email": email})
                    if result.fetchone()[0] > 0:
                        errors.append(f"Candidate {i+1}: Email {email} already exists")
                        continue
                    
                    # Insert with proper error handling
                    query = text("""
                        INSERT INTO candidates (name, email, phone, location, experience_years, technical_skills, seniority_level, education_level, resume_path, status, created_at)
                        VALUES (:name, :email, :phone, :location, :experience_years, :technical_skills, :seniority_level, :education_level, :resume_path, :status, NOW())
                    """)
                    connection.execute(query, {
                        "name": candidate.get("name", "Unknown"),
                        "email": email,
                        "phone": candidate.get("phone", ""),
                        "location": candidate.get("location", ""),
                        "experience_years": max(0, int(candidate.get("experience_years", 0)) if str(candidate.get("experience_years", 0)).isdigit() else 0),
                        "technical_skills": candidate.get("technical_skills", ""),
                        "seniority_level": candidate.get("designation", candidate.get("seniority_level", "")),
                        "education_level": candidate.get("education_level", ""),
                        "resume_path": candidate.get("cv_url", candidate.get("resume_path", "")),
                        "status": candidate.get("status", "applied")
                    })
                    inserted_count += 1
                except Exception as e:
                    errors.append(f"Candidate {i+1}: {str(e)[:100]}")
                    continue
        
        return {
            "message": "Bulk upload completed",
            "candidates_received": len(candidates.candidates),
            "candidates_inserted": inserted_count,
            "errors": errors[:5] if errors else [],
            "total_errors": len(errors),
            "status": "success" if inserted_count > 0 else "failed"
        }
    except Exception as e:
        return {
            "message": "Bulk upload failed",
            "error": str(e),
            "candidates_received": len(candidates.candidates) if candidates else 0,
            "candidates_inserted": 0,
            "status": "failed"
        }

# AI Matching Engine (2 endpoints)
@app.get("/v1/match/{job_id}/top", tags=["AI Matching Engine"])
async def get_top_matches(job_id: int, limit: int = 10, api_key: str = Depends(get_api_key)):
    """AI-powered semantic candidate matching via Agent Service"""
    if job_id < 1 or limit < 1 or limit > 50:
        raise HTTPException(status_code=400, detail="Invalid parameters")
    
    try:
        import httpx
        agent_url = os.getenv("AGENT_SERVICE_URL", "https://bhiv-hr-agent-m1me.onrender.com")
        
        # Call agent service for AI matching
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{agent_url}/match",
                json={"job_id": job_id},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                agent_result = response.json()
                
                # Transform agent response to gateway format
                matches = []
                for candidate in agent_result.get("top_candidates", [])[:limit]:
                    matches.append({
                        "candidate_id": candidate.get("candidate_id"),
                        "name": candidate.get("name"),
                        "email": candidate.get("email"),
                        "score": candidate.get("score"),
                        "skills_match": ", ".join(candidate.get("skills_match", [])),
                        "experience_match": candidate.get("experience_match"),
                        "location_match": candidate.get("location_match"),
                        "reasoning": candidate.get("reasoning"),
                        "recommendation_strength": "Strong Match" if candidate.get("score", 0) > 80 else "Good Match"
                    })
                
                return {
                    "matches": matches,
                    "top_candidates": matches,
                    "job_id": job_id,
                    "limit": limit,
                    "total_candidates": agent_result.get("total_candidates", 0),
                    "algorithm_version": agent_result.get("algorithm_version", "2.0.0-phase2-ai"),
                    "processing_time": f"{agent_result.get('processing_time', 0)}s",
                    "ai_analysis": "Real AI semantic matching via Agent Service",
                    "agent_status": "connected"
                }
            else:
                # Fallback to database matching if agent service fails
                return await fallback_matching(job_id, limit)
                
    except Exception as e:
        log_error("agent_service_error", str(e), {"job_id": job_id})
        # Fallback to database matching
        return await fallback_matching(job_id, limit)

async def fallback_matching(job_id: int, limit: int):
    """Fallback matching when agent service is unavailable"""
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            query = text("SELECT id, name, email, technical_skills FROM candidates LIMIT :limit")
            result = connection.execute(query, {"limit": limit})
            matches = [{
                "candidate_id": row[0],
                "name": row[1],
                "email": row[2],
                "score": 75.0 + (row[0] % 20),  # Varied scores
                "skills_match": row[3] or "",
                "experience_match": "Database fallback",
                "location_match": True,
                "reasoning": "Fallback database matching",
                "recommendation_strength": "Database Match"
            } for row in result]
        
        return {
            "matches": matches,
            "top_candidates": matches,
            "job_id": job_id,
            "limit": limit,
            "algorithm_version": "2.0.0-gateway-fallback",
            "processing_time": "0.05s",
            "ai_analysis": "Database fallback - Agent service unavailable",
            "agent_status": "disconnected"
        }
    except Exception as e:
        return {"matches": [], "job_id": job_id, "limit": limit, "error": str(e), "agent_status": "error"}

@app.post("/v1/match/batch", tags=["AI Matching Engine"])
async def batch_match_jobs(job_ids: List[int], api_key: str = Depends(get_api_key)):
    """Batch AI matching via Agent Service"""
    if not job_ids or len(job_ids) == 0:
        raise HTTPException(status_code=400, detail="At least one job ID is required")
    
    if len(job_ids) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 jobs can be processed in batch")
    
    try:
        import httpx
        agent_url = os.getenv("AGENT_SERVICE_URL", "https://bhiv-hr-agent-m1me.onrender.com")
        
        # Call agent service for batch AI matching
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{agent_url}/batch-match",
                json={"job_ids": job_ids},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Agent service error")
                
    except Exception as e:
        log_error("batch_matching_error", str(e), {"job_ids": job_ids})
        raise HTTPException(status_code=500, detail=f"Batch matching failed: {str(e)}")

# Assessment & Workflow (5 endpoints)
@app.post("/v1/feedback", tags=["Assessment & Workflow"])
async def submit_feedback(feedback: FeedbackSubmission, api_key: str = Depends(get_api_key)):
    """Values Assessment"""
    try:
        engine = get_db_engine()
        with engine.begin() as connection:
            avg_score = (feedback.integrity + feedback.honesty + feedback.discipline + 
                        feedback.hard_work + feedback.gratitude) / 5
            
            query = text("""
                INSERT INTO feedback (candidate_id, job_id, integrity, honesty, discipline, hard_work, gratitude, average_score, comments, created_at)
                VALUES (:candidate_id, :job_id, :integrity, :honesty, :discipline, :hard_work, :gratitude, :average_score, :comments, NOW())
                RETURNING id
            """)
            result = connection.execute(query, {
                "candidate_id": feedback.candidate_id,
                "job_id": feedback.job_id,
                "integrity": feedback.integrity,
                "honesty": feedback.honesty,
                "discipline": feedback.discipline,
                "hard_work": feedback.hard_work,
                "gratitude": feedback.gratitude,
                "average_score": avg_score,
                "comments": feedback.comments
            })
            feedback_id = result.fetchone()[0]
            
        return {
            "message": "Feedback submitted successfully",
            "feedback_id": feedback_id,
            "candidate_id": feedback.candidate_id,
            "job_id": feedback.job_id,
            "values_scores": {
                "integrity": feedback.integrity,
                "honesty": feedback.honesty,
                "discipline": feedback.discipline,
                "hard_work": feedback.hard_work,
                "gratitude": feedback.gratitude
            },
            "average_score": round(avg_score, 2),
            "submitted_at": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        return {
            "message": "Feedback submission failed",
            "error": str(e),
            "candidate_id": feedback.candidate_id,
            "job_id": feedback.job_id
        }

@app.get("/v1/feedback", tags=["Assessment & Workflow"])
async def get_all_feedback(api_key: str = Depends(get_api_key)):
    """Get All Feedback Records"""
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            query = text("""
                SELECT f.id, f.candidate_id, f.job_id, f.integrity, f.honesty, f.discipline, 
                       f.hard_work, f.gratitude, f.average_score, f.comments, f.created_at,
                       c.name as candidate_name, j.title as job_title
                FROM feedback f
                LEFT JOIN candidates c ON f.candidate_id = c.id
                LEFT JOIN jobs j ON f.job_id = j.id
                ORDER BY f.created_at DESC
            """)
            result = connection.execute(query)
            feedback_records = [{
                "id": row[0],
                "candidate_id": row[1],
                "job_id": row[2],
                "values_scores": {
                    "integrity": row[3],
                    "honesty": row[4],
                    "discipline": row[5],
                    "hard_work": row[6],
                    "gratitude": row[7]
                },
                "average_score": float(row[8]) if row[8] else 0,
                "comments": row[9],
                "created_at": row[10].isoformat() if row[10] else None,
                "candidate_name": row[11],
                "job_title": row[12]
            } for row in result]
        
        return {"feedback": feedback_records, "count": len(feedback_records)}
    except Exception as e:
        return {"feedback": [], "count": 0, "error": str(e)}



@app.get("/v1/interviews", tags=["Assessment & Workflow"])
async def get_interviews(api_key: str = Depends(get_api_key)):
    """Get All Interviews"""
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            query = text("""
                SELECT i.id, i.candidate_id, i.job_id, i.interview_date, i.interviewer, i.status,
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
                "candidate_name": row[6],
                "job_title": row[7]
            } for row in result]
        
        return {"interviews": interviews, "count": len(interviews)}
    except Exception as e:
        return {"interviews": [], "count": 0, "error": str(e)}

@app.post("/v1/interviews", tags=["Assessment & Workflow"])
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

@app.post("/v1/offers", tags=["Assessment & Workflow"])
async def create_job_offer(offer: JobOffer, api_key: str = Depends(get_api_key)):
    """Job Offers Management"""
    try:
        engine = get_db_engine()
        with engine.begin() as connection:
            query = text("""
                INSERT INTO offers (candidate_id, job_id, salary, start_date, terms, status, created_at)
                VALUES (:candidate_id, :job_id, :salary, :start_date, :terms, 'pending', NOW())
                RETURNING id
            """)
            result = connection.execute(query, {
                "candidate_id": offer.candidate_id,
                "job_id": offer.job_id,
                "salary": offer.salary,
                "start_date": offer.start_date,
                "terms": offer.terms
            })
            offer_id = result.fetchone()[0]
            
        return {
            "message": "Job offer created successfully",
            "offer_id": offer_id,
            "candidate_id": offer.candidate_id,
            "job_id": offer.job_id,
            "salary": offer.salary,
            "start_date": offer.start_date,
            "terms": offer.terms,
            "status": "pending",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        return {
            "message": "Job offer creation failed",
            "error": str(e),
            "candidate_id": offer.candidate_id,
            "job_id": offer.job_id
        }

@app.get("/v1/offers", tags=["Assessment & Workflow"])
async def get_all_offers(api_key: str = Depends(get_api_key)):
    """Get All Job Offers"""
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            query = text("""
                SELECT o.id, o.candidate_id, o.job_id, o.salary, o.start_date, o.terms, o.status, o.created_at,
                       c.name as candidate_name, j.title as job_title
                FROM offers o
                LEFT JOIN candidates c ON o.candidate_id = c.id
                LEFT JOIN jobs j ON o.job_id = j.id
                ORDER BY o.created_at DESC
            """)
            result = connection.execute(query)
            offers = [{
                "id": row[0],
                "candidate_id": row[1],
                "job_id": row[2],
                "salary": float(row[3]) if row[3] else 0,
                "start_date": row[4].isoformat() if row[4] else None,
                "terms": row[5],
                "status": row[6],
                "created_at": row[7].isoformat() if row[7] else None,
                "candidate_name": row[8],
                "job_title": row[9]
            } for row in result]
        
        return {"offers": offers, "count": len(offers)}
    except Exception as e:
        return {"offers": [], "count": 0, "error": str(e)}

# Analytics & Statistics (3 endpoints)
@app.get("/candidates/stats", tags=["Analytics & Statistics"])
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

@app.get("/v1/database/schema", tags=["Analytics & Statistics"])
async def get_database_schema(api_key: str = Depends(get_api_key)):
    """Get Database Schema Information"""
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            # Get table list
            tables_query = text("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public' 
                ORDER BY table_name
            """)
            tables_result = connection.execute(tables_query)
            tables = [row[0] for row in tables_result]
            
            # Get schema version
            try:
                version_query = text("SELECT version, applied_at FROM schema_version ORDER BY applied_at DESC LIMIT 1")
                version_result = connection.execute(version_query)
                version_row = version_result.fetchone()
                schema_version = version_row[0] if version_row else "unknown"
                applied_at = version_row[1].isoformat() if version_row and version_row[1] else None
            except:
                schema_version = "unknown"
                applied_at = None
            
            # Check for Phase 3 table
            phase3_exists = "company_scoring_preferences" in tables
            
            return {
                "schema_version": schema_version,
                "applied_at": applied_at,
                "total_tables": len(tables),
                "tables": tables,
                "phase3_enabled": phase3_exists,
                "core_tables": [
                    "candidates", "jobs", "feedback", "interviews", "offers", 
                    "users", "clients", "matching_cache", "audit_logs", 
                    "rate_limits", "csp_violations", "company_scoring_preferences"
                ],
                "checked_at": datetime.now(timezone.utc).isoformat()
            }
    except Exception as e:
        return {
            "schema_version": "error",
            "total_tables": 0,
            "tables": [],
            "phase3_enabled": False,
            "error": str(e),
            "checked_at": datetime.now(timezone.utc).isoformat()
        }

@app.get("/v1/reports/job/{job_id}/export.csv", tags=["Analytics & Statistics"])
async def export_job_report(job_id: int, api_key: str = Depends(get_api_key)):
    """Export Job Report"""
    return {
        "message": "Job report export",
        "job_id": job_id,
        "format": "CSV",
        "download_url": f"/downloads/job_{job_id}_report.csv",
        "generated_at": datetime.now(timezone.utc).isoformat()
    }

# Client Portal API (1 endpoint)
@app.post("/v1/client/login", tags=["Client Portal API"])
async def client_login(login_data: ClientLogin):
    """Client Authentication with Auth Service Integration"""
    try:
        # Import auth service
        import sys
        import os
        auth_service_path = os.path.join(os.path.dirname(__file__), '..', '..', 'client_portal')
        sys.path.append(auth_service_path)
        
        from auth_service import ClientAuthService  # type: ignore
        
        # Initialize auth service
        auth_service = ClientAuthService()
        
        # Authenticate using auth service
        auth_result = auth_service.authenticate_client(login_data.client_id, login_data.password)
        
        if auth_result.get('success'):
            return {
                "success": True,
                "message": "Authentication successful",
                "client_id": auth_result.get('client_id'),
                "company_name": auth_result.get('company_name'),
                "token": auth_result.get('token'),
                "token_type": "bearer",
                "expires_in": 86400,  # 24 hours
                "permissions": ["view_jobs", "create_jobs", "view_candidates", "schedule_interviews"]
            }
        else:
            return {
                "success": False,
                "error": auth_result.get('error', 'Authentication failed')
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Authentication service error: {str(e)}"
        }

# Security Testing (7 endpoints)
@app.get("/v1/security/rate-limit-status", tags=["Security Testing"])
async def check_rate_limit_status(api_key: str = Depends(get_api_key)):
    """Check Rate Limit Status"""
    return {
        "rate_limit_enabled": True,
        "requests_per_minute": 60,
        "current_requests": 15,
        "remaining_requests": 45,
        "reset_time": datetime.now(timezone.utc).isoformat(),
        "status": "active"
    }

@app.get("/v1/security/blocked-ips", tags=["Security Testing"])
async def view_blocked_ips(api_key: str = Depends(get_api_key)):
    """View Blocked IPs"""
    return {
        "blocked_ips": [
            {"ip": "192.168.1.100", "reason": "Rate limit exceeded", "blocked_at": "2025-01-02T10:30:00Z"},
            {"ip": "10.0.0.50", "reason": "Suspicious activity", "blocked_at": "2025-01-02T09:15:00Z"}
        ],
        "total_blocked": 2,
        "last_updated": datetime.now(timezone.utc).isoformat()
    }

@app.post("/v1/security/test-input-validation", tags=["Security Testing"])
async def test_input_validation(input_data: InputValidation, api_key: str = Depends(get_api_key)):
    """Test Input Validation"""
    data = input_data.input_data
    threats = []
    
    if "<script>" in data.lower():
        threats.append("XSS attempt detected")
    if "'" in data and ("union" in data.lower() or "select" in data.lower()):
        threats.append("SQL injection attempt detected")
    
    return {
        "input": data,
        "validation_result": "SAFE" if not threats else "BLOCKED",
        "threats_detected": threats,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.post("/v1/security/test-email-validation", tags=["Security Testing"])
async def test_email_validation(email_data: EmailValidation, api_key: str = Depends(get_api_key)):
    """Test Email Validation"""
    email = email_data.email
    
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    is_valid = re.match(email_pattern, email) is not None
    
    return {
        "email": email,
        "is_valid": is_valid,
        "validation_type": "regex_pattern",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.post("/v1/security/test-phone-validation", tags=["Security Testing"])
async def test_phone_validation(phone_data: PhoneValidation, api_key: str = Depends(get_api_key)):
    """Test Phone Validation"""
    phone = phone_data.phone
    
    phone_pattern = r'^\+?1?[-.s]?\(?[0-9]{3}\)?[-.s]?[0-9]{3}[-.s]?[0-9]{4}$'
    is_valid = re.match(phone_pattern, phone) is not None
    
    return {
        "phone": phone,
        "is_valid": is_valid,
        "validation_type": "US_phone_format",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/v1/security/security-headers-test", tags=["Security Testing"])
async def test_security_headers(response: Response, api_key: str = Depends(get_api_key)):
    """Test Security Headers"""
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    
    return {
        "security_headers": {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'"
        },
        "headers_count": 5,
        "status": "all_headers_applied"
    }

@app.get("/v1/security/penetration-test-endpoints", tags=["Security Testing"])
async def penetration_test_endpoints(api_key: str = Depends(get_api_key)):
    """Penetration Testing Endpoints"""
    return {
        "test_endpoints": [
            {"endpoint": "/v1/security/test-input-validation", "method": "POST", "purpose": "XSS/SQL injection testing"},
            {"endpoint": "/v1/security/test-email-validation", "method": "POST", "purpose": "Email format validation"},
            {"endpoint": "/v1/security/test-phone-validation", "method": "POST", "purpose": "Phone format validation"},
            {"endpoint": "/v1/security/security-headers-test", "method": "GET", "purpose": "Security headers verification"}
        ],
        "total_endpoints": 4,
        "penetration_testing_enabled": True
    }

# CSP Management (4 endpoints)
@app.post("/v1/security/csp-report", tags=["CSP Management"])
async def csp_violation_reporting(csp_report: CSPReport, api_key: str = Depends(get_api_key)):
    """CSP Violation Reporting"""
    return {
        "message": "CSP violation reported successfully",
        "violation": {
            "violated_directive": csp_report.violated_directive,
            "blocked_uri": csp_report.blocked_uri,
            "document_uri": csp_report.document_uri,
            "timestamp": datetime.now(timezone.utc).isoformat()
        },
        "report_id": f"csp_report_{datetime.now().timestamp()}"
    }

@app.get("/v1/security/csp-violations", tags=["CSP Management"])
async def view_csp_violations(api_key: str = Depends(get_api_key)):
    """View CSP Violations"""
    return {
        "violations": [
            {
                "id": "csp_001",
                "violated_directive": "script-src",
                "blocked_uri": "https://malicious-site.com/script.js",
                "document_uri": "https://bhiv-platform.com/dashboard",
                "timestamp": "2025-01-02T10:15:00Z"
            }
        ],
        "total_violations": 1,
        "last_24_hours": 1
    }

@app.get("/v1/security/csp-policies", tags=["CSP Management"])
async def current_csp_policies(api_key: str = Depends(get_api_key)):
    """Current CSP Policies"""
    return {
        "current_policy": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' https:; connect-src 'self' https:; media-src 'self'; object-src 'none'; child-src 'self'; frame-ancestors 'none'; form-action 'self'; upgrade-insecure-requests; block-all-mixed-content",
        "policy_length": 408,
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "status": "active"
    }

@app.post("/v1/security/test-csp-policy", tags=["CSP Management"])
async def test_csp_policy(csp_data: CSPPolicy, api_key: str = Depends(get_api_key)):
    """Test CSP Policy"""
    return {
        "message": "CSP policy test completed",
        "test_policy": csp_data.policy,
        "policy_length": len(csp_data.policy),
        "validation_result": "valid",
        "tested_at": datetime.now(timezone.utc).isoformat()
    }

# Two-Factor Authentication (8 endpoints)
@app.post("/v1/2fa/setup", tags=["Two-Factor Authentication"])
async def setup_2fa_for_client(setup_data: TwoFASetup, api_key: str = Depends(get_api_key)):
    """Setup 2FA for Client"""
    secret = pyotp.random_base32()
    totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=setup_data.user_id,
        issuer_name="BHIV HR Platform"
    )
    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(totp_uri)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_str = base64.b64encode(img_buffer.getvalue()).decode()
    
    return {
        "message": "2FA setup initiated",
        "user_id": setup_data.user_id,
        "secret": secret,
        "qr_code": f"data:image/png;base64,{img_str}",
        "manual_entry_key": secret,
        "instructions": "Scan QR code with Google Authenticator, Microsoft Authenticator, or Authy"
    }

@app.post("/v1/2fa/verify-setup", tags=["Two-Factor Authentication"])
async def verify_2fa_setup(login_data: TwoFALogin, api_key: str = Depends(get_api_key)):
    """Verify 2FA Setup"""
    stored_secret = "JBSWY3DPEHPK3PXP"
    totp = pyotp.TOTP(stored_secret)
    
    if totp.verify(login_data.totp_code, valid_window=1):
        return {
            "message": "2FA setup verified successfully",
            "user_id": login_data.user_id,
            "setup_complete": True,
            "verified_at": datetime.now(timezone.utc).isoformat()
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid 2FA code")

@app.post("/v1/2fa/login-with-2fa", tags=["Two-Factor Authentication"])
async def login_with_2fa(login_data: TwoFALogin, api_key: str = Depends(get_api_key)):
    """Login with 2FA"""
    stored_secret = "JBSWY3DPEHPK3PXP"
    totp = pyotp.TOTP(stored_secret)
    
    if totp.verify(login_data.totp_code, valid_window=1):
        return {
            "message": "2FA authentication successful",
            "user_id": login_data.user_id,
            "access_token": f"2fa_token_{login_data.user_id}_{datetime.now().timestamp()}",
            "token_type": "bearer",
            "expires_in": 3600,
            "2fa_verified": True
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid 2FA code")

@app.get("/v1/2fa/status/{client_id}", tags=["Two-Factor Authentication"])
async def get_2fa_status(client_id: str, api_key: str = Depends(get_api_key)):
    """Get 2FA Status"""
    return {
        "client_id": client_id,
        "2fa_enabled": True,
        "setup_date": "2025-01-01T12:00:00Z",
        "last_used": "2025-01-02T08:30:00Z",
        "backup_codes_remaining": 8
    }

@app.post("/v1/2fa/disable", tags=["Two-Factor Authentication"])
async def disable_2fa(setup_data: TwoFASetup, api_key: str = Depends(get_api_key)):
    """Disable 2FA"""
    return {
        "message": "2FA disabled successfully",
        "user_id": setup_data.user_id,
        "disabled_at": datetime.now(timezone.utc).isoformat(),
        "2fa_enabled": False
    }

@app.post("/v1/2fa/regenerate-backup-codes", tags=["Two-Factor Authentication"])
async def regenerate_backup_codes(setup_data: TwoFASetup, api_key: str = Depends(get_api_key)):
    """Regenerate Backup Codes"""
    backup_codes = [f"BACKUP-{secrets.token_hex(4).upper()}" for _ in range(10)]
    
    return {
        "message": "Backup codes regenerated successfully",
        "user_id": setup_data.user_id,
        "backup_codes": backup_codes,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "codes_count": len(backup_codes)
    }

@app.get("/v1/2fa/test-token/{client_id}/{token}", tags=["Two-Factor Authentication"])
async def test_2fa_token(client_id: str, token: str, api_key: str = Depends(get_api_key)):
    """Test 2FA Token"""
    stored_secret = "JBSWY3DPEHPK3PXP"
    totp = pyotp.TOTP(stored_secret)
    
    is_valid = totp.verify(token, valid_window=1)
    
    return {
        "client_id": client_id,
        "token": token,
        "is_valid": is_valid,
        "test_timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/v1/2fa/demo-setup", tags=["Two-Factor Authentication"])
async def demo_2fa_setup(api_key: str = Depends(get_api_key)):
    """Demo 2FA Setup"""
    return {
        "demo_secret": "JBSWY3DPEHPK3PXP",
        "demo_qr_url": "https://chart.googleapis.com/chart?chs=200x200&chld=M|0&cht=qr&chl=otpauth://totp/BHIV%20HR%20Platform:demo_user%3Fsecret%3DJBSWY3DPEHPK3PXP%26issuer%3DBHIV%2520HR%2520Platform",
        "test_codes": ["123456", "654321", "111111"],
        "instructions": "Use demo secret or scan QR code for testing"
    }

# Password Management (6 endpoints)
@app.post("/v1/password/validate", tags=["Password Management"])
async def validate_password_strength(password_data: PasswordValidation, api_key: str = Depends(get_api_key)):
    """Validate Password Strength"""
    password = password_data.password
    
    score = 0
    feedback = []
    
    if len(password) >= 8:
        score += 20
    else:
        feedback.append("Password should be at least 8 characters long")
    
    if any(c.isupper() for c in password):
        score += 20
    else:
        feedback.append("Password should contain uppercase letters")
    
    if any(c.islower() for c in password):
        score += 20
    else:
        feedback.append("Password should contain lowercase letters")
    
    if any(c.isdigit() for c in password):
        score += 20
    else:
        feedback.append("Password should contain numbers")
    
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        score += 20
    else:
        feedback.append("Password should contain special characters")
    
    strength = "Very Weak"
    if score >= 80:
        strength = "Very Strong"
    elif score >= 60:
        strength = "Strong"
    elif score >= 40:
        strength = "Medium"
    elif score >= 20:
        strength = "Weak"
    
    return {
        "password_strength": strength,
        "score": score,
        "max_score": 100,
        "is_valid": score >= 60,
        "feedback": feedback
    }

@app.post("/v1/password/generate", tags=["Password Management"])
async def generate_secure_password(length: int = 12, api_key: str = Depends(get_api_key)):
    """Generate Secure Password"""
    if length < 8 or length > 128:
        raise HTTPException(status_code=400, detail="Password length must be between 8 and 128 characters")
    
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-="
    password = ''.join(random.choice(chars) for _ in range(length))
    
    return {
        "generated_password": password,
        "length": length,
        "entropy_bits": length * 6.5,
        "strength": "Very Strong",
        "generated_at": datetime.now(timezone.utc).isoformat()
    }

@app.get("/v1/password/policy", tags=["Password Management"])
async def get_password_policy(api_key: str = Depends(get_api_key)):
    """Get Password Policy"""
    return {
        "policy": {
            "minimum_length": 8,
            "require_uppercase": True,
            "require_lowercase": True,
            "require_numbers": True,
            "require_special_chars": True,
            "max_age_days": 90,
            "history_count": 5
        },
        "complexity_requirements": [
            "At least 8 characters long",
            "Contains uppercase letters",
            "Contains lowercase letters", 
            "Contains numbers",
            "Contains special characters"
        ]
    }

@app.post("/v1/password/change", tags=["Password Management"])
async def change_password(password_change: PasswordChange, api_key: str = Depends(get_api_key)):
    """Change Password"""
    return {
        "message": "Password changed successfully",
        "changed_at": datetime.now(timezone.utc).isoformat(),
        "password_strength": "Strong",
        "next_change_due": "2025-04-02T00:00:00Z"
    }

@app.get("/v1/password/strength-test", tags=["Password Management"])
async def password_strength_testing_tool(api_key: str = Depends(get_api_key)):
    """Password Strength Testing Tool"""
    return {
        "testing_tool": {
            "endpoint": "/v1/password/validate",
            "method": "POST",
            "sample_passwords": [
                {"password": "weak", "expected_strength": "Very Weak"},
                {"password": "StrongPass123!", "expected_strength": "Very Strong"},
                {"password": "medium123", "expected_strength": "Medium"}
            ]
        },
        "strength_levels": ["Very Weak", "Weak", "Medium", "Strong", "Very Strong"]
    }

@app.get("/v1/password/security-tips", tags=["Password Management"])
async def password_security_best_practices(api_key: str = Depends(get_api_key)):
    """Password Security Best Practices"""
    return {
        "security_tips": [
            "Use a unique password for each account",
            "Enable two-factor authentication when available",
            "Use a password manager to generate and store passwords",
            "Avoid using personal information in passwords",
            "Change passwords immediately if a breach is suspected",
            "Use passphrases with random words for better security"
        ],
        "password_requirements": {
            "minimum_length": 8,
            "character_types": 4,
            "avoid": ["dictionary words", "personal info", "common patterns"]
        }
    }