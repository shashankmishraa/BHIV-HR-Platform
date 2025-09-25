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
                    f"PASS {test_name}: {method} {url} - {response.status_code} ({duration*1000:.1f}ms)"
                )
            else:
                self.failed_tests.append(result)
                self.log(
                    f"FAIL {test_name}: {method} {url} - Expected {expected_status}, got {response.status_code}",
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
            self.log(
                f"ERROR {test_name}: {method} {url} - Exception: {str(e)}", "ERROR"
            )
            return {"success": False, "error": str(e)}

    def run_comprehensive_tests(self):
        """Run all comprehensive tests"""
        self.log("STARTING AGGRESSIVE COMPREHENSIVE TESTING")
        self.log("=" * 60)

        # Test all endpoints systematically
        test_cases = [
            # Core endpoints
            ("GET", f"{BASE_URL}/", 200, "Root Endpoint"),
            ("GET", f"{BASE_URL}/health", 200, "Health Check"),
            ("GET", f"{BASE_URL}/test-candidates", 200, "Test Candidates"),
            ("GET", f"{BASE_URL}/http-methods-test", 200, "HTTP Methods Test"),
            # Job Management
            (
                "POST",
                f"{BASE_URL}/v1/jobs",
                {
                    "title": "Test Job",
                    "description": "Test",
                    "requirements": ["Python"],
                },
                200,
                "Create Job",
            ),
            ("GET", f"{BASE_URL}/v1/jobs", 200, "List Jobs"),
            # Candidate Management
            ("GET", f"{BASE_URL}/v1/candidates", 200, "List Candidates"),
            ("GET", f"{BASE_URL}/v1/candidates/stats", 200, "Candidate Stats"),
            (
                "POST",
                f"{BASE_URL}/v1/candidates/search",
                {"query": "python"},
                200,
                "Search Candidates",
            ),
            # AI Matching
            ("GET", f"{BASE_URL}/v1/match/1/top", 200, "Top Matches"),
            (
                "GET",
                f"{BASE_URL}/v1/match/performance-test",
                200,
                "AI Performance Test",
            ),
            ("GET", f"{BASE_URL}/v1/match/cache-status", 200, "Cache Status"),
            ("GET", f"{BASE_URL}/v1/match/cache-clear", 200, "Clear Cache"),
            # Security Features
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
            # Authentication
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
            # Password Management
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
            # CSP Management
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
            # Session Management
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
            # Interview Management
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
            # Database Management
            ("GET", f"{BASE_URL}/v1/database/health", 200, "Database Health"),
            (
                "POST",
                f"{BASE_URL}/v1/database/add-interviewer-column",
                {},
                200,
                "Add Interviewer Column",
            ),
            # Monitoring
            ("GET", f"{BASE_URL}/metrics", 200, "Prometheus Metrics"),
            ("GET", f"{BASE_URL}/health/detailed", 200, "Detailed Health"),
            ("GET", f"{BASE_URL}/monitoring/errors", 200, "Error Monitoring"),
            ("GET", f"{BASE_URL}/monitoring/dependencies", 200, "Dependencies"),
            ("GET", f"{BASE_URL}/monitoring/logs/search", 200, "Log Search"),
            ("GET", f"{BASE_URL}/metrics/dashboard", 200, "Metrics Dashboard"),
            # Agent Service
            ("GET", f"{AGENT_URL}/", 200, "Agent Root"),
            ("GET", f"{AGENT_URL}/health", 200, "Agent Health"),
            ("GET", f"{AGENT_URL}/status", 200, "Agent Status"),
            ("GET", f"{AGENT_URL}/version", 200, "Agent Version"),
            ("GET", f"{AGENT_URL}/metrics", 200, "Agent Metrics"),
            # Client Portal
            (
                "POST",
                f"{BASE_URL}/v1/client/login",
                {"username": "TECH001", "password": "demo123"},
                200,
                "Client Login",
            ),
            # Analytics
            ("GET", f"{BASE_URL}/candidates/stats", 200, "Candidate Statistics"),
            ("GET", f"{BASE_URL}/v1/reports/summary", 200, "Summary Report"),
        ]

        # Execute all tests
        for test_case in test_cases:
            if len(test_case) == 4:
                method, url, expected_status, name = test_case
                self.test_endpoint(method, url, None, expected_status, name)
            elif len(test_case) == 5:
                method, url, data, expected_status, name = test_case
                self.test_endpoint(method, url, data, expected_status, name)

        # Performance testing
        self.performance_test()

        # Stress testing
        self.stress_test()

        # Generate final report
        self.generate_final_report()

    def performance_test(self):
        """Test performance benchmarks"""
        self.log("TESTING PERFORMANCE BENCHMARKS")

        performance_endpoints = [
            f"{BASE_URL}/health",
            f"{BASE_URL}/v1/candidates",
            f"{BASE_URL}/v1/jobs",
            f"{BASE_URL}/v1/match/1/top",
        ]

        for endpoint in performance_endpoints:
            times = []
            for _ in range(5):
                start = time.time()
                try:
                    response = requests.get(endpoint, headers=HEADERS, timeout=5)
                    if response.status_code == 200:
                        times.append(time.time() - start)
                except:
                    pass

            if times:
                avg_time = sum(times) / len(times) * 1000
                self.log(
                    f"Performance {endpoint.split('/')[-1]}: {avg_time:.1f}ms average"
                )

    def stress_test(self):
        """Perform stress testing"""
        self.log("PERFORMING STRESS TESTS")

        def make_request():
            try:
                response = requests.get(
                    f"{BASE_URL}/health", headers=HEADERS, timeout=5
                )
                return response.status_code == 200
            except:
                return False

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(20)]
            successful = sum(
                1
                for future in concurrent.futures.as_completed(futures)
                if future.result()
            )

        self.log(f"Stress Test: {successful}/20 requests successful")

    def generate_final_report(self):
        """Generate comprehensive test report"""
        total_time = time.time() - self.start_time
        success_rate = (
            (len(self.passed_tests) / self.total_tests * 100)
            if self.total_tests > 0
            else 0
        )

        self.log("=" * 60)
        self.log("AGGRESSIVE TESTING COMPLETE")
        self.log("=" * 60)
        self.log(f"Total Tests: {self.total_tests}")
        self.log(f"Passed: {len(self.passed_tests)}")
        self.log(f"Failed: {len(self.failed_tests)}")
        self.log(f"Success Rate: {success_rate:.1f}%")
        self.log(f"Total Time: {total_time:.1f} seconds")

        if self.failed_tests:
            self.log("\nFAILED TESTS:")
            for test in self.failed_tests[:10]:  # Show first 10 failures
                self.log(
                    f"  - {test.get('test_name', 'Unknown')}: {test.get('error', 'Status code mismatch')}"
                )

        if success_rate >= 90:
            self.log("\nEXCELLENT: System is highly robust!")
        elif success_rate >= 80:
            self.log("\nGOOD: System is mostly functional with minor issues")
        elif success_rate >= 70:
            self.log("\nMODERATE: System has some significant issues")
        else:
            self.log("\nCRITICAL: System has major issues requiring attention")


if __name__ == "__main__":
    tester = AggressiveTester()
    tester.run_comprehensive_tests()
