"""
Basic Observability Framework
Provides essential health checks and metrics collection
"""

import logging
import time
from datetime import datetime, timezone
from typing import Dict, Any, Callable, Optional, List
from fastapi import FastAPI, Request, Response
import json

logger = logging.getLogger(__name__)

class HealthChecker:
    """Basic health checker with dependency monitoring"""
    
    def __init__(self, app: FastAPI, service_name: str, version: str):
        self.app = app
        self.service_name = service_name
        self.version = version
        self.dependencies: Dict[str, Callable] = {}
        self.startup_time = time.time()
        self._setup_endpoints()
    
    def _setup_endpoints(self):
        """Setup health check endpoints"""
        
        @self.app.get("/health")
        async def health_check():
            """Basic health check endpoint"""
            return {
                "status": "healthy",
                "service": self.service_name,
                "version": self.version,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "uptime_seconds": round(time.time() - self.startup_time, 2)
            }
        
        @self.app.get("/health/detailed")
        async def detailed_health_check():
            """Detailed health check with dependencies"""
            start_time = time.time()
            
            results = {
                "status": "healthy",
                "service": self.service_name,
                "version": self.version,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "uptime_seconds": round(time.time() - self.startup_time, 2),
                "dependencies": {},
                "check_duration_ms": 0
            }
            
            overall_healthy = True
            
            # Check all dependencies
            for name, check_func in self.dependencies.items():
                try:
                    dep_start = time.time()
                    
                    # Handle both sync and async functions
                    if hasattr(check_func, '__call__'):
                        if hasattr(check_func, '__await__'):
                            result = await check_func()
                        else:
                            result = check_func()
                    else:
                        result = {"status": "unknown", "error": "Invalid check function"}
                    
                    dep_duration = round((time.time() - dep_start) * 1000, 2)
                    
                    if isinstance(result, dict):
                        result["check_duration_ms"] = dep_duration
                        results["dependencies"][name] = result
                        
                        if result.get("status") != "healthy":
                            overall_healthy = False
                    else:
                        results["dependencies"][name] = {
                            "status": "unknown",
                            "error": "Invalid response format",
                            "check_duration_ms": dep_duration
                        }
                        overall_healthy = False
                        
                except Exception as e:
                    results["dependencies"][name] = {
                        "status": "unhealthy",
                        "error": str(e),
                        "check_duration_ms": round((time.time() - dep_start) * 1000, 2) if 'dep_start' in locals() else 0
                    }
                    overall_healthy = False
            
            results["status"] = "healthy" if overall_healthy else "degraded"
            results["check_duration_ms"] = round((time.time() - start_time) * 1000, 2)
            
            return results
        
        @self.app.get("/health/ready")
        async def readiness_check():
            """Kubernetes readiness probe"""
            # Check if all critical dependencies are healthy
            critical_deps = ["database"]  # Add more as needed
            
            for dep_name in critical_deps:
                if dep_name in self.dependencies:
                    try:
                        check_func = self.dependencies[dep_name]
                        if hasattr(check_func, '__await__'):
                            result = await check_func()
                        else:
                            result = check_func()
                        
                        if isinstance(result, dict) and result.get("status") != "healthy":
                            return Response(
                                content=json.dumps({
                                    "status": "not_ready",
                                    "reason": f"Dependency {dep_name} unhealthy",
                                    "timestamp": datetime.now(timezone.utc).isoformat()
                                }),
                                status_code=503,
                                media_type="application/json"
                            )
                    except Exception as e:
                        return Response(
                            content=json.dumps({
                                "status": "not_ready",
                                "reason": f"Dependency {dep_name} check failed: {str(e)}",
                                "timestamp": datetime.now(timezone.utc).isoformat()
                            }),
                            status_code=503,
                            media_type="application/json"
                        )
            
            return {
                "status": "ready",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        
        @self.app.get("/health/live")
        async def liveness_check():
            """Kubernetes liveness probe"""
            return {
                "status": "alive",
                "service": self.service_name,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "uptime_seconds": round(time.time() - self.startup_time, 2)
            }
    
    def add_dependency(self, name: str, check_func: Callable):
        """Add a dependency health check"""
        if not callable(check_func):
            raise ValueError(f"Health check for {name} must be callable")
        
        self.dependencies[name] = check_func
        logger.info(f"Added health dependency: {name}")

class MetricsCollector:
    """Basic metrics collector with Prometheus-compatible output"""
    
    def __init__(self):
        self.metrics = {
            "http_requests_total": 0,
            "http_request_duration_seconds": [],
            "http_errors_total": 0,
            "http_requests_in_progress": 0,
            "start_time": time.time()
        }
        self.request_counts_by_method = {}
        self.request_counts_by_status = {}
    
    def increment_requests(self, method: str = "GET", status_code: int = 200):
        """Increment request counters"""
        self.metrics["http_requests_total"] += 1
        
        # Track by method
        self.request_counts_by_method[method] = self.request_counts_by_method.get(method, 0) + 1
        
        # Track by status code
        status_class = f"{status_code // 100}xx"
        self.request_counts_by_status[status_class] = self.request_counts_by_status.get(status_class, 0) + 1
        
        # Track errors
        if status_code >= 400:
            self.metrics["http_errors_total"] += 1
    
    def record_duration(self, duration: float):
        """Record request duration"""
        self.metrics["http_request_duration_seconds"].append(duration)
        
        # Keep only last 1000 measurements for memory efficiency
        if len(self.metrics["http_request_duration_seconds"]) > 1000:
            self.metrics["http_request_duration_seconds"] = self.metrics["http_request_duration_seconds"][-1000:]
    
    def increment_in_progress(self):
        """Increment requests in progress"""
        self.metrics["http_requests_in_progress"] += 1
    
    def decrement_in_progress(self):
        """Decrement requests in progress"""
        self.metrics["http_requests_in_progress"] = max(0, self.metrics["http_requests_in_progress"] - 1)
    
    def get_metrics_json(self) -> Dict[str, Any]:
        """Get metrics in JSON format"""
        durations = self.metrics["http_request_duration_seconds"]
        
        # Calculate percentiles
        if durations:
            sorted_durations = sorted(durations)
            count = len(sorted_durations)
            p50 = sorted_durations[int(count * 0.5)] if count > 0 else 0
            p95 = sorted_durations[int(count * 0.95)] if count > 0 else 0
            p99 = sorted_durations[int(count * 0.99)] if count > 0 else 0
            avg_duration = sum(durations) / count
            max_duration = max(durations)
            min_duration = min(durations)
        else:
            p50 = p95 = p99 = avg_duration = max_duration = min_duration = 0
        
        uptime = time.time() - self.metrics["start_time"]
        
        return {
            "http_requests_total": self.metrics["http_requests_total"],
            "http_errors_total": self.metrics["http_errors_total"],
            "http_requests_in_progress": self.metrics["http_requests_in_progress"],
            "http_request_duration_seconds": {
                "avg": round(avg_duration, 4),
                "min": round(min_duration, 4),
                "max": round(max_duration, 4),
                "p50": round(p50, 4),
                "p95": round(p95, 4),
                "p99": round(p99, 4),
                "count": len(durations)
            },
            "http_requests_by_method": self.request_counts_by_method,
            "http_requests_by_status": self.request_counts_by_status,
            "uptime_seconds": round(uptime, 2),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    def get_prometheus_metrics(self) -> str:
        """Get metrics in Prometheus format"""
        durations = self.metrics["http_request_duration_seconds"]
        avg_duration = sum(durations) / len(durations) if durations else 0
        uptime = time.time() - self.metrics["start_time"]
        
        lines = [
            "# HELP http_requests_total Total number of HTTP requests",
            "# TYPE http_requests_total counter",
            f"http_requests_total {self.metrics['http_requests_total']}",
            "",
            "# HELP http_errors_total Total number of HTTP errors",
            "# TYPE http_errors_total counter", 
            f"http_errors_total {self.metrics['http_errors_total']}",
            "",
            "# HELP http_requests_in_progress Number of HTTP requests currently in progress",
            "# TYPE http_requests_in_progress gauge",
            f"http_requests_in_progress {self.metrics['http_requests_in_progress']}",
            "",
            "# HELP http_request_duration_seconds Average HTTP request duration",
            "# TYPE http_request_duration_seconds gauge",
            f"http_request_duration_seconds {avg_duration:.4f}",
            "",
            "# HELP process_uptime_seconds Process uptime in seconds",
            "# TYPE process_uptime_seconds gauge",
            f"process_uptime_seconds {uptime:.2f}",
            ""
        ]
        
        # Add method-specific metrics
        for method, count in self.request_counts_by_method.items():
            lines.append(f'http_requests_total{{method="{method}"}} {count}')
        
        # Add status-specific metrics  
        for status, count in self.request_counts_by_status.items():
            lines.append(f'http_requests_total{{status="{status}"}} {count}')
        
        return "\n".join(lines)

def setup_observability(app: FastAPI, service_name: str, version: str) -> HealthChecker:
    """Setup basic observability framework"""
    
    # Create health checker
    health_checker = HealthChecker(app, service_name, version)
    
    # Create metrics collector
    metrics_collector = MetricsCollector()
    
    # Add metrics endpoints
    @app.get("/metrics")
    async def get_prometheus_metrics():
        """Get metrics in Prometheus format"""
        return Response(
            content=metrics_collector.get_prometheus_metrics(),
            media_type="text/plain"
        )
    
    @app.get("/metrics/json")
    async def get_json_metrics():
        """Get metrics in JSON format"""
        return metrics_collector.get_metrics_json()
    
    # Add metrics middleware
    @app.middleware("http")
    async def metrics_middleware(request: Request, call_next):
        """Collect request metrics"""
        start_time = time.time()
        method = request.method
        
        # Increment in-progress counter
        metrics_collector.increment_in_progress()
        
        try:
            response = await call_next(request)
            
            # Record metrics
            duration = time.time() - start_time
            metrics_collector.record_duration(duration)
            metrics_collector.increment_requests(method, response.status_code)
            
            # Add metrics headers
            response.headers["X-Response-Time"] = f"{duration:.4f}"
            
            return response
            
        except Exception as e:
            # Record error
            duration = time.time() - start_time
            metrics_collector.record_duration(duration)
            metrics_collector.increment_requests(method, 500)
            raise
        finally:
            # Decrement in-progress counter
            metrics_collector.decrement_in_progress()
    
    logger.info(f"Basic observability framework initialized for {service_name} v{version}")
    
    return health_checker