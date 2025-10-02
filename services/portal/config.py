import httpx
import os

# API Configuration
API_BASE = os.getenv("GATEWAY_URL", "https://bhiv-hr-gateway-46pz.onrender.com")
API_KEY = os.getenv("API_KEY_SECRET", "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o")

# HTTP Client Configuration with proper timeouts
timeout_config = httpx.Timeout(
    connect=15.0,  # Connection timeout
    read=60.0,     # Read timeout for long operations
    write=30.0,    # Write timeout
    pool=10.0      # Pool timeout
)

limits = httpx.Limits(
    max_keepalive_connections=10,
    max_connections=20,
    keepalive_expiry=30.0
)

headers = {"Authorization": f"Bearer {API_KEY}"}

# Global HTTP client with connection pooling
http_client = httpx.Client(
    timeout=timeout_config,
    limits=limits,
    headers=headers,
    follow_redirects=True
)