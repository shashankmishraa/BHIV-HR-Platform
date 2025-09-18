#!/usr/bin/env python3
"""
BHIV HR Platform - Endpoint Fixes Verification Test
Tests all 20 previously broken endpoints to verify they are now working
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "https://bhiv-hr-gateway.onrender.com"
AGENT_URL = "https://bhiv-hr-agent.onrender.com"
API_KEY = "myverysecureapikey123"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def test_endpoint(method, url, data=None, expected_status=200, description=""):
    """Test an endpoint and return result"""
    try:
        if method == "GET":
            response = requests.get(url, headers=HEADERS, timeout=10)
        elif method == "POST":
            response = requests.post(url, headers=HEADERS, json=data, timeout=10)
        elif method == "PUT":
            response = requests.put(url, headers=HEADERS, json=data, timeout=10)
        elif method == "DELETE":
            response = requests.delete(url, headers=HEADERS, timeout=10)
        
        success = response.status_code == expected_status
        return {
            "success": success,
            "status_code": response.status_code,
            "description": description,
            "response_size": len(response.text),
            "has_json": response.headers.get('content-type', '').startswith('application/json')
        }
    except Exception as e:
        return {
            "success": False,
            "status_code": 0,
            "description": description,
            "error": str(e),
            "response_size": 0,
            "has_json": False
        }

def main():
    print("BHIV HR Platform - Endpoint Fixes Verification")
    print("=" * 60)
    print(f"Testing Time: {datetime.now().isoformat()}")
    print(f"Gateway URL: {BASE_URL}")
    print(f"Agent URL: {AGENT_URL}")
    print()

    # Test all 20 previously broken endpoints
    tests = [
        # 1. Database Schema Issue (CRITICAL)
        ("POST", f"{BASE_URL}/v1/interviews", {
            "candidate_id": 1,
            "job_id": 1,
            "interview_date": "2025-01-20T10:00:00Z",
            "interviewer": "John Smith",
            "notes": "Technical interview"
        }, 200, "1. Interview Scheduling (Database Schema Fix)"),
        
        # 2. Session Validation Failure (HIGH PRIORITY)
        ("GET", f"{BASE_URL}/v1/sessions/validate", None, 200, "2. Session Validation (Fixed Error Handling)"),
        
        # 3-9. Security Endpoints Missing (7 endpoints)
        ("GET", f"{BASE_URL}/v1/security/headers", None, 200, "3. Security Headers Endpoint"),
        ("POST", f"{BASE_URL}/v1/security/test-xss", {"input_data": "<script>alert('test')</script>"}, 200, "4. XSS Protection Testing"),
        ("POST", f"{BASE_URL}/v1/security/test-sql-injection", {"input_data": "'; DROP TABLE users; --"}, 200, "5. SQL Injection Testing"),
        ("GET", f"{BASE_URL}/v1/security/audit-log", None, 200, "6. Security Audit Logging"),
        ("GET", f"{BASE_URL}/v1/security/status", None, 200, "7. Security Status Monitoring"),
        ("POST", f"{BASE_URL}/v1/security/rotate-keys", None, 200, "8. API Key Rotation"),
        ("GET", f"{BASE_URL}/v1/security/policy", None, 200, "9. Security Policy Management"),
        
        # 10-12. Authentication Features Missing (3 endpoints)
        ("POST", f"{BASE_URL}/v1/2fa/verify", {"user_id": "test_user", "totp_code": "123456"}, 401, "10. 2FA Verification (Expected 401)"),
        ("GET", f"{BASE_URL}/v1/2fa/qr-code?user_id=test_user", None, 200, "11. QR Code Generation"),
        ("POST", f"{BASE_URL}/v1/password/reset", {"email": "test@example.com"}, 200, "12. Password Reset Functionality"),
        
        # 13-15. CSP Management Missing (3 endpoints)
        ("GET", f"{BASE_URL}/v1/csp/policy", None, 200, "13. CSP Policy Retrieval"),
        ("POST", f"{BASE_URL}/v1/csp/report", {
            "violated_directive": "script-src",
            "blocked_uri": "https://malicious.com/script.js",
            "document_uri": "https://bhiv-platform.com/page"
        }, 200, "14. CSP Violation Reporting"),
        ("PUT", f"{BASE_URL}/v1/csp/policy", {"policy": "default-src 'self'"}, 200, "15. CSP Policy Updates"),
        
        # 16-18. Agent Monitoring Missing (3 endpoints)
        ("GET", f"{AGENT_URL}/status", None, 200, "16. Agent Service Status"),
        ("GET", f"{AGENT_URL}/version", None, 200, "17. Agent Version Information"),
        ("GET", f"{AGENT_URL}/metrics", None, 200, "18. Agent Metrics Endpoint"),
        
        # 19. 500 Internal Server Error (Interview scheduling - should now work)
        ("GET", f"{BASE_URL}/v1/interviews", None, 200, "19. Get Interviews (Schema Compatible)"),
        
        # 20. 422 Unprocessable Entity (Input validation - should now handle gracefully)
        ("POST", f"{BASE_URL}/v1/security/test-input-validation", {"input_data": "test input"}, 200, "20. Input Validation (Enhanced Error Handling)")
    ]
    
    # Run tests
    results = []
    passed = 0
    failed = 0
    
    for i, (method, url, data, expected_status, description) in enumerate(tests, 1):
        print(f"Testing {i:2d}/20: {description}")
        result = test_endpoint(method, url, data, expected_status, description)
        results.append(result)
        
        if result["success"]:
            print(f"         PASS - Status: {result['status_code']}")
            passed += 1
        else:
            print(f"         FAIL - Status: {result.get('status_code', 'ERROR')}")
            if 'error' in result:
                print(f"         Error: {result['error']}")
            failed += 1
        
        time.sleep(0.5)  # Rate limiting
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)
    print(f"Total Tests: {len(tests)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {(passed/len(tests)*100):.1f}%")
    
    if passed == len(tests):
        print("\nALL ENDPOINTS FIXED SUCCESSFULLY!")
        print("The platform is now operating at 100% functionality.")
    elif passed >= len(tests) * 0.9:
        print(f"\nEXCELLENT PROGRESS!")
        print(f"Fixed {passed}/{len(tests)} endpoints ({(passed/len(tests)*100):.1f}% success rate)")
    else:
        print(f"\nPARTIAL SUCCESS")
        print(f"Fixed {passed}/{len(tests)} endpoints - some issues remain")
    
    # Detailed results
    print("\nDETAILED RESULTS:")
    print("-" * 60)
    for i, result in enumerate(results, 1):
        status = "PASS" if result["success"] else "FAIL"
        print(f"{i:2d}. {status} - {result['description']}")
        if not result["success"] and 'error' in result:
            print(f"    Error: {result['error']}")
    
    print(f"\nTest completed at: {datetime.now().isoformat()}")
    return passed == len(tests)

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)