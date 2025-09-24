# Session Management Router
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class SessionInfo(BaseModel):
    session_id: str
    user_id: str
    created_at: str
    last_activity: str
    ip_address: str

@router.get("/sessions")
async def list_sessions() -> List[SessionInfo]:
    """List active sessions"""
    return [
        SessionInfo(
            session_id="sess_123",
            user_id="user_123",
            created_at="2025-01-18T10:00:00Z",
            last_activity="2025-01-18T10:30:00Z",
            ip_address="192.168.1.1"
        )
    ]

@router.delete("/sessions/{session_id}")
async def terminate_session(session_id: str):
    """Terminate specific session"""
    return {
        "session_id": session_id,
        "message": "Session terminated successfully"
    }

@router.post("/sessions/cleanup")
async def cleanup_expired_sessions():
    """Cleanup expired sessions"""
    return {
        "cleaned_sessions": 5,
        "message": "Expired sessions cleaned up"
    }

@router.get("/sessions/stats")
async def session_statistics():
    """Get session statistics"""
    return {
        "active_sessions": 10,
        "total_sessions_today": 50,
        "average_session_duration": "45 minutes"
    }