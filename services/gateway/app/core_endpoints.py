# Core Endpoints Router
from fastapi import APIRouter, Request
from datetime import datetime, timezone
import os

router = APIRouter()

@router.get("/")
async def root():
    """API Gateway root endpoint"""
    return {
        "message": "BHIV HR Platform API Gateway",
        "version": "3.2.0",
        "status": "operational",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "BHIV HR Gateway",
        "version": "3.2.0",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@router.get("/test-candidates")
async def test_candidates():
    """Test endpoint for candidate data"""
    return {
        "message": "Test candidates endpoint",
        "count": 45,
        "status": "available"
    }

@router.get("/http-methods-test")
async def http_methods_test():
    """HTTP methods test endpoint"""
    return {
        "supported_methods": ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"],
        "status": "operational"
    }