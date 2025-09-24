"""Configuration management for BHIV HR Platform Gateway"""

import os
from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    app_name: str = "BHIV HR Platform Gateway"
    version: str = "3.2.0"
    environment: str = Field(default="production", env="ENVIRONMENT")
    debug: bool = Field(default=False, env="DEBUG")
    
    # Server
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    
    # Database
    database_url: str = Field(..., env="DATABASE_URL")
    
    # Security
    api_key_secret: str = Field(..., env="API_KEY_SECRET")
    jwt_secret: str = Field(..., env="JWT_SECRET")
    security_enabled: bool = Field(default=True, env="SECURITY_ENABLED")
    
    # CORS
    cors_origins: List[str] = Field(
        default=["*"], 
        env="CORS_ORIGINS"
    )
    
    # Service URLs
    agent_service_url: str = Field(
        default="https://bhiv-hr-agent-o6nx.onrender.com",
        env="AGENT_SERVICE_URL"
    )
    portal_url: str = Field(
        default="https://bhiv-hr-portal-xk2k.onrender.com",
        env="PORTAL_URL"
    )
    client_portal_url: str = Field(
        default="https://bhiv-hr-client-portal-zdbt.onrender.com",
        env="CLIENT_PORTAL_URL"
    )
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Rate Limiting
    rate_limit_requests: int = Field(default=60, env="RATE_LIMIT_REQUESTS")
    rate_limit_window: int = Field(default=60, env="RATE_LIMIT_WINDOW")
    
    # Workflow Settings
    workflow_timeout: int = Field(default=3600, env="WORKFLOW_TIMEOUT")
    max_concurrent_workflows: int = Field(default=50, env="MAX_CONCURRENT_WORKFLOWS")
    
    # Monitoring
    metrics_enabled: bool = Field(default=True, env="METRICS_ENABLED")
    health_check_interval: int = Field(default=30, env="HEALTH_CHECK_INTERVAL")
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra environment variables
        
        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str):
            if field_name == 'cors_origins':
                return [x.strip() for x in raw_val.split(',')]
            return cls.json_loads(raw_val)

# Global settings instance
settings = Settings()

def get_settings() -> Settings:
    """Get application settings"""
    return settings

def is_production() -> bool:
    """Check if running in production"""
    return settings.environment.lower() == "production"

def is_development() -> bool:
    """Check if running in development"""
    return settings.environment.lower() in ["development", "dev"]

def get_database_url() -> str:
    """Get database URL"""
    return settings.database_url

def get_cors_origins() -> List[str]:
    """Get CORS origins"""
    return settings.cors_origins