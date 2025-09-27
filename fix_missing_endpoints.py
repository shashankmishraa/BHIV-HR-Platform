#!/usr/bin/env python3
"""
Fix Missing API Endpoints
Add interviews and feedback endpoints
"""

import requests
from datetime import datetime

def check_missing_endpoints():
    """Check which endpoints are missing"""
    api_base = "https://bhiv-hr-gateway-46pz.onrender.com"
    headers = {"Authorization": "Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"}
    
    endpoints_to_check = [
        "/v1/interviews",
        "/v1/feedback", 
        "/docs"
    ]
    
    print("Checking API Endpoints")
    print("=" * 40)
    
    for endpoint in endpoints_to_check:
        try:
            response = requests.get(f"{api_base}{endpoint}", headers=headers, timeout=10)
            status = "EXISTS" if response.status_code in [200, 405] else "MISSING"
            print(f"{status}: {endpoint} - Status: {response.status_code}")
        except Exception as e:
            print(f"ERROR: {endpoint} - {str(e)}")

def test_database_persistence():
    """Test if job creation actually persists to database"""
    api_base = "https://bhiv-hr-gateway-46pz.onrender.com"
    headers = {"Authorization": "Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"}
    
    print("\nTesting Database Persistence")
    print("=" * 40)
    
    # Create a job
    test_job = {
        "title": "Database Test Job",
        "department": "Testing",
        "location": "Remote", 
        "experience_level": "Mid-level",
        "requirements": "Database testing",
        "description": "Test job for database persistence",
        "salary_min": 80000,
        "salary_max": 120000,
        "client_id": 1,
        "employment_type": "Full-time",
        "status": "active"
    }
    
    try:
        # Create job
        create_response = requests.post(f"{api_base}/v1/jobs", json=test_job, headers=headers, timeout=10)
        print(f"Job Creation: {create_response.status_code}")
        
        if create_response.status_code == 200:
            result = create_response.json()
            job_id = result.get('job_id')
            print(f"Created Job ID: {job_id}")
            
            # Try to retrieve the job
            get_response = requests.get(f"{api_base}/v1/jobs/{job_id}", headers=headers, timeout=10)
            print(f"Job Retrieval: {get_response.status_code}")
            
            # List all jobs
            list_response = requests.get(f"{api_base}/v1/jobs", headers=headers, timeout=10)
            print(f"Jobs List: {list_response.status_code}")
            
            if list_response.status_code == 200:
                jobs_data = list_response.json()
                jobs = jobs_data.get('jobs', [])
                print(f"Total Jobs in API: {len(jobs)}")
                
                # Check if our job is in the list
                our_job = next((j for j in jobs if j.get('title') == test_job['title']), None)
                if our_job:
                    print("SUCCESS: Job found in API response")
                else:
                    print("ISSUE: Job not found in API response")
        
    except Exception as e:
        print(f"Database test error: {e}")

def test_direct_database_connection():
    """Test direct database connection"""
    print("\nTesting Direct Database Connection")
    print("=" * 40)
    
    try:
        import psycopg2
        database_url = "postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu"
        
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Check jobs table
        cursor.execute("SELECT COUNT(*) FROM jobs")
        jobs_count = cursor.fetchone()[0]
        print(f"Jobs in Database: {jobs_count}")
        
        # Check candidates table
        cursor.execute("SELECT COUNT(*) FROM candidates")
        candidates_count = cursor.fetchone()[0]
        print(f"Candidates in Database: {candidates_count}")
        
        # Check recent jobs
        cursor.execute("SELECT id, title, created_at FROM jobs ORDER BY created_at DESC LIMIT 5")
        recent_jobs = cursor.fetchall()
        print(f"Recent Jobs: {len(recent_jobs)}")
        for job in recent_jobs:
            print(f"  ID: {job[0]}, Title: {job[1]}, Created: {job[2]}")
        
        cursor.close()
        conn.close()
        
        print("SUCCESS: Direct database connection working")
        
    except Exception as e:
        print(f"Database connection error: {e}")

def create_missing_endpoints_fix():
    """Create fix for missing endpoints"""
    
    interviews_router = '''
"""Interviews router - Missing endpoint fix"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

router = APIRouter(prefix="/v1/interviews", tags=["Interviews"])

class InterviewCreate(BaseModel):
    candidate_id: int
    job_id: int
    interview_date: str
    interviewer: str = "HR Team"
    notes: Optional[str] = None

@router.post("")
async def create_interview(interview: InterviewCreate):
    """Create new interview"""
    from app.shared.database import db_manager
    
    try:
        async with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO interviews (candidate_id, job_id, interview_date, interviewer, notes)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            """, (interview.candidate_id, interview.job_id, interview.interview_date, 
                  interview.interviewer, interview.notes))
            
            interview_id = cursor.fetchone()[0]
            conn.commit()
            
            return {
                "id": interview_id,
                "message": "Interview scheduled successfully",
                "interview_date": interview.interview_date,
                "interviewer": interview.interviewer
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("")
async def list_interviews():
    """List all interviews"""
    from app.shared.database import db_manager
    
    try:
        async with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT i.id, i.candidate_id, i.job_id, i.interview_date, 
                       i.interviewer, i.status, i.notes,
                       c.name as candidate_name, j.title as job_title
                FROM interviews i
                LEFT JOIN candidates c ON i.candidate_id = c.id
                LEFT JOIN jobs j ON i.job_id = j.id
                ORDER BY i.interview_date DESC
            """)
            
            interviews = []
            for row in cursor.fetchall():
                interviews.append({
                    "id": row[0],
                    "candidate_id": row[1],
                    "job_id": row[2],
                    "interview_date": row[3].isoformat() if row[3] else None,
                    "interviewer": row[4],
                    "status": row[5],
                    "notes": row[6],
                    "candidate_name": row[7],
                    "job_title": row[8]
                })
            
            return {"interviews": interviews, "total": len(interviews)}
    except Exception as e:
        return {"interviews": [], "total": 0, "error": str(e)}
'''
    
    feedback_router = '''
"""Feedback router - Missing endpoint fix"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/v1/feedback", tags=["Feedback"])

class FeedbackCreate(BaseModel):
    candidate_id: int
    job_id: int
    integrity: int
    honesty: int
    discipline: int
    hard_work: int
    gratitude: int
    comments: Optional[str] = None

@router.post("")
async def create_feedback(feedback: FeedbackCreate):
    """Submit values assessment feedback"""
    from app.shared.database import db_manager
    
    try:
        async with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO feedback (candidate_id, job_id, integrity, honesty, 
                                    discipline, hard_work, gratitude, comments)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (feedback.candidate_id, feedback.job_id, feedback.integrity,
                  feedback.honesty, feedback.discipline, feedback.hard_work,
                  feedback.gratitude, feedback.comments))
            
            feedback_id = cursor.fetchone()[0]
            conn.commit()
            
            # Calculate average score
            avg_score = (feedback.integrity + feedback.honesty + feedback.discipline + 
                        feedback.hard_work + feedback.gratitude) / 5
            
            return {
                "id": feedback_id,
                "message": "Values assessment submitted successfully",
                "average_score": round(avg_score, 2),
                "values": {
                    "integrity": feedback.integrity,
                    "honesty": feedback.honesty,
                    "discipline": feedback.discipline,
                    "hard_work": feedback.hard_work,
                    "gratitude": feedback.gratitude
                }
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("")
async def list_feedback():
    """List all feedback"""
    from app.shared.database import db_manager
    
    try:
        async with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT f.id, f.candidate_id, f.job_id, f.integrity, f.honesty,
                       f.discipline, f.hard_work, f.gratitude, f.comments,
                       c.name as candidate_name, j.title as job_title
                FROM feedback f
                LEFT JOIN candidates c ON f.candidate_id = c.id
                LEFT JOIN jobs j ON f.job_id = j.id
                ORDER BY f.created_at DESC
            """)
            
            feedback_list = []
            for row in cursor.fetchall():
                avg_score = (row[3] + row[4] + row[5] + row[6] + row[7]) / 5
                feedback_list.append({
                    "id": row[0],
                    "candidate_id": row[1],
                    "job_id": row[2],
                    "values": {
                        "integrity": row[3],
                        "honesty": row[4],
                        "discipline": row[5],
                        "hard_work": row[6],
                        "gratitude": row[7]
                    },
                    "average_score": round(avg_score, 2),
                    "comments": row[8],
                    "candidate_name": row[9],
                    "job_title": row[10]
                })
            
            return {"feedback": feedback_list, "total": len(feedback_list)}
    except Exception as e:
        return {"feedback": [], "total": 0, "error": str(e)}
'''
    
    print("Missing Endpoints Fix Code Generated")
    print("=" * 40)
    print("Interviews Router:")
    print(interviews_router[:200] + "...")
    print("\nFeedback Router:")
    print(feedback_router[:200] + "...")
    
    return True

def run_endpoint_diagnostics():
    """Run comprehensive endpoint diagnostics"""
    print("ENDPOINT DIAGNOSTICS")
    print(f"Timestamp: {datetime.now()}")
    print("=" * 50)
    
    check_missing_endpoints()
    test_database_persistence()
    test_direct_database_connection()
    create_missing_endpoints_fix()
    
    print("\nDIAGNOSTICS COMPLETE")
    print("Next steps:")
    print("1. Add missing interview and feedback routers to gateway")
    print("2. Fix database persistence in job/candidate creation")
    print("3. Re-run end-to-end verification")

if __name__ == "__main__":
    run_endpoint_diagnostics()