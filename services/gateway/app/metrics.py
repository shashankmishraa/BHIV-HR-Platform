"""Metrics module for gateway service"""

import logging
from typing import Dict, Any, Callable
from datetime import datetime, timezone
from fastapi import Request, Response
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

class MetricsCollector:
    """Simple metrics collector"""
    
    def __init__(self):
        self.request_count = 0
        self.error_count = 0
    
    def record_request(self, method: str, path: str, status_code: int, duration: float):
        """Record request metrics"""
        self.request_count += 1
        if status_code >= 400:
            self.error_count += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics"""
        return {
            "requests_total": self.request_count,
            "errors_total": self.error_count,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

# Global metrics collector
metrics_collector = MetricsCollector()

def get_metrics_response() -> Response:
    """Get metrics response"""
    try:
        metrics = metrics_collector.get_metrics()
        return JSONResponse(content=metrics)
    except Exception as e:
        logger.error(f"Metrics error: {e}")
        return JSONResponse(content={"error": "metrics unavailable"})

async def metrics_middleware(request: Request, call_next: Callable) -> Response:
    """Metrics middleware"""
    import time
    start_time = time.time()
    
    try:
        response = await call_next(request)
        duration = time.time() - start_time
        
        metrics_collector.record_request(
            request.method,
            request.url.path,
            response.status_code,
            duration
        )
        
        return response
    except Exception as e:
        logger.error(f"Metrics middleware error: {e}")
        return await call_next(request)