#!/usr/bin/env python3
"""
Final comprehensive test of client portal authentication
"""

import requests
import json
from datetime import datetime

# Test configuration
GATEWAY_URL = "https://bhiv-hr-gateway-46pz.onrender.com"
CLIENT_PORTAL_URL = "https://bhiv-hr-client-portal-5g33.onrender.com"

def test_complete_client_flow():
    """Test complete client authentication flow"""
    print("Final Client Portal Authentication Test")
    print("=" * 45)
    print(f"Timestamp: {datetime.now()}")
    print()
    
    # Step 1: Client Login
    print("Step 1: Testing Client Login...")
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
        
        print(f"Login API Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("success"):
                token = data.get("access_token")
                client_id = data.get("client_id")
                company_name = data.get("company_name")
                
                print(f"PASS | Login successful")
                print(f"  - Client ID: {client_id}")
                print(f"  - Company: {company_name}")
                print(f"  - Token: {token[:50]}...")
                
                # Step 2: Test authenticated API access
                print("\nStep 2: Testing Authenticated API Access...")
                
                headers = {"Authorization": f"Bearer {token}"}
                jobs_response = requests.get(f"{GATEWAY_URL}/v1/jobs", headers=headers, timeout=10)
                
                print(f"Jobs API Status: {jobs_response.status_code}")
                
                if jobs_response.status_code == 200:
                    jobs_data = jobs_response.json()
                    jobs = jobs_data.get("jobs", [])
                    print(f"PASS | Found {len(jobs)} jobs")
                    
                    if jobs:
                        print("Sample jobs:")
                        for i, job in enumerate(jobs[:3]):
                            print(f"  {i+1}. {job.get('title')} - {job.get('department')}")
                    
                    # Step 3: Test portal accessibility
                    print("\nStep 3: Testing Portal Accessibility...")
                    portal_response = requests.get(CLIENT_PORTAL_URL, timeout=10)
                    
                    print(f"Portal Status: {portal_response.status_code}")
                    
                    if portal_response.status_code == 200:
                        print("PASS | Client portal is accessible")
                        
                        # Summary
                        print("\n" + "=" * 45)
                        print("FINAL RESULT: ALL TESTS PASSED!")
                        print("=" * 45)
                        print("✓ Client login API working")
                        print("✓ JWT token authentication working")
                        print("✓ Authenticated API access working")
                        print("✓ Client portal accessible")
                        print("\nTimezone issue has been RESOLVED!")
                        print("Client portal authentication is fully operational.")
                        return True
                    else:
                        print(f"FAIL | Portal not accessible: {portal_response.status_code}")
                        return False
                else:
                    print(f"FAIL | Jobs API error: {jobs_response.status_code}")
                    return False
            else:
                print(f"FAIL | Login failed: {data.get('error')}")
                return False
        else:
            print(f"FAIL | HTTP {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"FAIL | Test error: {e}")
        return False

if __name__ == "__main__":
    success = test_complete_client_flow()
    
    if not success:
        print("\n" + "=" * 45)
        print("SOME TESTS FAILED")
        print("Check the output above for details.")