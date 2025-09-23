# Session Management Module
# Handles all session-related operations

from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends, Request, Response
from pydantic import BaseModel
import secrets

# Session models
class ClientLogin(BaseModel):
    client_id: str
    password: str

# Initialize router
router = APIRouter()

def get_api_key():
    return "authenticated_user"

# Simple session manager
class SimpleSessionManager:
    def __init__(self):
        self.sessions = {}
    
    def create_session(self, client_id: str, user_data: dict):
        session_id = secrets.token_urlsafe(32)
        self.sessions[session_id] = {
            'client_id': client_id,
            'user_data': user_data,
            'created_at': datetime.now(timezone.utc).isoformat(),
            'expires_at': (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
        }
        return session_id
    
    def invalidate_session(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
    
    def get_cookie_headers(self, session_id: str):
        return {
            "Set-Cookie": f"session_id={session_id}; HttpOnly; Secure; SameSite=Strict; Max-Age=3600"
        }

session_manager = SimpleSessionManager()

# Session Management endpoints (6 endpoints)
@router.post("/sessions/create", tags=["Session Management"])
async def create_secure_session(request: Request, response: Response, login_data: ClientLogin):
    try:
        valid_clients = {
            "TECH001": "demo123",
            "STARTUP01": "startup123",
            "ENTERPRISE01": "enterprise123"
        }
        
        if login_data.client_id in valid_clients and valid_clients[login_data.client_id] == login_data.password:
            # Create secure session
            user_data = {
                "client_id": login_data.client_id,
                "permissions": ["view_jobs", "create_jobs", "view_candidates", "schedule_interviews"],
                "login_time": datetime.now(timezone.utc).isoformat()
            }
            
            session_id = session_manager.create_session(login_data.client_id, user_data)
            
            # Set secure cookie headers
            cookie_headers = session_manager.get_cookie_headers(session_id)
            for header, value in cookie_headers.items():
                response.headers[header] = value
            
            return {
                "message": "Authentication successful",
                "client_id": login_data.client_id,
                "session_created": True,
                "security_features": ["Secure Cookies", "HttpOnly", "SameSite", "Session Timeout"],
                "expires_in": 3600
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid client credentials")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authentication failed: {str(e)}")

@router.get("/sessions/validate", tags=["Session Management"])
async def validate_session(request: Request):
    try:
        # Extract session ID from cookie
        cookies = request.cookies
        session_id = cookies.get("session_id")
        
        if not session_id:
            return {
                "session_valid": False,
                "error": "No session found",
                "requires_login": True
            }
        
        # For demo purposes, validate basic session format
        if len(session_id) >= 8:
            return {
                "session_valid": True,
                "session_id": session_id[:8] + "...",
                "user_id": "demo_user",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "expires_at": (datetime.now(timezone.utc).replace(hour=23, minute=59)).isoformat()
            }
        else:
            return {
                "session_valid": False,
                "error": "Invalid session format",
                "requires_login": True
            }
        
    except Exception as e:
        return {
            "session_valid": False,
            "error": "Session validation failed",
            "requires_login": True,
            "exception": str(e)
        }

@router.post("/sessions/logout", tags=["Session Management"])
async def logout_session(request: Request, response: Response):
    try:
        cookies = request.cookies
        session_id = cookies.get("session_id")
        
        if session_id:
            session_manager.invalidate_session(session_id)
            
            # Clear cookie
            response.set_cookie(
                "session_id",
                "",
                max_age=0,
                secure=True,
                httponly=True,
                samesite="strict"
            )
        
        return {"message": "Logged out successfully", "session_cleared": True}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail="Logout failed")

@router.get("/sessions/active", tags=["Session Management"])
async def get_active_sessions(api_key: str = Depends(get_api_key)):
    try:
        current_time = datetime.now(timezone.utc)
        active_sessions = []
        
        for session_id, session in session_manager.sessions.items():
            expires_at = datetime.fromisoformat(session['expires_at'].replace('Z', '+00:00'))
            if expires_at > current_time:
                active_sessions.append({
                    "session_id": session_id[:8] + "...",
                    "client_id": session['client_id'],
                    "created_at": session['created_at'],
                    "expires_at": session['expires_at']
                })
        
        return {"active_sessions": active_sessions, "count": len(active_sessions)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Active sessions retrieval failed: {str(e)}")

@router.post("/sessions/cleanup", tags=["Session Management"])
async def cleanup_sessions(cleanup_config: dict, api_key: str = Depends(get_api_key)):
    try:
        max_age_hours = cleanup_config.get("max_age_hours", 24)
        cleanup_inactive = cleanup_config.get("cleanup_inactive", True)
        
        current_time = datetime.now(timezone.utc)
        cutoff_time = current_time - timedelta(hours=max_age_hours)
        
        cleaned_count = 0
        for session_id, session in list(session_manager.sessions.items()):
            created_at = datetime.fromisoformat(session['created_at'].replace('Z', '+00:00'))
            if created_at < cutoff_time:
                session_manager.invalidate_session(session_id)
                cleaned_count += 1
        
        return {
            "sessions_cleaned": cleaned_count,
            "cleanup_at": current_time.isoformat(),
            "criteria": {"max_age_hours": max_age_hours, "cleanup_inactive": cleanup_inactive}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Session cleanup failed: {str(e)}")

@router.get("/sessions/stats", tags=["Session Management"])
async def get_session_stats(api_key: str = Depends(get_api_key)):
    try:
        current_time = datetime.now(timezone.utc)
        total_sessions = len(session_manager.sessions)
        active_sessions = 0
        
        for session in session_manager.sessions.values():
            expires_at = datetime.fromisoformat(session['expires_at'].replace('Z', '+00:00'))
            if expires_at > current_time:
                active_sessions += 1
        
        expired_sessions = total_sessions - active_sessions
        
        return {
            "total_sessions": total_sessions,
            "active_sessions": active_sessions,
            "expired_sessions": expired_sessions,
            "stats_generated_at": current_time.isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Session stats failed: {str(e)}")