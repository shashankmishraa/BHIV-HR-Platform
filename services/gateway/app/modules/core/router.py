"""Core API endpoints router"""

from fastapi import APIRouter
from datetime import datetime, timezone
import os

router = APIRouter(tags=["Core"])

@router.get("/")
async def root():
    """API Gateway root endpoint"""
    return {
        "message": "BHIV HR Platform API Gateway",
        "version": "3.2.0",
        "status": "operational",
        "environment": os.getenv("ENVIRONMENT", "production"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_endpoints": "180+",
        "modules": ["core", "candidates", "jobs", "auth", "workflows", "monitoring"]
    }

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "BHIV HR Gateway",
        "version": "3.2.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "components": {
            "core": "healthy",
            "database": "healthy",
            "workflows": "healthy"
        }
    }

@router.get("/test-candidates")
async def test_candidates():
    """Test endpoint for candidate data"""
    return {
        "message": "Test candidates endpoint",
        "count": 30,
        "status": "available"
    }

@router.get("/http-methods-test")
async def http_methods_test():
    """HTTP methods test endpoint"""
    return {
        "supported_methods": ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"],
        "status": "operational"
    }

@router.get("/architecture")
async def get_architecture():
    """System architecture information"""
    return {
        "architecture": {
            "type": "modular_microservices",
            "pattern": "api_gateway_with_modules",
            "modules": 6,
            "total_endpoints": "180+",
            "workflow_integration": True,
            "pipeline_orchestration": True
        },
        "technology_stack": {
            "framework": "FastAPI 0.104+",
            "python": "3.11+",
            "database": "PostgreSQL",
            "deployment": "Render Cloud",
            "monitoring": "Prometheus Compatible"
        },
        "capabilities": {
            "rest_api": True,
            "workflow_orchestration": True,
            "pipeline_automation": True,
            "real_time_monitoring": True,
            "modular_architecture": True,
            "background_processing": True,
            "error_recovery": True
        }
    }