#!/usr/bin/env python3
"""
Root Cause Analysis Script for BHIV HR Platform
Identifies and reports all critical issues preventing proper deployment
"""

import requests
import json
import sys
from datetime import datetime

def test_endpoint(url, headers=None, timeout=10):
    """Test a single endpoint and return status"""
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        return {
            "status": "SUCCESS" if response.status_code == 200 else "FAILED",
            "status_code": response.status_code,
            "response_size": len(response.text),
            "error": None
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "status_code": None,
            "response_size": 0,
            "error": str(e)
        }

def main():
    print("BHIV HR Platform - Root Cause Analysis")
    print("=" * 60)
    
    # Test configuration
    base_url = "https://bhiv-hr-gateway.onrender.com"
    headers = {"Authorization": "Bearer myverysecureapikey123"}
    
    # Critical endpoints to test
    critical_endpoints = [
        "/",
        "/health", 
        "/docs",
        "/v1/jobs",
        "/v1/candidates",
        "/v1/match/1/top"
    ]
    
    # All 47 endpoints
    all_endpoints = [
        "/", "/health", "/test-candidates",
        "/v1/jobs", "/v1/candidates", "/v1/candidates/search", "/v1/candidates/bulk",
        "/v1/match/1/top", "/v1/interviews", "/v1/client/login",
        "/candidates/stats", "/v1/reports/hiring-funnel", "/v1/reports/performance",
        "/metrics", "/health/detailed", "/metrics/dashboard",
        "/v1/security/rate-limit-status", "/v1/security/2fa/setup", "/v1/security/2fa/verify",
        "/v1/security/password/reset", "/v1/security/password/change", "/v1/security/sessions",
        "/v1/security/sessions/123", "/v1/security/audit-log", "/v1/security/api-keys",
        "/v1/security/permissions", "/v1/security/compliance", "/v1/security/data-export",
        "/v1/docs/daily-reflections", "/v1/docs/bias-analysis", "/v1/docs/project-structure",
        "/v1/docs/api-reference", "/v1/docs/user-guide", "/v1/docs/security-audit",
        "/v1/docs/deployment-guide", "/v1/docs/changelog", "/v1/docs/architecture",
        "/v1/docs/testing", "/v1/docs/performance", "/v1/docs/compliance"
    ]
    
    print(f"Testing {len(all_endpoints)} endpoints...")
    print()
    
    # Test critical endpoints first
    print("CRITICAL ENDPOINTS:")
    critical_results = {}
    for endpoint in critical_endpoints:
        url = f"{base_url}{endpoint}"
        result = test_endpoint(url, headers if endpoint != "/health" else None)
        critical_results[endpoint] = result
        status_icon = "OK" if result["status"] == "SUCCESS" else "FAIL"
        print(f"{status_icon} {endpoint}: {result['status']} ({result.get('status_code', 'N/A')})")
    
    print()
    
    # Test all endpoints
    print("ALL ENDPOINTS:")
    working_count = 0
    failed_count = 0
    error_count = 0
    
    for endpoint in all_endpoints:
        url = f"{base_url}{endpoint}"
        result = test_endpoint(url, headers if endpoint not in ["/health", "/"] else None)
        
        if result["status"] == "SUCCESS":
            working_count += 1
            print(f"OK   {endpoint}")
        elif result["status"] == "FAILED":
            failed_count += 1
            print(f"FAIL {endpoint} - HTTP {result['status_code']}")
        else:
            error_count += 1
            print(f"ERR  {endpoint} - {result['error']}")
    
    print()
    print("SUMMARY:")
    print(f"Working: {working_count}/{len(all_endpoints)} ({working_count/len(all_endpoints)*100:.1f}%)")
    print(f"Failed: {failed_count}/{len(all_endpoints)} ({failed_count/len(all_endpoints)*100:.1f}%)")
    print(f"Errors: {error_count}/{len(all_endpoints)} ({error_count/len(all_endpoints)*100:.1f}%)")
    
    # Root cause analysis
    print()
    print("ROOT CAUSE ANALYSIS:")
    
    if working_count < 20:
        print("CRITICAL: Less than 50% of endpoints working")
        print("   -> Likely deployment issue or application startup failure")
    
    if critical_results["/"]["status"] != "SUCCESS":
        print("CRITICAL: Root endpoint failing")
        print("   -> Application not starting properly")
    
    if critical_results["/health"]["status"] != "SUCCESS":
        print("CRITICAL: Health check failing")
        print("   -> Service unavailable or crashed")
    
    if critical_results["/v1/jobs"]["status"] != "SUCCESS":
        print("CRITICAL: Core API endpoints failing")
        print("   -> Authentication or database issues")
    
    # Check if it's a deployment issue
    try:
        root_response = requests.get(f"{base_url}/", timeout=10)
        if root_response.status_code == 200:
            data = root_response.json()
            reported_endpoints = data.get("endpoints", 0)
            print(f"Application reports {reported_endpoints} endpoints")
            if reported_endpoints != len(all_endpoints):
                print(f"WARNING: Expected {len(all_endpoints)}, got {reported_endpoints}")
        else:
            print("Cannot retrieve application metadata")
    except Exception as e:
        print(f"Failed to get application info: {e}")
    
    print()
    print("RECOMMENDED ACTIONS:")
    
    if working_count < 10:
        print("1. IMMEDIATE: Check Render deployment logs")
        print("2. Verify application is starting without errors")
        print("3. Check for import errors or syntax issues")
    elif working_count < 30:
        print("1. Check authentication middleware")
        print("2. Verify database connectivity")
        print("3. Review endpoint definitions")
    else:
        print("1. Most endpoints working - minor fixes needed")
        print("2. Address specific failing endpoints")
    
    print(f"\nAnalysis completed at {datetime.now().isoformat()}")
    
    return working_count >= 40  # Return success if most endpoints work

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)