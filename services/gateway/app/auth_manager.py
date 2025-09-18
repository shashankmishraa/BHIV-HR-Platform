"""
Advanced Authentication Manager
Handles 2FA, API key management, and session management
"""

import secrets
import hashlib
import pyotp
import qrcode
import io
import base64
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import json
import jwt

class AuthenticationMethod(Enum):
    API_KEY = "api_key"
    JWT_TOKEN = "jwt_token"
    TWO_FACTOR = "2fa"
    SESSION = "session"

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
    created_at: datetime = None
    last_login: Optional[datetime] = None

@dataclass
class APIKey:
    key_id: str
    key_hash: str
    name: str
    user_id: str
    permissions: List[str]
    created_at: datetime
    expires_at: Optional[datetime] = None
    last_used: Optional[datetime] = None
    is_active: bool = True

@dataclass
class Session:
    session_id: str
    user_id: str
    created_at: datetime
    expires_at: datetime
    ip_address: str
    user_agent: str
    is_active: bool = True

class AuthenticationManager:
    """Comprehensive authentication management system"""
    
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.api_keys: Dict[str, APIKey] = {}
        self.sessions: Dict[str, Session] = {}
        self.jwt_secret = secrets.token_urlsafe(32)
        self.session_timeout = timedelta(hours=24)
        self.api_key_timeout = timedelta(days=90)
        
        # Initialize demo users
        self._initialize_demo_users()
    
    def _initialize_demo_users(self):
        """Initialize demo users for testing"""
        demo_users = [
            User(
                user_id="user_001",
                username="admin",
                email="admin@bhiv.com",
                role=UserRole.ADMIN,
                created_at=datetime.now(timezone.utc)
            ),
            User(
                user_id="user_002", 
                username="hr_manager",
                email="hr@bhiv.com",
                role=UserRole.HR_MANAGER,
                created_at=datetime.now(timezone.utc)
            ),
            User(
                user_id="user_003",
                username="TECH001",
                email="tech001@client.com",
                role=UserRole.CLIENT,
                created_at=datetime.now(timezone.utc)
            )
        ]
        
        for user in demo_users:
            self.users[user.user_id] = user
    
    def setup_2fa(self, user_id: str) -> Dict[str, Any]:
        """Setup 2FA for a user"""
        if user_id not in self.users:
            raise ValueError("User not found")
        
        user = self.users[user_id]
        
        # Generate secret
        secret = pyotp.random_base32()
        user.two_factor_secret = secret
        
        # Generate QR code
        totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=user.email,
            issuer_name="BHIV HR Platform"
        )
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(totp_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG')
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        
        return {
            "user_id": user_id,
            "secret": secret,
            "qr_code": f"data:image/png;base64,{img_str}",
            "manual_entry_key": secret,
            "backup_codes": self._generate_backup_codes(),
            "setup_complete": False
        }
    
    def verify_2fa_setup(self, user_id: str, token: str) -> bool:
        """Verify 2FA setup with token"""
        if user_id not in self.users:
            return False
        
        user = self.users[user_id]
        if not user.two_factor_secret:
            return False
        
        totp = pyotp.TOTP(user.two_factor_secret)
        if totp.verify(token, valid_window=1):
            user.two_factor_enabled = True
            return True
        
        return False
    
    def verify_2fa_token(self, user_id: str, token: str) -> bool:
        """Verify 2FA token for authentication"""
        if user_id not in self.users:
            return False
        
        user = self.users[user_id]
        if not user.two_factor_enabled or not user.two_factor_secret:
            return False
        
        totp = pyotp.TOTP(user.two_factor_secret)
        return totp.verify(token, valid_window=1)
    
    def disable_2fa(self, user_id: str) -> bool:
        """Disable 2FA for a user"""
        if user_id not in self.users:
            return False
        
        user = self.users[user_id]
        user.two_factor_enabled = False
        user.two_factor_secret = None
        return True
    
    def generate_api_key(self, user_id: str, name: str, permissions: List[str] = None) -> Dict[str, Any]:
        """Generate new API key for user"""
        if user_id not in self.users:
            raise ValueError("User not found")
        
        # Generate key
        api_key = secrets.token_urlsafe(32)
        key_id = f"key_{secrets.token_hex(8)}"
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        # Create API key record
        api_key_record = APIKey(
            key_id=key_id,
            key_hash=key_hash,
            name=name,
            user_id=user_id,
            permissions=permissions or ["read", "write"],
            created_at=datetime.now(timezone.utc),
            expires_at=datetime.now(timezone.utc) + self.api_key_timeout
        )
        
        self.api_keys[key_id] = api_key_record
        
        return {
            "key_id": key_id,
            "api_key": api_key,
            "name": name,
            "permissions": api_key_record.permissions,
            "expires_at": api_key_record.expires_at.isoformat(),
            "created_at": api_key_record.created_at.isoformat()
        }
    
    def validate_api_key(self, api_key: str) -> Optional[Dict[str, Any]]:
        """Validate API key and return metadata"""
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        for key_record in self.api_keys.values():
            if (key_record.key_hash == key_hash and 
                key_record.is_active and
                (not key_record.expires_at or key_record.expires_at > datetime.now(timezone.utc))):
                
                # Update last used
                key_record.last_used = datetime.now(timezone.utc)
                
                return {
                    "key_id": key_record.key_id,
                    "user_id": key_record.user_id,
                    "permissions": key_record.permissions,
                    "name": key_record.name
                }
        
        return None
    
    def list_api_keys(self, user_id: str) -> List[Dict[str, Any]]:
        """List API keys for user"""
        user_keys = []
        for key_record in self.api_keys.values():
            if key_record.user_id == user_id and key_record.is_active:
                user_keys.append({
                    "key_id": key_record.key_id,
                    "name": key_record.name,
                    "permissions": key_record.permissions,
                    "created_at": key_record.created_at.isoformat(),
                    "expires_at": key_record.expires_at.isoformat() if key_record.expires_at else None,
                    "last_used": key_record.last_used.isoformat() if key_record.last_used else None
                })
        
        return user_keys
    
    def revoke_api_key(self, key_id: str) -> bool:
        """Revoke API key"""
        if key_id in self.api_keys:
            self.api_keys[key_id].is_active = False
            return True
        return False
    
    def create_session(self, user_id: str, ip_address: str, user_agent: str) -> str:
        """Create new session"""
        if user_id not in self.users:
            raise ValueError("User not found")
        
        session_id = secrets.token_urlsafe(32)
        session = Session(
            session_id=session_id,
            user_id=user_id,
            created_at=datetime.now(timezone.utc),
            expires_at=datetime.now(timezone.utc) + self.session_timeout,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        self.sessions[session_id] = session
        
        # Update user last login
        self.users[user_id].last_login = datetime.now(timezone.utc)
        
        return session_id
    
    def validate_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Validate session"""
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        
        if (session.is_active and 
            session.expires_at > datetime.now(timezone.utc)):
            
            return {
                "session_id": session_id,
                "user_id": session.user_id,
                "created_at": session.created_at.isoformat(),
                "expires_at": session.expires_at.isoformat(),
                "ip_address": session.ip_address
            }
        
        return None
    
    def invalidate_session(self, session_id: str) -> bool:
        """Invalidate session"""
        if session_id in self.sessions:
            self.sessions[session_id].is_active = False
            return True
        return False
    
    def generate_jwt_token(self, user_id: str, permissions: List[str] = None) -> str:
        """Generate JWT token"""
        if user_id not in self.users:
            raise ValueError("User not found")
        
        user = self.users[user_id]
        payload = {
            "user_id": user_id,
            "username": user.username,
            "role": user.role.value,
            "permissions": permissions or ["read"],
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
    
    def _generate_backup_codes(self) -> List[str]:
        """Generate backup codes for 2FA"""
        return [f"BACKUP-{secrets.token_hex(4).upper()}" for _ in range(10)]
    
    def get_user_info(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user information"""
        if user_id not in self.users:
            return None
        
        user = self.users[user_id]
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

# Global authentication manager instance
auth_manager = AuthenticationManager()