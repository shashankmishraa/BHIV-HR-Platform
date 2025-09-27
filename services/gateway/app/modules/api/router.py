"""API endpoints for data operations and testing"""

from datetime import datetime, timezone
from typing import List, Optional, Dict, Any

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from app.shared.auth import verify_api_key, require_write_access, require_admin_access

router = APIRouter(prefix="/api/v1", tags=["API Operations"])

@router.get("/test/auth")
async def test_authentication(auth_data: dict = Depends(verify_api_key)):
    """Test API authentication"""
    return {
        "message": "Authentication successful",
        "auth_type": auth_data.get("type"),
        "authenticated": True,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "access_info": auth_data.get("info", {})
    }

@router.post("/test/data")
async def create_test_data(auth_data: dict = Depends(require_write_access)):
    """Create test data for development"""
    from app.shared.database import db_manager
    
    try:
        with db_manager.get_connection() as conn:
            if conn is None:
                raise HTTPException(status_code=500, detail="Database connection unavailable")
            
            cursor = conn.cursor()
            
            # Create test candidates
            test_candidates = [
                ("John Doe", "john.doe@email.com", "+1234567890", "New York", "Python, FastAPI, React", 5, "Senior", "Bachelor's"),
                ("Jane Smith", "jane.smith@email.com", "+1234567891", "San Francisco", "JavaScript, Node.js, MongoDB", 3, "Mid-level", "Master's"),
                ("Bob Johnson", "bob.johnson@email.com", "+1234567892", "Austin", "Java, Spring Boot, MySQL", 7, "Senior", "Bachelor's")
            ]
            
            created_candidates = []
            for candidate in test_candidates:
                try:
                    cursor.execute("""
                        INSERT INTO candidates (name, email, phone, location, technical_skills,
                                              experience_years, seniority_level, education_level, status)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING id
                    """, (*candidate, 'active'))
                    
                    result = cursor.fetchone()
                    if result:
                        created_candidates.append({"id": result[0], "name": candidate[0]})
                except Exception:
                    continue
            
            conn.commit()
            
            return {
                "message": "Test data created successfully",
                "candidates_created": len(created_candidates),
                "candidates": created_candidates,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create test data: {str(e)}")

@router.get("/data/candidates")
async def get_all_candidates(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    auth_data: dict = Depends(verify_api_key)
):
    """Get all candidates with pagination"""
    from app.shared.database import db_manager
    
    try:
        with db_manager.get_connection() as conn:
            if conn is None:
                raise HTTPException(status_code=500, detail="Database connection unavailable")
            
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, name, email, phone, location, experience_years,
                       technical_skills, seniority_level, education_level, 
                       status, created_at
                FROM candidates 
                WHERE status = 'active'
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s
            """, (limit, offset))
            
            rows = cursor.fetchall()
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
            
            return {
                "candidates": candidates,
                "total": len(candidates),
                "limit": limit,
                "offset": offset,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/stats/system")
async def get_system_stats(auth_data: dict = Depends(verify_api_key)):
    """Get system statistics"""
    from app.shared.database import db_manager
    
    try:
        with db_manager.get_connection() as conn:
            if conn is None:
                return {
                    "database_status": "unavailable",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM candidates WHERE status = 'active'")
            result = cursor.fetchone()
            active_candidates = result[0] if result else 0
            
            return {
                "active_candidates": active_candidates,
                "database_status": "connected",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
    except Exception as e:
        return {
            "error": str(e),
            "database_status": "error",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }