"""Shared configuration management for BHIV HR Platform Services"""

import os
from typing import Dict, Any


class ServiceConfig:
    """Shared configuration for all services"""

    def __init__(self):
        self.environment = os.getenv("ENVIRONMENT", "production").lower()
        self.database_url = self._get_database_url()
        self.api_key_secret = os.getenv(
            "API_KEY_SECRET", "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
        )
        self.jwt_secret = os.getenv(
            "JWT_SECRET", "prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA"
        )

        # Service URLs
        self.gateway_url = self._get_gateway_url()
        self.agent_url = self._get_agent_url()
        self.portal_url = self._get_portal_url()
        self.client_portal_url = self._get_client_portal_url()

    def _get_database_url(self) -> str:
        """Get database URL based on environment"""
        if self.environment == "production":
            return os.getenv(
                "DATABASE_URL",
                "postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@dpg-d373qrogjchc73bu9gug-a.oregon-postgres.render.com/bhiv_hr_nqzb",
            )
        else:
            return os.getenv(
                "DATABASE_URL",
                "postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@db:5432/bhiv_hr_nqzb",
            )

    def _get_gateway_url(self) -> str:
        """Get gateway service URL"""
        if self.environment == "production":
            return os.getenv("GATEWAY_URL", "https://bhiv-hr-gateway-901a.onrender.com")
        else:
            return os.getenv("GATEWAY_URL", "http://gateway:8000")

    def _get_agent_url(self) -> str:
        """Get agent service URL"""
        if self.environment == "production":
            return os.getenv(
                "AGENT_SERVICE_URL", "https://bhiv-hr-agent-o6nx.onrender.com"
            )
        else:
            return os.getenv("AGENT_SERVICE_URL", "http://agent:9000")

    def _get_portal_url(self) -> str:
        """Get portal service URL"""
        if self.environment == "production":
            return os.getenv("PORTAL_URL", "https://bhiv-hr-portal-xk2k.onrender.com")
        else:
            return os.getenv("PORTAL_URL", "http://portal:8501")

    def _get_client_portal_url(self) -> str:
        """Get client portal service URL"""
        if self.environment == "production":
            return os.getenv(
                "CLIENT_PORTAL_URL", "https://bhiv-hr-client-portal-zdbt.onrender.com"
            )
        else:
            return os.getenv("CLIENT_PORTAL_URL", "http://client_portal:8502")

    def get_service_urls(self) -> Dict[str, str]:
        """Get all service URLs"""
        return {
            "gateway": self.gateway_url,
            "agent": self.agent_url,
            "portal": self.portal_url,
            "client_portal": self.client_portal_url,
        }

    def get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers"""
        return {
            "Authorization": f"Bearer {self.api_key_secret}",
            "Content-Type": "application/json",
        }

    def is_production(self) -> bool:
        """Check if running in production"""
        return self.environment == "production"

    def is_development(self) -> bool:
        """Check if running in development"""
        return self.environment in ["development", "dev"]


# Global configuration instance
service_config = ServiceConfig()


def get_service_config() -> ServiceConfig:
    """Get service configuration"""
    return service_config
