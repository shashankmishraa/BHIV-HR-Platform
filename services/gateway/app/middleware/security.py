from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import time
import logging
from ..core.security_enhanced import get_rate_limiter, get_security_validator

logger = logging.getLogger(__name__)

async def security_middleware(request: Request, call_next):
    """Security middleware for request validation"""
    start_time = time.time()
    
    try:
        # Rate limiting
        client_ip = request.client.host if request.client else "unknown"
        rate_limiter = get_rate_limiter()
        
        if not rate_limiter.is_allowed(client_ip):
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded"}
            )
        
        # Security headers validation
        security_validator = get_security_validator()
        
        # Validate API key if present (support both X-API-KEY and Authorization Bearer)
        api_key = request.headers.get("X-API-KEY")
        auth_header = request.headers.get("Authorization")
        
        # Extract Bearer token if present
        if auth_header and auth_header.startswith("Bearer "):
            api_key = auth_header[7:]  # Remove "Bearer " prefix
        
        # Skip validation for public endpoints
        if request.url.path in ["/health", "/", "/docs", "/openapi.json"]:
            api_key = None
        
        if api_key and not security_validator.validate_api_key(api_key):
            logger.warning(f"Invalid API key format from IP: {client_ip}")
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid API key format"}
            )
        
        # Process request
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self' 'unsafe-inline' 'unsafe-eval' data: https: http:"
        
        # Log request
        process_time = time.time() - start_time
        logger.info(f"Request processed: {request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s")
        
        return response
        
    except Exception as e:
        logger.error(f"Security middleware error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )