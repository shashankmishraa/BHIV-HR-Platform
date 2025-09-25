"""
Centralized logging configuration for BHIV HR Platform
"""
from pathlib import Path
import logging
import os
def setup_service_logging(service_name: str, log_level: str = "INFO"):
    """Setup centralized logging for a service"""
    
    # Determine log directory based on environment with security validation
    if os.path.exists('/app'):
        # Container environment
        log_dir = '/app/logs'
    else:
        # Local development - use secure path resolution
        base_path = Path(__file__).parent.parent.parent.resolve()
        log_dir = base_path / 'logs'
        log_dir = str(log_dir)
    
    # Create log directory securely
    try:
        os.makedirs(log_dir, exist_ok=True)
    except (OSError, PermissionError) as e:
        # Fallback to current directory if log directory creation fails
        log_dir = os.getcwd()
    
    # Configure logging with sanitized service name
    safe_service_name = ''.join(c for c in service_name if c.isalnum() or c in '-_')
    log_file = os.path.join(log_dir, f'{safe_service_name}.log')
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ],
        force=True  # Override existing configuration
    )
    
    return logging.getLogger(service_name)

def get_logger(name: str):
    """Get logger with centralized configuration"""
    return logging.getLogger(name)

class CorrelationContext:
    """Request correlation context for distributed tracing"""
    
    @staticmethod
    def set_correlation_id(correlation_id: str):
        pass
    
    @staticmethod
    def set_request_id(request_id: str):
        pass
    
    @staticmethod
    def clear():
        pass