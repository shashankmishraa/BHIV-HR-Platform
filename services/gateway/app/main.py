from fastapi import FastAPI, HTTPException, Header, Depends, Query, Request
from fastapi.middleware.cors import CORSMiddleware
import time
from datetime import datetime, timezone
import json
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
import os
import httpx
from typing import Optional
from .db.schemas import JobCreate, FeedbackCreate, InterviewCreate, OfferCreate, CandidateCreate, BulkCandidatesRequest
from .client_auth import authenticate_client, create_client_token, verify_client_token

# Semantic processing
try:
    from services.semantic_engine.semantic_processor import SemanticProcessor
    SEMANTIC_ENABLED = True
except ImportError:
    SEMANTIC_ENABLED = False
    SemanticProcessor = None
# from .api import routes_reports  # Temporarily disabled due to pandas issue

# Configure secure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Sanitize log inputs
def sanitize_log_input(input_str):
    if not isinstance(input_str, str):
        return str(input_str)
    return input_str.replace('\n', '').replace('\r', '')[:200]

from fastapi import FastAPI, HTTPException, Header, Depends, Query, Request
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="BHIV HR Platform API Gateway",
    description="Production-Ready AI-Powered Recruiting Platform with Microservices Architecture",
    version="3.0.0"
)

# Custom OpenAPI schema with organized tags
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="BHIV HR Platform API Gateway",
        version="3.0.0",
        description="Production-Ready AI-Powered Recruiting Platform",
        routes=app.routes,
    )
    openapi_schema["tags"] = [
        {"name": "Core API Endpoints", "description": "System health and platform information"},
        {"name": "Job Management", "description": "Create and manage job postings"},
        {"name": "Candidate Management", "description": "Search, filter and manage candidates"},
        {"name": "AI Matching Engine", "description": "Semantic candidate matching and ranking"},
        {"name": "Assessment & Workflow", "description": "Values assessment and hiring workflow"},
        {"name": "Analytics & Statistics", "description": "Platform metrics and reporting"},
        {"name": "Client Portal API", "description": "Client authentication and job management"}
    ]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Add CORS middleware with security
allowed_origins = os.getenv("CORS_ORIGINS", "http://localhost:8501,http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# Include report routes - temporarily disabled
# app.include_router(routes_reports.router, prefix="/v1/reports", tags=["reports"])

# Database connection with fallback
def get_db_engine():
    database_url = os.getenv("DATABASE_URL", "postgresql://bhiv_user:bhiv_pass@db:5432/bhiv_hr")
    return create_engine(database_url, pool_pre_ping=True, pool_recycle=300)

# API key validation with fallback
def validate_api_key(api_key: str) -> bool:
    expected_key = os.getenv("API_KEY_SECRET", "myverysecureapikey123")
    try:
        import secrets
        return secrets.compare_digest(api_key, expected_key)
    except:
        return api_key == expected_key

# Authentication dependency
def get_api_key(authorization: Optional[str] = Header(None), x_api_key: Optional[str] = Header(None)):
    api_key = None
    if authorization and authorization.startswith("Bearer "):
        api_key = authorization[7:]
    elif x_api_key:
        api_key = x_api_key
    
    if not api_key or not validate_api_key(api_key):
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key

@app.get("/", tags=["Core API Endpoints"], summary="API Root Information")
def read_root():
    return {
        "message": "🎯 BHIV HR Platform API Gateway",
        "version": "2.0.0",
        "status": "healthy",
"endpoints": {
            "jobs": "POST/GET /v1/jobs - Job management",
            "candidates": "GET /v1/candidates/job/{id} - List candidates",
            "search": "GET /v1/candidates/search - Search & filter",
            "match": "GET /v1/match/{job_id}/top - AI matching",
            "feedback": "POST /v1/feedback - Values assessment",
            "interviews": "POST /v1/interviews - Schedule interviews",
            "offers": "POST /v1/offers - Job offers",
            "reports": "GET /v1/reports/job/{id}/export.csv - Export reports",
            "values": "POST /v1/feedback - Values assessment with scoring",
            "health": "GET /health - Health check",
            "docs": "GET /docs - API documentation"
        }
    }

@app.get("/health", tags=["Core API Endpoints"], summary="Health Check")
def health_check():
    return {
        "status": "healthy",
        "service": "BHIV HR Gateway",
        "version": "3.0.0-FIXED",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/test-candidates", tags=["Core API Endpoints"], summary="Database Connectivity Test")
def test_candidates():
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            result = connection.execute(text("SELECT COUNT(*) FROM candidates"))
            total = result.fetchone()[0]
            
            result = connection.execute(text("SELECT COUNT(*) FROM candidates LIMIT 50"))
            limited = result.fetchone()[0]
            
        return {
            "total_in_db": total,
            "limited_query": limited,
            "message": "Direct database test"
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/v1/jobs", tags=["Job Management"], summary="Create New Job Posting")
async def create_job(job_data: JobCreate, api_key: str = Depends(get_api_key)):
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            # Create enhanced jobs table
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS jobs (
                    id SERIAL PRIMARY KEY,
                    client_id INTEGER,
                    title VARCHAR(255),
                    description TEXT,
                    department VARCHAR(100),
                    location VARCHAR(255),
                    experience_level VARCHAR(50),
                    employment_type VARCHAR(50),
                    requirements TEXT,
                    status VARCHAR(50) DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """))
            
            query = text("""
                INSERT INTO jobs (client_id, title, description, department, location, 
                                experience_level, employment_type, requirements, status, created_at)
                VALUES (:client_id, :title, :description, :department, :location,
                        :experience_level, :employment_type, :requirements, :status, NOW())
                RETURNING id
            """)
            result = connection.execute(query, {
                "client_id": job_data.client_id,
                "title": job_data.title,
                "description": job_data.description,
                "department": job_data.department,
                "location": job_data.location,
                "experience_level": job_data.experience_level,
                "employment_type": job_data.employment_type,
                "requirements": job_data.requirements,
                "status": job_data.status
            })
            job_id = result.fetchone()[0]
            connection.commit()
            
        return {"message": "Job created successfully", "job_id": job_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/v1/jobs", tags=["Job Management"], summary="List All Active Jobs")
async def list_jobs(api_key: str = Depends(get_api_key)):
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            query = text("""
                SELECT id, title, description, client_id, department, location, 
                       experience_level, employment_type, requirements, status, created_at 
                FROM jobs 
                WHERE status = 'active'
                ORDER BY id ASC
            """)
            result = connection.execute(query)
            
            jobs = []
            for row in result:
                jobs.append({
                    "id": row[0],
                    "title": row[1],
                    "description": row[2],
                    "client_id": row[3],
                    "department": row[4],
                    "location": row[5],
                    "experience_level": row[6],
                    "employment_type": row[7],
                    "requirements": row[8],
                    "status": row[9],
                    "created_at": row[10].isoformat() if row[10] else None
                })
        return {"jobs": jobs, "count": len(jobs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/v1/candidates/job/{job_id}", tags=["Candidate Management"], summary="Get Candidates by Job ID")
async def get_candidates_by_job(job_id: int, api_key: str = Depends(get_api_key)):
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            query = text("""
                SELECT id, name, email, phone, location, cv_url, experience_years, 
                       education_level, technical_skills, seniority_level, status, created_at
                FROM candidates 
                WHERE job_id = :job_id
                ORDER BY created_at DESC
            """)
            result = connection.execute(query, {"job_id": job_id})
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
        return {"job_id": job_id, "candidates": candidates, "count": len(candidates)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/v1/candidates/search", tags=["Candidate Management"], summary="Search & Filter Candidates")
async def search_candidates(
    request: Request,
    q: str = "",
    skills: str = "",
    location: str = "",
    experience_min: int = 0,
    api_key: str = Depends(get_api_key)
):
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            where_conditions = []
            params = {}
            
            # Get job_id from query params manually
            job_id = None
            if "job_id" in request.query_params:
                try:
                    job_id = int(request.query_params["job_id"])
                    where_conditions.append("job_id = :job_id")
                    params["job_id"] = job_id
                except (ValueError, TypeError):
                    pass
            
            if q:
                where_conditions.append("(LOWER(name) LIKE LOWER(:search) OR LOWER(email) LIKE LOWER(:search))")
                params["search"] = f"%{q}%"
            
            if skills:
                where_conditions.append("LOWER(technical_skills) LIKE LOWER(:skills)")
                params["skills"] = f"%{skills}%"
            
            if location:
                where_conditions.append("LOWER(location) LIKE LOWER(:location)")
                params["location"] = f"%{location}%"
            
            if experience_min > 0:
                where_conditions.append("experience_years >= :exp_min")
                params["exp_min"] = experience_min
            
            where_clause = "WHERE " + " AND ".join(where_conditions) if where_conditions else ""
            
            query_str = f"""
                SELECT DISTINCT id, name, email, phone, location, experience_years, 
                       technical_skills, seniority_level, status
                FROM candidates 
                {where_clause}
                ORDER BY experience_years DESC, name ASC
                LIMIT 50
            """
            
            query = text(query_str)
            result = connection.execute(query, params)
            
            # Remove duplicates based on name+email combination
            seen = set()
            candidates = []
            for row in result:
                key = f"{row[1]}_{row[2]}"  # name_email
                if key not in seen:
                    seen.add(key)
                    candidates.append({
                        "id": row[0],
                        "name": row[1],
                        "email": row[2],
                        "phone": row[3],
                        "location": row[4],
                        "experience_years": row[5],
                        "technical_skills": row[6],
                        "seniority_level": row[7],
                        "status": row[8]
                    })
            
        return {
            "candidates": candidates,
            "count": len(candidates),
            "message": f"Found {len(candidates)} unique candidates",
            "filters_applied": {"job_id": job_id, "skills": skills, "location": location, "experience_min": experience_min}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/v1/match/{job_id}/top", tags=["AI Matching Engine"], summary="Get AI-Matched Top Candidates")
async def get_top_candidates(job_id: int, api_key: str = Depends(get_api_key)):
    try:
        # Get job details
        engine = get_db_engine()
        with engine.connect() as connection:
            job_query = text("SELECT requirements, title FROM jobs WHERE id = :job_id")
            job_result = connection.execute(job_query, {"job_id": job_id})
            job_row = job_result.fetchone()
            
            if not job_row:
                return {"job_id": job_id, "top_candidates": [], "status": "job_not_found"}
            
            job_requirements = job_row[0] or job_row[1]
            
            # Get candidates
            candidates_query = text("""
                SELECT id, name, email, phone, location, experience_years, technical_skills
                FROM candidates ORDER BY id LIMIT 50
            """)
            candidates_result = connection.execute(candidates_query)
            
            candidates = []
            for row in candidates_result:
                candidate_data = {
                    'id': row[0],
                    'name': row[1],
                    'email': row[2],
                    'phone': row[3],
                    'location': row[4],
                    'experience_years': row[5],
                    'technical_skills': row[6]
                }
                
                # Enhanced semantic matching
                if SEMANTIC_ENABLED:
                    processor = SemanticProcessor()
                    match_result = processor.enhanced_matching(candidate_data, job_requirements)
                    candidate_data.update({
                        'score': match_result['total_score'],
                        'semantic_similarity': match_result['semantic_similarity'],
                        'skills_match': match_result['skills_match'],
                        'experience_match': match_result['experience_match'],
                        'explanation': match_result['explanation']
                    })
                else:
                    # Fallback basic scoring
                    candidate_data.update({
                        'score': min(100, (candidate_data['experience_years'] * 10) + 50),
                        'explanation': 'Basic scoring - semantic engine not available'
                    })
                
                candidates.append(candidate_data)
            
            # Sort by score
            candidates.sort(key=lambda x: x['score'], reverse=True)
            
        return {
            "job_id": job_id,
            "top_candidates": candidates[:10],
            "status": "success",
            "semantic_enabled": SEMANTIC_ENABLED
        }
    except Exception as e:
        return {"job_id": job_id, "top_candidates": [], "status": "error", "error": str(e)}

@app.post("/v1/feedback", tags=["Assessment & Workflow"], summary="Submit Values Assessment")
async def submit_feedback(feedback_data: FeedbackCreate, api_key: str = Depends(get_api_key)):
    try:
        from .services.values_scoring import ValuesScoring
        
        engine = get_db_engine()
        with engine.connect() as connection:
            # Create enhanced feedback table
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS feedback (
                    id SERIAL PRIMARY KEY,
                    candidate_id INTEGER REFERENCES candidates(id),
                    reviewer VARCHAR(255),
                    free_text TEXT,
                    values_scores JSONB,
                    overall_recommendation VARCHAR(50),
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """))
            
            # Process values assessment
            values_scores = feedback_data.values_scores or {
                "integrity": 3, "honesty": 3, "discipline": 3, "hard_work": 3, "gratitude": 3
            }
            
            values_profile = ValuesScoring.create_values_profile(
                values_scores, 
                getattr(feedback_data, 'feedback_text', '')
            )
            
            query = text("""
                INSERT INTO feedback (candidate_id, reviewer, free_text, values_scores, overall_recommendation, created_at)
                VALUES (:candidate_id, :reviewer, :feedback_text, :values_scores, :recommendation, NOW())
                RETURNING id
            """)
            
            result = connection.execute(query, {
                "candidate_id": feedback_data.candidate_id,
                "reviewer": sanitize_log_input(getattr(feedback_data, 'reviewer', 'Anonymous')),
                "feedback_text": sanitize_log_input(getattr(feedback_data, 'feedback_text', '')),
                "values_scores": json.dumps(values_profile["values_scores"]),
                "recommendation": values_profile["recommendation"]
            })
            feedback_id = result.fetchone()[0]
            
            # Update candidate with values prediction
            connection.execute(text("""
                UPDATE candidates 
                SET values_prediction = :values_scores
                WHERE id = :candidate_id
            """), {
                "candidate_id": feedback_data.candidate_id,
                "values_scores": json.dumps(values_profile["values_scores"])
            })
            
            connection.commit()
            
        return {
            "message": "Values assessment submitted successfully", 
            "feedback_id": feedback_id,
            "values_profile": values_profile
        }
    except Exception as e:
        logger.error(f"Feedback submission error: {sanitize_log_input(str(e))}")
        raise HTTPException(status_code=500, detail="Failed to submit feedback")

@app.post("/v1/interviews", tags=["Assessment & Workflow"], summary="Schedule Interview")
async def schedule_interview(interview_data: InterviewCreate, api_key: str = Depends(get_api_key)):
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS interviews (
                    id SERIAL PRIMARY KEY,
                    candidate_id INTEGER REFERENCES candidates(id),
                    job_id INTEGER REFERENCES jobs(id),
                    interview_date TIMESTAMP,
                    interviewer VARCHAR(255),
                    status VARCHAR(50) DEFAULT 'scheduled',
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """))
            
            query = text("""
                INSERT INTO interviews (candidate_id, job_id, interview_date, interviewer, status, created_at)
                VALUES (:candidate_id, :job_id, :interview_date, :interviewer, 'scheduled', NOW())
                RETURNING id
            """)
            
            result = connection.execute(query, {
                "candidate_id": interview_data.candidate_id,
                "job_id": interview_data.job_id,
                "interview_date": interview_data.interview_date,
                "interviewer": getattr(interview_data, 'interviewer', 'HR Manager')
            })
            interview_id = result.fetchone()[0]
            connection.commit()
            
        return {"message": "Interview scheduled successfully", "interview_id": interview_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/offers", tags=["Assessment & Workflow"], summary="Create Job Offer")
async def make_offer(offer_data: OfferCreate, api_key: str = Depends(get_api_key)):
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS offers (
                    id SERIAL PRIMARY KEY,
                    candidate_id INTEGER REFERENCES candidates(id),
                    job_id INTEGER REFERENCES jobs(id),
                    salary INTEGER,
                    status VARCHAR(50) DEFAULT 'sent',
                    offer_date TIMESTAMP DEFAULT NOW(),
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """))
            
            query = text("""
                INSERT INTO offers (candidate_id, job_id, salary, status, offer_date, created_at)
                VALUES (:candidate_id, :job_id, :salary, :status, NOW(), NOW())
                RETURNING id
            """)
            
            result = connection.execute(query, {
                "candidate_id": offer_data.candidate_id,
                "job_id": offer_data.job_id,
                "salary": getattr(offer_data, 'salary', 100000),
                "status": offer_data.status
            })
            offer_id = result.fetchone()[0]
            connection.commit()
            
        return {"message": "Job offer created successfully", "offer_id": offer_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/candidates/bulk", tags=["Candidate Management"], summary="Bulk Upload Candidates")
async def upload_candidates_bulk(request: BulkCandidatesRequest, api_key: str = Depends(get_api_key)):
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            # Create candidates table if not exists
            connection.execute(text("""
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
            
            inserted_count = 0
            for candidate in request.candidates:
                # Check if candidate already exists
                check_query = text("""
                    SELECT COUNT(*) FROM candidates 
                    WHERE name = :name AND email = :email
                """)
                result = connection.execute(check_query, {
                    "name": candidate.name,
                    "email": candidate.email
                })
                exists = result.fetchone()[0] > 0
                
                if not exists:
                    query = text("""
                        INSERT INTO candidates (job_id, name, email, phone, location, cv_url, 
                                              experience_years, education_level, technical_skills, 
                                              seniority_level, status, created_at)
                        VALUES (:job_id, :name, :email, :phone, :location, :cv_url, 
                                :experience_years, :education_level, :technical_skills, 
                                :seniority_level, :status, NOW())
                    """)
                    connection.execute(query, {
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
            
            connection.commit()
        
        return {
            "message": f"Successfully uploaded {inserted_count} new candidates (duplicates skipped)",
            "count": inserted_count,
            "total_processed": len(request.candidates),
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload candidates: {str(e)}")

@app.get("/candidates/stats", tags=["Analytics & Statistics"], summary="Platform Statistics")
def get_candidate_stats():
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            candidates_result = connection.execute(text("SELECT COUNT(*) FROM candidates"))
            total_candidates = candidates_result.fetchone()[0]
            
            jobs_result = connection.execute(text("SELECT COUNT(*) FROM jobs"))
            total_jobs = jobs_result.fetchone()[0]
            
            feedback_result = connection.execute(text("SELECT COUNT(*) FROM feedback"))
            total_feedback = feedback_result.fetchone()[0]
            
            return {
                "total_candidates": total_candidates,
                "total_jobs": total_jobs,
                "total_feedback": total_feedback,
                "status": "success"
            }
    except Exception as e:
        return {"total_candidates": 0, "total_jobs": 0, "total_feedback": 0, "status": "error"}

# Client Portal Endpoints
from pydantic import BaseModel

class ClientLoginRequest(BaseModel):
    client_id: str
    access_code: str

@app.post("/v1/client/login", tags=["Client Portal API"], summary="Client Authentication")
async def client_login(request: ClientLoginRequest):
    """Client authentication endpoint"""
    client_data = authenticate_client(request.client_id, request.access_code)
    if not client_data:
        raise HTTPException(status_code=401, detail="Invalid client credentials")
    
    token = create_client_token(client_data["client_id"], client_data["client_name"])
    return {
        "access_token": token,
        "token_type": "bearer",
        "client_name": client_data["client_name"]
    }

@app.get("/v1/client/jobs", tags=["Client Portal API"], summary="Get Client Jobs")
async def get_client_jobs(client_data: dict = Depends(verify_client_token)):
    """Get jobs for authenticated client"""
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            query = text("""
                SELECT id, title, description, created_at, status
                FROM jobs WHERE client_id = :client_id
                ORDER BY created_at DESC
            """)
            result = connection.execute(query, {"client_id": client_data["client_id"]})
            jobs = []
            for row in result:
                jobs.append({
                    "id": row[0],
                    "title": row[1],
                    "description": row[2],
                    "created_at": row[3].isoformat() if row[3] else None,
                    "status": row[4]
                })
        return {"jobs": jobs, "count": len(jobs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))