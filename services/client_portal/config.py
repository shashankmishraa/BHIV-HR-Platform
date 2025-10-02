import requests
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# API Configuration
API_BASE_URL = os.getenv("GATEWAY_URL", "https://bhiv-hr-gateway-46pz.onrender.com")
API_KEY = os.getenv("API_KEY_SECRET", "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o")

# Set required environment variables for auth service
os.environ.setdefault("DATABASE_URL", "postgresql://bhiv_user:bhiv_password@dpg-ctdvhf3tq21c73c5uqag-a.oregon-postgres.render.com/bhiv_hr_db")
os.environ.setdefault("JWT_SECRET", "fallback_jwt_secret_key_for_client_auth_2025")

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Ensure environment variables are available
if not os.getenv("DATABASE_URL"):
    os.environ["DATABASE_URL"] = "postgresql://bhiv_user:bhiv_password@dpg-ctdvhf3tq21c73c5uqag-a.oregon-postgres.render.com/bhiv_hr_db"
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