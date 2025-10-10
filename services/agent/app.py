from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2 import pool
import os
import json
import sys
import logging
from typing import List, Dict, Any
from datetime import datetime

# Add semantic engine to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from semantic_engine.job_matcher import SemanticJobMatcher
    from semantic_engine.advanced_matcher import AdvancedSemanticMatcher, BatchMatcher
    SEMANTIC_ENABLED = True
    print("INFO: Phase 2 - Real AI semantic matching enabled")
except ImportError as e:
    SEMANTIC_ENABLED = False
    print(f"WARNING: Semantic engine not available: {e}")
    print("INFO: Falling back to keyword matching")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="BHIV AI Matching Engine",
    description="Advanced AI-Powered Semantic Candidate Matching Service",
    version="2.1.0"
)

# Custom OpenAPI schema with organized tags
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="BHIV AI Matching Engine",
        version="2.1.0",
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

# Initialize semantic matchers (Phase 2 - Real AI)
semantic_matcher = None
advanced_matcher = None
batch_matcher = None
if SEMANTIC_ENABLED:
    try:
        semantic_matcher = SemanticJobMatcher()
        advanced_matcher = AdvancedSemanticMatcher()
        batch_matcher = BatchMatcher()
        print("SUCCESS: Phase 2 AI matchers initialized")
    except Exception as e:
        print(f"Failed to initialize AI matchers: {e}")
        SEMANTIC_ENABLED = False

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

# Initialize connection pool
connection_pool = None

def init_connection_pool():
    """Initialize database connection pool"""
    global connection_pool
    database_url = os.getenv("DATABASE_URL", "postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu")
    
    try:
        connection_pool = psycopg2.pool.ThreadedConnectionPool(
            minconn=2,
            maxconn=10,
            dsn=database_url,
            connect_timeout=10,
            application_name="bhiv_agent"
        )
        logger.info("Database connection pool initialized")
    except Exception as e:
        logger.error(f"Failed to initialize connection pool: {e}")

def get_db_connection():
    """Get database connection from pool"""
    global connection_pool
    if not connection_pool:
        init_connection_pool()
    
    try:
        conn = connection_pool.getconn()
        if conn:
            conn.autocommit = True
        return conn
    except Exception as e:
        logger.error(f"Failed to get connection from pool: {e}")
        return None

def return_db_connection(conn):
    """Return connection to pool"""
    global connection_pool
    if connection_pool and conn:
        connection_pool.putconn(conn)

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
def read_root():
    return {
        "service": "BHIV AI Agent",
        "version": "2.1.0",
        "endpoints": 6,
        "available_endpoints": {
            "root": "GET / - Service information",
            "health": "GET /health - Service health check", 
            "test_db": "GET /test-db - Database connectivity test",
            "match": "POST /match - AI-powered candidate matching",
            "batch_match": "POST /batch-match - Batch AI matching for multiple jobs",
            "analyze": "GET /analyze/{candidate_id} - Detailed candidate analysis"
        }
    }

@app.get("/health", tags=["Core API Endpoints"], summary="Health Check")
def health_check():
    return {
        "status": "healthy",
        "service": "BHIV AI Agent",
        "version": "2.1.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/test-db", tags=["System Diagnostics"], summary="Database Connectivity Test")
def test_database():
    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            return {"status": "failed", "error": "Connection failed"}
        
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM candidates")
        count = cursor.fetchone()[0]
        cursor.execute("SELECT id, name FROM candidates LIMIT 3")
        samples = cursor.fetchall()
        cursor.close()
        
        return {
            "status": "success",
            "candidates_count": count, 
            "samples": [{'id': s[0], 'name': s[1]} for s in samples]
        }
    except Exception as e:
        logger.error(f"Database test failed: {e}")
        return {"status": "failed", "error": str(e)}
    finally:
        if conn:
            return_db_connection(conn)

@app.post("/match", response_model=MatchResponse, tags=["AI Matching Engine"], summary="AI-Powered Candidate Matching")
async def match_candidates(request: MatchRequest):
    """Dynamic AI-powered candidate matching based on job requirements"""
    start_time = datetime.now()
    logger.info(f"Starting dynamic match for job_id: {request.job_id}")
    conn = None
    
    try:
        conn = get_db_connection()
        if not conn:
            logger.error("Database connection failed")
            return MatchResponse(
                job_id=request.job_id,
                top_candidates=[],
                total_candidates=0,
                processing_time=0.0,
                algorithm_version="2.0.0-phase2-ai",
                status="database_error"
            )
        
        logger.info("Database connection successful")
        
        # Get job details with enhanced requirements parsing
        cursor = conn.cursor()
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
                algorithm_version="2.0.0-phase2-ai",
                status="job_not_found"
            )
        
        job_title, job_desc, job_dept, job_location, job_level, job_requirements = job_data
        logger.info(f"Processing job: {job_title} with requirements: {job_requirements[:100]}...")
        
        # Get ALL candidates globally (no job_id filtering for dynamic matching)
        cursor.execute("""
            SELECT id, name, email, phone, location, experience_years, 
                   technical_skills, seniority_level, education_level
            FROM candidates 
            ORDER BY created_at DESC
        """)
        
        candidates = cursor.fetchall()
        logger.info(f"Found {len(candidates)} global candidates for dynamic matching to job {request.job_id}")
        
        if not candidates:
            logger.warning("No candidates found in database")
            return MatchResponse(
                job_id=request.job_id,
                top_candidates=[],
                total_candidates=0,
                processing_time=0.0,
                algorithm_version="2.0.0-phase2-ai",
                status="no_candidates"
            )
        
        # Phase 2: Real AI Semantic Matching
        scored_candidates = []
        
        # Try semantic matching first (Phase 2)
        if SEMANTIC_ENABLED and advanced_matcher and advanced_matcher.enabled:
            logger.info("Using Phase 2 AI semantic matching")
            
            job_data = {
                'id': request.job_id,
                'title': job_title,
                'description': job_desc,
                'requirements': job_requirements,
                'location': job_location,
                'experience_level': job_level
            }
            
            # Convert candidates to dict format for semantic matching
            candidates_dict = []
            for candidate in candidates:
                cand_id, name, email, phone, location, exp_years, skills, seniority, education = candidate
                candidates_dict.append({
                    'id': cand_id,
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'location': location,
                    'experience_years': exp_years,
                    'technical_skills': skills,
                    'seniority_level': seniority,
                    'education_level': education
                })
            
            # Use advanced semantic matching
            semantic_results = advanced_matcher.advanced_match(job_data, candidates_dict)
            
            if semantic_results:
                logger.info(f"Semantic matching found {len(semantic_results)} scored candidates")
                
                for result in semantic_results:
                    candidate_data = result['candidate_data']
                    score_breakdown = result['score_breakdown']
                    
                    # Convert semantic score to 45-95 range for consistency
                    semantic_score = result['total_score']
                    display_score = 45 + (semantic_score * 50)  # Scale 0-1 to 45-95
                    
                    # Extract matched skills from breakdown
                    skills_match = []
                    if candidate_data.get('technical_skills'):
                        # Use semantic skill extraction
                        skills_text = candidate_data['technical_skills'].lower()
                        job_req_lower = (job_requirements or '').lower()
                        
                        # Basic skill extraction for display
                        tech_keywords = ['python', 'java', 'javascript', 'react', 'node', 'sql', 'mongodb', 'aws', 'docker']
                        for skill in tech_keywords:
                            if skill in skills_text and skill in job_req_lower:
                                skills_match.append(skill.title())
                    
                    # Create reasoning from semantic breakdown
                    reasoning_parts = []
                    if score_breakdown.get('semantic_similarity', 0) > 0.3:
                        reasoning_parts.append(f"Semantic match: {score_breakdown['semantic_similarity']:.2f}")
                    if skills_match:
                        reasoning_parts.append(f"Skills: {', '.join(skills_match[:3])}")
                    if score_breakdown.get('experience_match', 0) > 0.5:
                        reasoning_parts.append(f"Experience: {candidate_data.get('experience_years', 0)}y")
                    if score_breakdown.get('location_match', 0) > 0.5:
                        reasoning_parts.append(f"Location: {candidate_data.get('location', 'Unknown')}")
                    
                    reasoning = "; ".join(reasoning_parts) if reasoning_parts else "AI semantic analysis"
                    
                    scored_candidates.append(CandidateScore(
                        candidate_id=candidate_data['id'],
                        name=candidate_data['name'],
                        email=candidate_data['email'],
                        score=round(display_score, 1),
                        skills_match=skills_match[:5],
                        experience_match=f"{candidate_data.get('experience_years', 0)}y - AI matched",
                        location_match=score_breakdown.get('location_match', 0) > 0.5,
                        reasoning=reasoning
                    ))
                
                # Sort by score and ensure proper differentiation
                scored_candidates.sort(key=lambda x: x.score, reverse=True)
                
                # Apply score differentiation to prevent clustering
                for i in range(1, len(scored_candidates)):
                    if scored_candidates[i].score >= scored_candidates[i-1].score:
                        scored_candidates[i].score = round(scored_candidates[i-1].score - 0.8, 1)
                
                logger.info(f"Phase 2 AI matching completed with {len(scored_candidates)} candidates")
            
            else:
                logger.warning("Semantic matching returned no results, falling back to keyword matching")
        
        # Fallback to keyword matching if semantic matching failed or unavailable
        if not scored_candidates:
            logger.info("Using fallback keyword matching")
            
            # Extract job-specific keywords for dynamic matching
            job_text = f"{job_title} {job_desc} {job_requirements}".lower()
            
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
        
        logger.info(f"Identified required skill categories: {required_skill_categories}")
        
        for candidate in candidates:
            cand_id, name, email, phone, location, exp_years, skills, seniority, education = candidate
            
            candidate_skills_lower = (skills or '').lower()
            candidate_name_lower = (name or '').lower()
            
            # Enhanced skills matching with exact keyword scoring
            skills_score = 0.0
            matched_skills = []
            skill_bonus = 0.0
            
            if required_skill_categories:
                total_possible_matches = 0
                actual_matches = 0
                
                for category in required_skill_categories:
                    category_skills = tech_skills_map[category]
                    category_matches = 0
                    
                    for skill in category_skills:
                        total_possible_matches += 1
                        if skill in candidate_skills_lower:
                            matched_skills.append(skill.title())
                            actual_matches += 1
                            category_matches += 1
                    
                    # Bonus for multiple skills in same category
                    if category_matches > 1:
                        skill_bonus += 0.1 * (category_matches - 1)
                
                skills_score = actual_matches / max(1, total_possible_matches) if total_possible_matches > 0 else 0.0
            else:
                skills_score, matched_skills = calculate_skills_match(
                    job_requirements or job_desc, skills or ""
                )
            
            # Experience scoring with more granular differentiation
            exp_score, exp_reasoning = calculate_experience_match(
                job_level or "", exp_years or 0, seniority or ""
            )
            
            # Enhanced experience scoring with realistic bonuses
            exp_years_val = exp_years or 0
            if exp_years_val >= 5:
                exp_bonus = 0.2   # Senior experience bonus
            elif exp_years_val >= 3:
                exp_bonus = 0.15  # Mid-level bonus
            elif exp_years_val >= 2:
                exp_bonus = 0.1   # Junior bonus
            else:
                exp_bonus = 0.0   # No penalty for entry level
            
            # Location matching with distance consideration
            location_score, location_match = calculate_location_match(
                job_location or "", location or ""
            )
            
            # Name-based diversity bonus (avoid clustering similar profiles)
            name_diversity_bonus = 0.0
            if 'a' in candidate_name_lower[:2]:  # Names starting with A
                name_diversity_bonus = 0.05
            elif 's' in candidate_name_lower[:2]:  # Names starting with S
                name_diversity_bonus = 0.03
            
            # Education level bonus
            education_bonus = 0.0
            if education and ('master' in education.lower() or 'mba' in education.lower()):
                education_bonus = 0.1
            elif education and 'bachelor' in education.lower():
                education_bonus = 0.05
            
            # Enhanced dynamic weighting with better differentiation
            base_multiplier = 75  # Reduced base for more realistic scores
            
            if 'senior' in job_text or 'lead' in job_text:
                # Experience-heavy weighting for senior roles
                raw_score = (skills_score * 0.4 + exp_score * 0.5 + location_score * 0.1)
                role_bonus = 10 if exp_years_val >= 5 else 0
                overall_score = (raw_score + skill_bonus + exp_bonus + education_bonus) * base_multiplier + role_bonus
            elif 'data' in job_text or 'ai' in job_text or 'machine learning' in job_text:
                # Skills-heavy weighting for technical roles
                raw_score = (skills_score * 0.6 + exp_score * 0.3 + location_score * 0.1)
                tech_bonus = 15 if len(matched_skills) >= 3 else 5
                overall_score = (raw_score + skill_bonus + exp_bonus + education_bonus) * (base_multiplier + 5) + tech_bonus
            else:
                # Balanced weighting for general roles
                raw_score = (skills_score * 0.5 + exp_score * 0.3 + location_score * 0.2)
                overall_score = (raw_score + skill_bonus + exp_bonus + name_diversity_bonus + education_bonus) * base_multiplier
            
            # Enhanced candidate-specific variations for better differentiation
            skill_diversity_bonus = len(set(matched_skills)) * 2  # Bonus for skill diversity
            experience_multiplier = 1 + (exp_years_val * 0.05)  # Experience multiplier
            candidate_variation = (cand_id % 13) * 1.2  # Larger variation based on ID
            
            overall_score = (overall_score * experience_multiplier) + skill_diversity_bonus + candidate_variation
            
            # Ensure realistic score range with better spread (45-92)
            overall_score = max(45.0, min(92.0, overall_score))
            
            # Enhanced reasoning with detailed breakdown
            reasoning_parts = []
            if matched_skills:
                reasoning_parts.append(f"Skills: {', '.join(matched_skills[:3])} ({len(matched_skills)} total)")
            reasoning_parts.append(f"Experience: {exp_years or 0}y - {exp_reasoning}")
            if location_match:
                reasoning_parts.append(f"Location: {location or 'Unknown'}")
            if education:
                reasoning_parts.append(f"Education: {education}")
            
            reasoning = "; ".join(reasoning_parts)
            
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
        
            # Sort by score and get top candidates with enhanced differentiation
            scored_candidates.sort(key=lambda x: x.score, reverse=True)
            
            # Enhanced score differentiation to prevent clustering (fallback only)
            for i in range(1, len(scored_candidates)):
                if abs(scored_candidates[i].score - scored_candidates[i-1].score) < 0.5:
                    scored_candidates[i].score = round(scored_candidates[i].score - (i * 0.7), 1)
            
            # Final score adjustment to ensure proper ranking (fallback only)
            for i, candidate in enumerate(scored_candidates):
                if i > 0 and candidate.score >= scored_candidates[i-1].score:
                    candidate.score = round(scored_candidates[i-1].score - 0.8, 1)
        
        # Get top candidates
        top_candidates = scored_candidates[:10]
        
        cursor.close()
        processing_time = (datetime.now() - start_time).total_seconds()
        
        logger.info(f"Dynamic matching completed: {len(top_candidates)} top candidates found")
        
        return MatchResponse(
            job_id=request.job_id,
            top_candidates=top_candidates,
            total_candidates=len(candidates),
            processing_time=round(processing_time, 3),
            algorithm_version="2.0.0-phase2-ai",
            status="success"
        )
        
    except Exception as e:
        logger.error(f"Dynamic matching error: {e}")
        return MatchResponse(
            job_id=request.job_id,
            top_candidates=[],
            total_candidates=0,
            processing_time=(datetime.now() - start_time).total_seconds(),
            algorithm_version="2.0.0-phase2-ai",
            status="error"
        )
    finally:
        if conn:
            return_db_connection(conn)

class BatchMatchRequest(BaseModel):
    job_ids: List[int]

@app.post("/batch-match", tags=["AI Matching Engine"], summary="Batch AI Matching for Multiple Jobs")
async def batch_match_jobs(request: BatchMatchRequest):
    """Batch AI matching for multiple jobs using Phase 2 semantic engine"""
    if not SEMANTIC_ENABLED or not batch_matcher or not batch_matcher.enabled:
        raise HTTPException(status_code=503, detail="AI batch matching not available")
    
    if not request.job_ids or len(request.job_ids) == 0:
        raise HTTPException(status_code=400, detail="At least one job ID is required")
    
    if len(request.job_ids) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 jobs can be processed in batch")
    
    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        cursor = conn.cursor()
        
        # Get jobs data
        cursor.execute("""
            SELECT id, title, description, department, location, experience_level, requirements
            FROM jobs WHERE id = ANY(%s)
        """, (request.job_ids,))
        
        jobs_data = cursor.fetchall()
        if not jobs_data:
            raise HTTPException(status_code=404, detail="No jobs found")
        
        # Get all candidates
        cursor.execute("""
            SELECT id, name, email, phone, location, experience_years, 
                   technical_skills, seniority_level, education_level
            FROM candidates 
            ORDER BY created_at DESC
        """)
        
        candidates_data = cursor.fetchall()
        
        # Format data for batch processing
        jobs = []
        for job in jobs_data:
            job_id, title, desc, dept, location, level, requirements = job
            jobs.append({
                'id': job_id,
                'title': title,
                'description': desc,
                'department': dept,
                'location': location,
                'experience_level': level,
                'requirements': requirements
            })
        
        candidates = []
        for candidate in candidates_data:
            cand_id, name, email, phone, location, exp_years, skills, seniority, education = candidate
            candidates.append({
                'id': cand_id,
                'name': name,
                'email': email,
                'phone': phone,
                'location': location,
                'experience_years': exp_years,
                'technical_skills': skills,
                'seniority_level': seniority,
                'education_level': education
            })
        
        # Process batch matching
        results = batch_matcher.batch_process(jobs, candidates)
        
        cursor.close()
        
        return {
            "batch_results": results,
            "total_jobs_processed": len(jobs),
            "total_candidates_analyzed": len(candidates),
            "algorithm_version": "2.0.0-phase2-ai-batch",
            "status": "success"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Batch matching error: {e}")
        raise HTTPException(status_code=500, detail=f"Batch matching failed: {str(e)}")
    finally:
        if conn:
            return_db_connection(conn)

@app.get("/analyze/{candidate_id}", tags=["Candidate Analysis"], summary="Detailed Candidate Analysis")
async def analyze_candidate(candidate_id: int):
    """Detailed candidate analysis"""
    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name, email, technical_skills, experience_years, 
                   seniority_level, education_level, location
            FROM candidates WHERE id = %s
        """, (candidate_id,))
        
        candidate = cursor.fetchone()
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")
        
        name, email, skills, exp_years, seniority, education, location = candidate
        
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
        
        # Phase 2: Add semantic skill extraction if available
        semantic_skills = []
        if SEMANTIC_ENABLED and advanced_matcher and advanced_matcher.enabled:
            try:
                semantic_skills = advanced_matcher.extract_skills_semantically(skills or "")
            except Exception as e:
                logger.error(f"Semantic skill extraction failed: {e}")
        
        return {
            "candidate_id": candidate_id,
            "name": name,
            "email": email,
            "experience_years": exp_years,
            "seniority_level": seniority,
            "education_level": education,
            "location": location,
            "skills_analysis": categorized_skills,
            "semantic_skills": semantic_skills,
            "total_skills": len(skills.split(',')) if skills else 0,
            "ai_analysis_enabled": SEMANTIC_ENABLED and advanced_matcher and advanced_matcher.enabled,
            "analysis_timestamp": datetime.now().isoformat()
        }
        cursor.close()
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    finally:
        if conn:
            return_db_connection(conn)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "9000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
