#!/usr/bin/env python3
"""
Quick Validation Test - Test Fixed Endpoints
"""

import requests
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"
AGENT_URL = "http://localhost:9000"
API_KEY = "myverysecureapikey123"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def test_fixed_endpoints():
    """Test the fixed endpoints"""
    print("Testing Fixed Endpoints")
    print("=" * 50)
    
    # Test performance optimized endpoints
    endpoints_to_test = [
        ("GET", f"{BASE_URL}/health/detailed", "Detailed Health (Optimized)"),
        ("GET", f"{BASE_URL}/monitoring/dependencies", "Dependencies (Optimized)"),
        ("GET", f"{BASE_URL}/metrics/dashboard", "Metrics Dashboard (Optimized)"),
        ("GET", f"{BASE_URL}/monitoring/logs/search?query=error", "Log Search (Fixed)"),
        ("POST", f"{BASE_URL}/v1/match/cache-clear", "Cache Clear (Fixed Method)"),
        ("GET", f"{BASE_URL}/v1/reports/summary", "Summary Report (New)"),
        ("POST", f"{BASE_URL}/v1/auth/2fa/setup", {"user_id": "test_user"}, "2FA Setup (New)"),
        ("GET", f"{BASE_URL}/v1/auth/api-keys?user_id=demo_user", "API Keys List (New)"),
    ]
    
    results = []
    
    for test_case in endpoints_to_test:
        if len(test_case) == 3:
            method, url, name = test_case
            data = None
        else:
            method, url, data, name = test_case
        
        try:
            start_time = time.time()
            
            if method == "GET":
                response = requests.get(url, headers=HEADERS, timeout=10)
            elif method == "POST":
                response = requests.post(url, headers=HEADERS, json=data, timeout=10)
            
            response_time = (time.time() - start_time) * 1000
            
            status = "PASS" if response.status_code == 200 else "FAIL"
            print(f"{status} {name}: {response.status_code} ({response_time:.1f}ms)")
            
            results.append({
                "name": name,
                "status_code": response.status_code,
                "response_time": response_time,
                "success": response.status_code == 200
            })
            
        except Exception as e:
            print(f"ERROR {name}: {str(e)}")
            results.append({
                "name": name,
                "error": str(e),
                "success": False
            })
    
    # Summary
    print("\n" + "=" * 50)
    print("VALIDATION SUMMARY")
    print("=" * 50)
    
    total_tests = len(results)
    passed_tests = sum(1 for r in results if r.get("success", False))
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%")
    
    # Performance analysis
    response_times = [r.get("response_time", 0) for r in results if r.get("success", False)]
    if response_times:
        avg_time = sum(response_times) / len(response_times)
        print(f"Average Response Time: {avg_time:.1f}ms")
        
        # Check if performance improved
        slow_endpoints = [r for r in results if r.get("response_time", 0) > 1000]
        if slow_endpoints:
            print(f"Slow Endpoints (>1s): {len(slow_endpoints)}")
            for endpoint in slow_endpoints:
                print(f"  - {endpoint['name']}: {endpoint.get('response_time', 0):.1f}ms")
        else:
            print("All endpoints responding in <1s")

if __name__ == "__main__":
    test_fixed_endpoints()