"""Simple Observability Module for BHIV HR Gateway"""

import logging
from typing import Any, Dict, Optional
from fastapi import FastAPI

logger = logging.getLogger(__name__)

def setup_simple_observability(app: FastAPI, service_name: str, version: str) -> None:
    """Setup basic observability for the service"""
    logger.info(f"Initializing observability for {service_name} v{version}")
    
    # Add basic health check endpoint if not exists
    @app.get("/observability/status")
    async def observability_status():
        return {
            "service": service_name,
            "version": version,
            "observability": "active",
            "timestamp": "2025-01-27T00:00:00Z"
        }
    
    logger.info("Simple observability initialized successfully")