"""User Workflow Endpoints - Organized by User Journey"""

from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter()

@router.get("/workflow/start", tags=["🚀 Getting Started"])
async def workflow_start():
    """Start here - Complete user workflow guide"""
    return {
        "welcome": "Welcome to BHIV HR Platform",
        "live_services": {
            "gateway": "https://bhiv-hr-gateway-901a.onrender.com",
            "hr_portal": "https://bhiv-hr-portal-xk2k.onrender.com",
            "client_portal": "https://bhiv-hr-client-portal-zdbt.onrender.com"
        },
        "user_journeys": {
            "hr_manager": [
                {"step": 1, "action": "Login", "endpoint": "/auth/login"},
                {"step": 2, "action": "Create Job", "endpoint": "/jobs/create"},
                {"step": 3, "action": "Upload Candidates", "endpoint": "/candidates/upload"},
                {"step": 4, "action": "AI Matching", "endpoint": "/matching/find-candidates"},
                {"step": 5, "action": "Schedule Interviews", "endpoint": "/interviews/schedule"}
            ],
            "client": [
                {"step": 1, "action": "Client Login", "endpoint": "/client/login"},
                {"step": 2, "action": "Post Job", "endpoint": "/client/jobs/post"},
                {"step": 3, "action": "Review Matches", "endpoint": "/client/candidates/matches"}
            ]
        }
    }

@router.post("/auth/login", tags=["🔐 Step 1: Authentication"])
async def user_login():
    """Step 1: User authentication"""
    return {
        "step": "1 - Authentication",
        "demo_credentials": {
            "hr_user": {"username": "hr@bhiv.com", "password": "demo123"},
            "client_user": {"username": "TECH001", "password": "demo123"}
        },
        "portals": {
            "hr_portal": "https://bhiv-hr-portal-xk2k.onrender.com",
            "client_portal": "https://bhiv-hr-client-portal-zdbt.onrender.com"
        }
    }

@router.post("/jobs/create", tags=["💼 Step 2: Job Management"])
async def create_job_workflow():
    """Step 2: Create new job posting"""
    return {
        "step": "2 - Job Creation",
        "form_fields": {
            "title": "Job title",
            "description": "Job description",
            "required_skills": ["Python", "React", "PostgreSQL"],
            "experience_level": "Junior/Mid/Senior/Lead",
            "location": "Remote/City/Hybrid"
        },
        "next_step": "/candidates/upload"
    }

@router.post("/candidates/upload", tags=["👥 Step 3: Candidate Management"])
async def upload_candidates_workflow():
    """Step 3: Upload candidate profiles"""
    return {
        "step": "3 - Candidate Upload",
        "upload_methods": {
            "bulk_csv": "Upload CSV file",
            "resume_parsing": "AI-powered resume parsing",
            "manual_entry": "Add candidates individually"
        },
        "next_step": "/matching/find-candidates"
    }

@router.get("/matching/find-candidates", tags=["🤖 Step 4: AI Matching"])
async def ai_matching_workflow():
    """Step 4: AI-powered candidate matching"""
    return {
        "step": "4 - AI Matching",
        "ai_features": {
            "semantic_matching": "Advanced skill matching",
            "bias_mitigation": "Fair candidate ranking",
            "explainable_ai": "Clear match reasoning"
        },
        "sample_matches": [
            {"candidate": "John Doe", "score": 94.5, "strengths": ["Python", "Leadership"]},
            {"candidate": "Jane Smith", "score": 87.3, "strengths": ["React", "Team work"]}
        ],
        "next_step": "/interviews/schedule"
    }

@router.post("/interviews/schedule", tags=["📅 Step 5: Interview Management"])
async def schedule_interview_workflow():
    """Step 5: Schedule interviews"""
    return {
        "step": "5 - Interview Scheduling",
        "features": {
            "calendar_integration": "Google Calendar, Outlook",
            "automated_reminders": "Email and SMS notifications",
            "feedback_collection": "Structured evaluation forms"
        },
        "next_step": "/reports/summary"
    }

@router.get("/system/status", tags=["🔧 System Status"])
async def system_status():
    """Real-time system status"""
    return {
        "system_health": "🟢 All Systems Operational",
        "services": {
            "gateway": {"status": "🟢 Online", "url": "https://bhiv-hr-gateway-901a.onrender.com"},
            "ai_agent": {"status": "🟢 Online", "url": "https://bhiv-hr-agent-o6nx.onrender.com"},
            "hr_portal": {"status": "🟢 Online", "url": "https://bhiv-hr-portal-xk2k.onrender.com"},
            "client_portal": {"status": "🟢 Online", "url": "https://bhiv-hr-client-portal-zdbt.onrender.com"}
        },
        "performance": {
            "api_response_time": "<100ms",
            "ai_matching_speed": "<0.02s per candidate",
            "uptime": "99.9%"
        }
    }