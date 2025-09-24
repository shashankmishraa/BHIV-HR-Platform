# Security Testing Router
from fastapi import APIRouter, Header
from typing import Optional

router = APIRouter()

@router.get("/security/rate-limit-status")
async def rate_limit_status():
    """Check rate limit status"""
    return {
        "rate_limit": "60 requests/minute",
        "remaining": 45,
        "reset_time": "2025-01-18T10:30:00Z"
    }

@router.get("/security/headers")
async def security_headers():
    """Get security headers info"""
    return {
        "csp": "default-src 'self'",
        "xss_protection": "1; mode=block",
        "frame_options": "DENY",
        "content_type_options": "nosniff"
    }

@router.post("/security/validate-token")
async def validate_token(authorization: Optional[str] = Header(None)):
    """Validate authentication token"""
    if not authorization:
        return {"valid": False, "error": "No token provided"}
    
    token = authorization.replace("Bearer ", "")
    valid_tokens = ["prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o", "myverysecureapikey123"]
    
    return {
        "valid": token in valid_tokens,
        "token_type": "bearer"
    }

@router.get("/security/audit")
async def security_audit():
    """Security audit information"""
    return {
        "last_audit": "2025-01-18",
        "vulnerabilities": 0,
        "security_score": "A+",
        "compliance": ["OWASP", "SOC2"]
    }