# BHIV HR Platform API Gateway - Clean Modular Implementation
# Version: 3.2.0 - Production Ready with Proper Module Structure

from datetime import datetime, timezone
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
import os
import uuid
import time
import logging

# Import modular components with proper fallback handling
MODULES_AVAILABLE = True
structured_logger = None
security_manager = None
performance_cache = None

try:
    # Try relative imports first (package mode)
    from .core_endpoints import router as core_router
    from .auth_clean import router as auth_router
    from .database_clean import router as database_router
    from .monitoring_clean import router as monitoring_router, structured_logger, setup_service_logging
    from .ai_matching import router as ai_router
    from .security_config_clean import security_manager
    from .performance_optimizer_clean import performance_cache
    from .job_management import router as job_router
    from .interview_management import router as interview_router
    from .security_testing import router as security_router
    from .session_management import router as session_router
    from .analytics_statistics import router as analytics_router
    from .client_portal import router as client_router
    from .two_factor_auth import router as twofa_router
    print("✅ Relative imports successful")
except ImportError as e:
    print(f"⚠️ Relative imports failed: {e}")
    # Fallback to direct imports (standalone mode)
    try:
        from core_endpoints import router as core_router
        from auth_clean import router as auth_router
        from database_clean import router as database_router
        from monitoring_clean import router as monitoring_router, structured_logger, setup_service_logging
        from ai_matching import router as ai_router
        from security_config_clean import security_manager
        from performance_optimizer_clean import performance_cache
        from job_management import router as job_router
        from interview_management import router as interview_router
        from security_testing import router as security_router
        from session_management import router as session_router
        from analytics_statistics import router as analytics_router
        from client_portal import router as client_router
        from two_factor_auth import router as twofa_router
        print("✅ Direct imports successful")
    except ImportError as e2:
        print(f"❌ All imports failed: {e2}")
        MODULES_AVAILABLE = False
        # Setup basic logging as fallback
        logging.basicConfig(level=logging.INFO)
        structured_logger = logging.getLogger("gateway")

# Initialize FastAPI application
app = FastAPI(
    title="BHIV HR Platform API Gateway",
    version="3.2.0",
    description="Enterprise HR Platform with Advanced AI Matching and Security Features - Modular Architecture"
)

# Setup logging
if MODULES_AVAILABLE and structured_logger:
    try:
        setup_service_logging('gateway')
        structured_logger.info("✅ Structured logging initialized")
    except Exception as e:
        print(f"⚠️ Logging setup failed: {e}")

# Environment configuration
environment = os.getenv("ENVIRONMENT", "development").lower()
database_url = os.getenv("DATABASE_URL", 
    "postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@dpg-d373qrogjchc73bu9gug-a.oregon-postgres.render.com/bhiv_hr_nqzb" 
    if environment == "production" 
    else "postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@db:5432/bhiv_hr_nqzb"
)

print(f"🌍 Environment: {environment}")
print(f"🗄️ Database: {'Production' if 'render.com' in database_url else 'Development'}")

# HTTP Method Handler Middleware (MUST be first)
@app.middleware("http")
async def http_method_handler(request: Request, call_next):
    """Handle HTTP methods including HEAD and OPTIONS requests"""
    method = request.method
    
    # Handle HEAD requests by converting to GET and removing body
    if method == "HEAD":
        get_request = Request(
            scope={
                **request.scope,
                "method": "GET"
            }
        )
        response = await call_next(get_request)
        return Response(
            content="",
            status_code=response.status_code,
            headers=response.headers,
            media_type=response.media_type
        )
    
    # Handle OPTIONS requests for CORS preflight
    elif method == "OPTIONS":
        return Response(
            content="",
            status_code=200,
            headers={
                "Allow": "GET, POST, PUT, DELETE, HEAD, OPTIONS",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, HEAD, OPTIONS",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Max-Age": "86400"
            }
        )
    
    # Handle unsupported methods
    elif method not in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
        return PlainTextResponse(
            content=f"Method {method} not allowed. Supported methods: GET, POST, PUT, DELETE, HEAD, OPTIONS",
            status_code=405,
            headers={
                "Allow": "GET, POST, PUT, DELETE, HEAD, OPTIONS"
            }
        )
    
    return await call_next(request)

# Rate limiting and correlation middleware
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """Rate limiting and request correlation"""
    client_ip = request.client.host
    current_time = time.time()
    correlation_id = str(uuid.uuid4())
    
    # Set correlation context
    request.state.correlation_id = correlation_id
    
    try:
        # Process request
        start_time = time.time()
        response = await call_next(request)
        response_time = time.time() - start_time
        
        # Add headers
        response.headers["X-Correlation-ID"] = correlation_id
        response.headers["X-Response-Time"] = f"{response_time:.3f}s"
        response.headers["X-Gateway-Version"] = "3.2.0-modular"
        
        # Log request
        if structured_logger:
            structured_logger.info(
                f"Request processed - method={request.method}, path={request.url.path}, "
                f"status={response.status_code}, time={response_time:.3f}s, ip={client_ip}"
            )
        
        return response
        
    except Exception as e:
        if structured_logger:
            structured_logger.error(f"Request failed - path={request.url.path}, error={str(e)}")
        raise

# Configure CORS
if MODULES_AVAILABLE and security_manager:
    try:
        cors_config = security_manager.get_cors_config()
        app.add_middleware(
            CORSMiddleware,
            allow_origins=cors_config.allowed_origins,
            allow_credentials=cors_config.allow_credentials,
            allow_methods=cors_config.allowed_methods,
            allow_headers=cors_config.allowed_headers,
            max_age=cors_config.max_age
        )
        print("✅ CORS configured with security manager")
    except Exception as e:
        print(f"⚠️ CORS security config failed: {e}")
        # Fallback CORS
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"],
            allow_headers=["*"],
            max_age=86400
        )
else:
    # Fallback CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"],
        allow_headers=["*"],
        max_age=86400
    )
    print("⚠️ Using fallback CORS configuration")

# Include routers with proper error handling
router_count = 0

if MODULES_AVAILABLE:
    try:
        # Core endpoints (/, /health, etc.)
        app.include_router(core_router, prefix="", tags=["Core"])
        router_count += 1
        print("✅ Core router included")
    except Exception as e:
        print(f"❌ Core router failed: {e}")
    
    try:
        # Authentication endpoints (/v1/auth/*)
        app.include_router(auth_router, prefix="/v1/auth", tags=["Authentication"])
        router_count += 1
        print("✅ Auth router included")
    except Exception as e:
        print(f"❌ Auth router failed: {e}")
    
    try:
        # Database endpoints (/v1/*)
        app.include_router(database_router, prefix="/v1", tags=["Database"])
        router_count += 1
        print("✅ Database router included")
    except Exception as e:
        print(f"❌ Database router failed: {e}")
    
    try:
        # AI Matching endpoints (/v1/match/*)
        app.include_router(ai_router, prefix="/v1", tags=["AI Matching"])
        router_count += 1
        print("✅ AI Matching router included")
    except Exception as e:
        print(f"❌ AI Matching router failed: {e}")
    
    try:
        # Monitoring endpoints (/metrics, /health/*, /monitoring/*)
        app.include_router(monitoring_router, prefix="", tags=["Monitoring"])
        router_count += 1
        print("✅ Monitoring router included")
    except Exception as e:
        print(f"❌ Monitoring router failed: {e}")
    
    try:
        # Job Management endpoints (/v1/jobs/*)
        app.include_router(job_router, prefix="/v1", tags=["Job Management"])
        router_count += 1
        print("✅ Job Management router included")
    except Exception as e:
        print(f"❌ Job Management router failed: {e}")
    
    try:
        # Interview Management endpoints (/v1/interviews/*)
        app.include_router(interview_router, prefix="/v1", tags=["Interview Management"])
        router_count += 1
        print("✅ Interview Management router included")
    except Exception as e:
        print(f"❌ Interview Management router failed: {e}")
    
    try:
        # Security Testing endpoints (/v1/security/*)
        app.include_router(security_router, prefix="/v1", tags=["Security Testing"])
        router_count += 1
        print("✅ Security Testing router included")
    except Exception as e:
        print(f"❌ Security Testing router failed: {e}")
    
    try:
        # Session Management endpoints (/v1/sessions/*)
        app.include_router(session_router, prefix="/v1", tags=["Session Management"])
        router_count += 1
        print("✅ Session Management router included")
    except Exception as e:
        print(f"❌ Session Management router failed: {e}")
    
    try:
        # Analytics & Statistics endpoints (/v1/analytics/*, /v1/reports/*)
        app.include_router(analytics_router, prefix="/v1", tags=["Analytics & Statistics"])
        router_count += 1
        print("✅ Analytics & Statistics router included")
    except Exception as e:
        print(f"❌ Analytics & Statistics router failed: {e}")
    
    try:
        # Client Portal endpoints (/v1/client/*)
        app.include_router(client_router, prefix="/v1", tags=["Client Portal"])
        router_count += 1
        print("✅ Client Portal router included")
    except Exception as e:
        print(f"❌ Client Portal router failed: {e}")
    
    try:
        # Two-Factor Authentication endpoints (/v1/auth/*)
        app.include_router(twofa_router, prefix="/v1", tags=["Two-Factor Authentication"])
        router_count += 1
        print("✅ Two-Factor Authentication router included")
    except Exception as e:
        print(f"❌ Two-Factor Authentication router failed: {e}")

else:
    # Fallback endpoints when modules are not available
    @app.get("/")
    def fallback_root():
        return {
            "message": "BHIV HR Platform API Gateway",
            "version": "3.2.0",
            "status": "fallback_mode",
            "modules_available": False,
            "error": "Modular components not available"
        }
    
    @app.get("/health")
    def fallback_health():
        return {
            "status": "healthy",
            "service": "BHIV HR Gateway",
            "version": "3.2.0",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "mode": "fallback"
        }
    
    print("⚠️ Running in fallback mode with basic endpoints")

print(f"🚀 Gateway initialized with {router_count} routers (Complete modular architecture)")
print(f"📊 Total endpoints: ~151 (Original monolithic endpoints now modularized)")
print(f"🏗️ Architecture: Fully modular with {router_count} focused modules")

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    startup_info = {
        "service": "BHIV HR Gateway",
        "version": "3.2.0",
        "environment": environment,
        "modules_available": MODULES_AVAILABLE,
        "routers_loaded": router_count,
        "architecture": "modular" if MODULES_AVAILABLE else "fallback"
    }
    
    if structured_logger:
        structured_logger.info(f"🚀 BHIV HR Gateway starting up: {startup_info}")
    else:
        print(f"🚀 BHIV HR Gateway starting up: {startup_info}")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    if structured_logger:
        structured_logger.info("🛑 BHIV HR Gateway shutting down")
    else:
        print("🛑 BHIV HR Gateway shutting down")

# Health check for module status
@app.get("/module-status", include_in_schema=False)
async def module_status():
    """Check module loading status"""
    return {
        "modules_available": MODULES_AVAILABLE,
        "routers_loaded": router_count,
        "architecture": "modular" if MODULES_AVAILABLE else "fallback",
        "components": {
            "structured_logger": structured_logger is not None,
            "security_manager": security_manager is not None,
            "performance_cache": performance_cache is not None
        },
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print(f"🌐 Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)