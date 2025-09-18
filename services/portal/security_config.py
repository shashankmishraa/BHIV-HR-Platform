"""
Enhanced Security Configuration for Portal
Addresses CWE-798 and provides comprehensive security management
"""
from typing import Optional, Dict, Any
import logging
import os
import secrets
import sys
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add shared directory to path for centralized security
shared_path = os.path.join(os.path.dirname(__file__), '..', 'shared')
if shared_path not in sys.path:
    sys.path.insert(0, shared_path)

try:
    from security_manager import SecurityManager, APIKeyManager
    ENHANCED_SECURITY = True
except ImportError:
    # Fallback for environments without enhanced security
    ENHANCED_SECURITY = False
    logger.warning("Enhanced security manager not available. Using fallback security.")

class FallbackSecurityManager:
    """Fallback security manager for development"""
    
    def __init__(self):
        self.api_key = self._get_fallback_api_key()
        logger.warning("Using fallback security manager. Install enhanced security for production.")
    
    def _get_fallback_api_key(self) -> str:
        """Get API key with fallback for development"""
        api_key = os.getenv("API_KEY_SECRET")
        environment = os.getenv("ENVIRONMENT", "development").lower()
        
        # Check for demo key in any environment
        if api_key == "myverysecureapikey123":
            if environment == "production":
                raise ValueError(
                    "Demo API key detected in production. Use a secure, unique API key. "
                    "Generate one using: python -c \"import secrets; print(secrets.token_urlsafe(32))\""
                )
            else:
                logger.warning(
                    "Demo API key detected. For production, set API_KEY_SECRET to a secure value. "
                    "Generate one using: python -c \"import secrets; print(secrets.token_urlsafe(32))\""
                )
                # Generate a temporary secure key for development
                return "temp_dev_key_" + secrets.token_urlsafe(24)
        
        if not api_key:
            if environment == "production":
                raise ValueError(
                    "API_KEY_SECRET environment variable is required for production. "
                    "Generate one using: python -c \"import secrets; print(secrets.token_urlsafe(32))\""
                )
            else:
                logger.warning("No API_KEY_SECRET found. Generating temporary key for development.")
                return "temp_dev_key_" + secrets.token_urlsafe(24)
        
        return api_key
    
    def get_api_headers(self) -> Dict[str, str]:
        """Get API headers"""
        return {"Authorization": f"Bearer {self.api_key}"}
    
    @staticmethod
    def generate_secure_key(length: int = 32) -> str:
        """Generate secure key"""
        return secrets.token_urlsafe(length)

class SecureAPIKeyManager:
    """Enhanced secure API key management"""
    
    def __init__(self):
        if ENHANCED_SECURITY:
            try:
                self.security_manager = SecurityManager()
                self.api_key_manager = APIKeyManager(self.security_manager)
                logger.info("Enhanced security manager initialized successfully")
            except Exception as e:
                logger.error(f"Enhanced security manager failed to initialize: {e}")
                logger.info("Falling back to basic security manager")
                self.fallback_manager = FallbackSecurityManager()
                self.security_manager = None
        else:
            self.fallback_manager = FallbackSecurityManager()
            self.security_manager = None
    
    def get_headers(self) -> Dict[str, str]:
        """Get secure authorization headers"""
        if self.security_manager:
            return self.security_manager.get_api_headers()
        else:
            return self.fallback_manager.get_api_headers()
    
    def validate_api_key(self, api_key: str) -> Optional[Dict[str, Any]]:
        """Validate API key"""
        if self.security_manager:
            return self.api_key_manager.validate_api_key(api_key)
        else:
            # Simple validation for fallback
            if api_key == self.fallback_manager.api_key:
                return {'client_id': 'system', 'permissions': ['read', 'write']}
            return None
    
    @staticmethod
    def generate_secure_api_key() -> str:
        """Generate a cryptographically secure API key"""
        return secrets.token_urlsafe(32)

# Global secure API key manager with error handling
try:
    secure_api = SecureAPIKeyManager()
except Exception as e:
    logger.error(f"Failed to initialize secure API manager: {e}")
    # Create a minimal fallback
    class MinimalSecureAPI:
        def __init__(self):
            api_key = os.getenv("API_KEY_SECRET")
            if not api_key or api_key == "myverysecureapikey123":
                api_key = "temp_fallback_" + secrets.token_urlsafe(24)
            self.api_key = api_key
        
        def get_headers(self):
            return {"Authorization": f"Bearer {self.api_key}"}
    
    secure_api = MinimalSecureAPI()