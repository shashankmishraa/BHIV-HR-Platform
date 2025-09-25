#!/usr/bin/env python3
"""
AGGRESSIVE COMPREHENSIVE TESTING SUITE
BHIV HR Platform - Complete System Validation
Tests every endpoint, service, feature, and functionality
"""

import requests
import json
import time
import concurrent.futures
import threading
from datetime import datetime
import sys
import os

# Configuration
BASE_URL = "http://localhost:8000"
AGENT_URL = "http://localhost:9000"
PORTAL_URL = "http://localhost:8501"
CLIENT_PORTAL_URL = "http://localhost:8502"
API_KEY = "myverysecureapikey123"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}


class AggressiveTester:
    def __init__(self):
        self.results = {}
        self.failed_tests = []
        self.passed_tests = []
        self.total_tests = 0
        self.start_time = time.time()

    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")

    def test_endpoint(self, method, url, data=None, expected_status=200, test_name=""):
        """Test individual endpoint with aggressive validation"""
        try:
            self.total_tests += 1
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

            # Aggressive validation
            success = response.status_code == expected_status

            result = {
                "method": method,
                "url": url,
                "status_code": response.status_code,
                "expected_status": expected_status,
                "response_time": round(duration * 1000, 2),
                "success": success,
                "response_size": len(response.content),
                "test_name": test_name,
            }

            if success:
                self.passed_tests.append(result)
                self.log(
                    f"✅ {test_name}: {method} {url} - {response.status_code} ({duration*1000:.1f}ms)"
                )
            else:
                self.failed_tests.append(result)
                self.log(
                    f"❌ {test_name}: {method} {url} - Expected {expected_status}, got {response.status_code}",
                    "ERROR",
                )

            return result

        except Exception as e:
            self.total_tests += 1
            self.failed_tests.append(
                {
                    "method": method,
                    "url": url,
                    "error": str(e),
                    "test_name": test_name,
                    "success": False,
                }
            )
            self.log(f"💥 {test_name}: {method} {url} - Exception: {str(e)}", "ERROR")
            return {"success": False, "error": str(e)}

    def test_core_endpoints(self):
        """Test all core API endpoints"""
        self.log("🚀 TESTING CORE ENDPOINTS")

        core_tests = [
            ("GET", f"{BASE_URL}/", 200, "Root Endpoint"),
            ("GET", f"{BASE_URL}/health", 200, "Health Check"),
            ("GET", f"{BASE_URL}/test-candidates", 200, "Test Candidates"),
            ("GET", f"{BASE_URL}/http-methods-test", 200, "HTTP Methods Test"),
        ]

        for method, url, expected, name in core_tests:
            self.test_endpoint(method, url, expected_status=expected, test_name=name)

    def test_job_management(self):
        """Test job management endpoints"""
        self.log("💼 TESTING JOB MANAGEMENT")

        # Test job creation
        job_data = {
            "title": "Aggressive Test Engineer",
            "description": "Testing all the things",
            "requirements": ["Python", "Testing", "Automation"],
            "location": "Remote",
            "salary_range": "80000-120000",
        }

        self.test_endpoint("POST", f"{BASE_URL}/v1/jobs", job_data, 200, "Create Job")
        self.test_endpoint(
            "GET", f"{BASE_URL}/v1/jobs", expected_status=200, test_name="List Jobs"
        )

    def test_candidate_management(self):
        """Test candidate management endpoints"""
        self.log("👥 TESTING CANDIDATE MANAGEMENT")

        candidate_tests = [
            ("GET", f"{BASE_URL}/v1/candidates", 200, "List Candidates"),
            ("GET", f"{BASE_URL}/v1/candidates/stats", 200, "Candidate Stats"),
            (
                "POST",
                f"{BASE_URL}/v1/candidates/search",
                {"query": "python"},
                200,
                "Search Candidates",
            ),
        ]

        for method, url, expected, name in candidate_tests:
            if method == "POST":
                self.test_endpoint(method, url, {"query": "python"}, expected, name)
            else:
                self.test_endpoint(
                    method, url, expected_status=expected, test_name=name
                )

    def test_ai_matching(self):
        """Test AI matching endpoints"""
        self.log("🤖 TESTING AI MATCHING ENGINE")

        ai_tests = [
            ("GET", f"{BASE_URL}/v1/match/1/top", 200, "Top Matches for Job 1"),
            (
                "GET",
                f"{BASE_URL}/v1/match/performance-test",
                200,
                "AI Performance Test",
            ),
            ("GET", f"{BASE_URL}/v1/match/cache-status", 200, "Cache Status"),
            ("GET", f"{BASE_URL}/v1/match/cache-clear", 200, "Clear Cache"),
        ]

        for method, url, expected, name in ai_tests:
            self.test_endpoint(method, url, expected_status=expected, test_name=name)

    def test_security_features(self):
        """Test all security endpoints"""
        self.log("🔒 TESTING SECURITY FEATURES")

        security_tests = [
            ("GET", f"{BASE_URL}/v1/security/headers", 200, "Security Headers"),
            (
                "POST",
                f"{BASE_URL}/v1/security/test-xss",
                {"input": "<script>alert('test')</script>"},
                200,
                "XSS Protection",
            ),
            (
                "POST",
                f"{BASE_URL}/v1/security/test-sql-injection",
                {"query": "'; DROP TABLE users; --"},
                200,
                "SQL Injection Protection",
            ),
            ("GET", f"{BASE_URL}/v1/security/audit-log", 200, "Audit Log"),
            ("GET", f"{BASE_URL}/v1/security/status", 200, "Security Status"),
            ("POST", f"{BASE_URL}/v1/security/rotate-keys", {}, 200, "Rotate Keys"),
            ("GET", f"{BASE_URL}/v1/security/policy", 200, "Security Policy"),
            (
                "GET",
                f"{BASE_URL}/v1/security/rate-limit-status",
                200,
                "Rate Limit Status",
            ),
            ("GET", f"{BASE_URL}/v1/security/cors-config", 200, "CORS Configuration"),
            (
                "GET",
                f"{BASE_URL}/v1/security/cookie-config",
                200,
                "Cookie Configuration",
            ),
        ]

        for method, url, expected, name in security_tests:
            if method == "POST":
                if "xss" in url:
                    data = {"input": "<script>alert('test')</script>"}
                elif "sql" in url:
                    data = {"query": "'; DROP TABLE users; --"}
                else:
                    data = {}
                self.test_endpoint(method, url, data, expected, name)
            else:
                self.test_endpoint(
                    method, url, expected_status=expected, test_name=name
                )

    def test_authentication(self):
        """Test authentication endpoints"""
        self.log("🔐 TESTING AUTHENTICATION")

        auth_tests = [
            (
                "POST",
                f"{BASE_URL}/v1/auth/2fa/setup",
                {"user_id": "test_user"},
                200,
                "2FA Setup",
            ),
            (
                "POST",
                f"{BASE_URL}/v1/auth/2fa/verify",
                {"user_id": "test_user", "token": "123456"},
                200,
                "2FA Verify",
            ),
            (
                "POST",
                f"{BASE_URL}/v1/auth/2fa/login",
                {"username": "test", "password": "test", "token": "123456"},
                200,
                "2FA Login",
            ),
            ("GET", f"{BASE_URL}/v1/auth/api-keys", 200, "List API Keys"),
            (
                "POST",
                f"{BASE_URL}/v1/auth/api-keys",
                {"name": "test_key"},
                200,
                "Create API Key",
            ),
        ]

        for method, url, expected, name in auth_tests:
            if method == "POST":
                if "setup" in url:
                    data = {"user_id": "test_user"}
                elif "verify" in url:
                    data = {"user_id": "test_user", "token": "123456"}
                elif "login" in url:
                    data = {"username": "test", "password": "test", "token": "123456"}
                elif "api-keys" in url:
                    data = {"name": "test_key"}
                else:
                    data = {}
                self.test_endpoint(method, url, data, expected, name)
            else:
                self.test_endpoint(
                    method, url, expected_status=expected, test_name=name
                )

    def test_password_management(self):
        """Test password management endpoints"""
        self.log("🔑 TESTING PASSWORD MANAGEMENT")

        password_tests = [
            (
                "POST",
                f"{BASE_URL}/v1/password/validate",
                {"password": "TestPass123!"},
                200,
                "Password Validation",
            ),
            ("GET", f"{BASE_URL}/v1/password/generate", 200, "Generate Password"),
            ("GET", f"{BASE_URL}/v1/password/policy", 200, "Password Policy"),
            (
                "POST",
                f"{BASE_URL}/v1/password/change",
                {"old_password": "old", "new_password": "new"},
                200,
                "Change Password",
            ),
            ("GET", f"{BASE_URL}/v1/password/strength-test", 200, "Strength Test Tool"),
            ("GET", f"{BASE_URL}/v1/password/security-tips", 200, "Security Tips"),
            (
                "POST",
                f"{BASE_URL}/v1/password/reset",
                {"email": "test@example.com"},
                200,
                "Password Reset",
            ),
        ]

        for method, url, expected, name in password_tests:
            if method == "POST":
                if "validate" in url:
                    data = {"password": "TestPass123!"}
                elif "change" in url:
                    data = {"old_password": "old", "new_password": "new"}
                elif "reset" in url:
                    data = {"email": "test@example.com"}
                else:
                    data = {}
                self.test_endpoint(method, url, data, expected, name)
            else:
                self.test_endpoint(
                    method, url, expected_status=expected, test_name=name
                )

    def test_csp_management(self):
        """Test CSP management endpoints"""
        self.log("🛡️ TESTING CSP MANAGEMENT")

        csp_tests = [
            ("GET", f"{BASE_URL}/v1/csp/policy", 200, "Get CSP Policy"),
            (
                "POST",
                f"{BASE_URL}/v1/csp/report",
                {"violation": "test"},
                200,
                "CSP Report",
            ),
            (
                "PUT",
                f"{BASE_URL}/v1/csp/policy",
                {"policy": "default-src 'self'"},
                200,
                "Update CSP Policy",
            ),
        ]

        for method, url, expected, name in csp_tests:
            if method == "POST":
                data = {"violation": "test"}
            elif method == "PUT":
                data = {"policy": "default-src 'self'"}
            else:
                data = None
            self.test_endpoint(method, url, data, expected, name)

    def test_session_management(self):
        """Test session management endpoints"""
        self.log("🎫 TESTING SESSION MANAGEMENT")

        session_tests = [
            (
                "POST",
                f"{BASE_URL}/v1/sessions/create",
                {"user_id": "test_user"},
                200,
                "Create Session",
            ),
            ("GET", f"{BASE_URL}/v1/sessions/validate", 200, "Validate Session"),
            (
                "POST",
                f"{BASE_URL}/v1/sessions/logout",
                {"session_id": "test_session"},
                200,
                "Logout Session",
            ),
        ]

        for method, url, expected, name in session_tests:
            if method == "POST":
                if "create" in url:
                    data = {"user_id": "test_user"}
                elif "logout" in url:
                    data = {"session_id": "test_session"}
                else:
                    data = {}
                self.test_endpoint(method, url, data, expected, name)
            else:
                self.test_endpoint(
                    method, url, expected_status=expected, test_name=name
                )

    def test_interview_management(self):
        """Test interview management endpoints"""
        self.log("📅 TESTING INTERVIEW MANAGEMENT")

        interview_tests = [
            ("GET", f"{BASE_URL}/v1/interviews", 200, "List Interviews"),
            (
                "POST",
                f"{BASE_URL}/v1/interviews",
                {
                    "candidate_id": 1,
                    "job_id": 1,
                    "scheduled_at": "2025-02-01T10:00:00Z",
                },
                200,
                "Schedule Interview",
            ),
        ]

        for method, url, expected, name in interview_tests:
            if method == "POST":
                data = {
                    "candidate_id": 1,
                    "job_id": 1,
                    "scheduled_at": "2025-02-01T10:00:00Z",
                }
                self.test_endpoint(method, url, data, expected, name)
            else:
                self.test_endpoint(
                    method, url, expected_status=expected, test_name=name
                )

    def test_database_management(self):
        """Test database management endpoints"""
        self.log("🗄️ TESTING DATABASE MANAGEMENT")

        db_tests = [
            ("GET", f"{BASE_URL}/v1/database/health", 200, "Database Health"),
            (
                "POST",
                f"{BASE_URL}/v1/database/add-interviewer-column",
                {},
                200,
                "Add Interviewer Column",
            ),
        ]

        for method, url, expected, name in db_tests:
            if method == "POST":
                self.test_endpoint(method, url, {}, expected, name)
            else:
                self.test_endpoint(
                    method, url, expected_status=expected, test_name=name
                )

    def test_monitoring_endpoints(self):
        """Test monitoring endpoints"""
        self.log("📊 TESTING MONITORING")

        monitoring_tests = [
            ("GET", f"{BASE_URL}/metrics", 200, "Prometheus Metrics"),
            ("GET", f"{BASE_URL}/health/detailed", 200, "Detailed Health"),
            ("GET", f"{BASE_URL}/monitoring/errors", 200, "Error Monitoring"),
            ("GET", f"{BASE_URL}/monitoring/dependencies", 200, "Dependencies"),
            ("GET", f"{BASE_URL}/monitoring/logs/search", 200, "Log Search"),
            ("GET", f"{BASE_URL}/metrics/dashboard", 200, "Metrics Dashboard"),
        ]

        for method, url, expected, name in monitoring_tests:
            self.test_endpoint(method, url, expected_status=expected, test_name=name)

    def test_agent_service(self):
        """Test AI Agent service endpoints"""
        self.log("🤖 TESTING AI AGENT SERVICE")

        agent_tests = [
            ("GET", f"{AGENT_URL}/", 200, "Agent Root"),
            ("GET", f"{AGENT_URL}/health", 200, "Agent Health"),
            ("GET", f"{AGENT_URL}/status", 200, "Agent Status"),
            ("GET", f"{AGENT_URL}/version", 200, "Agent Version"),
            ("GET", f"{AGENT_URL}/metrics", 200, "Agent Metrics"),
        ]

        for method, url, expected, name in agent_tests:
            self.test_endpoint(method, url, expected_status=expected, test_name=name)

    def test_client_portal(self):
        """Test client portal endpoints"""
        self.log("🏢 TESTING CLIENT PORTAL")

        client_tests = [
            (
                "POST",
                f"{BASE_URL}/v1/client/login",
                {"username": "TECH001", "password": "demo123"},
                200,
                "Client Login",
            ),
        ]

        for method, url, expected, name in client_tests:
            if method == "POST":
                data = {"username": "TECH001", "password": "demo123"}
                self.test_endpoint(method, url, data, expected, name)
            else:
                self.test_endpoint(
                    method, url, expected_status=expected, test_name=name
                )

    def test_analytics_reports(self):
        """Test analytics and reporting endpoints"""
        self.log("📈 TESTING ANALYTICS & REPORTS")

        analytics_tests = [
            ("GET", f"{BASE_URL}/candidates/stats", 200, "Candidate Statistics"),
            ("GET", f"{BASE_URL}/v1/reports/summary", 200, "Summary Report"),
        ]

        for method, url, expected, name in analytics_tests:
            self.test_endpoint(method, url, expected_status=expected, test_name=name)

    def stress_test_endpoints(self):
        """Perform stress testing with concurrent requests"""
        self.log("⚡ PERFORMING STRESS TESTS")

        def make_concurrent_request(endpoint):
            return requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS, timeout=5)

        endpoints = ["/health", "/v1/jobs", "/v1/candidates", "/metrics"]

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for _ in range(50):  # 50 concurrent requests
                for endpoint in endpoints:
                    future = executor.submit(make_concurrent_request, endpoint)
                    futures.append(future)

            successful = 0
            failed = 0

            for future in concurrent.futures.as_completed(futures):
                try:
                    response = future.result()
                    if response.status_code == 200:
                        successful += 1
                    else:
                        failed += 1
                except:
                    failed += 1

            self.log(f"Stress Test Results: {successful} successful, {failed} failed")

    def test_performance_benchmarks(self):
        """Test performance benchmarks"""
        self.log("🏃 TESTING PERFORMANCE BENCHMARKS")

        performance_endpoints = [
            f"{BASE_URL}/health",
            f"{BASE_URL}/v1/candidates",
            f"{BASE_URL}/v1/jobs",
            f"{BASE_URL}/v1/match/1/top",
        ]

        for endpoint in performance_endpoints:
            times = []
            for _ in range(10):
                start = time.time()
                try:
                    response = requests.get(endpoint, headers=HEADERS, timeout=5)
                    if response.status_code == 200:
                        times.append(time.time() - start)
                except:
                    pass

            if times:
                avg_time = sum(times) / len(times) * 1000
                min_time = min(times) * 1000
                max_time = max(times) * 1000
                self.log(
                    f"Performance {endpoint}: Avg={avg_time:.1f}ms, Min={min_time:.1f}ms, Max={max_time:.1f}ms"
                )

    def run_all_tests(self):
        """Run all aggressive tests"""
        self.log("🚀 STARTING AGGRESSIVE COMPREHENSIVE TESTING")
        self.log("=" * 60)

        # Core functionality tests
        self.test_core_endpoints()
        self.test_job_management()
        self.test_candidate_management()
        self.test_ai_matching()

        # Security tests
        self.test_security_features()
        self.test_authentication()
        self.test_password_management()
        self.test_csp_management()
        self.test_session_management()

        # Service tests
        self.test_interview_management()
        self.test_database_management()
        self.test_monitoring_endpoints()
        self.test_agent_service()
        self.test_client_portal()
        self.test_analytics_reports()

        # Performance tests
        self.stress_test_endpoints()
        self.test_performance_benchmarks()

        # Generate comprehensive report
        self.generate_final_report()

    def generate_final_report(self):
        """Generate comprehensive test report"""
        total_time = time.time() - self.start_time
        success_rate = (
            (len(self.passed_tests) / self.total_tests * 100)
            if self.total_tests > 0
            else 0
        )

        self.log("=" * 60)
        self.log("🎯 AGGRESSIVE TESTING COMPLETE")
        self.log("=" * 60)
        self.log(f"Total Tests: {self.total_tests}")
        self.log(f"Passed: {len(self.passed_tests)}")
        self.log(f"Failed: {len(self.failed_tests)}")
        self.log(f"Success Rate: {success_rate:.1f}%")
        self.log(f"Total Time: {total_time:.1f} seconds")

        if self.failed_tests:
            self.log("\n❌ FAILED TESTS:")
            for test in self.failed_tests:
                self.log(
                    f"  - {test.get('test_name', 'Unknown')}: {test.get('error', 'Status code mismatch')}"
                )

        if success_rate >= 90:
            self.log("\n🎉 EXCELLENT: System is highly robust!")
        elif success_rate >= 80:
            self.log("\n✅ GOOD: System is mostly functional with minor issues")
        elif success_rate >= 70:
            self.log("\n⚠️ MODERATE: System has some significant issues")
        else:
            self.log("\n🚨 CRITICAL: System has major issues requiring attention")


if __name__ == "__main__":
    tester = AggressiveTester()
    tester.run_all_tests()
