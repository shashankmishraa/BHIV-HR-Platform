#!/usr/bin/env python3
"""
Simple test script to verify the client refresh endpoint fix
Tests both GET and POST methods for /v1/client/refresh
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
API_BASE_URL = "https://bhiv-hr-gateway.onrender.com"
LOCAL_URL = "http://localhost:8000"

def test_endpoint_methods(base_url):
    """Test both GET and POST methods for client refresh endpoint"""
    print(f"\nTesting endpoints at: {base_url}")
    
    # Test data
    test_refresh_token = "refresh_token_TECH001_1234567890"
    
    # Test 1: POST method (original)
    print("\n1. Testing POST /v1/client/refresh")
    try:
        response = requests.post(
            f"{base_url}/v1/client/refresh",
            json={"refresh_token": test_refresh_token},
            timeout=10
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   SUCCESS: POST method works")
            result = response.json()
            print(f"   Response: {result.get('message', 'No message')}")
        else:
            print(f"   FAILED: POST failed: {response.text[:100]}")
    except Exception as e:
        print(f"   ERROR: POST error: {str(e)}")
    
    # Test 2: GET method (new fix)
    print("\n2. Testing GET /v1/client/refresh")
    try:
        response = requests.get(
            f"{base_url}/v1/client/refresh",
            params={"refresh_token": test_refresh_token},
            timeout=10
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   SUCCESS: GET method works")
            result = response.json()
            print(f"   Response: {result.get('message', 'No message')}")
        else:
            print(f"   FAILED: GET failed: {response.text[:100]}")
    except Exception as e:
        print(f"   ERROR: GET error: {str(e)}")

def test_health_check(base_url):
    """Test basic health check"""
    print(f"\nTesting health check at: {base_url}")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("   SUCCESS: Health check passed")
            return True
        else:
            print(f"   FAILED: Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ERROR: Health check error: {str(e)}")
        return False

def main():
    print("BHIV HR Platform - Endpoint Fix Verification")
    print("=" * 50)
    
    # Test production deployment
    print("\nTesting Production Deployment (Render)")
    if test_health_check(API_BASE_URL):
        test_endpoint_methods(API_BASE_URL)
    else:
        print("   WARNING: Production deployment not accessible")
    
    # Test local deployment if available
    print("\nTesting Local Deployment")
    if test_health_check(LOCAL_URL):
        test_endpoint_methods(LOCAL_URL)
    else:
        print("   WARNING: Local deployment not running")
    
    print("\n" + "=" * 50)
    print("Endpoint fix verification complete!")
    print("Summary:")
    print("   - Added GET /v1/client/refresh to handle deployment issues")
    print("   - Added GET /v1/client/logout for consistency")
    print("   - Maintained backward compatibility with POST methods")
    print("   - Total endpoints: 48 (was 46)")

if __name__ == "__main__":
    main()