from fastapi import FastAPI, HTTPException, Depends, Security, Response, Header, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from datetime import datetime, timezone
import os
import secrets
import pyotp
import qrcode
import io
import base64
from sqlalchemy import create_engine, text
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
import time
import json
import redis
import asyncio
from .monitoring import monitor, log_resume_processing, log_matching_performance, log_user_activity, log_error

security = HTTPBearer()

# Enhanced CORS configuration with environment-specific origins
def get_cors_origins():
    """Get CORS origins based on environment"""
    env = os.getenv("ENVIRONMENT", "development")
    
    if env == "production":
        return [
            "https://bhiv-hr-portal.onrender.com",
            "https://bhiv-hr-client-portal.onrender.com",
            "https://bhiv.ai",
            "https://www.bhiv.ai"
        ]
    elif env == "staging":
        return [
            "https://staging-bhiv-hr-portal.onrender.com",
            "https://staging-bhiv-hr-client-portal.onrender.com",
            "https://staging.bhiv.ai"
        ]
    else:  # development
        return [
            "http://localhost:8501",
            "http://localhost:8502",
            "http://127.0.0.1:8501",
            "http://127.0.0.1:8502"
        ]

app = FastAPI(
    title="BHIV HR Platform API Gateway",
    version="3.1.0",
    description="Enterprise HR Platform with Advanced Security Features"
)

# Enhanced CORS middleware with secure configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "X-Requested-With"],
    expose_headers=["X-RateLimit-Limit", "X-RateLimit-Remaining", "X-RateLimit-Reset"]
)

# Redis connection for distributed rate limiting
def get_redis_client():
    """Get Redis client for distributed rate limiting"""
    try:
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        return redis.from_url(redis_url, decode_responses=True)
    except:
        return None

redis_client = get_redis_client()

# Enhanced rate limiting with Redis backend
class RateLimiter:
    def __init__(self):
        self.redis_client = get_redis_client()
        self.fallback_storage = {}  # In-memory fallback
        
    def get_rate_limit_key(self, client_ip: str, endpoint: str, user_tier: str = "default") -> str:
        """Generate rate limit key"""
        return f"rate_limit:{user_tier}:{client_ip}:{endpoint}"
    
    def get_tier_limits(self, user_tier: str = "default") -> Dict[str, int]:
        """Get fixed rate limits per tier (no CPU-based adjustment)"""
        limits = {
            "default": {
                "/v1/jobs": 100,
                "/v1/candidates/search": 50,
                "/v1/match": 20,
                "/v1/candidates/bulk": 5,
                "/v1/security/rate-limit-status": 30,
                "/v1/security/test-input-validation": 10,
                "/v1/security/csp-report": 20,
                "default": 60
            },
            "premium": {
                "/v1/jobs": 500,
                "/v1/candidates/search": 200,
                "/v1/match": 100,
                "/v1/candidates/bulk": 25,
                "/v1/security/rate-limit-status": 100,
                "/v1/security/test-input-validation": 50,
                "/v1/security/csp-report": 100,
                "default": 300
            },
            "enterprise": {
                "/v1/jobs": 1000,
                "/v1/candidates/search": 500,
                "/v1/match": 200,
                "/v1/candidates/bulk": 50,
                "/v1/security/rate-limit-status": 200,
                "/v1/security/test-input-validation": 100,
                "/v1/security/csp-report": 200,
                "default": 600
            }
        }
        return limits.get(user_tier, limits["default"])
    
    async def check_rate_limit(self, client_ip: str, endpoint: str, user_tier: str = "default") -> tuple:
        """Check rate limit using Redis or fallback storage"""
        tier_limits = self.get_tier_limits(user_tier)
        limit = tier_limits.get(endpoint, tier_limits["default"])
        
        key = self.get_rate_limit_key(client_ip, endpoint, user_tier)
        current_time = int(time.time())
        window_start = current_time - 60  # 1-minute window
        
        if self.redis_client:
            try:
                # Use Redis for distributed rate limiting
                pipe = self.redis_client.pipeline()
                pipe.zremrangebyscore(key, 0, window_start)
                pipe.zcard(key)
                pipe.zadd(key, {str(current_time): current_time})
                pipe.expire(key, 60)
                results = pipe.execute()
                
                current_count = results[1]
                remaining = max(0, limit - current_count - 1)
                
                if current_count >= limit:
                    return False, limit, 0, current_time + 60
                
                return True, limit, remaining, current_time + 60
                
            except Exception as e:
                # Fallback to in-memory storage
                pass
        
        # Fallback in-memory rate limiting
        if key not in self.fallback_storage:
            self.fallback_storage[key] = []
        
        # Clean old entries
        self.fallback_storage[key] = [
            req_time for req_time in self.fallback_storage[key]
            if req_time > window_start
        ]
        
        current_count = len(self.fallback_storage[key])
        
        if current_count >= limit:
            return False, limit, 0, current_time + 60
        
        self.fallback_storage[key].append(current_time)
        remaining = limit - current_count - 1
        
        return True, limit, remaining, current_time + 60

rate_limiter = RateLimiter()

# Enhanced rate limiting middleware
async def enhanced_rate_limit_middleware(request: Request, call_next):
    """Enhanced rate limiting middleware with Redis backend"""
    client_ip = request.client.host
    endpoint_path = request.url.path
    
    # Skip rate limiting for health checks and static endpoints
    if endpoint_path in ["/health", "/", "/docs", "/openapi.json"]:
        response = await call_next(request)
        return response
    
    # Determine user tier from headers or JWT
    user_tier = "default"
    auth_header = request.headers.get("authorization", "")
    if "enterprise" in auth_header.lower():
        user_tier = "enterprise"
    elif "premium" in auth_header.lower():
        user_tier = "premium"
    
    # Check rate limit
    allowed, limit, remaining, reset_time = await rate_limiter.check_rate_limit(
        client_ip, endpoint_path, user_tier
    )
    
    if not allowed:
        return Response(
            status_code=429,
            content=json.dumps({
                "error": "rate_limit_exceeded",
                "message": f"Rate limit exceeded for {endpoint_path}. Limit: {limit}/minute",
                "retry_after": 60
            }),
            headers={
                "Content-Type": "application/json",
                "X-RateLimit-Limit": str(limit),
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": str(reset_time),
                "Retry-After": "60"
            }
        )
    
    response = await call_next(request)
    
    # Add rate limit headers to response
    response.headers["X-RateLimit-Limit"] = str(limit)
    response.headers["X-RateLimit-Remaining"] = str(remaining)
    response.headers["X-RateLimit-Reset"] = str(reset_time)
    
    return response

app.middleware("http")(enhanced_rate_limit_middleware)

# System load monitoring (separate from rate limiting)
class SystemMonitor:
    def __init__(self):
        self.cpu_threshold = 80
        self.memory_threshold = 85
        
    def get_system_load(self) -> Dict[str, float]:
        """Get current system load metrics"""
        try:
            import psutil
            return {
                "cpu_percent": psutil.cpu_percent(interval=0.1),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_percent": psutil.disk_usage('/').percent
            }
        except:
            return {"cpu_percent": 0, "memory_percent": 0, "disk_percent": 0}
    
    def is_system_overloaded(self) -> bool:
        """Check if system is overloaded"""
        metrics = self.get_system_load()
        return (metrics["cpu_percent"] > self.cpu_threshold or 
                metrics["memory_percent"] > self.memory_threshold)

system_monitor = SystemMonitor()

# Enhanced Pydantic models with comprehensive examples
class SecurityTestInput(BaseModel):
    """Enhanced security test input model"""
    input_data: str = Field(
        ..., 
        description="Input data to validate for security threats",
        example="<script>alert('test')</script>",
        min_length=1,
        max_length=1000
    )
    test_type: Optional[str] = Field(
        "xss", 
        description="Type of security test to perform",
        example="xss"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "input_data": "<script>alert('test')</script>",
                "test_type": "xss"
            }
        }

class CSPReportModel(BaseModel):
    """Enhanced CSP report model"""
    violated_directive: str = Field(
        ..., 
        description="The directive that was violated",
        example="script-src"
    )
    blocked_uri: str = Field(
        ..., 
        description="The URI that was blocked",
        example="https://malicious-site.com/script.js"
    )
    document_uri: str = Field(
        ..., 
        description="The document URI where violation occurred",
        example="https://bhiv-hr-portal.onrender.com/dashboard"
    )
    original_policy: Optional[str] = Field(
        None,
        description="The original CSP policy",
        example="default-src 'self'; script-src 'self'"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "violated_directive": "script-src",
                "blocked_uri": "https://malicious-site.com/script.js",
                "document_uri": "https://bhiv-hr-portal.onrender.com/dashboard",
                "original_policy": "default-src 'self'; script-src 'self'"
            }
        }

# Enhanced OpenAPI documentation
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="BHIV HR Platform API Gateway",
        version="3.1.0",
        description="""
        ## Enterprise HR Platform with Advanced Security Features
        
        ### Security Features
        - **Rate Limiting**: Distributed rate limiting with Redis backend
        - **CORS Protection**: Environment-specific origin restrictions
        - **Input Validation**: XSS and injection attack prevention
        - **CSP Monitoring**: Content Security Policy violation tracking
        
        ### Rate Limits by Tier
        - **Default**: 60 requests/minute (general), 20/min (AI matching)
        - **Premium**: 300 requests/minute (general), 100/min (AI matching)
        - **Enterprise**: 600 requests/minute (general), 200/min (AI matching)
        """,
        routes=app.routes,
    )
    
    # Add comprehensive examples for security endpoints
    if "paths" in openapi_schema:
        # Add examples for security testing endpoints
        security_examples = {
            "/v1/security/test-input-validation": {
                "post": {
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "examples": {
                                    "xss_test": {
                                        "summary": "XSS Attack Test",
                                        "value": {
                                            "input_data": "<script>alert('xss')</script>",
                                            "test_type": "xss"
                                        }
                                    },
                                    "sql_injection_test": {
                                        "summary": "SQL Injection Test",
                                        "value": {
                                            "input_data": "'; DROP TABLE users; --",
                                            "test_type": "sql_injection"
                                        }
                                    },
                                    "safe_input": {
                                        "summary": "Safe Input Test",
                                        "value": {
                                            "input_data": "John Doe",
                                            "test_type": "safe"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/v1/security/csp-report": {
                "post": {
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "examples": {
                                    "script_violation": {
                                        "summary": "Script Source Violation",
                                        "value": {
                                            "violated_directive": "script-src",
                                            "blocked_uri": "https://malicious-site.com/script.js",
                                            "document_uri": "https://bhiv-hr-portal.onrender.com/dashboard"
                                        }
                                    },
                                    "style_violation": {
                                        "summary": "Style Source Violation",
                                        "value": {
                                            "violated_directive": "style-src",
                                            "blocked_uri": "https://untrusted-cdn.com/styles.css",
                                            "document_uri": "https://bhiv-hr-portal.onrender.com/profile"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        
        # Merge examples into schema
        for path, methods in security_examples.items():
            if path in openapi_schema["paths"]:
                for method, config in methods.items():
                    if method in openapi_schema["paths"][path]:
                        openapi_schema["paths"][path][method].update(config)
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# All existing model definitions (keeping them as they are)
class JobCreate(BaseModel):
    title: str
    department: str
    location: str
    experience_level: str
    requirements: str
    description: str
    client_id: Optional[int] = 1
    employment_type: Optional[str] = "Full-time"

class CandidateBulk(BaseModel):
    candidates: List[Dict[str, Any]]

class FeedbackSubmission(BaseModel):
    candidate_id: int
    job_id: int
    integrity: int
    honesty: int
    discipline: int
    hard_work: int
    gratitude: int
    comments: Optional[str] = None

class InterviewSchedule(BaseModel):
    candidate_id: int
    job_id: int
    interview_date: str
    interviewer: Optional[str] = "HR Team"
    notes: Optional[str] = None

class JobOffer(BaseModel):
    candidate_id: int
    job_id: int
    salary: float
    start_date: str
    terms: str

class ClientLogin(BaseModel):
    client_id: str
    password: str

class TwoFASetup(BaseModel):
    user_id: str

class TwoFALogin(BaseModel):
    user_id: str
    totp_code: str

class PasswordValidation(BaseModel):
    password: str

class SecurityTest(BaseModel):
    test_type: str
    payload: str

class CSPPolicy(BaseModel):
    policy: str

class InputValidation(BaseModel):
    input_data: str

class EmailValidation(BaseModel):
    email: str

class PhoneValidation(BaseModel):
    phone: str

class CSPReport(BaseModel):
    violated_directive: str
    blocked_uri: str
    document_uri: str

class PasswordChange(BaseModel):
    old_password: str
    new_password: str

def get_db_engine():
    database_url = os.getenv("DATABASE_URL", "postgresql://bhiv_user:bhiv_pass@db:5432/bhiv_hr")
    return create_engine(database_url, pool_pre_ping=True, pool_recycle=3600)

def validate_api_key(api_key: str) -> bool:
    expected_key = os.getenv("API_KEY_SECRET", "myverysecureapikey123")
    return api_key == expected_key

def get_api_key(credentials: HTTPAuthorizationCredentials = Security(security)):
    if not credentials or not validate_api_key(credentials.credentials):
        raise HTTPException(status_code=401, detail="Invalid API key")
    return credentials.credentials

# Enhanced health endpoint (removed static rate limit headers)
@app.get("/health", tags=["Core API Endpoints"])
def health_check():
    """Enhanced Health Check without static rate limit headers"""
    system_load = system_monitor.get_system_load()
    is_overloaded = system_monitor.is_system_overloaded()
    
    return {
        "status": "degraded" if is_overloaded else "healthy",
        "service": "BHIV HR Gateway",
        "version": "3.1.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "system_load": system_load,
        "rate_limiting": {
            "backend": "redis" if redis_client else "memory",
            "status": "active"
        }
    }

# Enhanced security testing endpoints with comprehensive examples
@app.post(
    "/v1/security/test-input-validation", 
    tags=["Security Testing"],
    summary="Test Input Validation",
    description="""
    **Test input validation against common security threats**
    
    This endpoint validates input data against various security threats including:
    - XSS (Cross-Site Scripting) attacks
    - SQL injection attempts
    - Command injection
    - Path traversal attacks
    
    **Example Payloads:**
    - XSS: `<script>alert('xss')</script>`
    - SQL Injection: `'; DROP TABLE users; --`
    - Safe Input: `John Doe`
    
    **Response includes:**
    - Validation result (SAFE/THREAT)
    - Detected threat types
    - Risk level assessment
    """
)
async def test_input_validation(input_data: SecurityTestInput, api_key: str = Depends(get_api_key)):
    """Enhanced input validation with comprehensive threat detection"""
    
    # Enhanced threat detection patterns
    threat_patterns = {
        "xss": [r"<script", r"javascript:", r"onload=", r"onerror=", r"<iframe"],
        "sql_injection": [r"'.*OR.*'", r"DROP\s+TABLE", r"UNION\s+SELECT", r"--", r";.*--"],
        "command_injection": [r";\s*rm\s", r";\s*cat\s", r"&&", r"\|\|", r"`.*`"],
        "path_traversal": [r"\.\./", r"\.\.\\", r"/etc/passwd", r"C:\\Windows"]
    }
    
    detected_threats = []
    risk_level = "LOW"
    
    import re
    input_lower = input_data.input_data.lower()
    
    for threat_type, patterns in threat_patterns.items():
        for pattern in patterns:
            if re.search(pattern, input_lower, re.IGNORECASE):
                detected_threats.append(threat_type)
                risk_level = "HIGH"
                break
    
    validation_result = "THREAT" if detected_threats else "SAFE"
    
    return {
        "input": input_data.input_data,
        "validation_result": validation_result,
        "threats_detected": detected_threats,
        "risk_level": risk_level,
        "test_type": input_data.test_type,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "recommendations": [
            "Sanitize user input",
            "Use parameterized queries",
            "Implement CSP headers"
        ] if detected_threats else ["Input appears safe"]
    }

@app.get(
    "/v1/security/rate-limit-status", 
    tags=["Security Testing"],
    summary="Check Rate Limit Status",
    description="""
    **Get current rate limiting status and configuration**
    
    Returns detailed information about:
    - Current rate limits by tier
    - Backend storage type (Redis/Memory)
    - System load metrics
    - Rate limit enforcement status
    
    **Rate Limit Tiers:**
    - Default: 60 req/min (general), 20/min (AI matching)
    - Premium: 300 req/min (general), 100/min (AI matching)  
    - Enterprise: 600 req/min (general), 200/min (AI matching)
    """
)
async def check_rate_limit_status(request: Request, api_key: str = Depends(get_api_key)):
    """Enhanced rate limit status with detailed metrics"""
    
    client_ip = request.client.host
    user_tier = "default"  # Could be extracted from JWT/headers
    
    tier_limits = rate_limiter.get_tier_limits(user_tier)
    system_load = system_monitor.get_system_load()
    
    return {
        "rate_limit_enabled": True,
        "backend_type": "redis" if redis_client else "memory",
        "user_tier": user_tier,
        "tier_limits": tier_limits,
        "system_load": system_load,
        "client_ip": client_ip,
        "status": "active",
        "enforcement": "strict",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.post(
    "/v1/security/csp-report", 
    tags=["CSP Management"],
    summary="CSP Violation Reporting",
    description="""
    **Report Content Security Policy violations**
    
    This endpoint receives CSP violation reports from browsers when content
    violates the defined security policy.
    
    **Common Violation Types:**
    - script-src: Blocked external scripts
    - style-src: Blocked external stylesheets
    - img-src: Blocked external images
    - connect-src: Blocked AJAX/fetch requests
    
    **Example Violations:**
    - Malicious script injection attempts
    - Unauthorized third-party resources
    - Inline script/style violations
    """
)
async def csp_violation_reporting(csp_report: CSPReportModel, api_key: str = Depends(get_api_key)):
    """Enhanced CSP violation reporting with threat analysis"""
    
    # Analyze violation severity
    high_risk_directives = ["script-src", "object-src", "base-uri"]
    severity = "HIGH" if csp_report.violated_directive in high_risk_directives else "MEDIUM"
    
    # Check for known malicious patterns
    malicious_indicators = ["eval(", "javascript:", "data:", "blob:"]
    is_suspicious = any(indicator in csp_report.blocked_uri.lower() for indicator in malicious_indicators)
    
    report_id = f"csp_report_{datetime.now().timestamp()}"
    
    # Log violation for security monitoring
    violation_data = {
        "report_id": report_id,
        "violated_directive": csp_report.violated_directive,
        "blocked_uri": csp_report.blocked_uri,
        "document_uri": csp_report.document_uri,
        "severity": severity,
        "is_suspicious": is_suspicious,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    # Store in Redis if available for security analytics
    if redis_client:
        try:
            redis_client.lpush("csp_violations", json.dumps(violation_data))
            redis_client.expire("csp_violations", 86400 * 7)  # Keep for 7 days
        except:
            pass
    
    return {
        "message": "CSP violation reported successfully",
        "report_id": report_id,
        "severity": severity,
        "is_suspicious": is_suspicious,
        "action_taken": "logged_and_monitored",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

# Keep all other existing endpoints unchanged...
# (All the existing endpoints from the original file would go here)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)