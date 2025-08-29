"""
Enhanced security utilities for BHIV HR Platform
"""
import os
import secrets
import logging
import re
from typing import Optional
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timezone

logger = logging.getLogger(__name__)
security = HTTPBearer()

class SecurityConfig:
    """Security configuration and utilities"""
    
    @staticmethod
    def get_api_key() -> str:
        """Get API key from environment with validation"""
        api_key = os.getenv("API_KEY_SECRET")
        if not api_key or len(api_key) < 32:
            raise ValueError("API_KEY_SECRET must be at least 32 characters")
        return api_key
    
    @staticmethod
    def verify_api_key(credentials: HTTPAuthorizationCredentials = Security(security)) -> bool:
        """Secure API key verification"""
        try:
            expected_key = SecurityConfig.get_api_key()
            if not secrets.compare_digest(credentials.credentials, expected_key):
                logger.warning(f"Invalid API key attempt at {datetime.now(timezone.utc)}")
                raise HTTPException(status_code=401, detail="Invalid API key")
            return True
        except Exception as e:
            logger.error(f"API key verification failed: {str(e)}")
            raise HTTPException(status_code=401, detail="Authentication failed")
    
    @staticmethod
    def sanitize_input(input_str: str, max_length: int = 255) -> str:
        """Sanitize user input to prevent injection attacks"""
        if not isinstance(input_str, str):
            return str(input_str)[:max_length]
        
        # Remove potential injection patterns
        sanitized = re.sub(r'[<>"\';\\]', '', input_str)
        sanitized = sanitized.strip()[:max_length]
        return sanitized
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number format"""
        pattern = r'^\+?[\d\s\-\(\)]{10,15}$'
        return bool(re.match(pattern, phone))
    
    @staticmethod
    def mask_pii(data: str, mask_char: str = "*") -> str:
        """Mask personally identifiable information"""
        if not data:
            return data
        
        # Email masking
        if "@" in data:
            parts = data.split("@")
            if len(parts) == 2:
                username = parts[0]
                domain = parts[1]
                masked_username = username[:2] + mask_char * (len(username) - 2)
                return f"{masked_username}@{domain}"
        
        # Phone masking
        if len(data) >= 10 and any(c.isdigit() for c in data):
            return data[:3] + mask_char * (len(data) - 6) + data[-3:]
        
        # General masking for other PII
        if len(data) > 4:
            return data[:2] + mask_char * (len(data) - 4) + data[-2:]
        
        return mask_char * len(data)
    
    @staticmethod
    def log_security_event(event_type: str, details: str, user_id: Optional[str] = None):
        """Log security events for monitoring"""
        timestamp = datetime.now(timezone.utc).isoformat()
        sanitized_details = SecurityConfig.sanitize_input(details, 500)
        
        log_entry = {
            "timestamp": timestamp,
            "event_type": event_type,
            "details": sanitized_details,
            "user_id": user_id or "anonymous"
        }
        
        logger.info(f"SECURITY_EVENT: {log_entry}")

def get_secure_api_key(credentials: HTTPAuthorizationCredentials = Security(security)) -> str:
    """Dependency for secure API key validation"""
    SecurityConfig.verify_api_key(credentials)
    return credentials.credentials