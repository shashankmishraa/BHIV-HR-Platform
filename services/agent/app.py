from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import os
import json
from typing import List, Dict, Any
import logging
from datetime import datetime
import sys

# Add semantic engine to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

try:
    from services.semantic_engine.job_matcher import SemanticJobMatcher
    from services.semantic_engine.advanced_matcher import AdvancedSemanticMatcher, BatchMatcher
    SEMANTIC_ENABLED = True
except ImportError:
    SEMANTIC_ENABLED = False
    print("WARNING: Semantic matching not available, using fallback")

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

# Initialize semantic matchers
semantic_matcher = None
advanced_matcher = None
if SEMANTIC_ENABLED:
    try:
        semantic_matcher = SemanticJobMatcher()
        advanced_matcher = AdvancedSemanticMatcher()
        print("SUCCESS: Advanced semantic matching enabled")
    except Exception as e:
        print(f"Failed to initialize semantic matcher: {e}")
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

def get_db_connection():
    """Get database connection"""
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "db"),
            database=os.getenv("DB_NAME", "bhiv_hr"),
            user=os.getenv("DB_USER", "bhiv_user"),
            password=os.getenv("DB_PASSWORD", "bhiv_pass"),
            port=os.getenv("DB_PORT", "5432")
        )
        return conn
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return None

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
        "service": "Talah AI Agent",
        "version": "1.0.0",
        "endpoints": {
            "match": "POST /match - Get top candidates for job",
            "analyze": "GET /analyze/{candidate_id} - Analyze candidate",
            "health": "GET /health - Service health check"
        }
    }

@app.get("/health", tags=["Core API Endpoints"], summary="Health Check")
def health_check():
    return {
        "status": "healthy",
        "service": "Talah AI Agent",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/test-db", tags=["System Diagnostics"], summary="Database Connectivity Test")
def test_database():
    try:
        conn = get_db_connection()
        if not conn:
            return {"error": "Connection failed"}
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM candidates")
        count = cursor.fetchone()[0]
        cursor.execute("SELECT id, name FROM candidates LIMIT 3")
        samples = cursor.fetchall()
        conn.close()
        return {"candidates_count": count, "samples": samples}
    except Exception as e:
        return {"error": str(e)}

@app.post("/match", response_model=MatchResponse, tags=["AI Matching Engine"], summary="AI-Powered Candidate Matching")
async def match_candidates(request: MatchRequest):
    """Dynamic AI-powered candidate matching based on job requirements"""
    start_time = datetime.now()
    logger.info(f"Starting dynamic match for job_id: {request.job_id}")
    
    try:
        conn = get_db_connection()
        if not conn:
            logger.error("Database connection failed")
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        cursor = conn.cursor()
        logger.info("Database connection successful")
        
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
                algorithm_version="2.0.0-dynamic",
                status="no_candidates"
            )
        
        # Dynamic scoring based on job-specific requirements
        scored_candidates = []
        
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
            
            # Dynamic skills matching based on job requirements
            skills_score = 0.0
            matched_skills = []
            
            if required_skill_categories:
                category_matches = 0
                for category in required_skill_categories:
                    category_skills = tech_skills_map[category]
                    category_match = False
                    for skill in category_skills:
                        if skill in candidate_skills_lower:
                            matched_skills.append(skill.title())
                            category_match = True
                    if category_match:
                        category_matches += 1
                
                skills_score = category_matches / len(required_skill_categories)
            else:
                # Fallback to general skill matching
                skills_score, matched_skills = calculate_skills_match(
                    job_requirements or job_desc, skills or ""
                )
            
            # Dynamic experience matching
            exp_score, exp_reasoning = calculate_experience_match(
                job_level or "", exp_years or 0, seniority or ""
            )
            
            # Location matching
            location_score, location_match = calculate_location_match(
                job_location or "", location or ""
            )
            
            # Dynamic weighting based on job type
            if 'senior' in job_text or 'lead' in job_text:
                # Experience-heavy weighting for senior roles
                overall_score = (skills_score * 0.4 + exp_score * 0.5 + location_score * 0.1) * 100
            elif 'data' in job_text or 'ai' in job_text or 'machine learning' in job_text:
                # Skills-heavy weighting for technical roles
                overall_score = (skills_score * 0.6 + exp_score * 0.3 + location_score * 0.1) * 100
            else:
                # Balanced weighting for general roles
                overall_score = (skills_score * 0.5 + exp_score * 0.3 + location_score * 0.2) * 100
            
            # Enhanced reasoning with job-specific context
            reasoning_parts = []
            if matched_skills:
                reasoning_parts.append(f"Skills match: {', '.join(matched_skills[:3])}")
            reasoning_parts.append(f"Experience: {exp_reasoning}")
            if location_match:
                reasoning_parts.append("Location compatible")
            
            reasoning = "; ".join(reasoning_parts)
            
            scored_candidates.append(CandidateScore(
                candidate_id=cand_id,
                name=name,
                email=email,
                score=round(overall_score, 1),
                skills_match=matched_skills[:5],  # Top 5 matched skills
                experience_match=exp_reasoning,
                location_match=location_match,
                reasoning=reasoning
            ))
        
        # Sort by score and get top candidates
        scored_candidates.sort(key=lambda x: x.score, reverse=True)
        top_candidates = scored_candidates[:10]  # Return top 10 for better selection
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        conn.close()
        
        logger.info(f"Dynamic matching completed: {len(top_candidates)} top candidates found")
        
        return MatchResponse(
            job_id=request.job_id,
            top_candidates=top_candidates,
            total_candidates=len(candidates),
            processing_time=round(processing_time, 3),
            algorithm_version="2.0.0-dynamic",
            status="success"
        )
        
    except Exception as e:
        logger.error(f"Dynamic matching error: {e}")
        raise HTTPException(status_code=500, detail=f"Dynamic matching failed: {str(e)}")

@app.get("/analyze/{candidate_id}", tags=["Candidate Analysis"], summary="Detailed Candidate Analysis")
async def analyze_candidate(candidate_id: int):
    """Detailed candidate analysis"""
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
        
        conn.close()
        
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
            "analysis_timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)