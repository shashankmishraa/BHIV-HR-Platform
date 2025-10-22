import os
from typing import Optional

class Config:
    """Configuration for Candidate Portal"""
    
    def __init__(self):
        # Gateway API Configuration
        self.GATEWAY_URL = os.getenv(
            "GATEWAY_URL", 
            "https://bhiv-hr-gateway-46pz.onrender.com"
        )
        
        # API Authentication
        self.API_KEY = os.getenv(
            "API_KEY", 
            "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
        )
        
        # JWT Configuration for candidate authentication
        self.JWT_SECRET = os.getenv(
            "JWT_SECRET", 
            "candidate_jwt_secret_key_2025"
        )
        
        # Database Configuration (if needed for direct access)
        self.DATABASE_URL = os.getenv(
            "DATABASE_URL",
            "postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu"
        )
        
        # Portal Configuration
        self.PORTAL_PORT = int(os.getenv("CANDIDATE_PORTAL_PORT", "8503"))
        self.DEBUG = os.getenv("DEBUG", "False").lower() == "true"
        
        # File Upload Configuration
        self.MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
        self.ALLOWED_EXTENSIONS = ["pdf", "docx", "txt"]
        
        # Session Configuration
        self.SESSION_TIMEOUT = int(os.getenv("SESSION_TIMEOUT", "3600"))  # 1 hour
        
    def get_headers(self, token: Optional[str] = None) -> dict:
        """Get API headers with authentication"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token or self.API_KEY}"
        }
        return headers