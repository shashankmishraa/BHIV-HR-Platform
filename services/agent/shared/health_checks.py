#!/usr/bin/env python3
"""
BHIV HR Platform - Enhanced Health Check System
Comprehensive dependency validation and system monitoring
"""

import asyncio
import time
import psutil
import socket
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import aiohttp
import asyncpg
import redis
from pathlib import Path
import json

class HealthStatus(Enum):
    """Health check status levels"""
    HEALTHY = "healthy"
    DEGRADED = "degraded" 
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"

@dataclass
class HealthCheckResult:
    """Individual health check result"""
    name: str
    status: HealthStatus
    response_time_ms: float
    message: str
    details: Dict[str, Any]
    timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        result = asdict(self)
        result['status'] = self.status.value
        result['timestamp'] = self.timestamp.isoformat()
        return result

@dataclass
class SystemHealth:
    """Overall system health summary"""
    status: HealthStatus
    checks: List[HealthCheckResult]
    response_time_ms: float
    timestamp: datetime
    uptime_seconds: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'status': self.status.value,
            'checks': [check.to_dict() for check in self.checks],
            'response_time_ms': self.response_time_ms,
            'timestamp': self.timestamp.isoformat(),
            'uptime_seconds': self.uptime_seconds,
            'summary': {
                'total_checks': len(self.checks),
                'healthy_checks': len([c for c in self.checks if c.status == HealthStatus.HEALTHY]),
                'degraded_checks': len([c for c in self.checks if c.status == HealthStatus.DEGRADED]),
                'unhealthy_checks': len([c for c in self.checks if c.status == HealthStatus.UNHEALTHY])
            }
        }

class BaseHealthCheck:
    """Base class for health checks"""
    
    def __init__(self, name: str, timeout: float = 5.0):
        self.name = name
        self.timeout = timeout
    
    async def check(self) -> HealthCheckResult:
        """Execute health check"""
        start_time = time.time()
        
        try:
            result = await asyncio.wait_for(self._execute_check(), timeout=self.timeout)
            response_time = (time.time() - start_time) * 1000
            
            return HealthCheckResult(
                name=self.name,
                status=result.get('status', HealthStatus.UNKNOWN),
                response_time_ms=response_time,
                message=result.get('message', 'Check completed'),
                details=result.get('details', {}),
                timestamp=datetime.now()
            )
            
        except asyncio.TimeoutError:
            response_time = (time.time() - start_time) * 1000
            return HealthCheckResult(
                name=self.name,
                status=HealthStatus.UNHEALTHY,
                response_time_ms=response_time,
                message=f"Health check timed out after {self.timeout}s",
                details={'timeout': self.timeout},
                timestamp=datetime.now()
            )
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            return HealthCheckResult(
                name=self.name,
                status=HealthStatus.UNHEALTHY,
                response_time_ms=response_time,
                message=f"Health check failed: {str(e)}",
                details={'error': str(e), 'error_type': type(e).__name__},
                timestamp=datetime.now()
            )
    
    async def _execute_check(self) -> Dict[str, Any]:
        """Override this method in subclasses"""
        raise NotImplementedError

class DatabaseHealthCheck(BaseHealthCheck):
    """PostgreSQL database health check"""
    
    def __init__(self, connection_string: str, name: str = "database"):
        super().__init__(name)
        self.connection_string = connection_string
    
    async def _execute_check(self) -> Dict[str, Any]:
        """Check database connectivity and performance"""
        try:
            conn = await asyncpg.connect(self.connection_string)
            
            # Test basic connectivity
            await conn.execute("SELECT 1")
            
            # Check connection pool status
            pool_info = await conn.fetchrow("""
                SELECT 
                    count(*) as total_connections,
                    count(*) FILTER (WHERE state = 'active') as active_connections,
                    count(*) FILTER (WHERE state = 'idle') as idle_connections
                FROM pg_stat_activity 
                WHERE datname = current_database()
            """)
            
            # Check database size and performance
            db_stats = await conn.fetchrow("""
                SELECT 
                    pg_database_size(current_database()) as db_size_bytes,
                    (SELECT count(*) FROM pg_stat_activity WHERE state = 'active') as active_queries
            """)
            
            await conn.close()
            
            # Determine status based on metrics
            status = HealthStatus.HEALTHY
            if pool_info['active_connections'] > 50:
                status = HealthStatus.DEGRADED
            if pool_info['active_connections'] > 80:
                status = HealthStatus.UNHEALTHY
            
            return {
                'status': status,
                'message': f"Database healthy - {pool_info['active_connections']} active connections",
                'details': {
                    'total_connections': pool_info['total_connections'],
                    'active_connections': pool_info['active_connections'],
                    'idle_connections': pool_info['idle_connections'],
                    'database_size_mb': round(db_stats['db_size_bytes'] / (1024*1024), 2),
                    'active_queries': db_stats['active_queries']
                }
            }
            
        except Exception as e:
            return {
                'status': HealthStatus.UNHEALTHY,
                'message': f"Database connection failed: {str(e)}",
                'details': {'error': str(e)}
            }

class RedisHealthCheck(BaseHealthCheck):
    """Redis cache health check"""
    
    def __init__(self, redis_url: str, name: str = "redis"):
        super().__init__(name)
        self.redis_url = redis_url
    
    async def _execute_check(self) -> Dict[str, Any]:
        """Check Redis connectivity and performance"""
        try:
            r = redis.from_url(self.redis_url)
            
            # Test basic connectivity
            await r.ping()
            
            # Get Redis info
            info = await r.info()
            memory_usage = info.get('used_memory', 0)
            max_memory = info.get('maxmemory', 0)
            connected_clients = info.get('connected_clients', 0)
            
            # Determine status
            status = HealthStatus.HEALTHY
            if max_memory > 0 and memory_usage / max_memory > 0.8:
                status = HealthStatus.DEGRADED
            if connected_clients > 100:
                status = HealthStatus.DEGRADED
            
            await r.close()
            
            return {
                'status': status,
                'message': f"Redis healthy - {connected_clients} clients connected",
                'details': {
                    'connected_clients': connected_clients,
                    'used_memory_mb': round(memory_usage / (1024*1024), 2),
                    'memory_usage_percent': round((memory_usage / max_memory * 100), 2) if max_memory > 0 else 0,
                    'redis_version': info.get('redis_version', 'unknown')
                }
            }
            
        except Exception as e:
            return {
                'status': HealthStatus.UNHEALTHY,
                'message': f"Redis connection failed: {str(e)}",
                'details': {'error': str(e)}
            }

class HTTPServiceHealthCheck(BaseHealthCheck):
    """HTTP service dependency health check"""
    
    def __init__(self, url: str, name: str, expected_status: int = 200):
        super().__init__(name)
        self.url = url
        self.expected_status = expected_status
    
    async def _execute_check(self) -> Dict[str, Any]:
        """Check HTTP service availability"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url) as response:
                    status_code = response.status
                    response_text = await response.text()
                    
                    # Determine health status
                    if status_code == self.expected_status:
                        status = HealthStatus.HEALTHY
                        message = f"Service responding normally (HTTP {status_code})"
                    elif 200 <= status_code < 300:
                        status = HealthStatus.HEALTHY
                        message = f"Service responding (HTTP {status_code})"
                    elif 400 <= status_code < 500:
                        status = HealthStatus.DEGRADED
                        message = f"Service client error (HTTP {status_code})"
                    else:
                        status = HealthStatus.UNHEALTHY
                        message = f"Service error (HTTP {status_code})"
                    
                    return {
                        'status': status,
                        'message': message,
                        'details': {
                            'status_code': status_code,
                            'url': self.url,
                            'response_length': len(response_text)
                        }
                    }
                    
        except Exception as e:
            return {
                'status': HealthStatus.UNHEALTHY,
                'message': f"Service unreachable: {str(e)}",
                'details': {'error': str(e), 'url': self.url}
            }

class SystemResourcesHealthCheck(BaseHealthCheck):
    """System resources health check"""
    
    def __init__(self, name: str = "system_resources"):
        super().__init__(name)
    
    async def _execute_check(self) -> Dict[str, Any]:
        """Check system resource utilization"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            
            # Disk usage
            try:
                disk = psutil.disk_usage('/')
            except:
                disk = psutil.disk_usage('C:\\')
            
            # Network I/O
            network = psutil.net_io_counters()
            
            # Process count
            process_count = len(psutil.pids())
            
            # Determine overall status
            status = HealthStatus.HEALTHY
            issues = []
            
            if cpu_percent > 80:
                status = HealthStatus.DEGRADED
                issues.append(f"High CPU usage: {cpu_percent:.1f}%")
            
            if memory.percent > 85:
                status = HealthStatus.DEGRADED
                issues.append(f"High memory usage: {memory.percent:.1f}%")
            
            if disk.percent > 90:
                status = HealthStatus.DEGRADED
                issues.append(f"High disk usage: {disk.percent:.1f}%")
            
            if cpu_percent > 95 or memory.percent > 95:
                status = HealthStatus.UNHEALTHY
            
            message = "System resources normal"
            if issues:
                message = f"Resource issues detected: {', '.join(issues)}"
            
            return {
                'status': status,
                'message': message,
                'details': {
                    'cpu_percent': round(cpu_percent, 1),
                    'memory_percent': round(memory.percent, 1),
                    'memory_available_gb': round(memory.available / (1024**3), 2),
                    'disk_percent': round(disk.percent, 1),
                    'disk_free_gb': round(disk.free / (1024**3), 2),
                    'process_count': process_count,
                    'network_bytes_sent': network.bytes_sent,
                    'network_bytes_recv': network.bytes_recv
                }
            }
            
        except Exception as e:
            return {
                'status': HealthStatus.UNHEALTHY,
                'message': f"Failed to check system resources: {str(e)}",
                'details': {'error': str(e)}
            }

class AIModelHealthCheck(BaseHealthCheck):
    """AI model availability health check"""
    
    def __init__(self, model_path: str, name: str = "ai_model"):
        super().__init__(name)
        self.model_path = model_path
    
    async def _execute_check(self) -> Dict[str, Any]:
        """Check AI model availability and performance"""
        try:
            model_file = Path(self.model_path)
            
            if not model_file.exists():
                return {
                    'status': HealthStatus.UNHEALTHY,
                    'message': f"Model file not found: {self.model_path}",
                    'details': {'model_path': self.model_path, 'exists': False}
                }
            
            # Check file size and modification time
            file_stats = model_file.stat()
            file_size_mb = file_stats.st_size / (1024*1024)
            modified_time = datetime.fromtimestamp(file_stats.st_mtime)
            
            # Test model loading (mock - replace with actual model test)
            load_start = time.time()
            # model = load_model(self.model_path)  # Replace with actual loading
            load_time = (time.time() - load_start) * 1000
            
            status = HealthStatus.HEALTHY
            if load_time > 5000:  # 5 seconds
                status = HealthStatus.DEGRADED
            
            return {
                'status': status,
                'message': f"Model loaded successfully in {load_time:.0f}ms",
                'details': {
                    'model_path': self.model_path,
                    'file_size_mb': round(file_size_mb, 2),
                    'load_time_ms': round(load_time, 2),
                    'last_modified': modified_time.isoformat(),
                    'exists': True
                }
            }
            
        except Exception as e:
            return {
                'status': HealthStatus.UNHEALTHY,
                'message': f"Model check failed: {str(e)}",
                'details': {'error': str(e), 'model_path': self.model_path}
            }

class HealthCheckManager:
    """Manages and orchestrates health checks"""
    
    def __init__(self):
        self.checks: List[BaseHealthCheck] = []
        self.start_time = datetime.now()
    
    def add_check(self, check: BaseHealthCheck):
        """Add a health check"""
        self.checks.append(check)
    
    def add_database_check(self, connection_string: str, name: str = "database"):
        """Add database health check"""
        self.add_check(DatabaseHealthCheck(connection_string, name))
    
    def add_redis_check(self, redis_url: str, name: str = "redis"):
        """Add Redis health check"""
        self.add_check(RedisHealthCheck(redis_url, name))
    
    def add_http_service_check(self, url: str, name: str, expected_status: int = 200):
        """Add HTTP service health check"""
        self.add_check(HTTPServiceHealthCheck(url, name, expected_status))
    
    def add_system_resources_check(self):
        """Add system resources health check"""
        self.add_check(SystemResourcesHealthCheck())
    
    def add_ai_model_check(self, model_path: str, name: str = "ai_model"):
        """Add AI model health check"""
        self.add_check(AIModelHealthCheck(model_path, name))
    
    async def run_all_checks(self) -> SystemHealth:
        """Run all registered health checks"""
        start_time = time.time()
        
        # Run all checks concurrently
        check_tasks = [check.check() for check in self.checks]
        check_results = await asyncio.gather(*check_tasks, return_exceptions=True)
        
        # Process results
        results = []
        for i, result in enumerate(check_results):
            if isinstance(result, Exception):
                # Handle exceptions from individual checks
                results.append(HealthCheckResult(
                    name=self.checks[i].name,
                    status=HealthStatus.UNHEALTHY,
                    response_time_ms=0,
                    message=f"Check execution failed: {str(result)}",
                    details={'error': str(result)},
                    timestamp=datetime.now()
                ))
            else:
                results.append(result)
        
        # Determine overall system health
        overall_status = self._determine_overall_status(results)
        
        response_time = (time.time() - start_time) * 1000
        uptime = (datetime.now() - self.start_time).total_seconds()
        
        return SystemHealth(
            status=overall_status,
            checks=results,
            response_time_ms=response_time,
            timestamp=datetime.now(),
            uptime_seconds=uptime
        )
    
    def _determine_overall_status(self, results: List[HealthCheckResult]) -> HealthStatus:
        """Determine overall system health from individual check results"""
        if not results:
            return HealthStatus.UNKNOWN
        
        unhealthy_count = len([r for r in results if r.status == HealthStatus.UNHEALTHY])
        degraded_count = len([r for r in results if r.status == HealthStatus.DEGRADED])
        
        # If any critical checks are unhealthy, system is unhealthy
        if unhealthy_count > 0:
            return HealthStatus.UNHEALTHY
        
        # If any checks are degraded, system is degraded
        if degraded_count > 0:
            return HealthStatus.DEGRADED
        
        # All checks are healthy
        return HealthStatus.HEALTHY
    
    async def get_simple_health(self) -> Dict[str, Any]:
        """Get simple health status for basic endpoints"""
        system_health = await self.run_all_checks()
        
        return {
            'status': system_health.status.value,
            'timestamp': system_health.timestamp.isoformat(),
            'uptime_seconds': system_health.uptime_seconds,
            'checks_passed': len([c for c in system_health.checks if c.status == HealthStatus.HEALTHY]),
            'total_checks': len(system_health.checks)
        }
    
    async def get_detailed_health(self) -> Dict[str, Any]:
        """Get detailed health status with all check results"""
        system_health = await self.run_all_checks()
        return system_health.to_dict()

# Factory function for easy setup
def create_health_manager(config: Dict[str, Any]) -> HealthCheckManager:
    """Create health check manager with standard checks"""
    manager = HealthCheckManager()
    
    # Add system resources check
    manager.add_system_resources_check()
    
    # Add database check if configured
    if 'database_url' in config:
        manager.add_database_check(config['database_url'])
    
    # Add Redis check if configured
    if 'redis_url' in config:
        manager.add_redis_check(config['redis_url'])
    
    # Add service dependency checks
    for service in config.get('dependent_services', []):
        manager.add_http_service_check(
            service['url'], 
            service['name'], 
            service.get('expected_status', 200)
        )
    
    # Add AI model checks
    for model in config.get('ai_models', []):
        manager.add_ai_model_check(model['path'], model['name'])
    
    return manager