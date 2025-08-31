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
    print("⚠️ Semantic matching not available, using fallback")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="BHIV AI Agent - Day 2 Enhanced",
    description="Advanced AI-powered candidate matching with detailed semantic analysis",
    version="2.1.0"
)

# Initialize semantic matchers
semantic_matcher = None
advanced_matcher = None
if SEMANTIC_ENABLED:
    try:
        semantic_matcher = SemanticJobMatcher()
        advanced_matcher = AdvancedSemanticMatcher()
        print("✅ Advanced semantic matching enabled")
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
    """Calculate skills matching score"""
    if not job_requirements or not candidate_skills:
        return 0.0, []
    
    # Extract key skills from job requirements
    job_skills = set()
    tech_keywords = ['python', 'java', 'javascript', 'react', 'node', 'sql', 'aws', 'docker', 
                    'kubernetes', 'machine learning', 'ai', 'data science', 'pandas', 'numpy',
                    'tensorflow', 'pytorch', 'git', 'linux', 'mongodb', 'postgresql']
    
    job_req_lower = job_requirements.lower()
    candidate_skills_lower = candidate_skills.lower()
    
    for skill in tech_keywords:
        if skill in job_req_lower:
            job_skills.add(skill)
    
    # Find matching skills
    matched_skills = []
    for skill in job_skills:
        if skill in candidate_skills_lower:
            matched_skills.append(skill.title())
    
    # Calculate score
    if not job_skills:
        return 0.5, matched_skills  # Neutral score if no specific skills required
    
    score = len(matched_skills) / len(job_skills)
    return min(score, 1.0), matched_skills

def calculate_experience_match(job_level: str, candidate_years: int, candidate_level: str) -> tuple:
    """Calculate experience matching score"""
    if not job_level:
        return 0.5, "No specific level required"
    
    job_level_lower = job_level.lower()
    candidate_level_lower = (candidate_level or "").lower()
    
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
    
    job_loc_lower = job_location.lower()
    candidate_loc_lower = candidate_location.lower()
    
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

@app.get("/")
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

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Talah AI Agent",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/match", response_model=MatchResponse)
async def match_candidates(request: MatchRequest):
    """Advanced AI-powered candidate matching"""
    start_time = datetime.now()
    
    try:
        conn = get_db_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        cursor = conn.cursor()
        
        # Get job details
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
                algorithm_version="1.0.0",
                status="job_not_found"
            )
        
        job_title, job_desc, job_dept, job_location, job_level, job_requirements = job_data
        
        # Get all candidates for this job
        cursor.execute("""
            SELECT id, name, email, phone, location, experience_years, 
                   technical_skills, seniority_level, education_level
            FROM candidates 
            WHERE job_id = %s AND status = 'applied'
            ORDER BY created_at DESC
        """, (request.job_id,))
        
        candidates = cursor.fetchall()
        
        if not candidates:
            return MatchResponse(
                job_id=request.job_id,
                top_candidates=[],
                total_candidates=0,
                processing_time=0.0,
                algorithm_version="1.0.0",
                status="no_candidates"
            )
        
        # Score each candidate using advanced semantic matching
        scored_candidates = []
        
        # Prepare job data for semantic matching
        job_data = {
            'title': job_title,
            'description': job_desc,
            'required_skills': job_requirements,
            'experience_required': job_level,
            'location': job_location
        }
        
        for candidate in candidates:
            cand_id, name, email, phone, location, exp_years, skills, seniority, education = candidate
            
            # Prepare candidate data
            candidate_data = {
                'name': name,
                'email': email,
                'skills': skills or '',
                'experience': str(exp_years) if exp_years else 'Fresher',
                'designation': seniority or '',
                'location': location or ''
            }
            
            # Use advanced semantic matching if available
            if SEMANTIC_ENABLED and advanced_matcher:
                try:
                    match_result = advanced_matcher.calculate_detailed_match(candidate_data, job_data)
                    overall_score = match_result['total_score'] * 100
                    
                    # Extract detailed information
                    skills_breakdown = match_result['breakdown']['skills']['details']
                    matched_skills = skills_breakdown.get('matched', [])
                    exp_reasoning = match_result['breakdown']['experience']['details'].get('status', 'Unknown')
                    location_match = match_result['breakdown']['location']['details'].get('status') != 'Different location'
                    
                    reasoning = f"{match_result['recommendation']}; {'; '.join(match_result['strengths'])}"
                    
                except Exception as e:
                    logger.warning(f"Semantic matching failed for candidate {cand_id}: {e}")
                    # Fallback to basic matching
                    skills_score, matched_skills = calculate_skills_match(
                        job_requirements or job_desc, skills or ""
                    )
                    exp_score, exp_reasoning = calculate_experience_match(
                        job_level or "", exp_years or 0, seniority or ""
                    )
                    location_score, location_match = calculate_location_match(
                        job_location or "", location or ""
                    )
                    overall_score = (skills_score * 0.5 + exp_score * 0.3 + location_score * 0.2) * 100
                    reasoning = f"Skills: {', '.join(matched_skills)}; Experience: {exp_reasoning}"
            else:
                # Basic matching fallback
                skills_score, matched_skills = calculate_skills_match(
                    job_requirements or job_desc, skills or ""
                )
                exp_score, exp_reasoning = calculate_experience_match(
                    job_level or "", exp_years or 0, seniority or ""
                )
                location_score, location_match = calculate_location_match(
                    job_location or "", location or ""
                )
                overall_score = (skills_score * 0.5 + exp_score * 0.3 + location_score * 0.2) * 100
                reasoning = f"Skills: {', '.join(matched_skills)}; Experience: {exp_reasoning}"
            
            scored_candidates.append(CandidateScore(
                candidate_id=cand_id,
                name=name,
                email=email,
                score=round(overall_score, 1),
                skills_match=matched_skills,
                experience_match=exp_reasoning,
                location_match=location_match,
                reasoning=reasoning
            ))
        
        # Sort by score and get top 5
        scored_candidates.sort(key=lambda x: x.score, reverse=True)
        top_5 = scored_candidates[:5]
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        conn.close()
        
        return MatchResponse(
            job_id=request.job_id,
            top_candidates=top_5,
            total_candidates=len(candidates),
            processing_time=round(processing_time, 3),
            algorithm_version="2.0.0-semantic" if SEMANTIC_ENABLED else "1.0.0-basic",
            status="success"
        )
        
    except Exception as e:
        logger.error(f"Matching error: {e}")
        raise HTTPException(status_code=500, detail=f"Matching failed: {str(e)}")

@app.get("/analyze/{candidate_id}")
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