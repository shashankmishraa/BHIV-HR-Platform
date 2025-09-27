#!/usr/bin/env python3
"""
Test Database Persistence Fixes
"""

import requests
import time
from datetime import datetime

def test_job_persistence():
    """Test job creation and persistence"""
    api_base = "https://bhiv-hr-gateway-46pz.onrender.com"
    headers = {"Authorization": "Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"}
    
    print("Testing Job Persistence Fix")
    print("=" * 40)
    
    # Create job with all required fields
    test_job = {
        "title": "Persistence Test Job",
        "department": "Testing",
        "location": "Remote",
        "experience_level": "Mid-level", 
        "requirements": "Database persistence testing",
        "description": "Test job for database persistence verification",
        "salary_min": 85000,
        "salary_max": 125000,
        "client_id": 1,
        "employment_type": "Full-time",
        "status": "active"
    }
    
    try:
        # Create job
        create_response = requests.post(f"{api_base}/v1/jobs", json=test_job, headers=headers, timeout=10)
        print(f"Job Creation Status: {create_response.status_code}")
        
        if create_response.status_code == 200:
            result = create_response.json()
            job_id = result.get('job_id')
            print(f"Created Job ID: {job_id}")
            
            # Wait for processing
            time.sleep(3)
            
            # Check if job appears in list
            list_response = requests.get(f"{api_base}/v1/jobs", headers=headers, timeout=10)
            print(f"Jobs List Status: {list_response.status_code}")
            
            if list_response.status_code == 200:
                jobs_data = list_response.json()
                jobs = jobs_data.get('jobs', [])
                print(f"Total Jobs in API: {len(jobs)}")
                
                # Look for our job
                our_job = next((j for j in jobs if j.get('title') == test_job['title']), None)
                if our_job:
                    print("SUCCESS: Job persisted and appears in API")
                    return True
                else:
                    print("ISSUE: Job not found in API response")
                    return False
        else:
            print(f"Job creation failed: {create_response.text}")
            return False
            
    except Exception as e:
        print(f"Test error: {e}")
        return False

def test_candidate_persistence():
    """Test candidate creation and persistence"""
    api_base = "https://bhiv-hr-gateway-46pz.onrender.com"
    headers = {"Authorization": "Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"}
    
    print("\nTesting Candidate Persistence Fix")
    print("=" * 40)
    
    test_candidate = {
        "name": "Persistence Test Candidate",
        "email": "persistence.test@bhiv.com",
        "phone": "+1-555-0399",
        "location": "Remote",
        "technical_skills": "Database persistence, Testing, Verification",
        "experience_years": 5,
        "seniority_level": "Senior",
        "education_level": "Master's"
    }
    
    try:
        # Create candidate
        create_response = requests.post(f"{api_base}/v1/candidates", json=test_candidate, headers=headers, timeout=10)
        print(f"Candidate Creation Status: {create_response.status_code}")
        
        if create_response.status_code == 200:
            result = create_response.json()
            candidate_id = result.get('id')
            print(f"Created Candidate ID: {candidate_id}")
            
            # Wait for processing
            time.sleep(3)
            
            # Check if candidate appears in list
            list_response = requests.get(f"{api_base}/v1/candidates", headers=headers, timeout=10)
            print(f"Candidates List Status: {list_response.status_code}")
            
            if list_response.status_code == 200:
                candidates_data = list_response.json()
                candidates = candidates_data.get('candidates', [])
                print(f"Total Candidates in API: {len(candidates)}")
                
                # Look for our candidate
                our_candidate = next((c for c in candidates if c.get('name') == test_candidate['name']), None)
                if our_candidate:
                    print("SUCCESS: Candidate persisted and appears in API")
                    return True
                else:
                    print("ISSUE: Candidate not found in API response")
                    return False
        else:
            print(f"Candidate creation failed: {create_response.text}")
            return False
            
    except Exception as e:
        print(f"Test error: {e}")
        return False

def test_new_endpoints():
    """Test new interview and feedback endpoints"""
    api_base = "https://bhiv-hr-gateway-46pz.onrender.com"
    headers = {"Authorization": "Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"}
    
    print("\nTesting New Endpoints")
    print("=" * 40)
    
    # Test interviews endpoint
    try:
        interviews_response = requests.get(f"{api_base}/v1/interviews", headers=headers, timeout=10)
        print(f"Interviews Endpoint: {interviews_response.status_code}")
    except Exception as e:
        print(f"Interviews endpoint error: {e}")
    
    # Test feedback endpoint
    try:
        feedback_response = requests.get(f"{api_base}/v1/feedback", headers=headers, timeout=10)
        print(f"Feedback Endpoint: {feedback_response.status_code}")
    except Exception as e:
        print(f"Feedback endpoint error: {e}")

def run_persistence_tests():
    """Run all persistence tests"""
    print("DATABASE PERSISTENCE TESTS")
    print(f"Timestamp: {datetime.now()}")
    print("=" * 50)
    
    job_success = test_job_persistence()
    candidate_success = test_candidate_persistence()
    test_new_endpoints()
    
    print(f"\nTest Results:")
    print(f"Job Persistence: {'PASS' if job_success else 'FAIL'}")
    print(f"Candidate Persistence: {'PASS' if candidate_success else 'FAIL'}")
    
    return job_success and candidate_success

if __name__ == "__main__":
    success = run_persistence_tests()
    
    if success:
        print("\nAll persistence tests passed!")
    else:
        print("\nSome persistence tests failed")