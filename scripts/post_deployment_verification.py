#!/usr/bin/env python3
"""
Post-Deployment Verification Script
Comprehensive test after deployment fix
"""

import requests
import json
import time

def test_endpoint(url, headers=None, method="GET", timeout=10):
    """Test endpoint with proper method"""
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=timeout)
        elif method == "POST":
            response = requests.post(url, headers=headers, json={}, timeout=timeout)
        
        return {
            "status": "SUCCESS" if response.status_code in [200, 201] else "FAILED",
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
    print("BHIV HR Platform - Post-Deployment Verification")
    print("=" * 55)
    
    base_url = "https://bhiv-hr-gateway.onrender.com"
    headers = {"Authorization": "Bearer myverysecureapikey123"}
    
    # Step 1: Check deployment metadata
    print("1. CHECKING DEPLOYMENT METADATA")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            reported_endpoints = data.get("endpoints", 0)
            version = data.get("version", "Unknown")
            print(f"   Version: {version}")
            print(f"   Reported Endpoints: {reported_endpoints}")
            
            if reported_endpoints >= 47:
                print("   ✓ Endpoint count looks correct")
            else:
                print(f"   ✗ Expected 47+, got {reported_endpoints}")
        else:
            print(f"   ✗ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error checking metadata: {e}")
    
    print()
    
    # Step 2: Check OpenAPI spec
    print("2. CHECKING OPENAPI SPECIFICATION")
    try:
        response = requests.get(f"{base_url}/openapi.json", timeout=10)
        if response.status_code == 200:
            spec = response.json()
            actual_paths = list(spec.get('paths', {}).keys())
            print(f"   OpenAPI Paths: {len(actual_paths)}")
            
            if len(actual_paths) >= 47:
                print("   ✓ OpenAPI spec shows correct endpoint count")
            else:
                print(f"   ✗ Expected 47+, OpenAPI shows {len(actual_paths)}")
                print("   First 10 paths:")
                for path in actual_paths[:10]:
                    print(f"     {path}")
        else:
            print(f"   ✗ OpenAPI spec failed: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error checking OpenAPI: {e}")
    
    print()
    
    # Step 3: Test critical endpoints
    print("3. TESTING CRITICAL ENDPOINTS")
    critical_tests = [
        ("/", "GET", None),
        ("/health", "GET", None),
        ("/v1/jobs", "GET", headers),
        ("/v1/candidates", "GET", headers),
        ("/v1/match/1/top", "GET", headers),
        ("/metrics", "GET", None),
        ("/health/detailed", "GET", None)
    ]
    
    critical_passed = 0
    for endpoint, method, test_headers in critical_tests:
        result = test_endpoint(f"{base_url}{endpoint}", test_headers, method)
        status_icon = "✓" if result["status"] == "SUCCESS" else "✗"
        print(f"   {status_icon} {endpoint}: {result['status']} ({result.get('status_code', 'N/A')})")
        if result["status"] == "SUCCESS":
            critical_passed += 1
    
    print(f"   Critical Score: {critical_passed}/{len(critical_tests)} ({critical_passed/len(critical_tests)*100:.1f}%)")
    print()
    
    # Step 4: Test new endpoints (Security, Analytics, Documentation)
    print("4. TESTING NEW ENDPOINTS")
    new_endpoints = [
        ("/v1/security/rate-limit-status", "GET", headers),
        ("/v1/reports/hiring-funnel", "GET", headers),
        ("/v1/docs/project-structure", "GET", None),
        ("/metrics/dashboard", "GET", None)
    ]
    
    new_passed = 0
    for endpoint, method, test_headers in new_endpoints:
        result = test_endpoint(f"{base_url}{endpoint}", test_headers, method)
        status_icon = "✓" if result["status"] == "SUCCESS" else "✗"
        print(f"   {status_icon} {endpoint}: {result['status']} ({result.get('status_code', 'N/A')})")
        if result["status"] == "SUCCESS":
            new_passed += 1
    
    print(f"   New Endpoints Score: {new_passed}/{len(new_endpoints)} ({new_passed/len(new_endpoints)*100:.1f}%)")
    print()
    
    # Step 5: Overall assessment
    print("5. OVERALL ASSESSMENT")
    
    total_score = (critical_passed / len(critical_tests)) * 0.7 + (new_passed / len(new_endpoints)) * 0.3
    
    if total_score >= 0.9:
        print("   ✓ EXCELLENT: Deployment successful, all systems operational")
        status = "SUCCESS"
    elif total_score >= 0.7:
        print("   ⚠ GOOD: Most systems working, minor issues remain")
        status = "PARTIAL"
    elif total_score >= 0.5:
        print("   ⚠ FAIR: Core systems working, significant issues remain")
        status = "ISSUES"
    else:
        print("   ✗ POOR: Major deployment issues, requires immediate attention")
        status = "FAILED"
    
    print(f"   Overall Score: {total_score*100:.1f}%")
    print(f"   Status: {status}")
    
    # Step 6: Recommendations
    print()
    print("6. RECOMMENDATIONS")
    
    if status == "SUCCESS":
        print("   • Deployment completed successfully")
        print("   • All endpoints are functional")
        print("   • Platform ready for production use")
    elif status == "PARTIAL":
        print("   • Core functionality working")
        print("   • Some advanced features may need attention")
        print("   • Monitor for any remaining issues")
    elif status == "ISSUES":
        print("   • Deployment partially successful")
        print("   • Check Render logs for specific errors")
        print("   • May need additional deployment cycles")
    else:
        print("   • Deployment failed or incomplete")
        print("   • Check deployment source and trigger redeploy")
        print("   • Verify all files are updated correctly")
    
    print(f"\nVerification completed at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    return status == "SUCCESS"

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)