"""Simple observability fallback for production deployment"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class MetricsCollector:
    """Simple metrics collector"""
    
    def __init__(self):
        self.metrics = {}
    
    def collect_metrics(self) -> Dict[str, Any]:
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "active"
        }
    
    def record_request(self, *args, **kwargs):
        pass

def setup_simple_observability(app, service_name: str, version: str) -> Optional[Any]:
    """Setup simple observability"""
    logger.info(f"Simple observability setup for {service_name} v{version}")
    return None