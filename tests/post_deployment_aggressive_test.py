#!/usr/bin/env python3
"""
BHIV HR Platform - Post-Deployment Aggressive Testing Suite
Comprehensive verification of all deployed features, functions, and endpoints
"""

import requests
import json
import time
import concurrent.futures
from datetime import datetime
import threading

class AggressiveTester:
    def __init__(self):
        self.base_urls = {
            "gateway": "https://bhiv-hr-gateway.onrender.com",
            "agent": "https://bhiv-hr-agent.onrender.com",
            "portal": "https://bhiv-hr-portal.onrender.com", 
            "client_portal": "https://bhiv-hr-client-portal.onrender.com"
        }
        self.api_key = "myverysecureapikey123"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        self.results = {"passed": 0, "failed": 0, "warnings": 0, "total": 0}
        self.failures = []

    def test(self, name, expected_status, actual_status, details=""):
        """Record test result"""
        self.results["total"] += 1
        if actual_status == expected_status:
            self.results["passed"] += 1
            print(f"[PASS] {name}")
        elif actual_status in [200, 201, 202] and expected_status in [200, 201, 202]:
            self.results["passed"] += 1
            print(f"[PASS] {name} (got {actual_status})")
        else:
            self.results["failed"] += 1
            self.failures.append(f"{name}: Expected {expected_status}, got {actual_status}")
            print(f"[FAIL] {name}: Expected {expected_status}, got {actual_status}")
        if details:
            print(f"       {details}")

    def test_core_endpoints(self):
        """Test all core API endpoints"""
        print("\n=== CORE ENDPOINTS ===")
        
        endpoints = [
            ("GET", "/", 200, "Root endpoint"),
            ("GET", "/health", 200, "Health check"),
            ("GET", "/test-candidates", 200, "Test candidates"),
            ("GET", "/favicon.ico", 204, "Favicon"),
            ("GET", "/http-methods-test", 200, "HTTP methods test"),
        ]
        
        for method, path, expected, desc in endpoints:
            try:
                response = requests.get(f"{self.base_urls['gateway']}{path}", 
                                      headers=self.headers, timeout=10)
                self.test(desc, expected, response.status_code)
            except Exception as e:
                self.test(desc, expected, "ERROR", str(e))

    def test_job_management(self):
        """Test job management endpoints"""
        print("\n=== JOB MANAGEMENT ===")
        
        # Get jobs
        try:
            response = requests.get(f"{self.base_urls['gateway']}/v1/jobs", 
                                  headers=self.headers, timeout=10)
            self.test("Get all jobs", 200, response.status_code)
            if response.status_code == 200:
                data = response.json()
                job_count = len(data.get('jobs', []))
                print(f"       Found {job_count} jobs")
        except Exception as e:
            self.test("Get all jobs", 200, "ERROR", str(e))
        
        # Create job
        job_data = {
            "title": "Test Job",
            "department": "Engineering", 
            "location": "Remote",
            "experience_level": "Mid-level",
            "requirements": "Python, FastAPI",
            "description": "Test job description"
        }
        try:
            response = requests.post(f"{self.base_urls['gateway']}/v1/jobs",
                                   headers=self.headers, json=job_data, timeout=10)
            self.test("Create job", 200, response.status_code)
        except Exception as e:
            self.test("Create job", 200, "ERROR", str(e))

    def test_candidate_management(self):
        """Test candidate management endpoints"""
        print("\n=== CANDIDATE MANAGEMENT ===")
        
        endpoints = [
            ("/v1/candidates", "Get all candidates"),
            ("/v1/candidates/job/1", "Get candidates by job"),
            ("/v1/candidates/search", "Search candidates"),
        ]
        
        for path, desc in endpoints:
            try:
                response = requests.get(f"{self.base_urls['gateway']}{path}",
                                      headers=self.headers, timeout=10)
                self.test(desc, 200, response.status_code)
                if response.status_code == 200:
                    data = response.json()
                    count = len(data.get('candidates', []))
                    print(f"       Found {count} candidates")
            except Exception as e:
                self.test(desc, 200, "ERROR", str(e))
        
        # Test bulk upload
        bulk_data = {
            "candidates": [
                {
                    "name": "Test Candidate",
                    "email": f"test{int(time.time())}@example.com",
                    "technical_skills": "Python, JavaScript",
                    "experience_years": 3
                }
            ]
        }
        try:
            response = requests.post(f"{self.base_urls['gateway']}/v1/candidates/bulk",
                                   headers=self.headers, json=bulk_data, timeout=10)
            self.test("Bulk candidate upload", 200, response.status_code)
        except Exception as e:
            self.test("Bulk candidate upload", 200, "ERROR", str(e))

    def test_ai_matching(self):
        """Test AI matching functionality"""
        print("\n=== AI MATCHING ENGINE ===")
        
        endpoints = [
            ("/v1/match/1/top", "AI matching for job 1"),
            ("/v1/match/performance-test", "Performance test"),
            ("/v1/match/cache-status", "Cache status"),
        ]
        
        for path, desc in endpoints:
            try:
                response = requests.get(f"{self.base_urls['gateway']}{path}",
                                      headers=self.headers, timeout=15)
                self.test(desc, 200, response.status_code)
                if "match" in path and response.status_code == 200:
                    data = response.json()
                    matches = len(data.get('matches', []))
                    print(f"       Generated {matches} matches")
            except Exception as e:
                self.test(desc, 200, "ERROR", str(e))

    def test_security_features(self):
        """Test security endpoints"""
        print("\n=== SECURITY FEATURES ===")
        
        # Authentication tests
        try:
            response = requests.get(f"{self.base_urls['gateway']}/v1/jobs", timeout=10)
            self.test("Auth protection (no key)", 403, response.status_code)
        except Exception as e:
            self.test("Auth protection (no key)", 403, "ERROR", str(e))
        
        try:
            bad_headers = {"Authorization": "Bearer invalid_key"}
            response = requests.get(f"{self.base_urls['gateway']}/v1/jobs",
                                  headers=bad_headers, timeout=10)
            self.test("Auth protection (bad key)", 401, response.status_code)
        except Exception as e:
            self.test("Auth protection (bad key)", 401, "ERROR", str(e))
        
        # Security endpoints
        security_endpoints = [
            ("/v1/security/rate-limit-status", "Rate limit status"),
            ("/v1/security/cors-config", "CORS config"),
            ("/v1/security/cookie-config", "Cookie config"),
            ("/v1/security/blocked-ips", "Blocked IPs"),
            ("/v1/security/penetration-test-endpoints", "Penetration test endpoints"),
        ]
        
        for path, desc in security_endpoints:
            try:
                response = requests.get(f"{self.base_urls['gateway']}{path}",
                                      headers=self.headers, timeout=10)
                self.test(desc, 200, response.status_code)
            except Exception as e:
                self.test(desc, 200, "ERROR", str(e))

    def test_password_management(self):
        """Test password management"""
        print("\n=== PASSWORD MANAGEMENT ===")
        
        # Password validation
        password_data = {"password": "TestPassword123!"}
        try:
            response = requests.post(f"{self.base_urls['gateway']}/v1/password/validate",
                                   headers=self.headers, json=password_data, timeout=10)
            self.test("Password validation", 200, response.status_code)
            if response.status_code == 200:
                data = response.json()
                print(f"       Strength: {data.get('password_strength')}")
        except Exception as e:
            self.test("Password validation", 200, "ERROR", str(e))
        
        # Other password endpoints
        endpoints = [
            ("GET", "/v1/password/generate", "Password generation"),
            ("GET", "/v1/password/policy", "Password policy"),
            ("GET", "/v1/password/strength-test", "Strength test tool"),
            ("GET", "/v1/password/security-tips", "Security tips"),
        ]
        
        for method, path, desc in endpoints:
            try:
                response = requests.get(f"{self.base_urls['gateway']}{path}",
                                      headers=self.headers, timeout=10)
                self.test(desc, 200, response.status_code)
            except Exception as e:
                self.test(desc, 200, "ERROR", str(e))

    def test_2fa_system(self):
        """Test 2FA functionality"""
        print("\n=== TWO-FACTOR AUTHENTICATION ===")
        
        # 2FA setup
        setup_data = {"user_id": "test_user"}
        try:
            response = requests.post(f"{self.base_urls['gateway']}/v1/2fa/setup",
                                   headers=self.headers, json=setup_data, timeout=10)
            self.test("2FA setup", 200, response.status_code)
        except Exception as e:
            self.test("2FA setup", 200, "ERROR", str(e))
        
        # Other 2FA endpoints
        endpoints = [
            ("GET", "/v1/2fa/demo-setup", "2FA demo setup"),
            ("GET", "/v1/2fa/status/test_user", "2FA status"),
        ]
        
        for method, path, desc in endpoints:
            try:
                response = requests.get(f"{self.base_urls['gateway']}{path}",
                                      headers=self.headers, timeout=10)
                self.test(desc, 200, response.status_code)
            except Exception as e:
                self.test(desc, 200, "ERROR", str(e))

    def test_monitoring_system(self):
        """Test monitoring and observability"""
        print("\n=== MONITORING SYSTEM ===")
        
        endpoints = [
            ("/metrics", "Prometheus metrics"),
            ("/health/detailed", "Detailed health"),
            ("/health/simple", "Simple health"),
            ("/monitoring/errors", "Error monitoring"),
            ("/monitoring/dependencies", "Dependencies"),
            ("/metrics/dashboard", "Metrics dashboard"),
        ]
        
        for path, desc in endpoints:
            try:
                response = requests.get(f"{self.base_urls['gateway']}{path}",
                                      headers=self.headers, timeout=10)
                self.test(desc, 200, response.status_code)
            except Exception as e:
                self.test(desc, 200, "ERROR", str(e))

    def test_database_operations(self):
        """Test database functionality"""
        print("\n=== DATABASE OPERATIONS ===")
        
        endpoints = [
            ("/v1/database/health", "Database health"),
            ("/candidates/stats", "Candidate statistics"),
        ]
        
        for path, desc in endpoints:
            try:
                response = requests.get(f"{self.base_urls['gateway']}{path}",
                                      headers=self.headers, timeout=10)
                self.test(desc, 200, response.status_code)
                if "stats" in path and response.status_code == 200:
                    data = response.json()
                    print(f"       Total candidates: {data.get('total_candidates', 0)}")
            except Exception as e:
                self.test(desc, 200, "ERROR", str(e))

    def test_ai_agent_service(self):
        """Test AI Agent service"""
        print("\n=== AI AGENT SERVICE ===")
        
        agent_url = self.base_urls["agent"]
        endpoints = [
            ("/", "Agent root"),
            ("/health", "Agent health"),
            ("/docs", "Agent documentation"),
        ]
        
        for path, desc in endpoints:
            try:
                response = requests.get(f"{agent_url}{path}", timeout=10)
                self.test(desc, 200, response.status_code)
            except Exception as e:
                self.test(desc, 200, "ERROR", str(e))

    def test_portal_services(self):
        """Test portal services"""
        print("\n=== PORTAL SERVICES ===")
        
        portals = [
            ("HR Portal", self.base_urls["portal"]),
            ("Client Portal", self.base_urls["client_portal"])
        ]
        
        for name, url in portals:
            try:
                response = requests.get(url, timeout=15)
                self.test(f"{name} accessibility", 200, response.status_code)
            except Exception as e:
                self.test(f"{name} accessibility", 200, "ERROR", str(e))

    def test_performance_benchmarks(self):
        """Test performance under load"""
        print("\n=== PERFORMANCE TESTING ===")
        
        def make_request(endpoint):
            try:
                start = time.time()
                response = requests.get(f"{self.base_urls['gateway']}{endpoint}",
                                      headers=self.headers, timeout=10)
                return time.time() - start, response.status_code
            except:
                return 10.0, 500
        
        # Test critical endpoints under concurrent load
        endpoints = ["/health", "/v1/jobs", "/v1/candidates", "/v1/match/1/top"]
        
        for endpoint in endpoints:
            times = []
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                futures = [executor.submit(make_request, endpoint) for _ in range(5)]
                for future in concurrent.futures.as_completed(futures):
                    response_time, status = future.result()
                    times.append(response_time)
            
            avg_time = sum(times) / len(times)
            if avg_time < 3.0:
                self.test(f"Performance {endpoint}", "GOOD", "GOOD", f"Avg: {avg_time:.2f}s")
            else:
                self.test(f"Performance {endpoint}", "GOOD", "SLOW", f"Avg: {avg_time:.2f}s")

    def test_error_handling(self):
        """Test error handling and edge cases"""
        print("\n=== ERROR HANDLING ===")
        
        # Test invalid endpoints
        try:
            response = requests.get(f"{self.base_urls['gateway']}/invalid-endpoint",
                                  headers=self.headers, timeout=10)
            self.test("Invalid endpoint handling", 404, response.status_code)
        except Exception as e:
            self.test("Invalid endpoint handling", 404, "ERROR", str(e))
        
        # Test malformed requests
        try:
            response = requests.post(f"{self.base_urls['gateway']}/v1/jobs",
                                   headers=self.headers, json={"invalid": "data"}, timeout=10)
            self.test("Malformed request handling", 422, response.status_code)
        except Exception as e:
            self.test("Malformed request handling", 422, "ERROR", str(e))

    def run_comprehensive_test(self):
        """Run all tests"""
        print("BHIV HR PLATFORM - POST-DEPLOYMENT AGGRESSIVE TESTING")
        print("=" * 70)
        print(f"Started at: {datetime.now().isoformat()}")
        
        start_time = time.time()
        
        # Run all test suites
        self.test_core_endpoints()
        self.test_job_management()
        self.test_candidate_management()
        self.test_ai_matching()
        self.test_security_features()
        self.test_password_management()
        self.test_2fa_system()
        self.test_monitoring_system()
        self.test_database_operations()
        self.test_ai_agent_service()
        self.test_portal_services()
        self.test_performance_benchmarks()
        self.test_error_handling()
        
        total_time = time.time() - start_time
        
        # Generate final report
        print("\n" + "=" * 70)
        print("AGGRESSIVE TESTING RESULTS")
        print("=" * 70)
        
        print(f"Total Tests: {self.results['total']}")
        print(f"Passed: {self.results['passed']}")
        print(f"Failed: {self.results['failed']}")
        print(f"Success Rate: {(self.results['passed']/self.results['total'])*100:.1f}%")
        print(f"Testing Time: {total_time:.1f}s")
        
        if self.failures:
            print(f"\nFAILED TESTS ({len(self.failures)}):")
            for failure in self.failures:
                print(f"  - {failure}")
        
        # Final assessment
        success_rate = (self.results['passed']/self.results['total'])*100
        if success_rate >= 95:
            print("\n[EXCELLENT] Platform is performing exceptionally well!")
        elif success_rate >= 90:
            print("\n[VERY GOOD] Platform is performing very well!")
        elif success_rate >= 85:
            print("\n[GOOD] Platform is performing well with minor issues!")
        else:
            print("\n[NEEDS ATTENTION] Platform has some issues that need addressing!")
        
        print(f"\nCompleted at: {datetime.now().isoformat()}")
        return success_rate

if __name__ == "__main__":
    tester = AggressiveTester()
    tester.run_comprehensive_test()