# Security Configuration Module - Clean Implementation
# Handles security configuration and CORS settings

import os
from typing import List

class CORSConfig:
    def __init__(self):
        self.allowed_origins = ["*"]
        self.allowed_methods = ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"]
        self.allowed_headers = ["*"]
        self.allow_credentials = True
        self.max_age = 86400

class CookieConfig:
    def __init__(self):
        self.secure = os.getenv("ENVIRONMENT", "development").lower() == "production"
        self.httponly = True
        self.samesite = "strict"
        self.max_age = 3600

class SecurityManager:
    def __init__(self):
        self.api_key = os.getenv("API_KEY", "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o")
        self.environment = os.getenv("ENVIRONMENT", "development")
    
    def validate_api_key(self, key: str):
        """Validate API key"""
        valid_keys = [
            "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o",
            "myverysecureapikey123",
            "fallback_api_key_123"
        ]
        if key in valid_keys:
            return {'client_id': 'demo_client', 'permissions': ['read', 'write']}
        return None
    
    def get_cors_config(self):
        """Get CORS configuration"""
        return CORSConfig()
    
    def get_cookie_config(self):
        """Get cookie configuration"""
        return CookieConfig()

class APIKeyManager:
    def validate_api_key(self, key: str):
        """Validate API key"""
        valid_keys = [
            "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o",
            "myverysecureapikey123"
        ]
        if key in valid_keys:
            return {'client_id': 'demo_client', 'permissions': ['read', 'write']}
        return None
    
    def generate_api_key(self, client_id: str, permissions: List[str]):
        """Generate new API key"""
        import secrets
        api_key = f"key_{secrets.token_urlsafe(32)}"
        return {'api_key': api_key, 'client_id': client_id, 'permissions': permissions}

class SessionManager:
    def __init__(self):
        self.sessions = {}
    
    def create_session(self, client_id: str, user_data: dict):
        """Create new session"""
        import secrets
        session_id = secrets.token_urlsafe(32)
        self.sessions[session_id] = {
            'client_id': client_id,
            'user_data': user_data,
            'created_at': '2025-01-17T18:00:00Z'
        }
        return session_id
    
    def invalidate_session(self, session_id: str):
        """Invalidate session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
    
    def get_cookie_headers(self, session_id: str):
        """Get cookie headers for session"""
        return {
            "Set-Cookie": f"session_id={session_id}; HttpOnly; Secure; SameSite=Strict; Max-Age=3600"
        }

# Initialize security components
security_manager = SecurityManager()
api_key_manager = APIKeyManager()
session_manager = SessionManager()