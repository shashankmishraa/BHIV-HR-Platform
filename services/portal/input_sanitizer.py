"""
Input sanitization module to prevent XSS vulnerabilities
"""
from typing import Any, Dict, List, Union
import re

import html
class InputSanitizer:
    """Sanitizes user input to prevent XSS attacks"""
    
    @staticmethod
    def sanitize_string(value: str) -> str:
        """Sanitize string input to prevent XSS"""
        if not isinstance(value, str):
            return str(value)
        
        # HTML escape
        sanitized = html.escape(value)
        
        # Remove script tags
        sanitized = re.sub(r'<script[^>]*>.*?</script>', '', sanitized, flags=re.IGNORECASE | re.DOTALL)
        
        # Remove javascript: URLs
        sanitized = re.sub(r'javascript:', '', sanitized, flags=re.IGNORECASE)
        
        # Remove on* event handlers
        sanitized = re.sub(r'on\w+\s*=', '', sanitized, flags=re.IGNORECASE)
        
        return sanitized.strip()
    
    @staticmethod
    def sanitize_dict(data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize dictionary values"""
        sanitized = {}
        for key, value in data.items():
            if isinstance(value, str):
                sanitized[key] = InputSanitizer.sanitize_string(value)
            elif isinstance(value, dict):
                sanitized[key] = InputSanitizer.sanitize_dict(value)
            elif isinstance(value, list):
                sanitized[key] = InputSanitizer.sanitize_list(value)
            else:
                sanitized[key] = value
        return sanitized
    
    @staticmethod
    def sanitize_list(data: List[Any]) -> List[Any]:
        """Sanitize list values"""
        sanitized = []
        for item in data:
            if isinstance(item, str):
                sanitized.append(InputSanitizer.sanitize_string(item))
            elif isinstance(item, dict):
                sanitized.append(InputSanitizer.sanitize_dict(item))
            elif isinstance(item, list):
                sanitized.append(InputSanitizer.sanitize_list(item))
            else:
                sanitized.append(item)
        return sanitized

# Global sanitizer instance
sanitizer = InputSanitizer()