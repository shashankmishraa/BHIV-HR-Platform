"""
CSRF protection for Streamlit forms
"""
import secrets
import hashlib
import time
from typing import Optional

class CSRFProtection:
    """CSRF token generation and validation"""
    
    def __init__(self):
        self.tokens = {}  # In production, use Redis or database
        self.token_lifetime = 3600  # 1 hour
    
    def generate_token(self, session_id: str) -> str:
        """Generate CSRF token for session"""
        token = secrets.token_urlsafe(32)
        timestamp = time.time()
        
        # Store token with timestamp
        self.tokens[session_id] = {
            'token': token,
            'timestamp': timestamp
        }
        
        return token
    
    def validate_token(self, session_id: str, token: str) -> bool:
        """Validate CSRF token"""
        if session_id not in self.tokens:
            return False
        
        stored_data = self.tokens[session_id]
        stored_token = stored_data['token']
        timestamp = stored_data['timestamp']
        
        # Check if token expired
        if time.time() - timestamp > self.token_lifetime:
            del self.tokens[session_id]
            return False
        
        # Validate token
        return secrets.compare_digest(stored_token, token)
    
    def cleanup_expired_tokens(self):
        """Remove expired tokens"""
        current_time = time.time()
        expired_sessions = []
        
        for session_id, data in self.tokens.items():
            if current_time - data['timestamp'] > self.token_lifetime:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            del self.tokens[session_id]

# Global CSRF protection instance
csrf_guard = CSRFProtection()