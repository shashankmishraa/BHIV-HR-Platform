from fastapi import FastAPI, HTTPException
from datetime import datetime, timezone
import psutil
import time
import logging
from typing import Dict, List
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SystemMonitor:
    def __init__(self):
        self.start_time = time.time()
        self.request_count = 0
        self.error_count = 0
        self.response_times = []
        self.api_latency = []
        self.resume_processing_errors = []
        
    def record_request(self, response_time: float, status_code: int):
        """Record API request metrics"""
        self.request_count += 1
        self.response_times.append(response_time)
        self.api_latency.append(response_time)
        
        if status_code >= 400:
            self.error_count += 1
            
        # Keep only last 1000 entries
        if len(self.response_times) > 1000:
            self.response_times = self.response_times[-1000:]
        if len(self.api_latency) > 1000:
            self.api_latency = self.api_latency[-1000:]
    
    def record_resume_error(self, error: str, file_name: str):
        """Record resume processing errors"""
        self.resume_processing_errors.append({
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'error': error,
            'file_name': file_name
        })
        
        # Keep only last 100 errors
        if len(self.resume_processing_errors) > 100:
            self.resume_processing_errors = self.resume_processing_errors[-100:]
    
    def get_metrics(self) -> Dict:
        """Get current system metrics"""
        uptime = time.time() - self.start_time
        
        # Calculate averages
        avg_response_time = sum(self.response_times) / len(self.response_times) if self.response_times else 0
        avg_api_latency = sum(self.api_latency) / len(self.api_latency) if self.api_latency else 0
        
        # System metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            'system': {
                'uptime_seconds': round(uptime, 2),
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_used_gb': round(memory.used / (1024**3), 2),
                'memory_total_gb': round(memory.total / (1024**3), 2),
                'disk_percent': disk.percent,
                'disk_used_gb': round(disk.used / (1024**3), 2),
                'disk_total_gb': round(disk.total / (1024**3), 2)
            },
            'api': {
                'total_requests': self.request_count,
                'error_count': self.error_count,
                'error_rate': round((self.error_count / self.request_count * 100) if self.request_count > 0 else 0, 2),
                'avg_response_time_ms': round(avg_response_time * 1000, 2),
                'avg_api_latency_ms': round(avg_api_latency * 1000, 2),
                'requests_per_minute': round((self.request_count / (uptime / 60)) if uptime > 0 else 0, 2)
            },
            'resume_processing': {
                'total_errors': len(self.resume_processing_errors),
                'recent_errors': self.resume_processing_errors[-10:] if self.resume_processing_errors else []
            },
            'timestamp': datetime.now(timezone.utc).isoformat()
        }

# Global monitor instance
monitor = SystemMonitor()

def add_monitoring_endpoints(app: FastAPI):
    """Add monitoring endpoints to FastAPI app"""
    
    @app.get("/metrics", tags=["Monitoring"])
    async def get_metrics():
        """Get comprehensive system metrics"""
        return monitor.get_metrics()
    
    @app.get("/metrics/dashboard", tags=["Monitoring"])
    async def get_dashboard_metrics():
        """Get metrics formatted for dashboard display"""
        metrics = monitor.get_metrics()
        
        return {
            'status': 'healthy' if metrics['system']['cpu_percent'] < 80 and metrics['system']['memory_percent'] < 80 else 'warning',
            'uptime': f"{metrics['system']['uptime_seconds']:.0f}s",
            'performance': {
                'cpu': f"{metrics['system']['cpu_percent']:.1f}%",
                'memory': f"{metrics['system']['memory_percent']:.1f}%",
                'disk': f"{metrics['system']['disk_percent']:.1f}%"
            },
            'api_health': {
                'requests': metrics['api']['total_requests'],
                'errors': metrics['api']['error_count'],
                'error_rate': f"{metrics['api']['error_rate']:.1f}%",
                'avg_latency': f"{metrics['api']['avg_response_time_ms']:.1f}ms"
            },
            'alerts': generate_alerts(metrics)
        }
    
    @app.get("/health/detailed", tags=["Monitoring"])
    async def detailed_health_check():
        """Detailed health check with component status"""
        metrics = monitor.get_metrics()
        
        # Component health checks
        components = {
            'api_server': 'healthy',
            'database': check_database_health(),
            'ai_agent': check_ai_agent_health(),
            'file_system': 'healthy' if metrics['system']['disk_percent'] < 90 else 'warning',
            'memory': 'healthy' if metrics['system']['memory_percent'] < 80 else 'warning',
            'cpu': 'healthy' if metrics['system']['cpu_percent'] < 80 else 'warning'
        }
        
        overall_status = 'healthy' if all(status == 'healthy' for status in components.values()) else 'degraded'
        
        return {
            'overall_status': overall_status,
            'components': components,
            'metrics': metrics,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }

def generate_alerts(metrics: Dict) -> List[Dict]:
    """Generate alerts based on metrics"""
    alerts = []
    
    # CPU alert
    if metrics['system']['cpu_percent'] > 80:
        alerts.append({
            'type': 'warning',
            'component': 'cpu',
            'message': f"High CPU usage: {metrics['system']['cpu_percent']:.1f}%",
            'threshold': '80%'
        })
    
    # Memory alert
    if metrics['system']['memory_percent'] > 80:
        alerts.append({
            'type': 'warning',
            'component': 'memory',
            'message': f"High memory usage: {metrics['system']['memory_percent']:.1f}%",
            'threshold': '80%'
        })
    
    # Disk alert
    if metrics['system']['disk_percent'] > 85:
        alerts.append({
            'type': 'warning',
            'component': 'disk',
            'message': f"High disk usage: {metrics['system']['disk_percent']:.1f}%",
            'threshold': '85%'
        })
    
    # Error rate alert
    if metrics['api']['error_rate'] > 5:
        alerts.append({
            'type': 'error',
            'component': 'api',
            'message': f"High error rate: {metrics['api']['error_rate']:.1f}%",
            'threshold': '5%'
        })
    
    # Response time alert
    if metrics['api']['avg_response_time_ms'] > 500:
        alerts.append({
            'type': 'warning',
            'component': 'api',
            'message': f"Slow response time: {metrics['api']['avg_response_time_ms']:.1f}ms",
            'threshold': '500ms'
        })
    
    return alerts

def check_database_health() -> str:
    """Check database connectivity"""
    try:
        import psycopg2
        import os
        
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "db"),
            database=os.getenv("DB_NAME", "bhiv_hr"),
            user=os.getenv("DB_USER", "bhiv_user"),
            password=os.getenv("DB_PASSWORD", "bhiv_pass"),
            port=os.getenv("DB_PORT", "5432"),
            connect_timeout=5
        )
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        conn.close()
        return 'healthy'
    except Exception:
        return 'unhealthy'

def check_ai_agent_health() -> str:
    """Check AI agent connectivity"""
    try:
        import httpx
        response = httpx.get("http://agent:9000/health", timeout=5)
        return 'healthy' if response.status_code == 200 else 'unhealthy'
    except Exception:
        return 'unhealthy'

# Middleware for request monitoring
async def monitoring_middleware(request, call_next):
    """Middleware to monitor API requests"""
    start_time = time.time()
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        monitor.record_request(process_time, response.status_code)
        
        # Add performance headers
        response.headers["X-Process-Time"] = str(round(process_time * 1000, 2))
        return response
        
    except Exception as e:
        process_time = time.time() - start_time
        monitor.record_request(process_time, 500)
        logger.error(f"Request failed: {str(e)}")
        raise