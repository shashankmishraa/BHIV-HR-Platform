"""Live Endpoint Testing for BHIV HR Platform"""

import asyncio
import time
import requests
from typing import Dict, List

# Production URLs
GATEWAY_URL = "https://bhiv-hr-gateway-46pz.onrender.com"
AGENT_URL = "https://bhiv-hr-agent-m1me.onrender.com"
PORTAL_URL = "https://bhiv-hr-portal-cead.onrender.com"
CLIENT_PORTAL_URL = "https://bhiv-hr-client-portal-5g33.onrender.com"

import os
API_KEY = os.getenv('PROD_API_KEY', 'prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o')

class LiveEndpointTester:
    def __init__(self):
        self.results = []
        self.headers = {"Authorization": f"Bearer {API_KEY}"}
    
    def test_endpoint(self, url: str, method: str = "GET", data: dict = None, auth: bool = True) -> Dict:
        """Test a single endpoint"""
        try:
            start_time = time.time()
            headers = self.headers if auth else {}
            
            if method == "GET":
                response = requests.get(url, headers=headers, timeout=10)
            elif method == "POST":
                response = requests.post(url, json=data, headers=headers, timeout=10)
            
            duration = time.time() - start_time
            
            return {
                "url": url,
                "method": method,
                "status_code": response.status_code,
                "success": response.status_code < 400,
                "response_time": round(duration * 1000, 2),
                "error": None
            }
        except Exception as e:
            return {
                "url": url,
                "method": method,
                "status_code": 0,
                "success": False,
                "response_time": 0,
                "error": str(e)
            }
    
    def test_health_endpoints(self):
        """Test all health endpoints"""
        print("🔍 Testing Health Endpoints...")
        
        endpoints = [
            f"{GATEWAY_URL}/health",
            f"{GATEWAY_URL}/health/detailed",
            f"{GATEWAY_URL}/health/ready",
            f"{GATEWAY_URL}/health/live",
            f"{GATEWAY_URL}/health/probe",
            f"{AGENT_URL}/health",
            f"{AGENT_URL}/status"
        ]
        
        for endpoint in endpoints:
            result = self.test_endpoint(endpoint, auth=False)
            self.results.append(result)
            status = "✅" if result["success"] else "❌"
            print(f"  {status} {endpoint} ({result['response_time']}ms)")
    
    def test_api_endpoints(self):
        """Test API endpoints with authentication"""
        print("\n🔐 Testing API Endpoints...")
        
        endpoints = [
            f"{GATEWAY_URL}/candidates",
            f"{GATEWAY_URL}/jobs",
            f"{GATEWAY_URL}/candidates/stats",
            f"{GATEWAY_URL}/jobs/stats",
            f"{AGENT_URL}/match/candidates",
            f"{AGENT_URL}/analytics/performance"
        ]
        
        for endpoint in endpoints:
            result = self.test_endpoint(endpoint, auth=True)
            self.results.append(result)
            status = "✅" if result["success"] else "❌"
            print(f"  {status} {endpoint} ({result['response_time']}ms)")
    
    def test_system_endpoints(self):
        """Test system information endpoints"""
        print("\n📊 Testing System Endpoints...")
        
        endpoints = [
            f"{GATEWAY_URL}/",
            f"{GATEWAY_URL}/system/modules",
            f"{GATEWAY_URL}/system/architecture",
            f"{GATEWAY_URL}/metrics",
            f"{GATEWAY_URL}/metrics/json",
            f"{AGENT_URL}/metrics"
        ]
        
        for endpoint in endpoints:
            result = self.test_endpoint(endpoint, auth=False)
            self.results.append(result)
            status = "✅" if result["success"] else "❌"
            print(f"  {status} {endpoint} ({result['response_time']}ms)")
    
    def test_integration_endpoints(self):
        """Test integration utility endpoints"""
        print("\n🔗 Testing Integration Endpoints...")
        
        endpoints = [
            f"{GATEWAY_URL}/integration/status",
            f"{GATEWAY_URL}/integration/endpoints",
            f"{GATEWAY_URL}/integration/test-sequence",
            f"{GATEWAY_URL}/integration/module-info",
            f"{GATEWAY_URL}/integration/health-summary"
        ]
        
        for endpoint in endpoints:
            result = self.test_endpoint(endpoint, auth=False)
            self.results.append(result)
            status = "✅" if result["success"] else "❌"
            print(f"  {status} {endpoint} ({result['response_time']}ms)")
    
    def test_portal_accessibility(self):
        """Test portal accessibility"""
        print("\n🌐 Testing Portal Accessibility...")
        
        portals = [
            ("HR Portal", PORTAL_URL),
            ("Client Portal", CLIENT_PORTAL_URL)
        ]
        
        for name, url in portals:
            result = self.test_endpoint(url, auth=False)
            self.results.append(result)
            status = "✅" if result["success"] else "❌"
            print(f"  {status} {name}: {url} ({result['response_time']}ms)")
    
    def generate_report(self):
        """Generate test report"""
        print("\n" + "="*60)
        print("📋 COMPREHENSIVE ENDPOINT TEST REPORT")
        print("="*60)
        
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results if r["success"])
        failed_tests = total_tests - successful_tests
        
        print(f"Total Endpoints Tested: {total_tests}")
        print(f"Successful: {successful_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(successful_tests/total_tests*100):.1f}%")
        
        # Performance summary
        response_times = [r["response_time"] for r in self.results if r["success"]]
        if response_times:
            avg_response = sum(response_times) / len(response_times)
            print(f"Average Response Time: {avg_response:.2f}ms")
        
        # Failed endpoints
        if failed_tests > 0:
            print(f"\n❌ Failed Endpoints ({failed_tests}):")
            for result in self.results:
                if not result["success"]:
                    print(f"  - {result['url']} (Status: {result['status_code']}, Error: {result['error']})")
        
        print("\n🎉 Test completed!")
        return successful_tests == total_tests

def main():
    """Run comprehensive endpoint tests"""
    tester = LiveEndpointTester()
    
    print("🚀 BHIV HR Platform - Live Endpoint Testing")
    print("=" * 50)
    
    # Run all test suites
    tester.test_health_endpoints()
    tester.test_api_endpoints()
    tester.test_system_endpoints()
    tester.test_integration_endpoints()
    tester.test_portal_accessibility()
    
    # Generate final report
    success = tester.generate_report()
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())