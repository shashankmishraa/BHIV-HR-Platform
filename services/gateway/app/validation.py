#!/usr/bin/env python3
"""
Request Validation System
Standardized parameter and request body validation
"""

import re
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, validator
from fastapi import HTTPException

# Validation patterns
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
PHONE_PATTERN = re.compile(r'^\+?1?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}$')
API_KEY_PATTERN = re.compile(r'^[a-zA-Z0-9_-]{16,}$')

class ValidationError(Exception):
    """Custom validation error"""
    pass

def validate_email(email: str) -> bool:
    """Validate email format"""
    return bool(EMAIL_PATTERN.match(email))

def validate_phone(phone: str) -> bool:
    """Validate phone format"""
    return bool(PHONE_PATTERN.match(phone))

def validate_api_key_format(api_key: str) -> bool:
    """Validate API key format"""
    return bool(API_KEY_PATTERN.match(api_key))

def validate_pagination(limit: int, offset: int) -> None:
    """Validate pagination parameters"""
    if limit < 1 or limit > 100:
        raise HTTPException(status_code=400, detail="Limit must be between 1 and 100")
    if offset < 0:
        raise HTTPException(status_code=400, detail="Offset must be non-negative")

def validate_password_strength(password: str) -> Dict[str, Any]:
    """Validate password strength"""
    score = 0
    feedback = []
    
    if len(password) >= 8:
        score += 20
    else:
        feedback.append("Password should be at least 8 characters long")
    
    if any(c.isupper() for c in password):
        score += 20
    else:
        feedback.append("Password should contain uppercase letters")
    
    if any(c.islower() for c in password):
        score += 20
    else:
        feedback.append("Password should contain lowercase letters")
    
    if any(c.isdigit() for c in password):
        score += 20
    else:
        feedback.append("Password should contain numbers")
    
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        score += 20
    else:
        feedback.append("Password should contain special characters")
    
    return {
        "score": score,
        "is_valid": score >= 60,
        "feedback": feedback
    }

# Standardized request models
class JobCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    department: str = Field(..., min_length=1, max_length=100)
    location: str = Field(..., min_length=1, max_length=100)
    experience_level: str = Field(..., min_length=1, max_length=50)
    requirements: str = Field(..., min_length=1, max_length=2000)
    description: str = Field(..., min_length=1, max_length=5000)
    client_id: Optional[int] = Field(default=1, ge=1)
    employment_type: Optional[str] = Field(default="Full-time", max_length=50)

class CandidateSearchRequest(BaseModel):
    skills: Optional[str] = Field(None, max_length=200)
    location: Optional[str] = Field(None, max_length=100)
    experience_min: Optional[int] = Field(None, ge=0, le=50)
    
    @validator('skills')
    def validate_skills(cls, v):
        if v and len(v.strip()) == 0:
            return None
        return v.strip() if v else None

class PasswordValidationRequest(BaseModel):
    password: str = Field(..., min_length=1, max_length=128)

class EmailValidationRequest(BaseModel):
    email: str = Field(..., min_length=1, max_length=254)
    
    @validator('email')
    def validate_email_format(cls, v):
        if not validate_email(v):
            raise ValueError('Invalid email format')
        return v

class PhoneValidationRequest(BaseModel):
    phone: str = Field(..., min_length=1, max_length=20)
    
    @validator('phone')
    def validate_phone_format(cls, v):
        if not validate_phone(v):
            raise ValueError('Invalid phone format')
        return v

class TwoFASetupRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=50)

class TwoFALoginRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=50)
    totp_code: str = Field(..., min_length=6, max_length=6, pattern=r'^\d{6}$')

class ClientLoginRequest(BaseModel):
    client_id: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=1, max_length=128)

class FeedbackSubmissionRequest(BaseModel):
    candidate_id: int = Field(..., ge=1)
    job_id: int = Field(..., ge=1)
    integrity: int = Field(..., ge=1, le=5)
    honesty: int = Field(..., ge=1, le=5)
    discipline: int = Field(..., ge=1, le=5)
    hard_work: int = Field(..., ge=1, le=5)
    gratitude: int = Field(..., ge=1, le=5)
    comments: Optional[str] = Field(None, max_length=1000)

class InterviewScheduleRequest(BaseModel):
    candidate_id: int = Field(..., ge=1)
    job_id: int = Field(..., ge=1)
    interview_date: str = Field(..., min_length=1)
    interviewer: Optional[str] = Field(default="HR Team", max_length=100)
    notes: Optional[str] = Field(None, max_length=1000)

class SecurityTestRequest(BaseModel):
    test_type: str = Field(..., min_length=1, max_length=50)
    payload: str = Field(..., min_length=1, max_length=1000)

class CSPReportRequest(BaseModel):
    violated_directive: str = Field(..., min_length=1, max_length=100)
    blocked_uri: str = Field(..., min_length=1, max_length=500)
    document_uri: str = Field(..., min_length=1, max_length=500)

class PasswordChangeRequest(BaseModel):
    old_password: str = Field(..., min_length=1, max_length=128)
    new_password: str = Field(..., min_length=8, max_length=128)
    
    @validator('new_password')
    def validate_new_password(cls, v):
        validation = validate_password_strength(v)
        if not validation['is_valid']:
            raise ValueError(f"Password too weak: {', '.join(validation['feedback'])}")
        return v

def validate_request_params(
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    hours: Optional[int] = None,
    job_id: Optional[int] = None,
    candidate_id: Optional[int] = None
) -> None:
    """Validate common request parameters"""
    
    if limit is not None:
        if limit < 1 or limit > 100:
            raise HTTPException(status_code=400, detail="Limit must be between 1 and 100")
    
    if offset is not None:
        if offset < 0:
            raise HTTPException(status_code=400, detail="Offset must be non-negative")
    
    if hours is not None:
        if hours < 1 or hours > 168:  # Max 1 week
            raise HTTPException(status_code=400, detail="Hours must be between 1 and 168")
    
    if job_id is not None:
        if job_id < 1:
            raise HTTPException(status_code=400, detail="Job ID must be positive")
    
    if candidate_id is not None:
        if candidate_id < 1:
            raise HTTPException(status_code=400, detail="Candidate ID must be positive")

def sanitize_input(input_str: str, max_length: int = 1000) -> str:
    """Sanitize input string"""
    if not input_str:
        return ""
    
    # Remove potential XSS patterns
    sanitized = input_str.replace("<script>", "").replace("</script>", "")
    sanitized = sanitized.replace("javascript:", "")
    sanitized = sanitized.replace("onload=", "").replace("onerror=", "")
    
    # Limit length
    return sanitized[:max_length].strip()