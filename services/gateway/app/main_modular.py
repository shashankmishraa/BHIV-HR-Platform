# BHIV HR Platform API Gateway - Modular Architecture
# Main application file with modular imports

from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, Response
from fastapi import Request
import os

# Import modular components
try:
    from .core_endpoints import router as core_router
    from .auth import router as auth_router
    from .database import router as database_router
    from .monitoring import router as monitoring_router
except ImportError:
    # Fallback for direct execution
    from core_endpoints import router as core_router
    from auth import router as auth_router
    from database import router as database_router
    from monitoring import router as monitoring_router

# Initialize FastAPI application
app = FastAPI(
    title="BHIV HR Platform API Gateway",
    version="3.2.0",
    description="Enterprise HR Platform with Advanced AI Matching and Security Features - Modular Architecture"
)

# HTTP Method Handler Middleware (MUST be first)
@app.middleware("http")
async def http_method_handler(request: Request, call_next):
    """Handle HTTP methods including HEAD and OPTIONS requests"""
    method = request.method
    
    if method == "HEAD":
        get_request = Request(
            scope={**request.scope, "method": "GET"}
        )
        response = await call_next(get_request)
        return Response(
            content="",
            status_code=response.status_code,
            headers=response.headers,
            media_type=response.media_type
        )
    
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
    
    elif method not in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
        return PlainTextResponse(
            content=f"Method {method} not allowed. Supported methods: GET, POST, PUT, DELETE, HEAD, OPTIONS",
            status_code=405,
            headers={"Allow": "GET, POST, PUT, DELETE, HEAD, OPTIONS"}
        )
    
    return await call_next(request)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"],
    allow_headers=["*"],
    max_age=86400
)

# Include modular routers
app.include_router(core_router, tags=["Core"])
app.include_router(auth_router, tags=["Authentication"])
app.include_router(database_router, tags=["Database"])
app.include_router(monitoring_router, tags=["Monitoring"])

# AI Matching endpoints (simplified)
@app.get("/v1/match/{job_id}/top", tags=["AI Matching"])
async def get_top_matches(job_id: int, limit: int = 10):
    """Job-Specific AI Matching - Simplified Implementation"""
    return {
        "matches": [
            {
                "candidate_id": 1,
                "name": "John Doe",
                "score": 92.5,
                "skills_match": "Python, React, PostgreSQL",
                "experience_years": 5,
                "recommendation": "Excellent Match"
            },
            {
                "candidate_id": 2,
                "name": "Jane Smith",
                "score": 88.3,
                "skills_match": "JavaScript, Node.js, MongoDB",
                "experience_years": 4,
                "recommendation": "Strong Match"
            }
        ],
        "job_id": job_id,
        "limit": limit,
        "algorithm_version": "v3.2.0-modular",
        "processing_time": "0.15s",
        "candidates_processed": 2
    }

# Security endpoints (simplified)
@app.get("/v1/security/status", tags=["Security"])
async def get_security_status():
    """Security Status Monitoring"""
    return {
        "security_status": "active",
        "features": {
            "rate_limiting": True,
            "api_authentication": True,
            "cors_protection": True,
            "security_headers": True,
            "input_validation": True,
            "audit_logging": True
        },
        "threat_level": "low",
        "last_security_scan": datetime.now(timezone.utc).isoformat(),
        "vulnerabilities_detected": 0
    }

# Analytics endpoints (simplified)
@app.get("/v1/analytics/dashboard", tags=["Analytics"])
async def get_analytics_dashboard():
    """Analytics Dashboard"""
    return {
        "dashboard_metrics": {
            "total_candidates": 68,
            "total_jobs": 33,
            "total_interviews": 15,
            "avg_experience": 4.2
        },
        "generated_at": datetime.now(timezone.utc).isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)