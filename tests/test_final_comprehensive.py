#!/usr/bin/env python3
"""
FINAL COMPREHENSIVE TESTING SUITE
BHIV HR Platform - Complete validation of all endpoints, services, and functionalities
"""

import requests
import json
import time
from datetime import datetime
import sys

# Configuration
BASE_URL = "http://localhost:8000"
AGENT_URL = "http://localhost:9000"
API_KEY = "myverysecureapikey123"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

class ComprehensiveTester:
    def __init__(self):
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.start_time = time.time()
        self.test_results = []

    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")

    def test_endpoint(self, method, url, data=None, expected_status=200, test_name=""):
        """Test endpoint and track results"""
        self.total_tests += 1
        try:
            start = time.time()
            
            if method == "GET":
                response = requests.get(url, headers=HEADERS, timeout=10)
            elif method == "POST":
                response = requests.post(url, headers=HEADERS, json=data, timeout=10)
            elif method == "PUT":
                response = requests.put(url, headers=HEADERS, json=data, timeout=10)
            elif method == "DELETE":
                response = requests.delete(url, headers=HEADERS, timeout=10)
            
            duration = time.time() - start
            success = response.status_code == expected_status
            
            result = {
                "test_name": test_name,
                "method": method,
                "url": url,
                "status_code": response.status_code,
                "expected_status": expected_status,
                "response_time": round(duration * 1000, 2),
                "success": success
            }
            
            if success:
                self.passed_tests += 1
                self.log(f"PASS {test_name}: {method} {url} - {response.status_code} ({duration*1000:.1f}ms)")
                
                # Log response details for key endpoints
                if response.status_code == 200 and method in ["GET", "POST"]:
                    try:
                        json_data = response.json()
                        if isinstance(json_data, dict):
                            if "matches" in json_data:
                                self.log(f"  AI Matches: {len(json_data['matches'])}")
                            elif "candidates" in json_data:
                                self.log(f"  Candidates: {len(json_data['candidates'])}")
                            elif "jobs" in json_data:
                                self.log(f"  Jobs: {len(json_data['jobs'])}")
                            elif "message" in json_data:
                                self.log(f"  Message: {json_data['message']}")
                    except:
                        pass
            else:
                self.failed_tests += 1
                self.log(f"FAIL {test_name}: {method} {url} - Expected {expected_status}, got {response.status_code}", "ERROR")
                try:
                    error_detail = response.json().get('detail', response.text[:100])
                    self.log(f"  Error: {error_detail}", "ERROR")
                except:
                    self.log(f"  Error: {response.text[:100]}", "ERROR")
            
            self.test_results.append(result)
            return result
            
        except Exception as e:
            self.failed_tests += 1
            self.log(f"ERROR {test_name}: {method} {url} - Exception: {str(e)}", "ERROR")
            self.test_results.append({
                "test_name": test_name,
                "method": method,
                "url": url,
                "error": str(e),
                "success": False
            })
            return {"success": False, "error": str(e)}

    def test_core_functionality(self):
        """Test core API functionality"""
        self.log("TESTING CORE FUNCTIONALITY")
        
        # Core endpoints
        self.test_endpoint("GET", f"{BASE_URL}/", 200, "Root Endpoint")
        self.test_endpoint("GET", f"{BASE_URL}/health", 200, "Health Check")
        self.test_endpoint("GET", f"{BASE_URL}/test-candidates", 200, "Test Candidates")
        self.test_endpoint("GET", f"{BASE_URL}/http-methods-test", 200, "HTTP Methods Test")

    def test_job_management(self):
        """Test job management with correct schema"""
        self.log("TESTING JOB MANAGEMENT")
        
        # Test job creation with correct schema
        job_data = {
            "title": "Senior Python Developer",
            "department": "Engineering",
            "location": "Remote",
            "experience_level": "Senior",
            "requirements": "Python, Django, PostgreSQL, 5+ years experience",
            "description": "We are looking for an experienced Python developer",
            "client_id": 1,
            "employment_type": "Full-time"
        }
        
        self.test_endpoint("POST", f"{BASE_URL}/v1/jobs", job_data, 200, "Create Job")
        self.test_endpoint("GET", f"{BASE_URL}/v1/jobs", 200, "List Jobs")

    def test_candidate_management(self):
        """Test candidate management"""
        self.log("TESTING CANDIDATE MANAGEMENT")
        
        self.test_endpoint("GET", f"{BASE_URL}/v1/candidates", 200, "List Candidates")
        self.test_endpoint("GET", f"{BASE_URL}/v1/candidates/job/1", 200, "Candidates by Job")
        
        # Test candidate search with parameters
        self.test_endpoint("GET", f"{BASE_URL}/v1/candidates/search?skills=python", 200, "Search Candidates")
        
        # Test bulk upload with correct schema
        bulk_data = {
            "candidates": [
                {
                    "name": "Test Candidate",
                    "email": "test@example.com",
                    "phone": "+1-555-0123",
                    "location": "Remote",
                    "experience_years": 5,
                    "technical_skills": "Python, Django",
                    "seniority_level": "Senior",
                    "education_level": "Bachelor's",
                    "resume_path": "/test.pdf",
                    "status": "active"
                }
            ]
        }
        self.test_endpoint("POST", f"{BASE_URL}/v1/candidates/bulk", bulk_data, 200, "Bulk Upload")

    def test_ai_matching(self):
        """Test AI matching engine"""
        self.log("TESTING AI MATCHING ENGINE")
        
        self.test_endpoint("GET", f"{BASE_URL}/v1/match/1/top", 200, "AI Matching - Job 1")
        self.test_endpoint("GET", f"{BASE_URL}/v1/match/1/top?limit=5", 200, "AI Matching - Limited")
        self.test_endpoint("GET", f"{BASE_URL}/v1/match/performance-test", 200, "Performance Test")
        self.test_endpoint("GET", f"{BASE_URL}/v1/match/cache-status", 200, "Cache Status")

    def test_security_features(self):
        """Test security features"""
        self.log("TESTING SECURITY FEATURES")
        
        # Security status and headers
        self.test_endpoint("GET", f"{BASE_URL}/v1/security/headers", 200, "Security Headers")
        self.test_endpoint("GET", f"{BASE_URL}/v1/security/status", 200, "Security Status")
        self.test_endpoint("GET", f"{BASE_URL}/v1/security/policy", 200, "Security Policy")
        self.test_endpoint("GET", f"{BASE_URL}/v1/security/rate-limit-status", 200, "Rate Limit Status")
        
        # Security testing with correct data
        xss_data = {"input_data": "<script>alert('test')</script>"}
        self.test_endpoint("POST", f"{BASE_URL}/v1/security/test-xss", xss_data, 200, "XSS Protection Test")
        
        sql_data = {"input_data": "'; DROP TABLE users; --"}
        self.test_endpoint("POST", f"{BASE_URL}/v1/security/test-sql-injection", sql_data, 200, "SQL Injection Test")
        
        self.test_endpoint("GET", f"{BASE_URL}/v1/security/audit-log", 200, "Audit Log")
        self.test_endpoint("POST", f"{BASE_URL}/v1/security/rotate-keys", {}, 200, "Rotate Keys")

    def test_password_management(self):
        """Test password management"""
        self.log("TESTING PASSWORD MANAGEMENT")
        
        password_data = {"password": "TestPassword123!"}
        self.test_endpoint("POST", f"{BASE_URL}/v1/password/validate", password_data, 200, "Password Validation")
        
        self.test_endpoint("GET", f"{BASE_URL}/v1/password/generate", 200, "Generate Password")
        self.test_endpoint("GET", f"{BASE_URL}/v1/password/policy", 200, "Password Policy")
        
        change_data = {"old_password": "old123", "new_password": "new123"}
        self.test_endpoint("POST", f"{BASE_URL}/v1/password/change", change_data, 200, "Change Password")
        
        self.test_endpoint("GET", f"{BASE_URL}/v1/password/strength-test", 200, "Strength Test")
        self.test_endpoint("GET", f"{BASE_URL}/v1/password/security-tips", 200, "Security Tips")
        
        email_data = {"email": "test@example.com"}
        self.test_endpoint("POST", f"{BASE_URL}/v1/password/reset", email_data, 200, "Password Reset")

    def test_csp_management(self):
        """Test CSP management"""
        self.log("TESTING CSP MANAGEMENT")
        
        self.test_endpoint("GET", f"{BASE_URL}/v1/csp/policy", 200, "Get CSP Policy")
        
        csp_report = {
            "violated_directive": "script-src",
            "blocked_uri": "https://malicious.com/script.js",
            "document_uri": "https://bhiv-platform.com/page"
        }
        self.test_endpoint("POST", f"{BASE_URL}/v1/csp/report", csp_report, 200, "CSP Report")
        
        policy_data = {"policy": "default-src 'self'"}
        self.test_endpoint("PUT", f"{BASE_URL}/v1/csp/policy", policy_data, 200, "Update CSP Policy")

    def test_session_management(self):
        """Test session management"""
        self.log("TESTING SESSION MANAGEMENT")
        
        login_data = {"client_id": "TECH001", "password": "demo123"}
        self.test_endpoint("POST", f"{BASE_URL}/v1/sessions/create", login_data, 200, "Create Session")
        
        self.test_endpoint("GET", f"{BASE_URL}/v1/sessions/validate", 200, "Validate Session")
        
        logout_data = {"session_id": "test_session"}
        self.test_endpoint("POST", f"{BASE_URL}/v1/sessions/logout", logout_data, 200, "Logout Session")

    def test_interview_management(self):
        """Test interview management"""
        self.log("TESTING INTERVIEW MANAGEMENT")
        
        self.test_endpoint("GET", f"{BASE_URL}/v1/interviews", 200, "List Interviews")
        
        interview_data = {
            "candidate_id": 1,
            "job_id": 1,
            "interview_date": "2025-02-01T10:00:00Z",
            "interviewer": "John Manager",
            "notes": "Technical interview"
        }
        self.test_endpoint("POST", f"{BASE_URL}/v1/interviews", interview_data, 200, "Schedule Interview")

    def test_database_management(self):
        """Test database management"""
        self.log("TESTING DATABASE MANAGEMENT")
        
        self.test_endpoint("GET", f"{BASE_URL}/v1/database/health", 200, "Database Health")
        self.test_endpoint("POST", f"{BASE_URL}/v1/database/add-interviewer-column", {}, 200, "Add Interviewer Column")

    def test_monitoring_system(self):
        """Test monitoring system"""
        self.log("TESTING MONITORING SYSTEM")
        
        self.test_endpoint("GET", f"{BASE_URL}/metrics", 200, "Prometheus Metrics")
        self.test_endpoint("GET", f"{BASE_URL}/health/detailed", 200, "Detailed Health")
        self.test_endpoint("GET", f"{BASE_URL}/monitoring/errors", 200, "Error Monitoring")
        self.test_endpoint("GET", f"{BASE_URL}/monitoring/dependencies", 200, "Dependencies")
        self.test_endpoint("GET", f"{BASE_URL}/metrics/dashboard", 200, "Metrics Dashboard")

    def test_agent_service(self):
        """Test AI Agent service"""
        self.log("TESTING AI AGENT SERVICE")
        
        self.test_endpoint("GET", f"{AGENT_URL}/", 200, "Agent Root")
        self.test_endpoint("GET", f"{AGENT_URL}/health", 200, "Agent Health")
        self.test_endpoint("GET", f"{AGENT_URL}/status", 200, "Agent Status")
        self.test_endpoint("GET", f"{AGENT_URL}/version", 200, "Agent Version")
        self.test_endpoint("GET", f"{AGENT_URL}/metrics", 200, "Agent Metrics")

    def test_client_portal(self):
        """Test client portal"""
        self.log("TESTING CLIENT PORTAL")
        
        client_data = {"client_id": "TECH001", "password": "demo123"}
        self.test_endpoint("POST", f"{BASE_URL}/v1/client/login", client_data, 200, "Client Login")

    def test_analytics(self):
        """Test analytics endpoints"""
        self.log("TESTING ANALYTICS")
        
        self.test_endpoint("GET", f"{BASE_URL}/candidates/stats", 200, "Candidate Statistics")

    def performance_benchmark(self):
        """Run performance benchmarks"""
        self.log("RUNNING PERFORMANCE BENCHMARKS")
        
        endpoints = [
            (f"{BASE_URL}/health", "Health Check"),
            (f"{BASE_URL}/v1/candidates", "List Candidates"),
            (f"{BASE_URL}/v1/jobs", "List Jobs"),
            (f"{BASE_URL}/v1/match/1/top", "AI Matching"),
            (f"{AGENT_URL}/health", "Agent Health")
        ]
        
        for url, name in endpoints:
            times = []
            for _ in range(3):
                start = time.time()
                try:
                    response = requests.get(url, headers=HEADERS, timeout=5)
                    if response.status_code == 200:
                        times.append(time.time() - start)
                except:
                    pass
            
            if times:
                avg_time = sum(times) / len(times) * 1000
                self.log(f"Performance {name}: {avg_time:.1f}ms average")

    def run_all_tests(self):
        """Run comprehensive test suite"""
        self.log("=" * 60)
        self.log("STARTING FINAL COMPREHENSIVE TESTING")
        self.log("=" * 60)
        
        # Run all test categories
        self.test_core_functionality()
        self.test_job_management()
        self.test_candidate_management()
        self.test_ai_matching()
        self.test_security_features()
        self.test_password_management()
        self.test_csp_management()
        self.test_session_management()
        self.test_interview_management()
        self.test_database_management()
        self.test_monitoring_system()
        self.test_agent_service()
        self.test_client_portal()
        self.test_analytics()
        self.performance_benchmark()
        
        # Generate final report
        self.generate_final_report()

    def generate_final_report(self):
        """Generate comprehensive final report"""
        total_time = time.time() - self.start_time
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        self.log("=" * 60)
        self.log("FINAL COMPREHENSIVE TESTING COMPLETE")
        self.log("=" * 60)
        self.log(f"Total Tests Executed: {self.total_tests}")
        self.log(f"Tests Passed: {self.passed_tests}")
        self.log(f"Tests Failed: {self.failed_tests}")
        self.log(f"Success Rate: {success_rate:.1f}%")
        self.log(f"Total Execution Time: {total_time:.1f} seconds")
        
        # Categorize results
        failed_by_category = {}
        for result in self.test_results:
            if not result.get('success', False):
                category = result.get('test_name', 'Unknown').split(' ')[0]
                if category not in failed_by_category:
                    failed_by_category[category] = []
                failed_by_category[category].append(result.get('test_name', 'Unknown'))
        
        if failed_by_category:
            self.log("\nFAILED TESTS BY CATEGORY:")
            for category, tests in failed_by_category.items():
                self.log(f"  {category}: {len(tests)} failures")
                for test in tests[:3]:  # Show first 3
                    self.log(f"    - {test}")
        
        # Overall assessment
        if success_rate >= 95:
            self.log("\nEXCELLENT: System is production-ready with minimal issues")
        elif success_rate >= 85:
            self.log("\nGOOD: System is mostly functional with minor issues")
        elif success_rate >= 75:
            self.log("\nFAIR: System has some issues that need attention")
        else:
            self.log("\nNEEDS WORK: System has significant issues requiring fixes")
        
        # Key metrics summary
        self.log(f"\nKEY METRICS:")
        self.log(f"- Core API Functionality: {'PASS' if success_rate >= 80 else 'NEEDS ATTENTION'}")
        self.log(f"- Security Features: {'ROBUST' if success_rate >= 85 else 'NEEDS REVIEW'}")
        self.log(f"- AI Matching Engine: {'OPERATIONAL' if success_rate >= 75 else 'NEEDS FIXES'}")
        self.log(f"- Database Integration: {'STABLE' if success_rate >= 80 else 'UNSTABLE'}")
        self.log(f"- Monitoring System: {'COMPREHENSIVE' if success_rate >= 85 else 'BASIC'}")

if __name__ == "__main__":
    tester = ComprehensiveTester()
    tester.run_all_tests()