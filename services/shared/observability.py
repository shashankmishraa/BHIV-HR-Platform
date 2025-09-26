"""
Comprehensive Observability Framework for BHIV HR Platform
Provides standardized health checks, metrics, logging, and monitoring
"""

import json
import logging
import time
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
import psutil
import asyncio
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Request, Response
from fastapi.responses import JSONResponse, PlainTextResponse
import structlog

# Prometheus Metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration', ['method', 'endpoint'])
ACTIVE_CONNECTIONS = Gauge('active_connections', 'Active database connections')
MEMORY_USAGE = Gauge('memory_usage_bytes', 'Memory usage in bytes')
CPU_USAGE = Gauge('cpu_usage_percent', 'CPU usage percentage')
ERROR_COUNT = Counter('errors_total', 'Total errors', ['service', 'error_type'])

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

class HealthChecker:
    """Standardized health check implementation"""
    
    def __init__(self, service_name: str, version: str):
        self.service_name = service_name
        self.version = version
        self.dependencies = {}
        self.start_time = datetime.now(timezone.utc)
    
    def add_dependency(self, name: str, check_func):
        """Add dependency health check"""
        self.dependencies[name] = check_func
    
    async def get_health_status(self, detailed: bool = False) -> Dict[str, Any]:
        """Get comprehensive health status"""
        status = {
            "status": "healthy",
            "service": self.service_name,
            "version": self.version,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "uptime_seconds": (datetime.now(timezone.utc) - self.start_time).total_seconds()
        }
        
        if detailed:
            status["dependencies"] = {}
            overall_healthy = True
            
            for dep_name, check_func in self.dependencies.items():
                try:
                    dep_status = await check_func() if asyncio.iscoroutinefunction(check_func) else check_func()
                    status["dependencies"][dep_name] = dep_status
                    if dep_status.get("status") != "healthy":
                        overall_healthy = False
                except Exception as e:
                    status["dependencies"][dep_name] = {
                        "status": "unhealthy",
                        "error": str(e)
                    }
                    overall_healthy = False
            
            status["status"] = "healthy" if overall_healthy else "degraded"
            
            # Add system metrics
            status["system"] = {
                "cpu_percent": psutil.cpu_percent(),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_percent": psutil.disk_usage('/').percent
            }
        
        return status

class MetricsCollector:
    """Prometheus metrics collection and exposure"""
    
    @staticmethod
    def record_request(method: str, endpoint: str, status_code: int, duration: float):
        """Record HTTP request metrics"""
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status_code).inc()
        REQUEST_DURATION.labels(method=method, endpoint=endpoint).observe(duration)
    
    @staticmethod
    def update_system_metrics():
        """Update system resource metrics"""
        MEMORY_USAGE.set(psutil.virtual_memory().used)
        CPU_USAGE.set(psutil.cpu_percent())
    
    @staticmethod
    def record_error(service: str, error_type: str):
        """Record error occurrence"""
        ERROR_COUNT.labels(service=service, error_type=error_type).inc()
    
    @staticmethod
    def get_metrics() -> str:
        """Get Prometheus formatted metrics"""
        MetricsCollector.update_system_metrics()
        return generate_latest()

class ObservabilityMiddleware:
    """FastAPI middleware for observability"""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
    
    async def __call__(self, request: Request, call_next):
        start_time = time.time()
        
        # Add correlation ID
        correlation_id = request.headers.get("X-Correlation-ID", f"req_{int(time.time() * 1000)}")
        request.state.correlation_id = correlation_id
        
        # Log request start
        logger.info("Request started", 
                   method=request.method, 
                   path=request.url.path,
                   correlation_id=correlation_id,
                   service=self.service_name)
        
        try:
            response = await call_next(request)
            duration = time.time() - start_time
            
            # Record metrics
            MetricsCollector.record_request(
                request.method, 
                request.url.path, 
                response.status_code, 
                duration
            )
            
            # Add headers
            response.headers["X-Correlation-ID"] = correlation_id
            response.headers["X-Response-Time"] = str(duration)
            response.headers["X-Service"] = self.service_name
            
            # Log request completion
            logger.info("Request completed",
                       method=request.method,
                       path=request.url.path,
                       status_code=response.status_code,
                       duration=duration,
                       correlation_id=correlation_id,
                       service=self.service_name)
            
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            
            # Record error
            MetricsCollector.record_error(self.service_name, type(e).__name__)
            
            # Log error
            logger.error("Request failed",
                        method=request.method,
                        path=request.url.path,
                        error=str(e),
                        duration=duration,
                        correlation_id=correlation_id,
                        service=self.service_name,
                        exc_info=True)
            
            raise

def create_health_endpoints(app, health_checker: HealthChecker):
    """Add standardized health endpoints to FastAPI app"""
    
    @app.get("/health", tags=["Health"])
    async def health_check():
        """Simple health check"""
        status = await health_checker.get_health_status()
        status_code = 200 if status["status"] == "healthy" else 503
        return JSONResponse(content=status, status_code=status_code)
    
    @app.get("/health/detailed", tags=["Health"])
    async def detailed_health_check():
        """Detailed health check with dependencies"""
        status = await health_checker.get_health_status(detailed=True)
        status_code = 200 if status["status"] in ["healthy", "degraded"] else 503
        return JSONResponse(content=status, status_code=status_code)
    
    @app.get("/health/ready", tags=["Health"])
    async def readiness_check():
        """Kubernetes readiness probe"""
        status = await health_checker.get_health_status(detailed=True)
        if status["status"] == "healthy":
            return JSONResponse({"status": "ready"}, status_code=200)
        return JSONResponse({"status": "not_ready"}, status_code=503)
    
    @app.get("/health/live", tags=["Health"])
    async def liveness_check():
        """Kubernetes liveness probe"""
        return JSONResponse({"status": "alive"}, status_code=200)

def create_metrics_endpoints(app):
    """Add Prometheus metrics endpoint"""
    
    @app.get("/metrics", tags=["Metrics"])
    async def prometheus_metrics():
        """Prometheus metrics endpoint"""
        metrics = MetricsCollector.get_metrics()
        return PlainTextResponse(metrics, media_type=CONTENT_TYPE_LATEST)
    
    @app.get("/metrics/json", tags=["Metrics"])
    async def json_metrics():
        """JSON formatted metrics for debugging"""
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "system": {
                "cpu_percent": psutil.cpu_percent(),
                "memory_percent": psutil.virtual_memory().percent,
                "memory_used_mb": psutil.virtual_memory().used / 1024 / 1024,
                "disk_percent": psutil.disk_usage('/').percent
            },
            "service": {
                "uptime_seconds": time.time() - psutil.Process().create_time(),
                "threads": psutil.Process().num_threads(),
                "open_files": len(psutil.Process().open_files())
            }
        }

class AlertManager:
    """Simple alerting for critical issues"""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.alert_thresholds = {
            "cpu_percent": 80,
            "memory_percent": 85,
            "error_rate": 0.05,
            "response_time": 5.0
        }
    
    def check_alerts(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check for alert conditions"""
        alerts = []
        
        # CPU alert
        if metrics.get("cpu_percent", 0) > self.alert_thresholds["cpu_percent"]:
            alerts.append({
                "severity": "warning",
                "service": self.service_name,
                "metric": "cpu_usage",
                "value": metrics["cpu_percent"],
                "threshold": self.alert_thresholds["cpu_percent"],
                "message": f"High CPU usage: {metrics['cpu_percent']}%"
            })
        
        # Memory alert
        if metrics.get("memory_percent", 0) > self.alert_thresholds["memory_percent"]:
            alerts.append({
                "severity": "warning",
                "service": self.service_name,
                "metric": "memory_usage",
                "value": metrics["memory_percent"],
                "threshold": self.alert_thresholds["memory_percent"],
                "message": f"High memory usage: {metrics['memory_percent']}%"
            })
        
        return alerts

def setup_observability(app, service_name: str, version: str) -> HealthChecker:
    """Complete observability setup for a service"""
    
    # Create health checker
    health_checker = HealthChecker(service_name, version)
    
    # Add middleware
    app.middleware("http")(ObservabilityMiddleware(service_name))
    
    # Add endpoints
    create_health_endpoints(app, health_checker)
    create_metrics_endpoints(app)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s',
        handlers=[logging.StreamHandler()]
    )
    
    return health_checker