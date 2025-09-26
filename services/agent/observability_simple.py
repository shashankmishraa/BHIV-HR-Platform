"""
Simple observability framework for Agent service
Provides basic health checks and metrics without external dependencies
"""

import logging
import time
from datetime import datetime, timezone
from typing import Dict, Any, Callable, Optional

logger = logging.getLogger(__name__)

class SimpleHealthChecker:
    """Simple health checker implementation"""
    
    def __init__(self, app, service_name: str, version: str):
        self.app = app
        self.service_name = service_name
        self.version = version
        self.dependencies = {}
        self.setup_endpoints()
    
    def setup_endpoints(self):
        """Setup health check endpoints"""
        
        @self.app.get("/health")
        async def health_check():
            """Main health check endpoint"""
            return {
                "status": "healthy",
                "service": self.service_name,
                "version": self.version,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        
        @self.app.get("/health/detailed")
        async def detailed_health_check():
            """Detailed health check with dependencies"""
            results = {
                "status": "healthy",
                "service": self.service_name,
                "version": self.version,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "dependencies": {}
            }
            
            overall_healthy = True
            
            for name, check_func in self.dependencies.items():
                try:
                    if callable(check_func):
                        result = await check_func() if hasattr(check_func, '__call__') else check_func()
                        results["dependencies"][name] = result
                        if isinstance(result, dict) and result.get("status") != "healthy":
                            overall_healthy = False
                    else:
                        results["dependencies"][name] = {"status": "unknown", "error": "Invalid check function"}
                        overall_healthy = False
                except Exception as e:
                    results["dependencies"][name] = {"status": "unhealthy", "error": str(e)}
                    overall_healthy = False
            
            results["status"] = "healthy" if overall_healthy else "degraded"
            return results
        
        @self.app.get("/health/ready")
        async def readiness_check():
            """Readiness probe"""
            return {"status": "ready", "timestamp": datetime.now(timezone.utc).isoformat()}
        
        @self.app.get("/health/live")
        async def liveness_check():
            """Liveness probe"""
            return {"status": "alive", "timestamp": datetime.now(timezone.utc).isoformat()}
    
    def add_dependency(self, name: str, check_func: Callable):
        """Add a dependency health check"""
        self.dependencies[name] = check_func
        logger.info(f"Added health dependency: {name}")

class SimpleMetricsCollector:
    """Simple metrics collector implementation"""
    
    def __init__(self):
        self.metrics = {
            "requests_total": 0,
            "requests_duration_seconds": [],
            "errors_total": 0,
            "start_time": time.time()
        }
    
    def increment_requests(self):
        """Increment request counter"""
        self.metrics["requests_total"] += 1
    
    def record_duration(self, duration: float):
        """Record request duration"""
        self.metrics["requests_duration_seconds"].append(duration)
        # Keep only last 1000 measurements
        if len(self.metrics["requests_duration_seconds"]) > 1000:
            self.metrics["requests_duration_seconds"] = self.metrics["requests_duration_seconds"][-1000:]
    
    def increment_errors(self):
        """Increment error counter"""
        self.metrics["errors_total"] += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics"""
        durations = self.metrics["requests_duration_seconds"]
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        return {
            "requests_total": self.metrics["requests_total"],
            "errors_total": self.metrics["errors_total"],
            "avg_response_time_seconds": round(avg_duration, 4),
            "uptime_seconds": round(time.time() - self.metrics["start_time"], 2),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

def setup_simple_observability(app, service_name: str, version: str):
    """Setup simple observability framework"""
    
    # Create health checker
    health_checker = SimpleHealthChecker(app, service_name, version)
    
    # Create metrics collector
    metrics_collector = SimpleMetricsCollector()
    
    # Add metrics endpoint
    @app.get("/metrics/json")
    async def get_metrics():
        """Get metrics in JSON format"""
        return metrics_collector.get_metrics()
    
    # Add middleware for metrics collection
    @app.middleware("http")
    async def metrics_middleware(request, call_next):
        start_time = time.time()
        
        try:
            response = await call_next(request)
            metrics_collector.increment_requests()
            
            if response.status_code >= 400:
                metrics_collector.increment_errors()
            
            duration = time.time() - start_time
            metrics_collector.record_duration(duration)
            
            return response
            
        except Exception as e:
            metrics_collector.increment_errors()
            raise
    
    logger.info(f"Simple observability setup complete for {service_name}")
    
    return metrics_collector, health_checker, None, None  # metrics, health, alert, tracer

# Compatibility exports
MetricsCollector = SimpleMetricsCollector
setup_observability = setup_simple_observability