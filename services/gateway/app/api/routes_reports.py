from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy import create_engine, text
import pandas as pd
import io
import os
from datetime import datetime, timezone
from typing import Optional

router = APIRouter()

def get_db_engine():
    database_url = os.getenv("DATABASE_URL", "postgresql://bhiv_user:bhiv_pass@db:5432/bhiv_hr")
    return create_engine(database_url, pool_pre_ping=True, pool_recycle=300)

@router.get("/job/{job_id}/export.csv")
async def export_job_report(job_id: int):
    """Export comprehensive job report with candidate values scores"""
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            # Get job details
            job_query = text("""
                SELECT title, description, department, location, experience_level, 
                       employment_type, requirements, status, created_at
                FROM jobs WHERE id = :job_id
            """)
            job_result = connection.execute(job_query, {"job_id": job_id})
            job_data = job_result.fetchone()
            
            if not job_data:
                raise HTTPException(status_code=404, detail="Job not found")
            
            # Get candidates with feedback and values
            candidates_query = text("""
                SELECT 
                    c.id, c.name, c.email, c.phone, c.location, c.experience_years,
                    c.education_level, c.technical_skills, c.seniority_level, c.status,
                    c.created_at as applied_date,
                    f.reviewer, f.free_text as feedback_text, f.values_scores,
                    f.overall_recommendation, f.created_at as feedback_date,
                    i.interview_date, i.interviewer, i.status as interview_status,
                    o.salary, o.status as offer_status, o.offer_date
                FROM candidates c
                LEFT JOIN feedback f ON c.id = f.candidate_id
                LEFT JOIN interviews i ON c.id = i.candidate_id
                LEFT JOIN offers o ON c.id = o.candidate_id
                WHERE c.job_id = :job_id
                ORDER BY c.created_at DESC
            """)
            
            candidates_result = connection.execute(candidates_query, {"job_id": job_id})
            
            # Process results into DataFrame
            report_data = []
            for row in candidates_result:
                # Parse values scores if available
                values_scores = {}
                if row[12]:  # values_scores column
                    try:
                        import json
                        values_scores = json.loads(row[12])
                    except:
                        values_scores = {}
                
                report_row = {
                    'Job_ID': job_id,
                    'Job_Title': job_data[0],
                    'Candidate_ID': row[0],
                    'Candidate_Name': row[1],
                    'Email': row[2],
                    'Phone': row[3],
                    'Location': row[4],
                    'Experience_Years': row[5],
                    'Education_Level': row[6],
                    'Technical_Skills': row[7],
                    'Seniority_Level': row[8],
                    'Application_Status': row[9],
                    'Applied_Date': row[10],
                    'Reviewer': row[11] or 'Not Reviewed',
                    'Feedback_Text': row[12] or 'No feedback provided',
                    'Overall_Recommendation': row[13] or 'Pending',
                    'Feedback_Date': row[14],
                    'Values_Integrity': values_scores.get('integrity', 'N/A'),
                    'Values_Honesty': values_scores.get('honesty', 'N/A'),
                    'Values_Discipline': values_scores.get('discipline', 'N/A'),
                    'Values_Hard_Work': values_scores.get('hard_work', 'N/A'),
                    'Values_Gratitude': values_scores.get('gratitude', 'N/A'),
                    'Values_Average': calculate_values_average(values_scores),
                    'Interview_Date': row[15],
                    'Interviewer': row[16],
                    'Interview_Status': row[17],
                    'Offer_Salary': row[18],
                    'Offer_Status': row[19],
                    'Offer_Date': row[20]
                }
                report_data.append(report_row)
            
            # Create DataFrame and CSV
            df = pd.DataFrame(report_data)
            
            # Generate CSV content with resource management
            csv_buffer = io.StringIO()
            try:
                df.to_csv(csv_buffer, index=False)
                csv_content = csv_buffer.getvalue()
            finally:
                csv_buffer.close()
            
            # Create filename with timestamp
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            filename = f"job_{job_id}_report_{timestamp}.csv"
            
            # Return as streaming response
            return StreamingResponse(
                io.BytesIO(csv_content.encode('utf-8')),
                media_type="text/csv",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")

def calculate_values_average(values_scores):
    """Calculate average values score"""
    if not values_scores:
        return 'N/A'
    
    valid_scores = [score for score in values_scores.values() if isinstance(score, (int, float))]
    if not valid_scores:
        return 'N/A'
    
    return round(sum(valid_scores) / len(valid_scores), 2)

@router.get("/candidates/export.csv")
async def export_all_candidates():
    """Export all candidates with values data"""
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            query = text("""
                SELECT 
                    c.id, c.job_id, c.name, c.email, c.phone, c.location,
                    c.experience_years, c.education_level, c.technical_skills,
                    c.seniority_level, c.status, c.created_at,
                    f.values_scores, f.overall_recommendation,
                    j.title as job_title
                FROM candidates c
                LEFT JOIN feedback f ON c.id = f.candidate_id
                LEFT JOIN jobs j ON c.job_id = j.id
                ORDER BY c.created_at DESC
            """)
            
            result = connection.execute(query)
            
            candidates_data = []
            for row in result:
                values_scores = {}
                if row[12]:  # values_scores
                    try:
                        import json
                        values_scores = json.loads(row[12])
                    except:
                        values_scores = {}
                
                candidate_row = {
                    'Candidate_ID': row[0],
                    'Job_ID': row[1],
                    'Job_Title': row[14] or 'Unknown',
                    'Name': row[2],
                    'Email': row[3],
                    'Phone': row[4],
                    'Location': row[5],
                    'Experience_Years': row[6],
                    'Education_Level': row[7],
                    'Technical_Skills': row[8],
                    'Seniority_Level': row[9],
                    'Status': row[10],
                    'Applied_Date': row[11],
                    'Values_Integrity': values_scores.get('integrity', 'N/A'),
                    'Values_Honesty': values_scores.get('honesty', 'N/A'),
                    'Values_Discipline': values_scores.get('discipline', 'N/A'),
                    'Values_Hard_Work': values_scores.get('hard_work', 'N/A'),
                    'Values_Gratitude': values_scores.get('gratitude', 'N/A'),
                    'Values_Average': calculate_values_average(values_scores),
                    'Overall_Recommendation': row[13] or 'Pending'
                }
                candidates_data.append(candidate_row)
            
            df = pd.DataFrame(candidates_data)
            
            csv_buffer = io.StringIO()
            try:
                df.to_csv(csv_buffer, index=False)
                csv_content = csv_buffer.getvalue()
            finally:
                csv_buffer.close()
            
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            filename = f"all_candidates_report_{timestamp}.csv"
            
            return StreamingResponse(
                io.BytesIO(csv_content.encode('utf-8')),
                media_type="text/csv",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")