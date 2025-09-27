"""Centralized Configuration Management for BHIV HR Platform"""

import os
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"

@dataclass
class DatabaseConfig:
    url: str
    pool_size: int = 10
    max_overflow: int = 20
    pool_timeout: int = 30
    pool_recycle: int = 3600

@dataclass
class ServiceConfig:
    gateway_url: str
    agent_url: str
    portal_url: str
    client_portal_url: str

@dataclass
class SecurityConfig:
    api_key_secret: str
    jwt_secret: str
    secret_key: str
    session_timeout: int = 3600
    rate_limit_per_minute: int = 1000

@dataclass
class FeatureFlags:
    semantic_engine: bool = True
    observability: bool = True
    caching: bool = True
    async_processing: bool = True
    audit_logging: bool = True

class ConfigManager:
    """Centralized configuration manager"""
    
    def __init__(self):
        self.environment = Environment(os.getenv("ENVIRONMENT", "development").lower())
        self._config_cache: Dict[str, Any] = {}
        self._load_configuration()
    
    def _load_configuration(self):
        """Load configuration from environment variables"""
        
        # Database configuration
        self.database = DatabaseConfig(
            url=self._get_required_env("DATABASE_URL"),
            pool_size=int(os.getenv("DB_POOL_SIZE", "10")),
            max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "20")),
            pool_timeout=int(os.getenv("DB_POOL_TIMEOUT", "30")),
            pool_recycle=int(os.getenv("DB_POOL_RECYCLE", "3600"))
        )
        
        # Service URLs
        self.services = ServiceConfig(
            gateway_url=os.getenv("GATEWAY_URL", self._get_default_gateway_url()),
            agent_url=os.getenv("AGENT_SERVICE_URL", self._get_default_agent_url()),
            portal_url=os.getenv("PORTAL_URL", self._get_default_portal_url()),
            client_portal_url=os.getenv("CLIENT_PORTAL_URL", self._get_default_client_portal_url())
        )
        
        # Security configuration
        self.security = SecurityConfig(
            api_key_secret=self._get_required_env("API_KEY_SECRET"),
            jwt_secret=self._get_required_env("JWT_SECRET"),
            secret_key=os.getenv("SECRET_KEY", self._generate_fallback_secret()),
            session_timeout=int(os.getenv("SESSION_TIMEOUT", "3600")),
            rate_limit_per_minute=int(os.getenv("RATE_LIMIT_PER_MINUTE", "1000"))
        )
        
        # Feature flags
        self.features = FeatureFlags(
            semantic_engine=self._get_bool_env("ENABLE_SEMANTIC", True),
            observability=self._get_bool_env("OBSERVABILITY_ENABLED", True),
            caching=self._get_bool_env("ENABLE_CACHING", True),
            async_processing=self._get_bool_env("ENABLE_ASYNC", True),
            audit_logging=self._get_bool_env("ENABLE_AUDIT_LOG", True)
        )
    
    def _get_required_env(self, key: str) -> str:
        """Get required environment variable"""
        value = os.getenv(key)
        if not value:
            if self.environment == Environment.PRODUCTION:
                raise ValueError(f"Required environment variable {key} is not set")
            else:
                # Return development fallback
                return self._get_development_fallback(key)
        return value
    
    def _get_bool_env(self, key: str, default: bool = False) -> bool:
        """Get boolean environment variable"""
        value = os.getenv(key, str(default)).lower()
        return value in ("true", "1", "yes", "on")
    
    def _get_development_fallback(self, key: str) -> str:
        """Get development fallback values"""
        fallbacks = {
            "DATABASE_URL": "postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu",
            "API_KEY_SECRET": "dev_api_key_fallback_12345",
            "JWT_SECRET": "dev_jwt_secret_fallback_67890"
        }
        return fallbacks.get(key, f"dev_{key.lower()}_fallback")
    
    def _generate_fallback_secret(self) -> str:
        """Generate fallback secret for development"""
        import secrets
        return secrets.token_urlsafe(32)
    
    def _get_default_gateway_url(self) -> str:
        """Get default gateway URL based on environment"""
        if self.environment == Environment.PRODUCTION:
            return "https://bhiv-hr-gateway-46pz.onrender.com"
        return "http://gateway:8000"
    
    def _get_default_agent_url(self) -> str:
        """Get default agent URL based on environment"""
        if self.environment == Environment.PRODUCTION:
            return "https://bhiv-hr-agent-m1me.onrender.com"
        return "http://agent:9000"
    
    def _get_default_portal_url(self) -> str:
        """Get default portal URL based on environment"""
        if self.environment == Environment.PRODUCTION:
            return "https://bhiv-hr-portal-cead.onrender.com"
        return "http://localhost:8501"
    
    def _get_default_client_portal_url(self) -> str:
        """Get default client portal URL based on environment"""
        if self.environment == Environment.PRODUCTION:
            return "https://bhiv-hr-client-portal-5g33.onrender.com"
        return "http://localhost:8502"
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get configuration summary for debugging"""
        return {
            "environment": self.environment.value,
            "database": {
                "url_configured": bool(self.database.url),
                "pool_size": self.database.pool_size
            },
            "services": {
                "gateway": self.services.gateway_url,
                "agent": self.services.agent_url,
                "portal": self.services.portal_url,
                "client_portal": self.services.client_portal_url
            },
            "security": {
                "api_key_configured": bool(self.security.api_key_secret),
                "jwt_configured": bool(self.security.jwt_secret),
                "rate_limit": self.security.rate_limit_per_minute
            },
            "features": {
                "semantic_engine": self.features.semantic_engine,
                "observability": self.features.observability,
                "caching": self.features.caching,
                "async_processing": self.features.async_processing,
                "audit_logging": self.features.audit_logging
            }
        }
    
    def validate_configuration(self) -> Dict[str, Any]:
        """Validate configuration and return status"""
        issues = []
        warnings = []
        
        # Check required configurations
        if not self.database.url:
            issues.append("DATABASE_URL not configured")
        
        if not self.security.api_key_secret:
            issues.append("API_KEY_SECRET not configured")
        
        if not self.security.jwt_secret:
            issues.append("JWT_SECRET not configured")
        
        # Check environment-specific requirements
        if self.environment == Environment.PRODUCTION:
            if "fallback" in self.security.api_key_secret:
                warnings.append("Using fallback API key in production")
            
            if "localhost" in self.services.gateway_url:
                warnings.append("Using localhost URL in production")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "environment": self.environment.value
        }

# Global configuration instance
config = ConfigManager()

def get_config() -> ConfigManager:
    """Get global configuration instance"""
    return config

def reload_config() -> ConfigManager:
    """Reload configuration from environment"""
    global config
    config = ConfigManager()
    return config