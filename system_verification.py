#!/usr/bin/env python3
"""
System Verification and Issue Resolution
Clean implementation without Unicode characters
"""

import requests
import json
from datetime import datetime

def verify_system_health():
    """Verify system is operational"""
    api_base = "https://bhiv-hr-gateway-46pz.onrender.com"
    headers = {"Authorization": "Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"}
    
    try:
        response = requests.get(f"{api_base}/health", headers=headers, timeout=10)
        return response.status_code == 200, response.status_code
    except Exception as e:
        return False, str(e)

def test_database_connection():
    """Test database connectivity"""
    api_base = "https://bhiv-hr-gateway-46pz.onrender.com"
    headers = {"Authorization": "Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"}
    
    try:
        response = requests.get(f"{api_base}/test-candidates", headers=headers, timeout=10)
        return response.status_code == 200, response.status_code
    except Exception as e:
        return False, str(e)

def test_dashboard_data():
    """Test dashboard data retrieval"""
    api_base = "https://bhiv-hr-gateway-46pz.onrender.com"
    headers = {"Authorization": "Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"}
    
    try:
        jobs_response = requests.get(f"{api_base}/v1/jobs", headers=headers, timeout=10)
        candidates_response = requests.get(f"{api_base}/v1/candidates/search", headers=headers, timeout=10)
        
        jobs_success = jobs_response.status_code == 200
        candidates_success = candidates_response.status_code == 200
        
        if jobs_success and candidates_success:
            jobs_data = jobs_response.json()
            candidates_data = candidates_response.json()
            
            total_jobs = len(jobs_data.get('jobs', []))
            total_candidates = len(candidates_data.get('candidates', []))
            
            return True, f"Jobs: {total_jobs}, Candidates: {total_candidates}"
        else:
            return False, f"Jobs: {jobs_response.status_code}, Candidates: {candidates_response.status_code}"
            
    except Exception as e:
        return False, str(e)

def test_job_creation():
    """Test job creation functionality"""
    api_base = "https://bhiv-hr-gateway-46pz.onrender.com"
    headers = {"Authorization": "Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"}
    
    test_job = {
        "title": "System Test Engineer",
        "department": "Engineering", 
        "location": "Remote",
        "experience_level": "Mid-level",
        "requirements": "Python, Testing, System Verification",
        "description": "System verification engineer for platform testing",
        "client_id": 1,
        "employment_type": "Full-time",
        "status": "active"
    }
    
    try:
        response = requests.post(f"{api_base}/v1/jobs", json=test_job, headers=headers, timeout=10)
        if response.status_code == 200:
            result = response.json()
            job_id = result.get('job_id')
            return True, f"Job created with ID: {job_id}"
        else:
            return False, f"Status: {response.status_code}, Response: {response.text[:200]}"
    except Exception as e:
        return False, str(e)

def test_candidate_search():
    """Test candidate search functionality"""
    api_base = "https://bhiv-hr-gateway-46pz.onrender.com"
    headers = {"Authorization": "Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"}
    
    try:
        response = requests.get(f"{api_base}/v1/candidates/search", headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            candidates = data.get('candidates', [])
            return True, f"Found {len(candidates)} candidates"
        else:
            return False, f"Status: {response.status_code}, Response: {response.text[:200]}"
    except Exception as e:
        return False, str(e)

def test_ai_matching():
    """Test AI matching functionality"""
    try:
        agent_url = "https://bhiv-hr-agent-m1me.onrender.com"
        response = requests.post(f"{agent_url}/match", json={"job_id": 1}, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            candidates = data.get('top_candidates', [])
            return True, f"AI matched {len(candidates)} candidates"
        else:
            return False, f"Status: {response.status_code}"
    except Exception as e:
        return False, str(e)

def run_comprehensive_verification():
    """Run comprehensive system verification"""
    print("System Verification Started")
    print(f"Timestamp: {datetime.now()}")
    print("=" * 50)
    
    tests = [
        ("System Health Check", verify_system_health),
        ("Database Connection", test_database_connection),
        ("Dashboard Data", test_dashboard_data),
        ("Job Creation", test_job_creation),
        ("Candidate Search", test_candidate_search),
        ("AI Matching", test_ai_matching)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\nTesting: {test_name}")
        try:
            success, message = test_func()
            if success:
                print(f"PASS: {message}")
                results.append((test_name, True, message))
            else:
                print(f"FAIL: {message}")
                results.append((test_name, False, message))
        except Exception as e:
            print(f"ERROR: {str(e)}")
            results.append((test_name, False, str(e)))
    
    # Summary
    print("\n" + "=" * 50)
    print("VERIFICATION SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    print(f"Tests Passed: {passed}/{total} ({passed/total*100:.1f}%)")
    
    for test_name, success, message in results:
        status = "PASS" if success else "FAIL"
        print(f"{status}: {test_name} - {message}")
    
    return passed == total

if __name__ == "__main__":
    success = run_comprehensive_verification()
    
    if success:
        print("\nAll systems operational!")
    else:
        print("\nSome systems require attention")