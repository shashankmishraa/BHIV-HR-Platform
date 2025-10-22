#!/usr/bin/env python3
"""
Client Portal Endpoints Test Suite
Tests all client portal endpoints including authentication, job management, and candidate operations
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "https://bhiv-hr-gateway-46pz.onrender.com"
CLIENT_CREDENTIALS = {
    "client_id": "TECH001",
    "password": "demo123"
}

class ClientPortalTester:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.test_results = []
        
    def log_test(self, endpoint, method, status, response_time, details=""):
        """Log test results"""
        result = {
            "endpoint": endpoint,
            "method": method,
            "status": "PASS" if status else "FAIL",
            "response_time": f"{response_time:.3f}s",
            "details": details,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }
        self.test_results.append(result)
        print(f"{result['status']} {method} {endpoint} ({result['response_time']}) - {details}")

    def test_client_authentication(self):
        """Test client login endpoint"""
        print("\n[AUTH] Testing Client Authentication...")
        
        start_time = time.time()
        try:
            response = self.session.post(
                f"{BASE_URL}/v1/client/login",
                json=CLIENT_CREDENTIALS,
                timeout=10
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if "access_token" in data:
                    self.token = data["access_token"]
                    self.session.headers.update({"Authorization": f"Bearer {self.token}"})
                    self.log_test("/v1/client/login", "POST", True, response_time, "Login successful, token received")
                    return True
                else:
                    self.log_test("/v1/client/login", "POST", False, response_time, "No token in response")
            else:
                self.log_test("/v1/client/login", "POST", False, response_time, f"Status: {response.status_code}")
                
        except Exception as e:
            response_time = time.time() - start_time
            self.log_test("/v1/client/login", "POST", False, response_time, f"Error: {str(e)}")
            
        return False

    def test_health_endpoints(self):
        """Test health and status endpoints"""
        print("\n[HEALTH] Testing Health Endpoints...")
        
        endpoints = [
            ("/", "GET"),
            ("/health", "GET"),
            ("/health/detailed", "GET")
        ]
        
        for endpoint, method in endpoints:
            start_time = time.time()
            try:
                response = self.session.get(f"{BASE_URL}{endpoint}", timeout=10)
                response_time = time.time() - start_time
                
                success = response.status_code == 200
                details = f"Status: {response.status_code}"
                if success and response.headers.get('content-type', '').startswith('application/json'):
                    try:
                        data = response.json()
                        if 'status' in data:
                            details += f", Status: {data['status']}"
                    except:
                        pass
                        
                self.log_test(endpoint, method, success, response_time, details)
                
            except Exception as e:
                response_time = time.time() - start_time
                self.log_test(endpoint, method, False, response_time, f"Error: {str(e)}")

    def test_job_endpoints(self):
        """Test job management endpoints"""
        print("\n[JOBS] Testing Job Management...")
        
        if not self.token:
            print("[ERROR] Skipping job tests - no authentication token")
            return
            
        # Test GET /v1/jobs
        start_time = time.time()
        try:
            response = self.session.get(f"{BASE_URL}/v1/jobs", timeout=10)
            response_time = time.time() - start_time
            
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            if success:
                try:
                    jobs = response.json()
                    details += f", Found {len(jobs)} jobs"
                except:
                    details += ", Invalid JSON response"
                    success = False
                    
            self.log_test("/v1/jobs", "GET", success, response_time, details)
            
        except Exception as e:
            response_time = time.time() - start_time
            self.log_test("/v1/jobs", "GET", False, response_time, f"Error: {str(e)}")

        # Test POST /v1/jobs (Create new job)
        job_data = {
            "title": "Test Software Engineer",
            "department": "Engineering",
            "location": "Remote",
            "experience_level": "Mid-level",
            "requirements": "Python, FastAPI, PostgreSQL",
            "description": "Test job posting from client portal",
            "employment_type": "Full-time",
            "client_id": "TECH001"
        }
        
        start_time = time.time()
        try:
            response = self.session.post(
                f"{BASE_URL}/v1/jobs",
                json=job_data,
                timeout=10
            )
            response_time = time.time() - start_time
            
            success = response.status_code in [200, 201]
            details = f"Status: {response.status_code}"
            if success:
                try:
                    result = response.json()
                    if 'id' in result:
                        details += f", Job ID: {result['id']}"
                except:
                    pass
                    
            self.log_test("/v1/jobs", "POST", success, response_time, details)
            
        except Exception as e:
            response_time = time.time() - start_time
            self.log_test("/v1/jobs", "POST", False, response_time, f"Error: {str(e)}")

    def test_candidate_endpoints(self):
        """Test candidate-related endpoints"""
        print("\n[CANDIDATES] Testing Candidate Operations...")
        
        if not self.token:
            print("[ERROR] Skipping candidate tests - no authentication token")
            return
            
        endpoints = [
            ("/v1/candidates", "GET"),
            ("/v1/candidates/search?skills=Python", "GET"),
            ("/v1/candidates/stats", "GET")
        ]
        
        for endpoint, method in endpoints:
            start_time = time.time()
            try:
                response = self.session.get(f"{BASE_URL}{endpoint}", timeout=10)
                response_time = time.time() - start_time
                
                success = response.status_code == 200
                details = f"Status: {response.status_code}"
                if success:
                    try:
                        data = response.json()
                        if isinstance(data, list):
                            details += f", Found {len(data)} items"
                        elif isinstance(data, dict) and 'total_candidates' in data:
                            details += f", Total: {data['total_candidates']}"
                    except:
                        pass
                        
                self.log_test(endpoint, method, success, response_time, details)
                
            except Exception as e:
                response_time = time.time() - start_time
                self.log_test(endpoint, method, False, response_time, f"Error: {str(e)}")

    def test_matching_endpoints(self):
        """Test AI matching endpoints"""
        print("\n[AI] Testing AI Matching...")
        
        if not self.token:
            print("[ERROR] Skipping matching tests - no authentication token")
            return
            
        # Test matching for job ID 1 (assuming it exists)
        start_time = time.time()
        try:
            response = self.session.get(f"{BASE_URL}/v1/match/1/top", timeout=15)
            response_time = time.time() - start_time
            
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            if success:
                try:
                    matches = response.json()
                    if isinstance(matches, list):
                        details += f", Found {len(matches)} matches"
                        if matches and 'match_score' in matches[0]:
                            details += f", Top score: {matches[0]['match_score']}"
                except:
                    pass
                    
            self.log_test("/v1/match/1/top", "GET", success, response_time, details)
            
        except Exception as e:
            response_time = time.time() - start_time
            self.log_test("/v1/match/1/top", "GET", False, response_time, f"Error: {str(e)}")

    def test_security_endpoints(self):
        """Test security-related endpoints"""
        print("\n[SECURITY] Testing Security Features...")
        
        if not self.token:
            print("[ERROR] Skipping security tests - no authentication token")
            return
            
        endpoints = [
            ("/v1/security/rate-limit-status", "GET"),
            ("/v1/security/validate-input", "POST"),
            ("/v1/security/headers-test", "GET")
        ]
        
        for endpoint, method in endpoints:
            start_time = time.time()
            try:
                if method == "GET":
                    response = self.session.get(f"{BASE_URL}{endpoint}", timeout=10)
                else:
                    # For POST endpoints, send test data
                    test_data = {"input": "test input"}
                    response = self.session.post(f"{BASE_URL}{endpoint}", json=test_data, timeout=10)
                    
                response_time = time.time() - start_time
                
                success = response.status_code == 200
                details = f"Status: {response.status_code}"
                
                self.log_test(endpoint, method, success, response_time, details)
                
            except Exception as e:
                response_time = time.time() - start_time
                self.log_test(endpoint, method, False, response_time, f"Error: {str(e)}")

    def test_monitoring_endpoints(self):
        """Test monitoring and metrics endpoints"""
        print("\n[MONITORING] Testing Monitoring...")
        
        endpoints = [
            ("/metrics", "GET"),
            ("/metrics/dashboard", "GET")
        ]
        
        for endpoint, method in endpoints:
            start_time = time.time()
            try:
                response = self.session.get(f"{BASE_URL}{endpoint}", timeout=10)
                response_time = time.time() - start_time
                
                success = response.status_code == 200
                details = f"Status: {response.status_code}"
                
                self.log_test(endpoint, method, success, response_time, details)
                
            except Exception as e:
                response_time = time.time() - start_time
                self.log_test(endpoint, method, False, response_time, f"Error: {str(e)}")

    def run_all_tests(self):
        """Run complete test suite"""
        print("Starting Client Portal Endpoint Tests...")
        print(f"Target: {BASE_URL}")
        print(f"Client: {CLIENT_CREDENTIALS['client_id']}")
        print("=" * 60)
        
        # Run tests in order
        auth_success = self.test_client_authentication()
        self.test_health_endpoints()
        self.test_job_endpoints()
        self.test_candidate_endpoints()
        self.test_matching_endpoints()
        self.test_security_endpoints()
        self.test_monitoring_endpoints()
        
        # Print summary
        self.print_summary()
        
    def print_summary(self):
        """Print test results summary"""
        print("\n" + "=" * 60)
        print("TEST RESULTS SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for r in self.test_results if "✅ PASS" in r['status'])
        failed = sum(1 for r in self.test_results if "❌ FAIL" in r['status'])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Success Rate: {(passed/total*100):.1f}%")
        
        if failed > 0:
            print("\nFAILED TESTS:")
            for result in self.test_results:
                if "FAIL" in result['status']:
                    print(f"  - {result['method']} {result['endpoint']} - {result['details']}")
        
        print("\nPASSED TESTS:")
        for result in self.test_results:
            if "PASS" in result['status']:
                print(f"  - {result['method']} {result['endpoint']} ({result['response_time']})")

if __name__ == "__main__":
    tester = ClientPortalTester()
    tester.run_all_tests()