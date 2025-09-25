"""Security utilities for BHIV HR Platform Gateway"""

import os
import hashlib
import secrets
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from passlib.context import CryptContext
from fastapi import HTTPException, status
from jose import JWTError, jwt
from .config import get_settings

settings = get_settings()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SecurityManager:
    """Security utilities manager"""
    
    def __init__(self):
        self.api_key_secret = settings.api_key_secret
        self.jwt_secret = settings.jwt_secret
        
    def hash_password(self, password: str) -> str:
        """Hash a password"""
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def generate_api_key(self) -> str:
        """Generate a new API key"""
        return f"ak_{secrets.token_hex(20)}"
    
    def verify_api_key(self, api_key: str) -> bool:
        """Verify API key"""
        # In production, this would check against database
        return api_key == self.api_key_secret or api_key.startswith("ak_")
    
    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=1)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.jwt_secret, algorithm="HS256")
        return encoded_jwt
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=["HS256"])
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
    
    def generate_reset_token(self) -> str:
        """Generate password reset token"""
        return secrets.token_hex(16)
    
    def generate_verification_token(self) -> str:
        """Generate email verification token"""
        return secrets.token_hex(16)
    
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
    
    def validate_sql_input(self, input_str: str) -> bool:
        """Validate input for SQL injection patterns"""
        if not input_str:
            return True
        
        # Common SQL injection patterns
        sql_patterns = [
            'union', 'select', 'insert', 'update', 'delete', 'drop',
            'create', 'alter', 'exec', 'execute', '--', '/*', '*/',
            'xp_', 'sp_', 'waitfor', 'delay'
        ]
        
        input_lower = input_str.lower()
        for pattern in sql_patterns:
            if pattern in input_lower:
                return False
        
        return True
    
    def check_rate_limit(self, identifier: str, limit: int = 60, window: int = 60) -> bool:
        """Check rate limiting (simplified implementation)"""
        # In production, this would use Redis or similar
        return True
    
    def log_security_event(self, event_type: str, details: Dict[str, Any]):
        """Log security events"""
        logger = logging.getLogger("security")
        logger.warning(f"Security Event: {event_type} - {details}")

# Global security manager instance
security_manager = SecurityManager()

def get_security_manager() -> SecurityManager:
    """Get security manager instance"""
    return security_manager

def hash_password(password: str) -> str:
    """Hash password utility function"""
    return security_manager.hash_password(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password utility function"""
    return security_manager.verify_password(plain_password, hashed_password)

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create access token utility function"""
    return security_manager.create_access_token(data, expires_delta)

def verify_api_key(api_key: str) -> bool:
    """Verify API key utility function"""
    return security_manager.verify_api_key(api_key)