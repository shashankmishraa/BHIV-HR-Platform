"""Prometheus metrics integration for BHIV HR Platform"""

from prometheus_client import (
    Counter,
    Histogram,
    Gauge,
    generate_latest,
    CONTENT_TYPE_LATEST,
)
from fastapi import Request, Response
import time
import psutil
import os

# Metrics definitions
REQUEST_COUNT = Counter(
    "api_requests_total", "Total API requests", ["method", "endpoint", "status_code"]
)

REQUEST_DURATION = Histogram(
    "api_request_duration_seconds",
    "Request duration in seconds",
    ["method", "endpoint"],
)

ACTIVE_WORKFLOWS = Gauge("active_workflows_total", "Number of active workflows")

WORKFLOW_EXECUTIONS = Counter(
    "workflow_executions_total",
    "Total workflow executions",
    ["workflow_type", "status"],
)

SYSTEM_MEMORY_USAGE = Gauge("system_memory_usage_bytes", "System memory usage in bytes")

SYSTEM_CPU_USAGE = Gauge("system_cpu_usage_percent", "System CPU usage percentage")

DATABASE_CONNECTIONS = Gauge(
    "database_connections_active", "Active database connections"
)

ERROR_COUNT = Counter(
    "api_errors_total", "Total API errors", ["error_type", "endpoint"]
)


class MetricsCollector:
    """Metrics collection and management"""

    def __init__(self):
        self.start_time = time.time()

    def record_request(
        self, method: str, endpoint: str, status_code: int, duration: float
    ):
        """Record API request metrics"""
        REQUEST_COUNT.labels(
            method=method, endpoint=endpoint, status_code=status_code
        ).inc()
        REQUEST_DURATION.labels(method=method, endpoint=endpoint).observe(duration)

    def record_workflow_execution(self, workflow_type: str, status: str):
        """Record workflow execution metrics"""
        WORKFLOW_EXECUTIONS.labels(workflow_type=workflow_type, status=status).inc()

    def update_active_workflows(self, count: int):
        """Update active workflows count"""
        ACTIVE_WORKFLOWS.set(count)

    def record_error(self, error_type: str, endpoint: str):
        """Record error metrics"""
        ERROR_COUNT.labels(error_type=error_type, endpoint=endpoint).inc()

    def update_system_metrics(self):
        """Update system resource metrics"""
        try:
            # Memory usage
            memory = psutil.virtual_memory()
            SYSTEM_MEMORY_USAGE.set(memory.used)

            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            SYSTEM_CPU_USAGE.set(cpu_percent)

        except Exception as e:
            print(f"Error updating system metrics: {e}")

    def get_uptime(self) -> float:
        """Get system uptime in seconds"""
        return time.time() - self.start_time


# Global metrics collector
metrics_collector = MetricsCollector()


async def metrics_middleware(request: Request, call_next):
    """Middleware to collect request metrics"""
    start_time = time.time()

    # Process request
    response = await call_next(request)

    # Calculate duration
    duration = time.time() - start_time

    # Record metrics
    endpoint = request.url.path
    method = request.method
    status_code = response.status_code

    metrics_collector.record_request(method, endpoint, status_code, duration)

    # Record errors
    if status_code >= 400:
        error_type = "client_error" if status_code < 500 else "server_error"
        metrics_collector.record_error(error_type, endpoint)

    return response


def get_metrics_response() -> Response:
    """Get Prometheus metrics response"""
    # Update system metrics before generating response
    metrics_collector.update_system_metrics()

    # Generate metrics
    metrics_data = generate_latest()

    return Response(content=metrics_data, media_type=CONTENT_TYPE_LATEST)


def get_metrics_summary() -> dict:
    """Get metrics summary for dashboard"""
    return {
        "uptime_seconds": metrics_collector.get_uptime(),
        "total_requests": REQUEST_COUNT._value.sum(),
        "active_workflows": ACTIVE_WORKFLOWS._value.get(),
        "total_workflow_executions": WORKFLOW_EXECUTIONS._value.sum(),
        "total_errors": ERROR_COUNT._value.sum(),
        "system_metrics": {
            "memory_usage_bytes": SYSTEM_MEMORY_USAGE._value.get(),
            "cpu_usage_percent": SYSTEM_CPU_USAGE._value.get(),
        },
    }
