#!/usr/bin/env python3
"""
Gateway Auth Integration Test
Tests client portal auth integration with Gateway service
"""

import requests
import json
import sys

def test_gateway_auth_integration():
    """Test Gateway service auth integration"""
    print("Gateway Auth Integration Test")
    print("=" * 50)
    
    gateway_url = "https://bhiv-hr-gateway-46pz.onrender.com"
    
    try:
        # Test 1: Gateway health check
        print("1. Testing Gateway health...")
        health_response = requests.get(f"{gateway_url}/health", timeout=10)
        if health_response.status_code == 200:
            print("   Gateway is healthy")
        else:
            print(f"   Gateway health check failed: {health_response.status_code}")
            return False
        
        # Test 2: Client login endpoint
        print("2. Testing client login endpoint...")
        login_data = {
            "client_id": "TECH001",
            "password": "demo123456"  # Using 8+ character password
        }
        
        login_response = requests.post(
            f"{gateway_url}/v1/client/login",
            json=login_data,
            timeout=10
        )
        
        print(f"   Login response status: {login_response.status_code}")
        if login_response.status_code == 200:
            login_result = login_response.json()
            print(f"   Login result: {login_result}")
            
            if login_result.get('success'):
                token = login_result.get('token')
                print(f"   Authentication successful, token received")
                
                # Test 3: Use token for authenticated requests
                print("3. Testing authenticated requests...")
                headers = {"Authorization": f"Bearer {token}"}
                
                # Test jobs endpoint
                jobs_response = requests.get(f"{gateway_url}/v1/jobs", headers=headers, timeout=10)
                print(f"   Jobs endpoint status: {jobs_response.status_code}")
                
                # Test candidates endpoint
                candidates_response = requests.get(f"{gateway_url}/v1/candidates", headers=headers, timeout=10)
                print(f"   Candidates endpoint status: {candidates_response.status_code}")
                
                if jobs_response.status_code == 200 and candidates_response.status_code == 200:
                    print("   Authenticated requests successful")
                    
                    # Test 4: Job posting
                    print("4. Testing job posting...")
                    job_data = {
                        "title": "Integration Test Engineer",
                        "company": login_result.get('company_name', 'Test Company'),
                        "location": "Remote",
                        "description": "Test job for integration testing",
                        "requirements": ["Python", "Testing", "Integration"],
                        "salary_range": "70000-100000",
                        "job_type": "Full-time",
                        "experience_level": "Mid-level"
                    }
                    
                    job_response = requests.post(
                        f"{gateway_url}/v1/jobs",
                        json=job_data,
                        headers=headers,
                        timeout=10
                    )
                    
                    print(f"   Job posting status: {job_response.status_code}")
                    if job_response.status_code == 201:
                        job_result = job_response.json()
                        print(f"   Job created with ID: {job_result.get('job_id')}")
                        
                        print("\\n=== GATEWAY AUTH INTEGRATION SUMMARY ===")
                        print("Gateway health check: SUCCESS")
                        print("Client authentication: SUCCESS")
                        print("Token-based authorization: SUCCESS")
                        print("Authenticated API access: SUCCESS")
                        print("Job posting functionality: SUCCESS")
                        print("\\nGATEWAY AUTH INTEGRATION: FULLY OPERATIONAL")
                        return True
                    else:
                        print(f"   Job posting failed: {job_response.status_code}")
                else:
                    print("   Authenticated requests failed")
            else:
                print(f"   Authentication failed: {login_result.get('error')}")
        else:
            print(f"   Login endpoint failed: {login_response.status_code}")
            
    except Exception as e:
        print(f"Test error: {e}")
        return False
    
    return False

if __name__ == "__main__":
    success = test_gateway_auth_integration()
    sys.exit(0 if success else 1)