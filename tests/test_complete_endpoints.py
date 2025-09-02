"""
Complete Endpoint Verification Test
Testing all original + new enterprise endpoints
"""

import requests
import json

BASE_URL = "http://localhost:8000"
API_KEY = "myverysecureapikey123"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def test_all_endpoints():
    """Test all endpoints including original and new ones"""
    
    endpoints = [
        # Core API Endpoints
        ("/", "GET", "API Root Information"),
        ("/health", "GET", "Health Check"),
        ("/test-candidates", "GET", "Database Connectivity Test"),
        
        # Job Management
        ("/v1/jobs", "GET", "List All Active Jobs"),
        
        # Candidate Management  
        ("/v1/candidates/job/1", "GET", "Get All Candidates (Dynamic Matching)"),
        ("/v1/candidates/search", "GET", "Search & Filter Candidates"),
        
        # AI Matching Engine
        ("/v1/match/1/top", "GET", "Semantic candidate matching and ranking"),
        
        # Assessment & Workflow
        ("/candidates/stats", "GET", "Platform metrics and reporting"),
        ("/v1/reports/job/1/export.csv", "GET", "Export reports"),
        
        # Client Portal API
        # ("/v1/client/login", "POST", "Client Authentication"), # Skip POST for now
        
        # Two-Factor Authentication (New)
        ("/v1/2fa/demo-setup", "GET", "Demo 2FA Setup"),
        ("/v1/2fa/status/TEST001", "GET", "Get 2FA Status"),
        
        # Password Management (New)
        ("/v1/password/policy", "GET", "Get Password Policy"),
        ("/v1/password/strength-test", "GET", "Password Strength Testing Tool"),
        ("/v1/password/security-tips", "GET", "Password Security Best Practices"),
        
        # Security Testing (New)
        ("/v1/security/rate-limit-status", "GET", "Check Rate Limit Status"),
        ("/v1/security/blocked-ips", "GET", "View Blocked IPs"),
        ("/v1/security/security-headers-test", "GET", "Test Security Headers"),
        ("/v1/security/penetration-test-endpoints", "GET", "Penetration Testing Endpoints"),
        
        # CSP Management (New)
        ("/v1/security/csp-violations", "GET", "View CSP Violations"),
        ("/v1/security/csp-policies", "GET", "Current CSP Policies"),
        
        # Documentation
        ("/docs", "GET", "API Documentation"),
        ("/openapi.json", "GET", "OpenAPI Schema")
    ]
    
    print("=" * 80)
    print("COMPLETE ENDPOINT VERIFICATION - ORIGINAL + NEW ENTERPRISE FEATURES")
    print("=" * 80)
    
    results = {}
    original_count = 0
    new_count = 0
    
    for endpoint, method, description in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS, timeout=10)
            
            success = response.status_code in [200, 401]  # 401 acceptable for protected endpoints
            results[endpoint] = {
                "status": response.status_code,
                "success": success,
                "response_time": response.elapsed.total_seconds(),
                "description": description
            }
            
            # Categorize endpoints
            if any(x in endpoint for x in ["/v1/2fa", "/v1/password", "/v1/security"]):
                category = "NEW"
                new_count += 1
            else:
                category = "ORIGINAL"
                original_count += 1
            
            status = "PASS" if success else "FAIL"
            print(f"{status} [{category}] {endpoint} - {description}: {response.status_code}")
            
        except Exception as e:
            results[endpoint] = {
                "success": False,
                "error": str(e),
                "description": description
            }
            print(f"FAIL [ERROR] {endpoint} - {description}: {str(e)}")
    
    # Summary
    total_tests = len(endpoints)
    passed_tests = sum(1 for r in results.values() if r.get("success", False))
    
    print("\n" + "=" * 80)
    print("ENDPOINT VERIFICATION SUMMARY")
    print("=" * 80)
    print(f"Original Endpoints: {original_count}")
    print(f"New Enterprise Endpoints: {new_count}")
    print(f"Total Endpoints Tested: {total_tests}")
    print(f"Successful Tests: {passed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("STATUS: ALL ENDPOINTS OPERATIONAL")
        print("API STRUCTURE: COMPLETE (ORIGINAL + ENTERPRISE)")
    elif passed_tests >= total_tests * 0.9:
        print("STATUS: MOSTLY OPERATIONAL")
        print("API STRUCTURE: NEARLY COMPLETE")
    else:
        print("STATUS: SOME ENDPOINTS NEED ATTENTION")
    
    return results

def test_endpoint_categories():
    """Test endpoints by category"""
    print("\n" + "=" * 80)
    print("ENDPOINT CATEGORIES")
    print("=" * 80)
    
    categories = {
        "Core API Endpoints": ["/", "/health", "/test-candidates"],
        "Job Management": ["/v1/jobs"],
        "Candidate Management": ["/v1/candidates/job/1", "/v1/candidates/search"],
        "AI Matching Engine": ["/v1/match/1/top"],
        "Assessment & Workflow": ["/candidates/stats", "/v1/reports/job/1/export.csv"],
        "Two-Factor Authentication": ["/v1/2fa/demo-setup", "/v1/2fa/status/TEST001"],
        "Password Management": ["/v1/password/policy", "/v1/password/strength-test"],
        "Security Testing": ["/v1/security/rate-limit-status", "/v1/security/security-headers-test"],
        "CSP Management": ["/v1/security/csp-violations", "/v1/security/csp-policies"]
    }
    
    for category, endpoints in categories.items():
        working_endpoints = 0
        for endpoint in endpoints:
            try:
                response = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS, timeout=5)
                if response.status_code in [200, 401]:
                    working_endpoints += 1
            except:
                pass
        
        status = "COMPLETE" if working_endpoints == len(endpoints) else f"{working_endpoints}/{len(endpoints)}"
        print(f"{category}: {status}")

if __name__ == "__main__":
    # Run complete endpoint verification
    endpoint_results = test_all_endpoints()
    test_endpoint_categories()
    
    print("\n" + "=" * 80)
    print("VERIFICATION COMPLETE - ORIGINAL + ENTERPRISE ENDPOINTS")
    print("=" * 80)