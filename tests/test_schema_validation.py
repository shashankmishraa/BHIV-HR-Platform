#!/usr/bin/env python3
"""
SCHEMA VALIDATION AND COMPREHENSIVE TESTING
BHIV HR Platform - Validate all data models and API schemas
"""

import requests
import json
import time
from datetime import datetime
import sys

# Configuration
BASE_URL = "http://localhost:8000"
AGENT_URL = "http://localhost:9000"
API_KEY = "myverysecureapikey123"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}


def log(message, level="INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {level}: {message}")


def test_job_creation_with_correct_schema():
    """Test job creation with correct schema"""
    log("TESTING JOB CREATION WITH CORRECT SCHEMA")

    # Correct job data based on JobCreate model
    job_data = {
        "title": "Senior Python Developer",
        "department": "Engineering",
        "location": "Remote",
        "experience_level": "Senior",
        "requirements": "Python, Django, PostgreSQL, 5+ years experience",
        "description": "We are looking for an experienced Python developer to join our team",
        "client_id": 1,
        "employment_type": "Full-time",
    }

    try:
        response = requests.post(
            f"{BASE_URL}/v1/jobs", headers=HEADERS, json=job_data, timeout=10
        )
        log(f"Job Creation Response: {response.status_code}")
        if response.status_code == 200:
            log("✅ Job creation successful with correct schema")
            log(f"Response: {response.json()}")
        else:
            log(f"❌ Job creation failed: {response.text}")
    except Exception as e:
        log(f"❌ Job creation error: {str(e)}")


def test_candidate_bulk_upload_with_correct_schema():
    """Test candidate bulk upload with correct schema"""
    log("TESTING CANDIDATE BULK UPLOAD WITH CORRECT SCHEMA")

    # Correct bulk upload data based on CandidateBulk model
    bulk_data = {
        "candidates": [
            {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "+1-555-0123",
                "location": "New York, NY",
                "experience_years": 5,
                "technical_skills": "Python, Django, PostgreSQL, AWS",
                "seniority_level": "Senior Developer",
                "education_level": "Bachelor's in Computer Science",
                "resume_path": "/resumes/john_doe.pdf",
                "status": "active",
            },
            {
                "name": "Jane Smith",
                "email": "jane.smith@example.com",
                "phone": "+1-555-0124",
                "location": "San Francisco, CA",
                "experience_years": 3,
                "technical_skills": "JavaScript, React, Node.js, MongoDB",
                "seniority_level": "Mid-level Developer",
                "education_level": "Master's in Software Engineering",
                "resume_path": "/resumes/jane_smith.pdf",
                "status": "active",
            },
        ]
    }

    try:
        response = requests.post(
            f"{BASE_URL}/v1/candidates/bulk",
            headers=HEADERS,
            json=bulk_data,
            timeout=10,
        )
        log(f"Bulk Upload Response: {response.status_code}")
        if response.status_code == 200:
            log("✅ Bulk upload successful with correct schema")
            log(f"Response: {response.json()}")
        else:
            log(f"❌ Bulk upload failed: {response.text}")
    except Exception as e:
        log(f"❌ Bulk upload error: {str(e)}")


def test_interview_scheduling_with_correct_schema():
    """Test interview scheduling with correct schema"""
    log("TESTING INTERVIEW SCHEDULING WITH CORRECT SCHEMA")

    # Correct interview data based on InterviewSchedule model
    interview_data = {
        "candidate_id": 1,
        "job_id": 1,
        "interview_date": "2025-02-01T10:00:00Z",
        "interviewer": "John Manager",
        "notes": "Technical interview for Python developer position",
    }

    try:
        response = requests.post(
            f"{BASE_URL}/v1/interviews",
            headers=HEADERS,
            json=interview_data,
            timeout=10,
        )
        log(f"Interview Scheduling Response: {response.status_code}")
        if response.status_code == 200:
            log("✅ Interview scheduling successful with correct schema")
            log(f"Response: {response.json()}")
        else:
            log(f"❌ Interview scheduling failed: {response.text}")
    except Exception as e:
        log(f"❌ Interview scheduling error: {str(e)}")


def test_security_endpoints_with_correct_data():
    """Test security endpoints with correct data formats"""
    log("TESTING SECURITY ENDPOINTS WITH CORRECT DATA")

    # Test XSS protection
    xss_data = {"input_data": "<script>alert('xss test')</script>"}
    try:
        response = requests.post(
            f"{BASE_URL}/v1/security/test-xss",
            headers=HEADERS,
            json=xss_data,
            timeout=10,
        )
        log(f"XSS Test Response: {response.status_code}")
        if response.status_code == 200:
            log("✅ XSS test successful")
        else:
            log(f"❌ XSS test failed: {response.text}")
    except Exception as e:
        log(f"❌ XSS test error: {str(e)}")

    # Test SQL injection protection
    sql_data = {"input_data": "'; DROP TABLE users; --"}
    try:
        response = requests.post(
            f"{BASE_URL}/v1/security/test-sql-injection",
            headers=HEADERS,
            json=sql_data,
            timeout=10,
        )
        log(f"SQL Injection Test Response: {response.status_code}")
        if response.status_code == 200:
            log("✅ SQL injection test successful")
        else:
            log(f"❌ SQL injection test failed: {response.text}")
    except Exception as e:
        log(f"❌ SQL injection test error: {str(e)}")


def test_password_management_endpoints():
    """Test password management endpoints"""
    log("TESTING PASSWORD MANAGEMENT ENDPOINTS")

    # Test password validation
    password_data = {"password": "TestPassword123!"}
    try:
        response = requests.post(
            f"{BASE_URL}/v1/password/validate",
            headers=HEADERS,
            json=password_data,
            timeout=10,
        )
        log(f"Password Validation Response: {response.status_code}")
        if response.status_code == 200:
            log("✅ Password validation successful")
            result = response.json()
            log(
                f"Password strength: {result.get('password_strength')}, Score: {result.get('score')}"
            )
        else:
            log(f"❌ Password validation failed: {response.text}")
    except Exception as e:
        log(f"❌ Password validation error: {str(e)}")

    # Test password reset
    email_data = {"email": "test@example.com"}
    try:
        response = requests.post(
            f"{BASE_URL}/v1/password/reset",
            headers=HEADERS,
            json=email_data,
            timeout=10,
        )
        log(f"Password Reset Response: {response.status_code}")
        if response.status_code == 200:
            log("✅ Password reset successful")
        else:
            log(f"❌ Password reset failed: {response.text}")
    except Exception as e:
        log(f"❌ Password reset error: {str(e)}")


def test_csp_management_endpoints():
    """Test CSP management endpoints"""
    log("TESTING CSP MANAGEMENT ENDPOINTS")

    # Test CSP report
    csp_report_data = {
        "violated_directive": "script-src",
        "blocked_uri": "https://malicious-site.com/script.js",
        "document_uri": "https://bhiv-platform.com/dashboard",
    }
    try:
        response = requests.post(
            f"{BASE_URL}/v1/csp/report",
            headers=HEADERS,
            json=csp_report_data,
            timeout=10,
        )
        log(f"CSP Report Response: {response.status_code}")
        if response.status_code == 200:
            log("✅ CSP report successful")
        else:
            log(f"❌ CSP report failed: {response.text}")
    except Exception as e:
        log(f"❌ CSP report error: {str(e)}")

    # Test CSP policy update
    csp_policy_data = {
        "policy": "default-src 'self'; script-src 'self' 'unsafe-inline'"
    }
    try:
        response = requests.put(
            f"{BASE_URL}/v1/csp/policy",
            headers=HEADERS,
            json=csp_policy_data,
            timeout=10,
        )
        log(f"CSP Policy Update Response: {response.status_code}")
        if response.status_code == 200:
            log("✅ CSP policy update successful")
        else:
            log(f"❌ CSP policy update failed: {response.text}")
    except Exception as e:
        log(f"❌ CSP policy update error: {str(e)}")


def test_session_management_endpoints():
    """Test session management endpoints"""
    log("TESTING SESSION MANAGEMENT ENDPOINTS")

    # Test session creation
    login_data = {"client_id": "TECH001", "password": "demo123"}
    try:
        response = requests.post(
            f"{BASE_URL}/v1/sessions/create",
            headers=HEADERS,
            json=login_data,
            timeout=10,
        )
        log(f"Session Creation Response: {response.status_code}")
        if response.status_code == 200:
            log("✅ Session creation successful")
        else:
            log(f"❌ Session creation failed: {response.text}")
    except Exception as e:
        log(f"❌ Session creation error: {str(e)}")

    # Test session logout
    logout_data = {"session_id": "test_session_123"}
    try:
        response = requests.post(
            f"{BASE_URL}/v1/sessions/logout",
            headers=HEADERS,
            json=logout_data,
            timeout=10,
        )
        log(f"Session Logout Response: {response.status_code}")
        if response.status_code == 200:
            log("✅ Session logout successful")
        else:
            log(f"❌ Session logout failed: {response.text}")
    except Exception as e:
        log(f"❌ Session logout error: {str(e)}")


def test_client_portal_login():
    """Test client portal login"""
    log("TESTING CLIENT PORTAL LOGIN")

    client_login_data = {"client_id": "TECH001", "password": "demo123"}
    try:
        response = requests.post(
            f"{BASE_URL}/v1/client/login",
            headers=HEADERS,
            json=client_login_data,
            timeout=10,
        )
        log(f"Client Login Response: {response.status_code}")
        if response.status_code == 200:
            log("✅ Client login successful")
            result = response.json()
            log(f"Access token: {result.get('access_token', 'N/A')[:20]}...")
        else:
            log(f"❌ Client login failed: {response.text}")
    except Exception as e:
        log(f"❌ Client login error: {str(e)}")


def test_monitoring_endpoints_with_parameters():
    """Test monitoring endpoints with parameters"""
    log("TESTING MONITORING ENDPOINTS WITH PARAMETERS")

    # Test log search with query parameter
    try:
        response = requests.get(
            f"{BASE_URL}/monitoring/logs/search?query=error&hours=24",
            headers=HEADERS,
            timeout=10,
        )
        log(f"Log Search Response: {response.status_code}")
        if response.status_code == 200:
            log("✅ Log search successful")
        else:
            log(f"❌ Log search failed: {response.text}")
    except Exception as e:
        log(f"❌ Log search error: {str(e)}")


def test_ai_matching_with_different_parameters():
    """Test AI matching with different parameters"""
    log("TESTING AI MATCHING WITH DIFFERENT PARAMETERS")

    # Test with different job IDs and limits
    test_cases = [(1, 5), (2, 10), (1, 15)]

    for job_id, limit in test_cases:
        try:
            response = requests.get(
                f"{BASE_URL}/v1/match/{job_id}/top?limit={limit}",
                headers=HEADERS,
                timeout=15,
            )
            log(
                f"AI Matching (Job {job_id}, Limit {limit}) Response: {response.status_code}"
            )
            if response.status_code == 200:
                result = response.json()
                log(
                    f"✅ AI matching successful - {len(result.get('matches', []))} matches found"
                )
                log(f"Processing time: {result.get('processing_time', 'N/A')}")
                log(f"Algorithm version: {result.get('algorithm_version', 'N/A')}")
            else:
                log(f"❌ AI matching failed: {response.text}")
        except Exception as e:
            log(f"❌ AI matching error: {str(e)}")


def test_candidate_search_with_filters():
    """Test candidate search with various filters"""
    log("TESTING CANDIDATE SEARCH WITH FILTERS")

    # Test different search combinations
    search_params = [
        {"skills": "python"},
        {"location": "remote"},
        {"experience_min": 3},
        {"skills": "javascript", "location": "new york"},
        {"skills": "python", "experience_min": 5},
    ]

    for params in search_params:
        try:
            response = requests.get(
                f"{BASE_URL}/v1/candidates/search",
                headers=HEADERS,
                params=params,
                timeout=10,
            )
            log(f"Candidate Search Response ({params}): {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                log(f"✅ Search successful - {result.get('count', 0)} candidates found")
            else:
                log(f"❌ Search failed: {response.text}")
        except Exception as e:
            log(f"❌ Search error: {str(e)}")


def run_comprehensive_schema_validation():
    """Run all schema validation tests"""
    log("=" * 60)
    log("STARTING COMPREHENSIVE SCHEMA VALIDATION")
    log("=" * 60)

    start_time = time.time()

    # Test all endpoints with correct schemas
    test_job_creation_with_correct_schema()
    test_candidate_bulk_upload_with_correct_schema()
    test_interview_scheduling_with_correct_schema()
    test_security_endpoints_with_correct_data()
    test_password_management_endpoints()
    test_csp_management_endpoints()
    test_session_management_endpoints()
    test_client_portal_login()
    test_monitoring_endpoints_with_parameters()
    test_ai_matching_with_different_parameters()
    test_candidate_search_with_filters()

    total_time = time.time() - start_time

    log("=" * 60)
    log("SCHEMA VALIDATION COMPLETE")
    log("=" * 60)
    log(f"Total Validation Time: {total_time:.1f} seconds")
    log("All schema validations completed. Check results above.")


if __name__ == "__main__":
    run_comprehensive_schema_validation()
