#!/usr/bin/env python3
"""
Comprehensive Gateway Service Verification
"""

import requests
import json
from datetime import datetime

GATEWAY_URL = "https://bhiv-hr-gateway-46pz.onrender.com"
API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def test_endpoint(name, method, url, data=None, timeout=15):
    """Test individual endpoint"""
    try:
        if method == "GET":
            response = requests.get(url, headers=HEADERS, timeout=timeout)
        elif method == "POST":
            response = requests.post(url, headers=HEADERS, json=data, timeout=timeout)
        
        if response.status_code in [200, 201]:
            print(f"PASS: {name}")
            return True, response.json() if response.content else {}
        else:
            print(f"FAIL: {name} ({response.status_code})")
            return False, response.text
            
    except Exception as e:
        print(f"ERROR: {name} - {str(e)}")
        return False, str(e)

def main():
    print("BHIV HR Platform - Gateway Service Verification")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    passed = 0
    total = 0
    
    # Core API Tests
    print("=== CORE API ENDPOINTS ===")
    core_tests = [
        ("Gateway Root", "GET", f"{GATEWAY_URL}/"),
        ("Health Check", "GET", f"{GATEWAY_URL}/health"),
        ("Test Candidates DB", "GET", f"{GATEWAY_URL}/test-candidates"),
        ("Prometheus Metrics", "GET", f"{GATEWAY_URL}/metrics"),
        ("Detailed Health", "GET", f"{GATEWAY_URL}/health/detailed"),
        ("Metrics Dashboard", "GET", f"{GATEWAY_URL}/metrics/dashboard"),
        ("Candidate Stats", "GET", f"{GATEWAY_URL}/candidates/stats"),
    ]
    
    for name, method, url in core_tests:
        total += 1
        success, result = test_endpoint(name, method, url)
        if success:
            passed += 1
    
    print(f"\nCore API: {sum(1 for _, method, url in core_tests if test_endpoint('', method, url)[0])}/{len(core_tests)} passed")
    
    # Job Management
    print("\n=== JOB MANAGEMENT ===")
    job_tests = [
        ("List Jobs", "GET", f"{GATEWAY_URL}/v1/jobs"),
        ("Export Job Report", "GET", f"{GATEWAY_URL}/v1/reports/job/1/export.csv"),
    ]
    
    for name, method, url in job_tests:
        total += 1
        success, result = test_endpoint(name, method, url)
        if success:
            passed += 1
    
    # Test job creation
    total += 1
    job_data = {
        "title": "Test Engineer",
        "department": "Engineering", 
        "location": "Remote",
        "experience_level": "Senior",
        "requirements": "Python, FastAPI",
        "description": "Test job posting"
    }
    success, result = test_endpoint("Create Job", "POST", f"{GATEWAY_URL}/v1/jobs", job_data)
    if success:
        passed += 1
    
    # Candidate Management
    print("\n=== CANDIDATE MANAGEMENT ===")
    candidate_tests = [
        ("Get All Candidates", "GET", f"{GATEWAY_URL}/v1/candidates"),
        ("Get Candidate by ID", "GET", f"{GATEWAY_URL}/v1/candidates/1"),
        ("Search Candidates", "GET", f"{GATEWAY_URL}/v1/candidates/search?skills=Python"),
        ("Get Candidates by Job", "GET", f"{GATEWAY_URL}/v1/candidates/job/1"),
    ]
    
    for name, method, url in candidate_tests:
        total += 1
        success, result = test_endpoint(name, method, url)
        if success:
            passed += 1
    
    # AI Matching
    print("\n=== AI MATCHING ===")
    total += 1
    success, result = test_endpoint("AI Top Matches", "GET", f"{GATEWAY_URL}/v1/match/1/top")
    if success:
        passed += 1
        if isinstance(result, dict):
            matches = result.get('top_candidates', [])
            print(f"  Found {len(matches)} AI matches")
    
    # Security Features
    print("\n=== SECURITY FEATURES ===")
    security_tests = [
        ("Rate Limit Status", "GET", f"{GATEWAY_URL}/v1/security/rate-limit-status"),
        ("Blocked IPs", "GET", f"{GATEWAY_URL}/v1/security/blocked-ips"),
        ("Security Headers Test", "GET", f"{GATEWAY_URL}/v1/security/security-headers-test"),
        ("Penetration Test Endpoints", "GET", f"{GATEWAY_URL}/v1/security/penetration-test-endpoints"),
        ("CSP Policies", "GET", f"{GATEWAY_URL}/v1/security/csp-policies"),
        ("CSP Violations", "GET", f"{GATEWAY_URL}/v1/security/csp-violations"),
    ]
    
    for name, method, url in security_tests:
        total += 1
        success, result = test_endpoint(name, method, url)
        if success:
            passed += 1
    
    # 2FA Features
    print("\n=== 2FA FEATURES ===")
    twofa_tests = [
        ("2FA Demo Setup", "GET", f"{GATEWAY_URL}/v1/2fa/demo-setup"),
        ("2FA Status", "GET", f"{GATEWAY_URL}/v1/2fa/status/test_user"),
        ("2FA Test Token", "GET", f"{GATEWAY_URL}/v1/2fa/test-token/test_user/123456"),
    ]
    
    for name, method, url in twofa_tests:
        total += 1
        success, result = test_endpoint(name, method, url)
        if success:
            passed += 1
    
    # Password Management
    print("\n=== PASSWORD MANAGEMENT ===")
    password_tests = [
        ("Password Policy", "GET", f"{GATEWAY_URL}/v1/password/policy"),
        ("Password Strength Test", "GET", f"{GATEWAY_URL}/v1/password/strength-test"),
        ("Password Security Tips", "GET", f"{GATEWAY_URL}/v1/password/security-tips"),
    ]
    
    for name, method, url in password_tests:
        total += 1
        success, result = test_endpoint(name, method, url)
        if success:
            passed += 1
    
    # Assessment & Workflow
    print("\n=== ASSESSMENT & WORKFLOW ===")
    workflow_tests = [
        ("Get All Feedback", "GET", f"{GATEWAY_URL}/v1/feedback"),
        ("Get All Interviews", "GET", f"{GATEWAY_URL}/v1/interviews"),
        ("Get All Offers", "GET", f"{GATEWAY_URL}/v1/offers"),
    ]
    
    for name, method, url in workflow_tests:
        total += 1
        success, result = test_endpoint(name, method, url)
        if success:
            passed += 1
    
    # Client Portal
    print("\n=== CLIENT PORTAL ===")
    total += 1
    client_data = {"client_id": "TECH001", "password": "demo123"}
    success, result = test_endpoint("Client Login", "POST", f"{GATEWAY_URL}/v1/client/login", client_data)
    if success:
        passed += 1
    
    # Data Verification
    print("\n=== DATA VERIFICATION ===")
    total += 1
    success, result = test_endpoint("Database Connectivity", "GET", f"{GATEWAY_URL}/test-candidates")
    if success:
        passed += 1
        if isinstance(result, dict):
            count = result.get('total_candidates', 0)
            print(f"  Database contains {count} candidates")
    
    # Summary
    print("\n" + "=" * 60)
    print("GATEWAY SERVICE VERIFICATION SUMMARY")
    print("=" * 60)
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed >= total * 0.9:
        print("STATUS: EXCELLENT - Gateway service fully operational")
    elif passed >= total * 0.8:
        print("STATUS: GOOD - Minor issues detected")
    else:
        print("STATUS: ISSUES - Multiple failures detected")
    
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return passed, total

if __name__ == "__main__":
    main()