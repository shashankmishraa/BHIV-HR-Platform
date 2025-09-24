# Client Portal Router
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class ClientLogin(BaseModel):
    client_id: str
    password: str

class ClientProfile(BaseModel):
    company_name: Optional[str] = None
    contact_email: Optional[str] = None
    industry: Optional[str] = None

@router.post("/client/login")
async def client_login(credentials: ClientLogin):
    """Client portal login"""
    if credentials.client_id == "TECH001" and credentials.password == "demo123":
        return {
            "access_token": "client_token_123",
            "client_id": credentials.client_id,
            "company_name": "Tech Solutions Inc."
        }
    raise HTTPException(status_code=401, detail="Invalid client credentials")

@router.get("/client/profile")
async def get_client_profile():
    """Get client profile"""
    return {
        "client_id": "TECH001",
        "company_name": "Tech Solutions Inc.",
        "contact_email": "contact@techsolutions.com",
        "industry": "Technology",
        "active_jobs": 3
    }

@router.put("/client/profile")
async def update_client_profile(profile: ClientProfile):
    """Update client profile"""
    return {
        "message": "Profile updated successfully",
        **profile.dict(exclude_unset=True)
    }

@router.get("/client/jobs")
async def get_client_jobs():
    """Get jobs posted by client"""
    return {
        "jobs": [
            {
                "id": "job_123",
                "title": "Senior Developer",
                "status": "active",
                "applications": 15
            }
        ],
        "total": 1
    }

@router.get("/client/candidates/{job_id}")
async def get_job_candidates(job_id: str):
    """Get candidates for specific job"""
    return {
        "job_id": job_id,
        "candidates": [],
        "total": 0
    }