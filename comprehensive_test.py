#!/usr/bin/env python3
"""Comprehensive endpoint testing"""

import httpx
import json

def test_comprehensive_endpoints():
    """Test all documented endpoints"""
    
    gateway_url = "https://bhiv-hr-gateway-901a.onrender.com"
    agent_url = "https://bhiv-hr-agent-o6nx.onrender.com"
    
    api_key = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Comprehensive endpoint list based on documentation
    endpoints = [
        # Gateway Core (4 endpoints)
        ("GET", f"{gateway_url}/health"),
        ("GET", f"{gateway_url}/"),
        ("GET", f"{gateway_url}/docs"),
        ("GET", f"{gateway_url}/architecture"),
        
        # Jobs Module (10 endpoints)
        ("GET", f"{gateway_url}/v1/jobs"),
        ("POST", f"{gateway_url}/v1/jobs"),
        ("GET", f"{gateway_url}/v1/jobs/1"),
        ("PUT", f"{gateway_url}/v1/jobs/1"),
        ("DELETE", f"{gateway_url}/v1/jobs/1"),
        ("GET", f"{gateway_url}/v1/jobs/search"),
        ("POST", f"{gateway_url}/v1/jobs/1/match"),
        ("GET", f"{gateway_url}/v1/jobs/1/candidates"),
        ("POST", f"{gateway_url}/v1/jobs/bulk"),
        ("GET", f"{gateway_url}/v1/jobs/analytics"),
        
        # Candidates Module (12 endpoints)
        ("GET", f"{gateway_url}/v1/candidates"),
        ("POST", f"{gateway_url}/v1/candidates"),
        ("GET", f"{gateway_url}/v1/candidates/1"),
        ("PUT", f"{gateway_url}/v1/candidates/1"),
        ("DELETE", f"{gateway_url}/v1/candidates/1"),
        ("GET", f"{gateway_url}/v1/candidates/search"),
        ("POST", f"{gateway_url}/v1/candidates/1/match"),
        ("GET", f"{gateway_url}/v1/candidates/1/jobs"),
        ("POST", f"{gateway_url}/v1/candidates/bulk"),
        ("GET", f"{gateway_url}/v1/candidates/analytics"),
        ("POST", f"{gateway_url}/v1/candidates/upload"),
        ("GET", f"{gateway_url}/v1/candidates/export"),
        
        # Auth Module (17 endpoints)
        ("POST", f"{gateway_url}/v1/auth/login"),
        ("POST", f"{gateway_url}/v1/auth/logout"),
        ("POST", f"{gateway_url}/v1/auth/register"),
        ("GET", f"{gateway_url}/v1/auth/me"),
        ("PUT", f"{gateway_url}/v1/auth/profile"),
        ("POST", f"{gateway_url}/v1/auth/change-password"),
        ("POST", f"{gateway_url}/v1/auth/forgot-password"),
        ("POST", f"{gateway_url}/v1/auth/reset-password"),
        ("POST", f"{gateway_url}/v1/auth/verify-email"),
        ("POST", f"{gateway_url}/v1/auth/resend-verification"),
        ("GET", f"{gateway_url}/v1/auth/sessions"),
        ("DELETE", f"{gateway_url}/v1/auth/sessions/1"),
        ("POST", f"{gateway_url}/v1/auth/2fa/setup"),
        ("POST", f"{gateway_url}/v1/auth/2fa/verify"),
        ("DELETE", f"{gateway_url}/v1/auth/2fa/disable"),
        ("GET", f"{gateway_url}/v1/auth/permissions"),
        ("GET", f"{gateway_url}/v1/auth/roles"),
        
        # Workflows Module (15 endpoints)
        ("GET", f"{gateway_url}/v1/workflows"),
        ("POST", f"{gateway_url}/v1/workflows"),
        ("GET", f"{gateway_url}/v1/workflows/1"),
        ("PUT", f"{gateway_url}/v1/workflows/1"),
        ("DELETE", f"{gateway_url}/v1/workflows/1"),
        ("POST", f"{gateway_url}/v1/workflows/1/trigger"),
        ("GET", f"{gateway_url}/v1/workflows/1/status"),
        ("POST", f"{gateway_url}/v1/workflows/1/pause"),
        ("POST", f"{gateway_url}/v1/workflows/1/resume"),
        ("GET", f"{gateway_url}/v1/workflows/templates"),
        ("POST", f"{gateway_url}/v1/workflows/templates"),
        ("GET", f"{gateway_url}/v1/workflows/history"),
        ("GET", f"{gateway_url}/v1/workflows/analytics"),
        ("POST", f"{gateway_url}/v1/workflows/bulk-trigger"),
        ("GET", f"{gateway_url}/v1/workflows/queue"),
        
        # Monitoring Module (25 endpoints)
        ("GET", f"{gateway_url}/health/detailed"),
        ("GET", f"{gateway_url}/health/simple"),
        ("GET", f"{gateway_url}/health/database"),
        ("GET", f"{gateway_url}/health/services"),
        ("GET", f"{gateway_url}/health/resources"),
        ("GET", f"{gateway_url}/monitoring/errors"),
        ("GET", f"{gateway_url}/monitoring/errors/search"),
        ("GET", f"{gateway_url}/monitoring/errors/stats"),
        ("GET", f"{gateway_url}/monitoring/logs"),
        ("GET", f"{gateway_url}/monitoring/logs/search"),
        ("GET", f"{gateway_url}/monitoring/dependencies"),
        ("GET", f"{gateway_url}/monitoring/performance"),
        ("GET", f"{gateway_url}/monitoring/alerts"),
        ("POST", f"{gateway_url}/monitoring/alerts"),
        ("GET", f"{gateway_url}/monitoring/metrics"),
        ("GET", f"{gateway_url}/metrics"),
        ("GET", f"{gateway_url}/metrics/dashboard"),
        ("GET", f"{gateway_url}/metrics/prometheus"),
        ("GET", f"{gateway_url}/monitoring/backup/status"),
        ("POST", f"{gateway_url}/monitoring/backup/validate"),
        ("GET", f"{gateway_url}/monitoring/security/events"),
        ("GET", f"{gateway_url}/monitoring/security/threats"),
        ("GET", f"{gateway_url}/monitoring/audit/logs"),
        ("GET", f"{gateway_url}/monitoring/system/status"),
        ("GET", f"{gateway_url}/monitoring/uptime"),
        
        # Agent Service (15 endpoints)
        ("GET", f"{agent_url}/health"),
        ("GET", f"{agent_url}/"),
        ("GET", f"{agent_url}/docs"),
        ("POST", f"{agent_url}/v1/match/candidates"),
        ("POST", f"{agent_url}/v1/match/jobs"),
        ("POST", f"{agent_url}/v1/match/score"),
        ("POST", f"{agent_url}/v1/match/bulk"),
        ("POST", f"{agent_url}/v1/match/semantic"),
        ("POST", f"{agent_url}/v1/match/advanced"),
        ("GET", f"{agent_url}/v1/analytics/performance"),
        ("GET", f"{agent_url}/v1/analytics/metrics"),
        ("GET", f"{agent_url}/v1/models/status"),
        ("POST", f"{agent_url}/v1/models/reload"),
        ("GET", f"{agent_url}/v1/config"),
        ("POST", f"{agent_url}/v1/config/update")
    ]
    
    results = {"functional": [], "non_functional": [], "errors": []}
    
    print("Testing Comprehensive Endpoint Coverage...")
    print("=" * 60)
    
    for method, url in endpoints:
        try:
            if method == "GET":
                response = httpx.get(url, headers=headers, timeout=10.0)
            elif method == "POST":
                # Use minimal test data for POST requests
                test_data = {"test": True}
                response = httpx.post(url, headers=headers, json=test_data, timeout=10.0)
            elif method == "PUT":
                test_data = {"test": True}
                response = httpx.put(url, headers=headers, json=test_data, timeout=10.0)
            elif method == "DELETE":
                response = httpx.delete(url, headers=headers, timeout=10.0)
            
            # Consider 200-299 as success, 404 as endpoint not found, others as functional but with issues
            if 200 <= response.status_code < 300:
                status = "PASS"
                results["functional"].append({"method": method, "url": url, "status": response.status_code})
            elif response.status_code == 404:
                status = "NOT_FOUND"
                results["non_functional"].append({"method": method, "url": url, "status": response.status_code, "issue": "Endpoint not found"})
            elif response.status_code == 405:
                status = "METHOD_NOT_ALLOWED"
                results["non_functional"].append({"method": method, "url": url, "status": response.status_code, "issue": "Method not allowed"})
            elif response.status_code in [401, 403]:
                status = "AUTH_ISSUE"
                results["functional"].append({"method": method, "url": url, "status": response.status_code, "note": "Authentication required"})
            elif response.status_code == 422:
                status = "VALIDATION_ERROR"
                results["functional"].append({"method": method, "url": url, "status": response.status_code, "note": "Validation error (expected for test data)"})
            else:
                status = "ERROR"
                results["non_functional"].append({"method": method, "url": url, "status": response.status_code, "issue": f"HTTP {response.status_code}"})
            
            print(f"{status}: {method} {url.split('/')[-1]} - {response.status_code}")
                
        except Exception as e:
            print(f"EXCEPTION: {method} {url.split('/')[-1]} - {str(e)}")
            results["errors"].append({"method": method, "url": url, "error": str(e)})
    
    # Generate summary
    total = len(results["functional"]) + len(results["non_functional"]) + len(results["errors"])
    functional = len(results["functional"])
    non_functional = len(results["non_functional"])
    errors = len(results["errors"])
    
    print("\n" + "=" * 60)
    print("COMPREHENSIVE ANALYSIS SUMMARY:")
    print(f"Total Endpoints Tested: {total}")
    print(f"Functional: {functional} ({functional/total*100:.1f}%)")
    print(f"Non-Functional: {non_functional} ({non_functional/total*100:.1f}%)")
    print(f"Errors: {errors} ({errors/total*100:.1f}%)")
    
    if results["non_functional"]:
        print(f"\nNON-FUNCTIONAL ENDPOINTS ({len(results['non_functional'])}):")
        for endpoint in results["non_functional"]:
            print(f"  {endpoint['method']} {endpoint['url'].split('/')[-1]} - {endpoint['status']} ({endpoint.get('issue', 'Unknown issue')})")
    
    if results["errors"]:
        print(f"\nERROR ENDPOINTS ({len(results['errors'])}):")
        for endpoint in results["errors"]:
            print(f"  {endpoint['method']} {endpoint['url'].split('/')[-1]} - {endpoint['error']}")
    
    # Save detailed results
    with open("comprehensive_endpoint_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    return results

if __name__ == "__main__":
    test_comprehensive_endpoints()