# Security Configuration
from pydantic import BaseModel
from typing import List

class CORSConfig(BaseModel):
    allowed_origins: List[str] = ["*"]
    allow_credentials: bool = True
    allowed_methods: List[str] = ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"]
    allowed_headers: List[str] = ["*"]
    max_age: int = 86400

class SecurityManager:
    def __init__(self):
        self.cors_config = CORSConfig()
    
    def get_cors_config(self) -> CORSConfig:
        """Get CORS configuration"""
        return self.cors_config
    
    def validate_api_key(self, api_key: str) -> bool:
        """Validate API key"""
        valid_keys = ["prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o", "myverysecureapikey123"]
        return api_key in valid_keys

# Global security manager instance
security_manager = SecurityManager()