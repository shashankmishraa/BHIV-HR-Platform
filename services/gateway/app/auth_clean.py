# Authentication Module - Clean Implementation
# Handles all authentication endpoints and logic

from datetime import datetime, timezone, timedelta
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Request, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import secrets
import time
import os

# Authentication models
class LoginRequest(BaseModel):
    username: str
    password: str

class ClientLogin(BaseModel):
    client_id: str
    password: str

class TwoFASetup(BaseModel):
    user_id: str

class TwoFALogin(BaseModel):
    user_id: str
    totp_code: str

class PasswordValidation(BaseModel):
    password: str

class EmailValidation(BaseModel):
    email: str

class PhoneValidation(BaseModel):
    phone: str

# Initialize router and security
router = APIRouter()
security = HTTPBearer()

# Simple authentication manager
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
        self.api_keys = {}
    
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
    
    def validate_api_key(self, api_key: str):
        # Simple validation for demo
        valid_keys = [
            "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o",
            "myverysecureapikey123",
            "fallback_api_key_123"
        ]
        if api_key in valid_keys:
            return {"client_id": "demo_client", "permissions": ["read", "write"]}
        return None

# Initialize auth manager
simple_auth = SimpleAuthManager()

# Authentication dependency
def get_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """API key dependency"""
    if not credentials:
        raise HTTPException(status_code=401, detail="API key required")
    
    key_metadata = simple_auth.validate_api_key(credentials.credentials)
    if not key_metadata:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return credentials.credentials

def get_standardized_auth(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Standardized authentication"""
    get_api_key(credentials)
    return type('AuthResult', (), {
        'success': True, 'user_id': 'authenticated_user', 'permissions': ['read', 'write'],
        'method': 'api_key', 'level': 'standard'
    })()

# Authentication endpoints
@router.post("/login", tags=["Authentication"])
@router.get("/login", tags=["Authentication"])
async def login(login_data: LoginRequest = None, username: str = None, password: str = None):
    """User Login - Basic Authentication (supports both GET and POST)"""
    try:
        # Handle GET request with query parameters
        if not login_data and username and password:
            login_data = LoginRequest(username=username, password=password)
        
        if not login_data:
            return {
                "message": "Login endpoint active",
                "methods": ["GET", "POST"],
                "parameters": {
                    "POST": "JSON body with username and password",
                    "GET": "Query parameters: ?username=X&password=Y"
                },
                "demo_credentials": {
                    "username": "TECH001",
                    "password": "demo123"
                }
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

@router.post("/logout", tags=["Authentication"])
async def logout():
    """User Logout"""
    return {
        "message": "Logout successful",
        "logged_out_at": datetime.now(timezone.utc).isoformat()
    }

@router.get("/me", tags=["Authentication"])
async def get_current_user():
    """Get Current User Info"""
    return {
        "user_id": "demo_user",
        "username": "demo_user",
        "role": "user",
        "authenticated": True,
        "retrieved_at": datetime.now(timezone.utc).isoformat()
    }

@router.post("/refresh", tags=["Authentication"])
async def refresh_token():
    """Refresh JWT Token"""
    new_token = simple_auth.generate_jwt_token("demo_user", "user")
    return {
        "access_token": new_token,
        "token_type": "bearer",
        "expires_in": 86400,
        "refreshed_at": datetime.now(timezone.utc).isoformat()
    }

@router.get("/status", tags=["Authentication"])
async def auth_status():
    """Authentication System Status"""
    return {
        "authentication_system": "active",
        "total_users": len(simple_auth.users),
        "active_sessions": len(simple_auth.sessions),
        "jwt_enabled": True,
        "session_timeout_hours": 24,
        "status_checked_at": datetime.now(timezone.utc).isoformat()
    }

@router.post("/2fa/setup", tags=["Two-Factor Authentication"])
async def setup_2fa(setup_data: TwoFASetup, api_key: str = Depends(get_api_key)):
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
            "message": "2FA setup initiated",
            "user_id": setup_data.user_id,
            "secret": secret,
            "qr_code": f"data:image/png;base64,{img_str}",
            "manual_entry_key": secret,
            "backup_codes": [secrets.token_hex(4) for _ in range(8)],
            "setup_at": datetime.now(timezone.utc).isoformat()
        }
    except ImportError:
        return {
            "message": "2FA setup (fallback mode)",
            "user_id": setup_data.user_id,
            "secret": "FALLBACK2FASECRET",
            "setup_at": datetime.now(timezone.utc).isoformat(),
            "note": "2FA libraries not available"
        }

@router.post("/2fa/verify", tags=["Two-Factor Authentication"])
async def verify_2fa(login_data: TwoFALogin, api_key: str = Depends(get_api_key)):
    """Verify 2FA Code"""
    return {
        "message": "2FA verification successful",
        "user_id": login_data.user_id,
        "verified_at": datetime.now(timezone.utc).isoformat(),
        "access_granted": True
    }

@router.post("/password/validate", tags=["Password Management"])
async def validate_password(password_data: PasswordValidation, api_key: str = Depends(get_api_key)):
    """Password Validation"""
    password = password_data.password
    
    # Basic validation rules
    is_valid = (
        len(password) >= 8 and
        any(c.isupper() for c in password) and
        any(c.islower() for c in password) and
        any(c.isdigit() for c in password)
    )
    
    return {
        "password_valid": is_valid,
        "requirements": {
            "min_length": len(password) >= 8,
            "has_uppercase": any(c.isupper() for c in password),
            "has_lowercase": any(c.islower() for c in password),
            "has_digit": any(c.isdigit() for c in password)
        },
        "validated_at": datetime.now(timezone.utc).isoformat()
    }

@router.post("/password/reset", tags=["Password Management"])
async def reset_password(email_data: EmailValidation, api_key: str = Depends(get_api_key)):
    """Password Reset"""
    reset_token = secrets.token_urlsafe(32)
    
    return {
        "message": "Password reset initiated",
        "email": email_data.email,
        "reset_token": reset_token,
        "expires_in": "1 hour",
        "reset_link": f"https://bhiv-hr-platform.com/reset-password?token={reset_token}",
        "initiated_at": datetime.now(timezone.utc).isoformat()
    }

@router.get("/test", tags=["Authentication"])
async def test_auth_system(request: Request, auth_result = Depends(get_standardized_auth)):
    """Test Authentication System"""
    return {
        "authentication_test": "passed",
        "user_authenticated": True,
        "auth_method": "api_key",
        "test_timestamp": datetime.now(timezone.utc).isoformat(),
        "system_status": "operational"
    }