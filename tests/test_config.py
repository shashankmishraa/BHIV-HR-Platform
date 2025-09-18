#!/usr/bin/env python3
"""
BHIV HR Platform - Test Configuration
Centralized configuration for all testing frameworks
"""

from typing import Dict, Any, List
import os
class TestConfig:
    """Centralized test configuration"""
    
    # Service URLs
    API_BASE = os.getenv("TEST_API_BASE", "http://localhost:8000")
    AI_BASE = os.getenv("TEST_AI_BASE", "http://localhost:9000")
    PORTAL_BASE = os.getenv("TEST_PORTAL_BASE", "http://localhost:8501")
    CLIENT_PORTAL_BASE = os.getenv("TEST_CLIENT_PORTAL_BASE", "http://localhost:8502")
    
    # Authentication
    API_KEY = os.getenv("TEST_API_KEY", "myverysecureapikey123")
    
    # Test timeouts (seconds)
    REQUEST_TIMEOUT = 10
    WORKFLOW_TIMEOUT = 30
    PERFORMANCE_TIMEOUT = 60
    
    # Test data settings
    CLEANUP_ENABLED = True
    USE_REAL_DATA = False  # Set to True to use production-like data
    
    # Performance benchmarks (seconds)
    PERFORMANCE_BENCHMARKS = {
        "job_creation": 2.0,
        "candidate_upload_single": 1.0,
        "candidate_upload_batch_10": 5.0,
        "ai_matching": 10.0,
        "interview_scheduling": 1.0,
        "feedback_submission": 1.0,
        "offer_creation": 1.0,
        "concurrent_request": 0.5,
        "end_to_end_workflow": 30.0
    }
    
    # Test thresholds
    SUCCESS_THRESHOLDS = {
        "workflow_tests": 1.0,  # 100% - All workflows must pass
        "performance_tests": 0.8,  # 80% - Most benchmarks must pass
        "regression_tests": 0.9,  # 90% - Most regression tests must pass
        "overall_success": 0.8  # 80% - Overall success threshold
    }
    
    # Concurrent testing settings
    CONCURRENT_USERS = 5
    REQUESTS_PER_USER = 3
    
    # Test data volumes
    TEST_DATA_VOLUMES = {
        "small": {"jobs": 1, "candidates": 3},
        "medium": {"jobs": 3, "candidates": 10},
        "large": {"jobs": 5, "candidates": 25}
    }
    
    @classmethod
    def get_headers(cls) -> Dict[str, str]:
        """Get standard request headers"""
        return {
            "Authorization": f"Bearer {cls.API_KEY}",
            "Content-Type": "application/json"
        }
    
    @classmethod
    def get_test_volume(cls, size: str = "medium") -> Dict[str, int]:
        """Get test data volume configuration"""
        return cls.TEST_DATA_VOLUMES.get(size, cls.TEST_DATA_VOLUMES["medium"])

class WorkflowTestScenarios:
    """Predefined test scenarios for workflow testing"""
    
    COMPLETE_HIRING_WORKFLOW = {
        "name": "Complete Hiring Workflow",
        "description": "Full hiring process from job creation to offer",
        "steps": [
            "create_job",
            "upload_candidates", 
            "ai_matching",
            "schedule_interview",
            "submit_feedback",
            "create_offer",
            "verify_consistency"
        ],
        "expected_duration": 25.0,
        "critical": True
    }
    
    CLIENT_HR_SYNC = {
        "name": "Client-HR Portal Sync",
        "description": "Cross-portal data synchronization",
        "steps": [
            "client_create_job",
            "verify_hr_visibility",
            "hr_add_candidates",
            "verify_client_visibility"
        ],
        "expected_duration": 10.0,
        "critical": True
    }
    
    AI_MATCHING_WORKFLOW = {
        "name": "AI Matching Workflow", 
        "description": "AI-powered candidate matching and scoring",
        "steps": [
            "create_specialized_job",
            "upload_diverse_candidates",
            "semantic_matching",
            "verify_scoring",
            "individual_analysis"
        ],
        "expected_duration": 15.0,
        "critical": True
    }
    
    ERROR_HANDLING_WORKFLOW = {
        "name": "Error Handling Workflow",
        "description": "System resilience and error recovery",
        "steps": [
            "invalid_job_data",
            "invalid_candidate_data", 
            "nonexistent_resources",
            "authentication_errors"
        ],
        "expected_duration": 5.0,
        "critical": False
    }
    
    @classmethod
    def get_all_scenarios(cls) -> List[Dict[str, Any]]:
        """Get all test scenarios"""
        return [
            cls.COMPLETE_HIRING_WORKFLOW,
            cls.CLIENT_HR_SYNC,
            cls.AI_MATCHING_WORKFLOW,
            cls.ERROR_HANDLING_WORKFLOW
        ]
    
    @classmethod
    def get_critical_scenarios(cls) -> List[Dict[str, Any]]:
        """Get only critical test scenarios"""
        return [scenario for scenario in cls.get_all_scenarios() if scenario.get("critical", False)]

class PerformanceTestProfiles:
    """Performance testing profiles for different scenarios"""
    
    LIGHT_LOAD = {
        "name": "Light Load",
        "concurrent_users": 2,
        "requests_per_user": 2,
        "test_duration": 30,
        "data_volume": "small"
    }
    
    NORMAL_LOAD = {
        "name": "Normal Load", 
        "concurrent_users": 5,
        "requests_per_user": 3,
        "test_duration": 60,
        "data_volume": "medium"
    }
    
    STRESS_LOAD = {
        "name": "Stress Load",
        "concurrent_users": 10,
        "requests_per_user": 5,
        "test_duration": 120,
        "data_volume": "large"
    }
    
    @classmethod
    def get_profile(cls, profile_name: str) -> Dict[str, Any]:
        """Get performance testing profile"""
        profiles = {
            "light": cls.LIGHT_LOAD,
            "normal": cls.NORMAL_LOAD,
            "stress": cls.STRESS_LOAD
        }
        return profiles.get(profile_name, cls.NORMAL_LOAD)

class TestDataTemplates:
    """Templates for generating test data"""
    
    JOB_TEMPLATE = {
        "title": "Test {role} Position {id}",
        "description": "Test job for {role} with {skills} skills",
        "client_id": 1,
        "department": "Engineering",
        "location": "Remote",
        "experience_level": "Mid",
        "employment_type": "Full-time",
        "requirements": "{skills}",
        "status": "active"
    }
    
    CANDIDATE_TEMPLATE = {
        "name": "Test Candidate {id}",
        "email": "test.candidate{id}@testdomain.com",
        "phone": "+1-555-{phone:04d}",
        "location": "Remote",
        "experience_years": 3,
        "technical_skills": "{skills}",
        "seniority_level": "Mid-level",
        "education_level": "Bachelors",
        "job_id": 1,
        "status": "applied"
    }
    
    INTERVIEW_TEMPLATE = {
        "candidate_id": 1,
        "job_id": 1,
        "interview_date": "2025-02-15T10:00:00Z",
        "interviewer": "Test Interviewer {id}",
        "interview_type": "technical",
        "notes": "Test interview {id}"
    }
    
    FEEDBACK_TEMPLATE = {
        "candidate_id": 1,
        "reviewer": "Test Reviewer {id}",
        "feedback_text": "Test feedback for candidate assessment",
        "values_scores": {
            "integrity": 5,
            "honesty": 4,
            "discipline": 5,
            "hard_work": 5,
            "gratitude": 4
        },
        "technical_rating": 4.0,
        "cultural_fit_rating": 4.5,
        "recommendation": "hire"
    }
    
    OFFER_TEMPLATE = {
        "candidate_id": 1,
        "job_id": 1,
        "salary": 100000,
        "currency": "USD",
        "benefits": "Health insurance, 401k, PTO",
        "start_date": "2025-03-01T09:00:00Z",
        "status": "sent",
        "notes": "Test offer {id}"
    }

class TestEnvironments:
    """Test environment configurations"""
    
    LOCAL = {
        "name": "Local Development",
        "api_base": "http://localhost:8000",
        "ai_base": "http://localhost:9000",
        "portal_base": "http://localhost:8501",
        "client_portal_base": "http://localhost:8502",
        "database_cleanup": True,
        "performance_mode": False
    }
    
    STAGING = {
        "name": "Staging Environment",
        "api_base": "https://staging-api.bhiv-hr.com",
        "ai_base": "https://staging-ai.bhiv-hr.com", 
        "portal_base": "https://staging-portal.bhiv-hr.com",
        "client_portal_base": "https://staging-client.bhiv-hr.com",
        "database_cleanup": False,
        "performance_mode": True
    }
    
    PRODUCTION = {
        "name": "Production Environment",
        "api_base": "https://bhiv-hr-gateway.onrender.com",
        "ai_base": "https://bhiv-hr-agent.onrender.com",
        "portal_base": "https://bhiv-hr-portal.onrender.com",
        "client_portal_base": "https://bhiv-hr-client-portal.onrender.com",
        "database_cleanup": False,
        "performance_mode": True
    }
    
    @classmethod
    def get_environment(cls, env_name: str) -> Dict[str, Any]:
        """Get environment configuration"""
        environments = {
            "local": cls.LOCAL,
            "staging": cls.STAGING,
            "production": cls.PRODUCTION
        }
        return environments.get(env_name, cls.LOCAL)

# Global test configuration instance
test_config = TestConfig()