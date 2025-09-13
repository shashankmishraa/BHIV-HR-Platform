#!/usr/bin/env python3
"""
Complete Platform Verification - All Endpoints and Portal Functionalities
"""

import requests
import json
from datetime import datetime, timedelta

# Configuration
GATEWAY_URL = "https://bhiv-hr-gateway.onrender.com"
AGENT_URL = "https://bhiv-hr-agent.onrender.com"
HR_PORTAL_URL = "https://bhiv-hr-portal.onrender.com"
CLIENT_PORTAL_URL = "https://bhiv-hr-client-portal.onrender.com"
API_KEY = "myverysecureapikey123"

headers = {"Authorization": f"Bearer {API_KEY}"}

def test_endpoint(method, url, data=None, expected_status=200):
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=15)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=15)
        
        success = response.status_code == expected_status
        return {
            "success": success,
            "status": response.status_code,
            "data": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text[:100]
        }
    except Exception as e:
        return {"success": False, "status": "ERROR", "error": str(e)[:100]}

def check_portal(url, name):
    try:
        response = requests.get(url, timeout=15)
        content_length = len(response.text)
        has_content = content_length > 5000  # Proper content should be substantial
        
        return {
            "status": response.status_code,
            "content_length": content_length,
            "has_proper_content": has_content,
            "success": response.status_code == 200 and has_content
        }
    except Exception as e:
        return {"status": "ERROR", "error": str(e)[:100], "success": False}

def main():
    print("BHIV HR Platform - Complete Verification")
    print("=" * 60)
    
    results = {
        "core_endpoints": {},
        "job_management": {},
        "candidate_management": {},
        "ai_matching": {},
        "interview_management": {},
        "analytics": {},
        "monitoring": {},
        "client_portal": {},
        "portals": {},
        "summary": {}
    }
    
    # 1. Core Endpoints
    print("\n1. CORE ENDPOINTS")
    print("-" * 30)
    
    core_tests = [
        ("GET", f"{GATEWAY_URL}/", "Root"),
        ("GET", f"{GATEWAY_URL}/health", "Health"),
        ("GET", f"{GATEWAY_URL}/test-candidates", "DB Test")
    ]
    
    for method, url, name in core_tests:
        result = test_endpoint(method, url)
        results["core_endpoints"][name] = result
        status = "[OK]" if result["success"] else "[FAIL]"
        print(f"{status} {name}: {result['status']}")
    
    # 2. Job Management
    print("\n2. JOB MANAGEMENT")
    print("-" * 30)
    
    # Get jobs
    result = test_endpoint("GET", f"{GATEWAY_URL}/v1/jobs")
    results["job_management"]["list_jobs"] = result
    print(f"{'[OK]' if result['success'] else '[FAIL]'} List Jobs: {result['status']}")
    
    # Create job
    job_data = {
        "title": "Test Engineer",
        "department": "Engineering",
        "location": "Remote",
        "experience_level": "Mid",
        "requirements": "Python, FastAPI",
        "description": "Test job for verification"
    }
    result = test_endpoint("POST", f"{GATEWAY_URL}/v1/jobs", job_data, 200)
    results["job_management"]["create_job"] = result
    print(f"{'[OK]' if result['success'] else '[FAIL]'} Create Job: {result['status']}")
    
    # 3. Candidate Management
    print("\n3. CANDIDATE MANAGEMENT")
    print("-" * 30)
    
    candidate_tests = [
        ("GET", f"{GATEWAY_URL}/v1/candidates", "List All"),
        ("GET", f"{GATEWAY_URL}/v1/candidates/search?skills=Python", "Search"),
    ]
    
    for method, url, name in candidate_tests:
        result = test_endpoint(method, url)
        results["candidate_management"][name.lower().replace(" ", "_")] = result
        print(f"{'[OK]' if result['success'] else '[FAIL]'} {name}: {result['status']}")
    
    # Bulk upload
    bulk_data = {
        "candidates": [{
            "name": "Test Candidate",
            "email": f"test_{int(datetime.now().timestamp())}@example.com",
            "phone": "555-0123",
            "location": "Test City",
            "experience_years": 3,
            "technical_skills": "Python, JavaScript",
            "seniority_level": "Mid-level",
            "education_level": "Bachelor's"
        }]
    }
    result = test_endpoint("POST", f"{GATEWAY_URL}/v1/candidates/bulk", bulk_data)
    results["candidate_management"]["bulk_upload"] = result
    print(f"{'[OK]' if result['success'] else '[FAIL]'} Bulk Upload: {result['status']}")
    
    # 4. AI Matching
    print("\n4. AI MATCHING ENGINE")
    print("-" * 30)
    
    # AI matching tests
    match_data = {"job_id": 1, "requirements": "Python developer"}
    result = test_endpoint("POST", f"{GATEWAY_URL}/v1/match", match_data)
    results["ai_matching"]["match_post"] = result
    print(f"{'[OK]' if result['success'] else '[FAIL]'} AI Match POST: {result['status']}")
    
    result = test_endpoint("GET", f"{GATEWAY_URL}/v1/match/1/top")
    results["ai_matching"]["match_get"] = result
    print(f"{'[OK]' if result['success'] else '[FAIL]'} AI Match GET: {result['status']}")
    
    # 5. Interview Management
    print("\n5. INTERVIEW MANAGEMENT")
    print("-" * 30)
    
    # Get interviews
    result = test_endpoint("GET", f"{GATEWAY_URL}/v1/interviews")
    results["interview_management"]["list"] = result
    print(f"{'[OK]' if result['success'] else '[FAIL]'} List Interviews: {result['status']}")
    
    # Schedule interview
    interview_data = {
        "candidate_id": 1,
        "job_id": 1,
        "interview_date": (datetime.now() + timedelta(days=1)).isoformat(),
        "interviewer": "Test Interviewer",
        "notes": "Verification test"
    }
    result = test_endpoint("POST", f"{GATEWAY_URL}/v1/interviews", interview_data)
    results["interview_management"]["schedule"] = result
    print(f"{'[OK]' if result['success'] else '[FAIL]'} Schedule Interview: {result['status']}")
    
    # 6. Analytics
    print("\n6. ANALYTICS & STATISTICS")
    print("-" * 30)
    
    result = test_endpoint("GET", f"{GATEWAY_URL}/candidates/stats")
    results["analytics"]["stats"] = result
    print(f"{'[OK]' if result['success'] else '[FAIL]'} Candidate Stats: {result['status']}")
    
    # 7. Monitoring
    print("\n7. MONITORING ENDPOINTS")
    print("-" * 30)
    
    monitoring_tests = [
        ("GET", f"{GATEWAY_URL}/metrics", "Metrics"),
        ("GET", f"{GATEWAY_URL}/health/detailed", "Detailed Health")
    ]
    
    for method, url, name in monitoring_tests:
        result = test_endpoint(method, url)
        results["monitoring"][name.lower().replace(" ", "_")] = result
        print(f"{'[OK]' if result['success'] else '[FAIL]'} {name}: {result['status']}")
    
    # 8. Client Portal Authentication
    print("\n8. CLIENT PORTAL AUTHENTICATION")
    print("-" * 30)
    
    login_data = {"username": "TECH001", "password": "demo123"}
    result = test_endpoint("POST", f"{GATEWAY_URL}/v1/client/login", login_data)
    results["client_portal"]["login"] = result
    print(f"{'[OK]' if result['success'] else '[FAIL]'} Client Login: {result['status']}")
    
    # 9. Portal Functionality
    print("\n9. PORTAL FUNCTIONALITY")
    print("-" * 30)
    
    portals = [
        (HR_PORTAL_URL, "HR Portal"),
        (CLIENT_PORTAL_URL, "Client Portal")
    ]
    
    for url, name in portals:
        result = check_portal(url, name)
        results["portals"][name.lower().replace(" ", "_")] = result
        status = "[OK]" if result["success"] else "[FAIL]"
        content_info = f"({result.get('content_length', 0)} bytes)"
        print(f"{status} {name}: {result.get('status', 'ERROR')} {content_info}")
    
    # 10. AI Agent Health
    print("\n10. AI AGENT CONNECTIVITY")
    print("-" * 30)
    
    try:
        response = requests.get(f"{AGENT_URL}/health", timeout=10)
        agent_status = "[OK]" if response.status_code == 200 else "[FAIL]"
        print(f"{agent_status} AI Agent Health: {response.status_code}")
        results["ai_agent"] = {"status": response.status_code, "success": response.status_code == 200}
    except Exception as e:
        print(f"[FAIL] AI Agent Health: ERROR - {str(e)[:50]}")
        results["ai_agent"] = {"status": "ERROR", "success": False}
    
    # Summary
    print("\n" + "=" * 60)
    print("COMPREHENSIVE SUMMARY")
    print("=" * 60)
    
    # Count successes
    total_tests = 0
    passed_tests = 0
    
    for category, tests in results.items():
        if category == "summary":
            continue
        for test_name, test_result in tests.items():
            total_tests += 1
            if test_result.get("success", False):
                passed_tests += 1
    
    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {success_rate:.1f}%")
    
    # Platform status
    if success_rate >= 90:
        platform_status = "FULLY OPERATIONAL"
        status_icon = "[EXCELLENT]"
    elif success_rate >= 75:
        platform_status = "MOSTLY OPERATIONAL"
        status_icon = "[GOOD]"
    elif success_rate >= 50:
        platform_status = "PARTIALLY OPERATIONAL"
        status_icon = "[NEEDS ATTENTION]"
    else:
        platform_status = "CRITICAL ISSUES"
        status_icon = "[URGENT FIXES NEEDED]"
    
    print(f"\nPlatform Status: {status_icon} {platform_status}")
    
    # Key capabilities
    print(f"\nKey Capabilities:")
    capabilities = [
        ("Job Management", results["job_management"]),
        ("Candidate Management", results["candidate_management"]),
        ("AI Matching", results["ai_matching"]),
        ("Interview Scheduling", results["interview_management"]),
        ("Portal Access", results["portals"]),
        ("Analytics", results["analytics"])
    ]
    
    for cap_name, cap_results in capabilities:
        cap_success = all(test.get("success", False) for test in cap_results.values())
        cap_status = "[OK]" if cap_success else "[ISSUES]"
        print(f"  {cap_status} {cap_name}")
    
    print(f"\nVerification completed at: {datetime.now().isoformat()}")
    
    # Save results
    results["summary"] = {
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "success_rate": success_rate,
        "platform_status": platform_status,
        "timestamp": datetime.now().isoformat()
    }
    
    return results

if __name__ == "__main__":
    main()