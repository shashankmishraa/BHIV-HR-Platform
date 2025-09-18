#!/usr/bin/env python3
"""
Quick Test Script for BHIV HR Platform - Local Development
Verifies local Docker setup is running properly
"""

import requests
import json
import time
import sys
from typing import Dict, List, Any

# Local Configuration
BASE_URLS = {
    'gateway': 'http://localhost:8000',
    'agent': 'http://localhost:9000',
    'portal': 'http://localhost:8501',
    'client_portal': 'http://localhost:8502'
}

API_KEY = "myverysecureapikey123"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

class LocalTester:
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
    
    def test(self, name: str, url: str, method: str = 'GET', headers: Dict = None, data: Dict = None) -> bool:
        """Execute a test and record results"""
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=5)
            elif method == 'POST':
                response = requests.post(url, headers=headers, json=data, timeout=5)
            
            success = response.status_code in [200, 201]
            status = "✅ PASS" if success else f"❌ FAIL ({response.status_code})"
            
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
            print(f"❌ ERROR | {name}: {str(e)}")
            return False
    
    def run_local_tests(self):
        """Run local development test suite"""
        print("BHIV HR Platform - Local Development Test")
        print("=" * 50)
        
        # 1. Service Health Checks
        print("\nService Health:")
        self.test("Gateway Health", f"{BASE_URLS['gateway']}/health")
        self.test("Agent Health", f"{BASE_URLS['agent']}/health")
        self.test("Portal Accessibility", f"{BASE_URLS['portal']}")
        self.test("Client Portal Accessibility", f"{BASE_URLS['client_portal']}")
        
        # 2. Core API
        print("\nCore API:")
        self.test("API Root", f"{BASE_URLS['gateway']}/")
        self.test("Test Candidates", f"{BASE_URLS['gateway']}/test-candidates")
        
        # 3. Authenticated Endpoints
        print("\nAuthentication:")
        self.test("Jobs API", f"{BASE_URLS['gateway']}/v1/jobs", headers=HEADERS)
        self.test("Candidates API", f"{BASE_URLS['gateway']}/v1/candidates/search", headers=HEADERS)
        
        # 4. AI Agent
        print("\nAI Agent:")
        self.test("Agent Status", f"{BASE_URLS['agent']}/status")
        self.test("Agent Metrics", f"{BASE_URLS['agent']}/metrics")
        
        # 5. Database
        print("\nDatabase:")
        self.test("DB Health", f"{BASE_URLS['gateway']}/v1/database/health", headers=HEADERS)
        
        # 6. Monitoring
        print("\nMonitoring:")
        self.test("Metrics", f"{BASE_URLS['gateway']}/metrics")
        self.test("Health Detailed", f"{BASE_URLS['gateway']}/health/detailed")
        
        # Print Summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 50)
        print("LOCAL TEST SUMMARY")
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
        
        print("\nLocal Setup:", "READY" if self.failed < 3 else "ISSUES")

def main():
    """Main test execution"""
    tester = LocalTester()
    tester.run_local_tests()
    
    if tester.failed > 3:
        sys.exit(1)
    else:
        print("\nLocal development environment ready!")
        sys.exit(0)

if __name__ == "__main__":
    main()