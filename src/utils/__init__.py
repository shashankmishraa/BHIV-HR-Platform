"""
BHIV HR Platform - Utility Functions
Common utility functions used across services
"""

import os
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timezone

def get_env_var(key: str, default: Optional[str] = None, required: bool = False) -> str:
    """Get environment variable with validation"""
    value = os.getenv(key, default)
    if required and not value:
        raise ValueError(f"Required environment variable {key} is not set")
    return value

def setup_logging(service_name: str, level: str = "INFO") -> logging.Logger:
    """Setup standardized logging for services"""
    logger = logging.getLogger(service_name)
    logger.setLevel(getattr(logging, level.upper()))
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            f'%(asctime)s - {service_name} - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger

def get_current_timestamp() -> str:
    """Get current UTC timestamp in ISO format"""
    return datetime.now(timezone.utc).isoformat()

def validate_api_key(provided_key: str, expected_key: str) -> bool:
    """Validate API key securely"""
    if not provided_key or not expected_key:
        return False
    return provided_key == expected_key

def format_error_response(message: str, error_code: Optional[str] = None, details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Format standardized error response"""
    return {
        "success": False,
        "message": message,
        "error_code": error_code,
        "details": details,
        "timestamp": get_current_timestamp()
    }

def format_success_response(data: Any, message: str = "Operation completed successfully") -> Dict[str, Any]:
    """Format standardized success response"""
    return {
        "success": True,
        "message": message,
        "data": data,
        "timestamp": get_current_timestamp()
    }