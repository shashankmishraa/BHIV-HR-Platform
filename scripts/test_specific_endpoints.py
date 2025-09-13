#!/usr/bin/env python3
"""
Test specific endpoints to debug issues
"""

import requests
import json

GATEWAY_URL = "https://bhiv-hr-gateway.onrender.com"
API_KEY = "myverysecureapikey123"
headers = {"Authorization": f"Bearer {API_KEY}"}

def test_endpoint_detailed(method, url, data=None):
    """Test endpoint with detailed response"""
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=30)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=30)
        
        print(f"\n{method} {url}")
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.headers.get('content-type', '').startswith('application/json'):
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Response: {response.text[:500]}")
            
    except Exception as e:
        print(f"\n{method} {url}")
        print(f"Error: {str(e)}")

def main():
    print("Testing Specific Endpoints")
    print("=" * 50)
    
    # Test candidates endpoint
    test_endpoint_detailed("GET", f"{GATEWAY_URL}/v1/candidates")
    
    # Test job creation with proper data
    job_data = {
        "title": "Software Engineer",
        "department": "Engineering", 
        "location": "Remote",
        "experience_level": "Mid-level",
        "requirements": "Python, FastAPI, PostgreSQL",
        "description": "Full-stack developer position"
    }
    test_endpoint_detailed("POST", f"{GATEWAY_URL}/v1/jobs", job_data)
    
    # Test AI matching
    match_data = {
        "job_id": 1,
        "requirements": "Python developer",
        "location": "Remote"
    }
    test_endpoint_detailed("POST", f"{GATEWAY_URL}/v1/match", match_data)
    
    # Test interview scheduling
    interview_data = {
        "candidate_id": 1,
        "job_id": 1,
        "interview_date": "2025-01-20T10:00:00",
        "interviewer": "John Doe",
        "notes": "Technical interview"
    }
    test_endpoint_detailed("POST", f"{GATEWAY_URL}/v1/interviews", interview_data)

if __name__ == "__main__":
    main()