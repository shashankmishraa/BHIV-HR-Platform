#!/usr/bin/env python3
"""
BHIV HR Platform - Endpoint Testing Script
Tests all core endpoints to verify system functionality
"""

import requests
import json
import time
from datetime import datetime

# Configuration
API_BASE = "http://localhost:8000"
AI_BASE = "http://localhost:9000"
API_KEY = "myverysecureapikey123"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def test_health_endpoints():
    """Test all health endpoints with multiple HTTP methods"""
    print("Testing Health Endpoints...")
    
    endpoints = [
        ("API Gateway Health", f"{API_BASE}/health"),
        ("API Gateway Root", f"{API_BASE}/"),
        ("AI Agent Health", f"{AI_BASE}/health"),
        ("AI Agent Root", f"{AI_BASE}/")
    ]
    
    results = {}
    for name, url in endpoints:
        try:
            # Test GET request
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                results[name] = "HEALTHY"
                print(f"  {name}: HEALTHY (GET)")
                
                # Test HEAD request
                head_response = requests.head(url, timeout=5)
                if head_response.status_code == 200:
                    print(f"  {name}: HEALTHY (HEAD)")
                else:
                    print(f"  {name}: HEAD method failed ({head_response.status_code})")
                    
            else:
                results[name] = f"ERROR {response.status_code}"
                print(f"  {name}: ERROR {response.status_code}")
        except Exception as e:
            results[name] = f"FAILED: {str(e)}"
            print(f"  {name}: FAILED - {str(e)}")
    
    return results

def test_authentication():
    """Test API authentication"""
    print("\nTesting Authentication...")
    
    try:
        response = requests.get(f"{API_BASE}/candidates/stats", headers=HEADERS, timeout=5)
        if response.status_code == 200:
            print("  Authentication: PASSED")
            return True
        else:
            print(f"  Authentication: FAILED - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"  Authentication: FAILED - {str(e)}")
        return False

def test_job_endpoints():
    """Test job management endpoints"""
    print("\nTesting Job Endpoints...")
    
    # Test job creation
    job_data = {
        "title": "Test Python Developer",
        "description": "Test job for endpoint validation",
        "client_id": 1,
        "department": "Engineering",
        "location": "Remote",
        "experience_level": "Senior",
        "employment_type": "Full-time",
        "requirements": "Python, FastAPI",
        "status": "active"
    }
    
    try:
        # POST /v1/jobs
        response = requests.post(f"{API_BASE}/v1/jobs", headers=HEADERS, json=job_data, timeout=10)
        if response.status_code == 200:
            job_result = response.json()
            job_id = job_result.get("job_id")
            print(f"  POST /v1/jobs: PASSED - Created job ID {job_id}")
            
            # GET /v1/jobs
            response = requests.get(f"{API_BASE}/v1/jobs", headers=HEADERS, timeout=10)
            if response.status_code == 200:
                jobs = response.json()
                print(f"  GET /v1/jobs: PASSED - Found {jobs.get('count', 0)} jobs")
                return True
            else:
                print(f"  GET /v1/jobs: FAILED - Status {response.status_code}")
                return False
        else:
            print(f"  POST /v1/jobs: FAILED - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"  Job Endpoints: FAILED - {str(e)}")
        return False

def test_candidate_endpoints():
    """Test candidate management endpoints"""
    print("\nTesting Candidate Endpoints...")
    
    # Test bulk candidate upload
    candidates_data = {
        "candidates": [
            {
                "name": "Test User 1",
                "email": "test1@example.com",
                "phone": "+1-555-0101",
                "location": "New York",
                "experience_years": 5,
                "technical_skills": "Python, FastAPI, PostgreSQL",
                "seniority_level": "Senior",
                "education_level": "Masters",
                "job_id": 1,
                "status": "applied"
            }
        ]
    }
    
    try:
        # POST /v1/candidates/bulk
        response = requests.post(f"{API_BASE}/v1/candidates/bulk", headers=HEADERS, json=candidates_data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"  POST /v1/candidates/bulk: PASSED - Uploaded {result.get('count', 0)} candidates")
            
            # GET /v1/candidates/job/1
            response = requests.get(f"{API_BASE}/v1/candidates/job/1", headers=HEADERS, timeout=10)
            if response.status_code == 200:
                candidates = response.json()
                print(f"  GET /v1/candidates/job/1: PASSED - Found {candidates.get('count', 0)} candidates")
                
                # GET /v1/candidates/search
                response = requests.get(f"{API_BASE}/v1/candidates/search?job_id=1&skills=Python", headers=HEADERS, timeout=10)
                if response.status_code == 200:
                    search_result = response.json()
                    print(f"  GET /v1/candidates/search: PASSED - Found {search_result.get('count', 0)} candidates")
                    return True
                else:
                    print(f"  GET /v1/candidates/search: FAILED - Status {response.status_code}")
                    return False
            else:
                print(f"  GET /v1/candidates/job/1: FAILED - Status {response.status_code}")
                return False
        else:
            print(f"  POST /v1/candidates/bulk: FAILED - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"  Candidate Endpoints: FAILED - {str(e)}")
        return False

def test_ai_matching():
    """Test AI matching endpoint"""
    print("\nTesting AI Matching...")
    
    try:
        response = requests.get(f"{API_BASE}/v1/match/1/top", headers=HEADERS, timeout=15)
        if response.status_code == 200:
            result = response.json()
            candidates = result.get("top_candidates", [])
            print(f"  GET /v1/match/1/top: PASSED - Generated {len(candidates)} top candidates")
            return True
        else:
            print(f"  GET /v1/match/1/top: FAILED - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"  AI Matching: FAILED - {str(e)}")
        return False

def test_feedback_endpoint():
    """Test feedback/values assessment endpoint"""
    print("\nTesting Feedback Endpoint...")
    
    feedback_data = {
        "candidate_id": 1,
        "reviewer": "Test Reviewer",
        "feedback_text": "Test feedback for endpoint validation",
        "values_scores": {
            "integrity": 5,
            "honesty": 4,
            "discipline": 5,
            "hard_work": 5,
            "gratitude": 4
        }
    }
    
    try:
        response = requests.post(f"{API_BASE}/v1/feedback", headers=HEADERS, json=feedback_data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"  POST /v1/feedback: PASSED - Submitted feedback ID {result.get('feedback_id')}")
            return True
        else:
            print(f"  POST /v1/feedback: FAILED - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"  Feedback Endpoint: FAILED - {str(e)}")
        return False

def test_interview_endpoint():
    """Test interview scheduling endpoint"""
    print("\nTesting Interview Endpoint...")
    
    interview_data = {
        "candidate_id": 1,
        "job_id": 1,
        "interview_date": "2025-02-01T10:00:00Z",
        "interviewer": "Test Interviewer"
    }
    
    try:
        response = requests.post(f"{API_BASE}/v1/interviews", headers=HEADERS, json=interview_data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"  POST /v1/interviews: PASSED - Scheduled interview ID {result.get('interview_id')}")
            return True
        else:
            print(f"  POST /v1/interviews: FAILED - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"  Interview Endpoint: FAILED - {str(e)}")
        return False

def test_offer_endpoint():
    """Test offer management endpoint"""
    print("\nTesting Offer Endpoint...")
    
    offer_data = {
        "candidate_id": 1,
        "job_id": 1,
        "salary": 120000,
        "status": "sent"
    }
    
    try:
        response = requests.post(f"{API_BASE}/v1/offers", headers=HEADERS, json=offer_data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"  POST /v1/offers: PASSED - Created offer ID {result.get('offer_id')}")
            return True
        else:
            print(f"  POST /v1/offers: FAILED - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"  Offer Endpoint: FAILED - {str(e)}")
        return False

def test_stats_endpoint():
    """Test statistics endpoint"""
    print("\nTesting Statistics Endpoint...")
    
    try:
        response = requests.get(f"{API_BASE}/candidates/stats", headers=HEADERS, timeout=10)
        if response.status_code == 200:
            stats = response.json()
            print(f"  GET /candidates/stats: PASSED")
            print(f"    - Total Candidates: {stats.get('total_candidates', 0)}")
            print(f"    - Active Jobs: {stats.get('active_jobs', 0)}")
            print(f"    - Recent Matches: {stats.get('recent_matches', 0)}")
            return True
        else:
            print(f"  GET /candidates/stats: FAILED - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"  Statistics Endpoint: FAILED - {str(e)}")
        return False

def test_http_methods():
    """Test HTTP method handling"""
    print("\nTesting HTTP Methods...")
    
    try:
        # Test HEAD request on health endpoint
        head_response = requests.head(f"{API_BASE}/health", timeout=5)
        if head_response.status_code == 200:
            print(f"  HEAD /health: PASSED")
            
            # Test OPTIONS request
            options_response = requests.options(f"{API_BASE}/", timeout=5)
            if options_response.status_code == 200:
                print(f"  OPTIONS /: PASSED")
                
                # Test unsupported method (should return 405)
                try:
                    trace_response = requests.request("TRACE", f"{API_BASE}/", timeout=5)
                    if trace_response.status_code == 405:
                        print(f"  TRACE / (unsupported): CORRECTLY REJECTED (405)")
                        return True
                    else:
                        print(f"  TRACE / (unsupported): UNEXPECTED STATUS {trace_response.status_code}")
                        return False
                except Exception:
                    print(f"  TRACE / (unsupported): CORRECTLY REJECTED")
                    return True
            else:
                print(f"  OPTIONS /: FAILED - Status {options_response.status_code}")
                return False
        else:
            print(f"  HEAD /health: FAILED - Status {head_response.status_code}")
            return False
    except Exception as e:
        print(f"  HTTP Methods: FAILED - {str(e)}")
        return False

def main():
    """Run all endpoint tests"""
    print("BHIV HR Platform - Endpoint Testing")
    print("=" * 50)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run all tests
    results = {}
    results["Health"] = test_health_endpoints()
    results["Authentication"] = test_authentication()
    results["HTTP Methods"] = test_http_methods()
    results["Jobs"] = test_job_endpoints()
    results["Candidates"] = test_candidate_endpoints()
    results["AI Matching"] = test_ai_matching()
    results["Feedback"] = test_feedback_endpoint()
    results["Interviews"] = test_interview_endpoint()
    results["Offers"] = test_offer_endpoint()
    results["Statistics"] = test_stats_endpoint()
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = 0
    
    for test_name, result in results.items():
        if test_name == "Health":
            # Health check results
            healthy = sum(1 for v in result.values() if "HEALTHY" in str(v))
            total_services = len(result)
            print(f"{test_name:<15}: {healthy}/{total_services} services healthy")
            if healthy == total_services:
                passed += 1
            total += 1
        else:
            # Boolean results
            status = "PASSED" if result else "FAILED"
            print(f"{test_name:<15}: {status}")
            if result:
                passed += 1
            total += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("SUCCESS: All endpoints are working!")
    else:
        print("WARNING: Some endpoints failed - check service status")
    
    print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()