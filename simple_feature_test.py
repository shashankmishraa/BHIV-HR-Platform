#!/usr/bin/env python3
"""
Simple Feature Gap Analysis: Test key endpoints
"""

import requests
import json
import time

# Service URLs
GATEWAY_URL = "https://bhiv-hr-gateway-46pz.onrender.com"
AGENT_URL = "https://bhiv-hr-agent-m1me.onrender.com"
API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def test_endpoint(url, method="GET", data=None):
    """Test endpoint and return status"""
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=15)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=15)
        
        return {
            "url": url,
            "method": method,
            "status": response.status_code,
            "success": response.status_code in [200, 201],
            "size": len(response.text)
        }
    except Exception as e:
        return {
            "url": url,
            "method": method,
            "status": "ERROR",
            "success": False,
            "error": str(e)[:100]
        }

def main():
    print("BHIV HR Platform - Feature Gap Analysis")
    print("=" * 50)
    
    # Key Gateway endpoints from code analysis
    gateway_tests = [
        # Core endpoints
        (f"{GATEWAY_URL}/", "GET", "API Root"),
        (f"{GATEWAY_URL}/health", "GET", "Health Check"),
        (f"{GATEWAY_URL}/metrics", "GET", "Prometheus Metrics"),
        (f"{GATEWAY_URL}/health/detailed", "GET", "Detailed Health"),
        (f"{GATEWAY_URL}/metrics/dashboard", "GET", "Metrics Dashboard"),
        
        # Job Management
        (f"{GATEWAY_URL}/v1/jobs", "GET", "List Jobs"),
        
        # Candidate Management
        (f"{GATEWAY_URL}/v1/candidates", "GET", "Get Candidates"),
        (f"{GATEWAY_URL}/v1/candidates/search", "GET", "Search Candidates"),
        (f"{GATEWAY_URL}/v1/candidates/1", "GET", "Get Candidate by ID"),
        
        # AI Matching
        (f"{GATEWAY_URL}/v1/match/1/top", "GET", "AI Top Matches"),
        
        # Assessment
        (f"{GATEWAY_URL}/v1/feedback", "GET", "Get Feedback"),
        (f"{GATEWAY_URL}/v1/interviews", "GET", "Get Interviews"),
        (f"{GATEWAY_URL}/v1/offers", "GET", "Get Offers"),
        
        # Security Features
        (f"{GATEWAY_URL}/v1/security/rate-limit-status", "GET", "Rate Limit Status"),
        (f"{GATEWAY_URL}/v1/security/blocked-ips", "GET", "Blocked IPs"),
        (f"{GATEWAY_URL}/v1/security/security-headers-test", "GET", "Security Headers"),
        (f"{GATEWAY_URL}/v1/security/penetration-test-endpoints", "GET", "Penetration Test"),
        
        # CSP Management
        (f"{GATEWAY_URL}/v1/security/csp-violations", "GET", "CSP Violations"),
        (f"{GATEWAY_URL}/v1/security/csp-policies", "GET", "CSP Policies"),
        
        # 2FA Features
        (f"{GATEWAY_URL}/v1/2fa/status/test_user", "GET", "2FA Status"),
        (f"{GATEWAY_URL}/v1/2fa/demo-setup", "GET", "2FA Demo Setup"),
        
        # Password Management
        (f"{GATEWAY_URL}/v1/password/policy", "GET", "Password Policy"),
        (f"{GATEWAY_URL}/v1/password/strength-test", "GET", "Password Strength Test"),
        (f"{GATEWAY_URL}/v1/password/security-tips", "GET", "Password Security Tips"),
    ]
    
    # Agent endpoints
    agent_tests = [
        (f"{AGENT_URL}/", "GET", "Agent Root"),
        (f"{AGENT_URL}/health", "GET", "Agent Health"),
        (f"{AGENT_URL}/test-db", "GET", "Agent DB Test"),
        (f"{AGENT_URL}/analyze/1", "GET", "Candidate Analysis"),
    ]
    
    print("\nTesting Gateway Service...")
    gateway_results = []
    for url, method, name in gateway_tests:
        print(f"Testing: {name}")
        result = test_endpoint(url, method)
        result["feature"] = name
        gateway_results.append(result)
        time.sleep(0.1)
    
    print("\nTesting Agent Service...")
    agent_results = []
    for url, method, name in agent_tests:
        print(f"Testing: {name}")
        result = test_endpoint(url, method)
        result["feature"] = name
        agent_results.append(result)
        time.sleep(0.1)
    
    # POST endpoint tests
    print("\nTesting POST endpoints...")
    post_tests = [
        (f"{GATEWAY_URL}/v1/2fa/setup", "POST", "2FA Setup", {"user_id": "test"}),
        (f"{GATEWAY_URL}/v1/password/validate", "POST", "Password Validation", {"password": "Test123!"}),
        (f"{GATEWAY_URL}/v1/security/test-input-validation", "POST", "Input Validation", {"input_data": "test"}),
        (f"{AGENT_URL}/match", "POST", "AI Matching", {"job_id": 1}),
    ]
    
    post_results = []
    for url, method, name, data in post_tests:
        print(f"Testing: {name}")
        result = test_endpoint(url, method, data)
        result["feature"] = name
        post_results.append(result)
        time.sleep(0.1)
    
    # Generate Report
    print("\n" + "=" * 50)
    print("FEATURE GAP ANALYSIS RESULTS")
    print("=" * 50)
    
    all_results = gateway_results + agent_results + post_results
    working = [r for r in all_results if r['success']]
    failing = [r for r in all_results if not r['success']]
    
    print(f"\nTotal Features Tested: {len(all_results)}")
    print(f"Working Features: {len(working)} ({len(working)/len(all_results)*100:.1f}%)")
    print(f"Missing/Failing Features: {len(failing)} ({len(failing)/len(all_results)*100:.1f}%)")
    
    if failing:
        print(f"\nMISSING/FAILING FEATURES:")
        for feature in failing:
            print(f"  - {feature['feature']}: {feature['method']} {feature['status']}")
            if 'error' in feature:
                print(f"    Error: {feature['error']}")
    
    # Category Analysis
    print(f"\nFEATURE CATEGORIES:")
    categories = {
        'Core API': [r for r in all_results if any(x in r['feature'].lower() for x in ['root', 'health', 'metrics'])],
        'HR Functions': [r for r in all_results if any(x in r['feature'].lower() for x in ['job', 'candidate', 'feedback', 'interview', 'offer'])],
        'AI & Matching': [r for r in all_results if any(x in r['feature'].lower() for x in ['ai', 'match', 'analysis'])],
        'Security': [r for r in all_results if any(x in r['feature'].lower() for x in ['security', '2fa', 'password', 'csp'])],
    }
    
    for category, results in categories.items():
        working_cat = [r for r in results if r['success']]
        if results:
            print(f"  {category}: {len(working_cat)}/{len(results)} ({len(working_cat)/len(results)*100:.1f}%)")
    
    # Save results
    with open('feature_analysis_results.json', 'w') as f:
        json.dump({
            'gateway_results': gateway_results,
            'agent_results': agent_results,
            'post_results': post_results,
            'summary': {
                'total': len(all_results),
                'working': len(working),
                'failing': len(failing),
                'success_rate': len(working)/len(all_results)
            }
        }, f, indent=2, default=str)
    
    print(f"\nDetailed results saved to: feature_analysis_results.json")

if __name__ == "__main__":
    main()