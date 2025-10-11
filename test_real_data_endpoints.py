#!/usr/bin/env python3
"""
Test all endpoints with real data and proper authentication
"""
import requests
import json
import sys
import time

# Configuration
BASE_URL = "http://localhost:8000"
AGENT_URL = "http://localhost:9000"
API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def test_database_setup():
    """Test database connectivity and data"""
    print("=== Testing Database Setup ===")
    
    try:
        response = requests.get(f"{BASE_URL}/test-candidates", headers=HEADERS, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: Database connected")
            print(f"  Total candidates: {data.get('total_candidates', 0)}")
            return True
        else:
            print(f"FAILED: Database test returned {response.status_code}")
            return False
    except Exception as e:
        print(f"FAILED: Database test error - {e}")
        return False

def create_real_job():
    """Create a real job posting"""
    print("\n=== Creating Real Job ===")
    
    job_data = {
        "title": "Senior Python Developer",
        "department": "Engineering",
        "location": "San Francisco, CA",
        "experience_level": "Senior",
        "requirements": "Python, FastAPI, PostgreSQL, Docker, 5+ years experience, machine learning, REST APIs",
        "description": "We are looking for a Senior Python Developer to join our AI team. You will work on building scalable backend services using FastAPI, implement machine learning algorithms, and work with large datasets. Experience with Docker, PostgreSQL, and cloud platforms is required.",
        "employment_type": "Full-time"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/v1/jobs", headers=HEADERS, json=job_data, timeout=10)
        if response.status_code == 200:
            data = response.json()
            job_id = data.get('job_id')
            print(f"SUCCESS: Job created with ID {job_id}")
            print(f"  Title: {job_data['title']}")
            print(f"  Department: {job_data['department']}")
            return job_id
        else:
            print(f"FAILED: Job creation returned {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"FAILED: Job creation error - {e}")
        return None

def test_jobs_endpoint():
    """Test jobs listing endpoint"""
    print("\n=== Testing Jobs Endpoint ===")
    
    try:
        response = requests.get(f"{BASE_URL}/v1/jobs", headers=HEADERS, timeout=10)
        if response.status_code == 200:
            data = response.json()
            jobs = data.get('jobs', [])
            print(f"SUCCESS: Retrieved {len(jobs)} jobs")
            
            if jobs:
                latest_job = jobs[0]
                print(f"  Latest job: {latest_job.get('title')}")
                print(f"  Department: {latest_job.get('department')}")
                print(f"  Location: {latest_job.get('location')}")
                return latest_job.get('id')
            return None
        else:
            print(f"FAILED: Jobs endpoint returned {response.status_code}")
            return None
    except Exception as e:
        print(f"FAILED: Jobs endpoint error - {e}")
        return None

def test_candidates_endpoint():
    """Test candidates endpoint"""
    print("\n=== Testing Candidates Endpoint ===")
    
    try:
        response = requests.get(f"{BASE_URL}/v1/candidates", headers=HEADERS, timeout=10)
        if response.status_code == 200:
            data = response.json()
            candidates = data.get('candidates', [])
            total = data.get('total', 0)
            print(f"SUCCESS: Retrieved {len(candidates)} candidates (Total: {total})")
            
            if candidates:
                sample_candidate = candidates[0]
                print(f"  Sample candidate: {sample_candidate.get('name')}")
                print(f"  Skills: {sample_candidate.get('technical_skills', '')[:50]}...")
                print(f"  Experience: {sample_candidate.get('experience_years')} years")
                return sample_candidate.get('id')
            return None
        else:
            print(f"FAILED: Candidates endpoint returned {response.status_code}")
            return None
    except Exception as e:
        print(f"FAILED: Candidates endpoint error - {e}")
        return None

def test_candidate_search():
    """Test candidate search with real parameters"""
    print("\n=== Testing Candidate Search ===")
    
    search_params = {
        "skills": "Python",
        "location": "India",
        "experience_min": 2
    }
    
    try:
        response = requests.get(f"{BASE_URL}/v1/candidates/search", 
                              headers=HEADERS, params=search_params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            candidates = data.get('candidates', [])
            print(f"SUCCESS: Search found {len(candidates)} candidates")
            print(f"  Search filters: {data.get('filters')}")
            
            if candidates:
                for i, candidate in enumerate(candidates[:3]):
                    print(f"  {i+1}. {candidate.get('name')} - {candidate.get('experience_years')}y exp")
            return len(candidates) > 0
        else:
            print(f"FAILED: Search returned {response.status_code}")
            return False
    except Exception as e:
        print(f"FAILED: Search error - {e}")
        return False

def test_ai_matching_real(job_id):
    """Test AI matching with real job"""
    print(f"\n=== Testing AI Matching (Job ID: {job_id}) ===")
    
    if not job_id:
        print("SKIPPED: No job ID available")
        return False
    
    # Test direct agent matching
    try:
        payload = {"job_id": job_id}
        response = requests.post(f"{AGENT_URL}/match", json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: Agent AI matching")
            print(f"  Algorithm: {data.get('algorithm_version')}")
            print(f"  Status: {data.get('status')}")
            print(f"  Total candidates: {data.get('total_candidates', 0)}")
            print(f"  Top matches: {len(data.get('top_candidates', []))}")
            
            # Show top matches
            top_candidates = data.get('top_candidates', [])
            for i, candidate in enumerate(top_candidates[:3]):
                print(f"    {i+1}. {candidate.get('name')} - Score: {candidate.get('score')}")
                print(f"       Skills: {', '.join(candidate.get('skills_match', []))}")
            
            return len(top_candidates) > 0
        else:
            print(f"FAILED: Agent matching returned {response.status_code}")
            return False
    except Exception as e:
        print(f"FAILED: Agent matching error - {e}")
        return False

def test_gateway_ai_matching(job_id):
    """Test AI matching via gateway"""
    print(f"\n=== Testing Gateway AI Matching (Job ID: {job_id}) ===")
    
    if not job_id:
        print("SKIPPED: No job ID available")
        return False
    
    try:
        response = requests.get(f"{BASE_URL}/v1/match/{job_id}/top", headers=HEADERS, timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: Gateway AI matching")
            print(f"  Algorithm: {data.get('algorithm_version')}")
            print(f"  Agent status: {data.get('agent_status')}")
            print(f"  Matches found: {len(data.get('matches', []))}")
            
            # Show matches
            matches = data.get('matches', [])
            for i, match in enumerate(matches[:3]):
                print(f"    {i+1}. {match.get('name')} - Score: {match.get('score')}")
                print(f"       Reasoning: {match.get('reasoning', '')[:60]}...")
            
            return len(matches) > 0
        else:
            print(f"FAILED: Gateway matching returned {response.status_code}")
            return False
    except Exception as e:
        print(f"FAILED: Gateway matching error - {e}")
        return False

def test_feedback_system(candidate_id, job_id):
    """Test feedback submission with real data"""
    print(f"\n=== Testing Feedback System ===")
    
    if not candidate_id or not job_id:
        print("SKIPPED: Missing candidate or job ID")
        return False
    
    feedback_data = {
        "candidate_id": candidate_id,
        "job_id": job_id,
        "integrity": 5,
        "honesty": 4,
        "discipline": 5,
        "hard_work": 4,
        "gratitude": 5,
        "comments": "Excellent candidate with strong technical skills and great attitude"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/v1/feedback", headers=HEADERS, json=feedback_data, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: Feedback submitted")
            print(f"  Feedback ID: {data.get('feedback_id')}")
            print(f"  Average score: {data.get('average_score')}")
            print(f"  Values scores: {data.get('values_scores')}")
            return True
        else:
            print(f"FAILED: Feedback submission returned {response.status_code}")
            return False
    except Exception as e:
        print(f"FAILED: Feedback submission error - {e}")
        return False

def test_batch_matching():
    """Test batch AI matching"""
    print(f"\n=== Testing Batch AI Matching ===")
    
    try:
        # Get available job IDs first
        jobs_response = requests.get(f"{BASE_URL}/v1/jobs", headers=HEADERS, timeout=10)
        if jobs_response.status_code != 200:
            print("SKIPPED: Cannot get jobs for batch matching")
            return False
        
        jobs = jobs_response.json().get('jobs', [])
        if len(jobs) < 2:
            print("SKIPPED: Need at least 2 jobs for batch matching")
            return False
        
        job_ids = [job['id'] for job in jobs[:2]]
        payload = {"job_ids": job_ids}
        
        response = requests.post(f"{AGENT_URL}/batch-match", json=payload, timeout=60)
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: Batch matching completed")
            print(f"  Jobs processed: {data.get('total_jobs_processed', 0)}")
            print(f"  Candidates analyzed: {data.get('total_candidates_analyzed', 0)}")
            print(f"  Algorithm: {data.get('algorithm_version')}")
            
            batch_results = data.get('batch_results', {})
            for job_id, result in batch_results.items():
                print(f"    Job {job_id}: {len(result.get('top_matches', []))} matches")
            
            return True
        else:
            print(f"FAILED: Batch matching returned {response.status_code}")
            return False
    except Exception as e:
        print(f"FAILED: Batch matching error - {e}")
        return False

def main():
    """Run comprehensive real data tests"""
    print("=== BHIV HR Platform - Real Data Endpoint Testing ===")
    print("Testing all endpoints with authentic data and proper authentication...\n")
    
    results = {}
    
    # Test database setup
    results['database'] = test_database_setup()
    
    # Test job creation and listing
    job_id = create_real_job()
    if not job_id:
        job_id = test_jobs_endpoint()
    results['jobs'] = job_id is not None
    
    # Test candidates
    candidate_id = test_candidates_endpoint()
    results['candidates'] = candidate_id is not None
    
    # Test candidate search
    results['search'] = test_candidate_search()
    
    # Test AI matching
    results['agent_matching'] = test_ai_matching_real(job_id)
    results['gateway_matching'] = test_gateway_ai_matching(job_id)
    
    # Test feedback system
    results['feedback'] = test_feedback_system(candidate_id, job_id)
    
    # Test batch matching
    results['batch_matching'] = test_batch_matching()
    
    # Summary
    print("\n" + "="*60)
    print("COMPREHENSIVE TEST RESULTS")
    print("="*60)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results.items():
        status = "PASS" if success else "FAIL"
        print(f"{test_name.replace('_', ' ').title():.<40} {status}")
        if success:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Clean architecture with real data working perfectly")
        print("✅ Phase 3 AI engine operational")
        print("✅ All endpoints functional with authentication")
        return 0
    else:
        print(f"\n⚠️  {total - passed} tests failed")
        print("❌ Some functionality needs attention")
        return 1

if __name__ == "__main__":
    sys.exit(main())