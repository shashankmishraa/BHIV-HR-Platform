"""API Authentication and Authorization"""

import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()

# API Keys and JWT configuration
API_KEY_SECRET = os.getenv("API_KEY_SECRET", "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o")
JWT_SECRET = os.getenv("JWT_SECRET", "bhiv-hr-jwt-secret-key-2025")
ALGORITHM = "HS256"

# Valid API keys for different access levels
VALID_API_KEYS = {
    API_KEY_SECRET: {"name": "Production API", "level": "admin"},
    "demo_api_key_123": {"name": "Demo API", "level": "read"},
    "test_api_key_456": {"name": "Test API", "level": "write"}
}

def verify_api_key(credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
    """Verify API key from Authorization header"""
    if not credentials:
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    token = credentials.credentials
    
    # Check if it's a valid API key
    if token in VALID_API_KEYS:
        return {
            "type": "api_key",
            "key": token,
            "info": VALID_API_KEYS[token],
            "authenticated": True
        }
    
    # Try to decode as JWT token
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        return {
            "type": "jwt",
            "payload": payload,
            "authenticated": True
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid authentication token")

def create_jwt_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=24)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt

def require_admin_access(auth_data: dict = Depends(verify_api_key)) -> dict:
    """Require admin level access"""
    if auth_data.get("type") == "api_key":
        if auth_data["info"]["level"] != "admin":
            raise HTTPException(status_code=403, detail="Admin access required")
    return auth_data

def require_write_access(auth_data: dict = Depends(verify_api_key)) -> dict:
    """Require write level access or higher"""
    if auth_data.get("type") == "api_key":
        level = auth_data["info"]["level"]
        if level not in ["admin", "write"]:
            raise HTTPException(status_code=403, detail="Write access required")
    return auth_data