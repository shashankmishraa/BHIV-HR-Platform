"""
BHIV HR Platform - HR Portal Configuration
Version: 3.1.0 with Phase 3 Features
Updated: October 13, 2025
Status: Production Ready

Configuration for HR Portal Streamlit application:
- API Gateway connection settings
- HTTP client with connection pooling
- Timeout and retry configurations
- Production-ready defaults
"""

import httpx
import os

# Version Information
__version__ = "3.1.0"
__updated__ = "2025-10-13"
__status__ = "Production Ready"

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

# Portal Configuration
PORTAL_CONFIG = {
    "title": "BHIV HR Platform - Dashboard",
    "version": __version__,
    "api_endpoints": 50,
    "features": [
        "Candidate Management",
        "Job Posting", 
        "AI Matching",
        "Values Assessment",
        "Interview Scheduling",
        "Offer Management"
    ],
    "status": __status__,
    "updated": __updated__
}