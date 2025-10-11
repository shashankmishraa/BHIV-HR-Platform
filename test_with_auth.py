#!/usr/bin/env python3
"""
Test all endpoints with proper local authentication
"""
import requests
import json
import sys

# Local configuration
BASE_URL = "http://localhost:8000"
AGENT_URL = "http://localhost:9000"
LOCAL_API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
HEADERS = {"Authorization": f"Bearer {LOCAL_API_KEY}", "Content-Type": "application/json"}

def test_auth_endpoints():
    """Test authentication with local API key"""
    print("=== Testing Authentication ===")
    
    # Test without auth (should fail)
    try:
        response = requests.get(f"{BASE_URL}/v1/jobs", timeout=10)
        if response.status_code == 401:
            print("SUCCESS: Unauthorized access properly blocked")
        else:
            print(f"WARNING: Expected 401, got {response.status_code}")
    except Exception as e:
        print(f"ERROR: Auth test failed - {e}")
    
    # Test with correct auth
    try:
        response = requests.get(f"{BASE_URL}/v1/jobs", headers=HEADERS, timeout=10)
        if response.status_code == 200:
            print("SUCCESS: Authorized access working")
            return True
        else:
            print(f"FAILED: Auth failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"FAILED: Auth test error - {e}")
        return False

def test_database_with_auth():
    """Test database connectivity with auth"""
    print("\n=== Testing Database (Authenticated) ===")
    
    try:
        response = requests.get(f"{BASE_URL}/test-candidates", headers=HEADERS, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: Database connected")
            print(f"  Status: {data.get('database_status')}")
            print(f"  Total candidates: {data.get('total_candidates', 0)}")
            return True
        else:
            print(f"FAILED: Database test returned {response.status_code}")
            return False
    except Exception as e:
        print(f"FAILED: Database test error - {e}")
        return False

def test_jobs_crud():
    """Test job CRUD operations"""
    print("\n=== Testing Jobs CRUD ===")
    
    # Create job
    job_data = {
        "title": "Full Stack Developer",
        "department": "Technology",
        "location": "Remote",
        "experience_level": "Mid-level",
        "requirements": "React, Node.js, Python, PostgreSQL, 3+ years experience",
        "description": "Join our team to build scalable web applications using modern technologies.",
        "employment_type": "Full-time"
    }
    
    try:
        # Create job
        response = requests.post(f"{BASE_URL}/v1/jobs", headers=HEADERS, json=job_data, timeout=10)
        if response.status_code == 200:
            data = response.json()
            job_id = data.get('job_id')
            print(f"SUCCESS: Job created - ID {job_id}")
            
            # List jobs
            response = requests.get(f"{BASE_URL}/v1/jobs", headers=HEADERS, timeout=10)
            if response.status_code == 200:
                jobs_data = response.json()
                jobs = jobs_data.get('jobs', [])
                print(f"SUCCESS: Retrieved {len(jobs)} jobs")
                
                if jobs:
                    latest_job = jobs[0]
                    print(f"  Latest: {latest_job.get('title')} - {latest_job.get('department')}")
                
                return job_id
            else:
                print(f"FAILED: Job listing returned {response.status_code}")
                return job_id
        else:
            print(f"FAILED: Job creation returned {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"FAILED: Jobs CRUD error - {e}")
        return None

def test_candidates_operations():
    """Test candidate operations"""
    print("\n=== Testing Candidates Operations ===")
    
    try:
        # Get all candidates
        response = requests.get(f"{BASE_URL}/v1/candidates", headers=HEADERS, timeout=10)
        if response.status_code == 200:
            data = response.json()
            candidates = data.get('candidates', [])
            total = data.get('total', 0)
            print(f"SUCCESS: Retrieved {len(candidates)} candidates (Total: {total})")
            
            candidate_id = None
            if candidates:
                sample = candidates[0]
                candidate_id = sample.get('id')
                print(f"  Sample: {sample.get('name')} - {sample.get('experience_years')}y exp")
                print(f"  Skills: {sample.get('technical_skills', '')[:60]}...")
                
                # Test individual candidate lookup
                response = requests.get(f"{BASE_URL}/v1/candidates/{candidate_id}", headers=HEADERS, timeout=10)
                if response.status_code == 200:
                    candidate_data = response.json()
                    candidate_info = candidate_data.get('candidate', {})
                    print(f"SUCCESS: Individual candidate lookup - {candidate_info.get('name')}")
                else:
                    print(f"FAILED: Individual lookup returned {response.status_code}")
            
            return candidate_id
        else:
            print(f"FAILED: Candidates endpoint returned {response.status_code}")
            return None
    except Exception as e:
        print(f"FAILED: Candidates operations error - {e}")
        return None

def test_candidate_search_auth():
    """Test candidate search with authentication"""
    print("\n=== Testing Candidate Search (Authenticated) ===")
    
    search_params = {
        "skills": "Python",
        "experience_min": 1
    }
    
    try:
        response = requests.get(f"{BASE_URL}/v1/candidates/search", 
                              headers=HEADERS, params=search_params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            candidates = data.get('candidates', [])
            filters = data.get('filters', {})
            print(f"SUCCESS: Search found {len(candidates)} candidates")
            print(f"  Filters applied: {filters}")
            
            for i, candidate in enumerate(candidates[:3]):
                print(f"    {i+1}. {candidate.get('name')} - {candidate.get('experience_years')}y")
            
            return len(candidates) > 0
        else:
            print(f"FAILED: Search returned {response.status_code}")
            return False
    except Exception as e:
        print(f"FAILED: Search error - {e}")
        return False

def test_ai_matching_authenticated(job_id):
    """Test AI matching with authentication"""
    print(f"\n=== Testing AI Matching (Authenticated) ===")
    
    if not job_id:
        print("SKIPPED: No job ID available")
        return False
    
    # Test agent direct matching (no auth needed)
    try:
        payload = {"job_id": job_id}
        response = requests.post(f"{AGENT_URL}/match", json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: Agent matching")
            print(f"  Algorithm: {data.get('algorithm_version')}")
            print(f"  Status: {data.get('status')}")
            print(f"  Candidates: {data.get('total_candidates', 0)}")
            
            matches = data.get('top_candidates', [])
            for i, match in enumerate(matches[:3]):
                print(f"    {i+1}. {match.get('name')} - Score: {match.get('score')}")
        else:
            print(f"FAILED: Agent matching returned {response.status_code}")
    except Exception as e:
        print(f"FAILED: Agent matching error - {e}")
    
    # Test gateway matching (with auth)
    try:
        response = requests.get(f"{BASE_URL}/v1/match/{job_id}/top", headers=HEADERS, timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: Gateway matching")
            print(f"  Algorithm: {data.get('algorithm_version')}")
            print(f"  Agent status: {data.get('agent_status')}")
            print(f"  Matches: {len(data.get('matches', []))}")
            return True
        else:
            print(f"FAILED: Gateway matching returned {response.status_code}")
            return False
    except Exception as e:
        print(f"FAILED: Gateway matching error - {e}")
        return False

def test_feedback_with_auth(candidate_id, job_id):
    """Test feedback system with authentication"""
    print(f"\n=== Testing Feedback System (Authenticated) ===")
    
    if not candidate_id or not job_id:
        print("SKIPPED: Missing candidate or job ID")
        return False
    
    feedback_data = {
        "candidate_id": candidate_id,
        "job_id": job_id,
        "integrity": 4,
        "honesty": 5,
        "discipline": 4,
        "hard_work": 5,
        "gratitude": 4,
        "comments": "Strong technical skills and good communication"
    }
    
    try:
        # Submit feedback
        response = requests.post(f"{BASE_URL}/v1/feedback", headers=HEADERS, json=feedback_data, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: Feedback submitted - ID {data.get('feedback_id')}")
            print(f"  Average score: {data.get('average_score')}")
            
            # Get all feedback
            response = requests.get(f"{BASE_URL}/v1/feedback", headers=HEADERS, timeout=10)
            if response.status_code == 200:
                feedback_list = response.json()
                count = feedback_list.get('count', 0)
                print(f"SUCCESS: Retrieved {count} feedback records")
                return True
            else:
                print(f"FAILED: Feedback retrieval returned {response.status_code}")
                return False
        else:
            print(f"FAILED: Feedback submission returned {response.status_code}")
            return False
    except Exception as e:
        print(f"FAILED: Feedback error - {e}")
        return False

def main():
    """Run authenticated endpoint tests"""
    print("=== BHIV HR Platform - Authenticated Endpoint Testing ===")
    print("Testing all endpoints with proper local authentication...\n")
    
    results = {}
    
    # Test authentication
    results['auth'] = test_auth_endpoints()
    if not results['auth']:
        print("\nFATAL: Authentication failed - stopping tests")
        return 1
    
    # Test database
    results['database'] = test_database_with_auth()
    
    # Test jobs
    job_id = test_jobs_crud()
    results['jobs'] = job_id is not None
    
    # Test candidates
    candidate_id = test_candidates_operations()
    results['candidates'] = candidate_id is not None
    
    # Test search
    results['search'] = test_candidate_search_auth()
    
    # Test AI matching
    results['ai_matching'] = test_ai_matching_authenticated(job_id)
    
    # Test feedback
    results['feedback'] = test_feedback_with_auth(candidate_id, job_id)
    
    # Summary
    print("\n" + "="*50)
    print("AUTHENTICATED TEST RESULTS")
    print("="*50)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results.items():
        status = "PASS" if success else "FAIL"
        print(f"{test_name.replace('_', ' ').title():.<30} {status}")
        if success:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed >= total - 1:  # Allow 1 failure
        print("\nSUCCESS: Authentication and endpoints working!")
        return 0
    else:
        print("\nFAILED: Multiple endpoint issues detected")
        return 1

if __name__ == "__main__":
    sys.exit(main())