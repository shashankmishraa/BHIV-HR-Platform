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
shared_path = os.path.join(os.path.dirname(__file__), "..", "shared")
if shared_path not in sys.path:
    sys.path.insert(0, shared_path)

# Use production security manager directly
ENHANCED_SECURITY = True


class ProductionSecurityManager:
    """Production security manager"""

    def __init__(self):
        self.api_key = self._get_production_api_key()

    def _get_production_api_key(self) -> str:
        """Get production API key"""
        api_key = os.getenv("API_KEY_SECRET")
        environment = os.getenv("ENVIRONMENT", "production").lower()

        if not api_key:
            raise ValueError("API_KEY_SECRET environment variable is required")

        # Allow demo keys in development environment
        if environment == "development":
            return api_key

        # Reject demo keys in production
        if api_key in ["myverysecureapikey123", "demo", "test"]:
            raise ValueError("Demo API key not allowed. Use production key.")

        return api_key

    def get_api_headers(self) -> Dict[str, str]:
        """Get API headers"""
        return {"Authorization": f"Bearer {self.api_key}"}


class SecureAPIKeyManager:
    """Production API key management"""

    def __init__(self):
        self.security_manager = ProductionSecurityManager()

    def get_headers(self) -> Dict[str, str]:
        """Get secure authorization headers"""
        return self.security_manager.get_api_headers()

    def validate_api_key(self, api_key: str) -> Optional[Dict[str, Any]]:
        """Validate API key"""
        if api_key == self.security_manager.api_key:
            return {"client_id": "system", "permissions": ["read", "write"]}
        return None


# Initialize production security manager
secure_api = SecureAPIKeyManager()
