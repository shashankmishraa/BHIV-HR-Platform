"""Configuration management for gateway service"""

import os
from typing import List

class Settings:
    """Application settings"""
    
    def __init__(self):
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.environment = os.getenv("ENVIRONMENT", "production")
        self.cors_origins = ["*"]
        self.agent_service_url = os.getenv("AGENT_SERVICE_URL", "https://bhiv-hr-agent-m1me.onrender.com")
        self.api_key_secret = os.getenv("API_KEY_SECRET", "fallback_secret_key")
        self.jwt_secret = os.getenv("JWT_SECRET", "fallback_jwt_secret")
        self.database_url = os.getenv("DATABASE_URL", "")
        self.secret_key = os.getenv("SECRET_KEY", "fallback_secret")

def get_settings() -> Settings:
    """Get application settings"""
    return Settings()

def is_production() -> bool:
    """Check if running in production"""
    return os.getenv("ENVIRONMENT", "production").lower() == "production"