"""BHIV HR Platform API Gateway Application Package
Version: 3.2.0 - Modular Architecture
"""

from .main import app

__version__ = "3.2.0"
__architecture__ = "modular"
__modules__ = ["core", "candidates", "jobs", "auth", "workflows", "monitoring"]

__all__ = ["app"]
