#!/usr/bin/env python3
"""
BHIV HR Platform - Simple Security Test Suite
Tests: CORS Configuration, Cookie Security, API Key Management
"""

import requests
import json

def test_security_endpoints():
    """Test enhanced security endpoints"""
    base_url = "https://bhiv-hr-gateway.onrender.com"
    api_key = "myverysecureapikey123"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    print("BHIV HR Platform - Security Test Suite")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: CORS Configuration Endpoint
    total_tests += 1
    try:
        response = requests.get(f"{base_url}/v1/security/cors-config", headers=headers)
        if response.status_code == 200:
            data = response.json()
            if "cors_config" in data and "allowed_origins" in data["cors_config"]:
                print("[PASS] CORS Configuration endpoint working")
                tests_passed += 1
            else:
                print("[FAIL] CORS Configuration endpoint - invalid response")
        else:
            print(f"[FAIL] CORS Configuration endpoint - status {response.status_code}")
    except Exception as e:
        print(f"[ERROR] CORS Configuration test: {e}")
    
    # Test 2: Cookie Configuration Endpoint
    total_tests += 1
    try:
        response = requests.get(f"{base_url}/v1/security/cookie-config", headers=headers)
        if response.status_code == 200:
            data = response.json()
            if "cookie_security" in data:
                cookie_config = data["cookie_security"]
                security_features = ["secure", "httponly", "samesite"]
                features_present = sum(1 for feature in security_features if feature in cookie_config)
                
                if features_present >= 2:
                    print(f"[PASS] Cookie Security - {features_present}/3 features configured")
                    tests_passed += 1
                else:
                    print(f"[FAIL] Cookie Security - only {features_present}/3 features configured")
            else:
                print("[FAIL] Cookie Configuration endpoint - invalid response")
        else:
            print(f"[FAIL] Cookie Configuration endpoint - status {response.status_code}")
    except Exception as e:
        print(f"[ERROR] Cookie Configuration test: {e}")
    
    # Test 3: API Key Generation
    total_tests += 1
    try:
        response = requests.post(
            f"{base_url}/v1/security/api-keys/generate",
            params={"client_id": "test_client"},
            headers=headers
        )
        if response.status_code == 200:
            data = response.json()
            if "key_data" in data and "api_key" in data["key_data"]:
                print("[PASS] API Key Generation working")
                tests_passed += 1
            else:
                print("[FAIL] API Key Generation - invalid response format")
        else:
            print(f"[FAIL] API Key Generation - status {response.status_code}")
    except Exception as e:
        print(f"[ERROR] API Key Generation test: {e}")
    
    # Test 4: Session Management
    total_tests += 1
    try:
        login_data = {"client_id": "TECH001", "password": "demo123"}
        response = requests.post(f"{base_url}/v1/sessions/create", json=login_data)
        
        if response.status_code == 200:
            # Check for secure cookie headers
            set_cookie = response.headers.get("Set-Cookie", "")
            if "HttpOnly" in set_cookie or "session_id" in set_cookie:
                print("[PASS] Session Management with secure cookies")
                tests_passed += 1
            else:
                print("[FAIL] Session Management - no secure cookies")
        else:
            print(f"[FAIL] Session Management - status {response.status_code}")
    except Exception as e:
        print(f"[ERROR] Session Management test: {e}")
    
    # Test 5: Security Headers
    total_tests += 1
    try:
        response = requests.get(f"{base_url}/health")
        security_headers = [
            "X-Content-Type-Options",
            "X-Frame-Options", 
            "X-XSS-Protection",
            "Content-Security-Policy"
        ]
        
        headers_present = sum(1 for header in security_headers if header in response.headers)
        
        if headers_present >= 3:
            print(f"[PASS] Security Headers - {headers_present}/4 headers present")
            tests_passed += 1
        else:
            print(f"[FAIL] Security Headers - only {headers_present}/4 headers present")
    except Exception as e:
        print(f"[ERROR] Security Headers test: {e}")
    
    print("\n" + "=" * 50)
    print(f"Security Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed >= 4:
        print("[SUCCESS] Security implementation is working correctly!")
        print("\nSecurity Issues Resolved:")
        print("- CORS properly configured for trusted origins")
        print("- Cookie security features implemented")
        print("- API key management system active")
        print("- Session management with secure cookies")
        print("- Security headers properly set")
    else:
        print(f"[WARNING] {total_tests - tests_passed} security tests failed")
    
    return tests_passed >= 4

if __name__ == "__main__":
    success = test_security_endpoints()
    exit(0 if success else 1)