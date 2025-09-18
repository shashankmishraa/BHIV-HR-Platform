"""
BHIV HR Platform - Enhanced Security Configuration
Addresses: CORS Configuration, Cookie Security, API Key Management
"""

from datetime import datetime, timedelta, timezone
from typing import List, Dict, Optional, Set
import hashlib
import json
import os
import secrets
import time

from cryptography.fernet import Fernet
from dataclasses import dataclass
from enum import Enum
import jwt
import redis
class SecurityLevel(Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

@dataclass
class CORSConfig:
    """Secure CORS Configuration"""
    allowed_origins: List[str]
    allowed_methods: List[str]
    allowed_headers: List[str]
    allow_credentials: bool
    max_age: int

@dataclass
class CookieConfig:
    """Secure Cookie Configuration"""
    secure: bool
    httponly: bool
    samesite: str
    max_age: int
    domain: Optional[str]
    path: str

@dataclass
class APIKeyConfig:
    """API Key Management Configuration"""
    key_length: int
    rotation_interval_days: int
    max_active_keys: int
    hash_algorithm: str
    encryption_enabled: bool

class SecurityConfigManager:
    """Enterprise Security Configuration Manager"""
    
    def __init__(self, environment: str = None):
        self.environment = SecurityLevel(environment or os.getenv("ENVIRONMENT", "production"))
        self.redis_client = self._init_redis()
        self.encryption_key = self._get_encryption_key()
        self.cipher_suite = Fernet(self.encryption_key) if self.encryption_key else None
        
    def _init_redis(self) -> Optional[redis.Redis]:
        """Initialize Redis connection for session management"""
        try:
            redis_url = os.getenv("REDIS_URL")
            if redis_url:
                return redis.from_url(redis_url, decode_responses=True)
            return None
        except Exception:
            return None
    
    def _get_encryption_key(self) -> Optional[bytes]:
        """Get or generate encryption key for sensitive data"""
        key = os.getenv("ENCRYPTION_KEY")
        if key:
            return key.encode()
        # Generate new key for development
        if self.environment == SecurityLevel.DEVELOPMENT:
            return Fernet.generate_key()
        return None
    
    def get_cors_config(self) -> CORSConfig:
        """Get environment-specific CORS configuration"""
        if self.environment == SecurityLevel.PRODUCTION:
            return CORSConfig(
                allowed_origins=[
                    "https://bhiv-hr-portal.onrender.com",
                    "https://bhiv-hr-client-portal.onrender.com",
                    "https://bhiv-hr-gateway.onrender.com",
                    os.getenv("FRONTEND_URL", "https://app.bhiv.com")
                ],
                allowed_methods=["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"],
                allowed_headers=[
                    "Authorization",
                    "Content-Type", 
                    "X-Requested-With",
                    "X-API-Key",
                    "X-Correlation-ID"
                ],
                allow_credentials=True,
                max_age=86400  # 24 hours
            )
        elif self.environment == SecurityLevel.STAGING:
            return CORSConfig(
                allowed_origins=[
                    "https://staging.bhiv.com",
                    "https://bhiv-hr-portal.onrender.com",
                    "https://bhiv-hr-client-portal.onrender.com"
                ],
                allowed_methods=["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"],
                allowed_headers=["Authorization", "Content-Type", "X-Requested-With"],
                allow_credentials=True,
                max_age=3600  # 1 hour
            )
        else:  # Development
            return CORSConfig(
                allowed_origins=["http://localhost:3000", "http://localhost:8501", "http://localhost:8502"],
                allowed_methods=["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"],
                allowed_headers=["*"],
                allow_credentials=True,
                max_age=300  # 5 minutes
            )
    
    def get_cookie_config(self) -> CookieConfig:
        """Get secure cookie configuration"""
        is_production = self.environment == SecurityLevel.PRODUCTION
        
        return CookieConfig(
            secure=is_production,  # HTTPS only in production
            httponly=True,  # Prevent XSS access
            samesite="strict" if is_production else "lax",
            max_age=3600,  # 1 hour
            domain=os.getenv("COOKIE_DOMAIN") if is_production else None,
            path="/"
        )
    
    def get_api_key_config(self) -> APIKeyConfig:
        """Get API key management configuration"""
        return APIKeyConfig(
            key_length=32,
            rotation_interval_days=30,
            max_active_keys=5,
            hash_algorithm="sha256",
            encryption_enabled=True
        )

class APIKeyManager:
    """Enterprise API Key Management System"""
    
    def __init__(self, config_manager: SecurityConfigManager):
        self.config_manager = config_manager
        self.config = config_manager.get_api_key_config()
        self.redis_client = config_manager.redis_client
        
    def generate_api_key(self, client_id: str, permissions: List[str] = None) -> Dict:
        """Generate new API key with metadata"""
        key = secrets.token_urlsafe(self.config.key_length)
        key_id = secrets.token_hex(8)
        
        metadata = {
            "key_id": key_id,
            "client_id": client_id,
            "permissions": permissions or ["read"],
            "created_at": datetime.now(timezone.utc).isoformat(),
            "expires_at": (datetime.now(timezone.utc) + timedelta(days=self.config.rotation_interval_days)).isoformat(),
            "is_active": True,
            "usage_count": 0,
            "last_used": None
        }
        
        # Hash the key for storage
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        
        # Store in Redis if available
        if self.redis_client:
            self.redis_client.setex(
                f"api_key:{key_hash}",
                timedelta(days=self.config.rotation_interval_days).total_seconds(),
                json.dumps(metadata)
            )
            
            # Track active keys for client
            self.redis_client.sadd(f"client_keys:{client_id}", key_hash)
        
        return {
            "api_key": key,
            "key_id": key_id,
            "expires_at": metadata["expires_at"],
            "permissions": metadata["permissions"]
        }
    
    def validate_api_key(self, api_key: str) -> Optional[Dict]:
        """Validate API key and return metadata"""
        if not api_key:
            return None
            
        # Check static fallback key for development
        static_key = os.getenv("API_KEY_SECRET", "myverysecureapikey123")
        if api_key == static_key:
            return {
                "client_id": "static_client",
                "permissions": ["admin"],
                "key_type": "static",
                "valid": True
            }
        
        # Check dynamic keys in Redis
        if self.redis_client:
            key_hash = hashlib.sha256(api_key.encode()).hexdigest()
            metadata_json = self.redis_client.get(f"api_key:{key_hash}")
            
            if metadata_json:
                metadata = json.loads(metadata_json)
                
                # Update usage statistics
                metadata["usage_count"] += 1
                metadata["last_used"] = datetime.now(timezone.utc).isoformat()
                
                self.redis_client.setex(
                    f"api_key:{key_hash}",
                    timedelta(days=self.config.rotation_interval_days).total_seconds(),
                    json.dumps(metadata)
                )
                
                return metadata
        
        return None
    
    def rotate_api_keys(self, client_id: str) -> Dict:
        """Rotate API keys for a client"""
        if not self.redis_client:
            return {"error": "Key rotation requires Redis"}
        
        # Get current active keys
        current_keys = self.redis_client.smembers(f"client_keys:{client_id}")
        
        # Deactivate old keys (keep for grace period)
        for key_hash in current_keys:
            metadata_json = self.redis_client.get(f"api_key:{key_hash}")
            if metadata_json:
                metadata = json.loads(metadata_json)
                metadata["is_active"] = False
                metadata["deactivated_at"] = datetime.now(timezone.utc).isoformat()
                
                # Keep for 7 days grace period
                self.redis_client.setex(
                    f"api_key:{key_hash}",
                    timedelta(days=7).total_seconds(),
                    json.dumps(metadata)
                )
        
        # Generate new key
        new_key_data = self.generate_api_key(client_id)
        
        return {
            "message": "API keys rotated successfully",
            "new_key": new_key_data,
            "rotated_keys_count": len(current_keys),
            "grace_period_days": 7
        }
    
    def revoke_api_key(self, key_id: str) -> bool:
        """Revoke specific API key"""
        if not self.redis_client:
            return False
        
        # Find and revoke key
        for key in self.redis_client.scan_iter(match="api_key:*"):
            metadata_json = self.redis_client.get(key)
            if metadata_json:
                metadata = json.loads(metadata_json)
                if metadata.get("key_id") == key_id:
                    self.redis_client.delete(key)
                    return True
        
        return False

class SessionManager:
    """Secure Session Management with Cookie Security"""
    
    def __init__(self, config_manager: SecurityConfigManager):
        self.config_manager = config_manager
        self.cookie_config = config_manager.get_cookie_config()
        self.redis_client = config_manager.redis_client
        
    def create_session(self, user_id: str, user_data: Dict) -> str:
        """Create secure session with encrypted cookie"""
        session_id = secrets.token_urlsafe(32)
        
        session_data = {
            "user_id": user_id,
            "user_data": user_data,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "expires_at": (datetime.now(timezone.utc) + timedelta(seconds=self.cookie_config.max_age)).isoformat(),
            "ip_address": None,  # Set by middleware
            "user_agent": None   # Set by middleware
        }
        
        # Store in Redis if available
        if self.redis_client:
            self.redis_client.setex(
                f"session:{session_id}",
                self.cookie_config.max_age,
                json.dumps(session_data)
            )
        
        return session_id
    
    def validate_session(self, session_id: str) -> Optional[Dict]:
        """Validate session and return user data"""
        if not session_id or not self.redis_client:
            return None
        
        session_data_json = self.redis_client.get(f"session:{session_id}")
        if session_data_json:
            return json.loads(session_data_json)
        
        return None
    
    def invalidate_session(self, session_id: str) -> bool:
        """Invalidate session"""
        if self.redis_client:
            return bool(self.redis_client.delete(f"session:{session_id}"))
        return False
    
    def get_cookie_headers(self, session_id: str) -> Dict[str, str]:
        """Get secure cookie headers"""
        cookie_value = f"session_id={session_id}"
        
        # Add security attributes
        attributes = []
        if self.cookie_config.secure:
            attributes.append("Secure")
        if self.cookie_config.httponly:
            attributes.append("HttpOnly")
        if self.cookie_config.samesite:
            attributes.append(f"SameSite={self.cookie_config.samesite}")
        if self.cookie_config.max_age:
            attributes.append(f"Max-Age={self.cookie_config.max_age}")
        if self.cookie_config.domain:
            attributes.append(f"Domain={self.cookie_config.domain}")
        if self.cookie_config.path:
            attributes.append(f"Path={self.cookie_config.path}")
        
        if attributes:
            cookie_value += "; " + "; ".join(attributes)
        
        return {"Set-Cookie": cookie_value}

# Global security manager instance
security_manager = SecurityConfigManager()
api_key_manager = APIKeyManager(security_manager)
session_manager = SessionManager(security_manager)