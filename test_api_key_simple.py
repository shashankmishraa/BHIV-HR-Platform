#!/usr/bin/env python3
"""
Simple API key test
"""
import requests
import os

# Test different API keys
API_KEYS = [
    "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o",  # Production key
    "local_api_key_development_2025_secure",  # Old local key
]

BASE_URL = "http://localhost:8000"

def test_api_key(api_key, description):
    """Test a specific API key"""
    print(f"\n=== Testing {description} ===")
    print(f"API Key: {api_key[:20]}...")
    
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        response = requests.get(f"{BASE_URL}/v1/jobs", headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("SUCCESS: API key works!")
            return True
        elif response.status_code == 401:
            print("FAILED: Invalid API key")
        elif response.status_code == 403:
            print("FAILED: Forbidden (rate limited?)")
        else:
            print(f"FAILED: Unexpected status {response.status_code}")
        
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def check_environment():
    """Check environment variables"""
    print("=== Environment Check ===")
    
    # Check .env file
    try:
        with open('.env', 'r') as f:
            content = f.read()
            if 'API_KEY_SECRET=' in content:
                for line in content.split('\n'):
                    if line.startswith('API_KEY_SECRET='):
                        env_key = line.split('=', 1)[1]
                        print(f"Environment API Key: {env_key[:20]}...")
                        break
    except Exception as e:
        print(f"Could not read .env file: {e}")

def main():
    """Test API keys"""
    print("=== API Key Authentication Test ===")
    
    check_environment()
    
    for i, api_key in enumerate(API_KEYS):
        description = f"Key {i+1} ({'Production' if 'prod_' in api_key else 'Local'})"
        success = test_api_key(api_key, description)
        if success:
            print(f"\n✓ Working API Key Found: {description}")
            return 0
    
    print("\n✗ No working API keys found")
    print("\nTroubleshooting:")
    print("1. Check if gateway service restarted with new environment")
    print("2. Verify .env file has correct API_KEY_SECRET")
    print("3. Check docker-compose environment variables")
    
    return 1

if __name__ == "__main__":
    exit(main())