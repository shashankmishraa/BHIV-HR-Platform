"""
Performance Optimization Module
Handles caching, async operations, and performance monitoring
"""

import asyncio
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from functools import wraps
import json
import hashlib
from collections import defaultdict
import psutil

class PerformanceCache:
    """In-memory cache with TTL support"""
    
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._ttl: Dict[str, float] = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Get cached value if not expired"""
        if key in self._cache and key in self._ttl:
            if time.time() < self._ttl[key]:
                return self._cache[key]['value']
            else:
                # Expired, remove from cache
                self._cache.pop(key, None)
                self._ttl.pop(key, None)
        return None
    
    def set(self, key: str, value: Any, ttl_seconds: int = 300):
        """Set cached value with TTL"""
        self._cache[key] = {
            'value': value,
            'created_at': time.time()
        }
        self._ttl[key] = time.time() + ttl_seconds
    
    def clear(self):
        """Clear all cached values"""
        self._cache.clear()
        self._ttl.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        current_time = time.time()
        valid_entries = sum(1 for ttl in self._ttl.values() if current_time < ttl)
        expired_entries = len(self._ttl) - valid_entries
        
        return {
            "total_entries": len(self._cache),
            "valid_entries": valid_entries,
            "expired_entries": expired_entries,
            "cache_size_bytes": len(str(self._cache))
        }

class AsyncHealthChecker:
    """Async health checking with parallel execution"""
    
    def __init__(self, cache: PerformanceCache):
        self.cache = cache
        self.timeout = 5.0
    
    async def check_database_health(self, engine) -> Dict[str, Any]:
        """Check database health asynchronously"""
        try:
            loop = asyncio.get_event_loop()
            start_time = time.time()
            
            def db_check():
                with engine.connect() as conn:
                    conn.execute("SELECT 1")
                    return True
            
            result = await asyncio.wait_for(
                loop.run_in_executor(None, db_check),
                timeout=self.timeout
            )
            
            response_time = (time.time() - start_time) * 1000
            
            return {
                "status": "healthy",
                "response_time_ms": round(response_time, 2),
                "connection": "active"
            }
        except asyncio.TimeoutError:
            return {
                "status": "timeout",
                "response_time_ms": self.timeout * 1000,
                "connection": "timeout"
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "connection": "failed"
            }
    
    async def check_system_resources(self) -> Dict[str, Any]:
        """Check system resources asynchronously"""
        try:
            loop = asyncio.get_event_loop()
            
            def get_system_info():
                return {
                    "cpu_percent": psutil.cpu_percent(interval=0.1),
                    "memory_percent": psutil.virtual_memory().percent,
                    "disk_percent": psutil.disk_usage('/').percent if hasattr(psutil.disk_usage('/'), 'percent') else 0
                }
            
            system_info = await loop.run_in_executor(None, get_system_info)
            
            status = "healthy"
            if system_info["cpu_percent"] > 90 or system_info["memory_percent"] > 90:
                status = "warning"
            if system_info["cpu_percent"] > 95 or system_info["memory_percent"] > 95:
                status = "critical"
            
            return {
                "status": status,
                "cpu_usage": system_info["cpu_percent"],
                "memory_usage": system_info["memory_percent"],
                "disk_usage": system_info["disk_percent"],
                "response_time_ms": 100
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "response_time_ms": 0
            }
    
    async def check_external_service(self, url: str, name: str) -> Dict[str, Any]:
        """Check external service health"""
        import aiohttp
        
        try:
            start_time = time.time()
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url) as response:
                    response_time = (time.time() - start_time) * 1000
                    
                    return {
                        "name": name,
                        "status": "healthy" if response.status == 200 else "unhealthy",
                        "status_code": response.status,
                        "response_time_ms": round(response_time, 2),
                        "url": url
                    }
        except asyncio.TimeoutError:
            return {
                "name": name,
                "status": "timeout",
                "response_time_ms": self.timeout * 1000,
                "url": url
            }
        except Exception as e:
            return {
                "name": name,
                "status": "error",
                "error": str(e),
                "url": url
            }

class PerformanceMonitor:
    """Performance monitoring and metrics collection"""
    
    def __init__(self):
        self.request_times = defaultdict(list)
        self.error_counts = defaultdict(int)
        self.endpoint_stats = defaultdict(lambda: {"count": 0, "total_time": 0, "errors": 0})
    
    def record_request(self, endpoint: str, response_time: float, status_code: int):
        """Record request performance metrics"""
        self.request_times[endpoint].append(response_time)
        self.endpoint_stats[endpoint]["count"] += 1
        self.endpoint_stats[endpoint]["total_time"] += response_time
        
        if status_code >= 400:
            self.endpoint_stats[endpoint]["errors"] += 1
            self.error_counts[endpoint] += 1
        
        # Keep only last 100 requests per endpoint
        if len(self.request_times[endpoint]) > 100:
            self.request_times[endpoint] = self.request_times[endpoint][-100:]
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        summary = {
            "total_endpoints": len(self.endpoint_stats),
            "total_requests": sum(stats["count"] for stats in self.endpoint_stats.values()),
            "total_errors": sum(stats["errors"] for stats in self.endpoint_stats.values()),
            "endpoints": {}
        }
        
        for endpoint, stats in self.endpoint_stats.items():
            if stats["count"] > 0:
                avg_time = stats["total_time"] / stats["count"]
                error_rate = (stats["errors"] / stats["count"]) * 100
                
                summary["endpoints"][endpoint] = {
                    "requests": stats["count"],
                    "avg_response_time_ms": round(avg_time * 1000, 2),
                    "error_rate_percent": round(error_rate, 2),
                    "total_errors": stats["errors"]
                }
        
        return summary

def cache_result(cache_key: str, ttl_seconds: int = 300):
    """Decorator for caching function results"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get cache instance from app state or create new one
            cache = getattr(wrapper, '_cache', PerformanceCache())
            if not hasattr(wrapper, '_cache'):
                wrapper._cache = cache
            
            # Try to get from cache first
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            cache.set(cache_key, result, ttl_seconds)
            return result
        
        return wrapper
    return decorator

def performance_monitor(func):
    """Decorator for monitoring function performance"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            response_time = time.time() - start_time
            
            # Record successful request
            monitor = getattr(wrapper, '_monitor', PerformanceMonitor())
            if not hasattr(wrapper, '_monitor'):
                wrapper._monitor = monitor
            
            monitor.record_request(func.__name__, response_time, 200)
            return result
            
        except Exception as e:
            response_time = time.time() - start_time
            
            # Record failed request
            monitor = getattr(wrapper, '_monitor', PerformanceMonitor())
            if not hasattr(wrapper, '_monitor'):
                wrapper._monitor = monitor
            
            monitor.record_request(func.__name__, response_time, 500)
            raise
    
    return wrapper

# Global instances
performance_cache = PerformanceCache()
performance_monitor_instance = PerformanceMonitor()
async_health_checker = AsyncHealthChecker(performance_cache)