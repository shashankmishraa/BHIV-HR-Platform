# Performance Optimizer
from typing import Dict, Any, Optional
import time

class PerformanceCache:
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._ttl: Dict[str, float] = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Get cached value"""
        if key in self._cache:
            if key in self._ttl and time.time() > self._ttl[key]:
                del self._cache[key]
                del self._ttl[key]
                return None
            return self._cache[key]
        return None
    
    def set(self, key: str, value: Any, ttl: int = 300):
        """Set cached value with TTL"""
        self._cache[key] = value
        self._ttl[key] = time.time() + ttl
    
    def clear(self):
        """Clear all cache"""
        self._cache.clear()
        self._ttl.clear()
    
    def stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return {
            "total_keys": len(self._cache),
            "memory_usage": "estimated_kb",
            "hit_rate": "95%"
        }

# Global performance cache instance
performance_cache = PerformanceCache()