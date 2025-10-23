#!/usr/bin/env python3
"""
HR Portal Integration Testing
Tests all key functions and database/API integrations
"""

import requests
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
GATEWAY_URL = "https://bhiv-hr-gateway-46pz.onrender.com"
HR_PORTAL_URL = "https://bhiv-hr-portal-cead.onrender.com"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def test_hr_portal_accessibility():
    """Test HR Portal basic accessibility"""
    logger.info("=== HR PORTAL ACCESSIBILITY TEST ===")
    try:
        response = requests.get(HR_PORTAL_URL, timeout=30)
        if response.status_code == 200:
            logger.info("✅ HR Portal accessible")
            if "streamlit" in response.text.lower():
                logger.info("✅ Streamlit framework detected")
            if "bhiv" in response.text.lower():
                logger.info("✅ BHIV branding detected")
            return True
        else:
            logger.error(f"❌ HR Portal HTTP {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ HR Portal not accessible: {e}")
        return False

def test_gateway_integration():
    """Test HR Portal's Gateway API integration"""
    logger.info("=== GATEWAY INTEGRATION TEST ===")
    
    # Test endpoints that HR Portal uses
    endpoints = [
        ("/health", "Gateway Health"),
        ("/v1/candidates", "Candidates Data"),
        ("/v1/jobs", "Jobs Data"),
        ("/v1/interviews", "Interviews Data"),
        ("/test-candidates", "Test Candidates")
    ]
    
    success_count = 0
    for endpoint, description in endpoints:
        try:
            response = requests.get(f"{GATEWAY_URL}{endpoint}", headers=HEADERS, timeout=15)
            if response.status_code == 200:
                data = response.json()
                if endpoint == "/v1/candidates":
                    logger.info(f"✅ {description}: {len(data)} candidates")
                elif endpoint == "/v1/jobs":
                    jobs = data.get('jobs', []) if isinstance(data, dict) else data
                    logger.info(f"✅ {description}: {len(jobs)} jobs")
                elif endpoint == "/test-candidates":
                    logger.info(f"✅ {description}: {data.get('total_candidates', 0)} total")
                else:
                    logger.info(f"✅ {description}: OK")
                success_count += 1
            else:
                logger.error(f"❌ {description}: HTTP {response.status_code}")
        except Exception as e:
            logger.error(f"❌ {description}: {e}")
    
    logger.info(f"Gateway Integration: {success_count}/{len(endpoints)} endpoints working")
    return success_count == len(endpoints)

def test_job_creation_function():
    """Test job creation functionality"""
    logger.info("=== JOB CREATION TEST ===")
    
    job_data = {
        "title": "Test HR Portal Job",
        "department": "Engineering",
        "location": "Remote",
        "experience_level": "Mid",
        "requirements": "Test requirements for HR portal integration",
        "description": "Test job created via HR portal integration test",
        "client_id": "TECH001",
        "employment_type": "Full-time"
    }
    
    try:
        response = requests.post(f"{GATEWAY_URL}/v1/jobs", json=job_data, headers=HEADERS, timeout=15)
        if response.status_code == 200:
            result = response.json()
            job_id = result.get("job_id", "Unknown")
            logger.info(f"✅ Job Creation: Job {job_id} created successfully")
            return True, job_id
        else:
            logger.error(f"❌ Job Creation: HTTP {response.status_code} - {response.text}")
            return False, None
    except Exception as e:
        logger.error(f"❌ Job Creation: {e}")
        return False, None

def test_candidate_search_function():
    """Test candidate search functionality"""
    logger.info("=== CANDIDATE SEARCH TEST ===")
    
    search_params = {
        "job_id": 1,
        "q": "python",
        "experience_min": 2
    }
    
    try:
        response = requests.get(f"{GATEWAY_URL}/v1/candidates/search", 
                              params=search_params, headers=HEADERS, timeout=15)
        if response.status_code == 200:
            data = response.json()
            candidates = data.get("candidates", [])
            count = data.get("count", 0)
            logger.info(f"✅ Candidate Search: Found {count} candidates")
            if candidates:
                logger.info(f"✅ Sample candidate: {candidates[0].get('name', 'Unknown')}")
            return True
        else:
            logger.error(f"❌ Candidate Search: HTTP {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Candidate Search: {e}")
        return False

def test_interview_scheduling():
    """Test interview scheduling functionality"""
    logger.info("=== INTERVIEW SCHEDULING TEST ===")
    
    interview_data = {
        "candidate_id": 1,
        "job_id": 1,
        "interview_date": "2025-10-25 14:00:00",
        "interviewer": "HR Portal Test",
        "notes": "Test interview scheduled via HR portal"
    }
    
    try:
        response = requests.post(f"{GATEWAY_URL}/v1/interviews", 
                               json=interview_data, headers=HEADERS, timeout=15)
        if response.status_code == 200:
            result = response.json()
            logger.info(f"✅ Interview Scheduling: Interview scheduled successfully")
            return True
        else:
            logger.error(f"❌ Interview Scheduling: HTTP {response.status_code} - {response.text}")
            return False
    except Exception as e:
        logger.error(f"❌ Interview Scheduling: {e}")
        return False

def test_bulk_candidate_upload():
    """Test bulk candidate upload functionality"""
    logger.info("=== BULK CANDIDATE UPLOAD TEST ===")
    
    candidates_data = {
        "candidates": [
            {
                "name": "HR Portal Test Candidate",
                "email": "hrtest@example.com",
                "phone": "+1-555-0199",
                "experience_years": 3,
                "status": "applied",
                "job_id": 1,
                "location": "Remote",
                "technical_skills": "Python, JavaScript, Testing",
                "designation": "Software Developer",
                "education_level": "Bachelors"
            }
        ]
    }
    
    try:
        response = requests.post(f"{GATEWAY_URL}/v1/candidates/bulk", 
                               json=candidates_data, headers=HEADERS, timeout=15)
        if response.status_code == 200:
            result = response.json()
            logger.info(f"✅ Bulk Upload: {len(candidates_data['candidates'])} candidates uploaded")
            return True
        else:
            logger.error(f"❌ Bulk Upload: HTTP {response.status_code} - {response.text}")
            return False
    except Exception as e:
        logger.error(f"❌ Bulk Upload: {e}")
        return False

def test_ai_matching_integration():
    """Test AI matching integration"""
    logger.info("=== AI MATCHING INTEGRATION TEST ===")
    
    try:
        # Test Gateway AI endpoint
        response = requests.get(f"{GATEWAY_URL}/v1/match/1/top", headers=HEADERS, timeout=20)
        if response.status_code == 200:
            data = response.json()
            candidates = data.get("candidates", [])
            logger.info(f"✅ AI Matching (Gateway): {len(candidates)} candidates matched")
            return True
        else:
            logger.warning(f"⚠️ AI Matching (Gateway): HTTP {response.status_code}")
            
        # Test direct Agent service
        agent_url = "https://bhiv-hr-agent-m1me.onrender.com"
        response = requests.post(f"{agent_url}/match", json={"job_id": 1}, timeout=20)
        if response.status_code == 200:
            data = response.json()
            candidates = data.get("top_candidates", [])
            logger.info(f"✅ AI Matching (Agent): {len(candidates)} candidates matched")
            return True
        else:
            logger.warning(f"⚠️ AI Matching (Agent): HTTP {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ AI Matching: {e}")
        return False

def test_values_assessment():
    """Test values assessment functionality"""
    logger.info("=== VALUES ASSESSMENT TEST ===")
    
    feedback_data = {
        "candidate_id": 1,
        "job_id": 1,
        "integrity": 4,
        "honesty": 5,
        "discipline": 4,
        "hard_work": 4,
        "gratitude": 5,
        "comments": "HR Portal integration test feedback",
        "reviewer_name": "HR Portal Test"
    }
    
    try:
        response = requests.post(f"{GATEWAY_URL}/v1/feedback", 
                               json=feedback_data, headers=HEADERS, timeout=15)
        if response.status_code == 200:
            result = response.json()
            logger.info(f"✅ Values Assessment: Feedback submitted successfully")
            return True
        else:
            logger.error(f"❌ Values Assessment: HTTP {response.status_code} - {response.text}")
            return False
    except Exception as e:
        logger.error(f"❌ Values Assessment: {e}")
        return False

def test_export_functionality():
    """Test export functionality"""
    logger.info("=== EXPORT FUNCTIONALITY TEST ===")
    
    try:
        # Test job export
        response = requests.get(f"{GATEWAY_URL}/v1/reports/job/1/export.csv", 
                              headers=HEADERS, timeout=15)
        if response.status_code == 200:
            logger.info(f"✅ Export: Job report exported ({len(response.content)} bytes)")
            return True
        else:
            logger.warning(f"⚠️ Export: HTTP {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Export: {e}")
        return False

def main():
    """Main HR Portal integration test"""
    logger.info("🚀 Starting HR Portal Integration Testing...")
    
    tests = [
        ("Portal Accessibility", test_hr_portal_accessibility),
        ("Gateway Integration", test_gateway_integration),
        ("Job Creation", test_job_creation_function),
        ("Candidate Search", test_candidate_search_function),
        ("Interview Scheduling", test_interview_scheduling),
        ("Bulk Upload", test_bulk_candidate_upload),
        ("AI Matching", test_ai_matching_integration),
        ("Values Assessment", test_values_assessment),
        ("Export Functionality", test_export_functionality)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\n--- Testing {test_name} ---")
        try:
            if test_func():
                passed += 1
                logger.info(f"✅ {test_name}: PASSED")
            else:
                logger.error(f"❌ {test_name}: FAILED")
        except Exception as e:
            logger.error(f"❌ {test_name}: ERROR - {e}")
    
    logger.info(f"\n=== HR PORTAL TEST SUMMARY ===")
    logger.info(f"Tests Passed: {passed}/{total}")
    logger.info(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed >= total * 0.8:
        logger.info("✅ HR Portal integration is WORKING WELL")
    else:
        logger.warning("⚠️ HR Portal has integration issues")

if __name__ == "__main__":
    main()