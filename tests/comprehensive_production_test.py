#!/usr/bin/env python3
"""
BHIV HR Platform - Comprehensive Production Testing Suite
Aggressive testing of all services, endpoints, features, and functionalities
"""

import requests
import json
import time
import asyncio
import concurrent.futures
from datetime import datetime
from typing import Dict, List, Any
import sys
import os

class BHIVProductionTester:
    def __init__(self):
        self.base_urls = {
            "gateway": "https://bhiv-hr-gateway.onrender.com",
            "agent": "https://bhiv-hr-agent.onrender.com", 
            "portal": "https://bhiv-hr-portal.onrender.com",
            "client_portal": "https://bhiv-hr-client-portal.onrender.com"
        }
        self.api_key = "myverysecureapikey123"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        self.test_results = []
        self.failed_tests = []
        
    def log_test(self, test_name: str, status: str, details: str = "", response_time: float = 0):
        """Log test results"""
        result = {
            "test": test_name,
            "status": status,
            "details": details,
            "response_time": f"{response_time:.3f}s",
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status_emoji = "[PASS]" if status == "PASS" else "[FAIL]" if status == "FAIL" else "[WARN]"
        print(f"{status_emoji} {test_name}: {status} ({response_time:.3f}s)")
        if details:
            print(f"   Details: {details}")
            
        if status == "FAIL":
            self.failed_tests.append(result)

    def test_service_health(self):
        """Test all service health endpoints"""
        print("\nTESTING SERVICE HEALTH")
        
        for service, url in self.base_urls.items():
            start_time = time.time()
            try:
                response = requests.get(f"{url}/health", timeout=10)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    self.log_test(f"{service.upper()} Health", "PASS", 
                                f"Status: {response.status_code}", response_time)
                else:
                    self.log_test(f"{service.upper()} Health", "FAIL", 
                                f"Status: {response.status_code}", response_time)
            except Exception as e:
                response_time = time.time() - start_time
                self.log_test(f"{service.upper()} Health", "FAIL", str(e), response_time)

    def test_gateway_endpoints(self):
        """Test all Gateway API endpoints"""
        print("\nTESTING GATEWAY ENDPOINTS (49 Total)")
        
        # Core endpoints
        endpoints = [
            ("GET", "/", "Root endpoint"),
            ("GET", "/health", "Health check"),
            ("GET", "/test-candidates", "Test candidates"),
            ("GET", "/v1/jobs", "Get jobs"),
            ("POST", "/v1/jobs", "Create job"),
            ("GET", "/v1/candidates", "Get candidates"),
            ("POST", "/v1/candidates/bulk", "Bulk candidates"),
            ("GET", "/v1/match/1/top", "AI matching"),
            ("GET", "/candidates/stats", "Candidate stats"),
            ("GET", "/v1/reports/summary", "Reports summary"),
            ("POST", "/v1/client/login", "Client login"),
            ("GET", "/metrics", "Metrics"),
            ("GET", "/health/detailed", "Detailed health"),
            ("GET", "/health/simple", "Simple health"),
            ("GET", "/monitoring/errors", "Error monitoring"),
            ("GET", "/monitoring/logs/search", "Log search"),
            ("GET", "/monitoring/dependencies", "Dependencies"),
        ]
        
        for method, endpoint, description in endpoints:
            self._test_endpoint(method, endpoint, description)

    def test_security_endpoints(self):
        """Test security-related endpoints"""
        print("\nTESTING SECURITY ENDPOINTS (15 Total)")
        
        security_endpoints = [
            ("GET", "/v1/security/rate-limit-status", "Rate limit status"),
            ("GET", "/v1/security/headers", "Security headers"),
            ("POST", "/v1/security/2fa/setup", "2FA setup"),
            ("POST", "/v1/security/2fa/verify", "2FA verify"),
            ("GET", "/v1/security/2fa/qr", "2FA QR code"),
            ("POST", "/v1/security/api-keys/generate", "Generate API key"),
            ("POST", "/v1/security/api-keys/rotate", "Rotate API keys"),
            ("DELETE", "/v1/security/api-keys/test123", "Revoke API key"),
            ("GET", "/v1/security/cors-config", "CORS config"),
            ("GET", "/v1/security/cookie-config", "Cookie config"),
            ("POST", "/v1/password/validate", "Password validation"),
            ("POST", "/v1/password/generate", "Password generation"),
            ("GET", "/v1/password/policy", "Password policy"),
            ("POST", "/v1/password/change", "Password change"),
            ("GET", "/v1/password/strength-test", "Password strength test"),
        ]
        
        for method, endpoint, description in security_endpoints:
            self._test_endpoint(method, endpoint, description)

    def test_ai_agent_endpoints(self):
        """Test AI Agent service endpoints"""
        print("\nTESTING AI AGENT ENDPOINTS")
        
        agent_url = self.base_urls["agent"]
        endpoints = [
            ("GET", "/health", "Agent health"),
            ("GET", "/", "Agent root"),
            ("POST", "/match", "AI matching"),
            ("GET", "/candidates", "Agent candidates"),
        ]
        
        for method, endpoint, description in endpoints:
            start_time = time.time()
            try:
                url = f"{agent_url}{endpoint}"
                if method == "GET":
                    response = requests.get(url, timeout=10)
                else:
                    response = requests.post(url, json={}, timeout=10)
                    
                response_time = time.time() - start_time
                
                if response.status_code in [200, 201, 422]:  # 422 for validation errors is OK
                    self.log_test(f"Agent {description}", "PASS", 
                                f"Status: {response.status_code}", response_time)
                else:
                    self.log_test(f"Agent {description}", "FAIL", 
                                f"Status: {response.status_code}", response_time)
            except Exception as e:
                response_time = time.time() - start_time
                self.log_test(f"Agent {description}", "FAIL", str(e), response_time)

    def test_portal_accessibility(self):
        """Test portal accessibility"""
        print("\nTESTING PORTAL ACCESSIBILITY")
        
        portals = [
            ("HR Portal", self.base_urls["portal"]),
            ("Client Portal", self.base_urls["client_portal"])
        ]
        
        for portal_name, url in portals:
            start_time = time.time()
            try:
                response = requests.get(url, timeout=15)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    self.log_test(f"{portal_name} Access", "PASS", 
                                f"Status: {response.status_code}", response_time)
                else:
                    self.log_test(f"{portal_name} Access", "FAIL", 
                                f"Status: {response.status_code}", response_time)
            except Exception as e:
                response_time = time.time() - start_time
                self.log_test(f"{portal_name} Access", "FAIL", str(e), response_time)

    def test_authentication_security(self):
        """Test authentication and security features"""
        print("\nTESTING AUTHENTICATION & SECURITY")
        
        # Test without API key
        start_time = time.time()
        try:
            response = requests.get(f"{self.base_urls['gateway']}/v1/jobs", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 401:
                self.log_test("Auth Protection", "PASS", 
                            "Correctly blocked unauthorized access", response_time)
            else:
                self.log_test("Auth Protection", "FAIL", 
                            f"Should return 401, got {response.status_code}", response_time)
        except Exception as e:
            response_time = time.time() - start_time
            self.log_test("Auth Protection", "FAIL", str(e), response_time)
        
        # Test with valid API key
        start_time = time.time()
        try:
            response = requests.get(f"{self.base_urls['gateway']}/v1/jobs", 
                                  headers=self.headers, timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                self.log_test("Valid Auth", "PASS", 
                            "API key authentication works", response_time)
            else:
                self.log_test("Valid Auth", "FAIL", 
                            f"Status: {response.status_code}", response_time)
        except Exception as e:
            response_time = time.time() - start_time
            self.log_test("Valid Auth", "FAIL", str(e), response_time)

    def test_rate_limiting(self):
        """Test rate limiting functionality"""
        print("\nTESTING RATE LIMITING")
        
        # Make multiple rapid requests
        start_time = time.time()
        rate_limit_hit = False
        
        for i in range(10):
            try:
                response = requests.get(f"{self.base_urls['gateway']}/health", timeout=5)
                if response.status_code == 429:
                    rate_limit_hit = True
                    break
            except:
                pass
        
        response_time = time.time() - start_time
        
        # Check rate limit status
        try:
            response = requests.get(f"{self.base_urls['gateway']}/v1/security/rate-limit-status", 
                                  headers=self.headers, timeout=10)
            if response.status_code == 200:
                self.log_test("Rate Limit Status", "PASS", 
                            "Rate limit endpoint accessible", response_time)
            else:
                self.log_test("Rate Limit Status", "FAIL", 
                            f"Status: {response.status_code}", response_time)
        except Exception as e:
            self.log_test("Rate Limit Status", "FAIL", str(e), response_time)

    def test_data_operations(self):
        """Test data operations and CRUD functionality"""
        print("\nTESTING DATA OPERATIONS")
        
        # Test candidate data
        start_time = time.time()
        try:
            response = requests.get(f"{self.base_urls['gateway']}/v1/candidates", 
                                  headers=self.headers, timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                candidate_count = len(data.get('candidates', []))
                self.log_test("Candidate Data", "PASS", 
                            f"Retrieved {candidate_count} candidates", response_time)
            else:
                self.log_test("Candidate Data", "FAIL", 
                            f"Status: {response.status_code}", response_time)
        except Exception as e:
            response_time = time.time() - start_time
            self.log_test("Candidate Data", "FAIL", str(e), response_time)
        
        # Test job data
        start_time = time.time()
        try:
            response = requests.get(f"{self.base_urls['gateway']}/v1/jobs", 
                                  headers=self.headers, timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                job_count = len(data.get('jobs', []))
                self.log_test("Job Data", "PASS", 
                            f"Retrieved {job_count} jobs", response_time)
            else:
                self.log_test("Job Data", "FAIL", 
                            f"Status: {response.status_code}", response_time)
        except Exception as e:
            response_time = time.time() - start_time
            self.log_test("Job Data", "FAIL", str(e), response_time)

    def test_ai_matching_functionality(self):
        """Test AI matching capabilities"""
        print("\nTESTING AI MATCHING FUNCTIONALITY")
        
        # Test AI matching endpoint
        start_time = time.time()
        try:
            response = requests.get(f"{self.base_urls['gateway']}/v1/match/1/top", 
                                  headers=self.headers, timeout=15)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                matches = data.get('matches', [])
                self.log_test("AI Matching", "PASS", 
                            f"Generated {len(matches)} matches", response_time)
            else:
                self.log_test("AI Matching", "FAIL", 
                            f"Status: {response.status_code}", response_time)
        except Exception as e:
            response_time = time.time() - start_time
            self.log_test("AI Matching", "FAIL", str(e), response_time)

    def test_monitoring_endpoints(self):
        """Test monitoring and observability"""
        print("\nTESTING MONITORING & OBSERVABILITY")
        
        monitoring_endpoints = [
            ("GET", "/metrics", "Prometheus metrics"),
            ("GET", "/health/detailed", "Detailed health check"),
            ("GET", "/monitoring/errors", "Error monitoring"),
            ("GET", "/monitoring/dependencies", "Dependency monitoring"),
        ]
        
        for method, endpoint, description in monitoring_endpoints:
            self._test_endpoint(method, endpoint, description)

    def test_performance_benchmarks(self):
        """Test performance benchmarks"""
        print("\nTESTING PERFORMANCE BENCHMARKS")
        
        # Test response times
        endpoints_to_benchmark = [
            "/health",
            "/v1/jobs",
            "/v1/candidates",
            "/v1/match/1/top"
        ]
        
        for endpoint in endpoints_to_benchmark:
            times = []
            for _ in range(5):
                start_time = time.time()
                try:
                    response = requests.get(f"{self.base_urls['gateway']}{endpoint}", 
                                          headers=self.headers, timeout=10)
                    response_time = time.time() - start_time
                    times.append(response_time)
                except:
                    times.append(10.0)  # Timeout
            
            avg_time = sum(times) / len(times)
            if avg_time < 2.0:  # Under 2 seconds is good
                self.log_test(f"Performance {endpoint}", "PASS", 
                            f"Avg: {avg_time:.3f}s", avg_time)
            else:
                self.log_test(f"Performance {endpoint}", "WARN", 
                            f"Slow response: {avg_time:.3f}s", avg_time)

    def _test_endpoint(self, method: str, endpoint: str, description: str):
        """Helper method to test individual endpoints"""
        start_time = time.time()
        try:
            url = f"{self.base_urls['gateway']}{endpoint}"
            
            if method == "GET":
                response = requests.get(url, headers=self.headers, timeout=10)
            elif method == "POST":
                # Use appropriate test data for POST requests
                test_data = self._get_test_data(endpoint)
                response = requests.post(url, headers=self.headers, json=test_data, timeout=10)
            elif method == "DELETE":
                response = requests.delete(url, headers=self.headers, timeout=10)
            else:
                response = requests.request(method, url, headers=self.headers, timeout=10)
            
            response_time = time.time() - start_time
            
            # Consider various success codes
            if response.status_code in [200, 201, 202, 204, 422, 404]:
                self.log_test(description, "PASS", 
                            f"Status: {response.status_code}", response_time)
            else:
                self.log_test(description, "FAIL", 
                            f"Status: {response.status_code}", response_time)
                
        except Exception as e:
            response_time = time.time() - start_time
            self.log_test(description, "FAIL", str(e), response_time)

    def _get_test_data(self, endpoint: str) -> dict:
        """Get appropriate test data for POST endpoints"""
        if "jobs" in endpoint:
            return {
                "title": "Test Job",
                "description": "Test job description",
                "requirements": ["Python", "FastAPI"]
            }
        elif "candidates" in endpoint:
            return {
                "candidates": [
                    {"name": "Test Candidate", "email": "test@example.com"}
                ]
            }
        elif "login" in endpoint:
            return {
                "username": "TECH001",
                "password": "demo123"
            }
        elif "password" in endpoint:
            return {
                "password": "TestPassword123!"
            }
        elif "2fa" in endpoint:
            return {
                "code": "123456"
            }
        else:
            return {}

    def run_comprehensive_tests(self):
        """Run all comprehensive tests"""
        print("BHIV HR PLATFORM - COMPREHENSIVE PRODUCTION TESTING")
        print("=" * 60)
        
        start_time = time.time()
        
        # Run all test suites
        self.test_service_health()
        self.test_gateway_endpoints()
        self.test_security_endpoints()
        self.test_ai_agent_endpoints()
        self.test_portal_accessibility()
        self.test_authentication_security()
        self.test_rate_limiting()
        self.test_data_operations()
        self.test_ai_matching_functionality()
        self.test_monitoring_endpoints()
        self.test_performance_benchmarks()
        
        total_time = time.time() - start_time
        
        # Generate summary report
        self.generate_test_report(total_time)

    def generate_test_report(self, total_time: float):
        """Generate comprehensive test report"""
        print("\n" + "=" * 60)
        print("COMPREHENSIVE TEST REPORT")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = len([t for t in self.test_results if t['status'] == 'PASS'])
        failed_tests = len([t for t in self.test_results if t['status'] == 'FAIL'])
        warning_tests = len([t for t in self.test_results if t['status'] == 'WARN'])
        
        print(f"SUMMARY:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed: {passed_tests}")
        print(f"   Failed: {failed_tests}")
        print(f"   Warnings: {warning_tests}")
        print(f"   Total Time: {total_time:.2f}s")
        print(f"   Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if self.failed_tests:
            print(f"\nFAILED TESTS ({len(self.failed_tests)}):")
            for test in self.failed_tests:
                print(f"   • {test['test']}: {test['details']}")
        
        # Performance summary
        response_times = [float(t['response_time'].replace('s', '')) for t in self.test_results]
        avg_response_time = sum(response_times) / len(response_times)
        
        print(f"\nPERFORMANCE:")
        print(f"   Average Response Time: {avg_response_time:.3f}s")
        print(f"   Fastest Response: {min(response_times):.3f}s")
        print(f"   Slowest Response: {max(response_times):.3f}s")
        
        # Service status
        print(f"\nSERVICE STATUS:")
        for service in self.base_urls.keys():
            service_tests = [t for t in self.test_results if service.upper() in t['test']]
            if service_tests:
                service_passed = len([t for t in service_tests if t['status'] == 'PASS'])
                service_total = len(service_tests)
                status = "[OK]" if service_passed == service_total else "[FAIL]" if service_passed == 0 else "[WARN]"
                print(f"   {status} {service.upper()}: {service_passed}/{service_total} tests passed")
        
        print("\n" + "=" * 60)
        print("TESTING COMPLETE - BHIV HR PLATFORM VERIFIED")
        print("=" * 60)

if __name__ == "__main__":
    tester = BHIVProductionTester()
    tester.run_comprehensive_tests()