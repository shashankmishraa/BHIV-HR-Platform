"""
Observability Manager - Unified interface for observability frameworks
Handles fallback between enhanced and basic observability
"""

import logging
import os
from typing import Optional, Tuple, Any

# Try to import enhanced observability first
try:
    from .observability_enhanced import (
        setup_enhanced_observability,
        EnhancedMetricsCollector,
        EnhancedHealthChecker,
        AlertManager,
        DistributedTracing
    )
    ENHANCED_AVAILABLE = True
except ImportError as e:
    ENHANCED_AVAILABLE = False
    logging.warning(f"Enhanced observability not available: {e}")

# Fallback to basic observability
try:
    from .observability import (
        setup_observability,
        HealthChecker,
        MetricsCollector
    )
    BASIC_AVAILABLE = True
except ImportError as e:
    BASIC_AVAILABLE = False
    logging.error(f"Basic observability not available: {e}")

# Try to import async manager
try:
    from .async_manager import (
        initialize_async_engine,
        get_async_engine,
        shutdown_async_engine,
        AsyncProcessingEngine
    )
    ASYNC_MANAGER_AVAILABLE = True
except ImportError as e:
    ASYNC_MANAGER_AVAILABLE = False
    logging.warning(f"Async manager not available: {e}")

class ObservabilityManager:
    """Unified observability manager with fallback support"""
    
    def __init__(self):
        self.enhanced_mode = False
        self.health_checker = None
        self.metrics_collector = None
        self.alert_manager = None
        self.tracer = None
        
    def setup_observability(self, app, service_name: str, version: str) -> Tuple[Any, ...]:
        """Setup observability with automatic fallback"""
        
        # Check if enhanced mode is explicitly disabled
        disable_enhanced = os.getenv("DISABLE_ENHANCED_OBSERVABILITY", "false").lower() == "true"
        
        if ENHANCED_AVAILABLE and not disable_enhanced:
            try:
                # Try enhanced observability
                result = setup_enhanced_observability(app, service_name, version)
                self.metrics_collector, self.health_checker, self.alert_manager, self.tracer = result
                self.enhanced_mode = True
                logging.info(f"Enhanced observability initialized for {service_name}")
                return result
                
            except Exception as e:
                logging.error(f"Enhanced observability failed, falling back to basic: {e}")
        
        if BASIC_AVAILABLE:
            try:
                # Fallback to basic observability
                self.health_checker = setup_observability(app, service_name, version)
                self.metrics_collector = MetricsCollector()
                self.alert_manager = None
                self.tracer = None
                self.enhanced_mode = False
                logging.info(f"Basic observability initialized for {service_name}")
                return self.metrics_collector, self.health_checker, self.alert_manager, self.tracer
                
            except Exception as e:
                logging.error(f"Basic observability failed: {e}")
        
        # No observability available
        logging.warning("No observability framework available")
        return None, None, None, None
    
    def is_enhanced(self) -> bool:
        """Check if enhanced observability is active"""
        return self.enhanced_mode
    
    def get_health_checker(self):
        """Get health checker instance"""
        return self.health_checker
    
    def get_metrics_collector(self):
        """Get metrics collector instance"""
        return self.metrics_collector
    
    def get_alert_manager(self):
        """Get alert manager instance"""
        return self.alert_manager
    
    def get_tracer(self):
        """Get tracer instance"""
        return self.tracer

class AsyncManager:
    """Unified async manager with fallback support"""
    
    def __init__(self):
        self.async_engine = None
        self.enhanced_mode = False
        
    async def initialize_async_processing(self, database_url: str) -> bool:
        """Initialize async processing with fallback"""
        
        if not ASYNC_MANAGER_AVAILABLE:
            logging.warning("Async manager not available")
            return False
            
        try:
            self.async_engine = await initialize_async_engine(database_url)
            self.enhanced_mode = True
            logging.info("Enhanced async processing initialized")
            return True
            
        except Exception as e:
            logging.error(f"Failed to initialize async processing: {e}")
            return False
    
    def get_async_engine(self):
        """Get async engine instance"""
        if self.enhanced_mode and ASYNC_MANAGER_AVAILABLE:
            return get_async_engine()
        return None
    
    async def shutdown_async_processing(self):
        """Shutdown async processing"""
        if self.enhanced_mode and ASYNC_MANAGER_AVAILABLE:
            try:
                await shutdown_async_engine()
                logging.info("Async processing shutdown complete")
            except Exception as e:
                logging.error(f"Error during async shutdown: {e}")
    
    def is_enhanced(self) -> bool:
        """Check if enhanced async processing is active"""
        return self.enhanced_mode

# Global instances
_observability_manager: Optional[ObservabilityManager] = None
_async_manager: Optional[AsyncManager] = None

def get_observability_manager() -> ObservabilityManager:
    """Get global observability manager"""
    global _observability_manager
    if _observability_manager is None:
        _observability_manager = ObservabilityManager()
    return _observability_manager

def get_async_manager() -> AsyncManager:
    """Get global async manager"""
    global _async_manager
    if _async_manager is None:
        _async_manager = AsyncManager()
    return _async_manager

def setup_unified_observability(app, service_name: str, version: str):
    """Unified setup function for observability"""
    manager = get_observability_manager()
    return manager.setup_observability(app, service_name, version)

async def initialize_unified_async(database_url: str):
    """Unified setup function for async processing"""
    manager = get_async_manager()
    return await manager.initialize_async_processing(database_url)

async def shutdown_unified_async():
    """Unified shutdown function for async processing"""
    manager = get_async_manager()
    await manager.shutdown_async_processing()

# Compatibility functions for existing code
def setup_observability_compat(app, service_name: str, version: str):
    """Compatibility function for existing setup_observability calls"""
    result = setup_unified_observability(app, service_name, version)
    # Return health_checker for compatibility
    return result[1] if result[1] else None

# Export compatibility names
setup_observability = setup_observability_compat