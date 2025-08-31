from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Optional
import jwt
from datetime import datetime, timedelta

security = HTTPBearer()

# Simple client database (in production, use proper database)
CLIENT_DB = {
    "1": {"name": "TechCorp Inc", "access_code": "client123", "active": True},
    "2": {"name": "StartupXYZ", "access_code": "startup456", "active": True}
}

SECRET_KEY = "client_secret_key_2024"

def create_client_token(client_id: str, client_name: str) -> str:
    """Create JWT token for client authentication"""
    payload = {
        "client_id": client_id,
        "client_name": client_name,
        "exp": datetime.utcnow() + timedelta(hours=24),
        "type": "client"
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_client_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict:
    """Verify client JWT token"""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
        if payload.get("type") != "client":
            raise HTTPException(status_code=401, detail="Invalid token type")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def authenticate_client(client_id: str, access_code: str) -> Optional[Dict]:
    """Authenticate client credentials"""
    client = CLIENT_DB.get(client_id)
    if client and client["access_code"] == access_code and client["active"]:
        return {"client_id": client_id, "client_name": client["name"]}
    return None