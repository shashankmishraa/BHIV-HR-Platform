"""
Security utilities and authentication
"""
import os
import secrets
import logging
from typing import Optional
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import re

logger = logging.getLogger(__name__)
security = HTTPBearer()

def get_api_key() -> str:
    """Get API key from environment"""
    api_key = os.getenv("API_KEY_SECRET")
    if not api_key:
        raise ValueError("API_KEY_SECRET environment variable is required")
    return api_key

def verify_api_key(credentials: HTTPAuthorizationCredentials = Security(security)) -> bool:
    """Verify API key"""
    try:
        expected_key = get_api_key()
        if not secrets.compare_digest(credentials.credentials, expected_key):
            raise HTTPException(status_code=401, detail="Invalid API key")
        return True
    except Exception as e:
        logger.error("API key verification failed")
        raise HTTPException(status_code=401, detail="Authentication failed")

def sanitize_input(input_str: str) -> str:
    """Sanitize user input to prevent injection attacks"""
    if not isinstance(input_str, str):
        return str(input_str)
    
    # Remove potential injection patterns
    sanitized = re.sub(r'[<>"\';\\]', '', input_str)
    return sanitized.strip()

def validate_file_path(file_path: str) -> str:
    """Validate file path to prevent directory traversal"""
    if not file_path:
        raise ValueError("File path cannot be empty")
    
    # Remove path traversal attempts
    clean_path = os.path.normpath(file_path)
    if '..' in clean_path or clean_path.startswith('/'):
        raise ValueError("Invalid file path")
    
    return clean_path

def get_database_url() -> str:
    """Get database URL from environment"""
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL environment variable is required")
    return db_url