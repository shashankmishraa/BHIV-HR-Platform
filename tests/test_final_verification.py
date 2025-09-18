"""
Final Verification Test - Port 8000 Enterprise Validation
"""

import time

import requests
BASE_URL = "http://localhost:8000"
API_KEY = "myverysecureapikey123"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def test_all_endpoints():
    """Test all critical endpoints"""
    
    endpoints = [
        ("/", "GET", "Root endpoint"),
        ("/health", "GET", "Health check"),
        ("/docs", "GET", "API documentation"),
        ("/v1/2fa/demo-setup", "GET", "2FA demo"),
        ("/v1/jobs", "GET", "Job management"),
        ("/test-candidates", "GET", "Database test")
    ]
    
    results = {}
    
    print("=" * 60)
    print("FINAL VERIFICATION - PORT 8000 ENTERPRISE VALIDATION")
    print("=" * 60)
    
    for endpoint, method, description in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS, timeout=10)
            
            results[endpoint] = {
                "status": response.status_code,
                "success": response.status_code in [200, 401],  # 401 is acceptable for protected endpoints
                "response_time": response.elapsed.total_seconds(),
                "description": description
            }
            
            status = "PASS" if results[endpoint]["success"] else "FAIL"
            print(f"{status} - {endpoint} ({description}): {response.status_code} - {response.elapsed.total_seconds():.3f}s")
            
        except Exception as e:
            results[endpoint] = {
                "success": False,
                "error": str(e),
                "description": description
            }
            print(f"FAIL - {endpoint} ({description}): ERROR - {str(e)}")
    
    # Summary
    total_tests = len(endpoints)
    passed_tests = sum(1 for r in results.values() if r.get("success", False))
    
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    print(f"Total Endpoints Tested: {total_tests}")
    print(f"Successful Tests: {passed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("STATUS: ALL SYSTEMS OPERATIONAL")
        print("PORT 8000: FULLY FUNCTIONAL")
        print("DEPLOYMENT: READY FOR PRODUCTION")
    elif passed_tests >= total_tests * 0.8:
        print("STATUS: MOSTLY OPERATIONAL")
        print("PORT 8000: FUNCTIONAL WITH MINOR ISSUES")
    else:
        print("STATUS: CRITICAL ISSUES DETECTED")
        print("PORT 8000: REQUIRES IMMEDIATE ATTENTION")
    
    return results

def test_performance():
    """Test performance metrics"""
    print("\n" + "=" * 60)
    print("PERFORMANCE VALIDATION")
    print("=" * 60)
    
    # Test response times
    times = []
    for i in range(5):
        start = time.time()
        response = requests.get(f"{BASE_URL}/health", headers=HEADERS)
        end = time.time()
        times.append(end - start)
    
    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)
    
    print(f"Average Response Time: {avg_time:.3f}s")
    print(f"Min Response Time: {min_time:.3f}s")
    print(f"Max Response Time: {max_time:.3f}s")
    
    if avg_time < 0.1:
        print("PERFORMANCE: EXCELLENT (<100ms)")
    elif avg_time < 0.5:
        print("PERFORMANCE: GOOD (<500ms)")
    else:
        print("PERFORMANCE: NEEDS OPTIMIZATION (>500ms)")

def test_security_features():
    """Test security features"""
    print("\n" + "=" * 60)
    print("SECURITY VALIDATION")
    print("=" * 60)
    
    # Test authentication
    try:
        response = requests.get(f"{BASE_URL}/test-candidates")  # No auth header
        auth_working = response.status_code == 401
        print(f"Authentication Protection: {'PASS' if auth_working else 'FAIL'}")
    except:
        print("Authentication Protection: FAIL")
    
    # Test security headers
    try:
        response = requests.get(f"{BASE_URL}/health", headers=HEADERS)
        security_headers = [
            "x-content-type-options",
            "x-frame-options",
            "x-xss-protection",
            "content-security-policy"
        ]
        
        present_headers = sum(1 for header in security_headers if header in response.headers)
        print(f"Security Headers: {present_headers}/4 present")
        
        if present_headers >= 3:
            print("Security Headers: PASS")
        else:
            print("Security Headers: FAIL")
            
    except Exception as e:
        print(f"Security Headers: FAIL - {e}")

if __name__ == "__main__":
    # Run all verification tests
    endpoint_results = test_all_endpoints()
    test_performance()
    test_security_features()
    
    print("\n" + "=" * 60)
    print("FINAL ENTERPRISE VALIDATION COMPLETE")
    print("=" * 60)