#!/usr/bin/env python3
"""
BHIV HR Platform - Environment-Specific Configuration
Secure configuration management for different deployment environments
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

class Environment(Enum):
    """Supported deployment environments"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"

@dataclass
class DatabaseConfig:
    """Database configuration"""
    url: str
    pool_size: int = 10
    timeout: int = 30
    
    @classmethod
    def from_env(cls) -> 'DatabaseConfig':
        return cls(
            url=os.getenv("DATABASE_URL", ""),
            pool_size=int(os.getenv("DATABASE_POOL_SIZE", "10")),
            timeout=int(os.getenv("DATABASE_TIMEOUT", "30"))
        )

@dataclass
class SecurityConfig:
    """Security configuration"""
    api_key: str
    client_access_code: str
    cors_origins: list
    rate_limit_enabled: bool = True
    
    @classmethod
    def from_env(cls) -> 'SecurityConfig':
        cors_origins = os.getenv("CORS_ORIGINS", "").split(",")
        return cls(
            api_key=os.getenv("API_KEY_SECRET", ""),
            client_access_code=os.getenv("CLIENT_ACCESS_CODE", ""),
            cors_origins=[origin.strip() for origin in cors_origins if origin.strip()],
            rate_limit_enabled=os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true"
        )

@dataclass
class ServiceConfig:
    """Service URLs configuration"""
    gateway_url: str
    agent_url: str
    portal_url: str
    client_portal_url: str
    
    @classmethod
    def from_env(cls) -> 'ServiceConfig':
        return cls(
            gateway_url=os.getenv("GATEWAY_URL", "http://gateway:8000"),
            agent_url=os.getenv("AGENT_URL", "http://agent:9000"),
            portal_url=os.getenv("PORTAL_URL", "http://portal:8501"),
            client_portal_url=os.getenv("CLIENT_PORTAL_URL", "http://client_portal:8502")
        )

@dataclass
class FeatureConfig:
    """Feature flags configuration"""
    enable_semantic: bool
    enable_auto_sync: bool
    enable_values_assessment: bool
    max_candidates_per_request: int
    
    @classmethod
    def from_env(cls) -> 'FeatureConfig':
        return cls(
            enable_semantic=os.getenv("ENABLE_SEMANTIC", "false").lower() == "true",
            enable_auto_sync=os.getenv("ENABLE_AUTO_SYNC", "true").lower() == "true",
            enable_values_assessment=os.getenv("ENABLE_VALUES_ASSESSMENT", "true").lower() == "true",
            max_candidates_per_request=int(os.getenv("MAX_CANDIDATES_PER_REQUEST", "50"))
        )

class ConfigurationManager:
    """Centralized configuration management"""
    
    def __init__(self):
        self.environment = self._detect_environment()
        self.database = DatabaseConfig.from_env()
        self.security = SecurityConfig.from_env()
        self.services = ServiceConfig.from_env()
        self.features = FeatureConfig.from_env()
    
    def _detect_environment(self) -> Environment:
        """Detect current environment"""
        env_name = os.getenv("ENVIRONMENT", "development").lower()
        try:
            return Environment(env_name)
        except ValueError:
            return Environment.DEVELOPMENT
    
    def validate_configuration(self) -> Dict[str, Any]:
        """Validate current configuration"""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        # Validate required fields
        if not self.database.url:
            validation_result["errors"].append("DATABASE_URL is required")
            validation_result["valid"] = False
        
        if not self.security.api_key:
            validation_result["errors"].append("API_KEY_SECRET is required")
            validation_result["valid"] = False
        
        # Security validations
        if self.security.api_key and len(self.security.api_key) < 32:
            validation_result["warnings"].append("API_KEY_SECRET should be at least 32 characters")
        
        if self._is_insecure_value(self.security.api_key):
            validation_result["errors"].append("API_KEY_SECRET appears to be a default/insecure value")
            validation_result["valid"] = False
        
        if "password" in self.database.url.lower() and self._is_insecure_password(self.database.url):
            validation_result["warnings"].append("Database password appears to be insecure")
        
        return validation_result
    
    def _is_insecure_value(self, value: str) -> bool:
        """Check if value is insecure default"""
        if not value:
            return False
        
        insecure_patterns = [
            "myverysecureapikey123",
            "your_secure_api_key",
            "demo123",
            "test123",
            "password",
            "secret"
        ]
        return any(pattern in value.lower() for pattern in insecure_patterns)
    
    def _is_insecure_password(self, database_url: str) -> bool:
        """Check if database URL contains insecure password"""
        insecure_passwords = ["password", "bhiv_pass", "your_password", "123456"]
        return any(pwd in database_url.lower() for pwd in insecure_passwords)
    
    def get_environment_info(self) -> Dict[str, Any]:
        """Get current environment information"""
        return {
            "environment": self.environment.value,
            "database_configured": bool(self.database.url),
            "security_configured": bool(self.security.api_key),
            "features_enabled": {
                "semantic": self.features.enable_semantic,
                "auto_sync": self.features.enable_auto_sync,
                "values_assessment": self.features.enable_values_assessment
            }
        }
    
    def get_service_urls(self) -> Dict[str, str]:
        """Get service URLs for current environment"""
        return {
            "gateway": self.services.gateway_url,
            "agent": self.services.agent_url,
            "portal": self.services.portal_url,
            "client_portal": self.services.client_portal_url
        }

# Global configuration instance
config = ConfigurationManager()

def get_config() -> ConfigurationManager:
    """Get global configuration instance"""
    return config