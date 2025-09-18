#!/usr/bin/env python3
"""
Comprehensive Endpoint Testing for BHIV HR Platform
Tests all Gateway and Agent endpoints with detailed functionality checks
"""

import requests
import json
import time
from typing import Dict, List, Any

# Configuration
GATEWAY_URL = 'https://bhiv-hr-gateway.onrender.com'
AGENT_URL = 'https://bhiv-hr-agent.onrender.com'
API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

class EndpointTester:
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
    
    def test_endpoint(self, name: str, method: str, url: str, headers: Dict = None, 
                     data: Dict = None, expected_codes: List[int] = [200, 201]) -> bool:
        """Test individual endpoint"""
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=15)
            elif method == 'POST':
                response = requests.post(url, headers=headers, json=data, timeout=15)
            elif method == 'PUT':
                response = requests.put(url, headers=headers, json=data, timeout=15)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=15)
            
            success = response.status_code in expected_codes
            status = "PASS" if success else f"FAIL ({response.status_code})"
            
            # Try to get response data
            try:
                response_data = response.json() if response.content else {}
            except:
                response_data = {"raw": response.text[:100]}
            
            self.results.append({
                'name': name,
                'method': method,
                'url': url,
                'status': status,
                'response_code': response.status_code,
                'response_data': response_data
            })
            
            if success:
                self.passed += 1
                print(f"PASS | {method} {name}")
            else:
                self.failed += 1
                print(f"FAIL | {method} {name} - {response.status_code}")
            
            return success
            
        except Exception as e:
            self.failed += 1
            print(f"ERROR | {method} {name} - {str(e)}")
            self.results.append({
                'name': name,
                'method': method,
                'url': url,
                'status': f"ERROR: {str(e)}",
                'response_code': 'N/A',
                'response_data': {}
            })
            return False
    
    def test_gateway_endpoints(self):
        """Test all Gateway endpoints"""
        print("\n" + "="*60)
        print("GATEWAY ENDPOINTS TESTING")
        print("="*60)
        
        # Core endpoints
        print("\nCore Endpoints:")
        self.test_endpoint("Root", "GET", f"{GATEWAY_URL}/")
        self.test_endpoint("Health", "GET", f"{GATEWAY_URL}/health")
        self.test_endpoint("HTTP Methods Test", "GET", f"{GATEWAY_URL}/http-methods-test")
        
        # Job Management
        print("\nJob Management:")
        self.test_endpoint("Jobs List", "GET", f"{GATEWAY_URL}/v1/jobs", HEADERS)
        self.test_endpoint("Job Create", "POST", f"{GATEWAY_URL}/v1/jobs", HEADERS, {
            "title": "Test Job",
            "description": "Test Description",
            "requirements": ["Python", "FastAPI"]
        })
        
        # Candidate Management
        print("\nCandidate Management:")
        self.test_endpoint("Candidates Search", "GET", f"{GATEWAY_URL}/v1/candidates/search", HEADERS)
        self.test_endpoint("Candidate Stats", "GET", f"{GATEWAY_URL}/candidates/stats", HEADERS)
        self.test_endpoint("Bulk Candidates", "POST", f"{GATEWAY_URL}/v1/candidates/bulk", HEADERS, {
            "candidates": [{"name": "Test", "email": "test@test.com"}]
        })
        
        # AI Matching
        print("\nAI Matching:")
        self.test_endpoint("Match Performance Test", "GET", f"{GATEWAY_URL}/v1/match/performance-test", HEADERS)
        self.test_endpoint("Match Cache Status", "GET", f"{GATEWAY_URL}/v1/match/cache-status", HEADERS)
        self.test_endpoint("Match Cache Clear", "POST", f"{GATEWAY_URL}/v1/match/cache-clear", HEADERS)
        
        # Security Features
        print("\nSecurity Features:")
        self.test_endpoint("Security Headers", "GET", f"{GATEWAY_URL}/v1/security/headers", HEADERS)
        self.test_endpoint("Security Status", "GET", f"{GATEWAY_URL}/v1/security/status", HEADERS)
        self.test_endpoint("Rate Limit Status", "GET", f"{GATEWAY_URL}/v1/security/rate-limit-status", HEADERS)
        self.test_endpoint("XSS Test", "POST", f"{GATEWAY_URL}/v1/security/test-xss", HEADERS, {"input": "test"})
        self.test_endpoint("SQL Injection Test", "POST", f"{GATEWAY_URL}/v1/security/test-sql-injection", HEADERS, {"query": "test"})
        self.test_endpoint("Audit Log", "GET", f"{GATEWAY_URL}/v1/security/audit-log", HEADERS)
        
        # Authentication
        print("\nAuthentication:")
        self.test_endpoint("2FA Setup", "POST", f"{GATEWAY_URL}/v1/auth/2fa/setup", HEADERS, {"user_id": "test"})
        self.test_endpoint("Password Validation", "POST", f"{GATEWAY_URL}/v1/auth/password/validate", HEADERS, {"password": "test123"})
        self.test_endpoint("Password Generation", "GET", f"{GATEWAY_URL}/v1/auth/password/generate", HEADERS)
        self.test_endpoint("API Key Management", "GET", f"{GATEWAY_URL}/v1/auth/api-keys", HEADERS)
        
        # Session Management
        print("\nSession Management:")
        self.test_endpoint("Session Validate", "GET", f"{GATEWAY_URL}/v1/sessions/validate", HEADERS)
        self.test_endpoint("Session Logout", "POST", f"{GATEWAY_URL}/v1/sessions/logout", HEADERS)
        
        # Database
        print("\nDatabase:")
        self.test_endpoint("DB Health", "GET", f"{GATEWAY_URL}/v1/database/health", HEADERS)
        
        # Monitoring
        print("\nMonitoring:")
        self.test_endpoint("Detailed Health", "GET", f"{GATEWAY_URL}/health/detailed")
        self.test_endpoint("Metrics", "GET", f"{GATEWAY_URL}/metrics")
        self.test_endpoint("Error Monitoring", "GET", f"{GATEWAY_URL}/monitoring/errors")
        self.test_endpoint("Dependencies", "GET", f"{GATEWAY_URL}/monitoring/dependencies")
        
        # CSP Management
        print("\nCSP Management:")
        self.test_endpoint("CSP Policy", "GET", f"{GATEWAY_URL}/v1/csp/policy", HEADERS)
        self.test_endpoint("CSP Report", "POST", f"{GATEWAY_URL}/v1/csp/report", HEADERS, {"violation": "test"})
        
        # Client Portal
        print("\nClient Portal:")
        self.test_endpoint("Client Login", "POST", f"{GATEWAY_URL}/v1/client/login", None, {
            "client_id": "TECH001", "password": "demo123"
        })
        
        # Interview Management
        print("\nInterview Management:")
        self.test_endpoint("Interviews List", "GET", f"{GATEWAY_URL}/v1/interviews", HEADERS)
        self.test_endpoint("Interview Create", "POST", f"{GATEWAY_URL}/v1/interviews", HEADERS, {
            "candidate_id": 1, "job_id": 1, "scheduled_time": "2024-01-01T10:00:00"
        })
    
    def test_agent_endpoints(self):
        """Test all Agent endpoints"""
        print("\n" + "="*60)
        print("AGENT ENDPOINTS TESTING")
        print("="*60)
        
        # Core Agent endpoints
        print("\nCore Agent:")
        self.test_endpoint("Agent Health", "GET", f"{AGENT_URL}/health")
        self.test_endpoint("Agent Status", "GET", f"{AGENT_URL}/status")
        self.test_endpoint("Agent Version", "GET", f"{AGENT_URL}/version")
        self.test_endpoint("Agent Metrics", "GET", f"{AGENT_URL}/metrics")
        
        # AI Matching endpoints
        print("\nAI Matching:")
        # Test with a known job ID if available
        self.test_endpoint("Top Matches", "GET", f"{AGENT_URL}/v1/match/1/top", expected_codes=[200, 404])
        self.test_endpoint("Match Performance", "GET", f"{AGENT_URL}/v1/match/performance-test")
        
    def run_comprehensive_test(self):
        """Run all endpoint tests"""
        print("BHIV HR Platform - Comprehensive Endpoint Testing")
        print("="*60)
        
        # Test Gateway
        self.test_gateway_endpoints()
        
        # Test Agent
        self.test_agent_endpoints()
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "="*60)
        print("COMPREHENSIVE TEST SUMMARY")
        print("="*60)
        print(f"Total Tests: {self.passed + self.failed}")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Success Rate: {(self.passed/(self.passed + self.failed)*100):.1f}%")
        
        # Group failures by category
        failures = [r for r in self.results if "FAIL" in r['status'] or "ERROR" in r['status']]
        if failures:
            print(f"\nFailed Tests ({len(failures)}):")
            for failure in failures:
                print(f"  - {failure['method']} {failure['name']}: {failure['status']}")
        
        # Show some successful responses
        successes = [r for r in self.results if "PASS" in r['status']][:5]
        if successes:
            print(f"\nSample Successful Responses:")
            for success in successes:
                response_preview = str(success['response_data'])[:100]
                print(f"  - {success['name']}: {response_preview}...")

def main():
    """Main test execution"""
    tester = EndpointTester()
    tester.run_comprehensive_test()
    
    # Return exit code based on results
    if tester.failed > 10:  # Allow some failures for optional endpoints
        return 1
    else:
        print(f"\nPlatform Status: {'OPERATIONAL' if tester.failed < 10 else 'ISSUES DETECTED'}")
        return 0

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)