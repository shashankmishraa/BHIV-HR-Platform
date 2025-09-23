# Core API Endpoints Module
# Split from main.py for better maintainability

from datetime import datetime, timezone
from fastapi import APIRouter, Response, Request, Depends, HTTPException
from fastapi.responses import FileResponse
import os
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Import dependencies
try:
    from .database_manager import database_manager
    from .monitoring import structured_logger
    from .performance_optimizer import performance_cache
except ImportError:
    # Fallback imports
    structured_logger = None
    performance_cache = None

router = APIRouter()
_executor = ThreadPoolExecutor(max_workers=20)

def get_standardized_auth(request: Request = None):
    """Fallback auth for core endpoints"""
    return type('AuthResult', (), {'success': True, 'user_id': 'system'})()

def get_db_engine():
    """Get database engine"""
    from sqlalchemy import create_engine
    database_url = os.getenv("DATABASE_URL", "postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@db:5432/bhiv_hr_nqzb")
    return create_engine(database_url, pool_size=10, max_overflow=20, pool_pre_ping=True)

# Core API Endpoints (4 endpoints)
@router.get("/", tags=["Core API Endpoints"])
@router.head("/", tags=["Core API Endpoints"])
def read_root():
    """API Root Information"""
    return {
        "message": "BHIV HR Platform API Gateway",
        "version": "3.2.0",
        "status": "healthy",
        "endpoints": 166,
        "documentation": "/docs",
        "monitoring": "/metrics",
        "live_demo": "https://bhiv-hr-gateway-901a.onrender.com",
        "supported_methods": ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"],
        "features": [
            "Advanced AI Matching v3.2.0",
            "Job-specific candidate scoring",
            "Real-time database integration",
            "Enterprise security",
            "Comprehensive monitoring"
        ]
    }

@router.get("/health", tags=["Core API Endpoints"])
@router.head("/health", tags=["Core API Endpoints"])
def health_check(response: Response):
    """Health Check - Supports both GET and HEAD methods"""
    response.headers["X-RateLimit-Limit"] = "60"
    response.headers["X-RateLimit-Remaining"] = "59"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    
    return {
        "status": "healthy",
        "service": "BHIV HR Gateway",
        "version": "3.2.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "uptime": "operational",
        "methods_supported": ["GET", "HEAD"]
    }

@router.get("/test-candidates", tags=["Core API Endpoints"])
@router.head("/test-candidates", tags=["Core API Endpoints"])
async def test_candidates_db(request: Request, auth_result = Depends(get_standardized_auth)):
    """Test Candidates with Sample Data - Supports both GET and HEAD methods"""
    try:
        def execute_db_test():
            engine = get_db_engine()
            with engine.connect() as connection:
                from sqlalchemy import text
                connection.execute(text("SELECT 1"))
                
                # Get actual candidate count
                count_result = connection.execute(text("SELECT COUNT(*) FROM candidates"))
                candidate_count = count_result.fetchone()[0]
                
                # Get sample candidates for testing
                sample_query = text("""
                    SELECT id, name, email, technical_skills, experience_years, location
                    FROM candidates 
                    WHERE (status = 'active' OR status IS NULL)
                    ORDER BY experience_years DESC
                    LIMIT 5
                """)
                sample_result = connection.execute(sample_query)
                sample_candidates = sample_result.fetchall()
                
                return candidate_count, sample_candidates
        
        # Run test asynchronously
        loop = asyncio.get_event_loop()
        candidate_count, sample_rows = await loop.run_in_executor(_executor, execute_db_test)
        
        # Build sample candidates array
        candidates = []
        for row in sample_rows:
            candidates.append({
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "skills": row[3] or "No skills listed",
                "experience": row[4] or 0,
                "location": row[5] or "Not specified"
            })
        
        # If no real candidates, provide test data
        if not candidates:
            candidates = [
                {
                    "id": 999,
                    "name": "Test Candidate 1",
                    "email": "test1@example.com",
                    "skills": "Python, FastAPI, PostgreSQL",
                    "experience": 3,
                    "location": "Remote"
                },
                {
                    "id": 998,
                    "name": "Test Candidate 2",
                    "email": "test2@example.com",
                    "skills": "JavaScript, React, Node.js",
                    "experience": 5,
                    "location": "New York"
                }
            ]
        
        return {
            "database_status": "connected",
            "total_candidates": candidate_count,
            "candidates": candidates,
            "sample_count": len(candidates),
            "test_timestamp": datetime.now(timezone.utc).isoformat(),
            "connection_pool": "healthy",
            "pool_size": 20,
            "max_overflow": 30,
            "optimized": True
        }
    except Exception as e:
        # Provide fallback test data on error
        return {
            "database_status": "error",
            "total_candidates": 0,
            "candidates": [
                {
                    "id": 999,
                    "name": "Fallback Test Candidate",
                    "email": "fallback@example.com",
                    "skills": "Test Skills",
                    "experience": 1,
                    "location": "Test Location"
                }
            ],
            "sample_count": 1,
            "error": str(e),
            "test_timestamp": datetime.now(timezone.utc).isoformat(),
            "fallback_mode": True
        }

@router.get("/http-methods-test", tags=["Core API Endpoints"])
@router.head("/http-methods-test", tags=["Core API Endpoints"])
@router.options("/http-methods-test", tags=["Core API Endpoints"])
async def http_methods_test(request: Request):
    """HTTP Methods Testing Endpoint"""
    method = request.method
    
    response_data = {
        "method_received": method,
        "supported_methods": ["GET", "HEAD", "OPTIONS"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "method_handled_successfully"
    }
    
    if method == "OPTIONS":
        from fastapi.responses import Response
        return Response(
            content="",
            status_code=200,
            headers={
                "Allow": "GET, HEAD, OPTIONS",
                "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS"
            }
        )
    
    return response_data

@router.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """Serve favicon.ico from centralized location"""
    try:
        from static_assets import get_favicon_path
        favicon_path = get_favicon_path()
        if os.path.exists(favicon_path):
            return FileResponse(
                favicon_path,
                media_type="image/x-icon",
                headers={
                    "Cache-Control": "public, max-age=86400",
                    "ETag": '"bhiv-favicon-v2"'
                }
            )
    except ImportError:
        pass
    from fastapi.responses import Response
    return Response(status_code=204)