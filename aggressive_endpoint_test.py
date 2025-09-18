#!/usr/bin/env python3
"""
Aggressive Endpoint Testing - Deep validation of all endpoints
"""

import requests
import json
import time
from typing import Dict, List, Any

GATEWAY_URL = 'https://bhiv-hr-gateway.onrender.com'
AGENT_URL = 'https://bhiv-hr-agent.onrender.com'
API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

class AggressiveTester:
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
    
    def test_endpoint_aggressive(self, name: str, method: str, url: str, test_cases: List[Dict]) -> None:
        """Test endpoint with multiple scenarios"""
        print(f"\nTesting {name}:")
        for i, case in enumerate(test_cases):
            try:
                if method == 'GET':
                    response = requests.get(url, headers=case.get('headers'), params=case.get('params'), timeout=10)
                elif method == 'POST':
                    response = requests.post(url, headers=case.get('headers'), json=case.get('data'), timeout=10)
                elif method == 'PUT':
                    response = requests.put(url, headers=case.get('headers'), json=case.get('data'), timeout=10)
                elif method == 'DELETE':
                    response = requests.delete(url, headers=case.get('headers'), timeout=10)
                
                expected = case.get('expected_codes', [200, 201])
                success = response.status_code in expected
                
                if success:
                    self.passed += 1
                    print(f"  PASS | Case {i+1}: {case.get('description', 'Test')} ({response.status_code})")
                else:
                    self.failed += 1
                    print(f"  FAIL | Case {i+1}: {case.get('description', 'Test')} ({response.status_code})")
                
                # Validate response structure if specified
                if success and case.get('validate_response'):
                    try:
                        data = response.json()
                        required_fields = case.get('required_fields', [])
                        for field in required_fields:
                            if field not in data:
                                print(f"    WARN | Missing field: {field}")
                    except:
                        pass
                        
            except Exception as e:
                self.failed += 1
                print(f"  ERROR | Case {i+1}: {str(e)}")
    
    def run_aggressive_tests(self):
        """Run comprehensive aggressive tests"""
        print("BHIV HR Platform - Aggressive Endpoint Testing")
        print("="*60)
        
        # Gateway Core Endpoints
        self.test_endpoint_aggressive("Gateway Root", "GET", f"{GATEWAY_URL}/", [
            {"description": "Basic request", "expected_codes": [200]},
            {"description": "With headers", "headers": {"User-Agent": "Test"}, "expected_codes": [200]}
        ])
        
        self.test_endpoint_aggressive("Gateway Health", "GET", f"{GATEWAY_URL}/health", [
            {"description": "Health check", "expected_codes": [200], "validate_response": True, "required_fields": ["status", "service"]}
        ])
        
        # Job Management - Aggressive Testing
        self.test_endpoint_aggressive("Jobs List", "GET", f"{GATEWAY_URL}/v1/jobs", [
            {"description": "Authenticated request", "headers": HEADERS, "expected_codes": [200]},
            {"description": "No auth", "expected_codes": [401, 403]},
            {"description": "Invalid auth", "headers": {"Authorization": "Bearer invalid"}, "expected_codes": [401, 403]}
        ])
        
        self.test_endpoint_aggressive("Job Create", "POST", f"{GATEWAY_URL}/v1/jobs", [
            {"description": "Valid job", "headers": HEADERS, "data": {
                "title": "Software Engineer",
                "description": "Python developer role",
                "department": "Engineering",
                "location": "Remote",
                "experience_level": "Mid",
                "requirements": "Python, FastAPI, PostgreSQL",
                "employment_type": "Full-time"
            }, "expected_codes": [200, 201]},
            {"description": "Missing fields", "headers": HEADERS, "data": {"title": "Test"}, "expected_codes": [400, 422]},
            {"description": "No auth", "data": {"title": "Test"}, "expected_codes": [401, 403]}
        ])
        
        # Candidate Management
        self.test_endpoint_aggressive("Candidates Search", "GET", f"{GATEWAY_URL}/v1/candidates/search", [
            {"description": "Basic search", "headers": HEADERS, "expected_codes": [200]},
            {"description": "With query", "headers": HEADERS, "params": {"q": "python"}, "expected_codes": [200]},
            {"description": "No auth", "expected_codes": [401, 403]}
        ])
        
        self.test_endpoint_aggressive("Bulk Candidates", "POST", f"{GATEWAY_URL}/v1/candidates/bulk", [
            {"description": "Valid candidates", "headers": HEADERS, "data": {
                "candidates": [
                    {"name": "John Doe", "email": "john@test.com", "skills": ["Python", "React"]},
                    {"name": "Jane Smith", "email": "jane@test.com", "skills": ["Java", "Spring"]}
                ]
            }, "expected_codes": [200, 201]},
            {"description": "Empty list", "headers": HEADERS, "data": {"candidates": []}, "expected_codes": [400, 422]},
            {"description": "Invalid format", "headers": HEADERS, "data": {"candidates": "invalid"}, "expected_codes": [400, 422]}
        ])
        
        # AI Matching
        self.test_endpoint_aggressive("Match Performance", "GET", f"{GATEWAY_URL}/v1/match/performance-test", [
            {"description": "Performance test", "headers": HEADERS, "expected_codes": [200]}
        ])
        
        self.test_endpoint_aggressive("Match Cache", "GET", f"{GATEWAY_URL}/v1/match/cache-status", [
            {"description": "Cache status", "headers": HEADERS, "expected_codes": [200]}
        ])
        
        # Security Testing
        self.test_endpoint_aggressive("Security Headers", "GET", f"{GATEWAY_URL}/v1/security/headers", [
            {"description": "Security headers", "headers": HEADERS, "expected_codes": [200]}
        ])
        
        self.test_endpoint_aggressive("XSS Test", "POST", f"{GATEWAY_URL}/v1/security/test-xss", [
            {"description": "Safe input", "headers": HEADERS, "data": {"input_data": "safe text"}, "expected_codes": [200]},
            {"description": "XSS attempt", "headers": HEADERS, "data": {"input_data": "<script>alert('xss')</script>"}, "expected_codes": [200, 400]},
            {"description": "Missing input", "headers": HEADERS, "data": {}, "expected_codes": [400, 422]}
        ])
        
        self.test_endpoint_aggressive("SQL Injection Test", "POST", f"{GATEWAY_URL}/v1/security/test-sql-injection", [
            {"description": "Safe query", "headers": HEADERS, "data": {"input_data": "SELECT * FROM users"}, "expected_codes": [200]},
            {"description": "SQL injection", "headers": HEADERS, "data": {"input_data": "'; DROP TABLE users; --"}, "expected_codes": [200, 400]},
            {"description": "Missing query", "headers": HEADERS, "data": {}, "expected_codes": [400, 422]}
        ])
        
        # Authentication
        self.test_endpoint_aggressive("2FA Setup", "POST", f"{GATEWAY_URL}/v1/auth/2fa/setup", [
            {"description": "Valid user", "headers": HEADERS, "data": {"user_id": "test_user"}, "expected_codes": [200, 201]},
            {"description": "Missing user_id", "headers": HEADERS, "data": {}, "expected_codes": [400, 422]}
        ])
        
        # Session Management
        self.test_endpoint_aggressive("Session Create", "POST", f"{GATEWAY_URL}/v1/sessions/create", [
            {"description": "Valid credentials", "headers": HEADERS, "data": {"username": "test", "password": "test123"}, "expected_codes": [200, 201, 400, 422]},
            {"description": "Invalid credentials", "headers": HEADERS, "data": {"username": "invalid", "password": "wrong"}, "expected_codes": [401, 400, 422]}
        ])
        
        # Database
        self.test_endpoint_aggressive("Database Health", "GET", f"{GATEWAY_URL}/v1/database/health", [
            {"description": "DB health check", "headers": HEADERS, "expected_codes": [200]}
        ])
        
        # Monitoring
        self.test_endpoint_aggressive("Detailed Health", "GET", f"{GATEWAY_URL}/health/detailed", [
            {"description": "Detailed health", "expected_codes": [200]}
        ])
        
        self.test_endpoint_aggressive("Metrics", "GET", f"{GATEWAY_URL}/metrics", [
            {"description": "Prometheus metrics", "expected_codes": [200]}
        ])
        
        # Client Portal
        self.test_endpoint_aggressive("Client Login", "POST", f"{GATEWAY_URL}/v1/client/login", [
            {"description": "Valid client", "data": {"client_id": "TECH001", "password": "demo123"}, "expected_codes": [200]},
            {"description": "Invalid client", "data": {"client_id": "INVALID", "password": "wrong"}, "expected_codes": [401, 400]}
        ])
        
        # Interview Management
        self.test_endpoint_aggressive("Interviews List", "GET", f"{GATEWAY_URL}/v1/interviews", [
            {"description": "List interviews", "headers": HEADERS, "expected_codes": [200]}
        ])
        
        self.test_endpoint_aggressive("Interview Create", "POST", f"{GATEWAY_URL}/v1/interviews", [
            {"description": "Valid interview", "headers": HEADERS, "data": {
                "candidate_id": 1,
                "job_id": 1,
                "scheduled_time": "2024-12-01T10:00:00",
                "interviewer": "John Doe",
                "type": "technical"
            }, "expected_codes": [200, 201]},
            {"description": "Missing fields", "headers": HEADERS, "data": {"candidate_id": 1}, "expected_codes": [400, 422]}
        ])
        
        # Agent Endpoints
        self.test_endpoint_aggressive("Agent Health", "GET", f"{AGENT_URL}/health", [
            {"description": "Agent health", "expected_codes": [200]}
        ])
        
        self.test_endpoint_aggressive("Agent Status", "GET", f"{AGENT_URL}/status", [
            {"description": "Agent status", "expected_codes": [200]}
        ])
        
        self.test_endpoint_aggressive("Agent Metrics", "GET", f"{AGENT_URL}/metrics", [
            {"description": "Agent metrics", "expected_codes": [200]}
        ])
        
        # Print Results
        self.print_results()
    
    def print_results(self):
        """Print test results"""
        print("\n" + "="*60)
        print("AGGRESSIVE TEST RESULTS")
        print("="*60)
        total = self.passed + self.failed
        print(f"Total Test Cases: {total}")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Success Rate: {(self.passed/total*100):.1f}%")
        
        if self.failed < 10:
            print("Status: EXCELLENT - Platform highly robust")
        elif self.failed < 20:
            print("Status: GOOD - Minor issues detected")
        else:
            print("Status: NEEDS ATTENTION - Multiple issues found")

def main():
    tester = AggressiveTester()
    tester.run_aggressive_tests()

if __name__ == "__main__":
    main()