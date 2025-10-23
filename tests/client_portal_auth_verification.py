#!/usr/bin/env python3
"""
Verify client portal authentication is fully working after timezone fix
"""

import requests
import json
from datetime import datetime

# Test configuration
GATEWAY_URL = "https://bhiv-hr-gateway-46pz.onrender.com"
CLIENT_PORTAL_URL = "https://bhiv-hr-client-portal-5g33.onrender.com"

def test_client_login_api():
    """Test client login through Gateway API"""
    print("Testing Client Login API...")
    
    login_data = {
        "client_id": "TECH001",
        "password": "demo123"
    }
    
    try:
        response = requests.post(
            f"{GATEWAY_URL}/v1/client/login",
            json=login_data,
            timeout=15
        )
        
        print(f"API Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {data}")
            
            if data.get("success"):
                print("PASS | Client login API working")
                return data.get("token"), data.get("client_data", {})
            else:
                print(f"FAIL | Login failed: {data.get('error')}")
                return None, None
        else:
            print(f"FAIL | HTTP {response.status_code}: {response.text}")
            return None, None
            
    except Exception as e:
        print(f"FAIL | API test error: {e}")
        return None, None

def test_portal_accessibility():
    """Test client portal is accessible"""
    print("\nTesting Client Portal Accessibility...")
    
    try:
        response = requests.get(CLIENT_PORTAL_URL, timeout=10)
        print(f"Portal Status: {response.status_code}")
        
        if response.status_code == 200:
            print("PASS | Client portal is accessible")
            return True
        else:
            print(f"FAIL | Portal not accessible: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"FAIL | Portal accessibility error: {e}")
        return False

def test_jobs_api_with_auth(token):
    """Test jobs API with client authentication"""
    print("\nTesting Jobs API with Client Auth...")
    
    if not token:
        print("SKIP | No token available")
        return False
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{GATEWAY_URL}/v1/jobs", headers=headers, timeout=10)
        
        print(f"Jobs API Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            jobs = data.get("jobs", [])
            print(f"PASS | Found {len(jobs)} jobs")
            return True
        else:
            print(f"FAIL | Jobs API error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"FAIL | Jobs API test error: {e}")
        return False

def main():
    """Run all verification tests"""
    print("Client Portal Authentication Verification")
    print("=" * 45)
    print(f"Timestamp: {datetime.now()}")
    print()
    
    # Test 1: Client login API
    token, client_data = test_client_login_api()
    
    # Test 2: Portal accessibility
    portal_accessible = test_portal_accessibility()
    
    # Test 3: Authenticated API access
    jobs_working = test_jobs_api_with_auth(token)
    
    # Summary
    print("\n" + "=" * 45)
    print("VERIFICATION SUMMARY")
    print("=" * 45)
    
    tests = [
        ("Client Login API", token is not None),
        ("Portal Accessibility", portal_accessible),
        ("Authenticated Jobs API", jobs_working)
    ]
    
    passed = 0
    for test_name, result in tests:
        status = "PASS" if result else "FAIL"
        print(f"{status} | {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("\nSUCCESS: Client portal authentication is fully working!")
        print("Timezone issue has been resolved.")
        print("All authentication flows are operational.")
    else:
        print("\nISSUE: Some tests failed.")
        print("Check the output above for details.")

if __name__ == "__main__":
    main()