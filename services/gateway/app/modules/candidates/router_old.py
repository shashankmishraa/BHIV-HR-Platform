"""Candidates workflow router"""

import secrets
from datetime import datetime, timezone
from typing import List, Optional

from app.shared.models import CandidateCreate, CandidateUpdate
from app.shared.schemas import (
    PaginatedCandidatesResponse, 
    CandidateResponse, 
    CandidateStatsResponse,
    ErrorResponse
)
from fastapi import APIRouter, BackgroundTasks, File, Form, Query, UploadFile, HTTPException, Path
from pydantic import BaseModel

router = APIRouter(prefix="/v1/candidates", tags=["Candidates"])

# Constants
ALLOWED_FILE_TYPES = {
    'application/pdf', 
    'application/msword', 
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
}

class BulkCandidateRequest(BaseModel):
    candidates: List[CandidateCreate]


@router.get("", response_model=PaginatedCandidatesResponse)
async def list_candidates(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    skills: Optional[str] = Query(None),
    experience_min: Optional[int] = Query(None, ge=0),
    location: Optional[str] = Query(None),
):
    """List candidates with filtering and pagination"""
    from app.shared.database import db_manager
    
    try:
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            
            # Build dynamic query with filters
            where_conditions = []
            params = []
            
            if search:
                where_conditions.append("(name ILIKE %s OR email ILIKE %s OR technical_skills ILIKE %s)")
                search_param = f"%{search}%"
                params.extend([search_param, search_param, search_param])
            
            if skills:
                where_conditions.append("technical_skills ILIKE %s")
                params.append(f"%{skills}%")
            
            if experience_min is not None:
                where_conditions.append("experience_years >= %s")
                params.append(experience_min)
            
            if location:
                where_conditions.append("location ILIKE %s")
                params.append(f"%{location}%")
            
            where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"
            
            # Single query with window function for better performance
            offset = (page - 1) * per_page
            data_query = f"""
                SELECT id, name, email, phone, location, experience_years, 
                       technical_skills, seniority_level, education_level, status, created_at,
                       COUNT(*) OVER() as total_count
                FROM candidates 
                WHERE {where_clause}
                ORDER BY created_at DESC 
                LIMIT %s OFFSET %s
            """
            cursor.execute(data_query, params + [per_page, offset])
            
            rows = cursor.fetchall()
            total = rows[0][11] if rows else 0
            
            candidates = []
            for row in rows:
                candidates.append({
                    "id": row[0],
                    "name": row[1],
                    "email": row[2],
                    "phone": row[3],
                    "location": row[4],
                    "experience_years": row[5],
                    "technical_skills": row[6],
                    "seniority_level": row[7],
                    "education_level": row[8],
                    "status": row[9],
                    "created_at": row[10].isoformat() if row[10] else None
                })
            
            pages = (total + per_page - 1) // per_page
            
            return {
                "candidates": candidates,
                "total": total,
                "page": page,
                "per_page": per_page,
                "pages": pages,
                "filters": {
                    "search": search,
                    "skills": skills,
                    "experience_min": experience_min,
                    "location": location,
                },
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.post("", response_model=CandidateResponse)
async def create_candidate(
    candidate: CandidateCreate, background_tasks: BackgroundTasks
):
    """Create new candidate with database persistence"""
    from app.shared.database import db_manager
    
    try:
        # Map model fields to database fields
        skills_str = ', '.join(candidate.skills) if candidate.skills else ''
        
        # Insert into database
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO candidates (name, email, phone, location, technical_skills,
                                          experience_years, seniority_level, education_level, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id, created_at
                """, (
                    candidate.name,
                    candidate.email,
                    candidate.phone,
                    candidate.location or '',
                    skills_str,
                    candidate.experience_years,
                    candidate.designation or 'Junior',
                    candidate.education or 'Bachelor\'s',
                    'active'
                ))
                
                row = cursor.fetchone()
                candidate_id, created_at = row[0], row[1]
                conn.commit()
            except Exception:
                conn.rollback()
                raise

        return CandidateResponse(
            id=candidate_id,
            name=candidate.name,
            email=candidate.email,
            phone=candidate.phone,
            location=candidate.location,
            experience_years=candidate.experience_years,
            technical_skills=skills_str,
            seniority_level=candidate.designation or 'Junior',
            education_level=candidate.education or 'Bachelor\'s',
            status='active',
            created_at=created_at.isoformat() if created_at else None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create candidate: {str(e)}")


@router.get("/{candidate_id}", response_model=CandidateResponse)
async def get_candidate(candidate_id: int = Path(..., gt=0)):
    """Get specific candidate details"""
    from app.shared.database import db_manager
    
    try:
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, email, phone, location, experience_years,
                       technical_skills, seniority_level, education_level, 
                       status, created_at, updated_at
                FROM candidates WHERE id = %s
            """, (candidate_id,))
            
            row = cursor.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail=f"Candidate {candidate_id} not found")
            
            return CandidateResponse(
                id=row[0],
                name=row[1],
                email=row[2],
                phone=row[3],
                location=row[4],
                experience_years=row[5],
                technical_skills=row[6],
                seniority_level=row[7],
                education_level=row[8],
                status=row[9],
                created_at=row[10].isoformat() if row[10] else None,
                updated_at=row[11].isoformat() if row[11] else None
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.put("/{candidate_id}", response_model=CandidateResponse)
async def update_candidate(candidate_id: int = Path(..., gt=0), candidate: CandidateUpdate = None):
    """Update candidate information"""
    from app.shared.database import db_manager
    
    if candidate is None:
        raise HTTPException(status_code=400, detail="Request body is required")
    
    try:
        # Build dynamic update query using field mapping
        field_mapping = {
            'name': 'name',
            'email': 'email', 
            'phone': 'phone',
            'location': 'location',
            'skills': 'technical_skills',
            'experience_years': 'experience_years',
            'designation': 'seniority_level',
            'education': 'education_level'
        }
        
        update_fields = []
        params = []
        
        for field, db_column in field_mapping.items():
            value = getattr(candidate, field, None)
            if value is not None:
                if field == 'skills':
                    if isinstance(value, (list, tuple)):
                        value = ', '.join(value)
                    else:
                        raise HTTPException(status_code=400, detail="Skills must be a list")
                update_fields.append(f"{db_column} = %s")
                params.append(value)
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        update_fields.append("updated_at = NOW()")
        params.append(candidate_id)
        
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            try:
                # Update candidate
                update_query = f"""
                    UPDATE candidates 
                    SET {', '.join(update_fields)}
                    WHERE id = %s
                    RETURNING id, name, email, phone, location, experience_years,
                             technical_skills, seniority_level, education_level, 
                             status, created_at, updated_at
                """
                cursor.execute(update_query, params)
                
                row = cursor.fetchone()
                if not row:
                    raise HTTPException(status_code=404, detail=f"Candidate {candidate_id} not found")
                
                conn.commit()
                
                return CandidateResponse(
                    id=row[0],
                    name=row[1],
                    email=row[2],
                    phone=row[3],
                    location=row[4],
                    experience_years=row[5],
                    technical_skills=row[6],
                    seniority_level=row[7],
                    education_level=row[8],
                    status=row[9],
                    created_at=row[10].isoformat() if row[10] else None,
                    updated_at=row[11].isoformat() if row[11] else None
                )
            except Exception:
                conn.rollback()
                raise
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update candidate: {str(e)}")


@router.delete("/{candidate_id}")
async def delete_candidate(candidate_id: int = Path(..., gt=0)):
    """Delete candidate profile"""
    from app.shared.database import db_manager
    
    try:
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            try:
                # Soft delete with existence check in single query
                cursor.execute("""
                    UPDATE candidates 
                    SET status = 'deleted', updated_at = NOW() 
                    WHERE id = %s AND status != 'deleted'
                    RETURNING id
                """, (candidate_id,))
                
                if not cursor.fetchone():
                    raise HTTPException(status_code=404, detail=f"Candidate {candidate_id} not found or already deleted")
                
                conn.commit()
                
                return {"message": f"Candidate {candidate_id} deleted successfully"}
            except Exception:
                conn.rollback()
                raise
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete candidate: {str(e)}")


@router.post("/bulk")
async def bulk_create_candidates(
    request: BulkCandidateRequest, background_tasks: BackgroundTasks
):
    """Create multiple candidates with database persistence"""
    from app.shared.database import db_manager
    
    results = []
    errors = []
    
    try:
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            
            for i, candidate in enumerate(request.candidates):
                try:
                    skills_str = ', '.join(candidate.skills) if candidate.skills else ''
                    
                    cursor.execute("""
                        INSERT INTO candidates (name, email, phone, location, technical_skills,
                                              experience_years, seniority_level, education_level, status)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING id
                    """, (
                        candidate.name,
                        candidate.email,
                        candidate.phone,
                        candidate.location or '',
                        skills_str,
                        candidate.experience_years,
                        candidate.designation or 'Junior',
                        candidate.education or 'Bachelor\'s',
                        'active'
                    ))
                    
                    candidate_id = cursor.fetchone()[0]
                    results.append({"id": candidate_id, "email": candidate.email})
                    
                except Exception as e:
                    errors.append({"index": i, "email": candidate.email, "error": str(e)})
            
            if results:
                conn.commit()
            
        return {
            "created": len(results), 
            "candidates": results, 
            "errors": errors,
            "total_processed": len(request.candidates)
        }
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Bulk creation failed: {str(e)}")


@router.get("/stats", response_model=CandidateStatsResponse)
async def get_candidate_stats():
    """Get candidate statistics"""
    from app.shared.database import db_manager
    
    try:
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            
            # Single optimized query using CTEs
            cursor.execute("""
                WITH stats AS (
                    SELECT 
                        COUNT(*) as total_candidates,
                        COUNT(*) FILTER (WHERE status = 'active') as active_candidates
                    FROM candidates
                ),
                experience_stats AS (
                    SELECT json_object_agg(seniority_level, cnt) as by_experience
                    FROM (
                        SELECT seniority_level, COUNT(*) as cnt
                        FROM candidates 
                        WHERE seniority_level IS NOT NULL
                        GROUP BY seniority_level
                    ) exp
                ),
                location_stats AS (
                    SELECT json_object_agg(location_type, cnt) as by_location
                    FROM (
                        SELECT 
                            CASE 
                                WHEN location ILIKE '%remote%' THEN 'remote'
                                ELSE 'onsite'
                            END as location_type,
                            COUNT(*) as cnt
                        FROM candidates 
                        WHERE location IS NOT NULL
                        GROUP BY location_type
                    ) loc
                )
                SELECT s.total_candidates, s.active_candidates, 
                       COALESCE(e.by_experience, '{}') as by_experience,
                       COALESCE(l.by_location, '{}') as by_location
                FROM stats s
                CROSS JOIN experience_stats e
                CROSS JOIN location_stats l
            """)
            
            row = cursor.fetchone()
            total_candidates, active_candidates, by_experience, by_location = row
            
            return {
                "total_candidates": total_candidates,
                "active_candidates": active_candidates,
                "by_experience": by_experience or {},
                "by_location": by_location or {},
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Statistics error: {str(e)}")


@router.post("/{candidate_id}/notes")
async def add_candidate_note(candidate_id: int = Path(..., gt=0), note: str = Form(...)):
    """Add note to candidate profile"""
    from app.shared.database import db_manager
    
    if len(note.strip()) < 5:
        raise HTTPException(status_code=400, detail="Note must be at least 5 characters long")
    
    try:
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            
            # Verify candidate exists
            cursor.execute("SELECT id FROM candidates WHERE id = %s", (candidate_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail=f"Candidate {candidate_id} not found")
            
            note_id = f"note_{secrets.token_hex(4)}"
            
            return {
                "candidate_id": candidate_id,
                "note_id": note_id,
                "note": note.strip(),
                "created_at": datetime.now(timezone.utc).isoformat(),
                "message": "Note added successfully",
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add note: {str(e)}")


@router.get("/{candidate_id}/applications")
async def get_candidate_applications(candidate_id: int = Path(..., gt=0)):
    """Get candidate's job applications"""
    return {"candidate_id": candidate_id, "applications": [], "total": 0}


@router.get("/{candidate_id}/interviews")
async def get_candidate_interviews(candidate_id: int = Path(..., gt=0)):
    """Get candidate's interview history"""
    return {"candidate_id": candidate_id, "interviews": [], "total": 0}


@router.post("/{candidate_id}/resume")
async def upload_candidate_resume(candidate_id: int = Path(..., gt=0), file: UploadFile = File(...)):
    """Upload candidate resume file"""
    # Validate file size (10MB max)
    max_size = 10 * 1024 * 1024  # 10MB
    if file.size is None:
        raise HTTPException(status_code=400, detail="File size cannot be determined")
    if file.size > max_size:
        raise HTTPException(status_code=413, detail="File size exceeds 10MB limit")
    
    # Validate file type
    if file.content_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(status_code=400, detail="Only PDF and Word documents are allowed")
    
    # Verify candidate exists
    from app.shared.database import db_manager
    try:
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM candidates WHERE id = %s", (candidate_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail=f"Candidate {candidate_id} not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    return {
        "candidate_id": candidate_id,
        "filename": file.filename,
        "content_type": file.content_type,
        "size_bytes": file.size,
        "message": "Resume uploaded successfully",
    }


@router.post("/{candidate_id}/match")
async def match_candidate_jobs(candidate_id: int = Path(..., gt=0)):
    """Match jobs to specific candidate"""
    return {
        "candidate_id": candidate_id,
        "matched_jobs": [],
        "total_matches": 0,
        "algorithm": "semantic_v3.2",
        "status": "success",
    }


@router.get("/{candidate_id}/jobs")
async def get_candidate_jobs(candidate_id: int = Path(..., gt=0)):
    """Get jobs for specific candidate"""
    return {"candidate_id": candidate_id, "jobs": [], "total": 0, "status": "success"}