"""
SQL injection protection utilities
"""
from typing import Any, Dict, List
import re
class SQLProtection:
    """Protects against SQL injection attacks"""
    
    # SQL injection patterns to detect
    SQL_PATTERNS = [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION)\b)",
        r"(--|#|/\*|\*/)",
        r"(\b(OR|AND)\s+\d+\s*=\s*\d+)",
        r"(\'\s*(OR|AND)\s*\'\w*\'\s*=\s*\'\w*)",
        r"(\bUNION\s+SELECT\b)",
        r"(\bINTO\s+OUTFILE\b)",
        r"(\bLOAD_FILE\b)",
    ]
    
    @staticmethod
    def is_sql_injection_attempt(value: str) -> bool:
        """Check if input contains SQL injection patterns"""
        if not isinstance(value, str):
            return False
            
        for pattern in SQLProtection.SQL_PATTERNS:
            if re.search(pattern, value, re.IGNORECASE):
                return True
        return False
    
    @staticmethod
    def sanitize_sql_input(value: str) -> str:
        """Sanitize input to prevent SQL injection"""
        if not isinstance(value, str):
            return str(value)
        
        # Remove dangerous SQL keywords and characters
        sanitized = value
        
        # Remove SQL comments
        sanitized = re.sub(r'--.*$', '', sanitized, flags=re.MULTILINE)
        sanitized = re.sub(r'/\*.*?\*/', '', sanitized, flags=re.DOTALL)
        
        # Escape single quotes
        sanitized = sanitized.replace("'", "''")
        
        # Remove semicolons (statement terminators)
        sanitized = sanitized.replace(';', '')
        
        return sanitized.strip()
    
    @staticmethod
    def validate_search_params(params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and sanitize search parameters"""
        safe_params = {}
        
        for key, value in params.items():
            if isinstance(value, str):
                if SQLProtection.is_sql_injection_attempt(value):
                    raise ValueError(f"Invalid input detected in {key}")
                safe_params[key] = SQLProtection.sanitize_sql_input(value)
            else:
                safe_params[key] = value
                
        return safe_params

# Global SQL protection instance
sql_guard = SQLProtection()