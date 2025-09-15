#!/usr/bin/env python3
"""
BHIV HR Platform - Complete Endpoint Testing Script
Tests all 47 endpoints for functionality and response validation
"""

import requests
import json
import time
from datetime import datetime
import pyotp

# Configuration
BASE_URL = "http://localhost:8000"  # Change to your deployment URL
API_KEY = "myverysecureapikey123"
CLIENT_CREDENTIALS = {"client_id": "TECH001", "password": "demo123"}

class EndpointTester:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {api_key}"}
        self.client_token = None
        self.test_results = []
        
    def test_endpoint(self, method, endpoint, data=None, headers=None, expected_status=200):
        """Test a single endpoint"""
        url = f"{self.base_url}{endpoint}"
        test_headers = headers or self.headers
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=test_headers, timeout=10)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, headers=test_headers, timeout=10)
            elif method.upper() == "PUT":
                response = requests.put(url, json=data, headers=test_headers, timeout=10)
            
            success = response.status_code == expected_status
            result = {
                "endpoint": endpoint,
                "method": method,
                "status_code": response.status_code,
                "expected": expected_status,
                "success": success,
                "response_size": len(response.text),
                "response_time": response.elapsed.total_seconds()
            }
            
            if success:
                try:
                    result["response_data"] = response.json()
                except:
                    result["response_data"] = response.text[:100]
            else:
                result["error"] = response.text[:200]
                
            self.test_results.append(result)
            return result
            
        except Exception as e:
            result = {
                "endpoint": endpoint,
                "method": method,
                "success": False,
                "error": str(e),
                "status_code": 0
            }
            self.test_results.append(result)
            return result
    
    def run_all_tests(self):
        """Run tests for all 47 endpoints"""
        print("🚀 Starting comprehensive endpoint testing...")
        print("=" * 60)
        
        # 1. Core API Endpoints (3)
        print("\n📋 Testing Core API Endpoints...")
        self.test_endpoint("GET", "/")
        self.test_endpoint("GET", "/health")
        self.test_endpoint("GET", "/test-candidates")
        
        # 2. Monitoring (3)
        print("\n📊 Testing Monitoring Endpoints...")
        self.test_endpoint("GET", "/metrics")
        self.test_endpoint("GET", "/health/detailed")
        self.test_endpoint("GET", "/metrics/dashboard")
        
        # 3. Client Portal Authentication (5)
        print("\n🔐 Testing Client Portal Authentication...")
        
        # Login to get client token
        login_result = self.test_endpoint("POST", "/v1/client/login", 
                                        data=CLIENT_CREDENTIALS, headers={})
        if login_result["success"]:
            self.client_token = login_result["response_data"]["access_token"]
            client_headers = {"Authorization": f"Bearer {self.client_token}"}
            
            # Test other client endpoints
            self.test_endpoint("GET", "/v1/client/verify", headers=client_headers)
            self.test_endpoint("POST", "/v1/client/refresh", 
                             data={"refresh_token": login_result["response_data"]["refresh_token"]}, 
                             headers={})
            self.test_endpoint("POST", "/v1/client/logout", 
                             data={"access_token": self.client_token}, headers={})
        
        # 4. Job Management (2)
        print("\n💼 Testing Job Management...")
        job_data = {
            "title": "Test Developer",
            "department": "Engineering",
            "location": "Remote",
            "experience_level": "Mid-level",
            "requirements": "Python, FastAPI",
            "description": "Test job posting"
        }
        self.test_endpoint("POST", "/v1/jobs", data=job_data)
        self.test_endpoint("GET", "/v1/jobs")
        
        # 5. Candidate Management (3)
        print("\n👥 Testing Candidate Management...")
        self.test_endpoint("GET", "/v1/candidates/job/1")
        self.test_endpoint("GET", "/v1/candidates/search?skills=python&location=remote")
        
        bulk_data = {
            "candidates": [
                {
                    "name": "Test Candidate",
                    "email": "test@example.com",
                    "phone": "123-456-7890",
                    "location": "Remote",
                    "experience_years": 3,
                    "technical_skills": "Python, JavaScript"
                }
            ]
        }
        self.test_endpoint("POST", "/v1/candidates/bulk", data=bulk_data)
        
        # 6. AI Matching (1)
        print("\n🤖 Testing AI Matching...")
        self.test_endpoint("GET", "/v1/match/1/top?limit=5")
        
        # 7. Assessment & Workflow (4)
        print("\n📝 Testing Assessment & Workflow...")
        feedback_data = {
            "candidate_id": 1,
            "job_id": 1,
            "integrity": 5,
            "honesty": 5,
            "discipline": 4,
            "hard_work": 5,
            "gratitude": 4
        }
        self.test_endpoint("POST", "/v1/feedback", data=feedback_data)
        self.test_endpoint("GET", "/v1/interviews")
        
        interview_data = {
            "candidate_id": 1,
            "job_id": 1,
            "interview_date": "2025-02-01T10:00:00",
            "interviewer": "HR Manager"
        }
        self.test_endpoint("POST", "/v1/interviews", data=interview_data)
        
        offer_data = {
            "candidate_id": 1,
            "job_id": 1,
            "salary": 75000.0,
            "start_date": "2025-03-01",
            "terms": "Full-time employment"
        }
        self.test_endpoint("POST", "/v1/offers", data=offer_data)
        
        # 8. Analytics (2)
        print("\n📈 Testing Analytics...")
        self.test_endpoint("GET", "/candidates/stats")
        self.test_endpoint("GET", "/v1/reports/job/1/export.csv")
        
        # 9. Security Testing (7)
        print("\n🔒 Testing Security Endpoints...")
        self.test_endpoint("GET", "/v1/security/rate-limit-status")
        self.test_endpoint("GET", "/v1/security/blocked-ips")
        
        self.test_endpoint("POST", "/v1/security/test-input-validation", 
                         data={"input_data": "test input"})
        self.test_endpoint("POST", "/v1/security/test-email-validation", 
                         data={"email": "test@example.com"})
        self.test_endpoint("POST", "/v1/security/test-phone-validation", 
                         data={"phone": "123-456-7890"})
        
        self.test_endpoint("GET", "/v1/security/security-headers-test")
        self.test_endpoint("GET", "/v1/security/penetration-test-endpoints")
        
        # 10. Two-Factor Authentication (8)
        print("\n🔐 Testing 2FA Endpoints...")
        self.test_endpoint("POST", "/v1/2fa/setup", data={"user_id": "testuser"})
        
        # Generate valid TOTP for testing
        totp = pyotp.TOTP("JBSWY3DPEHPK3PXP")
        current_token = totp.now()
        
        self.test_endpoint("POST", "/v1/2fa/verify-setup", 
                         data={"user_id": "testuser", "totp_code": current_token})
        self.test_endpoint("POST", "/v1/2fa/login-with-2fa", 
                         data={"user_id": "testuser", "totp_code": current_token})
        
        self.test_endpoint("GET", "/v1/2fa/status/testuser")
        self.test_endpoint("POST", "/v1/2fa/disable", data={"user_id": "testuser"})
        self.test_endpoint("POST", "/v1/2fa/regenerate-backup-codes", data={"user_id": "testuser"})
        self.test_endpoint("GET", f"/v1/2fa/test-token/testuser/{current_token}")
        self.test_endpoint("GET", "/v1/2fa/demo-setup")
        
        # 11. Password Management (6)
        print("\n🔑 Testing Password Management...")
        self.test_endpoint("POST", "/v1/password/validate", 
                         data={"password": "StrongPass123!"})
        self.test_endpoint("POST", "/v1/password/generate?length=16")
        self.test_endpoint("GET", "/v1/password/policy")
        
        self.test_endpoint("POST", "/v1/password/change", 
                         data={"old_password": "old123", "new_password": "new123"})
        self.test_endpoint("GET", "/v1/password/strength-test")
        self.test_endpoint("GET", "/v1/password/security-tips")
        
        # 12. CSP Management (4)
        print("\n🛡️ Testing CSP Management...")
        csp_report_data = {
            "violated_directive": "script-src",
            "blocked_uri": "https://malicious.com/script.js",
            "document_uri": "https://example.com/page"
        }
        self.test_endpoint("POST", "/v1/security/csp-report", data=csp_report_data)
        self.test_endpoint("GET", "/v1/security/csp-violations")
        self.test_endpoint("GET", "/v1/security/csp-policies")
        self.test_endpoint("POST", "/v1/security/test-csp-policy", 
                         data={"policy": "default-src 'self'"})
        
        # Generate test report
        self.generate_report()
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 60)
        print("📊 ENDPOINT TESTING REPORT")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        successful_tests = sum(1 for r in self.test_results if r["success"])
        failed_tests = total_tests - successful_tests
        
        print(f"Total Endpoints Tested: {total_tests}")
        print(f"Successful Tests: {successful_tests}")
        print(f"Failed Tests: {failed_tests}")
        print(f"Success Rate: {(successful_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print(f"\n❌ FAILED TESTS ({failed_tests}):")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['method']} {result['endpoint']}: {result.get('error', 'Unknown error')}")
        
        print(f"\n✅ SUCCESSFUL TESTS ({successful_tests}):")
        categories = {
            "Core API": 0, "Monitoring": 0, "Client Portal": 0, "Job Management": 0,
            "Candidate Management": 0, "AI Matching": 0, "Assessment": 0, "Analytics": 0,
            "Security Testing": 0, "2FA": 0, "Password Management": 0, "CSP Management": 0
        }
        
        for result in self.test_results:
            if result["success"]:
                endpoint = result["endpoint"]
                if endpoint in ["/", "/health", "/test-candidates"]:
                    categories["Core API"] += 1
                elif "/metrics" in endpoint or "/health/detailed" in endpoint:
                    categories["Monitoring"] += 1
                elif "/v1/client/" in endpoint:
                    categories["Client Portal"] += 1
                elif "/v1/jobs" in endpoint:
                    categories["Job Management"] += 1
                elif "/v1/candidates/" in endpoint:
                    categories["Candidate Management"] += 1
                elif "/v1/match/" in endpoint:
                    categories["AI Matching"] += 1
                elif endpoint in ["/v1/feedback", "/v1/interviews", "/v1/offers"]:
                    categories["Assessment"] += 1
                elif "/candidates/stats" in endpoint or "/v1/reports/" in endpoint:
                    categories["Analytics"] += 1
                elif "/v1/security/" in endpoint and "/csp" not in endpoint:
                    categories["Security Testing"] += 1
                elif "/v1/2fa/" in endpoint:
                    categories["2FA"] += 1
                elif "/v1/password/" in endpoint:
                    categories["Password Management"] += 1
                elif "/csp" in endpoint:
                    categories["CSP Management"] += 1
        
        for category, count in categories.items():
            print(f"  - {category}: {count} endpoints")
        
        # Performance summary
        response_times = [r.get("response_time", 0) for r in self.test_results if r["success"]]
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            print(f"\n⚡ PERFORMANCE:")
            print(f"  - Average Response Time: {avg_response_time:.3f}s")
            print(f"  - Fastest Response: {min(response_times):.3f}s")
            print(f"  - Slowest Response: {max(response_times):.3f}s")
        
        print(f"\n🎯 OVERALL STATUS: {'✅ PASSED' if failed_tests == 0 else '❌ NEEDS ATTENTION'}")

def main():
    """Main test execution"""
    print("BHIV HR Platform - Endpoint Functionality Testing")
    print("=" * 60)
    print(f"Base URL: {BASE_URL}")
    print(f"API Key: {API_KEY[:10]}...")
    print(f"Test Started: {datetime.now()}")
    
    tester = EndpointTester(BASE_URL, API_KEY)
    tester.run_all_tests()

if __name__ == "__main__":
    main()