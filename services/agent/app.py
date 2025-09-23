from contextlib import contextmanager
from datetime import datetime, timezone
from typing import List, Dict, Any
import asyncio
import json
import logging
import os
import re
import sys

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from psycopg2 import pool
from pydantic import BaseModel
import psutil
import psycopg2
# Import semantic engine components
try:
    from semantic_engine import SemanticJobMatcher, AdvancedSemanticMatcher, BatchMatcher, SemanticProcessor
    SEMANTIC_ENABLED = True
    print("SUCCESS: Advanced semantic engine loaded")
except ImportError as e:
    SEMANTIC_ENABLED = False
    print(f"WARNING: Semantic matching not available, using fallback: {e}")
    
    # Create fallback classes
    class SemanticJobMatcher:
        def __init__(self): pass
    class AdvancedSemanticMatcher:
        def __init__(self): pass
    class BatchMatcher:
        def __init__(self, max_workers=2): pass
    class SemanticProcessor:
        def __init__(self): pass
        def semantic_match(self, job_dict, candidate_dict): 
            return {'score': 75.0, 'matched_skills': [], 'reasoning': 'Fallback matching'}

# Configure secure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('agent.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)

# Security: Input sanitization for logging
def sanitize_for_logging(input_str: str) -> str:
    """Sanitize input for safe logging to prevent log injection"""
    if not isinstance(input_str, str):
        input_str = str(input_str)
    # Remove control characters and limit length
    sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', input_str)
    return sanitized[:200] + '...' if len(sanitized) > 200 else sanitized

from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="BHIV AI Matching Engine",
    description="Advanced AI-Powered Semantic Candidate Matching Service",
    version="3.2.0"
)

# Mount static files for favicon and assets
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# HTTP Method Handler Middleware (MUST be first)
@app.middleware("http")
async def http_method_handler(request: Request, call_next):
    """Handle HTTP methods including HEAD and OPTIONS requests"""
    method = request.method
    path = request.url.path
    
    # Handle HEAD requests by converting to GET and removing body
    if method == "HEAD":
        # Create new request with GET method
        get_request = Request(
            scope={
                **request.scope,
                "method": "GET"
            }
        )
        response = await call_next(get_request)
        # Remove body content for HEAD response but keep headers
        return Response(
            content="",
            status_code=response.status_code,
            headers=response.headers,
            media_type=response.media_type
        )
    
    # Handle OPTIONS requests for CORS preflight
    elif method == "OPTIONS":
        return Response(
            content="",
            status_code=200,
            headers={
                "Allow": "GET, POST, PUT, DELETE, HEAD, OPTIONS",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, HEAD, OPTIONS",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Max-Age": "86400"
            }
        )
    
    # Handle unsupported methods
    elif method not in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
        return PlainTextResponse(
            content=f"Method {method} not allowed. Supported methods: GET, POST, PUT, DELETE, HEAD, OPTIONS",
            status_code=405,
            headers={
                "Allow": "GET, POST, PUT, DELETE, HEAD, OPTIONS"
            }
        )
    
    return await call_next(request)

# Add CORS middleware with HEAD and OPTIONS support
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"],
    allow_headers=["*"],
)

# Custom OpenAPI schema with organized tags
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="BHIV AI Matching Engine",
        version="3.1.0",
        description="Advanced AI-Powered Semantic Candidate Matching Service",
        routes=app.routes,
    )
    openapi_schema["tags"] = [
        {"name": "Core API Endpoints", "description": "Service health and system information"},
        {"name": "AI Matching Engine", "description": "Semantic candidate matching and scoring"},
        {"name": "Candidate Analysis", "description": "Detailed candidate profile analysis"},
        {"name": "System Diagnostics", "description": "Database connectivity and testing"}
    ]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Initialize semantic engine components
semantic_matcher = None
advanced_matcher = None
batch_matcher = None
semantic_processor = None

if SEMANTIC_ENABLED:
    try:
        # Initialize all semantic components
        semantic_matcher = SemanticJobMatcher()
        advanced_matcher = AdvancedSemanticMatcher()
        batch_matcher = BatchMatcher(max_workers=2)
        semantic_processor = SemanticProcessor()
        
        logger.info("SUCCESS: Complete semantic engine initialized")
    except Exception as e:
        logger.error(f"Failed to initialize semantic engine: {sanitize_for_logging(str(e))}")
        SEMANTIC_ENABLED = False
        semantic_matcher = None
        advanced_matcher = None
        batch_matcher = None
        semantic_processor = None

class MatchRequest(BaseModel):
    job_id: int

class CandidateScore(BaseModel):
    candidate_id: int
    name: str
    email: str
    score: float
    skills_match: List[str]
    experience_match: str
    location_match: bool
    reasoning: str

class MatchResponse(BaseModel):
    job_id: int
    top_candidates: List[CandidateScore]
    total_candidates: int
    processing_time: float
    algorithm_version: str
    status: str

@contextmanager
def get_db_connection():
    """Get database connection with proper resource management
    
    Yields:
        psycopg2.connection: Database connection object
        
    Raises:
        HTTPException: If connection fails
    """
    conn = None
    try:
        # Environment-aware database URL
        environment = os.getenv("ENVIRONMENT", "development").lower()
        if environment == "production":
            # Production database on Render
            default_db_url = "postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@dpg-d373qrogjchc73bu9gug-a.oregon-postgres.render.com/bhiv_hr_nqzb"
        else:
            # Local development database in Docker
            default_db_url = "postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@db:5432/bhiv_hr_nqzb"
        
        database_url = os.getenv("DATABASE_URL", default_db_url)
        if database_url:
            conn = psycopg2.connect(database_url)
        else:
            conn = psycopg2.connect(
                host=os.getenv("DB_HOST", "db"),
                database=os.getenv("DB_NAME", "bhiv_hr_nqzb"),
                user=os.getenv("DB_USER", "bhiv_user"),
                password=os.getenv("DB_PASSWORD", "B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J"),
                port=os.getenv("DB_PORT", "5432")
            )
        
        if not conn:
            raise HTTPException(status_code=500, detail="Database connection failed")
            
        yield conn
        
    except psycopg2.OperationalError as e:
        logger.error(f"Database operational error: {sanitize_for_logging(str(e))}")
        raise HTTPException(status_code=503, detail="Database temporarily unavailable")
    except psycopg2.DatabaseError as e:
        logger.error(f"Database error: {sanitize_for_logging(str(e))}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected database error: {sanitize_for_logging(str(e))}")
        raise HTTPException(status_code=500, detail="Database connection failed")
    finally:
        if conn:
            try:
                conn.close()
            except Exception as e:
                logger.error(f"Error closing connection: {sanitize_for_logging(str(e))}")

def calculate_skills_match(job_requirements: str, candidate_skills: str) -> tuple:
    """Enhanced skills matching with dynamic keyword extraction"""
    if not job_requirements or not candidate_skills:
        return 0.0, []
    
    # Expanded tech keywords with categories
    tech_keywords = {
        'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'go', 'rust', 'php', 'ruby'],
        'web_frontend': ['react', 'angular', 'vue', 'html', 'css', 'bootstrap', 'jquery'],
        'web_backend': ['node', 'express', 'django', 'flask', 'spring', 'laravel'],
        'database': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch'],
        'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform'],
        'data_science': ['machine learning', 'ai', 'data science', 'pandas', 'numpy', 'tensorflow', 'pytorch'],
        'tools': ['git', 'jenkins', 'jira', 'linux', 'unix', 'bash'],
        'mobile': ['android', 'ios', 'react native', 'flutter', 'swift', 'kotlin']
    }
    
    job_req_lower = str(job_requirements).lower() if job_requirements else ""
    candidate_skills_lower = str(candidate_skills).lower() if candidate_skills else ""
    
    # Extract required skills from job requirements
    required_skills = set()
    for category, skills in tech_keywords.items():
        for skill in skills:
            if skill in job_req_lower:
                required_skills.add(skill)
    
    # Find matching skills
    matched_skills = []
    for skill in required_skills:
        if skill in candidate_skills_lower:
            matched_skills.append(skill.title())
    
    # Calculate score with bonus for multiple category matches
    if not required_skills:
        return 0.5, matched_skills  # Neutral score if no specific skills required
    
    base_score = len(matched_skills) / len(required_skills)
    
    # Bonus for diverse skill matching across categories
    matched_categories = set()
    for category, skills in tech_keywords.items():
        if any(skill in candidate_skills_lower for skill in skills):
            matched_categories.add(category)
    
    category_bonus = min(0.2, len(matched_categories) * 0.05)
    final_score = min(1.0, base_score + category_bonus)
    
    return final_score, matched_skills

def calculate_experience_match(job_level: str, candidate_years: int, candidate_level: str) -> tuple:
    """Calculate experience matching score"""
    if not job_level or job_level.strip() == "":
        return 0.5, "No specific level required"
    
    job_level_lower = str(job_level).lower() if job_level else ""
    candidate_level_lower = str(candidate_level).lower() if candidate_level else ""
    
    # Experience level mapping
    level_scores = {
        'entry': (0, 2),
        'junior': (1, 3), 
        'mid': (2, 5),
        'senior': (4, 8),
        'lead': (6, 15),
        'principal': (8, 20)
    }
    
    # Determine required experience range
    required_range = None
    for level, years_range in level_scores.items():
        if level in job_level_lower:
            required_range = years_range
            break
    
    if not required_range:
        return 0.5, "Experience level unclear"
    
    min_years, max_years = required_range
    
    # Calculate score based on candidate experience
    if candidate_years >= min_years and candidate_years <= max_years:
        score = 1.0
        match_desc = f"Perfect match for {job_level} level"
    elif candidate_years < min_years:
        gap = min_years - candidate_years
        score = max(0.3, 1.0 - (gap * 0.2))
        match_desc = f"Below required experience by {gap} years"
    else:
        excess = candidate_years - max_years
        score = max(0.7, 1.0 - (excess * 0.1))
        match_desc = f"Overqualified by {excess} years"
    
    return score, match_desc

def calculate_location_match(job_location: str, candidate_location: str) -> tuple:
    """Calculate location matching"""
    if not job_location or not candidate_location:
        return 0.5, False
    
    job_loc_lower = str(job_location).lower() if job_location else ""
    candidate_loc_lower = str(candidate_location).lower() if candidate_location else ""
    
    # Remote work
    if 'remote' in job_loc_lower:
        return 1.0, True
    
    # Exact match
    if job_loc_lower == candidate_loc_lower:
        return 1.0, True
    
    # City match (basic)
    job_cities = ['mumbai', 'delhi', 'bangalore', 'pune', 'hyderabad', 'chennai']
    for city in job_cities:
        if city in job_loc_lower and city in candidate_loc_lower:
            return 0.9, True
    
    return 0.3, False

@app.get("/", tags=["Core API Endpoints"], summary="AI Service Information")
@app.head("/", tags=["Core API Endpoints"], summary="AI Service Information (HEAD)")
def read_root():
    return {
        "service": "BHIV AI Agent",
        "version": "3.1.0",
        "semantic_engine": "enabled" if SEMANTIC_ENABLED else "fallback",
        "endpoints": {
            "match": "POST /match - Get top candidates for job",
            "analyze": "GET /analyze/{candidate_id} - Analyze candidate",
            "health": "GET /health - Service health check",
            "semantic_status": "GET /semantic-status - Semantic engine status",
            "test_db": "GET /test-db - Database connectivity test",
            "http_methods_test": "GET /http-methods-test - HTTP methods testing",
            "favicon": "GET /favicon.ico - Service favicon"
        },
        "supported_methods": ["GET", "POST", "HEAD", "OPTIONS"]
    }

@app.get("/health", tags=["Core API Endpoints"], summary="Health Check")
@app.head("/health", tags=["Core API Endpoints"], summary="Health Check (HEAD)")
def health_check():
    return {
        "status": "healthy",
        "service": "BHIV AI Agent",
        "version": "3.1.0",
        "semantic_engine": "enabled" if SEMANTIC_ENABLED else "fallback",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "uptime": "operational",
        "methods_supported": ["GET", "HEAD"]
    }

@app.get("/semantic-status", tags=["System Diagnostics"], summary="Semantic Engine Status")
def semantic_engine_status():
    """Check semantic engine status and capabilities"""
    status = {
        "semantic_engine_enabled": SEMANTIC_ENABLED,
        "components": {
            "job_matcher": semantic_matcher is not None,
            "advanced_matcher": advanced_matcher is not None,
            "batch_matcher": batch_matcher is not None,
            "semantic_processor": semantic_processor is not None
        },
        "algorithm_version": "3.0.0-semantic" if SEMANTIC_ENABLED else "2.0.0-fallback",
        "capabilities": []
    }
    
    if SEMANTIC_ENABLED:
        status["capabilities"] = [
            "Advanced semantic matching",
            "Bias mitigation",
            "Skill embeddings",
            "Cultural fit analysis",
            "Batch processing",
            "Model artifacts"
        ]
        
        # Get model statistics if available
        if semantic_processor and hasattr(semantic_processor, 'model_manager'):
            try:
                model_stats = semantic_processor.model_manager.get_model_stats()
                status["model_statistics"] = model_stats
            except Exception as e:
                status["model_statistics"] = {"error": str(e)}
    else:
        status["capabilities"] = ["Basic keyword matching", "Experience scoring", "Location matching"]
        status["fallback_reason"] = "Semantic engine components not available"
    
    return status

@app.get("/test-db", tags=["System Diagnostics"], summary="Database Connectivity Test")
@app.head("/test-db", tags=["System Diagnostics"], summary="Database Connectivity Test (HEAD)")
def test_database():
    """Test database connectivity and return sample data
    
    Returns:
        dict: Database status with candidate count and samples
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                # Get candidate count
                cursor.execute("SELECT COUNT(*) FROM candidates")
                count = cursor.fetchone()[0]
                
                # Get sample candidates for verification
                cursor.execute("SELECT id, name FROM candidates LIMIT 3")
                samples = cursor.fetchall()
        
        logger.info(f"Database test successful: {count} candidates found")
        
        return {
            "status": "connected",
            "candidates_count": count,
            "samples": samples,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "connection_pool": "direct"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Database test error: {sanitize_for_logging(str(e))}")
        return {"error": "Database connectivity issue", "status": "error"}

@app.get("/http-methods-test", tags=["System Diagnostics"], summary="HTTP Methods Testing")
@app.head("/http-methods-test", tags=["System Diagnostics"], summary="HTTP Methods Testing (HEAD)")
@app.options("/http-methods-test", tags=["System Diagnostics"], summary="HTTP Methods Testing (OPTIONS)")
async def http_methods_test(request: Request):
    """HTTP Methods Testing Endpoint for AI Agent Service"""
    method = request.method
    
    response_data = {
        "service": "BHIV AI Agent",
        "method_received": method,
        "supported_methods": ["GET", "POST", "HEAD", "OPTIONS"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "semantic_engine": "enabled" if SEMANTIC_ENABLED else "fallback",
        "status": "method_handled_successfully"
    }
    
    if method == "OPTIONS":
        return Response(
            content="",
            status_code=200,
            headers={
                "Allow": "GET, POST, HEAD, OPTIONS",
                "Access-Control-Allow-Methods": "GET, POST, HEAD, OPTIONS"
            }
        )
    
    return response_data

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """Serve favicon.ico for AI Agent Service"""
    favicon_path = os.path.join(os.path.dirname(__file__), "static", "favicon.ico")
    if os.path.exists(favicon_path):
        return FileResponse(
            favicon_path,
            media_type="image/x-icon",
            headers={
                "Cache-Control": "public, max-age=86400",  # Cache for 24 hours
                "ETag": '"bhiv-ai-favicon-v1"'
            }
        )
    else:
        # Return 204 No Content instead of 404 to reduce log noise
        return Response(status_code=204)

@app.post("/match", response_model=MatchResponse, tags=["AI Matching Engine"], summary="AI-Powered Candidate Matching")
async def match_candidates(request: MatchRequest):
    """Dynamic AI-powered candidate matching based on job requirements"""
    start_time = datetime.now(timezone.utc)
    logger.info(f"Starting dynamic match for job_id: {sanitize_for_logging(str(request.job_id))}")
    
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                # Get job details with enhanced requirements parsing
                cursor.execute("""
                    SELECT title, description, department, location, experience_level, requirements
                    FROM jobs WHERE id = %s
                """, (request.job_id,))
                
                job_data = cursor.fetchone()
                if not job_data:
                    return MatchResponse(
                        job_id=request.job_id,
                        top_candidates=[],
                        total_candidates=0,
                        processing_time=0.0,
                        algorithm_version="2.0.0-dynamic",
                        status="job_not_found"
                    )
                
                job_title, job_desc, job_dept, job_location, job_level, job_requirements = job_data
                logger.info(f"Processing job: {sanitize_for_logging(str(job_title))}")
                
                # Get ALL candidates globally (no job_id filtering for dynamic matching)
                cursor.execute("""
                    SELECT id, name, email, phone, location, experience_years, 
                           technical_skills, seniority_level, education_level
                    FROM candidates 
                    ORDER BY created_at DESC
                """)
                
                candidates = cursor.fetchall()
                logger.info(f"Found {len(candidates)} global candidates for dynamic matching")
                
                if not candidates:
                    logger.warning("No candidates found in database")
                    return MatchResponse(
                        job_id=request.job_id,
                        top_candidates=[],
                        total_candidates=0,
                        processing_time=0.0,
                        algorithm_version="2.0.0-dynamic",
                        status="no_candidates"
                    )
        
        # Use semantic engine if available, otherwise fallback
        if SEMANTIC_ENABLED and semantic_processor:
            logger.info("Using advanced semantic processing")
            scored_candidates = await process_with_semantic_engine(
                job_data, candidates, request.job_id
            )
        else:
            logger.info("Using fallback matching algorithm")
            scored_candidates = process_with_fallback_algorithm(
                job_data, candidates, request.job_id
            )
        
        # Sort by score and get top candidates
        scored_candidates.sort(key=lambda x: x.score, reverse=True)
        top_candidates = scored_candidates[:10]
        
        processing_time = (datetime.now(timezone.utc) - start_time).total_seconds()
        
        algorithm_version = "3.0.0-semantic" if SEMANTIC_ENABLED else "2.0.0-fallback"
        logger.info(f"Matching completed: {len(top_candidates)} candidates, algorithm: {algorithm_version}")
        
        return MatchResponse(
            job_id=request.job_id,
            top_candidates=top_candidates,
            total_candidates=len(candidates),
            processing_time=round(processing_time, 3),
            algorithm_version=algorithm_version,
            status="success"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Matching error: {sanitize_for_logging(str(e))}")
        raise HTTPException(status_code=500, detail="Matching process failed")

async def process_with_semantic_engine(job_data: tuple, candidates: list, job_id: int) -> list:
    """Process candidates using advanced semantic engine with error handling"""
    job_title, job_desc, job_dept, job_location, job_level, job_requirements = job_data
    
    # Prepare job data for semantic processing
    job_dict = {
        'id': job_id,
        'title': job_title,
        'description': job_desc,
        'department': job_dept,
        'location': job_location,
        'experience_level': job_level,
        'requirements': job_requirements
    }
    
    scored_candidates = []
    
    # Process candidates with async optimization
    async def process_candidate(candidate):
        try:
            cand_id, name, email, phone, location, exp_years, skills, seniority, education = candidate
            
            # Prepare candidate data
            candidate_dict = {
                'id': cand_id,
                'name': name,
                'email': email,
                'phone': phone,
                'location': location,
                'experience_years': exp_years or 0,
                'technical_skills': skills or '',
                'seniority_level': seniority or '',
                'education_level': education or ''
            }
            
            # Use semantic processor for matching with error handling
            match_result = semantic_processor.semantic_match(job_dict, candidate_dict)
            
            # Create candidate score object
            return CandidateScore(
                candidate_id=cand_id,
                name=name,
                email=email,
                score=match_result['score'],
                skills_match=match_result.get('matched_skills', []),
                experience_match=match_result.get('reasoning', 'Semantic analysis'),
                location_match=location == job_location if job_location else True,
                reasoning=match_result.get('reasoning', 'Advanced semantic matching')
            )
        except Exception as e:
            logger.error(f"Error processing candidate {cand_id}: {sanitize_for_logging(str(e))}")
            # Return fallback score for failed candidates
            return CandidateScore(
                candidate_id=cand_id,
                name=name,
                email=email,
                score=50.0,
                skills_match=[],
                experience_match="Processing error",
                location_match=False,
                reasoning="Fallback due to processing error"
            )
    
    # Process candidates in batches for better performance
    batch_size = 10
    for i in range(0, len(candidates), batch_size):
        batch = candidates[i:i + batch_size]
        tasks = [process_candidate(candidate) for candidate in batch]
        batch_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in batch_results:
            if isinstance(result, CandidateScore):
                scored_candidates.append(result)
            else:
                logger.error(f"Batch processing error: {sanitize_for_logging(str(result))}")
    
    return scored_candidates

def process_with_fallback_algorithm(job_data: tuple, candidates: list, job_id: int) -> list:
    """Fallback algorithm when semantic engine is not available"""
    job_title, job_desc, job_dept, job_location, job_level, job_requirements = job_data
    
    # Extract job-specific keywords for dynamic matching
    job_text = f"{job_title or ''} {job_desc or ''} {job_requirements or ''}".lower()
        
    # Dynamic skill extraction based on job requirements
    tech_skills_map = {
        'python': ['python', 'django', 'flask', 'pandas', 'numpy'],
        'java': ['java', 'spring', 'hibernate', 'maven', 'gradle'],
        'javascript': ['javascript', 'js', 'react', 'node', 'angular', 'vue'],
        'data science': ['data science', 'machine learning', 'ai', 'tensorflow', 'pytorch'],
        'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes'],
        'database': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis'],
        'web': ['html', 'css', 'react', 'angular', 'vue', 'bootstrap'],
        'mobile': ['android', 'ios', 'react native', 'flutter', 'swift'],
        'devops': ['docker', 'kubernetes', 'jenkins', 'ci/cd', 'terraform']
    }
    
    # Identify required skills from job description
    required_skill_categories = []
    for category, skills in tech_skills_map.items():
        if any(skill in job_text for skill in skills):
            required_skill_categories.append(category)
    
    scored_candidates = []
    
    for candidate in candidates:
        cand_id, name, email, phone, location, exp_years, skills, seniority, education = candidate
        
        candidate_skills_lower = (skills or '').lower()
        
        # Enhanced skills matching
        skills_score = 0.0
        matched_skills = []
        
        if required_skill_categories:
            total_possible_matches = 0
            actual_matches = 0
            
            for category in required_skill_categories:
                category_skills = tech_skills_map[category]
                for skill in category_skills:
                    total_possible_matches += 1
                    if skill in candidate_skills_lower:
                        matched_skills.append(skill.title())
                        actual_matches += 1
            
            skills_score = actual_matches / max(1, total_possible_matches)
        else:
            skills_score, matched_skills = calculate_skills_match(
                job_requirements or job_desc, skills or ""
            )
        
        # Experience scoring
        exp_score, exp_reasoning = calculate_experience_match(
            job_level or "", exp_years or 0, seniority or ""
        )
        
        # Location matching
        location_score, location_match = calculate_location_match(
            job_location or "", location or ""
        )
        
        # Calculate overall score
        raw_score = (skills_score * 0.5 + exp_score * 0.3 + location_score * 0.2)
        overall_score = raw_score * 85 + (cand_id % 10) * 1.5  # Add variation
        overall_score = max(50.0, min(90.0, overall_score))
        
        reasoning = f"Skills: {len(matched_skills)} matches; Experience: {exp_reasoning}"
        
        scored_candidates.append(CandidateScore(
            candidate_id=cand_id,
            name=name,
            email=email,
            score=round(overall_score, 1),
            skills_match=matched_skills[:5],
            experience_match=exp_reasoning,
            location_match=location_match,
            reasoning=reasoning
        ))
    
    return scored_candidates

@app.get("/analyze/{candidate_id}", tags=["Candidate Analysis"], summary="Detailed Candidate Analysis")
async def analyze_candidate(candidate_id: int):
    """Detailed candidate analysis with proper error handling"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT name, email, technical_skills, experience_years, 
                           seniority_level, education_level, location
                    FROM candidates WHERE id = %s
                """, (candidate_id,))
                
                candidate = cursor.fetchone()
                if not candidate:
                    return {
                        "candidate_id": candidate_id,
                        "error": "Candidate not found",
                        "status": "not_found",
                        "available_candidates": "Check /test-db for available candidate IDs"
                    }
                
                name, email, skills, exp_years, seniority, education, location = candidate
        
        # Analyze skills
        skill_categories = {
            'Programming': ['python', 'java', 'javascript', 'c++', 'go'],
            'Web Development': ['react', 'node', 'html', 'css', 'django'],
            'Data Science': ['pandas', 'numpy', 'tensorflow', 'machine learning', 'ai'],
            'Cloud': ['aws', 'azure', 'docker', 'kubernetes'],
            'Database': ['sql', 'mysql', 'postgresql', 'mongodb']
        }
        
        skills_lower = (skills or "").lower()
        categorized_skills = {}
        
        for category, skill_list in skill_categories.items():
            found_skills = [skill for skill in skill_list if skill in skills_lower]
            if found_skills:
                categorized_skills[category] = found_skills
        
        return {
            "candidate_id": candidate_id,
            "name": name,
            "email": email,
            "experience_years": exp_years,
            "seniority_level": seniority,
            "education_level": education,
            "location": location,
            "skills_analysis": categorized_skills,
            "total_skills": len(skills.split(',')) if skills else 0,
            "analysis_timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "success"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analysis error: {sanitize_for_logging(str(e))}")
        return {
            "candidate_id": candidate_id,
            "error": "Analysis failed",
            "status": "error",
            "analysis_timestamp": datetime.now(timezone.utc).isoformat()
        }

@app.get("/status", tags=["System Diagnostics"], summary="Agent Service Status")
def get_agent_status():
    """Agent Service Status with real database connectivity check"""
    # Test actual database connectivity
    db_status = "disconnected"
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                db_status = "active"
    except Exception:
        db_status = "error"
    
    # Count actual endpoints dynamically
    endpoint_count = len([route for route in app.routes if hasattr(route, 'methods')])
    
    return {
        "service": "BHIV AI Agent",
        "status": "operational",
        "version": "3.1.0",
        "semantic_engine": "enabled" if SEMANTIC_ENABLED else "fallback",
        "uptime": "healthy",
        "endpoints_available": endpoint_count,
        "database_connection": db_status,
        "connection_pool": "direct",
        "last_health_check": datetime.now(timezone.utc).isoformat()
    }

@app.get("/version", tags=["System Diagnostics"], summary="Agent Version Information")
def get_agent_version():
    """Agent Version Information"""
    return {
        "service": "BHIV AI Agent",
        "version": "3.1.0",
        "build_date": "2025-01-17",
        "semantic_engine_version": "3.0.0" if SEMANTIC_ENABLED else "2.0.0-fallback",
        "api_version": "v1",
        "supported_features": [
            "AI-powered candidate matching",
            "Semantic analysis",
            "Candidate profiling",
            "Skills categorization",
            "Experience matching"
        ]
    }

@app.get("/metrics", tags=["System Diagnostics"], summary="Agent Metrics Endpoint")
def get_agent_metrics():
    """Agent Metrics Endpoint with real system metrics"""
    try:
        # Get real system metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        memory_usage_mb = memory.used / (1024 * 1024)
        memory_percent = memory.percent
        
        # Test database connectivity and get connection info
        db_connections = 0
        db_status = "disconnected"
        candidate_count = 0
        
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) FROM candidates")
                    candidate_count = cursor.fetchone()[0]
                    db_status = "connected"
                    db_connections = 1
        except Exception:
            pass
        
        return {
            "service_metrics": {
                "database_status": db_status,
                "total_candidates": candidate_count,
                "semantic_engine_status": "enabled" if SEMANTIC_ENABLED else "fallback",
                "connection_pool_status": "direct"
            },
            "performance_metrics": {
                "cpu_usage_percent": round(cpu_percent, 2),
                "memory_usage_mb": round(memory_usage_mb, 2),
                "memory_usage_percent": round(memory_percent, 2),
                "database_connections": db_connections,
                "available_memory_mb": round(memory.available / (1024 * 1024), 2)
            },
            "system_info": {
                "python_version": sys.version.split()[0],
                "platform": sys.platform,
                "process_id": os.getpid()
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        logger.error(f"Metrics collection error: {sanitize_for_logging(str(e))}")
        return {
            "error": "Metrics collection failed",
            "fallback_metrics": {
                "service": "BHIV AI Agent",
                "status": "operational",
                "semantic_engine": "enabled" if SEMANTIC_ENABLED else "fallback"
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)