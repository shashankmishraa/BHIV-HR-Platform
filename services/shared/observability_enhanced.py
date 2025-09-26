"""
Enhanced Production Observability Framework
Comprehensive monitoring, metrics, tracing, and alerting
"""

import asyncio
import json
import logging
import time
import traceback
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Callable
import threading
from contextlib import contextmanager
from dataclasses import dataclass, asdict
from enum import Enum

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

try:
    from prometheus_client import (
        Counter, Histogram, Gauge, Summary, Info,
        generate_latest, CONTENT_TYPE_LATEST,
        CollectorRegistry, multiprocess, values
    )
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False

try:
    import structlog
    STRUCTLOG_AVAILABLE = True
except ImportError:
    STRUCTLOG_AVAILABLE = False
    
try:
    from opentelemetry import trace, metrics
    from opentelemetry.exporter.prometheus import PrometheusMetricReader
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.trace import TracerProvider
    OPENTELEMETRY_AVAILABLE = True
except ImportError:
    OPENTELEMETRY_AVAILABLE = False

class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

@dataclass
class MetricPoint:
    name: str
    value: float
    labels: Dict[str, str]
    timestamp: datetime
    unit: str = ""

@dataclass
class Alert:
    id: str
    severity: AlertSeverity
    service: str
    metric: str
    message: str
    value: float
    threshold: float
    timestamp: datetime
    resolved: bool = False

class EnhancedMetricsCollector:
    """Enhanced metrics collection with multiple backends"""
    
    def __init__(self, service_name: str, enable_prometheus: bool = True):
        self.service_name = service_name
        self.enable_prometheus = enable_prometheus
        self.custom_metrics: Dict[str, List[MetricPoint]] = {}
        self._lock = threading.Lock()
        
        # Initialize Prometheus metrics if available
        if PROMETHEUS_AVAILABLE and enable_prometheus:
            self._init_prometheus_metrics()
        
        # Initialize OpenTelemetry if available
        if OPENTELEMETRY_AVAILABLE:
            self._init_opentelemetry()
    
    def _init_prometheus_metrics(self):
        """Initialize Prometheus metrics"""
        self.request_counter = Counter(
            'http_requests_total',
            'Total HTTP requests',
            ['service', 'method', 'endpoint', 'status_code']
        )
        
        self.request_duration = Histogram(
            'http_request_duration_seconds',
            'HTTP request duration',
            ['service', 'method', 'endpoint'],
            buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
        )
        
        self.active_connections = Gauge(
            'active_connections_total',
            'Active connections',
            ['service', 'connection_type']
        )
        
        self.error_counter = Counter(
            'errors_total',
            'Total errors',
            ['service', 'error_type', 'severity']
        )
        
        self.system_cpu = Gauge('system_cpu_percent', 'CPU usage percentage', ['service'])
        self.system_memory = Gauge('system_memory_bytes', 'Memory usage in bytes', ['service', 'type'])
        self.system_disk = Gauge('system_disk_percent', 'Disk usage percentage', ['service'])
        
        self.business_metrics = Counter(
            'business_operations_total',
            'Business operations',
            ['service', 'operation', 'status']
        )
        
        self.async_tasks = Gauge(
            'async_tasks_active',
            'Active async tasks',
            ['service', 'task_type']
        )
        
        self.database_operations = Histogram(
            'database_operation_duration_seconds',
            'Database operation duration',
            ['service', 'operation', 'table']
        )
    
    def _init_opentelemetry(self):
        """Initialize OpenTelemetry tracing and metrics"""
        self.tracer = trace.get_tracer(self.service_name)
        self.meter = metrics.get_meter(self.service_name)
    
    def record_request(self, method: str, endpoint: str, status_code: int, duration: float):
        """Record HTTP request metrics"""
        if PROMETHEUS_AVAILABLE and hasattr(self, 'request_counter'):
            self.request_counter.labels(
                service=self.service_name,
                method=method,
                endpoint=endpoint,
                status_code=str(status_code)
            ).inc()
            
            self.request_duration.labels(
                service=self.service_name,
                method=method,
                endpoint=endpoint
            ).observe(duration)
    
    def record_error(self, error_type: str, severity: str = "error"):
        """Record error occurrence"""
        if PROMETHEUS_AVAILABLE and hasattr(self, 'error_counter'):
            self.error_counter.labels(
                service=self.service_name,
                error_type=error_type,
                severity=severity
            ).inc()
    
    def update_system_metrics(self):
        """Update system resource metrics"""
        if not PSUTIL_AVAILABLE or not PROMETHEUS_AVAILABLE:
            return
            
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=0.1)
            self.system_cpu.labels(service=self.service_name).set(cpu_percent)
            
            # Memory metrics
            memory = psutil.virtual_memory()
            self.system_memory.labels(service=self.service_name, type='used').set(memory.used)
            self.system_memory.labels(service=self.service_name, type='available').set(memory.available)
            
            # Disk metrics
            disk = psutil.disk_usage('/')
            self.system_disk.labels(service=self.service_name).set(disk.percent)
            
        except Exception as e:
            logging.error(f"Error updating system metrics: {e}")
    
    def record_business_operation(self, operation: str, status: str = "success"):
        """Record business operation metrics"""
        if PROMETHEUS_AVAILABLE and hasattr(self, 'business_metrics'):
            self.business_metrics.labels(
                service=self.service_name,
                operation=operation,
                status=status
            ).inc()
    
    def record_async_task(self, task_type: str, count: int):
        """Record async task metrics"""
        if PROMETHEUS_AVAILABLE and hasattr(self, 'async_tasks'):
            self.async_tasks.labels(
                service=self.service_name,
                task_type=task_type
            ).set(count)
    
    def record_database_operation(self, operation: str, table: str, duration: float):
        """Record database operation metrics"""
        if PROMETHEUS_AVAILABLE and hasattr(self, 'database_operations'):
            self.database_operations.labels(
                service=self.service_name,
                operation=operation,
                table=table
            ).observe(duration)
    
    def add_custom_metric(self, name: str, value: float, labels: Dict[str, str] = None, unit: str = ""):
        """Add custom metric point"""
        with self._lock:
            if name not in self.custom_metrics:
                self.custom_metrics[name] = []
            
            metric_point = MetricPoint(
                name=name,
                value=value,
                labels=labels or {},
                timestamp=datetime.now(timezone.utc),
                unit=unit
            )
            
            self.custom_metrics[name].append(metric_point)
            
            # Keep only last 1000 points per metric
            if len(self.custom_metrics[name]) > 1000:
                self.custom_metrics[name] = self.custom_metrics[name][-1000:]
    
    def get_prometheus_metrics(self) -> str:
        """Get Prometheus formatted metrics"""
        if not PROMETHEUS_AVAILABLE:
            return "# Prometheus not available\n"
        
        self.update_system_metrics()
        return generate_latest()
    
    def get_custom_metrics(self) -> Dict[str, Any]:
        """Get custom metrics in JSON format"""
        with self._lock:
            return {
                name: [asdict(point) for point in points[-10:]]  # Last 10 points
                for name, points in self.custom_metrics.items()
            }

class EnhancedHealthChecker:
    """Enhanced health checking with dependency management"""
    
    def __init__(self, service_name: str, version: str):
        self.service_name = service_name
        self.version = version
        self.start_time = datetime.now(timezone.utc)
        self.dependencies: Dict[str, Callable] = {}
        self.health_history: List[Dict[str, Any]] = []
        self._lock = threading.Lock()
    
    def add_dependency(self, name: str, check_func: Callable, timeout: float = 5.0):
        """Add dependency health check with timeout"""
        async def wrapped_check():
            try:
                if asyncio.iscoroutinefunction(check_func):
                    return await asyncio.wait_for(check_func(), timeout=timeout)
                else:
                    return check_func()
            except asyncio.TimeoutError:
                return {"status": "timeout", "error": f"Health check timed out after {timeout}s"}
            except Exception as e:
                return {"status": "error", "error": str(e)}
        
        self.dependencies[name] = wrapped_check
    
    async def get_health_status(self, detailed: bool = False) -> Dict[str, Any]:
        """Get comprehensive health status"""
        uptime_seconds = (datetime.now(timezone.utc) - self.start_time).total_seconds()
        
        status = {
            "status": "healthy",
            "service": self.service_name,
            "version": self.version,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "uptime_seconds": round(uptime_seconds, 2)
        }
        
        if detailed:
            # Check dependencies
            dependency_results = {}
            overall_healthy = True
            
            for dep_name, check_func in self.dependencies.items():
                try:
                    dep_result = await check_func()
                    dependency_results[dep_name] = dep_result
                    
                    if dep_result.get("status") not in ["healthy", "ok", "connected"]:
                        overall_healthy = False
                        
                except Exception as e:
                    dependency_results[dep_name] = {
                        "status": "error",
                        "error": str(e)
                    }
                    overall_healthy = False
            
            status["dependencies"] = dependency_results
            status["status"] = "healthy" if overall_healthy else "degraded"
            
            # Add system information
            if PSUTIL_AVAILABLE:
                try:
                    status["system"] = {
                        "cpu_percent": psutil.cpu_percent(),
                        "memory_percent": psutil.virtual_memory().percent,
                        "disk_percent": psutil.disk_usage('/').percent,
                        "load_average": psutil.getloadavg() if hasattr(psutil, 'getloadavg') else None
                    }
                except Exception as e:
                    status["system"] = {"error": str(e)}
            
            # Add process information
            try:
                process = psutil.Process()
                status["process"] = {
                    "pid": process.pid,
                    "memory_mb": process.memory_info().rss / 1024 / 1024,
                    "cpu_percent": process.cpu_percent(),
                    "threads": process.num_threads(),
                    "open_files": len(process.open_files()) if hasattr(process, 'open_files') else 0
                }
            except Exception as e:
                status["process"] = {"error": str(e)}
        
        # Store health history
        with self._lock:
            self.health_history.append({
                "timestamp": status["timestamp"],
                "status": status["status"],
                "uptime": uptime_seconds
            })
            
            # Keep only last 100 health checks
            if len(self.health_history) > 100:
                self.health_history = self.health_history[-100:]
        
        return status
    
    def get_health_history(self) -> List[Dict[str, Any]]:
        """Get health check history"""
        with self._lock:
            return self.health_history.copy()

class AlertManager:
    """Enhanced alerting system"""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.alerts: Dict[str, Alert] = {}
        self.alert_rules: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()
        
        # Default alert rules
        self.add_alert_rule("high_cpu", "cpu_percent", 80.0, AlertSeverity.WARNING)
        self.add_alert_rule("critical_cpu", "cpu_percent", 95.0, AlertSeverity.CRITICAL)
        self.add_alert_rule("high_memory", "memory_percent", 85.0, AlertSeverity.WARNING)
        self.add_alert_rule("critical_memory", "memory_percent", 95.0, AlertSeverity.CRITICAL)
        self.add_alert_rule("high_error_rate", "error_rate", 0.05, AlertSeverity.ERROR)
    
    def add_alert_rule(self, rule_name: str, metric: str, threshold: float, severity: AlertSeverity):
        """Add alert rule"""
        self.alert_rules[rule_name] = {
            "metric": metric,
            "threshold": threshold,
            "severity": severity
        }
    
    def check_alerts(self, metrics: Dict[str, float]) -> List[Alert]:
        """Check metrics against alert rules"""
        new_alerts = []
        
        with self._lock:
            for rule_name, rule in self.alert_rules.items():
                metric_name = rule["metric"]
                threshold = rule["threshold"]
                severity = rule["severity"]
                
                if metric_name in metrics:
                    value = metrics[metric_name]
                    
                    # Check if alert should be triggered
                    should_alert = value > threshold
                    alert_id = f"{self.service_name}_{rule_name}"
                    
                    existing_alert = self.alerts.get(alert_id)
                    
                    if should_alert and (not existing_alert or existing_alert.resolved):
                        # Create new alert
                        alert = Alert(
                            id=alert_id,
                            severity=severity,
                            service=self.service_name,
                            metric=metric_name,
                            message=f"{metric_name} is {value}, exceeding threshold {threshold}",
                            value=value,
                            threshold=threshold,
                            timestamp=datetime.now(timezone.utc)
                        )
                        
                        self.alerts[alert_id] = alert
                        new_alerts.append(alert)
                        
                    elif not should_alert and existing_alert and not existing_alert.resolved:
                        # Resolve existing alert
                        existing_alert.resolved = True
        
        return new_alerts
    
    def get_active_alerts(self) -> List[Alert]:
        """Get all active alerts"""
        with self._lock:
            return [alert for alert in self.alerts.values() if not alert.resolved]

class DistributedTracing:
    """Distributed tracing implementation"""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.active_spans: Dict[str, Dict[str, Any]] = {}
        
    @contextmanager
    def trace_operation(self, operation_name: str, **tags):
        """Trace an operation"""
        span_id = str(uuid.uuid4())
        start_time = time.time()
        
        span_data = {
            "span_id": span_id,
            "operation_name": operation_name,
            "service_name": self.service_name,
            "start_time": start_time,
            "tags": tags
        }
        
        self.active_spans[span_id] = span_data
        
        try:
            yield span_id
        except Exception as e:
            span_data["error"] = str(e)
            span_data["error_type"] = type(e).__name__
            raise
        finally:
            span_data["end_time"] = time.time()
            span_data["duration"] = span_data["end_time"] - start_time
            # In production, this would be sent to a tracing backend
            logging.info(f"Trace completed: {json.dumps(span_data)}")
            self.active_spans.pop(span_id, None)

def setup_enhanced_observability(app, service_name: str, version: str) -> tuple:
    """Setup enhanced observability for a service"""
    
    # Initialize components
    metrics_collector = EnhancedMetricsCollector(service_name)
    health_checker = EnhancedHealthChecker(service_name, version)
    alert_manager = AlertManager(service_name)
    tracer = DistributedTracing(service_name)
    
    # Add observability middleware
    @app.middleware("http")
    async def observability_middleware(request, call_next):
        start_time = time.time()
        correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
        
        # Add correlation ID to request state
        request.state.correlation_id = correlation_id
        
        # Start tracing
        with tracer.trace_operation(
            f"{request.method} {request.url.path}",
            method=request.method,
            path=request.url.path,
            correlation_id=correlation_id
        ):
            try:
                response = await call_next(request)
                duration = time.time() - start_time
                
                # Record metrics
                metrics_collector.record_request(
                    request.method,
                    request.url.path,
                    response.status_code,
                    duration
                )
                
                # Add response headers
                response.headers["X-Correlation-ID"] = correlation_id
                response.headers["X-Response-Time"] = str(duration)
                response.headers["X-Service"] = service_name
                
                return response
                
            except Exception as e:
                duration = time.time() - start_time
                
                # Record error
                metrics_collector.record_error(type(e).__name__)
                
                # Log error with correlation ID
                logging.error(
                    f"Request failed: {e}",
                    extra={
                        "correlation_id": correlation_id,
                        "method": request.method,
                        "path": request.url.path,
                        "duration": duration
                    }
                )
                raise
    
    # Add health endpoints
    @app.get("/health")
    async def health_check():
        status = await health_checker.get_health_status()
        return status
    
    @app.get("/health/detailed")
    async def detailed_health_check():
        status = await health_checker.get_health_status(detailed=True)
        return status
    
    @app.get("/metrics")
    async def prometheus_metrics():
        from fastapi.responses import PlainTextResponse
        metrics = metrics_collector.get_prometheus_metrics()
        return PlainTextResponse(metrics, media_type=CONTENT_TYPE_LATEST if PROMETHEUS_AVAILABLE else "text/plain")
    
    @app.get("/metrics/custom")
    async def custom_metrics():
        return metrics_collector.get_custom_metrics()
    
    @app.get("/alerts")
    async def get_alerts():
        return [asdict(alert) for alert in alert_manager.get_active_alerts()]
    
    return metrics_collector, health_checker, alert_manager, tracer