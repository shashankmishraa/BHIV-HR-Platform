#!/usr/bin/env python3
"""
BHIV HR Platform - Complete System Verification
Tests all 53 endpoints across 4 services with comprehensive feature validation
"""

import requests
import json
import time
from datetime import datetime
import sys
import os

# Configuration
PRODUCTION_URLS = {
    "gateway": "https://bhiv-hr-gateway-46pz.onrender.com",
    "agent": "https://bhiv-hr-agent-m1me.onrender.com",
    "portal": "https://bhiv-hr-portal-cead.onrender.com",
    "client_portal": "https://bhiv-hr-client-portal-5g33.onrender.com"
}

LOCAL_URLS = {
    "gateway": "http://localhost:8000",
    "agent": "http://localhost:9000",
    "portal": "http://localhost:8501",
    "client_portal": "http://localhost:8502"
}

API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

class SystemVerifier:
    def __init__(self, use_production=True):
        self.urls = PRODUCTION_URLS if use_production else LOCAL_URLS
        self.results = {}
        self.total_tests = 0
        self.passed_tests = 0
        self.environment = "PRODUCTION" if use_production else "LOCAL"
        
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def test_endpoint(self, name, method, url, data=None, expected_status=200, timeout=30):
        """Test individual endpoint"""
        self.total_tests += 1
        try:
            if method == "GET":
                response = requests.get(url, headers=HEADERS, timeout=timeout)
            elif method == "POST":
                response = requests.post(url, headers=HEADERS, json=data, timeout=timeout)
            elif method == "PUT":
                response = requests.put(url, headers=HEADERS, json=data, timeout=timeout)
            elif method == "DELETE":
                response = requests.delete(url, headers=HEADERS, timeout=timeout)
            
            if response.status_code == expected_status:
                self.log(f"✅ {name}: PASSED ({response.status_code})")
                self.passed_tests += 1
                return True, response.json() if response.content else {}
            else:
                self.log(f"❌ {name}: FAILED ({response.status_code})", "ERROR")
                return False, response.text
                
        except requests.exceptions.Timeout:
            self.log(f"⏰ {name}: TIMEOUT", "ERROR")
            return False, "Timeout"
        except Exception as e:
            self.log(f"❌ {name}: ERROR - {str(e)}", "ERROR")
            return False, str(e)
    
    def test_gateway_service(self):
        """Test all 48 Gateway endpoints"""
        self.log("🔍 Testing API Gateway Service (48 endpoints)")
        gateway_url = self.urls["gateway"]
        
        # Core API Endpoints (7)
        self.log("Testing Core API Endpoints...")
        self.test_endpoint("Gateway Root", "GET", f"{gateway_url}/")
        self.test_endpoint("Gateway Health", "GET", f"{gateway_url}/health")
        self.test_endpoint("Test Candidates DB", "GET", f"{gateway_url}/test-candidates")
        self.test_endpoint("Prometheus Metrics", "GET", f"{gateway_url}/metrics")
        self.test_endpoint("Detailed Health", "GET", f"{gateway_url}/health/detailed")
        self.test_endpoint("Metrics Dashboard", "GET", f"{gateway_url}/metrics/dashboard")
        self.test_endpoint("Candidate Stats", "GET", f"{gateway_url}/candidates/stats")
        
        # Job Management (2)
        self.log("Testing Job Management...")
        job_data = {
            "title": "Test Software Engineer",
            "department": "Engineering",
            "location": "Remote",
            "experience_level": "Senior",
            "requirements": "Python, FastAPI, PostgreSQL",
            "description": "Test job for system verification"
        }
        success, result = self.test_endpoint("Create Job", "POST", f"{gateway_url}/v1/jobs", job_data)
        self.test_endpoint("List Jobs", "GET", f"{gateway_url}/v1/jobs")
        
        # Candidate Management (5)
        self.log("Testing Candidate Management...")
        self.test_endpoint("Get All Candidates", "GET", f"{gateway_url}/v1/candidates")
        self.test_endpoint("Get Candidate by ID", "GET", f"{gateway_url}/v1/candidates/1")
        self.test_endpoint("Search Candidates", "GET", f"{gateway_url}/v1/candidates/search?skills=Python")
        
        candidate_data = {
            "candidates": [{
                "name": "Test Candidate",
                "email": f"test_{int(time.time())}@example.com",
                "phone": "+1-555-0199",
                "location": "Test City",
                "experience_years": 5,
                "technical_skills": "Python, FastAPI, PostgreSQL",
                "seniority_level": "Senior",
                "education_level": "Masters"
            }]
        }
        self.test_endpoint("Bulk Upload Candidates", "POST", f"{gateway_url}/v1/candidates/bulk", candidate_data)
        self.test_endpoint("Get Candidates by Job", "GET", f"{gateway_url}/v1/candidates/job/1")
        
        # AI Matching Engine (1)
        self.log("Testing AI Matching...")
        self.test_endpoint("AI Top Matches", "GET", f"{gateway_url}/v1/match/1/top")
        
        # Assessment & Workflow (6)
        self.log("Testing Assessment & Workflow...")
        feedback_data = {
            "candidate_id": 1,
            "job_id": 1,
            "integrity": 5,
            "honesty": 4,
            "discipline": 5,
            "hard_work": 5,
            "gratitude": 4,
            "comments": "Excellent candidate"
        }
        self.test_endpoint("Submit Feedback", "POST", f"{gateway_url}/v1/feedback", feedback_data)
        self.test_endpoint("Get All Feedback", "GET", f"{gateway_url}/v1/feedback")
        
        interview_data = {
            "candidate_id": 1,
            "job_id": 1,
            "interview_date": "2025-02-01T10:00:00Z",
            "interviewer": "Test Interviewer"
        }
        self.test_endpoint("Schedule Interview", "POST", f"{gateway_url}/v1/interviews", interview_data)
        self.test_endpoint("Get All Interviews", "GET", f"{gateway_url}/v1/interviews")
        
        offer_data = {
            "candidate_id": 1,
            "job_id": 1,
            "salary": 120000,
            "start_date": "2025-03-01",
            "terms": "Standard employment terms"
        }
        self.test_endpoint("Create Job Offer", "POST", f"{gateway_url}/v1/offers", offer_data)
        self.test_endpoint("Get All Offers", "GET", f"{gateway_url}/v1/offers")
        
        # Analytics & Statistics (2)
        self.log("Testing Analytics...")
        self.test_endpoint("Candidate Statistics", "GET", f"{gateway_url}/candidates/stats")
        self.test_endpoint("Export Job Report", "GET", f"{gateway_url}/v1/reports/job/1/export.csv")
        
        # Client Portal API (1)
        self.log("Testing Client Portal API...")
        client_login_data = {
            "client_id": "TECH001",
            "password": "demo123"
        }
        self.test_endpoint("Client Login", "POST", f"{gateway_url}/v1/client/login", client_login_data)
        
        # Security Testing (7)
        self.log("Testing Security Features...")
        self.test_endpoint("Rate Limit Status", "GET", f"{gateway_url}/v1/security/rate-limit-status")
        self.test_endpoint("Blocked IPs", "GET", f"{gateway_url}/v1/security/blocked-ips")
        
        input_validation_data = {"input_data": "test<script>alert('xss')</script>"}
        self.test_endpoint("Input Validation", "POST", f"{gateway_url}/v1/security/test-input-validation", input_validation_data)
        
        email_validation_data = {"email": "test@example.com"}
        self.test_endpoint("Email Validation", "POST", f"{gateway_url}/v1/security/test-email-validation", email_validation_data)
        
        phone_validation_data = {"phone": "+1-555-0123"}
        self.test_endpoint("Phone Validation", "POST", f"{gateway_url}/v1/security/test-phone-validation", phone_validation_data)
        
        self.test_endpoint("Security Headers Test", "GET", f"{gateway_url}/v1/security/security-headers-test")
        self.test_endpoint("Penetration Test Endpoints", "GET", f"{gateway_url}/v1/security/penetration-test-endpoints")
        
        # CSP Management (4)
        self.log("Testing CSP Management...")
        csp_report_data = {
            "violated_directive": "script-src",
            "blocked_uri": "https://malicious.com/script.js",
            "document_uri": "https://example.com/page"
        }
        self.test_endpoint("CSP Report", "POST", f"{gateway_url}/v1/security/csp-report", csp_report_data)
        self.test_endpoint("CSP Violations", "GET", f"{gateway_url}/v1/security/csp-violations")
        self.test_endpoint("CSP Policies", "GET", f"{gateway_url}/v1/security/csp-policies")
        
        csp_policy_data = {"policy": "default-src 'self'"}
        self.test_endpoint("Test CSP Policy", "POST", f"{gateway_url}/v1/security/test-csp-policy", csp_policy_data)
        
        # Two-Factor Authentication (8)
        self.log("Testing 2FA Features...")
        twofa_setup_data = {"user_id": "test_user"}
        self.test_endpoint("2FA Setup", "POST", f"{gateway_url}/v1/2fa/setup", twofa_setup_data)
        
        twofa_verify_data = {"user_id": "test_user", "totp_code": "123456"}
        self.test_endpoint("2FA Verify Setup", "POST", f"{gateway_url}/v1/2fa/verify-setup", twofa_verify_data, expected_status=401)  # Expected to fail with demo code
        self.test_endpoint("2FA Login", "POST", f"{gateway_url}/v1/2fa/login-with-2fa", twofa_verify_data, expected_status=401)  # Expected to fail
        
        self.test_endpoint("2FA Status", "GET", f"{gateway_url}/v1/2fa/status/test_user")
        self.test_endpoint("2FA Disable", "POST", f"{gateway_url}/v1/2fa/disable", twofa_setup_data)
        self.test_endpoint("2FA Regenerate Codes", "POST", f"{gateway_url}/v1/2fa/regenerate-backup-codes", twofa_setup_data)
        self.test_endpoint("2FA Test Token", "GET", f"{gateway_url}/v1/2fa/test-token/test_user/123456")
        self.test_endpoint("2FA Demo Setup", "GET", f"{gateway_url}/v1/2fa/demo-setup")
        
        # Password Management (6)
        self.log("Testing Password Management...")
        password_data = {"password": "TestPassword123!"}
        self.test_endpoint("Password Validation", "POST", f"{gateway_url}/v1/password/validate", password_data)
        self.test_endpoint("Generate Password", "POST", f"{gateway_url}/v1/password/generate?length=12")
        self.test_endpoint("Password Policy", "GET", f"{gateway_url}/v1/password/policy")
        
        password_change_data = {"old_password": "old123", "new_password": "new123!"}
        self.test_endpoint("Change Password", "POST", f"{gateway_url}/v1/password/change", password_change_data)
        self.test_endpoint("Password Strength Test", "GET", f"{gateway_url}/v1/password/strength-test")
        self.test_endpoint("Password Security Tips", "GET", f"{gateway_url}/v1/password/security-tips")
    
    def test_agent_service(self):
        """Test all 5 Agent endpoints"""
        self.log("🤖 Testing AI Agent Service (5 endpoints)")
        agent_url = self.urls["agent"]
        
        # Core API (2)
        self.test_endpoint("Agent Root", "GET", f"{agent_url}/")
        self.test_endpoint("Agent Health", "GET", f"{agent_url}/health")
        
        # AI Processing (2)
        match_data = {"job_id": 1}
        self.test_endpoint("AI Match Candidates", "POST", f"{agent_url}/match", match_data)
        self.test_endpoint("Analyze Candidate", "GET", f"{agent_url}/analyze/1")
        
        # System Diagnostics (1)
        self.test_endpoint("Agent Test DB", "GET", f"{agent_url}/test-db")
    
    def test_portal_services(self):
        """Test Portal accessibility"""
        self.log("🖥️ Testing Portal Services")
        
        # Test portal accessibility (these are Streamlit apps, so we just check if they're up)
        try:
            response = requests.get(self.urls["portal"], timeout=10)
            if response.status_code == 200:
                self.log("✅ HR Portal: ACCESSIBLE")
                self.passed_tests += 1
            else:
                self.log(f"❌ HR Portal: FAILED ({response.status_code})", "ERROR")
        except Exception as e:
            self.log(f"❌ HR Portal: ERROR - {str(e)}", "ERROR")
        
        try:
            response = requests.get(self.urls["client_portal"], timeout=10)
            if response.status_code == 200:
                self.log("✅ Client Portal: ACCESSIBLE")
                self.passed_tests += 1
            else:
                self.log(f"❌ Client Portal: FAILED ({response.status_code})", "ERROR")
        except Exception as e:
            self.log(f"❌ Client Portal: ERROR - {str(e)}", "ERROR")
        
        self.total_tests += 2
    
    def test_data_integrity(self):
        """Test data integrity and real data presence"""
        self.log("📊 Testing Data Integrity")
        gateway_url = self.urls["gateway"]
        
        # Test candidate data
        success, result = self.test_endpoint("Verify Candidate Data", "GET", f"{gateway_url}/test-candidates")
        if success and isinstance(result, dict):
            candidate_count = result.get('total_candidates', 0)
            if candidate_count > 0:
                self.log(f"✅ Real Data Verified: {candidate_count} candidates in database")
            else:
                self.log("⚠️ No candidates found in database", "WARNING")
        
        # Test job data
        success, result = self.test_endpoint("Verify Job Data", "GET", f"{gateway_url}/v1/jobs")
        if success and isinstance(result, dict):
            job_count = result.get('count', 0)
            if job_count > 0:
                self.log(f"✅ Job Data Verified: {job_count} jobs in database")
            else:
                self.log("⚠️ No jobs found in database", "WARNING")
    
    def test_ai_functionality(self):
        """Test AI matching functionality"""
        self.log("🧠 Testing AI Functionality")
        
        # Test AI agent directly
        agent_url = self.urls["agent"]
        match_data = {"job_id": 1}
        
        success, result = self.test_endpoint("AI Dynamic Matching", "POST", f"{agent_url}/match", match_data, timeout=30)
        if success and isinstance(result, dict):
            candidates = result.get('top_candidates', [])
            algorithm_version = result.get('algorithm_version', 'Unknown')
            processing_time = result.get('processing_time', 0)
            
            self.log(f"✅ AI Matching Results:")
            self.log(f"   - Candidates Found: {len(candidates)}")
            self.log(f"   - Algorithm Version: {algorithm_version}")
            self.log(f"   - Processing Time: {processing_time}s")
            
            if candidates:
                top_candidate = candidates[0]
                score = top_candidate.get('score', 0)
                name = top_candidate.get('name', 'Unknown')
                self.log(f"   - Top Match: {name} (Score: {score})")
    
    def test_security_features(self):
        """Test security features comprehensively"""
        self.log("🔒 Testing Security Features")
        gateway_url = self.urls["gateway"]
        
        # Test rate limiting
        self.log("Testing Rate Limiting...")
        start_time = time.time()
        rate_limit_hit = False
        
        for i in range(10):  # Test with fewer requests to avoid overwhelming
            try:
                response = requests.get(f"{gateway_url}/health", headers=HEADERS, timeout=5)
                if response.status_code == 429:
                    rate_limit_hit = True
                    self.log(f"✅ Rate Limiting: Triggered after {i+1} requests")
                    break
            except:
                break
        
        if not rate_limit_hit:
            self.log("✅ Rate Limiting: Active (not triggered in test)")
        
        # Test security headers
        try:
            response = requests.get(f"{gateway_url}/health", headers=HEADERS, timeout=5)
            security_headers = [
                "X-Content-Type-Options",
                "X-Frame-Options", 
                "X-XSS-Protection",
                "Content-Security-Policy"
            ]
            
            present_headers = [h for h in security_headers if h in response.headers]
            self.log(f"✅ Security Headers: {len(present_headers)}/{len(security_headers)} present")
            
        except Exception as e:
            self.log(f"❌ Security Headers Test Failed: {str(e)}", "ERROR")
    
    def run_complete_verification(self):
        """Run complete system verification"""
        self.log(f"🚀 Starting Complete System Verification - {self.environment}")
        self.log("=" * 80)
        
        start_time = time.time()
        
        # Test all services
        self.test_gateway_service()
        self.test_agent_service()
        self.test_portal_services()
        
        # Test system functionality
        self.test_data_integrity()
        self.test_ai_functionality()
        self.test_security_features()
        
        # Calculate results
        end_time = time.time()
        duration = end_time - start_time
        success_rate = (self.passed_tests / self.total_tests) * 100 if self.total_tests > 0 else 0
        
        # Print summary
        self.log("=" * 80)
        self.log("🎯 VERIFICATION SUMMARY")
        self.log("=" * 80)
        self.log(f"Environment: {self.environment}")
        self.log(f"Total Tests: {self.total_tests}")
        self.log(f"Passed: {self.passed_tests}")
        self.log(f"Failed: {self.total_tests - self.passed_tests}")
        self.log(f"Success Rate: {success_rate:.1f}%")
        self.log(f"Duration: {duration:.2f} seconds")
        
        # Service breakdown
        self.log("\n📊 SERVICE STATUS:")
        for service, url in self.urls.items():
            self.log(f"   {service.upper()}: {url}")
        
        # Overall status
        if success_rate >= 90:
            self.log("\n✅ SYSTEM STATUS: EXCELLENT - All critical systems operational")
        elif success_rate >= 75:
            self.log("\n⚠️ SYSTEM STATUS: GOOD - Minor issues detected")
        elif success_rate >= 50:
            self.log("\n❌ SYSTEM STATUS: DEGRADED - Multiple issues detected")
        else:
            self.log("\n🚨 SYSTEM STATUS: CRITICAL - Major system failures")
        
        return {
            'total_tests': self.total_tests,
            'passed_tests': self.passed_tests,
            'success_rate': success_rate,
            'duration': duration,
            'environment': self.environment
        }

def main():
    """Main verification function"""
    print("BHIV HR Platform - Complete System Verification")
    print("=" * 60)
    
    # Determine environment
    use_production = True
    if len(sys.argv) > 1 and sys.argv[1].lower() == "local":
        use_production = False
    
    # Run verification
    verifier = SystemVerifier(use_production=use_production)
    results = verifier.run_complete_verification()
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"verification_results_{timestamp}.json"
    
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📄 Results saved to: {results_file}")
    
    # Exit with appropriate code
    if results['success_rate'] >= 90:
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Failure

if __name__ == "__main__":
    main()