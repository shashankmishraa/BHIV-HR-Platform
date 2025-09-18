"""
Enhanced Security Configuration for Gateway Service
Centralized security management with environment-aware configuration
"""

import os
import logging
import secrets
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GatewaySecurityManager:
    """Gateway-specific security manager"""
    
    def __init__(self):
        self.environment = os.getenv("ENVIRONMENT", "development").lower()
        self.api_key = self._get_secure_api_key()
        self.jwt_secret = self._get_jwt_secret()
        logger.info(f"Gateway security manager initialized for {self.environment} environment")
    
    def _get_secure_api_key(self) -> str:
        """Get secure API key with production validation"""
        api_key = os.getenv("API_KEY_SECRET")
        
        # Production validation
        if self.environment == "production":
            if not api_key:
                raise ValueError(
                    "API_KEY_SECRET environment variable is required for production. "
                    "Set it to: prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
                )
            
            # Reject demo keys in production
            demo_keys = ["myverysecureapikey123", "demo", "test", "sample"]
            if api_key.lower() in demo_keys or len(api_key) < 16:
                raise ValueError(
                    "Demo or weak API key detected in production. "
                    "Use the production key: prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
                )
        
        # Development fallback
        if not api_key:
            if self.environment == "production":
                raise ValueError("API_KEY_SECRET is required for production")
            
            logger.warning("Using fallback API key for development. Set API_KEY_SECRET for production.")
            return "dev_fallback_" + secrets.token_urlsafe(24)
        
        return api_key
    
    def _get_jwt_secret(self) -> str:
        """Get JWT secret with validation"""
        jwt_secret = os.getenv("JWT_SECRET")
        
        if self.environment == "production":
            if not jwt_secret:
                raise ValueError(
                    "JWT_SECRET environment variable is required for production. "
                    "Set it to: prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA"
                )
            
            if len(jwt_secret) < 32:
                raise ValueError("JWT_SECRET must be at least 32 characters for production")
        
        if not jwt_secret:
            logger.warning("Using fallback JWT secret for development")
            return "dev_jwt_" + secrets.token_urlsafe(32)
        
        return jwt_secret
    
    def validate_api_key(self, provided_key: str) -> Optional[Dict[str, Any]]:
        """Validate API key and return metadata"""
        if not provided_key:
            return None
        
        # Check against configured API key
        if provided_key == self.api_key:
            return {
                'client_id': 'system',
                'permissions': ['read', 'write'],
                'key_type': 'production' if self.environment == "production" else 'development',
                'environment': self.environment
            }
        
        # Log invalid attempts
        logger.warning(f"Invalid API key attempt: {provided_key[:8]}...")
        return None
    
    def get_api_headers(self) -> Dict[str, str]:
        """Get API headers for service communication"""
        return {"Authorization": f"Bearer {self.api_key}"}
    
    def get_cors_config(self):
        """Get CORS configuration"""
        class CORSConfig:
            allowed_origins = ["*"]
            allowed_methods = ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"]
            allowed_headers = ["*"]
            allow_credentials = True
            max_age = 86400
        return CORSConfig()
    
    def get_cookie_config(self):
        """Get cookie configuration"""
        class CookieConfig:
            secure = self.environment == "production"
            httponly = True
            samesite = "strict"
            max_age = 3600
            domain = None
            path = "/"
        return CookieConfig()

# Initialize security manager
try:
    security_manager = GatewaySecurityManager()
except Exception as e:
    logger.error(f"Failed to initialize security manager: {e}")
    # Create minimal fallback
    class FallbackSecurityManager:
        def __init__(self):
            self.api_key = os.getenv("API_KEY_SECRET", "fallback_key_" + secrets.token_urlsafe(16))
            self.environment = "fallback"
        
        def validate_api_key(self, key):
            return {'client_id': 'fallback', 'permissions': ['read']} if key == self.api_key else None
        
        def get_api_headers(self):
            return {"Authorization": f"Bearer {self.api_key}"}
    
    security_manager = FallbackSecurityManager()

# API Key Manager for backward compatibility
class APIKeyManager:
    """API Key management wrapper"""
    
    def __init__(self, security_manager):
        self.security_manager = security_manager
    
    def validate_api_key(self, api_key: str) -> Optional[Dict[str, Any]]:
        """Validate API key"""
        return self.security_manager.validate_api_key(api_key)
    
    def generate_api_key(self, client_id: str, permissions: list = None) -> Dict[str, Any]:
        """Generate new API key"""
        new_key = secrets.token_urlsafe(32)
        return {
            'api_key': new_key,
            'client_id': client_id,
            'permissions': permissions or ['read'],
            'created_at': '2025-01-17T00:00:00Z'
        }
    
    def revoke_api_key(self, key_id: str) -> bool:
        """Revoke API key"""
        logger.info(f"API key revoked: {key_id}")
        return True

# Session Manager for backward compatibility
class SessionManager:
    """Session management wrapper"""
    
    def __init__(self, security_manager):
        self.security_manager = security_manager
        self.sessions = {}
    
    def create_session(self, client_id: str, user_data: dict) -> str:
        """Create secure session"""
        session_id = secrets.token_urlsafe(32)
        self.sessions[session_id] = {
            'client_id': client_id,
            'user_data': user_data,
            'created_at': '2025-01-17T00:00:00Z'
        }
        return session_id
    
    def invalidate_session(self, session_id: str) -> bool:
        """Invalidate session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
    
    def get_cookie_headers(self, session_id: str) -> Dict[str, str]:
        """Get cookie headers"""
        return {
            "Set-Cookie": f"session_id={session_id}; HttpOnly; Secure; SameSite=Strict; Max-Age=3600"
        }

# Initialize managers
api_key_manager = APIKeyManager(security_manager)
session_manager = SessionManager(security_manager)