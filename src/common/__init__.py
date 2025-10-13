"""
BHIV HR Platform - Common Utilities
Shared utilities and constants across all services
Version: 3.1.0 with Phase 3 Features
Updated: October 13, 2025
Status: Production Ready
"""

__version__ = "3.1.0"
__author__ = "BHIV HR Platform Team"
__updated__ = "2025-10-13"
__status__ = "Production Ready"

# Common constants
API_VERSION = "v1"
DEFAULT_PAGE_SIZE = 50
MAX_PAGE_SIZE = 100
DEFAULT_TIMEOUT = 30

# Service names
SERVICES = {
    "gateway": "API Gateway",
    "agent": "AI Agent", 
    "portal": "HR Portal",
    "client_portal": "Client Portal",
    "database": "Database"
}

# API endpoints base paths
API_PATHS = {
    "jobs": "/v1/jobs",
    "candidates": "/v1/candidates", 
    "matching": "/v1/match",
    "feedback": "/v1/feedback",
    "interviews": "/v1/interviews",
    "offers": "/v1/offers"
}