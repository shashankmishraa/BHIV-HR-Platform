"""
Security configuration for API key management
Addresses CWE-798 - Hardcoded Credentials vulnerability
"""
import os
import secrets
import hashlib
from typing import Optional

class SecureAPIKeyManager:
    """Secure API key management to prevent hardcoded credentials"""
    
    def __init__(self):
        self.api_key = self._get_secure_api_key()
    
    def _get_secure_api_key(self) -> str:
        """Get API key from secure environment variable"""
        api_key = os.getenv("API_KEY_SECRET")
        
        if not api_key:
            raise ValueError(
                "API_KEY_SECRET environment variable is required. "
                "Never use hardcoded credentials in production."
            )
        
        # Validate API key format (should not be demo key)
        if api_key and api_key == "myverysecureapikey123":
            raise ValueError(
                "Demo API key detected. Use a secure, unique API key in production."
            )
        
        return api_key
    
    def get_headers(self) -> dict:
        """Get secure authorization headers"""
        return {"Authorization": f"Bearer {self.api_key}"}
    
    @staticmethod
    def generate_secure_api_key() -> str:
        """Generate a cryptographically secure API key"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def hash_api_key(api_key: str) -> str:
        """Hash API key for secure storage"""
        return hashlib.sha256(api_key.encode()).hexdigest()

# Global secure API key manager
secure_api = SecureAPIKeyManager()