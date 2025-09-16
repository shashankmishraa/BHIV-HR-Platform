#!/usr/bin/env python3
"""
Comprehensive Endpoint Testing Suite
Tests all 50 endpoints across Gateway and AI Agent services
"""

import requests
import json
import time
from datetime import datetime
import sys

# Configuration
GATEWAY_BASE = "http://localhost:8000"
AGENT_BASE = "http://localhost:9000"
API_KEY = "myverysecureapikey123"

class EndpointTester:
    def __init__(self):
        self.results = []
        self.headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        
    def test_endpoint(self, method, url, data=None, auth_required=True, expected_status=200):
        """Test individual endpoint"""
        try:
            headers = self.headers if auth_required else {"Content-Type": "application/json"}
            
            start_time = time.time()
            if method == "GET":
                response = requests.get(url, headers=headers, timeout=10)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=data, timeout=10)
            elif method == "PUT":
                response = requests.put(url, headers=headers, json=data, timeout=10)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers, timeout=10)
            
            response_time = time.time() - start_time
            
            success = response.status_code == expected_status
            result = {
                "endpoint": f"{method} {url}",
                "status_code": response.status_code,
                "expected": expected_status,
                "success": success,
                "response_time": round(response_time * 1000, 2),
                "response_size": len(response.content)
            }
            
            if success:
                try:
                    result["response_data"] = response.json()
                except:
                    result["response_data"] = response.text[:200]
            else:
                result["error"] = response.text[:200]
            
            self.results.append(result)
            return result
            
        except Exception as e:
            result = {
                "endpoint": f"{method} {url}",
                "status_code": 0,
                "expected": expected_status,
                "success": False,
                "response_time": 0,
                "error": str(e)
            }
            self.results.append(result)
            return result
    
    def test_gateway_core_endpoints(self):
        """Test Gateway Core API Endpoints (3)"""
        print("Testing Gateway Core Endpoints...")
        
        self.test_endpoint("GET", f"{GATEWAY_BASE}/", auth_required=False)
        self.test_endpoint("GET", f"{GATEWAY_BASE}/health", auth_required=False)
        self.test_endpoint("GET", f"{GATEWAY_BASE}/test-candidates")
    
    def test_job_management(self):
        """Test Job Management Endpoints (2)"""
        print("Testing Job Management...")
        
        # Create job
        job_data = {
            "title": "Test Developer",
            "department": "Engineering",
            "location": "Remote",
            "experience_level": "Mid",
            "requirements": "Python, React, 3+ years",
            "description": "Test job posting"
        }
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/jobs", data=job_data)
        
        # List jobs
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/jobs")
    
    def test_candidate_management(self):
        """Test Candidate Management Endpoints (3)"""
        print("Testing Candidate Management...")
        
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/candidates/job/1")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/candidates/search?skills=python")
        
        # Bulk upload
        bulk_data = {
            "candidates": [{
                "name": "Test Candidate",
                "email": f"test{int(time.time())}@example.com",
                "technical_skills": "Python, Django",
                "experience_years": 3
            }]
        }
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/candidates/bulk", data=bulk_data)
    
    def test_ai_matching(self):
        """Test AI Matching Endpoints (2)"""
        print("Testing AI Matching...")
        
        # Gateway matching
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/match/1/top?limit=5")
        
        # Agent matching
        match_data = {"job_id": 1}
        self.test_endpoint("POST", f"{AGENT_BASE}/match", data=match_data, auth_required=False)
    
    def test_assessment_workflow(self):
        """Test Assessment & Workflow Endpoints (3)"""
        print("Testing Assessment & Workflow...")
        
        # Submit feedback
        feedback_data = {
            "candidate_id": 1,
            "job_id": 1,
            "integrity": 5,
            "honesty": 4,
            "discipline": 5,
            "hard_work": 4,
            "gratitude": 5,
            "comments": "Test feedback"
        }
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/feedback", data=feedback_data)
        
        # Get interviews
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/interviews")
        
        # Schedule interview
        interview_data = {
            "candidate_id": 1,
            "job_id": 1,
            "interview_date": "2025-01-20T10:00:00",
            "interviewer": "Test Interviewer"
        }
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/interviews", data=interview_data)
    
    def test_client_portal(self):
        """Test Client Portal API (1)"""
        print("Testing Client Portal...")
        
        login_data = {"client_id": "TECH001", "password": "demo123"}
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/client/login", data=login_data, auth_required=False)
    
    def test_security_endpoints(self):
        """Test Security Testing Endpoints (7)"""
        print("Testing Security Endpoints...")
        
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/security/rate-limit-status")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/security/blocked-ips")
        
        # Input validation tests
        xss_data = {"input_data": "<script>alert('xss')</script>"}
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/security/test-input-validation", data=xss_data)
        
        email_data = {"email": "test@example.com"}
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/security/test-email-validation", data=email_data)
        
        phone_data = {"phone": "+1-555-123-4567"}
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/security/test-phone-validation", data=phone_data)
        
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/security/security-headers-test")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/security/penetration-test-endpoints")
    
    def test_csp_management(self):
        """Test CSP Management Endpoints (4)"""
        print("Testing CSP Management...")
        
        csp_report_data = {
            "violated_directive": "script-src",
            "blocked_uri": "https://malicious.com/script.js",
            "document_uri": "https://example.com/page"
        }
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/security/csp-report", data=csp_report_data)
        
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/security/csp-violations")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/security/csp-policies")
        
        csp_policy_data = {"policy": "default-src 'self'"}
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/security/test-csp-policy", data=csp_policy_data)
    
    def test_2fa_endpoints(self):
        """Test Two-Factor Authentication Endpoints (8)"""
        print("Testing 2FA Endpoints...")
        
        setup_data = {"user_id": "TECH001"}
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/2fa/setup", data=setup_data)
        
        verify_data = {"user_id": "TECH001", "totp_code": "123456"}
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/2fa/verify-setup", data=verify_data, expected_status=401)
        
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/2fa/login-with-2fa", data=verify_data, expected_status=401)
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/2fa/status/TECH001")
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/2fa/disable", data=setup_data)
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/2fa/regenerate-backup-codes", data=setup_data)
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/2fa/test-token/TECH001/123456")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/2fa/demo-setup")
    
    def test_password_management(self):
        """Test Password Management Endpoints (6)"""
        print("Testing Password Management...")
        
        password_data = {"password": "StrongPass123!"}
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/password/validate", data=password_data)
        
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/password/generate?length=12")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/password/policy")
        
        change_data = {"old_password": "old123", "new_password": "new123"}
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/password/change", data=change_data)
        
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/password/strength-test")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/password/security-tips")
    
    def test_analytics_statistics(self):
        """Test Analytics & Statistics Endpoints (2)"""
        print("Testing Analytics & Statistics...")
        
        self.test_endpoint("GET", f"{GATEWAY_BASE}/candidates/stats")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/reports/job/1/export.csv")
    
    def test_monitoring_endpoints(self):
        """Test Monitoring Endpoints (3)"""
        print("Testing Monitoring...")
        
        self.test_endpoint("GET", f"{GATEWAY_BASE}/metrics", auth_required=False)
        self.test_endpoint("GET", f"{GATEWAY_BASE}/health/detailed", auth_required=False)
        self.test_endpoint("GET", f"{GATEWAY_BASE}/metrics/dashboard", auth_required=False)
    
    def test_agent_endpoints(self):
        """Test AI Agent Endpoints (4)"""
        print("Testing AI Agent...")
        
        self.test_endpoint("GET", f"{AGENT_BASE}/", auth_required=False)
        self.test_endpoint("GET", f"{AGENT_BASE}/health", auth_required=False)
        self.test_endpoint("GET", f"{AGENT_BASE}/test-db", auth_required=False)
        self.test_endpoint("GET", f"{AGENT_BASE}/analyze/1", auth_required=False)
    
    def run_all_tests(self):
        """Run comprehensive test suite"""
        print("BHIV HR Platform - Comprehensive Endpoint Testing")
        print("=" * 60)
        print(f"Start Time: {datetime.now().isoformat()}")
        print(f"Gateway: {GATEWAY_BASE}")
        print(f"Agent: {AGENT_BASE}")
        print("=" * 60)
        
        # Run all test categories
        test_categories = [
            ("Gateway Core", self.test_gateway_core_endpoints),
            ("Job Management", self.test_job_management),
            ("Candidate Management", self.test_candidate_management),
            ("AI Matching", self.test_ai_matching),
            ("Assessment & Workflow", self.test_assessment_workflow),
            ("Client Portal", self.test_client_portal),
            ("Security Testing", self.test_security_endpoints),
            ("CSP Management", self.test_csp_management),
            ("Two-Factor Auth", self.test_2fa_endpoints),
            ("Password Management", self.test_password_management),
            ("Analytics & Statistics", self.test_analytics_statistics),
            ("Monitoring", self.test_monitoring_endpoints),
            ("AI Agent", self.test_agent_endpoints)
        ]
        
        for category_name, test_func in test_categories:
            print(f"\n{category_name}")
            print("-" * 40)
            try:
                test_func()
            except Exception as e:
                print(f"ERROR in {category_name}: {str(e)}")
        
        self.print_summary()
    
    def print_summary(self):
        """Print test results summary"""
        print("\n" + "=" * 60)
        print("TEST RESULTS SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Endpoints Tested: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%")
        
        # Response time statistics
        response_times = [r["response_time"] for r in self.results if r["success"]]
        if response_times:
            avg_time = sum(response_times) / len(response_times)
            max_time = max(response_times)
            print(f"Average Response Time: {avg_time:.2f}ms")
            print(f"Max Response Time: {max_time:.2f}ms")
        
        # Failed tests details
        if failed_tests > 0:
            print("\nFAILED TESTS:")
            print("-" * 40)
            for result in self.results:
                if not result["success"]:
                    print(f"FAIL {result['endpoint']} - Status: {result['status_code']}")
                    if "error" in result:
                        print(f"     Error: {result['error'][:100]}")
        
        # Successful tests summary
        print("\nSUCCESSFUL TESTS BY CATEGORY:")
        print("-" * 40)
        categories = {}
        for result in self.results:
            if result["success"]:
                endpoint = result["endpoint"]
                if "/v1/jobs" in endpoint:
                    category = "Job Management"
                elif "/v1/candidates" in endpoint:
                    category = "Candidate Management"
                elif "/v1/security" in endpoint:
                    category = "Security"
                elif "/v1/2fa" in endpoint:
                    category = "Two-Factor Auth"
                elif "/v1/password" in endpoint:
                    category = "Password Management"
                elif "/match" in endpoint:
                    category = "AI Matching"
                elif "/health" in endpoint or "/metrics" in endpoint:
                    category = "Monitoring"
                else:
                    category = "Other"
                
                categories[category] = categories.get(category, 0) + 1
        
        for category, count in sorted(categories.items()):
            print(f"{category}: {count} endpoints")
        
        print("\n" + "=" * 60)
        if passed_tests == total_tests:
            print("ALL TESTS PASSED! Platform is fully functional.")
        elif passed_tests >= total_tests * 0.9:
            print("MOSTLY SUCCESSFUL! Minor issues detected.")
        else:
            print("ISSUES DETECTED! Check failed endpoints above.")
        
        return passed_tests == total_tests

def main():
    """Run endpoint testing"""
    tester = EndpointTester()
    success = tester.run_all_tests()
    
    # Save detailed results
    with open('endpoint_test_results.json', 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "total_tests": len(tester.results),
            "passed": sum(1 for r in tester.results if r["success"]),
            "results": tester.results
        }, f, indent=2)
    
    print(f"\nDetailed results saved to: endpoint_test_results.json")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())