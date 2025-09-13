#!/usr/bin/env python3
"""
Test all 47 endpoints for integration and connectivity
"""

import requests
import json
from datetime import datetime, timedelta

GATEWAY_URL = "https://bhiv-hr-gateway.onrender.com"
API_KEY = "myverysecureapikey123"
headers = {"Authorization": f"Bearer {API_KEY}"}

def test_endpoint(method, url, data=None, auth_required=True):
    try:
        req_headers = headers if auth_required else {}
        
        if method == "GET":
            response = requests.get(url, headers=req_headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, headers=req_headers, json=data or {}, timeout=10)
        elif method == "DELETE":
            response = requests.delete(url, headers=req_headers, timeout=10)
        
        return {
            "status": response.status_code,
            "success": response.status_code < 400,
            "response_size": len(response.text),
            "has_json": response.headers.get('content-type', '').startswith('application/json')
        }
    except Exception as e:
        return {"status": "ERROR", "success": False, "error": str(e)[:50]}

def main():
    print("Testing All 47 Endpoints - Integration & Connectivity")
    print("=" * 60)
    
    # All 47 endpoints
    endpoints = [
        # Core (3)
        ("GET", f"{GATEWAY_URL}/", None, False),
        ("GET", f"{GATEWAY_URL}/health", None, False),
        ("GET", f"{GATEWAY_URL}/test-candidates", None, True),
        
        # Job Management (2)
        ("POST", f"{GATEWAY_URL}/v1/jobs", {"title": "Test Job", "department": "Engineering", "location": "Remote", "experience_level": "Mid", "requirements": "Python", "description": "Test"}, True),
        ("GET", f"{GATEWAY_URL}/v1/jobs", None, True),
        
        # Candidate Management (4)
        ("GET", f"{GATEWAY_URL}/v1/candidates", None, True),
        ("GET", f"{GATEWAY_URL}/v1/candidates/search?skills=Python", None, True),
        ("POST", f"{GATEWAY_URL}/v1/candidates/bulk", {"candidates": [{"name": "Test", "email": "test@test.com"}]}, True),
        ("GET", f"{GATEWAY_URL}/candidates/stats", None, True),
        
        # AI Matching (2)
        ("POST", f"{GATEWAY_URL}/v1/match", {"job_id": 1}, True),
        ("GET", f"{GATEWAY_URL}/v1/match/1/top", None, True),
        
        # Interview Management (2)
        ("GET", f"{GATEWAY_URL}/v1/interviews", None, True),
        ("POST", f"{GATEWAY_URL}/v1/interviews", {"candidate_id": 1, "job_id": 1, "interview_date": datetime.now().isoformat(), "interviewer": "Test"}, True),
        
        # Client Portal (1)
        ("POST", f"{GATEWAY_URL}/v1/client/login", {"username": "TECH001", "password": "demo123"}, False),
        
        # Monitoring (3)
        ("GET", f"{GATEWAY_URL}/metrics", None, False),
        ("GET", f"{GATEWAY_URL}/health/detailed", None, False),
        ("GET", f"{GATEWAY_URL}/metrics/dashboard", None, False),
        
        # Security (15)
        ("GET", f"{GATEWAY_URL}/v1/security/rate-limit-status", None, True),
        ("POST", f"{GATEWAY_URL}/v1/security/2fa/setup", {}, True),
        ("POST", f"{GATEWAY_URL}/v1/security/2fa/verify", {"token": "123456"}, True),
        ("POST", f"{GATEWAY_URL}/v1/security/password/reset", {"email": "test@test.com"}, False),
        ("POST", f"{GATEWAY_URL}/v1/security/password/change", {"old_password": "old", "new_password": "new"}, True),
        ("GET", f"{GATEWAY_URL}/v1/security/sessions", None, True),
        ("DELETE", f"{GATEWAY_URL}/v1/security/sessions/sess_123", None, True),
        ("GET", f"{GATEWAY_URL}/v1/security/audit-log", None, True),
        ("POST", f"{GATEWAY_URL}/v1/security/api-keys", {"name": "Test Key"}, True),
        ("GET", f"{GATEWAY_URL}/v1/security/api-keys", None, True),
        ("DELETE", f"{GATEWAY_URL}/v1/security/api-keys/key_123", None, True),
        ("GET", f"{GATEWAY_URL}/v1/security/permissions", None, True),
        ("POST", f"{GATEWAY_URL}/v1/security/permissions", {"permissions": ["read:all"]}, True),
        ("GET", f"{GATEWAY_URL}/v1/security/compliance", None, True),
        ("POST", f"{GATEWAY_URL}/v1/security/data-export", {"user_id": "123"}, True),
        
        # Analytics (2)
        ("GET", f"{GATEWAY_URL}/v1/reports/hiring-funnel", None, True),
        ("GET", f"{GATEWAY_URL}/v1/reports/performance", None, True),
        
        # Documentation (13)
        ("GET", f"{GATEWAY_URL}/v1/docs/daily-reflections", None, False),
        ("POST", f"{GATEWAY_URL}/v1/docs/daily-reflections", {"reflection": "Test reflection"}, True),
        ("GET", f"{GATEWAY_URL}/v1/docs/bias-analysis", None, False),
        ("GET", f"{GATEWAY_URL}/v1/docs/project-structure", None, False),
        ("GET", f"{GATEWAY_URL}/v1/docs/api-reference", None, False),
        ("GET", f"{GATEWAY_URL}/v1/docs/user-guide", None, False),
        ("GET", f"{GATEWAY_URL}/v1/docs/security-audit", None, False),
        ("GET", f"{GATEWAY_URL}/v1/docs/deployment-guide", None, False),
        ("GET", f"{GATEWAY_URL}/v1/docs/changelog", None, False),
        ("GET", f"{GATEWAY_URL}/v1/docs/architecture", None, False),
        ("GET", f"{GATEWAY_URL}/v1/docs/testing", None, False),
        ("GET", f"{GATEWAY_URL}/v1/docs/performance", None, False),
        ("GET", f"{GATEWAY_URL}/v1/docs/compliance", None, False),
    ]
    
    print(f"Testing {len(endpoints)} endpoints...\n")
    
    results = {
        "working": 0,
        "failing": 0,
        "categories": {}
    }
    
    categories = [
        ("Core", 3),
        ("Job Management", 2),
        ("Candidate Management", 4),
        ("AI Matching", 2),
        ("Interview Management", 2),
        ("Client Portal", 1),
        ("Monitoring", 3),
        ("Security", 15),
        ("Analytics", 2),
        ("Documentation", 13)
    ]
    
    endpoint_idx = 0
    
    for category, count in categories:
        print(f"{category.upper()} ({count} endpoints)")
        print("-" * 40)
        
        category_results = {"working": 0, "total": count}
        
        for i in range(count):
            if endpoint_idx < len(endpoints):
                method, url, data, auth = endpoints[endpoint_idx]
                endpoint_name = url.split('/')[-1] or url.split('/')[-2]
                
                result = test_endpoint(method, url, data, auth)
                
                if result["success"]:
                    print(f"[OK] {method} {endpoint_name}: {result['status']}")
                    results["working"] += 1
                    category_results["working"] += 1
                else:
                    print(f"[FAIL] {method} {endpoint_name}: {result.get('status', 'ERROR')}")
                    results["failing"] += 1
                
                endpoint_idx += 1
        
        results["categories"][category] = category_results
        success_rate = (category_results["working"] / category_results["total"]) * 100
        print(f"Category Success Rate: {success_rate:.1f}%\n")
    
    # Summary
    total_endpoints = results["working"] + results["failing"]
    overall_success = (results["working"] / total_endpoints) * 100
    
    print("=" * 60)
    print("INTEGRATION & CONNECTIVITY SUMMARY")
    print("=" * 60)
    print(f"Total Endpoints Tested: {total_endpoints}")
    print(f"Working: {results['working']}")
    print(f"Failing: {results['failing']}")
    print(f"Overall Success Rate: {overall_success:.1f}%")
    
    print(f"\nCATEGORY BREAKDOWN:")
    for category, stats in results["categories"].items():
        success_rate = (stats["working"] / stats["total"]) * 100
        print(f"  {category}: {stats['working']}/{stats['total']} ({success_rate:.1f}%)")
    
    # Integration Status
    if overall_success >= 90:
        integration_status = "FULLY INTEGRATED"
    elif overall_success >= 75:
        integration_status = "MOSTLY INTEGRATED"
    elif overall_success >= 50:
        integration_status = "PARTIALLY INTEGRATED"
    else:
        integration_status = "INTEGRATION ISSUES"
    
    print(f"\nIntegration Status: {integration_status}")
    
    # Connectivity Assessment
    core_working = results["categories"]["Core"]["working"] == results["categories"]["Core"]["total"]
    monitoring_working = results["categories"]["Monitoring"]["working"] >= 2
    
    if core_working and monitoring_working:
        connectivity_status = "FULLY CONNECTED"
    elif core_working:
        connectivity_status = "CORE CONNECTED"
    else:
        connectivity_status = "CONNECTION ISSUES"
    
    print(f"Connectivity Status: {connectivity_status}")
    
    print(f"\nTest completed at: {datetime.now().isoformat()}")

if __name__ == "__main__":
    main()