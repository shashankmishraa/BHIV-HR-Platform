#!/usr/bin/env python3
import requests
import json
import time

# Test configuration
GATEWAY_URL = "https://bhiv-hr-gateway-46pz.onrender.com"
AGENT_URL = "https://bhiv-hr-agent-m1me.onrender.com"
API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def test_endpoint(url, name, method="GET", data=None):
    try:
        start_time = time.time()
        if method == "GET":
            response = requests.get(url, headers=HEADERS, timeout=10)
        else:
            response = requests.post(url, headers=HEADERS, json=data, timeout=10)
        
        response_time = (time.time() - start_time) * 1000
        
        if response.status_code == 200:
            print(f"PASS {name} ({response.status_code}) - {response_time:.0f}ms")
            return True
        else:
            print(f"FAIL {name} ({response.status_code}) - {response_time:.0f}ms")
            return False
    except Exception as e:
        print(f"ERROR {name} - {str(e)}")
        return False

def main():
    print("BHIV HR Platform - Live Endpoint Testing")
    print("=" * 50)
    
    passed = 0
    total = 0
    
    # Test Gateway Core Endpoints
    print("\nGateway Service Tests:")
    endpoints = [
        (f"{GATEWAY_URL}/", "Root"),
        (f"{GATEWAY_URL}/health", "Health"),
        (f"{GATEWAY_URL}/test-candidates", "Test Candidates"),
        (f"{GATEWAY_URL}/v1/jobs", "List Jobs"),
        (f"{GATEWAY_URL}/v1/candidates", "List Candidates"),
        (f"{GATEWAY_URL}/v1/candidates/search", "Search Candidates"),
        (f"{GATEWAY_URL}/v1/match/1/top", "AI Matching"),
        (f"{GATEWAY_URL}/candidates/stats", "Candidate Stats"),
        (f"{GATEWAY_URL}/metrics", "Metrics"),
    ]
    
    for url, name in endpoints:
        if test_endpoint(url, name):
            passed += 1
        total += 1
    
    # Test Agent Service
    print("\nAgent Service Tests:")
    agent_endpoints = [
        (f"{AGENT_URL}/", "Agent Root"),
        (f"{AGENT_URL}/health", "Agent Health"),
        (f"{AGENT_URL}/test-db", "Agent DB Test"),
    ]
    
    for url, name in agent_endpoints:
        if test_endpoint(url, name):
            passed += 1
        total += 1
    
    # Test AI Matching
    print("\nAI Matching Test:")
    match_data = {"job_id": 1}
    if test_endpoint(f"{AGENT_URL}/match", "AI Match", "POST", match_data):
        passed += 1
    total += 1
    
    # Test Job Creation
    print("\nJob Creation Test:")
    job_data = {
        "title": "Test Job",
        "department": "Engineering", 
        "location": "Remote",
        "experience_level": "Mid",
        "requirements": "Python, FastAPI",
        "description": "Test job"
    }
    if test_endpoint(f"{GATEWAY_URL}/v1/jobs", "Create Job", "POST", job_data):
        passed += 1
    total += 1
    
    print(f"\n" + "=" * 50)
    print(f"RESULTS: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed/total >= 0.8:
        print("STATUS: SYSTEM OPERATIONAL")
    else:
        print("STATUS: SYSTEM ISSUES DETECTED")

if __name__ == "__main__":
    main()