"""Simple Observability Framework for BHIV HR Platform"""

import time
import logging
from datetime import datetime, timezone
from typing import Dict, Any, Callable, Optional
from fastapi import FastAPI, Request, Response

logger = logging.getLogger(__name__)

class SimpleHealthChecker:
    """Simple health checker with dependency management"""
    
    def __init__(self):
        self.dependencies = {}
        self.status = "healthy"
    
    def add_dependency(self, name: str, check_func: Callable):
        """Add a health check dependency"""
        self.dependencies[name] = check_func
        logger.info(f"Health dependency '{name}' registered")
    
    async def check_health(self) -> Dict[str, Any]:
        """Check health of all dependencies"""
        results = {"status": "healthy", "checks": {}}
        
        for name, check_func in self.dependencies.items():
            try:
                if callable(check_func):
                    result = await check_func() if hasattr(check_func, '__call__') else check_func()
                    results["checks"][name] = result
            except Exception as e:
                results["checks"][name] = {"status": "unhealthy", "error": str(e)}
                results["status"] = "degraded"
        
        return results

class SimpleMetricsCollector:
    """Simple metrics collector"""
    
    def __init__(self):
        self.metrics = {
            "requests_total": 0,
            "requests_duration": [],
            "errors_total": 0
        }
    
    def record_request(self, duration: float, status_code: int):
        """Record request metrics"""
        self.metrics["requests_total"] += 1
        self.metrics["requests_duration"].append(duration)
        if status_code >= 400:
            self.metrics["errors_total"] += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics"""
        durations = self.metrics["requests_duration"]
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        return {
            "requests_total": self.metrics["requests_total"],
            "requests_duration_avg": round(avg_duration, 4),
            "errors_total": self.metrics["errors_total"],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

def setup_simple_observability(app: FastAPI, service_name: str, version: str):
    """Setup simple observability framework"""
    
    health_checker = SimpleHealthChecker()
    metrics_collector = SimpleMetricsCollector()
    
    # Add health endpoints
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "service": service_name, "version": version}
    
    @app.get("/health/detailed")
    async def detailed_health():
        return await health_checker.check_health()
    
    @app.get("/metrics/json")
    async def metrics_json():
        return metrics_collector.get_metrics()
    
    # Add metrics middleware
    @app.middleware("http")
    async def metrics_middleware(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        metrics_collector.record_request(duration, response.status_code)
        return response
    
    logger.info(f"Simple observability setup complete for {service_name}")
    return health_checker

# Compatibility exports
MetricsCollector = SimpleMetricsCollector
setup_observability = setup_simple_observability