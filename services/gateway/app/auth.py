# Authentication Module
# Extracted from main.py for modular architecture

from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, HTTPException, Depends, Request, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional
import secrets
import time

router = APIRouter()
security = HTTPBearer()

# Authentication Models
class LoginRequest(BaseModel):
    username: str
    password: str

class TwoFASetup(BaseModel):
    user_id: str

class TwoFALogin(BaseModel):
    user_id: str
    totp_code: str

class ClientLogin(BaseModel):
    client_id: str
    password: str

class PasswordValidation(BaseModel):
    password: str

class EmailValidation(BaseModel):
    email: str

class PhoneValidation(BaseModel):
    phone: str

# Simple Authentication Manager
class SimpleAuthManager:
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
    
    def authenticate_user(self, username: str, password: str):
        if username in self.users and self.users[username]["password"] == password:
            return {
                "user_id": username,
                "username": username,
                "role": self.users[username]["role"],
                "authenticated": True
            }
        return None
    
    def generate_jwt_token(self, user_id: str, role: str = "user") -> str:
        try:
            import jwt
            payload = {
                "user_id": user_id,
                "role": role,
                "exp": datetime.utcnow() + timedelta(hours=24),
                "iat": datetime.utcnow()
            }
            return jwt.encode(payload, self.jwt_secret, algorithm="HS256")
        except ImportError:
            return f"token_{user_id}_{int(time.time())}"

simple_auth = SimpleAuthManager()

def get_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """API Key Authentication"""
    if not credentials:
        raise HTTPException(status_code=401, detail="API key required")
    return credentials.credentials

# Authentication Endpoints
@router.post("/auth/login", tags=["Authentication"])
@router.get("/auth/login", tags=["Authentication"])
async def login(login_data: LoginRequest = None, username: str = None, password: str = None):
    """User Login - Basic Authentication"""
    try:
        if not login_data and username and password:
            login_data = LoginRequest(username=username, password=password)
        
        if not login_data:
            return {
                "message": "Login endpoint active",
                "methods": ["GET", "POST"],
                "demo_credentials": {"username": "TECH001", "password": "demo123"}
            }
        
        user = simple_auth.authenticate_user(login_data.username, login_data.password)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        
        access_token = simple_auth.generate_jwt_token(user["user_id"], user["role"])
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": 86400,
            "user_id": user["user_id"],
            "username": user["username"],
            "role": user["role"],
            "login_time": datetime.now(timezone.utc).isoformat(),
            "message": "Login successful"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

@router.post("/v1/auth/login", tags=["Authentication"])
@router.get("/v1/auth/login", tags=["Authentication"])
async def login_v1(login_data: LoginRequest = None, username: str = None, password: str = None):
    """User Login - API v1"""
    return await login(login_data, username, password)

@router.post("/v1/auth/logout", tags=["Authentication"])
async def logout():
    """User Logout"""
    return {
        "message": "Logout successful",
        "logged_out_at": datetime.now(timezone.utc).isoformat()
    }

@router.get("/v1/auth/me", tags=["Authentication"])
async def get_current_user():
    """Get Current User Info"""
    return {
        "user_id": "demo_user",
        "username": "demo_user",
        "role": "user",
        "authenticated": True,
        "retrieved_at": datetime.now(timezone.utc).isoformat()
    }

@router.post("/v1/auth/refresh", tags=["Authentication"])
async def refresh_token():
    """Refresh JWT Token"""
    new_token = simple_auth.generate_jwt_token("demo_user", "user")
    return {
        "access_token": new_token,
        "token_type": "bearer",
        "expires_in": 86400,
        "refreshed_at": datetime.now(timezone.utc).isoformat()
    }

@router.get("/v1/auth/status", tags=["Authentication"])
async def auth_status_simple():
    """Authentication System Status"""
    return {
        "authentication_system": "active",
        "total_users": len(simple_auth.users),
        "active_sessions": len(simple_auth.sessions),
        "jwt_enabled": True,
        "session_timeout_hours": 24,
        "status_checked_at": datetime.now(timezone.utc).isoformat()
    }

@router.post("/v1/auth/2fa/setup", tags=["Two-Factor Authentication"])
async def setup_2fa_for_user(setup_data: TwoFASetup, api_key: str = Depends(get_api_key)):
    """Setup 2FA for User"""
    try:
        import pyotp
        import qrcode
        import io
        import base64
        
        secret = pyotp.random_base32()
        totp = pyotp.TOTP(secret)
        
        # Generate QR code
        provisioning_uri = totp.provisioning_uri(
            name=setup_data.user_id,
            issuer_name="BHIV HR Platform"
        )
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(provisioning_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG')
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        
        return {
            "message": "2FA setup initiated successfully",
            "user_id": setup_data.user_id,
            "secret": secret,
            "qr_code": f"data:image/png;base64,{img_str}",
            "manual_entry_key": secret,
            "backup_codes": [secrets.token_hex(4) for _ in range(10)],
            "setup_at": datetime.now(timezone.utc).isoformat()
        }
    except ImportError:
        return {
            "message": "2FA libraries not available",
            "user_id": setup_data.user_id,
            "fallback_mode": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"2FA setup failed: {str(e)}")

@router.post("/v1/client/login", tags=["Client Portal API"])
async def client_login(login_data: ClientLogin):
    """Client Authentication"""
    try:
        valid_clients = {
            "TECH001": "demo123",
            "STARTUP01": "startup123",
            "ENTERPRISE01": "enterprise123"
        }
        
        if login_data.client_id in valid_clients and valid_clients[login_data.client_id] == login_data.password:
            return {
                "message": "Authentication successful",
                "client_id": login_data.client_id,
                "access_token": f"client_token_{login_data.client_id}_{datetime.now().timestamp()}",
                "token_type": "bearer",
                "expires_in": 3600,
                "permissions": ["view_jobs", "create_jobs", "view_candidates", "schedule_interviews"]
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid client credentials")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Authentication system error")

@router.post("/v1/password/reset", tags=["Password Management"])
async def reset_password(email_data: EmailValidation, api_key: str = Depends(get_api_key)):
    """Password Reset Functionality"""
    email = email_data.email
    reset_token = secrets.token_urlsafe(32)
    
    return {
        "message": "Password reset initiated",
        "email": email,
        "reset_token": reset_token,
        "expires_in": "1 hour",
        "reset_link": f"https://bhiv-hr-platform.com/reset-password?token={reset_token}",
        "initiated_at": datetime.now(timezone.utc).isoformat()
    }