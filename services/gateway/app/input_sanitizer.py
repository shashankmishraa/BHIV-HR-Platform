"""
Input Sanitization and XSS Protection Module
Comprehensive security layer for all user inputs
"""

from typing import Any, Dict, List, Optional, Union
import logging
import re

from urllib.parse import quote, unquote
import bleach
import html
logger = logging.getLogger(__name__)

class InputSanitizer:
    """Comprehensive input sanitization and XSS protection"""
    
    # XSS patterns to detect and block
    XSS_PATTERNS = [
        r'<script[^>]*>.*?</script>',
        r'javascript:',
        r'vbscript:',
        r'onload\s*=',
        r'onerror\s*=',
        r'onclick\s*=',
        r'onmouseover\s*=',
        r'onfocus\s*=',
        r'onblur\s*=',
        r'<iframe[^>]*>',
        r'<object[^>]*>',
        r'<embed[^>]*>',
        r'<link[^>]*>',
        r'<meta[^>]*>',
        r'<style[^>]*>.*?</style>',
        r'expression\s*\(',
        r'url\s*\(',
        r'@import',
        r'<svg[^>]*>.*?</svg>',
        r'<math[^>]*>.*?</math>',
    ]
    
    # SQL injection patterns
    SQL_PATTERNS = [
        r"(\b(union|select|insert|update|delete|drop|create|alter|exec|execute)\b)",
        r"(\b(or|and)\s+\d+\s*=\s*\d+)",
        r"(\b(or|and)\s+['\"]?\w+['\"]?\s*=\s*['\"]?\w+['\"]?)",
        r"(--|#|/\*|\*/)",
        r"(\bxp_cmdshell\b)",
        r"(\bsp_executesql\b)",
        r"('.*'|\".*\")",
        r"(\bwaitfor\s+delay\b)",
        r"(\bbenchmark\s*\()",
        r"(\bsleep\s*\()",
    ]
    
    # Allowed HTML tags for rich text (very restrictive)
    ALLOWED_TAGS = ['b', 'i', 'u', 'em', 'strong', 'p', 'br']
    ALLOWED_ATTRIBUTES = {}
    
    def __init__(self):
        self.xss_regex = re.compile('|'.join(self.XSS_PATTERNS), re.IGNORECASE | re.DOTALL)
        self.sql_regex = re.compile('|'.join(self.SQL_PATTERNS), re.IGNORECASE)
    
    def sanitize_string(self, value: str, max_length: int = 1000, allow_html: bool = False) -> str:
        """Sanitize string input with comprehensive protection"""
        if not isinstance(value, str):
            value = str(value)
        
        # Truncate to max length
        if len(value) > max_length:
            value = value[:max_length]
            logger.warning(f"Input truncated to {max_length} characters")
        
        # Remove null bytes and control characters
        value = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', value)
        
        # Normalize unicode
        value = value.encode('utf-8', errors='ignore').decode('utf-8')
        
        if allow_html:
            # Use bleach for HTML sanitization
            value = bleach.clean(
                value,
                tags=self.ALLOWED_TAGS,
                attributes=self.ALLOWED_ATTRIBUTES,
                strip=True
            )
        else:
            # HTML escape for plain text
            value = html.escape(value, quote=True)
        
        # Additional XSS protection
        value = self._remove_xss_patterns(value)
        
        return value.strip()
    
    def _remove_xss_patterns(self, value: str) -> str:
        """Remove XSS patterns from input"""
        # Remove dangerous patterns
        value = self.xss_regex.sub('', value)
        
        # Remove data URLs
        value = re.sub(r'data:\s*[^;]*;[^,]*,', '', value, flags=re.IGNORECASE)
        
        # Remove javascript protocol
        value = re.sub(r'javascript\s*:', '', value, flags=re.IGNORECASE)
        
        # Remove vbscript protocol
        value = re.sub(r'vbscript\s*:', '', value, flags=re.IGNORECASE)
        
        return value
    
    def detect_xss(self, value: str) -> List[str]:
        """Detect XSS patterns in input"""
        threats = []
        
        if self.xss_regex.search(value):
            threats.append("XSS pattern detected")
        
        # Check for encoded XSS attempts
        try:
            decoded = unquote(value)
            if decoded != value and self.xss_regex.search(decoded):
                threats.append("Encoded XSS pattern detected")
        except:
            pass
        
        return threats
    
    def detect_sql_injection(self, value: str) -> List[str]:
        """Detect SQL injection patterns"""
        threats = []
        
        if self.sql_regex.search(value):
            threats.append("SQL injection pattern detected")
        
        # Check for common SQL injection indicators
        if "'" in value and any(keyword in value.lower() for keyword in ['union', 'select', 'insert', 'update', 'delete']):
            threats.append("Potential SQL injection attempt")
        
        return threats
    
    def sanitize_email(self, email: str) -> str:
        """Sanitize email address"""
        if not email:
            return ""
        
        # Basic email validation and sanitization
        email = email.strip().lower()
        
        # Remove dangerous characters
        email = re.sub(r'[<>"\'\\\x00-\x1f\x7f-\x9f]', '', email)
        
        # Validate email format
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            logger.warning(f"Invalid email format: {email}")
            return ""
        
        return email
    
    def sanitize_phone(self, phone: str) -> str:
        """Sanitize phone number"""
        if not phone:
            return ""
        
        # Remove all non-digit characters except + - ( ) space
        phone = re.sub(r'[^\d\+\-\(\)\s]', '', phone)
        
        # Limit length
        if len(phone) > 20:
            phone = phone[:20]
        
        return phone.strip()
    
    def sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for safe storage"""
        if not filename:
            return ""
        
        # Remove path traversal attempts
        filename = filename.replace('..', '').replace('/', '').replace('\\', '')
        
        # Remove dangerous characters
        filename = re.sub(r'[<>:"|?*\x00-\x1f\x7f-\x9f]', '', filename)
        
        # Limit length
        if len(filename) > 255:
            name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
            filename = name[:250] + ('.' + ext if ext else '')
        
        return filename.strip()
    
    def sanitize_url(self, url: str) -> str:
        """Sanitize URL input"""
        if not url:
            return ""
        
        # Remove dangerous protocols
        dangerous_protocols = ['javascript:', 'vbscript:', 'data:', 'file:', 'ftp:']
        url_lower = url.lower()
        
        for protocol in dangerous_protocols:
            if url_lower.startswith(protocol):
                logger.warning(f"Dangerous protocol detected in URL: {protocol}")
                return ""
        
        # Only allow http and https
        if not (url_lower.startswith('http://') or url_lower.startswith('https://')):
            if not url_lower.startswith('//'):  # Protocol relative URLs
                url = 'https://' + url
        
        # Remove XSS patterns
        url = self._remove_xss_patterns(url)
        
        return url.strip()
    
    def sanitize_dict(self, data: Dict[str, Any], schema: Optional[Dict[str, Dict]] = None) -> Dict[str, Any]:
        """Sanitize dictionary data based on schema"""
        if not isinstance(data, dict):
            return {}
        
        sanitized = {}
        
        for key, value in data.items():
            # Sanitize key
            clean_key = self.sanitize_string(key, max_length=100)
            
            if schema and clean_key in schema:
                field_config = schema[clean_key]
                field_type = field_config.get('type', 'string')
                max_length = field_config.get('max_length', 1000)
                allow_html = field_config.get('allow_html', False)
                
                if field_type == 'email':
                    sanitized[clean_key] = self.sanitize_email(str(value))
                elif field_type == 'phone':
                    sanitized[clean_key] = self.sanitize_phone(str(value))
                elif field_type == 'url':
                    sanitized[clean_key] = self.sanitize_url(str(value))
                elif field_type == 'filename':
                    sanitized[clean_key] = self.sanitize_filename(str(value))
                elif field_type == 'integer':
                    try:
                        sanitized[clean_key] = int(value)
                    except (ValueError, TypeError):
                        sanitized[clean_key] = 0
                elif field_type == 'float':
                    try:
                        sanitized[clean_key] = float(value)
                    except (ValueError, TypeError):
                        sanitized[clean_key] = 0.0
                else:  # string
                    sanitized[clean_key] = self.sanitize_string(str(value), max_length, allow_html)
            else:
                # Default sanitization
                if isinstance(value, str):
                    sanitized[clean_key] = self.sanitize_string(value)
                elif isinstance(value, (int, float)):
                    sanitized[clean_key] = value
                elif isinstance(value, dict):
                    sanitized[clean_key] = self.sanitize_dict(value)
                elif isinstance(value, list):
                    sanitized[clean_key] = [self.sanitize_string(str(item)) for item in value]
                else:
                    sanitized[clean_key] = self.sanitize_string(str(value))
        
        return sanitized
    
    def validate_and_sanitize(self, data: Any, field_type: str = 'string', **kwargs) -> tuple[Any, List[str]]:
        """Validate and sanitize input with threat detection"""
        threats = []
        
        if isinstance(data, str):
            # Detect threats first
            threats.extend(self.detect_xss(data))
            threats.extend(self.detect_sql_injection(data))
            
            # Sanitize based on type
            if field_type == 'email':
                sanitized = self.sanitize_email(data)
            elif field_type == 'phone':
                sanitized = self.sanitize_phone(data)
            elif field_type == 'url':
                sanitized = self.sanitize_url(data)
            elif field_type == 'filename':
                sanitized = self.sanitize_filename(data)
            else:
                max_length = kwargs.get('max_length', 1000)
                allow_html = kwargs.get('allow_html', False)
                sanitized = self.sanitize_string(data, max_length, allow_html)
        
        elif isinstance(data, dict):
            schema = kwargs.get('schema')
            sanitized = self.sanitize_dict(data, schema)
        
        else:
            sanitized = data
        
        return sanitized, threats

# Global sanitizer instance
sanitizer = InputSanitizer()

# Convenience functions
def sanitize_input(data: Any, field_type: str = 'string', **kwargs) -> Any:
    """Sanitize input data"""
    sanitized, threats = sanitizer.validate_and_sanitize(data, field_type, **kwargs)
    if threats:
        logger.warning(f"Security threats detected: {threats}")
    return sanitized

def detect_threats(data: str) -> List[str]:
    """Detect security threats in input"""
    threats = []
    threats.extend(sanitizer.detect_xss(data))
    threats.extend(sanitizer.detect_sql_injection(data))
    return threats