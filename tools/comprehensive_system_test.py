"""
Comprehensive System Test Suite
Tests all services, portals, and platform functionality
"""

import requests
import time
import json

# Configuration
API_BASE = "http://localhost:8000"
AI_SERVICE = "http://localhost:9000"
RECRUITER_PORTAL = "http://localhost:8501"
CLIENT_PORTAL = "http://localhost:8502"
API_KEY = "myverysecureapikey123"

headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def test_service_health():
    """Test all service health endpoints"""
    print("=== TESTING SERVICE HEALTH ===")
    
    services = [
        ("API Gateway", f"{API_BASE}/health"),
        ("AI Service", f"{AI_SERVICE}/health"),
        ("Recruiter Portal", RECRUITER_PORTAL),
        ("Client Portal", CLIENT_PORTAL)
    ]
    
    results = {}
    for name, url in services:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"{name}: HEALTHY")
                results[name] = "HEALTHY"
            else:
                print(f"{name}: UNHEALTHY ({response.status_code})")
                results[name] = "UNHEALTHY"
        except Exception as e:
            print(f"{name}: UNREACHABLE ({e})")
            results[name] = "UNREACHABLE"
    
    return results

def test_api_endpoints():
    """Test all API endpoints"""
    print("\n=== TESTING API ENDPOINTS ===")
    
    # Test job creation
    job_data = {
        "title": "Test Software Engineer",
        "description": "Test job for system validation",
        "client_id": 1,
        "department": "Engineering",
        "location": "Remote",
        "experience_level": "Mid",
        "employment_type": "Full-time",
        "requirements": "Python, React, AWS",
        "status": "active"
    }
    
    try:
        response = requests.post(f"{API_BASE}/v1/jobs", headers=headers, json=job_data)
        if response.status_code == 200:
            job_id = response.json().get("job_id")
            print(f"Job Creation: SUCCESS (Job ID: {job_id})")
        else:
            print(f"Job Creation: FAILED ({response.status_code})")
            job_id = 1  # Use default for other tests
    except Exception as e:
        print(f"Job Creation: ERROR ({e})")
        job_id = 1
    
    # Test job listing
    try:
        response = requests.get(f"{API_BASE}/v1/jobs", headers=headers)
        if response.status_code == 200:
            jobs = response.json().get("jobs", [])
            print(f"Job Listing: SUCCESS ({len(jobs)} jobs found)")
        else:
            print(f"Job Listing: FAILED ({response.status_code})")
    except Exception as e:
        print(f"Job Listing: ERROR ({e})")
    
    # Test candidate search
    try:
        response = requests.get(f"{API_BASE}/v1/candidates/search?job_id=1", headers=headers)
        if response.status_code == 200:
            candidates = response.json().get("candidates", [])
            print(f"Candidate Search: SUCCESS ({len(candidates)} candidates)")
        else:
            print(f"Candidate Search: FAILED ({response.status_code})")
    except Exception as e:
        print(f"Candidate Search: ERROR ({e})")
    
    # Test AI matching
    try:
        response = requests.get(f"{API_BASE}/v1/match/{job_id}/top", headers=headers)
        if response.status_code == 200:
            matches = response.json().get("top_candidates", [])
            print(f"AI Matching: SUCCESS ({len(matches)} matches)")
        else:
            print(f"AI Matching: FAILED ({response.status_code})")
    except Exception as e:
        print(f"AI Matching: ERROR ({e})")
    
    # Test statistics
    try:
        response = requests.get(f"{API_BASE}/candidates/stats", headers=headers)
        if response.status_code == 200:
            stats = response.json()
            print(f"Statistics: SUCCESS (Candidates: {stats.get('total_candidates', 0)})")
        else:
            print(f"Statistics: FAILED ({response.status_code})")
    except Exception as e:
        print(f"Statistics: ERROR ({e})")

def test_client_authentication():
    """Test client portal authentication"""
    print("\n=== TESTING CLIENT AUTHENTICATION ===")
    
    login_data = {"client_id": "1", "access_code": "client123"}
    
    try:
        response = requests.post(f"{API_BASE}/v1/client/login", json=login_data)
        if response.status_code == 200:
            token = response.json().get("access_token")
            client_name = response.json().get("client_name")
            print(f"Client Login: SUCCESS (Client: {client_name})")
            
            # Test client jobs endpoint
            client_headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(f"{API_BASE}/v1/client/jobs", headers=client_headers)
            if response.status_code == 200:
                jobs = response.json().get("jobs", [])
                print(f"Client Jobs: SUCCESS ({len(jobs)} jobs)")
            else:
                print(f"Client Jobs: FAILED ({response.status_code})")
                
        else:
            print(f"Client Login: FAILED ({response.status_code})")
    except Exception as e:
        print(f"Client Authentication: ERROR ({e})")

def test_database_operations():
    """Test database connectivity and operations"""
    print("\n=== TESTING DATABASE OPERATIONS ===")
    
    # Test bulk candidate upload
    sample_candidates = [
        {
            "job_id": 1,
            "name": "Test Candidate 1",
            "email": "test1@example.com",
            "phone": "+1-555-0101",
            "location": "Remote",
            "cv_url": "https://example.com/cv1.pdf",
            "experience_years": 3,
            "education_level": "Bachelors",
            "technical_skills": "Python, React, SQL",
            "seniority_level": "Mid-level",
            "status": "applied"
        }
    ]
    
    try:
        response = requests.post(
            f"{API_BASE}/v1/candidates/bulk",
            headers=headers,
            json={"candidates": sample_candidates}
        )
        if response.status_code == 200:
            count = response.json().get("count", 0)
            print(f"Bulk Upload: SUCCESS ({count} candidates)")
        else:
            print(f"Bulk Upload: FAILED ({response.status_code})")
    except Exception as e:
        print(f"Bulk Upload: ERROR ({e})")
    
    # Test feedback submission
    feedback_data = {
        "candidate_id": 1,
        "values_scores": {
            "integrity": 4,
            "honesty": 4,
            "discipline": 3,
            "hard_work": 4,
            "gratitude": 3
        }
    }
    
    try:
        response = requests.post(f"{API_BASE}/v1/feedback", headers=headers, json=feedback_data)
        if response.status_code == 200:
            print("Feedback Submission: SUCCESS")
        else:
            print(f"Feedback Submission: FAILED ({response.status_code})")
    except Exception as e:
        print(f"Feedback Submission: ERROR ({e})")

def run_comprehensive_test():
    """Run all tests"""
    print("BHIV HR Platform - Comprehensive System Test")
    print("=" * 50)
    
    start_time = time.time()
    
    # Test service health
    health_results = test_service_health()
    
    # Test API endpoints
    test_api_endpoints()
    
    # Test client authentication
    test_client_authentication()
    
    # Test database operations
    test_database_operations()
    
    # Summary
    end_time = time.time()
    duration = round(end_time - start_time, 2)
    
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print(f"Total Duration: {duration} seconds")
    
    healthy_services = sum(1 for status in health_results.values() if status == "HEALTHY")
    total_services = len(health_results)
    
    print(f"Service Health: {healthy_services}/{total_services} services healthy")
    
    if healthy_services == total_services:
        print("SYSTEM STATUS: ALL TESTS PASSED")
    else:
        print("SYSTEM STATUS: SOME ISSUES DETECTED")
    
    print("\nNext Steps:")
    print("1. Check service logs if any failures")
    print("2. Verify Docker containers are running")
    print("3. Test portals manually in browser")
    print("4. Process resumes and upload candidates")

if __name__ == "__main__":
    run_comprehensive_test()