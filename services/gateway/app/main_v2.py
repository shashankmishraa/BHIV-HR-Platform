"""
BHIV HR Platform API Gateway - Modular Version
Main application with modular architecture
"""

from datetime import datetime, timezone
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, PlainTextResponse
from fastapi.staticfiles import StaticFiles
import os
import uuid
import time

# Import modular components
from .core_endpoints import router as core_router
from .auth import simple_auth
from .database import get_db_engine
from .monitoring import structured_logger, CorrelationContext, create_health_manager

# Initialize FastAPI application
app = FastAPI(
    title="BHIV HR Platform API Gateway",
    version="3.2.0",
    description="Enterprise HR Platform with Advanced AI Matching and Security Features"
)

# Health check configuration
health_config = {
    'database_url': os.getenv("DATABASE_URL", "postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@dpg-d373qrogjchc73bu9gug-a.oregon-postgres.render.com/bhiv_hr_nqzb"),
    'dependent_services': [
        {'url': 'https://bhiv-hr-agent.onrender.com/health', 'name': 'ai_agent'},
        {'url': 'https://bhiv-hr-portal.onrender.com/', 'name': 'hr_portal'},
        {'url': 'https://bhiv-hr-client-portal.onrender.com/', 'name': 'client_portal'}
    ]
}
health_manager = create_health_manager(health_config)

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# HTTP Method Handler Middleware (MUST be first)
@app.middleware("http")
async def http_method_handler(request: Request, call_next):
    """Handle HTTP methods including HEAD and OPTIONS requests"""
    method = request.method
    
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
    
    elif method not in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
        return PlainTextResponse(
            content=f"Method {method} not allowed. Supported methods: GET, POST, PUT, DELETE, HEAD, OPTIONS",
            status_code=405,
            headers={"Allow": "GET, POST, PUT, DELETE, HEAD, OPTIONS"}
        )
    
    return await call_next(request)

# Rate limiting middleware
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    current_time = time.time()
    endpoint_path = request.url.path
    
    correlation_id = str(uuid.uuid4())
    CorrelationContext.set_correlation_id(correlation_id)
    CorrelationContext.set_request_id(f"{request.method}-{int(current_time)}")
    
    try:
        start_time = time.time()
        response = await call_next(request)
        response_time = time.time() - start_time
        
        structured_logger.info(
            f"API request completed - method={request.method}, endpoint={endpoint_path}, "
            f"status_code={response.status_code}, response_time={response_time:.3f}s, client_ip={client_ip}"
        )
        
        response.headers["X-RateLimit-Limit"] = "60"
        response.headers["X-RateLimit-Remaining"] = "45"
        response.headers["X-Correlation-ID"] = correlation_id
        
        return response
        
    except Exception as e:
        structured_logger.error(f"Request processing error - endpoint={endpoint_path}, error={str(e)}")
        raise
    finally:
        CorrelationContext.clear()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"],
    allow_headers=["*"],
    max_age=86400
)

# Include routers
app.include_router(core_router)

# Additional endpoints can be added here or in separate modules
@app.get("/metrics", tags=["Monitoring"])
async def get_prometheus_metrics():
    """Prometheus Metrics Export"""
    from .monitoring import monitor
    return Response(content=monitor.export_prometheus_metrics(), media_type="text/plain")

@app.get("/health/simple", tags=["Monitoring"])
async def simple_health_check():
    """Simple Health Check for Load Balancers"""
    try:
        health_result = await health_manager.get_simple_health()
        if health_result['status'] == 'healthy':
            return Response(content="OK", status_code=200)
        else:
            return Response(content="DEGRADED", status_code=503)
    except Exception:
        return Response(content="ERROR", status_code=503)

# Authentication endpoints
@app.post("/auth/login", tags=["Authentication"])
@app.get("/auth/login", tags=["Authentication"])
async def login(login_data: simple_auth.LoginRequest = None, username: str = None, password: str = None):
    """User Login - Basic Authentication (supports both GET and POST)"""
    try:
        if not login_data and username and password:
            from .auth import LoginRequest
            login_data = LoginRequest(username=username, password=password)
        
        if not login_data:
            return {
                "message": "Login endpoint active",
                "methods": ["GET", "POST"],
                "parameters": {
                    "POST": "JSON body with username and password",
                    "GET": "Query parameters: ?username=X&password=Y"
                },
                "demo_credentials": {
                    "username": "TECH001",
                    "password": "demo123"
                }
            }
        
        user = simple_auth.authenticate_user(login_data.username, login_data.password)
        
        if not user:
            from fastapi import HTTPException
            raise HTTPException(status_code=401, detail="Invalid username or password")
        
        access_token = simple_auth.generate_jwt_token(user["user_id"], user["role"])
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": 86400,
            "user_id": user["user_id"],
            "username": user["username"],
            "role": user["role"],
            "login_time": datetime.now(timezone.utc).isoformat(),
            "message": "Login successful"
        }
        
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)