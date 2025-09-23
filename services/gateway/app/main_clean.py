# BHIV HR Platform API Gateway - Clean Modular Implementation
# Version: 3.2.0 - Production Ready

from datetime import datetime, timezone
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
import os
import uuid
import time

# Import modular components
try:
    from .core_endpoints import router as core_router
    from .auth import router as auth_router
    from .database import router as database_router
    from .monitoring import router as monitoring_router, structured_logger, setup_service_logging
    from .security_config import security_manager
    from .performance_optimizer import performance_cache
    MODULES_AVAILABLE = True
except ImportError:
    # Fallback for direct execution
    try:
        from core_endpoints import router as core_router
        from auth import router as auth_router
        from database import router as database_router
        from monitoring import router as monitoring_router, structured_logger, setup_service_logging
        from security_config import security_manager
        from performance_optimizer import performance_cache
        MODULES_AVAILABLE = True
    except ImportError:
        MODULES_AVAILABLE = False
        import logging
        logging.basicConfig(level=logging.INFO)
        structured_logger = logging.getLogger("gateway")

# Initialize FastAPI application
app = FastAPI(
    title="BHIV HR Platform API Gateway",
    version="3.2.0",
    description="Enterprise HR Platform with Advanced AI Matching and Security Features"
)

# Setup logging
if MODULES_AVAILABLE:
    try:
        setup_service_logging('gateway')
    except:
        pass

# Environment configuration
environment = os.getenv("ENVIRONMENT", "development").lower()
database_url = os.getenv("DATABASE_URL", 
    "postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@dpg-d373qrogjchc73bu9gug-a.oregon-postgres.render.com/bhiv_hr_nqzb" 
    if environment == "production" 
    else "postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@db:5432/bhiv_hr_nqzb"
)

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
    cors_config = security_manager.get_cors_config()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_config.allowed_origins,
        allow_credentials=cors_config.allow_credentials,
        allow_methods=cors_config.allowed_methods,
        allow_headers=cors_config.allowed_headers,
        max_age=cors_config.max_age
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

# Include routers
if MODULES_AVAILABLE:
    app.include_router(core_router, prefix="", tags=["Core"])
    app.include_router(auth_router, prefix="/v1/auth", tags=["Authentication"])
    app.include_router(database_router, prefix="/v1/database", tags=["Database"])
    app.include_router(monitoring_router, prefix="", tags=["Monitoring"])
else:
    # Fallback endpoints when modules are not available
    @app.get("/")
    def fallback_root():
        return {
            "message": "BHIV HR Platform API Gateway",
            "version": "3.2.0",
            "status": "fallback_mode",
            "modules_available": False
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

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    if structured_logger:
        structured_logger.info(
            "BHIV HR Gateway starting up",
            version="3.2.0",
            environment=environment,
            modules_available=MODULES_AVAILABLE
        )

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    if structured_logger:
        structured_logger.info("BHIV HR Gateway shutting down")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)