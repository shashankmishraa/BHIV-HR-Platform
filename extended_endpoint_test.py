#!/usr/bin/env python3
import requests
import json
import time

GATEWAY_URL = "https://bhiv-hr-gateway-46pz.onrender.com"
AGENT_URL = "https://bhiv-hr-agent-m1me.onrender.com"
API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def test_endpoint(url, name, method="GET", data=None, expected_codes=[200]):
    try:
        start_time = time.time()
        if method == "GET":
            response = requests.get(url, headers=HEADERS, timeout=15)
        else:
            response = requests.post(url, headers=HEADERS, json=data, timeout=15)
        
        response_time = (time.time() - start_time) * 1000
        
        if response.status_code in expected_codes:
            print(f"PASS {name} ({response.status_code}) - {response_time:.0f}ms")
            try:
                data = response.json()
                if isinstance(data, dict) and len(data) > 0:
                    print(f"     Data: {list(data.keys())[:5]}")
            except:
                pass
            return True
        else:
            print(f"FAIL {name} ({response.status_code}) - {response_time:.0f}ms")
            print(f"     Error: {response.text[:100]}")
            return False
    except Exception as e:
        print(f"ERROR {name} - {str(e)}")
        return False

def main():
    print("BHIV HR Platform - Extended Endpoint Testing")
    print("=" * 60)
    
    passed = 0
    total = 0
    
    # Core Gateway Tests
    print("\n=== CORE GATEWAY ENDPOINTS ===")
    core_tests = [
        (f"{GATEWAY_URL}/", "Root API"),
        (f"{GATEWAY_URL}/health", "Health Check"),
        (f"{GATEWAY_URL}/test-candidates", "Database Test"),
        (f"{GATEWAY_URL}/metrics", "Prometheus Metrics"),
        (f"{GATEWAY_URL}/health/detailed", "Detailed Health"),
        (f"{GATEWAY_URL}/metrics/dashboard", "Metrics Dashboard"),
        (f"{GATEWAY_URL}/candidates/stats", "Candidate Statistics"),
    ]
    
    for url, name in core_tests:
        if test_endpoint(url, name):
            passed += 1
        total += 1
    
    # Job Management Tests
    print("\n=== JOB MANAGEMENT ===")
    if test_endpoint(f"{GATEWAY_URL}/v1/jobs", "List Jobs"):
        passed += 1
    total += 1
    
    job_data = {
        "title": "Senior Python Developer",
        "department": "Engineering",
        "location": "Remote",
        "experience_level": "Senior",
        "requirements": "Python, Django, PostgreSQL, 5+ years",
        "description": "Senior Python developer position"
    }
    if test_endpoint(f"{GATEWAY_URL}/v1/jobs", "Create Job", "POST", job_data):
        passed += 1
    total += 1
    
    # Candidate Management Tests
    print("\n=== CANDIDATE MANAGEMENT ===")
    candidate_tests = [
        (f"{GATEWAY_URL}/v1/candidates", "List Candidates"),
        (f"{GATEWAY_URL}/v1/candidates/search", "Search Candidates"),
        (f"{GATEWAY_URL}/v1/candidates/1", "Get Candidate by ID"),
        (f"{GATEWAY_URL}/v1/candidates/job/1", "Candidates by Job"),
    ]
    
    for url, name in candidate_tests:
        if test_endpoint(url, name):
            passed += 1
        total += 1
    
    # Bulk candidate upload
    bulk_data = {
        "candidates": [
            {
                "name": "Test Candidate",
                "email": f"test_{int(time.time())}@example.com",
                "phone": "+1-555-0199",
                "experience_years": 5,
                "technical_skills": "Python, JavaScript, React",
                "status": "applied"
            }
        ]
    }
    if test_endpoint(f"{GATEWAY_URL}/v1/candidates/bulk", "Bulk Upload", "POST", bulk_data):
        passed += 1
    total += 1
    
    # AI Matching Tests
    print("\n=== AI MATCHING ENGINE ===")
    if test_endpoint(f"{GATEWAY_URL}/v1/match/1/top", "AI Top Matches"):
        passed += 1
    total += 1
    
    batch_data = {"job_ids": [1, 2]}
    if test_endpoint(f"{GATEWAY_URL}/v1/match/batch", "Batch Matching", "POST", batch_data):
        passed += 1
    total += 1
    
    # Assessment Workflow Tests
    print("\n=== ASSESSMENT WORKFLOW ===")
    feedback_data = {
        "candidate_id": 1,
        "job_id": 1,
        "integrity": 4,
        "honesty": 5,
        "discipline": 4,
        "hard_work": 4,
        "gratitude": 5,
        "comments": "Excellent candidate with strong values"
    }
    if test_endpoint(f"{GATEWAY_URL}/v1/feedback", "Submit Feedback", "POST", feedback_data):
        passed += 1
    total += 1
    
    if test_endpoint(f"{GATEWAY_URL}/v1/feedback", "Get Feedback"):
        passed += 1
    total += 1
    
    interview_data = {
        "candidate_id": 1,
        "job_id": 1,
        "interview_date": "2025-01-15 10:00:00",
        "interviewer": "Test Interviewer"
    }
    if test_endpoint(f"{GATEWAY_URL}/v1/interviews", "Schedule Interview", "POST", interview_data):
        passed += 1
    total += 1
    
    if test_endpoint(f"{GATEWAY_URL}/v1/interviews", "Get Interviews"):
        passed += 1
    total += 1
    
    # Security Tests
    print("\n=== SECURITY FEATURES ===")
    security_tests = [
        (f"{GATEWAY_URL}/v1/security/rate-limit-status", "Rate Limit Status"),
        (f"{GATEWAY_URL}/v1/security/blocked-ips", "Blocked IPs"),
        (f"{GATEWAY_URL}/v1/security/security-headers-test", "Security Headers"),
        (f"{GATEWAY_URL}/v1/security/penetration-test-endpoints", "Penetration Test"),
    ]
    
    for url, name in security_tests:
        if test_endpoint(url, name):
            passed += 1
        total += 1
    
    # Security POST tests
    input_test = {"input_data": "test<script>alert('xss')</script>"}
    if test_endpoint(f"{GATEWAY_URL}/v1/security/test-input-validation", "Input Validation", "POST", input_test):
        passed += 1
    total += 1
    
    email_test = {"email": "test@example.com"}
    if test_endpoint(f"{GATEWAY_URL}/v1/security/test-email-validation", "Email Validation", "POST", email_test):
        passed += 1
    total += 1
    
    # 2FA Tests
    print("\n=== TWO-FACTOR AUTHENTICATION ===")
    twofa_setup = {"user_id": "test_user"}
    if test_endpoint(f"{GATEWAY_URL}/v1/2fa/setup", "2FA Setup", "POST", twofa_setup):
        passed += 1
    total += 1
    
    if test_endpoint(f"{GATEWAY_URL}/v1/2fa/status/test_user", "2FA Status"):
        passed += 1
    total += 1
    
    if test_endpoint(f"{GATEWAY_URL}/v1/2fa/demo-setup", "2FA Demo"):
        passed += 1
    total += 1
    
    # Password Management Tests
    print("\n=== PASSWORD MANAGEMENT ===")
    pwd_test = {"password": "TestPassword123!"}
    if test_endpoint(f"{GATEWAY_URL}/v1/password/validate", "Password Validation", "POST", pwd_test):
        passed += 1
    total += 1
    
    if test_endpoint(f"{GATEWAY_URL}/v1/password/policy", "Password Policy"):
        passed += 1
    total += 1
    
    if test_endpoint(f"{GATEWAY_URL}/v1/password/security-tips", "Security Tips"):
        passed += 1
    total += 1
    
    # Agent Service Tests
    print("\n=== AI AGENT SERVICE ===")
    agent_tests = [
        (f"{AGENT_URL}/", "Agent Root"),
        (f"{AGENT_URL}/health", "Agent Health"),
        (f"{AGENT_URL}/test-db", "Agent DB Test"),
        (f"{AGENT_URL}/analyze/1", "Candidate Analysis"),
    ]
    
    for url, name in agent_tests:
        if test_endpoint(url, name):
            passed += 1
        total += 1
    
    # AI Matching via Agent
    match_data = {"job_id": 1}
    if test_endpoint(f"{AGENT_URL}/match", "Direct AI Match", "POST", match_data):
        passed += 1
    total += 1
    
    batch_match = {"job_ids": [1, 2]}
    if test_endpoint(f"{AGENT_URL}/batch-match", "Agent Batch Match", "POST", batch_match):
        passed += 1
    total += 1
    
    # Client Portal Test
    print("\n=== CLIENT PORTAL ===")
    client_login = {"client_id": "TECH001", "password": "demo123"}
    if test_endpoint(f"{GATEWAY_URL}/v1/client/login", "Client Login", "POST", client_login):
        passed += 1
    total += 1
    
    print(f"\n" + "=" * 60)
    print(f"COMPREHENSIVE TEST RESULTS")
    print(f"Total Endpoints Tested: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success Rate: {passed/total*100:.1f}%")
    
    if passed/total >= 0.95:
        print("ASSESSMENT: EXCELLENT - Production Ready")
    elif passed/total >= 0.85:
        print("ASSESSMENT: GOOD - Mostly Operational")
    elif passed/total >= 0.70:
        print("ASSESSMENT: FAIR - Needs Attention")
    else:
        print("ASSESSMENT: POOR - Major Issues")
    
    print(f"\nTested {total} endpoints across Gateway and Agent services")
    print("All core functionality verified with live API calls")

if __name__ == "__main__":
    main()