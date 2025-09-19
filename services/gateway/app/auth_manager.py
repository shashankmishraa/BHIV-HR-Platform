#!/usr/bin/env python3
"""
Enhanced Authentication Manager
Provides comprehensive authentication, session management, and security features
"""

import hashlib
import secrets
import time
import jwt
import pyotp
import qrcode
import io
import base64
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass, field

class UserRole(Enum):
    ADMIN = "admin"
    HR_MANAGER = "hr_manager"
    RECRUITER = "recruiter"
    CLIENT = "client"
    VIEWER = "viewer"

@dataclass
class User:
    user_id: str
    username: str
    email: str
    role: UserRole
    is_active: bool = True
    two_factor_enabled: bool = False
    two_factor_secret: Optional[str] = None
    password_hash: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_login: Optional[datetime] = None
    failed_login_attempts: int = 0
    account_locked_until: Optional[datetime] = None

@dataclass
class Session:
    session_id: str
    user_id: str
    created_at: datetime
    expires_at: datetime
    ip_address: str
    user_agent: str
    is_active: bool = True
    last_activity: Optional[datetime] = None
    session_type: str = "web"
    two_factor_verified: bool = False

@dataclass
class APIKey:
    key_id: str
    api_key: str
    user_id: str
    name: str
    permissions: List[str]
    created_at: datetime
    expires_at: Optional[datetime] = None
    is_active: bool = True
    last_used: Optional[datetime] = None

class AuthManager:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.sessions: Dict[str, Session] = {}
        self.api_keys: Dict[str, APIKey] = {}
        self.password_history: Dict[str, List[Dict[str, Any]]] = {}
        self.jwt_secret = secrets.token_urlsafe(32)
        
        # Initialize with demo users
        self._initialize_demo_users()
    
    def _initialize_demo_users(self):
        """Initialize demo users for testing"""
        demo_users = [
            {
                "user_id": "demo_user",
                "username": "demo_user",
                "email": "demo@bhiv.com",
                "role": UserRole.CLIENT
            },
            {
                "user_id": "admin_user",
                "username": "admin",
                "email": "admin@bhiv.com", 
                "role": UserRole.ADMIN
            },
            {
                "user_id": "hr_manager",
                "username": "hr_manager",
                "email": "hr@bhiv.com",
                "role": UserRole.HR_MANAGER
            }
        ]
        
        for user_data in demo_users:
            user = User(**user_data)
            self.users[user.user_id] = user
    
    def get_user_info(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user information"""
        user = self.users.get(user_id)
        if not user:
            return None
        
        return {
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "role": user.role.value,
            "is_active": user.is_active,
            "two_factor_enabled": user.two_factor_enabled,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "last_login": user.last_login.isoformat() if user.last_login else None
        }
    
    def setup_2fa(self, user_id: str) -> Dict[str, Any]:
        """Setup 2FA for user"""
        user = self.users.get(user_id)
        if not user:
            raise ValueError("User not found")
        
        # Generate secret
        secret = pyotp.random_base32()
        user.two_factor_secret = secret
        
        # Generate QR code
        totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=user.email,
            issuer_name="BHIV HR Platform"
        )
        
        # Create QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(totp_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        qr_code_b64 = base64.b64encode(img_buffer.getvalue()).decode()
        
        # Generate backup codes
        backup_codes = [f"BACKUP-{secrets.token_hex(4).upper()}" for _ in range(10)]
        
        return {
            "secret": secret,
            "qr_code": f"data:image/png;base64,{qr_code_b64}",
            "manual_entry_key": secret,
            "backup_codes": backup_codes,
            "setup_complete": False
        }
    
    def verify_2fa_setup(self, user_id: str, token: str) -> bool:
        """Verify 2FA setup token"""
        user = self.users.get(user_id)
        if not user or not user.two_factor_secret:
            return False
        
        totp = pyotp.TOTP(user.two_factor_secret)
        if totp.verify(token, valid_window=1):
            user.two_factor_enabled = True
            return True
        return False
    
    def verify_2fa_token(self, user_id: str, token: str) -> bool:
        """Verify 2FA token for login"""
        user = self.users.get(user_id)
        if not user or not user.two_factor_enabled or not user.two_factor_secret:
            return False
        
        totp = pyotp.TOTP(user.two_factor_secret)
        return totp.verify(token, valid_window=1)
    
    def disable_2fa(self, user_id: str) -> bool:
        """Disable 2FA for user"""
        user = self.users.get(user_id)
        if not user:
            return False
        
        user.two_factor_enabled = False
        user.two_factor_secret = None
        return True
    
    def create_session(self, user_id: str, ip_address: str = "unknown", user_agent: str = "unknown") -> str:
        """Create new session"""
        session_id = secrets.token_urlsafe(32)
        current_time = datetime.now(timezone.utc)
        
        session = Session(
            session_id=session_id,
            user_id=user_id,
            created_at=current_time,
            expires_at=current_time + timedelta(hours=24),
            ip_address=ip_address,
            user_agent=user_agent,
            last_activity=current_time
        )
        
        self.sessions[session_id] = session
        
        # Update user last login
        user = self.users.get(user_id)
        if user:
            user.last_login = current_time
        
        return session_id
    
    def invalidate_session(self, session_id: str) -> bool:
        """Invalidate session"""
        session = self.sessions.get(session_id)
        if session:
            session.is_active = False
            return True
        return False
    
    def generate_jwt_token(self, user_id: str, permissions: List[str]) -> str:
        """Generate JWT token"""
        user = self.users.get(user_id)
        if not user:
            raise ValueError("User not found")
        
        payload = {
            "user_id": user_id,
            "username": user.username,
            "role": user.role.value,
            "permissions": permissions,
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(hours=24)
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
    
    def generate_api_key(self, user_id: str, name: str, permissions: List[str]) -> Dict[str, Any]:
        """Generate API key"""
        key_id = f"key_{secrets.token_hex(8)}"
        api_key = f"bhiv_{secrets.token_urlsafe(32)}"
        current_time = datetime.now(timezone.utc)
        
        api_key_obj = APIKey(
            key_id=key_id,
            api_key=api_key,
            user_id=user_id,
            name=name,
            permissions=permissions,
            created_at=current_time,
            expires_at=current_time + timedelta(days=90)
        )
        
        self.api_keys[key_id] = api_key_obj
        
        return {
            "key_id": key_id,
            "api_key": api_key,
            "name": name,
            "permissions": permissions,
            "created_at": current_time.isoformat(),
            "expires_at": api_key_obj.expires_at.isoformat() if api_key_obj.expires_at else None
        }
    
    def list_api_keys(self, user_id: str) -> List[Dict[str, Any]]:
        """List API keys for user"""
        user_keys = []
        for key_id, api_key in self.api_keys.items():
            if api_key.user_id == user_id:
                user_keys.append({
                    "key_id": key_id,
                    "name": api_key.name,
                    "permissions": api_key.permissions,
                    "created_at": api_key.created_at.isoformat(),
                    "expires_at": api_key.expires_at.isoformat() if api_key.expires_at else None,
                    "is_active": api_key.is_active,
                    "last_used": api_key.last_used.isoformat() if api_key.last_used else None
                })
        return user_keys
    
    def revoke_api_key(self, key_id: str) -> bool:
        """Revoke API key"""
        api_key = self.api_keys.get(key_id)
        if api_key:
            api_key.is_active = False
            return True
        return False
    
    def get_password_history(self, user_id: str) -> List[Dict[str, Any]]:
        """Get password history for user"""
        return self.password_history.get(user_id, [])
    
    def reset_password(self, user_id: str, new_password: str, force_change: bool = True, reset_reason: str = "user_request") -> bool:
        """Reset user password"""
        user = self.users.get(user_id)
        if not user:
            return False
        
        # Hash new password
        password_hash = hashlib.sha256(new_password.encode()).hexdigest()
        
        # Store in password history
        if user_id not in self.password_history:
            self.password_history[user_id] = []
        
        self.password_history[user_id].append({
            "hash": password_hash,
            "changed_at": datetime.now(timezone.utc).isoformat(),
            "reason": reset_reason,
            "ip_address": "system",
            "user_agent": "admin_reset"
        })
        
        # Keep only last 12 passwords
        self.password_history[user_id] = self.password_history[user_id][-12:]
        
        user.password_hash = password_hash
        return True
    
    def optimize_session_storage(self):
        """Optimize session storage by removing expired sessions"""
        current_time = datetime.now(timezone.utc)
        expired_sessions = []
        
        for session_id, session in self.sessions.items():
            if session.expires_at <= current_time or not session.is_active:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            del self.sessions[session_id]

# Global auth manager instance
auth_manager = AuthManager()