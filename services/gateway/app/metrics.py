"""Metrics Module for BHIV HR Gateway"""

import time
from typing import Any, Dict, Callable
from fastapi import Request, Response

class MetricsCollector:
    def __init__(self):
        self.request_count = 0
        self.start_time = time.time()
    
    def collect_metrics(self) -> Dict[str, Any]:
        return {
            "requests_total": self.request_count,
            "uptime_seconds": time.time() - self.start_time
        }
    
    def get_metrics(self) -> Dict[str, Any]:
        return {
            "status": "available",
            "metrics": self.collect_metrics(),
            "timestamp": time.time()
        }
    
    def record_request(self):
        self.request_count += 1

# Global metrics collector
metrics_collector = MetricsCollector()

async def metrics_middleware(request: Request, call_next: Callable) -> Response:
    """Middleware to collect request metrics"""
    metrics_collector.record_request()
    response = await call_next(request)
    return response