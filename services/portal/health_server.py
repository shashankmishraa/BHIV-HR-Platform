"""
Health Check Server for HR Portal
Provides standardized health endpoints for monitoring
"""

import asyncio
import json
import logging
import threading
import time
from datetime import datetime, timezone
from typing import Dict, Any

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import psutil
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PortalHealthServer:
    def __init__(self, port: int = 8503):
        self.port = port
        self.app = FastAPI(title="HR Portal Health Server", version="1.0.0")
        self.start_time = datetime.now(timezone.utc)
        self.setup_routes()
    
    def setup_routes(self):
        """Setup health check routes"""
        
        @self.app.get("/health")
        async def health_check():
            """Simple health check"""
            return JSONResponse({
                "status": "healthy",
                "service": "BHIV HR Portal",
                "version": "1.0.0",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "uptime_seconds": (datetime.now(timezone.utc) - self.start_time).total_seconds()
            })
        
        @self.app.get("/health/detailed")
        async def detailed_health_check():
            """Detailed health check with dependencies"""
            status = {
                "status": "healthy",
                "service": "BHIV HR Portal",
                "version": "1.0.0",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "uptime_seconds": (datetime.now(timezone.utc) - self.start_time).total_seconds(),
                "dependencies": {},
                "system": {
                    "cpu_percent": psutil.cpu_percent(),
                    "memory_percent": psutil.virtual_memory().percent,
                    "disk_percent": psutil.disk_usage('/').percent
                }
            }
            
            # Check Gateway connectivity
            try:
                gateway_url = "https://bhiv-hr-gateway-901a.onrender.com/health"
                response = requests.get(gateway_url, timeout=5)
                if response.status_code == 200:
                    status["dependencies"]["gateway"] = {
                        "status": "healthy",
                        "response_time_ms": response.elapsed.total_seconds() * 1000
                    }
                else:
                    status["dependencies"]["gateway"] = {
                        "status": "unhealthy",
                        "status_code": response.status_code
                    }
                    status["status"] = "degraded"
            except Exception as e:
                status["dependencies"]["gateway"] = {
                    "status": "unhealthy",
                    "error": str(e)
                }
                status["status"] = "degraded"
            
            return JSONResponse(status)
        
        @self.app.get("/health/ready")
        async def readiness_check():
            """Kubernetes readiness probe"""
            return JSONResponse({"status": "ready"})
        
        @self.app.get("/health/live")
        async def liveness_check():
            """Kubernetes liveness probe"""
            return JSONResponse({"status": "alive"})
        
        @self.app.get("/metrics/json")
        async def json_metrics():
            """JSON formatted metrics"""
            return {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "service": "BHIV HR Portal",
                "system": {
                    "cpu_percent": psutil.cpu_percent(),
                    "memory_percent": psutil.virtual_memory().percent,
                    "memory_used_mb": psutil.virtual_memory().used / 1024 / 1024,
                    "disk_percent": psutil.disk_usage('/').percent
                },
                "uptime_seconds": (datetime.now(timezone.utc) - self.start_time).total_seconds()
            }
    
    def run(self):
        """Run the health server"""
        logger.info(f"Starting HR Portal Health Server on port {self.port}")
        uvicorn.run(self.app, host="0.0.0.0", port=self.port, log_level="info")

def start_health_server(port: int = 8503):
    """Start health server in background thread"""
    health_server = PortalHealthServer(port)
    
    def run_server():
        health_server.run()
    
    health_thread = threading.Thread(target=run_server, daemon=True)
    health_thread.start()
    logger.info(f"HR Portal Health Server started on port {port}")
    return health_thread

if __name__ == "__main__":
    # Run standalone
    health_server = PortalHealthServer()
    health_server.run()