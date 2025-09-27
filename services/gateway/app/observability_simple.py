"""
Local observability module for Gateway service
Provides basic health checks and metrics without external dependencies
"""

import logging
import time
from datetime import datetime, timezone
from typing import Dict, Any

logger = logging.getLogger(__name__)

def setup_simple_observability(app, service_name: str, version: str):
    """Setup simple observability framework"""
    
    logger.info(f"Local observability setup for {service_name} v{version}")
    
    # Add basic middleware for request tracking
    @app.middleware("http")
    async def observability_middleware(request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(round(process_time, 4))
        return response
    
    return None, None, None, None  # metrics, health, alert, tracer