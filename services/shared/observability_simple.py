"""Simple Observability Module for BHIV HR Platform"""

import logging
from typing import Any, Dict, Optional
from fastapi import FastAPI

logger = logging.getLogger(__name__)

def setup_simple_observability(app: FastAPI, service_name: str, version: str) -> None:
    """Setup simple observability for the service"""
    try:
        logger.info(f"Observability initialized for {service_name} v{version}")
        
        # Add basic middleware for request tracking
        @app.middleware("http")
        async def observability_middleware(request, call_next):
            response = await call_next(request)
            return response
            
    except Exception as e:
        logger.warning(f"Observability setup failed: {e}")