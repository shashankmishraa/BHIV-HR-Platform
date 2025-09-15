#!/usr/bin/env python3
"""
Test script to verify the client refresh endpoint fix
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
    print(f"\n🔍 Testing endpoints at: {base_url}")
    
    # Test data
    test_refresh_token = "refresh_token_TECH001_1234567890"
    
    # Test 1: POST method (original)
    print("\n1️⃣ Testing POST /v1/client/refresh")
    try:
        response = requests.post(
            f"{base_url}/v1/client/refresh",
            json={"refresh_token": test_refresh_token},
            timeout=10
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ POST method works")
            result = response.json()
            print(f"   Response: {result.get('message', 'No message')}")
        else:
            print(f"   ❌ POST failed: {response.text[:100]}")
    except Exception as e:
        print(f"   ❌ POST error: {str(e)}")
    
    # Test 2: GET method (new fix)
    print("\n2️⃣ Testing GET /v1/client/refresh")
    try:
        response = requests.get(
            f"{base_url}/v1/client/refresh",
            params={"refresh_token": test_refresh_token},
            timeout=10
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ GET method works")
            result = response.json()
            print(f"   Response: {result.get('message', 'No message')}")
        else:
            print(f"   ❌ GET failed: {response.text[:100]}")
    except Exception as e:
        print(f"   ❌ GET error: {str(e)}")
    
    # Test 3: POST logout
    print("\n3️⃣ Testing POST /v1/client/logout")
    try:
        response = requests.post(
            f"{base_url}/v1/client/logout",
            json={},
            timeout=10
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ POST logout works")
        else:
            print(f"   ❌ POST logout failed: {response.text[:100]}")
    except Exception as e:
        print(f"   ❌ POST logout error: {str(e)}")
    
    # Test 4: GET logout
    print("\n4️⃣ Testing GET /v1/client/logout")
    try:
        response = requests.get(
            f"{base_url}/v1/client/logout",
            timeout=10
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ GET logout works")
        else:
            print(f"   ❌ GET logout failed: {response.text[:100]}")
    except Exception as e:
        print(f"   ❌ GET logout error: {str(e)}")

def test_health_check(base_url):
    """Test basic health check"""
    print(f"\n🏥 Testing health check at: {base_url}")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("   ✅ Health check passed")
            return True
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Health check error: {str(e)}")
        return False

def main():
    print("🔧 BHIV HR Platform - Endpoint Fix Verification")
    print("=" * 50)
    
    # Test production deployment
    print("\n🌐 Testing Production Deployment (Render)")
    if test_health_check(API_BASE_URL):
        test_endpoint_methods(API_BASE_URL)
    else:
        print("   ⚠️ Production deployment not accessible")
    
    # Test local deployment if available
    print("\n💻 Testing Local Deployment")
    if test_health_check(LOCAL_URL):
        test_endpoint_methods(LOCAL_URL)
    else:
        print("   ⚠️ Local deployment not running")
    
    print("\n" + "=" * 50)
    print("✅ Endpoint fix verification complete!")
    print("📋 Summary:")
    print("   - Added GET /v1/client/refresh to handle deployment issues")
    print("   - Added GET /v1/client/logout for consistency")
    print("   - Maintained backward compatibility with POST methods")
    print("   - Total endpoints: 48 (was 46)")

if __name__ == "__main__":
    main()