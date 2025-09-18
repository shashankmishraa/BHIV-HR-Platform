#!/usr/bin/env python3
"""
Quick validation test for all fixes applied
Tests database health check, authentication endpoints, and system functionality
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "https://bhiv-hr-gateway.onrender.com"
API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def test_endpoint(method, endpoint, expected_status=200, data=None):
    """Test a single endpoint"""
    url = f"{BASE_URL}{endpoint}"
    try:
        start_time = time.time()
        
        if method.upper() == "GET":
            response = requests.get(url, headers=HEADERS, timeout=30)
        elif method.upper() == "POST":
            response = requests.post(url, headers=HEADERS, json=data, timeout=30)
        else:
            return {"status": "SKIP", "reason": f"Method {method} not supported in test"}
        
        response_time = (time.time() - start_time) * 1000
        
        if response.status_code == expected_status:
            return {
                "status": "PASS",
                "response_time_ms": round(response_time, 2),
                "status_code": response.status_code
            }
        else:
            return {
                "status": "FAIL",
                "response_time_ms": round(response_time, 2),
                "status_code": response.status_code,
                "expected": expected_status,
                "response": response.text[:200]
            }
    except Exception as e:
        return {
            "status": "ERROR",
            "error": str(e)
        }

def main():
    print("BHIV HR Platform - Fixes Validation Test")
    print("=" * 60)
    print(f"Testing fixes applied on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Base URL: {BASE_URL}")
    print()

    # Test cases for all fixes
    test_cases = [
        # 1. Database Health Check Fix
        ("GET", "/health/detailed", 200, "Database Health Check Fix"),
        
        # 2. Authentication Endpoints Fix
        ("GET", "/v1/auth/status", 200, "Authentication Status Endpoint"),
        ("GET", "/v1/auth/user/info", 200, "User Info Endpoint"),
        ("GET", "/v1/auth/users", 200, "Users List Endpoint"),
        ("GET", "/v1/auth/sessions", 200, "Sessions List Endpoint"),
        ("GET", "/v1/auth/system/health", 200, "Auth System Health"),
        ("GET", "/v1/auth/permissions", 200, "Permissions Endpoint"),
        ("GET", "/v1/auth/metrics", 200, "Auth Metrics Endpoint"),
        ("GET", "/v1/auth/config", 200, "Auth Configuration"),
        ("GET", "/v1/auth/test", 200, "Auth System Test"),
        
        # 3. Core System Endpoints
        ("GET", "/health", 200, "Basic Health Check"),
        ("GET", "/", 200, "Root Endpoint"),
        ("GET", "/v1/jobs", 200, "Jobs Endpoint"),
        ("GET", "/v1/candidates", 200, "Candidates Endpoint"),
        
        # 4. Performance Optimized Endpoints
        ("GET", "/metrics", 200, "Metrics Endpoint"),
        ("GET", "/monitoring/dependencies", 200, "Dependencies Check"),
        ("GET", "/health/simple", 200, "Simple Health Check"),
        
        # 5. Security Endpoints
        ("GET", "/v1/security/status", 200, "Security Status"),
        ("GET", "/v1/security/headers", 200, "Security Headers"),
        
        # 6. AI Matching Endpoints
        ("GET", "/v1/match/1/top", 200, "AI Matching Endpoint"),
        ("GET", "/v1/match/cache-status", 200, "Cache Status"),
    ]

    results = []
    passed = 0
    failed = 0
    errors = 0

    print("Running validation tests...")
    print()

    for method, endpoint, expected_status, description in test_cases:
        print(f"Testing: {description}")
        print(f"  {method} {endpoint}")
        
        result = test_endpoint(method, endpoint, expected_status)
        result["endpoint"] = endpoint
        result["description"] = description
        result["method"] = method
        results.append(result)
        
        if result["status"] == "PASS":
            print(f"  PASS ({result['response_time_ms']}ms)")
            passed += 1
        elif result["status"] == "FAIL":
            print(f"  FAIL (Status: {result['status_code']}, Expected: {expected_status})")
            failed += 1
        else:
            print(f"  ERROR ({result.get('error', 'Unknown error')})")
            errors += 1
        print()

    # Summary
    print("=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    print(f"Total Tests: {len(test_cases)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Errors: {errors}")
    print(f"Success Rate: {(passed / len(test_cases)) * 100:.1f}%")
    print()

    # Detailed results for failures
    if failed > 0 or errors > 0:
        print("DETAILED FAILURE ANALYSIS")
        print("-" * 40)
        for result in results:
            if result["status"] in ["FAIL", "ERROR"]:
                print(f"FAIL: {result['description']}")
                print(f"   Endpoint: {result['method']} {result['endpoint']}")
                if result["status"] == "FAIL":
                    print(f"   Status Code: {result['status_code']} (Expected: {result.get('expected', 'N/A')})")
                    if "response" in result:
                        print(f"   Response: {result['response']}")
                else:
                    print(f"   Error: {result.get('error', 'Unknown error')}")
                print()

    # Fix verification
    print("FIX VERIFICATION STATUS")
    print("-" * 40)
    
    # Check specific fixes
    fix_status = {
        "Database Health Check": any(r["endpoint"] == "/health/detailed" and r["status"] == "PASS" for r in results),
        "Authentication Endpoints": any(r["endpoint"] == "/v1/auth/status" and r["status"] == "PASS" for r in results),
        "Performance Optimization": any(r["endpoint"] == "/monitoring/dependencies" and r["status"] == "PASS" for r in results),
        "Core API Functionality": any(r["endpoint"] == "/v1/jobs" and r["status"] == "PASS" for r in results),
    }
    
    for fix_name, is_working in fix_status.items():
        status_icon = "PASS" if is_working else "FAIL"
        print(f"{status_icon} {fix_name}: {'WORKING' if is_working else 'NEEDS ATTENTION'}")
    
    print()
    print("=" * 60)
    
    if passed == len(test_cases):
        print("ALL FIXES VALIDATED SUCCESSFULLY!")
        print("System is ready for production use")
    elif passed >= len(test_cases) * 0.8:  # 80% success rate
        print("MOST FIXES VALIDATED SUCCESSFULLY!")
        print("Minor issues detected - system operational")
    else:
        print("SOME FIXES NEED ATTENTION")
        print("Review failed tests and apply additional fixes")
    
    print(f"Validation completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return passed == len(test_cases)

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)