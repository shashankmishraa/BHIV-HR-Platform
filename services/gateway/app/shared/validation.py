"""Shared validation utilities for BHIV HR Platform"""

from typing import List, Union, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator
from enum import Enum


class ExperienceLevel(str, Enum):
    """Standardized experience levels"""

    ENTRY = "Entry-level"
    MID = "Mid-level"
    SENIOR = "Senior-level"
    LEAD = "Lead-level"
    EXECUTIVE = "Executive-level"


class JobType(str, Enum):
    """Standardized job types"""

    FULL_TIME = "Full-time"
    PART_TIME = "Part-time"
    CONTRACT = "Contract"
    INTERN = "Intern"
    FREELANCE = "Freelance"


class ValidationUtils:
    """Utility functions for data validation"""

    @staticmethod
    def normalize_requirements(requirements: Union[List[str], str]) -> List[str]:
        """Convert requirements to standardized list format"""
        if isinstance(requirements, str):
            # Split by comma, semicolon, or newline and clean up
            import re

            items = re.split(r"[,;\n]", requirements)
            return [item.strip() for item in items if item.strip()]
        elif isinstance(requirements, list):
            return [str(item).strip() for item in requirements if str(item).strip()]
        else:
            raise ValueError("Requirements must be a list or comma-separated string")

    @staticmethod
    def normalize_experience_level(level: str) -> str:
        """Normalize experience level to standard format"""
        level_mapping = {
            # Input variations -> Standard format
            "entry": ExperienceLevel.ENTRY,
            "entry-level": ExperienceLevel.ENTRY,
            "entry level": ExperienceLevel.ENTRY,
            "junior": ExperienceLevel.ENTRY,
            "mid": ExperienceLevel.MID,
            "mid-level": ExperienceLevel.MID,
            "mid level": ExperienceLevel.MID,
            "middle": ExperienceLevel.MID,
            "intermediate": ExperienceLevel.MID,
            "senior": ExperienceLevel.SENIOR,
            "senior-level": ExperienceLevel.SENIOR,
            "senior level": ExperienceLevel.SENIOR,
            "sr": ExperienceLevel.SENIOR,
            "lead": ExperienceLevel.LEAD,
            "lead-level": ExperienceLevel.LEAD,
            "lead level": ExperienceLevel.LEAD,
            "team lead": ExperienceLevel.LEAD,
            "tech lead": ExperienceLevel.LEAD,
            "executive": ExperienceLevel.EXECUTIVE,
            "executive-level": ExperienceLevel.EXECUTIVE,
            "executive level": ExperienceLevel.EXECUTIVE,
            "c-level": ExperienceLevel.EXECUTIVE,
            "director": ExperienceLevel.EXECUTIVE,
        }

        normalized_key = level.lower().strip()
        result = level_mapping.get(normalized_key)

        if not result:
            raise ValueError(
                f"Invalid experience level: '{level}'. Supported: Entry, Mid, Senior, Lead, Executive"
            )

        return result.value

    @staticmethod
    def validate_salary_range(salary_min: int, salary_max: int) -> tuple[int, int]:
        """Validate and normalize salary range"""
        if salary_min < 0:
            raise ValueError("Minimum salary cannot be negative")
        if salary_max < 0:
            raise ValueError("Maximum salary cannot be negative")
        if salary_max < salary_min:
            raise ValueError(
                "Maximum salary must be greater than or equal to minimum salary"
            )
        if salary_min > 10000000 or salary_max > 10000000:
            raise ValueError("Salary values cannot exceed $10,000,000")

        return salary_min, salary_max

    @staticmethod
    def validate_job_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive job data validation and normalization"""
        validated_data = data.copy()

        # Normalize requirements
        if "requirements" in validated_data:
            validated_data["requirements"] = ValidationUtils.normalize_requirements(
                validated_data["requirements"]
            )

        # Normalize experience level
        if "experience_level" in validated_data:
            validated_data["experience_level"] = (
                ValidationUtils.normalize_experience_level(
                    validated_data["experience_level"]
                )
            )

        # Validate salary range
        if "salary_min" in validated_data and "salary_max" in validated_data:
            salary_min, salary_max = ValidationUtils.validate_salary_range(
                validated_data["salary_min"], validated_data["salary_max"]
            )
            validated_data["salary_min"] = salary_min
            validated_data["salary_max"] = salary_max

        return validated_data


class StandardJobCreate(BaseModel):
    """Standardized job creation model with comprehensive validation"""

    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=20, max_length=5000)
    requirements: Union[List[str], str] = Field(
        ..., description="Skills and requirements"
    )
    location: str = Field(..., min_length=2, max_length=100)
    department: str = Field(..., min_length=2, max_length=100)
    experience_level: str = Field(
        ..., description="Experience level (Entry, Mid, Senior, Lead, Executive)"
    )
    salary_min: int = Field(
        ..., ge=0, le=10000000, description="Minimum salary (required)"
    )
    salary_max: int = Field(
        ..., ge=0, le=10000000, description="Maximum salary (required)"
    )
    job_type: str = Field(default="Full-time")
    company_id: Union[str, int] = Field(default="default")

    @field_validator("requirements")
    @classmethod
    def validate_requirements(cls, v):
        return ValidationUtils.normalize_requirements(v)

    @field_validator("experience_level")
    @classmethod
    def validate_experience_level(cls, v):
        return ValidationUtils.normalize_experience_level(v)

    @field_validator("salary_max")
    @classmethod
    def validate_salary_range(cls, v, info):
        if "salary_min" in info.data:
            ValidationUtils.validate_salary_range(info.data["salary_min"], v)
        return v


class StandardJobUpdate(BaseModel):
    """Standardized job update model"""

    title: Optional[str] = Field(None, min_length=5, max_length=200)
    description: Optional[str] = Field(None, min_length=20, max_length=5000)
    requirements: Optional[Union[List[str], str]] = Field(None)
    location: Optional[str] = Field(None, min_length=2, max_length=100)
    department: Optional[str] = Field(None, min_length=2, max_length=100)
    experience_level: Optional[str] = Field(None)
    salary_min: Optional[int] = Field(None, ge=0, le=10000000)
    salary_max: Optional[int] = Field(None, ge=0, le=10000000)
    job_type: Optional[str] = None

    @field_validator("requirements")
    @classmethod
    def validate_requirements(cls, v):
        if v is not None:
            return ValidationUtils.normalize_requirements(v)
        return v

    @field_validator("experience_level")
    @classmethod
    def validate_experience_level(cls, v):
        if v is not None:
            return ValidationUtils.normalize_experience_level(v)
        return v
