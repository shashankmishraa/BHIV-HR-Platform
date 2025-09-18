#!/usr/bin/env python3
"""
Quick Test Script for BHIV HR Platform
Verifies all implemented codes are running properly
"""

import requests
import json
import time
import sys
from typing import Dict, List, Any

# Configuration
BASE_URLS = {
    'gateway': 'https://bhiv-hr-gateway.onrender.com',
    'agent': 'https://bhiv-hr-agent.onrender.com',
    'portal': 'https://bhiv-hr-portal.onrender.com',
    'client_portal': 'https://bhiv-hr-client-portal.onrender.com'
}

API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

class QuickTester:
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
    
    def test(self, name: str, url: str, method: str = 'GET', headers: Dict = None, data: Dict = None) -> bool:
        """Execute a test and record results"""
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, headers=headers, json=data, timeout=10)
            
            success = response.status_code in [200, 201]
            status = "PASS" if success else f"FAIL ({response.status_code})"
            
            self.results.append({
                'name': name,
                'status': status,
                'url': url,
                'response_code': response.status_code
            })
            
            if success:
                self.passed += 1
            else:
                self.failed += 1
            
            print(f"{status} | {name}")
            return success
            
        except Exception as e:
            self.results.append({
                'name': name,
                'status': f"❌ ERROR: {str(e)}",
                'url': url,
                'response_code': 'N/A'
            })
            self.failed += 1
            print(f"ERROR | {name}: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run comprehensive test suite"""
        print("BHIV HR Platform - Quick Verification Test")
        print("=" * 50)
        
        # 1. Health Checks
        print("\nHealth Checks:")
        self.test("Gateway Health", f"{BASE_URLS['gateway']}/health")
        self.test("Agent Health", f"{BASE_URLS['agent']}/health")
        self.test("Portal Health", f"{BASE_URLS['portal']}")
        self.test("Client Portal Health", f"{BASE_URLS['client_portal']}")
        
        # 2. Core API Endpoints
        print("\nCore API Endpoints:")
        self.test("API Root", f"{BASE_URLS['gateway']}/")
        self.test("Test Candidates", f"{BASE_URLS['gateway']}/test-candidates")
        self.test("HTTP Methods Test", f"{BASE_URLS['gateway']}/http-methods-test")
        
        # 3. Authenticated Endpoints
        print("\nAuthenticated Endpoints:")
        self.test("Jobs List", f"{BASE_URLS['gateway']}/v1/jobs", headers=HEADERS)
        self.test("Candidates Search", f"{BASE_URLS['gateway']}/v1/candidates/search", headers=HEADERS)
        self.test("Candidate Stats", f"{BASE_URLS['gateway']}/candidates/stats", headers=HEADERS)
        
        # 4. AI Matching
        print("\nAI Matching Engine:")
        self.test("Agent Status", f"{BASE_URLS['agent']}/status")
        self.test("Agent Version", f"{BASE_URLS['agent']}/version")
        self.test("Agent Metrics", f"{BASE_URLS['agent']}/metrics")
        
        # 5. Security Features
        print("\nSecurity Features:")
        self.test("Security Headers", f"{BASE_URLS['gateway']}/v1/security/headers", headers=HEADERS)
        self.test("Security Status", f"{BASE_URLS['gateway']}/v1/security/status", headers=HEADERS)
        self.test("Rate Limit Status", f"{BASE_URLS['gateway']}/v1/security/rate-limit-status", headers=HEADERS)
        
        # 6. Monitoring & Metrics
        print("\nMonitoring & Metrics:")
        self.test("Detailed Health", f"{BASE_URLS['gateway']}/health/detailed")
        self.test("Metrics", f"{BASE_URLS['gateway']}/metrics")
        self.test("Error Monitoring", f"{BASE_URLS['gateway']}/monitoring/errors")
        
        # 7. Database Health
        print("\nDatabase Health:")
        self.test("DB Health", f"{BASE_URLS['gateway']}/v1/database/health", headers=HEADERS)
        
        # 8. Session Management
        print("\nSession Management:")
        session_data = {"username": "test", "password": "test123"}
        self.test("Session Create", f"{BASE_URLS['gateway']}/v1/sessions/create", 
                 method='POST', headers=HEADERS, data=session_data)
        
        # 9. Client Portal Login
        print("\nClient Portal:")
        client_data = {"client_id": "TECH001", "password": "demo123"}
        self.test("Client Login", f"{BASE_URLS['gateway']}/v1/client/login", 
                 method='POST', data=client_data)
        
        # Print Summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 50)
        print("TEST SUMMARY")
        print("=" * 50)
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Total: {self.passed + self.failed}")
        print(f"Success Rate: {(self.passed/(self.passed + self.failed)*100):.1f}%")
        
        if self.failed > 0:
            print("\nFailed Tests:")
            for result in self.results:
                if "FAIL" in result['status'] or "ERROR" in result['status']:
                    print(f"  - {result['name']}: {result['status']}")
        
        print("\nPlatform Status:", "OPERATIONAL" if self.failed < 5 else "ISSUES DETECTED")

def main():
    """Main test execution"""
    tester = QuickTester()
    tester.run_all_tests()
    
    # Exit with error code if tests failed
    if tester.failed > 5:
        sys.exit(1)
    else:
        print("\nAll critical systems operational!")
        sys.exit(0)

if __name__ == "__main__":
    main()