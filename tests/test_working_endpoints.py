#!/usr/bin/env python3
"""
Test Working Client Portal Endpoints
Tests endpoints that should work without authentication
"""

import requests
import time

BASE_URL = "https://bhiv-hr-gateway-46pz.onrender.com"
API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"

def test_endpoint(endpoint, method="GET", data=None, auth_required=True):
    """Test a single endpoint"""
    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    
    if auth_required:
        headers["Authorization"] = f"Bearer {API_KEY}"
    
    start_time = time.time()
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=15)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=15)
        
        response_time = time.time() - start_time
        
        status = "PASS" if response.status_code == 200 else "FAIL"
        
        result = {
            "endpoint": endpoint,
            "method": method,
            "status_code": response.status_code,
            "response_time": f"{response_time:.3f}s",
            "result": status
        }
        
        if response.status_code == 200:
            try:
                data = response.json()
                if isinstance(data, dict):
                    if "jobs" in data:
                        result["details"] = f"Found {len(data['jobs'])} jobs"
                    elif "candidates" in data:
                        result["details"] = f"Found {len(data['candidates'])} candidates"
                    elif "matches" in data:
                        result["details"] = f"Found {len(data['matches'])} matches"
                    elif "status" in data:
                        result["details"] = f"Status: {data['status']}"
                    else:
                        result["details"] = "Valid JSON response"
                elif isinstance(data, list):
                    result["details"] = f"Array with {len(data)} items"
            except:
                result["details"] = "Non-JSON response"
        else:
            result["details"] = f"HTTP {response.status_code}"
            
        return result
        
    except requests.exceptions.Timeout:
        return {
            "endpoint": endpoint,
            "method": method,
            "status_code": "TIMEOUT",
            "response_time": "15.000s+",
            "result": "FAIL",
            "details": "Request timeout"
        }
    except Exception as e:
        return {
            "endpoint": endpoint,
            "method": method,
            "status_code": "ERROR",
            "response_time": "N/A",
            "result": "FAIL",
            "details": str(e)[:50]
        }

def main():
    """Test all available endpoints"""
    print("Client Portal Endpoint Testing")
    print("=" * 50)
    
    # Test endpoints that don't require authentication
    public_endpoints = [
        ("/", "GET", None, False),
        ("/health", "GET", None, False),
        ("/health/detailed", "GET", None, False),
        ("/metrics", "GET", None, False),
        ("/metrics/dashboard", "GET", None, False)
    ]
    
    # Test endpoints that require API key authentication
    authenticated_endpoints = [
        ("/v1/jobs", "GET", None, True),
        ("/v1/candidates", "GET", None, True),
        ("/v1/candidates/search", "GET", None, True),
        ("/v1/candidates/stats", "GET", None, True),
        ("/v1/match/1/top", "GET", None, True),
        ("/v1/security/rate-limit-status", "GET", None, True),
        ("/test-candidates", "GET", None, True)
    ]
    
    # Test job creation
    job_creation_test = [
        ("/v1/jobs", "POST", {
            "title": "Test Engineer",
            "department": "Engineering", 
            "location": "Remote",
            "experience_level": "Mid-level",
            "requirements": "Python, Testing",
            "description": "Test job posting",
            "employment_type": "Full-time"
        }, True)
    ]
    
    # Test client login (expected to fail with current production code)
    client_login_test = [
        ("/v1/client/login", "POST", {
            "client_id": "TECH001",
            "password": "demo123"
        }, False)
    ]
    
    all_tests = []
    
    print("\\nTesting Public Endpoints...")
    for endpoint, method, data, auth in public_endpoints:
        result = test_endpoint(endpoint, method, data, auth)
        all_tests.append(result)
        print(f"{result['result']} {method} {endpoint} ({result['response_time']}) - {result['details']}")
    
    print("\\nTesting Authenticated Endpoints...")
    for endpoint, method, data, auth in authenticated_endpoints:
        result = test_endpoint(endpoint, method, data, auth)
        all_tests.append(result)
        print(f"{result['result']} {method} {endpoint} ({result['response_time']}) - {result['details']}")
    
    print("\\nTesting Job Creation...")
    for endpoint, method, data, auth in job_creation_test:
        result = test_endpoint(endpoint, method, data, auth)
        all_tests.append(result)
        print(f"{result['result']} {method} {endpoint} ({result['response_time']}) - {result['details']}")
    
    print("\\nTesting Client Login (Known Issue)...")
    for endpoint, method, data, auth in client_login_test:
        result = test_endpoint(endpoint, method, data, auth)
        all_tests.append(result)
        print(f"{result['result']} {method} {endpoint} ({result['response_time']}) - {result['details']}")
    
    # Summary
    passed = sum(1 for test in all_tests if test['result'] == 'PASS')
    failed = sum(1 for test in all_tests if test['result'] == 'FAIL')
    total = len(all_tests)
    
    print("\\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {(passed/total*100):.1f}%")
    
    print("\\nWorking Endpoints:")
    for test in all_tests:
        if test['result'] == 'PASS':
            print(f"  - {test['method']} {test['endpoint']} ({test['response_time']})")
    
    if failed > 0:
        print("\\nFailed Endpoints:")
        for test in all_tests:
            if test['result'] == 'FAIL':
                print(f"  - {test['method']} {test['endpoint']} - {test['details']}")

if __name__ == "__main__":
    main()