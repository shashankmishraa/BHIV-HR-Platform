#!/usr/bin/env python3
"""
Comprehensive validation tests for HR Portal and Client Portal
Tests all validation scenarios including edge cases
"""

import sys
import os
import pytest
from pydantic import ValidationError

# Add paths for imports
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "services", "gateway", "app")
)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "services"))

from services.shared.models import JobCreate, JobUpdate
from services.shared.validation import ValidationUtils, StandardJobCreate


class TestJobValidation:
    """Test job creation and update validation"""

    def test_valid_job_creation_list_requirements(self):
        """Test valid job creation with list requirements"""
        job_data = {
            "title": "Senior Software Engineer",
            "description": "We are looking for a senior software engineer with strong technical skills",
            "requirements": ["Python", "FastAPI", "PostgreSQL"],  # List format
            "location": "San Francisco, CA",
            "department": "Engineering",
            "experience_level": "Senior-level",
            "salary_min": 120000,
            "salary_max": 180000,
        }

        job = JobCreate(**job_data)
        assert job.title == "Senior Software Engineer"
        assert isinstance(job.requirements, list)
        assert len(job.requirements) == 3
        assert job.experience_level == "Senior-level"
        assert job.salary_min == 120000
        assert job.salary_max == 180000

    def test_valid_job_creation_string_requirements(self):
        """Test valid job creation with string requirements (should convert to list)"""
        job_data = {
            "title": "Software Engineer",
            "description": "Looking for a software engineer with good skills",
            "requirements": "Python, FastAPI, PostgreSQL, Docker",  # String format
            "location": "New York, NY",
            "department": "Engineering",
            "experience_level": "Mid-level",
            "salary_min": 80000,
            "salary_max": 120000,
        }

        job = JobCreate(**job_data)
        assert isinstance(job.requirements, list)
        assert len(job.requirements) == 4
        assert "Python" in job.requirements
        assert "Docker" in job.requirements

    def test_experience_level_normalization(self):
        """Test experience level normalization"""
        test_cases = [
            ("Entry", "Entry-level"),
            ("Mid", "Mid-level"),
            ("Senior", "Senior-level"),
            ("Lead", "Lead-level"),
            ("Executive", "Executive-level"),
        ]

        for input_level, expected_level in test_cases:
            job_data = {
                "title": "Test Job",
                "description": "Test job description for validation",
                "requirements": ["Python"],
                "location": "Test City",
                "department": "Engineering",
                "experience_level": input_level,
                "salary_min": 50000,
                "salary_max": 80000,
            }

            job = JobCreate(**job_data)
            assert job.experience_level == expected_level

    def test_invalid_experience_level(self):
        """Test invalid experience level raises validation error"""
        job_data = {
            "title": "Test Job",
            "description": "Test job description for validation",
            "requirements": ["Python"],
            "location": "Test City",
            "department": "Engineering",
            "experience_level": "Expert",  # Invalid
            "salary_min": 50000,
            "salary_max": 80000,
        }

        with pytest.raises(ValidationError) as exc_info:
            JobCreate(**job_data)

        errors = exc_info.value.errors()
        assert any("experience_level" in str(error["loc"]) for error in errors)

    def test_missing_salary_fields(self):
        """Test missing salary fields raise validation errors"""
        job_data = {
            "title": "Test Job",
            "description": "Test job description for validation",
            "requirements": ["Python"],
            "location": "Test City",
            "department": "Engineering",
            "experience_level": "Senior-level",
            # Missing salary_min and salary_max
        }

        with pytest.raises(ValidationError) as exc_info:
            JobCreate(**job_data)

        errors = exc_info.value.errors()
        error_fields = [str(error["loc"]) for error in errors]
        assert any("salary_min" in field for field in error_fields)
        assert any("salary_max" in field for field in error_fields)

    def test_invalid_salary_range(self):
        """Test invalid salary range (max < min) raises validation error"""
        job_data = {
            "title": "Test Job",
            "description": "Test job description for validation",
            "requirements": ["Python"],
            "location": "Test City",
            "department": "Engineering",
            "experience_level": "Senior-level",
            "salary_min": 120000,
            "salary_max": 80000,  # Invalid: max < min
        }

        with pytest.raises(ValidationError) as exc_info:
            JobCreate(**job_data)

        errors = exc_info.value.errors()
        assert any("salary_max" in str(error["loc"]) for error in errors)

    def test_empty_requirements_string(self):
        """Test empty requirements string raises validation error"""
        job_data = {
            "title": "Test Job",
            "description": "Test job description for validation",
            "requirements": "",  # Empty string
            "location": "Test City",
            "department": "Engineering",
            "experience_level": "Senior-level",
            "salary_min": 50000,
            "salary_max": 80000,
        }

        with pytest.raises(ValidationError) as exc_info:
            JobCreate(**job_data)

        errors = exc_info.value.errors()
        assert any("requirements" in str(error["loc"]) for error in errors)

    def test_empty_requirements_list(self):
        """Test empty requirements list raises validation error"""
        job_data = {
            "title": "Test Job",
            "description": "Test job description for validation",
            "requirements": [],  # Empty list
            "location": "Test City",
            "department": "Engineering",
            "experience_level": "Senior-level",
            "salary_min": 50000,
            "salary_max": 80000,
        }

        with pytest.raises(ValidationError) as exc_info:
            JobCreate(**job_data)

        errors = exc_info.value.errors()
        assert any("requirements" in str(error["loc"]) for error in errors)


class TestValidationUtils:
    """Test validation utility functions"""

    def test_normalize_requirements_string(self):
        """Test requirements normalization from string"""
        test_cases = [
            ("Python, FastAPI, PostgreSQL", ["Python", "FastAPI", "PostgreSQL"]),
            ("Python; FastAPI; PostgreSQL", ["Python", "FastAPI", "PostgreSQL"]),
            ("Python\nFastAPI\nPostgreSQL", ["Python", "FastAPI", "PostgreSQL"]),
            (
                "  Python  ,  FastAPI  ,  PostgreSQL  ",
                ["Python", "FastAPI", "PostgreSQL"],
            ),
        ]

        for input_str, expected in test_cases:
            result = ValidationUtils.normalize_requirements(input_str)
            assert result == expected

    def test_normalize_requirements_list(self):
        """Test requirements normalization from list"""
        input_list = ["Python", "FastAPI", "PostgreSQL"]
        result = ValidationUtils.normalize_requirements(input_list)
        assert result == input_list

    def test_normalize_experience_level_variations(self):
        """Test experience level normalization with various inputs"""
        test_cases = [
            ("entry", "Entry-level"),
            ("ENTRY", "Entry-level"),
            ("Entry Level", "Entry-level"),
            ("junior", "Entry-level"),
            ("mid", "Mid-level"),
            ("middle", "Mid-level"),
            ("intermediate", "Mid-level"),
            ("senior", "Senior-level"),
            ("sr", "Senior-level"),
            ("lead", "Lead-level"),
            ("team lead", "Lead-level"),
            ("executive", "Executive-level"),
            ("c-level", "Executive-level"),
        ]

        for input_level, expected in test_cases:
            result = ValidationUtils.normalize_experience_level(input_level)
            assert result == expected

    def test_validate_salary_range_valid(self):
        """Test valid salary range validation"""
        result = ValidationUtils.validate_salary_range(50000, 80000)
        assert result == (50000, 80000)

    def test_validate_salary_range_invalid(self):
        """Test invalid salary range validation"""
        with pytest.raises(ValueError):
            ValidationUtils.validate_salary_range(80000, 50000)  # max < min

        with pytest.raises(ValueError):
            ValidationUtils.validate_salary_range(-10000, 50000)  # negative min

        with pytest.raises(ValueError):
            ValidationUtils.validate_salary_range(50000, -10000)  # negative max


class TestPortalIntegration:
    """Test portal-specific validation scenarios"""

    def test_hr_portal_format(self):
        """Test HR Portal data format validation"""
        hr_portal_data = {
            "title": "Senior Software Engineer",
            "department": "Engineering",
            "location": "Remote",
            "experience_level": "Senior",  # HR Portal format
            "requirements": "Python, FastAPI, PostgreSQL, Docker",  # String format
            "description": "We are looking for a senior software engineer...",
            "salary_min": 100000,
            "salary_max": 150000,
            "job_type": "Full-time",
            "company_id": "1",
        }

        job = JobCreate(**hr_portal_data)
        assert job.experience_level == "Senior-level"  # Normalized
        assert isinstance(job.requirements, list)
        assert len(job.requirements) == 4

    def test_client_portal_format(self):
        """Test Client Portal data format validation"""
        client_portal_data = {
            "title": "Software Engineer",
            "description": "Looking for a software engineer",
            "requirements": "Python, JavaScript, React",  # String format
            "location": "New York",
            "department": "Engineering",
            "experience_level": "Mid",  # Client Portal format
            "salary_min": 70000,
            "salary_max": 100000,
            "job_type": "Full-time",
            "company_id": "123",
        }

        job = JobCreate(**client_portal_data)
        assert job.experience_level == "Mid-level"  # Normalized
        assert isinstance(job.requirements, list)
        assert "JavaScript" in job.requirements


class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_maximum_salary_boundary(self):
        """Test maximum salary boundary"""
        job_data = {
            "title": "Executive Position",
            "description": "High-level executive position with competitive compensation",
            "requirements": ["Leadership", "Strategy"],
            "location": "New York",
            "department": "Executive",
            "experience_level": "Executive-level",
            "salary_min": 9000000,
            "salary_max": 10000000,  # Maximum allowed
        }

        job = JobCreate(**job_data)
        assert job.salary_max == 10000000

    def test_salary_exceeds_maximum(self):
        """Test salary exceeding maximum raises validation error"""
        job_data = {
            "title": "Test Job",
            "description": "Test job description",
            "requirements": ["Test"],
            "location": "Test City",
            "department": "Test",
            "experience_level": "Senior-level",
            "salary_min": 5000000,
            "salary_max": 15000000,  # Exceeds maximum
        }

        with pytest.raises(ValidationError):
            JobCreate(**job_data)

    def test_minimum_title_length(self):
        """Test minimum title length validation"""
        job_data = {
            "title": "Job",  # Too short (< 5 characters)
            "description": "Test job description for validation",
            "requirements": ["Test"],
            "location": "Test City",
            "department": "Test",
            "experience_level": "Senior-level",
            "salary_min": 50000,
            "salary_max": 80000,
        }

        with pytest.raises(ValidationError):
            JobCreate(**job_data)

    def test_minimum_description_length(self):
        """Test minimum description length validation"""
        job_data = {
            "title": "Test Job Title",
            "description": "Short",  # Too short (< 20 characters)
            "requirements": ["Test"],
            "location": "Test City",
            "department": "Test",
            "experience_level": "Senior-level",
            "salary_min": 50000,
            "salary_max": 80000,
        }

        with pytest.raises(ValidationError):
            JobCreate(**job_data)


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
