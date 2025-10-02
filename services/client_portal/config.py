import requests
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# API Configuration
API_BASE_URL = os.getenv("GATEWAY_URL", "https://bhiv-hr-gateway-46pz.onrender.com")
API_KEY = os.getenv("API_KEY_SECRET", "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o")

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

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