# Validation Middleware
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError
import json

async def validation_exception_handler(request: Request, exc: ValidationError):
    """Custom validation error handler"""
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(x) for x in error["loc"])
        errors.append({
            "field": field,
            "message": error["msg"],
            "type": error["type"],
            "input": error.get("input")
        })
    
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "message": "Request validation failed",
            "details": errors,
            "total_errors": len(errors)
        }
    )

def validate_required_fields(data: dict, required_fields: list) -> list:
    """Validate required fields are present"""
    missing_fields = []
    for field in required_fields:
        if field not in data or data[field] is None or data[field] == "":
            missing_fields.append(field)
    return missing_fields

def validate_job_data(job_data: dict) -> dict:
    """Validate job creation data"""
    required_fields = [
        "title", "description", "requirements", "location", 
        "department", "experience_level", "salary_min", "salary_max"
    ]
    
    missing = validate_required_fields(job_data, required_fields)
    if missing:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "Missing required fields",
                "missing_fields": missing,
                "required_fields": required_fields
            }
        )
    
    # Validate salary range
    if job_data.get("salary_max", 0) < job_data.get("salary_min", 0):
        raise HTTPException(
            status_code=422,
            detail={
                "error": "Invalid salary range",
                "message": "salary_max must be greater than or equal to salary_min"
            }
        )
    
    # Validate experience level
    valid_levels = ["Entry-level", "Mid-level", "Senior", "Lead", "Executive"]
    if job_data.get("experience_level") not in valid_levels:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "Invalid experience level",
                "valid_options": valid_levels,
                "provided": job_data.get("experience_level")
            }
        )
    
    return job_data

def validate_candidate_data(candidate_data: dict) -> dict:
    """Validate candidate creation data"""
    required_fields = ["name", "email"]
    
    missing = validate_required_fields(candidate_data, required_fields)
    if missing:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "Missing required fields",
                "missing_fields": missing,
                "required_fields": required_fields
            }
        )
    
    # Validate email format
    email = candidate_data.get("email", "")
    if "@" not in email or "." not in email:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "Invalid email format",
                "message": "Email must contain @ and . characters"
            }
        )
    
    return candidate_data