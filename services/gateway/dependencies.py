from fastapi import HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
import jwt
from datetime import datetime, timezone

security = HTTPBearer()

def validate_api_key(api_key: str) -> bool:
    """Validate API key against environment variable"""
    expected_key = os.getenv("API_KEY_SECRET", "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o")
    return api_key == expected_key

def get_api_key(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Dependency for API key authentication"""
    if not credentials or not validate_api_key(credentials.credentials):
        raise HTTPException(status_code=401, detail="Invalid API key")
    return credentials.credentials

def get_auth(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Dual authentication: API key or client JWT token"""
    if not credentials:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    # Try API key first
    if validate_api_key(credentials.credentials):
        return {"type": "api_key", "credentials": credentials.credentials}
    
    # Try client JWT token
    try:
        jwt_secret = os.getenv("JWT_SECRET", "fallback_jwt_secret_key_for_client_auth_2025")
        payload = jwt.decode(credentials.credentials, jwt_secret, algorithms=["HS256"])
        return {"type": "client_token", "client_id": payload.get("client_id")}
    except:
        pass
    
    raise HTTPException(status_code=401, detail="Invalid authentication")

def auth_dependency(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Standard auth dependency for all services"""
    return get_auth(credentials)