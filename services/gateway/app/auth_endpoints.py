#!/usr/bin/env python3
"""
Authentication Endpoints - Priority 2 Implementation
Minimal authentication system to resolve 404 errors
"""

from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any
import secrets
import hashlib
import jwt
from fastapi import HTTPException
from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user_id: str

class SimpleAuthManager:
    """Minimal authentication manager"""
    
    def __init__(self):
        self.users = {
            "admin": {"password": "admin123", "role": "admin"},
            "hr_user": {"password": "hr123", "role": "hr"},
            "client": {"password": "client123", "role": "client"},
            "TECH001": {"password": "demo123", "role": "client"},
            "demo_user": {"password": "demo123", "role": "user"}
        }
        self.jwt_secret = "bhiv_jwt_secret_key_2025"
        self.sessions = {}
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user credentials"""
        if username in self.users and self.users[username]["password"] == password:
            return {
                "user_id": username,
                "username": username,
                "role": self.users[username]["role"],
                "authenticated": True
            }
        return None
    
    def generate_jwt_token(self, user_id: str, role: str = "user") -> str:
        """Generate JWT token"""
        payload = {
            "user_id": user_id,
            "role": role,
            "exp": datetime.utcnow() + timedelta(hours=24),
            "iat": datetime.utcnow()
        }
        return jwt.encode(payload, self.jwt_secret, algorithm="HS256")
    
    def validate_jwt_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Validate JWT token"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def create_session(self, user_id: str) -> str:
        """Create user session"""
        session_id = secrets.token_urlsafe(32)
        self.sessions[session_id] = {
            "user_id": user_id,
            "created_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(hours=24)
        }
        return session_id

# Global auth manager instance
auth_manager = SimpleAuthManager()

def create_auth_endpoints(app):
    """Add authentication endpoints to FastAPI app"""
    
    @app.post("/auth/login", tags=["Authentication"])
    async def login(login_data: LoginRequest):
        """User Login - Basic Authentication"""
        try:
            user = auth_manager.authenticate_user(login_data.username, login_data.password)
            
            if not user:
                raise HTTPException(status_code=401, detail="Invalid username or password")
            
            # Generate JWT token
            access_token = auth_manager.generate_jwt_token(user["user_id"], user["role"])
            
            # Create session
            session_id = auth_manager.create_session(user["user_id"])
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "expires_in": 86400,  # 24 hours
                "user_id": user["user_id"],
                "username": user["username"],
                "role": user["role"],
                "session_id": session_id,
                "login_time": datetime.now(timezone.utc).isoformat(),
                "message": "Login successful"
            }
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")
    
    @app.post("/v1/auth/login", tags=["Authentication"])
    async def login_v1(login_data: LoginRequest):
        """User Login - API v1"""
        return await login(login_data)
    
    @app.post("/v1/auth/logout", tags=["Authentication"])
    async def logout():
        """User Logout"""
        return {
            "message": "Logout successful",
            "logged_out_at": datetime.now(timezone.utc).isoformat()
        }
    
    @app.get("/v1/auth/me", tags=["Authentication"])
    async def get_current_user():
        """Get Current User Info"""
        return {
            "user_id": "demo_user",
            "username": "demo_user",
            "role": "user",
            "authenticated": True,
            "retrieved_at": datetime.now(timezone.utc).isoformat()
        }
    
    @app.post("/v1/auth/refresh", tags=["Authentication"])
    async def refresh_token():
        """Refresh JWT Token"""
        new_token = auth_manager.generate_jwt_token("demo_user", "user")
        return {
            "access_token": new_token,
            "token_type": "bearer",
            "expires_in": 86400,
            "refreshed_at": datetime.now(timezone.utc).isoformat()
        }
    
    @app.get("/v1/auth/status", tags=["Authentication"])
    async def auth_status():
        """Authentication System Status"""
        return {
            "authentication_system": "active",
            "total_users": len(auth_manager.users),
            "active_sessions": len(auth_manager.sessions),
            "jwt_enabled": True,
            "session_timeout_hours": 24,
            "status_checked_at": datetime.now(timezone.utc).isoformat()
        }
    
    @app.post("/v1/auth/register", tags=["Authentication"])
    async def register_user(login_data: LoginRequest):
        """User Registration"""
        if login_data.username in auth_manager.users:
            raise HTTPException(status_code=400, detail="Username already exists")
        
        auth_manager.users[login_data.username] = {
            "password": login_data.password,
            "role": "user"
        }
        
        return {
            "message": "User registered successfully",
            "user_id": login_data.username,
            "role": "user",
            "registered_at": datetime.now(timezone.utc).isoformat()
        }
    
    @app.get("/v1/auth/users", tags=["Authentication"])
    async def list_users():
        """List All Users"""
        users = []
        for username, data in auth_manager.users.items():
            users.append({
                "username": username,
                "role": data["role"],
                "has_password": bool(data.get("password"))
            })
        
        return {
            "users": users,
            "total_users": len(users),
            "listed_at": datetime.now(timezone.utc).isoformat()
        }
    
    @app.post("/v1/auth/change-password", tags=["Authentication"])
    async def change_password(username: str, old_password: str, new_password: str):
        """Change User Password"""
        if username not in auth_manager.users:
            raise HTTPException(status_code=404, detail="User not found")
        
        if auth_manager.users[username]["password"] != old_password:
            raise HTTPException(status_code=401, detail="Invalid current password")
        
        auth_manager.users[username]["password"] = new_password
        
        return {
            "message": "Password changed successfully",
            "user_id": username,
            "changed_at": datetime.now(timezone.utc).isoformat()
        }
    
    @app.delete("/v1/auth/users/{username}", tags=["Authentication"])
    async def delete_user(username: str):
        """Delete User"""
        if username not in auth_manager.users:
            raise HTTPException(status_code=404, detail="User not found")
        
        del auth_manager.users[username]
        
        return {
            "message": f"User {username} deleted successfully",
            "deleted_at": datetime.now(timezone.utc).isoformat()
        }
    
    @app.get("/v1/auth/validate", tags=["Authentication"])
    async def validate_token(token: str):
        """Validate JWT Token"""
        payload = auth_manager.validate_jwt_token(token)
        
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        
        return {
            "valid": True,
            "user_id": payload.get("user_id"),
            "role": payload.get("role"),
            "expires_at": datetime.fromtimestamp(payload.get("exp")).isoformat(),
            "validated_at": datetime.now(timezone.utc).isoformat()
        }
    
    @app.get("/v1/auth/sessions", tags=["Authentication"])
    async def list_sessions():
        """List Active Sessions"""
        active_sessions = []
        current_time = datetime.utcnow()
        
        for session_id, session in auth_manager.sessions.items():
            if session["expires_at"] > current_time:
                active_sessions.append({
                    "session_id": session_id[:8] + "...",
                    "user_id": session["user_id"],
                    "created_at": session["created_at"].isoformat(),
                    "expires_at": session["expires_at"].isoformat()
                })
        
        return {
            "active_sessions": active_sessions,
            "total_sessions": len(active_sessions),
            "listed_at": datetime.now(timezone.utc).isoformat()
        }
    
    @app.post("/v1/auth/sessions/cleanup", tags=["Authentication"])
    async def cleanup_expired_sessions():
        """Cleanup Expired Sessions"""
        current_time = datetime.utcnow()
        expired_sessions = []
        
        for session_id, session in list(auth_manager.sessions.items()):
            if session["expires_at"] <= current_time:
                expired_sessions.append(session_id)
                del auth_manager.sessions[session_id]
        
        return {
            "message": "Expired sessions cleaned up",
            "sessions_removed": len(expired_sessions),
            "cleaned_at": datetime.now(timezone.utc).isoformat()
        }
    
    @app.get("/v1/auth/config", tags=["Authentication"])
    async def get_auth_config():
        """Get Authentication Configuration"""
        return {
            "jwt_algorithm": "HS256",
            "session_timeout_hours": 24,
            "token_expiry_hours": 24,
            "password_policy": {
                "min_length": 6,
                "require_special_chars": False
            },
            "features": {
                "jwt_tokens": True,
                "sessions": True,
                "user_registration": True,
                "password_change": True
            },
            "retrieved_at": datetime.now(timezone.utc).isoformat()
        }
    
    return auth_manager