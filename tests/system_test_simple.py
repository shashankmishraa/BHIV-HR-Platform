#!/usr/bin/env python3
"""
BHIV HR Platform - Simple System Test
Tests core endpoints to verify system functionality
"""

import requests
import json
import time
from datetime import datetime

# Configuration
GATEWAY_URL = "https://bhiv-hr-gateway-46pz.onrender.com"
AGENT_URL = "https://bhiv-hr-agent-m1me.onrender.com"
API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def test_endpoint(name, method, url, data=None, timeout=30):
    """Test individual endpoint"""
    try:
        if method == "GET":
            response = requests.get(url, headers=HEADERS, timeout=timeout)
        elif method == "POST":
            response = requests.post(url, headers=HEADERS, json=data, timeout=timeout)
        
        if response.status_code in [200, 201]:
            print(f"PASS: {name} ({response.status_code})")
            return True, response.json() if response.content else {}
        else:
            print(f"FAIL: {name} ({response.status_code})")
            return False, response.text
            
    except Exception as e:
        print(f"ERROR: {name} - {str(e)}")
        return False, str(e)

def main():
    """Run system tests"""
    print("BHIV HR Platform - System Test")
    print("=" * 50)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    passed = 0
    total = 0
    
    # Core Gateway Tests
    print("Testing Gateway Service...")
    
    tests = [
        ("Gateway Health", "GET", f"{GATEWAY_URL}/health"),
        ("Gateway Root", "GET", f"{GATEWAY_URL}/"),
        ("Test Candidates", "GET", f"{GATEWAY_URL}/test-candidates"),
        ("List Jobs", "GET", f"{GATEWAY_URL}/v1/jobs"),
        ("Get Candidates", "GET", f"{GATEWAY_URL}/v1/candidates"),
        ("Candidate Stats", "GET", f"{GATEWAY_URL}/candidates/stats"),
        ("AI Matching", "GET", f"{GATEWAY_URL}/v1/match/1/top"),
        ("Security Headers", "GET", f"{GATEWAY_URL}/v1/security/security-headers-test"),
        ("Rate Limit Status", "GET", f"{GATEWAY_URL}/v1/security/rate-limit-status"),
        ("Password Policy", "GET", f"{GATEWAY_URL}/v1/password/policy"),
    ]
    
    for name, method, url in tests:
        total += 1
        success, result = test_endpoint(name, method, url)
        if success:
            passed += 1
    
    print()
    print("Testing AI Agent Service...")
    
    agent_tests = [
        ("Agent Health", "GET", f"{AGENT_URL}/health"),
        ("Agent Root", "GET", f"{AGENT_URL}/"),
        ("Agent DB Test", "GET", f"{AGENT_URL}/test-db"),
    ]
    
    for name, method, url in agent_tests:
        total += 1
        success, result = test_endpoint(name, method, url)
        if success:
            passed += 1
    
    # Test AI Matching
    print()
    print("Testing AI Matching...")
    total += 1
    match_data = {"job_id": 1}
    success, result = test_endpoint("AI Match", "POST", f"{AGENT_URL}/match", match_data)
    if success:
        passed += 1
        if isinstance(result, dict):
            candidates = result.get('top_candidates', [])
            print(f"  Found {len(candidates)} matched candidates")
            if candidates:
                top_score = candidates[0].get('score', 0)
                print(f"  Top candidate score: {top_score}")
    
    # Test Data Integrity
    print()
    print("Testing Data Integrity...")
    total += 1
    success, result = test_endpoint("Database Check", "GET", f"{GATEWAY_URL}/test-candidates")
    if success:
        passed += 1
        if isinstance(result, dict):
            count = result.get('total_candidates', 0)
            print(f"  Total candidates in database: {count}")
    
    # Summary
    print()
    print("=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("STATUS: ALL TESTS PASSED - System is fully operational")
    elif passed >= total * 0.8:
        print("STATUS: MOSTLY WORKING - Minor issues detected")
    else:
        print("STATUS: ISSUES DETECTED - Some services may be down")
    
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()