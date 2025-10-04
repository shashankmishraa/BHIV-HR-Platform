#!/usr/bin/env python3
"""
BHIV HR Platform - Comprehensive Dynamic Testing Suite
Tests all 53 endpoints with unique datasets and verifies database integration
"""

import requests
import json
import time
import random
import string
from datetime import datetime, timedelta
import uuid

class DynamicTester:
    def __init__(self):
        self.gateway_url = "https://bhiv-hr-gateway-46pz.onrender.com"
        self.agent_url = "https://bhiv-hr-agent-m1me.onrender.com"
        self.api_key = "Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
        self.headers = {"Authorization": self.api_key, "Content-Type": "application/json"}
        
        # Track created data for verification
        self.created_data = {
            'jobs': [],
            'candidates': [],
            'feedback': [],
            'interviews': [],
            'offers': []
        }
        
        self.test_results = []
        self.unique_id = str(uuid.uuid4())[:8]
    
    def generate_unique_candidate(self):
        """Generate unique candidate data"""
        return {
            "name": f"TestCandidate_{self.unique_id}_{random.randint(1000, 9999)}",
            "email": f"test_{self.unique_id}_{random.randint(1000, 9999)}@dynamictest.com",
            "phone": f"+1-555-{random.randint(1000, 9999)}",
            "location": random.choice(["New York", "San Francisco", "Remote", "Chicago", "Austin"]),
            "experience_years": random.randint(1, 15),
            "technical_skills": random.choice([
                "Python, Django, PostgreSQL, AWS",
                "JavaScript, React, Node.js, MongoDB", 
                "Java, Spring Boot, MySQL, Docker",
                "C#, .NET, SQL Server, Azure",
                "Go, Kubernetes, Redis, GCP"
            ]),
            "seniority_level": random.choice(["Junior", "Mid-level", "Senior", "Lead"]),
            "education_level": random.choice(["Bachelor's", "Master's", "PhD", "Bootcamp"])
        }
    
    def generate_unique_job(self):
        """Generate unique job data"""
        return {
            "title": f"DynamicTest_{self.unique_id}_Engineer_{random.randint(100, 999)}",
            "department": random.choice(["Engineering", "Data Science", "DevOps", "QA", "Product"]),
            "location": random.choice(["Remote", "New York", "San Francisco", "Austin"]),
            "experience_level": random.choice(["Junior", "Mid-level", "Senior"]),
            "requirements": f"Dynamic testing skills, {random.choice(['Python', 'JavaScript', 'Java'])}, {random.choice(['AWS', 'Azure', 'GCP'])}",
            "description": f"Dynamic test position created at {datetime.now().isoformat()}"
        }
    
    def test_endpoint(self, name, method, url, data=None, expected_status=200):
        """Test individual endpoint and record results"""
        try:
            start_time = time.time()
            
            if method == "GET":
                response = requests.get(url, headers=self.headers, timeout=30)
            elif method == "POST":
                response = requests.post(url, headers=self.headers, json=data, timeout=30)
            elif method == "PUT":
                response = requests.put(url, headers=self.headers, json=data, timeout=30)
            elif method == "DELETE":
                response = requests.delete(url, headers=self.headers, timeout=30)
            
            response_time = time.time() - start_time
            
            result = {
                'name': name,
                'method': method,
                'url': url,
                'status_code': response.status_code,
                'response_time': round(response_time * 1000, 2),
                'success': response.status_code == expected_status,
                'data_sent': data,
                'response_data': None,
                'error': None
            }
            
            try:
                result['response_data'] = response.json()
            except:
                result['response_data'] = response.text[:200]
            
            self.test_results.append(result)
            
            status = "PASS" if result['success'] else "FAIL"
            print(f"{len(self.test_results):2d}. {name}: {status} ({response.status_code}) - {response_time*1000:.0f}ms")
            
            return result
            
        except Exception as e:
            result = {
                'name': name,
                'method': method,
                'url': url,
                'status_code': 0,
                'response_time': 0,
                'success': False,
                'data_sent': data,
                'response_data': None,
                'error': str(e)
            }
            self.test_results.append(result)
            print(f"{len(self.test_results):2d}. {name}: ERROR - {str(e)[:50]}")
            return result
    
    def run_comprehensive_tests(self):
        """Run all 53 endpoints with dynamic data"""
        print("BHIV HR Platform - Comprehensive Dynamic Testing")
        print("=" * 60)
        print(f"Test Session ID: {self.unique_id}")
        print(f"Started: {datetime.now().isoformat()}")
        print()
        
        # GATEWAY SERVICE TESTS (48 endpoints)
        print("GATEWAY SERVICE ENDPOINTS (48 total):")
        print("-" * 40)
        
        # Core API (7 endpoints)
        print("\n1. CORE API ENDPOINTS:")
        self.test_endpoint("Gateway Root", "GET", f"{self.gateway_url}/")
        self.test_endpoint("Gateway Health", "GET", f"{self.gateway_url}/health")
        self.test_endpoint("Test Candidates DB", "GET", f"{self.gateway_url}/test-candidates")
        self.test_endpoint("Prometheus Metrics", "GET", f"{self.gateway_url}/metrics")
        self.test_endpoint("Detailed Health", "GET", f"{self.gateway_url}/health/detailed")
        self.test_endpoint("Metrics Dashboard", "GET", f"{self.gateway_url}/metrics/dashboard")
        self.test_endpoint("Candidate Stats", "GET", f"{self.gateway_url}/candidates/stats")
        
        # Job Management (2 endpoints)
        print("\n2. JOB MANAGEMENT:")
        self.test_endpoint("List Jobs", "GET", f"{self.gateway_url}/v1/jobs")
        
        # Create dynamic job
        job_data = self.generate_unique_job()
        job_result = self.test_endpoint("Create Job", "POST", f"{self.gateway_url}/v1/jobs", job_data, 200)
        if job_result['success'] and job_result['response_data']:
            job_id = job_result['response_data'].get('job_id')
            if job_id:
                self.created_data['jobs'].append({'id': job_id, 'data': job_data})
        
        # Candidate Management (5 endpoints)
        print("\n3. CANDIDATE MANAGEMENT:")
        self.test_endpoint("List Candidates", "GET", f"{self.gateway_url}/v1/candidates?limit=10")
        self.test_endpoint("Get Candidate by ID", "GET", f"{self.gateway_url}/v1/candidates/1")
        self.test_endpoint("Search Candidates", "GET", f"{self.gateway_url}/v1/candidates/search?skills=Python&limit=5")
        
        # Bulk upload dynamic candidates
        candidates_data = [self.generate_unique_candidate() for _ in range(3)]
        bulk_result = self.test_endpoint("Bulk Upload Candidates", "POST", 
                                       f"{self.gateway_url}/v1/candidates/bulk", 
                                       {"candidates": candidates_data}, 200)
        if bulk_result['success']:
            self.created_data['candidates'].extend(candidates_data)
        
        # Get candidates for job
        if self.created_data['jobs']:
            job_id = self.created_data['jobs'][0]['id']
            self.test_endpoint("Get Candidates for Job", "GET", f"{self.gateway_url}/v1/candidates/job/{job_id}")
        else:
            self.test_endpoint("Get Candidates for Job", "GET", f"{self.gateway_url}/v1/candidates/job/1")
        
        # AI Matching (1 endpoint)
        print("\n4. AI MATCHING:")
        if self.created_data['jobs']:
            job_id = self.created_data['jobs'][0]['id']
            self.test_endpoint("Get Top Matches", "GET", f"{self.gateway_url}/v1/match/{job_id}/top?limit=5")
        else:
            self.test_endpoint("Get Top Matches", "GET", f"{self.gateway_url}/v1/match/1/top?limit=5")
        
        # Assessment & Workflow (6 endpoints)
        print("\n5. ASSESSMENT & WORKFLOW:")
        self.test_endpoint("Get All Feedback", "GET", f"{self.gateway_url}/v1/feedback")
        
        # Submit dynamic feedback
        feedback_data = {
            "candidate_id": 1,
            "job_id": self.created_data['jobs'][0]['id'] if self.created_data['jobs'] else 1,
            "integrity": random.randint(3, 5),
            "honesty": random.randint(3, 5),
            "discipline": random.randint(3, 5),
            "hard_work": random.randint(3, 5),
            "gratitude": random.randint(3, 5),
            "comments": f"Dynamic test feedback - {self.unique_id}"
        }
        feedback_result = self.test_endpoint("Submit Feedback", "POST", f"{self.gateway_url}/v1/feedback", feedback_data)
        if feedback_result['success']:
            self.created_data['feedback'].append(feedback_data)
        
        self.test_endpoint("Get All Interviews", "GET", f"{self.gateway_url}/v1/interviews")
        
        # Schedule dynamic interview
        interview_data = {
            "candidate_id": 1,
            "job_id": self.created_data['jobs'][0]['id'] if self.created_data['jobs'] else 1,
            "interview_date": (datetime.now() + timedelta(days=7)).isoformat(),
            "interviewer": f"DynamicTester_{self.unique_id}",
            "notes": f"Dynamic test interview - {self.unique_id}"
        }
        interview_result = self.test_endpoint("Schedule Interview", "POST", f"{self.gateway_url}/v1/interviews", interview_data)
        if interview_result['success']:
            self.created_data['interviews'].append(interview_data)
        
        self.test_endpoint("Get All Offers", "GET", f"{self.gateway_url}/v1/offers")
        
        # Create dynamic offer
        offer_data = {
            "candidate_id": 1,
            "job_id": self.created_data['jobs'][0]['id'] if self.created_data['jobs'] else 1,
            "salary": random.randint(70000, 150000),
            "start_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
            "terms": f"Dynamic test offer - {self.unique_id}"
        }
        offer_result = self.test_endpoint("Create Job Offer", "POST", f"{self.gateway_url}/v1/offers", offer_data)
        if offer_result['success']:
            self.created_data['offers'].append(offer_data)
        
        # Client Portal (1 endpoint)
        print("\n6. CLIENT PORTAL:")
        client_data = {"client_id": "TECH001", "password": "demo123"}
        self.test_endpoint("Client Login", "POST", f"{self.gateway_url}/v1/client/login", client_data)
        
        # Reports (1 endpoint)
        print("\n7. REPORTS:")
        job_id = self.created_data['jobs'][0]['id'] if self.created_data['jobs'] else 1
        self.test_endpoint("Export Job Report", "GET", f"{self.gateway_url}/v1/reports/job/{job_id}/export.csv")
        
        # Security Testing (11 endpoints)
        print("\n8. SECURITY TESTING:")
        self.test_endpoint("Rate Limit Status", "GET", f"{self.gateway_url}/v1/security/rate-limit-status")
        self.test_endpoint("Blocked IPs", "GET", f"{self.gateway_url}/v1/security/blocked-ips")
        
        # Dynamic security tests
        input_test = {"input_data": f"<script>alert('test_{self.unique_id}')</script>"}
        self.test_endpoint("Input Validation", "POST", f"{self.gateway_url}/v1/security/test-input-validation", input_test)
        
        email_test = {"email": f"test_{self.unique_id}@example.com"}
        self.test_endpoint("Email Validation", "POST", f"{self.gateway_url}/v1/security/test-email-validation", email_test)
        
        phone_test = {"phone": f"+1-555-{random.randint(1000, 9999)}"}
        self.test_endpoint("Phone Validation", "POST", f"{self.gateway_url}/v1/security/test-phone-validation", phone_test)
        
        self.test_endpoint("Security Headers", "GET", f"{self.gateway_url}/v1/security/security-headers-test")
        self.test_endpoint("Penetration Test Endpoints", "GET", f"{self.gateway_url}/v1/security/penetration-test-endpoints")
        
        # CSP Management (4 endpoints)
        print("\n9. CSP MANAGEMENT:")
        self.test_endpoint("CSP Policies", "GET", f"{self.gateway_url}/v1/security/csp-policies")
        self.test_endpoint("CSP Violations", "GET", f"{self.gateway_url}/v1/security/csp-violations")
        
        csp_report = {
            "violated_directive": "script-src",
            "blocked_uri": f"https://malicious-{self.unique_id}.com/script.js",
            "document_uri": f"https://test-{self.unique_id}.com/page"
        }
        self.test_endpoint("CSP Report", "POST", f"{self.gateway_url}/v1/security/csp-report", csp_report)
        
        csp_policy = {"policy": f"default-src 'self'; script-src 'self' test-{self.unique_id}.com"}
        self.test_endpoint("Test CSP Policy", "POST", f"{self.gateway_url}/v1/security/test-csp-policy", csp_policy)
        
        # Two-Factor Authentication (8 endpoints)
        print("\n10. TWO-FACTOR AUTHENTICATION:")
        user_setup = {"user_id": f"test_user_{self.unique_id}"}
        self.test_endpoint("2FA Setup", "POST", f"{self.gateway_url}/v1/2fa/setup", user_setup)
        
        totp_data = {"user_id": f"test_user_{self.unique_id}", "totp_code": "123456"}
        self.test_endpoint("2FA Verify Setup", "POST", f"{self.gateway_url}/v1/2fa/verify-setup", totp_data, 401)  # Expected to fail
        self.test_endpoint("2FA Login", "POST", f"{self.gateway_url}/v1/2fa/login-with-2fa", totp_data, 401)  # Expected to fail
        
        self.test_endpoint("2FA Status", "GET", f"{self.gateway_url}/v1/2fa/status/test_user_{self.unique_id}")
        self.test_endpoint("2FA Disable", "POST", f"{self.gateway_url}/v1/2fa/disable", user_setup)
        self.test_endpoint("2FA Regenerate Codes", "POST", f"{self.gateway_url}/v1/2fa/regenerate-backup-codes", user_setup)
        self.test_endpoint("2FA Test Token", "GET", f"{self.gateway_url}/v1/2fa/test-token/test_user_{self.unique_id}/123456")
        self.test_endpoint("2FA Demo Setup", "GET", f"{self.gateway_url}/v1/2fa/demo-setup")
        
        # Password Management (6 endpoints)
        print("\n11. PASSWORD MANAGEMENT:")
        password_test = {"password": f"TestPass123!_{self.unique_id}"}
        self.test_endpoint("Password Validate", "POST", f"{self.gateway_url}/v1/password/validate", password_test)
        self.test_endpoint("Password Generate", "POST", f"{self.gateway_url}/v1/password/generate?length=16")
        self.test_endpoint("Password Policy", "GET", f"{self.gateway_url}/v1/password/policy")
        
        password_change = {"old_password": "oldpass123", "new_password": f"NewPass123!_{self.unique_id}"}
        self.test_endpoint("Password Change", "POST", f"{self.gateway_url}/v1/password/change", password_change)
        self.test_endpoint("Password Strength Test", "GET", f"{self.gateway_url}/v1/password/strength-test")
        self.test_endpoint("Password Security Tips", "GET", f"{self.gateway_url}/v1/password/security-tips")
        
        # AGENT SERVICE TESTS (5 endpoints)
        print("\n\nAGENT SERVICE ENDPOINTS (5 total):")
        print("-" * 40)
        
        # Core (2 endpoints)
        print("\n12. AGENT CORE:")
        self.test_endpoint("Agent Root", "GET", f"{self.agent_url}/")
        self.test_endpoint("Agent Health", "GET", f"{self.agent_url}/health")
        
        # AI Processing (2 endpoints)
        print("\n13. AI PROCESSING:")
        match_data = {"job_id": self.created_data['jobs'][0]['id'] if self.created_data['jobs'] else 1}
        self.test_endpoint("AI Match", "POST", f"{self.agent_url}/match", match_data)
        self.test_endpoint("Analyze Candidate", "GET", f"{self.agent_url}/analyze/1")
        
        # Diagnostics (1 endpoint)
        print("\n14. DIAGNOSTICS:")
        self.test_endpoint("Agent DB Test", "GET", f"{self.agent_url}/test-db")
        
        return self.generate_report()
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 60)
        print("COMPREHENSIVE TEST REPORT")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r['success'])
        failed_tests = total_tests - passed_tests
        
        avg_response_time = sum(r['response_time'] for r in self.test_results) / total_tests if total_tests > 0 else 0
        
        print(f"\nTEST SUMMARY:")
        print(f"Total Endpoints Tested: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print(f"Average Response Time: {avg_response_time:.1f}ms")
        
        print(f"\nDYNAMIC DATA CREATED:")
        print(f"Jobs: {len(self.created_data['jobs'])}")
        print(f"Candidates: {len(self.created_data['candidates'])}")
        print(f"Feedback: {len(self.created_data['feedback'])}")
        print(f"Interviews: {len(self.created_data['interviews'])}")
        print(f"Offers: {len(self.created_data['offers'])}")
        
        if failed_tests > 0:
            print(f"\nFAILED TESTS:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['name']}: {result['status_code']} - {result.get('error', 'HTTP Error')}")
        
        # Save detailed report
        report_data = {
            'test_session_id': self.unique_id,
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_tests': total_tests,
                'passed': passed_tests,
                'failed': failed_tests,
                'success_rate': (passed_tests/total_tests)*100,
                'avg_response_time': avg_response_time
            },
            'created_data': self.created_data,
            'detailed_results': self.test_results
        }
        
        with open(f'test_report_{self.unique_id}.json', 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\nDetailed report saved: test_report_{self.unique_id}.json")
        
        return report_data

if __name__ == "__main__":
    tester = DynamicTester()
    report = tester.run_comprehensive_tests()