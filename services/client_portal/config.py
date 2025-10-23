"""
BHIV HR Platform - Client Portal Configuration
Version: 3.1.0 with Phase 3 Features
Updated: October 13, 2025
Status: Production Ready

Configuration for Client Portal Streamlit application:
- API Gateway connection settings
- JWT authentication configuration
- HTTP session with retry strategy
- Production database connections
"""

import requests
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Version Information
__version__ = "3.1.0"
__updated__ = "2025-10-23"
__status__ = "Production Ready - Database Fixed"

# API Configuration - FIXED FOR PRODUCTION
# Production: Use actual Render URLs, not Docker internal URLs
API_BASE_URL = os.getenv("GATEWAY_URL", "https://bhiv-hr-gateway-46pz.onrender.com")
API_KEY = os.getenv("API_KEY_SECRET", "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o")

# Set required environment variables for auth service
os.environ.setdefault("DATABASE_URL", "postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu")
os.environ.setdefault("JWT_SECRET", "fallback_jwt_secret_key_for_client_auth_2025")

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Ensure environment variables are available
if not os.getenv("DATABASE_URL"):
    os.environ["DATABASE_URL"] = "postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu"
if not os.getenv("JWT_SECRET"):
    os.environ["JWT_SECRET"] = "fallback_jwt_secret_key_for_client_auth_2025"

# Configure session with retry strategy and timeouts
def create_session():
    session = requests.Session()
    
    # Retry strategy
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    
    # Mount adapter with retry strategy
    adapter = HTTPAdapter(
        max_retries=retry_strategy,
        pool_connections=10,
        pool_maxsize=20
    )
    
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update(headers)
    
    # Set timeouts
    session.timeout = (15, 60)  # (connect, read)
    
    return session

# Global session
http_session = create_session()

# Client Portal Configuration
CLIENT_PORTAL_CONFIG = {
    "title": "BHIV HR Platform - Client Portal",
    "version": __version__,
    "authentication": "JWT Token-based",
    "features": [
        "Job Posting",
        "Candidate Review", 
        "Interview Scheduling",
        "Offer Management",
        "Real-time Sync with HR Portal"
    ],
    "demo_credentials": {
        "username": "TECH001",
        "password": "demo123"
    },
    "status": __status__,
    "updated": __updated__
}