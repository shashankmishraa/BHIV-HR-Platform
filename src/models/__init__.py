"""
BHIV HR Platform - Shared Data Models
Common Pydantic models used across services
Version: 3.1.0 with Phase 3 Features
Updated: October 13, 2025
Status: Production Ready

Provides standardized data models for:
- API responses and error handling
- Health checks and service information
- Pagination and data validation
- Cross-service communication
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class BaseResponse(BaseModel):
    """Base response model for all API responses"""
    success: bool = True
    message: str = "Operation completed successfully"
    timestamp: datetime = Field(default_factory=datetime.now)

class ErrorResponse(BaseResponse):
    """Error response model"""
    success: bool = False
    error_code: Optional[str] = None
    details: Optional[dict] = None

class PaginatedResponse(BaseResponse):
    """Paginated response model"""
    total: int
    page: int = 1
    page_size: int = 50
    has_next: bool = False
    has_previous: bool = False

class HealthCheck(BaseModel):
    """Health check response model"""
    status: str = "healthy"
    service: str
    version: str
    timestamp: datetime = Field(default_factory=datetime.now)
    uptime_seconds: Optional[float] = None

class ServiceInfo(BaseModel):
    """Service information model"""
    name: str
    version: str
    endpoints: int
    status: str = "operational"
    url: Optional[str] = None
    updated: Optional[str] = "2025-10-13"

__version__ = "3.1.0"
__updated__ = "2025-10-13"
__status__ = "Production Ready"