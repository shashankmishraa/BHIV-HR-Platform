#!/usr/bin/env python3
"""
Comprehensive deployment verification script
Tests all services and endpoints after workflow fixes
"""

import requests
import time
import sys
from datetime import datetime

def test_service(name, base_url, endpoints):
    """Test a service with multiple endpoints"""
    print(f"\n🔍 Testing {name} ({base_url})")
    results = {"service": name, "base_url": base_url, "tests": []}
    
    for endpoint in endpoints:
        url = f"{base_url}{endpoint}"
        try:
            start_time = time.time()
            response = requests.get(url, timeout=10)
            duration = time.time() - start_time
            
            status = "PASS" if response.status_code == 200 else f"FAIL ({response.status_code})"
            print(f"  {endpoint}: {status} ({duration:.3f}s)")
            
            results["tests"].append({
                "endpoint": endpoint,
                "status_code": response.status_code,
                "duration": duration,
                "success": response.status_code == 200
            })
        except Exception as e:
            print(f"  {endpoint}: ERROR ({str(e)})")
            results["tests"].append({
                "endpoint": endpoint,
                "error": str(e),
                "success": False
            })
    
    return results

def main():
    print("BHIV HR Platform - Comprehensive Deployment Verification")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    # Define services and their endpoints
    services = {
        "Gateway": {
            "url": "https://bhiv-hr-gateway-46pz.onrender.com",
            "endpoints": [
                "/health",
                "/health/detailed", 
                "/health/ready",
                "/health/live",
                "/health/probe",
                "/metrics",
                "/metrics/json",
                "/",
                "/system/modules",
                "/architecture",
                "/integration/status",
                "/integration/endpoints",
                "/v1/candidates",
                "/v1/jobs",
                "/v1/auth/profile"
            ]
        },
        "AI Agent": {
            "url": "https://bhiv-hr-agent-m1me.onrender.com", 
            "endpoints": [
                "/health",
                "/health/detailed",
                "/status",
                "/metrics",
                "/metrics/json",
                "/match/candidates",
                "/analytics/performance",
                "/models/status"
            ]
        },
        "HR Portal": {
            "url": "https://bhiv-hr-portal-cead.onrender.com",
            "endpoints": ["/"]
        },
        "Client Portal": {
            "url": "https://bhiv-hr-client-portal-5g33.onrender.com",
            "endpoints": ["/"]
        }
    }
    
    all_results = []
    total_tests = 0
    passed_tests = 0
    
    # Test each service
    for service_name, config in services.items():
        results = test_service(service_name, config["url"], config["endpoints"])
        all_results.append(results)
        
        # Count results
        for test in results["tests"]:
            total_tests += 1
            if test.get("success", False):
                passed_tests += 1
    
    # Summary
    print(f"\nVERIFICATION SUMMARY")
    print("=" * 30)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    # Service status
    print(f"\nSERVICE STATUS")
    print("=" * 20)
    for results in all_results:
        service_tests = results["tests"]
        service_passed = sum(1 for t in service_tests if t.get("success", False))
        service_total = len(service_tests)
        status = "HEALTHY" if service_passed == service_total else "PARTIAL" if service_passed > 0 else "DOWN"
        print(f"{results['service']}: {status} ({service_passed}/{service_total})")
    
    # Performance summary
    print(f"\nPERFORMANCE SUMMARY")
    print("=" * 25)
    for results in all_results:
        durations = [t.get("duration", 0) for t in results["tests"] if t.get("success", False)]
        if durations:
            avg_duration = sum(durations) / len(durations)
            print(f"{results['service']}: {avg_duration:.3f}s average")
    
    # Exit with appropriate code
    if passed_tests == total_tests:
        print(f"\nALL SYSTEMS OPERATIONAL!")
        return 0
    else:
        print(f"\n{total_tests - passed_tests} issues detected")
        return 1

if __name__ == "__main__":
    sys.exit(main())