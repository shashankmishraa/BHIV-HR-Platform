#!/usr/bin/env python3
"""
Comprehensive Platform Verification Script
Tests all endpoints and portal functionalities
"""

import requests
import json
import time
from datetime import datetime, timedelta
import sys

# Configuration
GATEWAY_URL = "https://bhiv-hr-gateway.onrender.com"
AGENT_URL = "https://bhiv-hr-agent.onrender.com"
HR_PORTAL_URL = "https://bhiv-hr-portal.onrender.com"
CLIENT_PORTAL_URL = "https://bhiv-hr-client-portal.onrender.com"
API_KEY = "myverysecureapikey123"

headers = {"Authorization": f"Bearer {API_KEY}"}

def test_endpoint(method, url, data=None, expected_status=200):
    """Test single endpoint"""
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=30)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=30)
        
        status = "[OK]" if response.status_code == expected_status else "[ERR]"
        return {
            "status": status,
            "code": response.status_code,
            "response": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text[:200]
        }
    except Exception as e:
        return {"status": "[ERR]", "code": "ERROR", "response": str(e)}

def check_portal_health(url, name):
    """Check portal health"""
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            return f"[OK] {name} Portal: Online"
        else:
            return f"[ERR] {name} Portal: Status {response.status_code}"
    except Exception as e:
        return f"[ERR] {name} Portal: {str(e)}"

def main():
    print("BHIV HR Platform - Comprehensive Verification")
    print("=" * 60)
    
    # 1. Service Health Checks
    print("\n1. SERVICE HEALTH CHECKS")
    print("-" * 30)
    
    services = [
        ("Gateway", f"{GATEWAY_URL}/health"),
        ("AI Agent", f"{AGENT_URL}/health"),
        ("HR Portal", HR_PORTAL_URL),
        ("Client Portal", CLIENT_PORTAL_URL)
    ]
    
    for name, url in services:
        if "portal" in name.lower():
            print(check_portal_health(url, name.split()[0]))
        else:
            result = test_endpoint("GET", url)
            print(f"{result['status']} {name}: {result['code']} - {result['response']}")
    
    # 2. Core API Endpoints
    print("\n2. CORE API ENDPOINTS")
    print("-" * 30)
    
    core_endpoints = [
        ("GET", f"{GATEWAY_URL}/", "Root endpoint"),
        ("GET", f"{GATEWAY_URL}/health", "Health check"),
        ("GET", f"{GATEWAY_URL}/test-candidates", "Test candidates")
    ]
    
    for method, url, desc in core_endpoints:
        result = test_endpoint(method, url)
        print(f"{result['status']} {desc}: {result['code']}")
    
    # 3. Job Management
    print("\n3. JOB MANAGEMENT")
    print("-" * 30)
    
    # Get jobs
    result = test_endpoint("GET", f"{GATEWAY_URL}/v1/jobs")
    print(f"{result['status']} Get Jobs: {result['code']}")
    
    # Create job
    job_data = {
        "title": "Test Software Engineer",
        "description": "Test job for verification",
        "requirements": "Python, FastAPI",
        "location": "Remote",
        "salary_range": "80000-120000",
        "experience_required": "3-5 years"
    }
    result = test_endpoint("POST", f"{GATEWAY_URL}/v1/jobs", job_data, 201)
    print(f"{result['status']} Create Job: {result['code']}")
    
    # 4. Candidate Management
    print("\n4. CANDIDATE MANAGEMENT")
    print("-" * 30)
    
    # Get candidates
    result = test_endpoint("GET", f"{GATEWAY_URL}/v1/candidates")
    print(f"{result['status']} Get Candidates: {result['code']}")
    
    # Search candidates
    result = test_endpoint("GET", f"{GATEWAY_URL}/v1/candidates/search?skills=Python")
    print(f"{result['status']} Search Candidates: {result['code']}")
    
    # Bulk upload test
    bulk_data = {
        "candidates": [{
            "name": "Test Candidate",
            "email": f"test_{int(time.time())}@example.com",
            "phone": "555-0123",
            "location": "Test City",
            "experience_years": 3,
            "technical_skills": "Python, JavaScript",
            "seniority_level": "Mid-level",
            "education_level": "Bachelor's"
        }]
    }
    result = test_endpoint("POST", f"{GATEWAY_URL}/v1/candidates/bulk", bulk_data)
    print(f"{result['status']} Bulk Upload: {result['code']}")
    
    # 5. AI Matching Engine
    print("\n5. AI MATCHING ENGINE")
    print("-" * 30)
    
    match_data = {
        "job_id": 1,
        "requirements": "Python developer with 3+ years experience",
        "location": "Remote"
    }
    result = test_endpoint("POST", f"{GATEWAY_URL}/v1/match", match_data)
    print(f"{result['status']} AI Matching: {result['code']}")
    
    # 6. Interview Management
    print("\n6. INTERVIEW MANAGEMENT")
    print("-" * 30)
    
    # Get interviews
    result = test_endpoint("GET", f"{GATEWAY_URL}/v1/interviews")
    print(f"{result['status']} Get Interviews: {result['code']}")
    
    # Schedule interview
    interview_data = {
        "candidate_id": 1,
        "job_id": 1,
        "interview_date": (datetime.now() + timedelta(days=7)).isoformat(),
        "interviewer": "Test Interviewer",
        "notes": "Verification test interview"
    }
    result = test_endpoint("POST", f"{GATEWAY_URL}/v1/interviews", interview_data)
    print(f"{result['status']} Schedule Interview: {result['code']}")
    
    # 7. Analytics & Statistics
    print("\n7. ANALYTICS & STATISTICS")
    print("-" * 30)
    
    result = test_endpoint("GET", f"{GATEWAY_URL}/candidates/stats")
    print(f"{result['status']} Candidate Stats: {result['code']}")
    
    # 8. Security Features
    print("\n8. SECURITY FEATURES")
    print("-" * 30)
    
    # Test without API key
    try:
        response = requests.get(f"{GATEWAY_URL}/v1/jobs", timeout=10)
        status = "[OK]" if response.status_code == 401 else "[ERR]"
        print(f"{status} API Key Protection: {response.status_code}")
    except Exception as e:
        print(f"[ERR] API Key Protection: {str(e)}")
    
    # 9. Portal Functionality Tests
    print("\n9. PORTAL FUNCTIONALITY")
    print("-" * 30)
    
    # Test portal pages
    portal_pages = [
        (HR_PORTAL_URL, "HR Portal Main"),
        (CLIENT_PORTAL_URL, "Client Portal Main")
    ]
    
    for url, name in portal_pages:
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                # Check for key elements
                content = response.text.lower()
                if "streamlit" in content or "bhiv" in content or "hr" in content:
                    print(f"[OK] {name}: Loaded successfully")
                else:
                    print(f"[WARN] {name}: Loaded but content unclear")
            else:
                print(f"[ERR] {name}: Status {response.status_code}")
        except Exception as e:
            print(f"[ERR] {name}: {str(e)}")
    
    # 10. Database Connectivity
    print("\n10. DATABASE CONNECTIVITY")
    print("-" * 30)
    
    # Test database through API
    db_tests = [
        ("GET", f"{GATEWAY_URL}/v1/candidates", "Candidate DB Read"),
        ("GET", f"{GATEWAY_URL}/v1/jobs", "Jobs DB Read"),
        ("GET", f"{GATEWAY_URL}/v1/interviews", "Interviews DB Read")
    ]
    
    for method, url, desc in db_tests:
        result = test_endpoint(method, url)
        print(f"{result['status']} {desc}: {result['code']}")
    
    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    print("[OK] = Working correctly")
    print("[ERR] = Issues detected")
    print("[WARN] = Partial functionality")
    print("\nFor detailed logs, check individual service endpoints.")
    print(f"Verification completed at: {datetime.now().isoformat()}")

if __name__ == "__main__":
    main()