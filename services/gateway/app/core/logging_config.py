import logging
import re
from typing import Any

class SecurityLogFilter(logging.Filter):
    """Filter to sanitize log messages and prevent log injection"""
    
    def __init__(self):
        super().__init__()
        # Patterns to detect potential log injection
        self.injection_patterns = [
            re.compile(r'[\r\n]'),  # CRLF injection
            re.compile(r'%[0-9a-fA-F]{2}'),  # URL encoding
            re.compile(r'<script[^>]*>.*?</script>', re.IGNORECASE),  # Script tags
            re.compile(r'javascript:', re.IGNORECASE),  # JavaScript protocol
        ]
    
    def filter(self, record: logging.LogRecord) -> bool:
        """Sanitize log message to prevent injection attacks"""
        if hasattr(record, 'msg') and record.msg:
            # Convert message to string
            msg = str(record.msg)
            
            # Remove potential injection patterns
            for pattern in self.injection_patterns:
                msg = pattern.sub('', msg)
            
            # Limit message length to prevent DoS
            if len(msg) > 1000:
                msg = msg[:1000] + "... [TRUNCATED]"
            
            # Replace the message
            record.msg = msg
        
        return True

def setup_logging():
    """Configure secure logging for the application"""
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Create handler
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    
    # Add security filter
    security_filter = SecurityLogFilter()
    handler.addFilter(security_filter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)
    
    return root_logger