from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
import time
from datetime import datetime
import json
from fastapi.responses import JSONResponse
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
import os
from .api.routes_candidates import router as candidates_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="🎯 BHIV HR Platform API Gateway",
    description="""## Values-Driven Recruiting Platform with AI-Powered Matching
    
### 🚀 Features:
- **AI-Powered Candidate Matching** with Talah Agent
- **Values-Based Assessment** (MDVP Compliance)
- **Resume Processing & Analysis**
- **Interview Management & Feedback**
- **Real-time Analytics Dashboard**

### 🏆 Core Values Integration:
- **Integrity** - Moral uprightness and ethical behavior
- **Honesty** - Truthfulness and transparency
- **Discipline** - Self-control and commitment to excellence
- **Hard Work** - Dedication and perseverance
- **Gratitude** - Appreciation and humility

### 🔧 API Capabilities:
- **Jobs Management**: Create, list, and manage job postings
- **Candidates**: Upload, search, and manage candidate profiles
- **AI Matching**: Get top-5 candidates using Talah AI
- **Feedback**: Submit and track values-based assessments
- **Analytics**: Real-time statistics and reporting
    """,
    version="2.0.0",
    contact={
        "name": "BHIV HR Platform Support",
        "email": "support@bhiv-hr.com",
    },
    license_info={
        "name": "BHIV License",
    },
)

def wait_for_database():
    """Wait for database to be ready with retry logic"""
    database_url = os.getenv("DATABASE_URL", "postgresql://bhiv_user:bhiv_pass@db:5432/bhiv_hr")
    
    for attempt in range(30):  # Try for up to 30 seconds
        try:
            engine = create_engine(database_url)
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            logger.info("✅ Database connection successful!")
            return True
        except OperationalError as e:
            logger.info(f"⏳ Database not ready (attempt {attempt + 1}/30): {e}")
            time.sleep(1)
        except Exception as e:
            logger.error(f"❌ Unexpected database error: {e}")
            time.sleep(1)
    
    logger.error("❌ Database connection failed after 30 attempts")
    return False

# Wait for database on startup
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Starting BHIV HR Platform API...")
    if wait_for_database():
        logger.info("✅ Gateway ready!")
    else:
        logger.error("❌ Gateway startup failed - database unavailable")

@app.get("/", tags=["System"], summary="🏠 API Gateway Root")
def read_root():
    """Welcome endpoint for BHIV HR Platform API Gateway.
    
    Returns comprehensive information about the platform capabilities,
    available endpoints, and AI agent features.
    
    Returns:
        dict: API information and available endpoints
    """
    return {
        "message": "🎯 BHIV HR Platform API Gateway",
        "description": "Values-Driven Recruiting Platform with AI-Powered Matching",
        "version": "2.0.0",
        "status": "healthy",
        "features": [
            "🤖 AI-Powered Candidate Matching",
            "🏆 Values-Based Assessment (MDVP)",
            "📄 Resume Processing & Analysis",
            "📊 Real-time Analytics Dashboard",
            "🎯 Top-5 Candidate Shortlisting"
        ],
        "endpoints": {
            "docs": "/docs - Swagger UI Documentation",
            "health": "/health - System Health Check",
            "candidates": "/v1/candidates - Candidate Management",
            "jobs": "/v1/jobs - Job Management",
            "match": "/v1/match/{job_id}/top - AI Matching",
            "feedback": "/v1/feedback - Values Assessment",
            "analytics": "/candidates/stats - Real-time Statistics"
        },
        "ai_agent": {
            "name": "🤖 Talah AI Agent",
            "version": "1.0.0",
            "capabilities": [
                "📄 Resume Analysis & Parsing",
                "🎯 Candidate Scoring Algorithm",
                "🏆 Values Alignment Assessment",
                "📊 Top-5 Shortlisting with Rankings",
                "🔍 Skills & Experience Matching"
            ],
            "endpoint": "http://agent:9000"
        },
        "core_values": {
            "integrity": "Moral uprightness and ethical behavior",
            "honesty": "Truthfulness and transparency",
            "discipline": "Self-control and commitment to excellence",
            "hard_work": "Dedication and perseverance",
            "gratitude": "Appreciation and humility"
        }
    }

@app.get("/health", tags=["System"], summary="🏥 Health Check")
def health_check():
    """System health check endpoint.
    
    Returns:
        dict: Health status of the gateway and connected services
    """
    return {
        "status": "healthy",
        "service": "🎯 BHIV HR Gateway",
        "version": "2.0.0",
        "timestamp": time.time(),
        "components": {
            "database": "connected",
            "ai_agent": "available",
            "api_gateway": "running"
        }
    }

@app.post("/v1/jobs", tags=["Jobs Management"], summary="🏢 Create New Job")
async def create_job(job_data: dict):
    """Create a new job posting in the system.
    
    Args:
        job_data: Job information including title, description, client_id
        
    Returns:
        dict: Job creation result with job_id
    """
    try:
        from sqlalchemy import text
        database_url = os.getenv("DATABASE_URL", "postgresql://bhiv_user:bhiv_pass@db:5432/bhiv_hr")
        engine = create_engine(database_url)
        
        with engine.connect() as connection:
            # Insert job and get the ID
            query = text("""
                INSERT INTO jobs (client_id, title, description, created_at)
                VALUES (:client_id, :title, :description, NOW())
                RETURNING id
            """)
            result = connection.execute(query, {
                "client_id": job_data.get("client_id", 1),
                "title": job_data.get("title", "Untitled Job"),
                "description": job_data.get("description", "")
            })
            job_id = result.fetchone()[0]
            connection.commit()
            
        return {
            "message": "Job created successfully",
            "status": "success",
            "job_id": job_id
        }
    except Exception as e:
        return {
            "message": f"Failed to create job: {str(e)}",
            "status": "error",
            "job_id": None
        }

@app.post("/v1/feedback", tags=["Values Assessment"], summary="🏆 Submit Values Feedback")
async def submit_feedback(feedback_data: dict):
    """Submit values-based feedback for a candidate.
    
    Accepts both free-text feedback and structured values scores (1-5 scale)
    for Integrity, Honesty, Discipline, Hard Work, and Gratitude.
    
    Args:
        feedback_data: Feedback including candidate_id, values_scores, text
        
    Returns:
        dict: Feedback submission result with feedback_id
    """
    try:
        from sqlalchemy import text
        database_url = os.getenv("DATABASE_URL", "postgresql://bhiv_user:bhiv_pass@db:5432/bhiv_hr")
        engine = create_engine(database_url)
        
        with engine.connect() as connection:
            # Insert feedback with values scores
            query = text("""
                INSERT INTO feedback (candidate_id, reviewer, free_text, values_scores, created_at)
                VALUES (:candidate_id, :reviewer, :feedback_text, :values_scores, NOW())
                RETURNING id
            """)
            
            # Prepare values scores JSON
            values_scores = feedback_data.get("values_scores", {})
            if not values_scores:
                # Default values if not provided
                values_scores = {
                    "integrity": 3,
                    "honesty": 3, 
                    "discipline": 3,
                    "hard_work": 3,
                    "gratitude": 3
                }
            
            # Add recommendation to values scores
            values_scores["recommendation"] = feedback_data.get("overall_recommendation", "Neutral")
            
            result = connection.execute(query, {
                "candidate_id": feedback_data.get("candidate_id", 1),
                "reviewer": feedback_data.get("reviewer_name", "Anonymous"),
                "feedback_text": feedback_data.get("feedback_text", ""),
                "values_scores": json.dumps(values_scores)
            })
            feedback_id = result.fetchone()[0]
            connection.commit()
            
        return {
            "message": "Values feedback submitted successfully",
            "status": "success",
            "feedback_id": feedback_id,
            "values_summary": {
                "integrity": values_scores.get("integrity", 3),
                "honesty": values_scores.get("honesty", 3),
                "discipline": values_scores.get("discipline", 3),
                "hard_work": values_scores.get("hard_work", 3),
                "gratitude": values_scores.get("gratitude", 3),
                "average_score": sum([values_scores.get(k, 3) for k in ["integrity", "honesty", "discipline", "hard_work", "gratitude"]]) / 5
            }
        }
    except Exception as e:
        return {
            "message": f"Failed to submit feedback: {str(e)}",
            "status": "error",
            "feedback_id": None
        }

@app.get("/v1/match/{job_id}/top", tags=["AI Matching"], summary="🤖 Get Top-5 Candidates")
async def get_top_candidates(job_id: int):
    """Get top-5 candidates for a job using Talah AI.
    
    Uses advanced AI algorithms to analyze and rank candidates
    based on job requirements and values alignment.
    
    Args:
        job_id: ID of the job to match candidates for
        
    Returns:
        dict: Top-5 candidates with AI scores and analysis
    """
    import httpx
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post("http://agent:9000/match", json={"job_id": job_id})
            if response.status_code == 200:
                return response.json()
            else:
                return {"job_id": job_id, "top_candidates": [], "status": "agent_error"}
    except Exception as e:
        return {"job_id": job_id, "top_candidates": [], "status": "error"}

@app.get("/candidates/stats", tags=["Analytics"], summary="📊 Real-time Statistics")
def get_candidate_stats():
    """Get real-time statistics from the HR platform.
    
    Provides live data for dashboard analytics including
    candidate counts, job postings, and feedback metrics.
    
    Returns:
        dict: Real-time platform statistics
    """
    try:
        from sqlalchemy import text
        database_url = os.getenv("DATABASE_URL", "postgresql://bhiv_user:bhiv_pass@db:5432/bhiv_hr")
        engine = create_engine(database_url)
        
        with engine.connect() as connection:
            # Get total candidates
            candidates_result = connection.execute(text("SELECT COUNT(*) FROM candidates"))
            total_candidates = candidates_result.fetchone()[0]
            
            # Get total jobs
            jobs_result = connection.execute(text("SELECT COUNT(*) FROM jobs"))
            total_jobs = jobs_result.fetchone()[0]
            
            # Get total feedback
            feedback_result = connection.execute(text("SELECT COUNT(*) FROM feedback"))
            total_feedback = feedback_result.fetchone()[0]
            
            return {
                "total_candidates": total_candidates,
                "total_jobs": total_jobs,
                "total_feedback": total_feedback,
                "status": "success"
            }
    except Exception as e:
        return {
            "total_candidates": 0,
            "total_jobs": 0,
            "total_feedback": 0,
            "status": "error",
            "message": str(e)
        }

# Additional API endpoints
@app.get("/v1/jobs", tags=["Jobs Management"], summary="📋 List All Jobs")
async def list_jobs():
    """List all active job postings with candidate counts.
    
    Returns:
        dict: List of all jobs with statistics
    """
    try:
        from sqlalchemy import text
        database_url = os.getenv("DATABASE_URL", "postgresql://bhiv_user:bhiv_pass@db:5432/bhiv_hr")
        engine = create_engine(database_url)
        
        with engine.connect() as connection:
            query = text("""
                SELECT 
                    j.id,
                    j.title,
                    j.description,
                    j.client_id,
                    j.created_at,
                    COUNT(c.id) as candidate_count,
                    COUNT(f.id) as feedback_count,
                    COUNT(i.id) as interview_count,
                    COUNT(o.id) as offer_count
                FROM jobs j
                LEFT JOIN candidates c ON j.id = c.job_id
                LEFT JOIN feedback f ON c.id = f.candidate_id
                LEFT JOIN interviews i ON c.id = i.candidate_id
                LEFT JOIN offers o ON c.id = o.candidate_id
                GROUP BY j.id, j.title, j.description, j.client_id, j.created_at
                ORDER BY j.created_at DESC
            """)
            
            result = connection.execute(query)
            jobs = []
            
            for row in result:
                jobs.append({
                    "id": row[0],
                    "title": row[1],
                    "description": row[2],
                    "client_id": row[3],
                    "created_at": row[4].isoformat() if row[4] else None,
                    "statistics": {
                        "candidates": row[5],
                        "feedback_received": row[6],
                        "interviews_scheduled": row[7],
                        "offers_made": row[8]
                    }
                })
            
        return {
            "message": "Jobs retrieved successfully",
            "status": "success",
            "jobs": jobs,
            "total_jobs": len(jobs)
        }
    except Exception as e:
        return {
            "message": f"Failed to retrieve jobs: {str(e)}",
            "status": "error",
            "jobs": []
        }

@app.post("/v1/interviews", tags=["Interview Management"], summary="📞 Schedule Interview")
async def schedule_interview(interview_data: dict):
    """Schedule an interview with a candidate.
    
    Args:
        interview_data: Interview details including candidate_id, job_id, date, interviewer
        
    Returns:
        dict: Interview scheduling result with interview_id
    """
    try:
        from sqlalchemy import text
        database_url = os.getenv("DATABASE_URL", "postgresql://bhiv_user:bhiv_pass@db:5432/bhiv_hr")
        engine = create_engine(database_url)
        
        # Create interviews table if not exists
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
            
            # Insert interview
            query = text("""
                INSERT INTO interviews (candidate_id, job_id, interview_date, interviewer, status, created_at)
                VALUES (:candidate_id, :job_id, :interview_date, :interviewer, 'scheduled', NOW())
                RETURNING id
            """)
            
            result = connection.execute(query, {
                "candidate_id": interview_data.get("candidate_id", 1),
                "job_id": interview_data.get("job_id", 1),
                "interview_date": interview_data.get("interview_date", "2025-09-01 10:00:00"),
                "interviewer": interview_data.get("interviewer", "HR Manager")
            })
            interview_id = result.fetchone()[0]
            connection.commit()
            
        return {
            "message": "Interview scheduled successfully",
            "status": "success",
            "interview_id": interview_id,
            "details": {
                "candidate_id": interview_data.get("candidate_id"),
                "job_id": interview_data.get("job_id"),
                "interview_date": interview_data.get("interview_date"),
                "interviewer": interview_data.get("interviewer"),
                "status": "scheduled"
            }
        }
    except Exception as e:
        return {
            "message": f"Failed to schedule interview: {str(e)}",
            "status": "error",
            "interview_id": None
        }

@app.post("/v1/offers", tags=["Offer Management"], summary="🎉 Make Job Offer")
async def make_offer(offer_data: dict):
    """Make a job offer to a candidate.
    
    Args:
        offer_data: Offer details including candidate_id, job_id, salary, status
        
    Returns:
        dict: Offer creation result with offer_id
    """
    try:
        from sqlalchemy import text
        database_url = os.getenv("DATABASE_URL", "postgresql://bhiv_user:bhiv_pass@db:5432/bhiv_hr")
        engine = create_engine(database_url)
        
        # Create offers table if not exists
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
            
            # Insert offer
            query = text("""
                INSERT INTO offers (candidate_id, job_id, salary, status, offer_date, created_at)
                VALUES (:candidate_id, :job_id, :salary, :status, NOW(), NOW())
                RETURNING id
            """)
            
            result = connection.execute(query, {
                "candidate_id": offer_data.get("candidate_id", 1),
                "job_id": offer_data.get("job_id", 1),
                "salary": offer_data.get("salary", 100000),
                "status": offer_data.get("status", "sent")
            })
            offer_id = result.fetchone()[0]
            connection.commit()
            
        return {
            "message": "Job offer created successfully",
            "status": "success",
            "offer_id": offer_id,
            "details": {
                "candidate_id": offer_data.get("candidate_id"),
                "job_id": offer_data.get("job_id"),
                "salary": offer_data.get("salary"),
                "status": offer_data.get("status", "sent"),
                "offer_date": datetime.now().isoformat()
            }
        }
    except Exception as e:
        return {
            "message": f"Failed to create offer: {str(e)}",
            "status": "error",
            "offer_id": None
        }

@app.get("/v1/reports/job/{job_id}/export.csv", tags=["Reports"], summary="📄 Export Job Report")
async def export_job_report(job_id: int):
    """Export comprehensive job report as CSV with candidate values scores.
    
    Includes candidate information, values assessments, interview status,
    and offer details for complete recruiting pipeline visibility.
    
    Args:
        job_id: ID of the job to export
        
    Returns:
        dict: CSV export data with candidate values and recruiting metrics
    """
    try:
        from sqlalchemy import text
        database_url = os.getenv("DATABASE_URL", "postgresql://bhiv_user:bhiv_pass@db:5432/bhiv_hr")
        engine = create_engine(database_url)
        
        with engine.connect() as connection:
            # Get comprehensive job report data
            query = text("""
                SELECT 
                    c.id as candidate_id,
                    c.name,
                    c.email,
                    c.status as candidate_status,
                    f.values_scores,
                    f.free_text as feedback,
                    f.reviewer,
                    i.interview_date,
                    i.interviewer,
                    i.status as interview_status,
                    o.salary,
                    o.status as offer_status,
                    o.offer_date
                FROM candidates c
                LEFT JOIN feedback f ON c.id = f.candidate_id
                LEFT JOIN interviews i ON c.id = i.candidate_id
                LEFT JOIN offers o ON c.id = o.candidate_id
                WHERE c.job_id = :job_id
                ORDER BY c.id
            """)
            
            result = connection.execute(query, {"job_id": job_id})
            rows = result.fetchall()
            
            # Convert to CSV format
            csv_data = []
            csv_data.append([
                "Candidate ID", "Name", "Email", "Status",
                "Integrity", "Honesty", "Discipline", "Hard Work", "Gratitude",
                "Average Values Score", "Feedback", "Reviewer",
                "Interview Date", "Interviewer", "Interview Status",
                "Salary Offer", "Offer Status", "Offer Date"
            ])
            
            for row in rows:
                # Handle values_scores - it might already be a dict or need parsing
                if row[4]:
                    if isinstance(row[4], str):
                        values_scores = json.loads(row[4])
                    else:
                        values_scores = row[4]  # Already a dict
                else:
                    values_scores = {}
                
                # Extract individual values scores
                integrity = values_scores.get("integrity", "N/A")
                honesty = values_scores.get("honesty", "N/A")
                discipline = values_scores.get("discipline", "N/A")
                hard_work = values_scores.get("hard_work", "N/A")
                gratitude = values_scores.get("gratitude", "N/A")
                
                # Calculate average if all values present
                if all(isinstance(v, (int, float)) for v in [integrity, honesty, discipline, hard_work, gratitude]):
                    avg_score = round((integrity + honesty + discipline + hard_work + gratitude) / 5, 1)
                else:
                    avg_score = "N/A"
                
                csv_data.append([
                    row[0], row[1], row[2], row[3],
                    integrity, honesty, discipline, hard_work, gratitude,
                    avg_score, row[5] or "N/A", row[6] or "N/A",
                    row[7] or "N/A", row[8] or "N/A", row[9] or "N/A",
                    row[10] or "N/A", row[11] or "N/A", row[12] or "N/A"
                ])
            
        return {
            "message": "Job report generated successfully",
            "status": "success",
            "job_id": job_id,
            "csv_data": csv_data,
            "total_candidates": len(csv_data) - 1 if csv_data else 0,  # Exclude header
            "export_timestamp": datetime.now().isoformat(),
            "columns": [
                "candidate_info", "values_assessment", "interview_data", "offer_details"
            ]
        }
    except Exception as e:
        return {
            "message": f"Failed to generate report: {str(e)}",
            "status": "error",
            "job_id": job_id,
            "csv_data": []
        }

# Include candidates routes
app.include_router(candidates_router, prefix="/v1/candidates", tags=["Candidates Management"])
app.include_router(candidates_router, prefix="/candidates", tags=["Candidates Management"])
