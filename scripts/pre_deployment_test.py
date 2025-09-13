#!/usr/bin/env python3
"""
Pre-deployment verification for Render
Tests all critical endpoints before deployment
"""

import requests
import json
from datetime import datetime, timedelta

# Test against local if available, otherwise production
GATEWAY_URL = "https://bhiv-hr-gateway.onrender.com"
API_KEY = "myverysecureapikey123"
headers = {"Authorization": f"Bearer {API_KEY}"}

def test_endpoint(method, url, data=None, expected_status=200):
    """Test endpoint with proper error handling"""
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=10)
        
        success = response.status_code == expected_status
        return {
            "success": success,
            "status": response.status_code,
            "data": response.json() if response.headers.get('content-type', '').startswith('application/json') else None
        }
    except Exception as e:
        return {"success": False, "status": "ERROR", "error": str(e)}

def main():
    print("Pre-Deployment Verification for Render")
    print("=" * 50)
    
    tests = [
        # Core endpoints
        ("GET", f"{GATEWAY_URL}/health", None, 200),
        ("GET", f"{GATEWAY_URL}/", None, 200),
        
        # Job management
        ("GET", f"{GATEWAY_URL}/v1/jobs", None, 200),
        
        # Candidate management  
        ("GET", f"{GATEWAY_URL}/v1/candidates", None, 200),
        ("GET", f"{GATEWAY_URL}/v1/candidates/search?skills=Python", None, 200),
        
        # AI matching
        ("GET", f"{GATEWAY_URL}/v1/match/1/top", None, 200),
        
        # Interview management
        ("GET", f"{GATEWAY_URL}/v1/interviews", None, 200),
        
        # Analytics
        ("GET", f"{GATEWAY_URL}/candidates/stats", None, 200),
        
        # Monitoring
        ("GET", f"{GATEWAY_URL}/metrics", None, 200),
        ("GET", f"{GATEWAY_URL}/health/detailed", None, 200),
    ]
    
    passed = 0
    failed = 0
    
    for method, url, data, expected in tests:
        endpoint_name = url.split('/')[-1] or url.split('/')[-2]
        result = test_endpoint(method, url, data, expected)
        
        if result["success"]:
            print(f"[PASS] {endpoint_name}: {result['status']}")
            passed += 1
        else:
            print(f"[FAIL] {endpoint_name}: {result.get('status', 'ERROR')}")
            if 'error' in result:
                print(f"  Error: {result['error']}")
            failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed")
    
    # Test interview scheduling with corrected payload
    print("\nTesting Interview Scheduling:")
    interview_data = {
        "candidate_id": 1,
        "job_id": 1, 
        "interview_date": (datetime.now() + timedelta(days=1)).isoformat(),
        "interviewer": "Test Interviewer",
        "notes": "Pre-deployment test"
    }
    
    result = test_endpoint("POST", f"{GATEWAY_URL}/v1/interviews", interview_data, 200)
    if result["success"]:
        print("[PASS] Interview Scheduling")
    else:
        print(f"[FAIL] Interview Scheduling: {result.get('status', 'ERROR')}")
    
    # Test client login
    print("\nTesting Client Login:")
    login_data = {"username": "TECH001", "password": "demo123"}
    result = test_endpoint("POST", f"{GATEWAY_URL}/v1/client/login", login_data, 200)
    if result["success"]:
        print("[PASS] Client Login")
    else:
        print(f"[FAIL] Client Login: {result.get('status', 'ERROR')}")
    
    print(f"\nDeployment Readiness: {'READY' if failed == 0 else 'NEEDS FIXES'}")

if __name__ == "__main__":
    main()