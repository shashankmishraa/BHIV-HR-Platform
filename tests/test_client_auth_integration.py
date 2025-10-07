#!/usr/bin/env python3
"""
Comprehensive Client Portal Auth Integration Test
Tests auth service with all services and database connectivity
"""

import requests
import json
import time
import sys
import os
from datetime import datetime

# Test Configuration
GATEWAY_URL = "https://bhiv-hr-gateway-46pz.onrender.com"
AGENT_URL = "https://bhiv-hr-agent-m1me.onrender.com"
HR_PORTAL_URL = "https://bhiv-hr-portal-cead.onrender.com"
CLIENT_PORTAL_URL = "https://bhiv-hr-client-portal-5g33.onrender.com"

# Test credentials
TEST_CLIENT_ID = "TECH001"
TEST_PASSWORD = "demo123"

class ClientAuthIntegrationTest:
    def __init__(self):
        self.results = []
        self.token = None
        self.client_data = None
        
    def log_result(self, test_name, success, message, details=None):
        """Log test result"""
        status = "PASS" if success else "FAIL"
        result = {
            'test': test_name,
            'status': status,
            'message': message,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        self.results.append(result)
        print(f"{status} {test_name}: {message}")
        if details and not success:
            print(f"   Details: {details}")
    
    def test_service_health(self):
        """Test all service health endpoints"""
        services = [
            ("Gateway", f"{GATEWAY_URL}/health"),
            ("Agent", f"{AGENT_URL}/health"),
            ("HR Portal", HR_PORTAL_URL),
            ("Client Portal", CLIENT_PORTAL_URL)
        ]
        
        for service_name, url in services:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    self.log_result(f"{service_name} Health", True, f"Service is healthy")
                else:
                    self.log_result(f"{service_name} Health", False, f"HTTP {response.status_code}")
            except Exception as e:
                self.log_result(f"{service_name} Health", False, f"Connection failed: {str(e)}")
    
    def test_database_connectivity(self):
        """Test database connectivity through Gateway"""
        try:
            response = requests.get(f"{GATEWAY_URL}/v1/candidates", timeout=10)
            if response.status_code == 200:
                data = response.json()
                candidate_count = len(data.get('candidates', []))
                self.log_result("Database Connectivity", True, f"Connected - {candidate_count} candidates found")
            else:
                self.log_result("Database Connectivity", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_result("Database Connectivity", False, f"Failed: {str(e)}")
    
    def test_client_portal_auth_endpoint(self):
        """Test client portal authentication endpoint"""
        try:
            auth_data = {
                "client_id": TEST_CLIENT_ID,
                "password": TEST_PASSWORD
            }
            
            response = requests.post(
                f"{GATEWAY_URL}/v1/client/login",
                json=auth_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.token = data.get('token')
                    self.client_data = data
                    self.log_result("Client Auth Endpoint", True, f"Authentication successful for {TEST_CLIENT_ID}")
                    return True
                else:
                    self.log_result("Client Auth Endpoint", False, f"Auth failed: {data.get('error')}")
            else:
                self.log_result("Client Auth Endpoint", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_result("Client Auth Endpoint", False, f"Request failed: {str(e)}")
        return False
    
    def test_authenticated_endpoints(self):
        """Test authenticated endpoints with client token"""
        if not self.token:
            self.log_result("Authenticated Endpoints", False, "No token available")
            return
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # Test job endpoints
        endpoints = [
            ("GET Jobs", f"{GATEWAY_URL}/v1/jobs"),
            ("GET Candidates", f"{GATEWAY_URL}/v1/candidates"),
            ("GET Metrics", f"{GATEWAY_URL}/metrics")
        ]
        
        for endpoint_name, url in endpoints:
            try:
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code == 200:
                    self.log_result(f"Auth {endpoint_name}", True, "Access granted")
                else:
                    self.log_result(f"Auth {endpoint_name}", False, f"HTTP {response.status_code}")
            except Exception as e:
                self.log_result(f"Auth {endpoint_name}", False, f"Request failed: {str(e)}")
    
    def test_job_posting_flow(self):
        """Test complete job posting flow"""
        if not self.token:
            self.log_result("Job Posting Flow", False, "No token available")
            return
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # Create test job
        job_data = {
            "title": "Test Integration Engineer",
            "company": self.client_data.get('company_name', 'Test Company'),
            "location": "Remote",
            "description": "Integration test job posting",
            "requirements": ["Python", "Testing", "API Integration"],
            "salary_range": "80000-120000",
            "job_type": "Full-time",
            "experience_level": "Mid-level"
        }
        
        try:
            response = requests.post(
                f"{GATEWAY_URL}/v1/jobs",
                json=job_data,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 201:
                job_response = response.json()
                job_id = job_response.get('job_id')
                self.log_result("Job Posting Flow", True, f"Job created with ID: {job_id}")
                
                # Test job retrieval
                get_response = requests.get(f"{GATEWAY_URL}/v1/jobs", headers=headers, timeout=10)
                if get_response.status_code == 200:
                    jobs = get_response.json().get('jobs', [])
                    if any(job.get('id') == job_id for job in jobs):
                        self.log_result("Job Retrieval", True, "Posted job found in listings")
                    else:
                        self.log_result("Job Retrieval", False, "Posted job not found in listings")
                
            else:
                self.log_result("Job Posting Flow", False, f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_result("Job Posting Flow", False, f"Request failed: {str(e)}")
    
    def test_ai_matching_integration(self):
        """Test AI matching service integration"""
        if not self.token:
            self.log_result("AI Matching Integration", False, "No token available")
            return
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        try:
            # Get available jobs first
            jobs_response = requests.get(f"{GATEWAY_URL}/v1/jobs", headers=headers, timeout=10)
            if jobs_response.status_code == 200:
                jobs = jobs_response.json().get('jobs', [])
                if jobs:
                    job_id = jobs[0].get('id')
                    
                    # Test AI matching
                    match_response = requests.get(
                        f"{GATEWAY_URL}/v1/match/{job_id}/top",
                        headers=headers,
                        timeout=15
                    )
                    
                    if match_response.status_code == 200:
                        matches = match_response.json()
                        match_count = len(matches.get('matches', []))
                        self.log_result("AI Matching Integration", True, f"Found {match_count} candidate matches")
                    else:
                        self.log_result("AI Matching Integration", False, f"HTTP {match_response.status_code}")
                else:
                    self.log_result("AI Matching Integration", False, "No jobs available for matching")
            else:
                self.log_result("AI Matching Integration", False, "Could not retrieve jobs")
                
        except Exception as e:
            self.log_result("AI Matching Integration", False, f"Request failed: {str(e)}")
    
    def test_portal_accessibility(self):
        """Test portal accessibility"""
        portals = [
            ("HR Portal", HR_PORTAL_URL),
            ("Client Portal", CLIENT_PORTAL_URL)
        ]
        
        for portal_name, url in portals:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    content_length = len(response.content)
                    self.log_result(f"{portal_name} Access", True, f"Portal accessible ({content_length} bytes)")
                else:
                    self.log_result(f"{portal_name} Access", False, f"HTTP {response.status_code}")
            except Exception as e:
                self.log_result(f"{portal_name} Access", False, f"Connection failed: {str(e)}")
    
    def test_security_features(self):
        """Test security features"""
        # Test invalid credentials
        try:
            invalid_auth = {
                "client_id": "INVALID",
                "password": "wrong"
            }
            
            response = requests.post(
                f"{GATEWAY_URL}/v1/client/login",
                json=invalid_auth,
                timeout=10
            )
            
            if response.status_code == 401 or (response.status_code == 200 and not response.json().get('success')):
                self.log_result("Security - Invalid Auth", True, "Invalid credentials properly rejected")
            else:
                self.log_result("Security - Invalid Auth", False, "Invalid credentials accepted")
                
        except Exception as e:
            self.log_result("Security - Invalid Auth", False, f"Test failed: {str(e)}")
        
        # Test rate limiting
        try:
            rate_response = requests.get(f"{GATEWAY_URL}/v1/security/rate-limit-status", timeout=10)
            if rate_response.status_code == 200:
                self.log_result("Security - Rate Limiting", True, "Rate limiting endpoint accessible")
            else:
                self.log_result("Security - Rate Limiting", False, f"HTTP {rate_response.status_code}")
        except Exception as e:
            self.log_result("Security - Rate Limiting", False, f"Test failed: {str(e)}")
    
    def run_all_tests(self):
        """Run complete integration test suite"""
        print("Starting Client Portal Auth Integration Tests")
        print("=" * 60)
        
        # Core service tests
        self.test_service_health()
        self.test_database_connectivity()
        
        # Authentication tests
        auth_success = self.test_client_portal_auth_endpoint()
        
        if auth_success:
            self.test_authenticated_endpoints()
            self.test_job_posting_flow()
            self.test_ai_matching_integration()
        
        # Portal and security tests
        self.test_portal_accessibility()
        self.test_security_features()
        
        # Summary
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for r in self.results if "PASS" in r['status'])
        failed = sum(1 for r in self.results if "FAIL" in r['status'])
        total = len(self.results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if failed > 0:
            print("\nFAILED TESTS:")
            for result in self.results:
                if "FAIL" in result['status']:
                    print(f"  - {result['test']}: {result['message']}")
        
        print(f"\nClient Auth Integration: {'OPERATIONAL' if passed >= total * 0.8 else 'ISSUES DETECTED'}")
        
        return passed >= total * 0.8

if __name__ == "__main__":
    tester = ClientAuthIntegrationTest()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)