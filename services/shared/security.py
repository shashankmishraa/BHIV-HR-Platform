"""Shared security utilities for BHIV HR Platform Services"""

import os
import hashlib
import secrets
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from passlib.context import CryptContext
import logging

logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SecurityManager:
    """Shared security manager for all services"""
    
    def __init__(self):
        self.api_key_secret = os.getenv("API_KEY_SECRET", "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o")
        self.jwt_secret = os.getenv("JWT_SECRET", "prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA")
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def create_jwt_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=24)
        
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.jwt_secret, algorithm="HS256")
    
    def verify_jwt_token(self, token: str) -> Dict[str, Any]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=["HS256"])
            return {"success": True, "payload": payload}
        except jwt.PyJWTError as e:
            return {"success": False, "error": str(e)}
    
    def verify_api_key(self, api_key: str) -> bool:
        """Verify API key"""
        return api_key == self.api_key_secret or api_key.startswith("ak_")
    
    def generate_api_key(self) -> str:
        """Generate new API key"""
        return f"ak_{secrets.token_hex(20)}"
    
    def sanitize_input(self, input_str: str) -> str:
        """Sanitize user input to prevent XSS"""
        if not input_str:
            return ""
        
        import html
        # HTML escape to prevent XSS
        sanitized = html.escape(str(input_str))
        
        # Additional sanitization for dangerous patterns
        dangerous_patterns = ['javascript:', 'data:', 'vbscript:', 'onload=', 'onerror=']
        for pattern in dangerous_patterns:
            sanitized = sanitized.replace(pattern.lower(), '')
            sanitized = sanitized.replace(pattern.upper(), '')
        
        return sanitized.strip()
    
    def log_security_event(self, event_type: str, details: Dict[str, Any]):
        """Log security events"""
        logger.warning(f"Security Event: {event_type} - {details}")

# Global security manager instance
security_manager = SecurityManager()

def hash_password(password: str) -> str:
    """Hash password utility function"""
    return security_manager.hash_password(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password utility function"""
    return security_manager.verify_password(plain_password, hashed_password)