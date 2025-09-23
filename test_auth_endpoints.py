#!/usr/bin/env python3
"""
Test Authentication Endpoints - Priority 2 Resolution
"""

import requests
import json
from datetime import datetime

def test_auth_endpoints():
    """Test authentication endpoints"""
    
    base_url = "https://bhiv-hr-gateway-901a.onrender.com"
    
    print("=== TESTING AUTHENTICATION ENDPOINTS ===")
    print(f"Testing against: {base_url}")
    print(f"Test time: {datetime.now()}")
    print()
    
    # Test 1: Basic login endpoint
    print("1. Testing /auth/login")
    try:
        response = requests.post(
            f"{base_url}/auth/login",
            json={"username": "admin", "password": "admin123"},
            timeout=30
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Success: {data.get('message', 'Login successful')}")
            print(f"   User: {data.get('username', 'N/A')}")
            print(f"   Token: {data.get('access_token', 'N/A')[:20]}...")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Exception: {str(e)}")
    print()
    
    # Test 2: V1 login endpoint
    print("2. Testing /v1/auth/login")
    try:
        response = requests.post(
            f"{base_url}/v1/auth/login",
            json={"username": "TECH001", "password": "demo123"},
            timeout=30
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Success: {data.get('message', 'Login successful')}")
            print(f"   User: {data.get('username', 'N/A')}")
            print(f"   Role: {data.get('role', 'N/A')}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Exception: {str(e)}")
    print()
    
    # Test 3: Auth status endpoint
    print("3. Testing /v1/auth/status")
    try:
        response = requests.get(f"{base_url}/v1/auth/status", timeout=30)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   System: {data.get('authentication_system', 'N/A')}")
            print(f"   Users: {data.get('total_users', 0)}")
            print(f"   JWT Enabled: {data.get('jwt_enabled', False)}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Exception: {str(e)}")
    print()
    
    # Test 4: Current user endpoint
    print("4. Testing /v1/auth/me")
    try:
        response = requests.get(f"{base_url}/v1/auth/me", timeout=30)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   User ID: {data.get('user_id', 'N/A')}")
            print(f"   Authenticated: {data.get('authenticated', False)}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Exception: {str(e)}")
    print()
    
    # Test 5: Logout endpoint
    print("5. Testing /v1/auth/logout")
    try:
        response = requests.post(f"{base_url}/v1/auth/logout", timeout=30)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Message: {data.get('message', 'Logout successful')}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Exception: {str(e)}")
    print()
    
    print("=== AUTHENTICATION TEST COMPLETE ===")

if __name__ == "__main__":
    test_auth_endpoints()