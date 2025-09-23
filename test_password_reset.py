#!/usr/bin/env python3
"""
Test Password Reset Endpoint
"""

import requests
import json

# Configuration
BASE_URL = "https://bhiv-hr-gateway-901a.onrender.com"
API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"

def test_password_reset():
    """Test password reset endpoint"""
    
    # Test data
    test_email = "test@example.com"
    
    # Headers
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Request payload
    payload = {
        "email": test_email
    }
    
    print("Testing Password Reset Endpoint...")
    print(f"URL: {BASE_URL}/v1/password/reset")
    print(f"Email: {test_email}")
    
    try:
        # Make request
        response = requests.post(
            f"{BASE_URL}/v1/password/reset",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("[PASS] Password Reset Test PASSED")
            print(f"Message: {result.get('message')}")
            print(f"Email: {result.get('email')}")
            print(f"Reset Token: {result.get('reset_token')[:20]}...")
            print(f"Expires In: {result.get('expires_in')}")
            print(f"Reset Link: {result.get('reset_link')[:50]}...")
            print(f"Initiated At: {result.get('initiated_at')}")
            return True
        else:
            print("[FAIL] Password Reset Test FAILED")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Request Error: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected Error: {e}")
        return False

if __name__ == "__main__":
    success = test_password_reset()
    exit(0 if success else 1)