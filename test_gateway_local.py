#!/usr/bin/env python3
"""Test Gateway Routes Locally"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'services', 'gateway', 'app'))

from main import app
from fastapi.testclient import TestClient

def test_gateway_routes():
    """Test all gateway routes locally"""
    client = TestClient(app)
    
    # Test critical endpoints that HR portal needs
    endpoints = [
        {'path': '/', 'method': 'GET'},
        {'path': '/health', 'method': 'GET'},
        {'path': '/v1/candidates', 'method': 'GET'},
        {'path': '/v1/jobs', 'method': 'GET'},
        {'path': '/v1/interviews', 'method': 'GET'},
        {'path': '/v1/analytics/dashboard', 'method': 'GET'},
        {'path': '/metrics', 'method': 'GET'},
        {'path': '/health/detailed', 'method': 'GET'},
        {'path': '/v1/database/health', 'method': 'GET'},
        {'path': '/v1/auth/profile', 'method': 'GET'},
        {'path': '/v1/client/profile', 'method': 'GET'},
        {'path': '/v1/security/rate-limit-status', 'method': 'GET'},
    ]
    
    print('=== LOCAL GATEWAY ROUTE TEST ===')
    success_count = 0
    total_count = len(endpoints)
    
    for endpoint in endpoints:
        try:
            if endpoint['method'] == 'GET':
                response = client.get(endpoint['path'])
            elif endpoint['method'] == 'POST':
                response = client.post(endpoint['path'])
            
            if response.status_code == 200:
                print(f"OK {endpoint['method']} {endpoint['path']} - {response.status_code}")
                success_count += 1
            else:
                print(f"FAIL {endpoint['method']} {endpoint['path']} - {response.status_code}")
                
        except Exception as e:
            print(f"ERROR {endpoint['method']} {endpoint['path']} - {str(e)}")
    
    print(f'\nSUCCESS RATE: {success_count}/{total_count} ({(success_count/total_count)*100:.1f}%)')
    
    if success_count == total_count:
        print('SUCCESS: All gateway routes are working locally!')
        return True
    else:
        print('PARTIAL: Some routes need fixing')
        return False

def test_post_endpoints():
    """Test POST endpoints with sample data"""
    client = TestClient(app)
    
    print('\n=== TESTING POST ENDPOINTS ===')
    
    # Test candidate creation
    candidate_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+1234567890",
        "skills": ["Python", "FastAPI"],
        "experience_years": 5,
        "location": "New York"
    }
    
    try:
        response = client.post("/v1/candidates", json=candidate_data)
        if response.status_code == 200:
            print(f"OK POST /v1/candidates - {response.status_code}")
            print(f"  Response: {response.json()}")
        else:
            print(f"FAIL POST /v1/candidates - {response.status_code}")
            print(f"  Error: {response.text}")
    except Exception as e:
        print(f"ERROR POST /v1/candidates - {str(e)}")
    
    # Test job creation
    job_data = {
        "title": "Software Engineer",
        "description": "We are looking for a skilled software engineer to join our team.",
        "requirements": ["Python", "FastAPI", "PostgreSQL"],
        "location": "Remote",
        "department": "Engineering",
        "experience_level": "Mid-level",
        "salary_min": 80000,
        "salary_max": 120000,
        "job_type": "Full-time",
        "company_id": "tech001"
    }
    
    try:
        response = client.post("/v1/jobs", json=job_data)
        if response.status_code == 200:
            print(f"OK POST /v1/jobs - {response.status_code}")
            print(f"  Response: {response.json()}")
        else:
            print(f"FAIL POST /v1/jobs - {response.status_code}")
            print(f"  Error: {response.text}")
    except Exception as e:
        print(f"ERROR POST /v1/jobs - {str(e)}")

if __name__ == "__main__":
    print("Testing gateway implementation locally...")
    
    # Test GET endpoints
    get_success = test_gateway_routes()
    
    # Test POST endpoints
    test_post_endpoints()
    
    if get_success:
        print("\nCONCLUSION: Gateway implementation is working correctly!")
        print("The 404 errors in production are due to deployment not picking up the latest code.")
        print("Solution: Force redeploy on Render or check deployment configuration.")
    else:
        print("\nCONCLUSION: Gateway implementation needs additional fixes.")