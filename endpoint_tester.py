import requests
import json
import time
from typing import Dict, List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

class EndpointTester:
    def __init__(self):
        self.gateway_url = "https://bhiv-hr-gateway-901a.onrender.com"
        self.agent_url = "https://bhiv-hr-agent-o6nx.onrender.com"
        self.api_key = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
        self.headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        
        self.results = {
            "functional": [],
            "non_functional": [],
            "missing": [],
            "authentication_required": [],
            "errors": []
        }

    def test_endpoint(self, method: str, url: str, data: dict = None, auth_required: bool = True) -> Dict:
        """Test a single endpoint"""
        headers = self.headers if auth_required else {"Content-Type": "application/json"}
        
        try:
            start_time = time.time()
            
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, timeout=10)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=data, timeout=10)
            elif method.upper() == "PUT":
                response = requests.put(url, headers=headers, json=data, timeout=10)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=headers, timeout=10)
            elif method.upper() == "HEAD":
                response = requests.head(url, headers=headers, timeout=10)
            elif method.upper() == "OPTIONS":
                response = requests.options(url, headers=headers, timeout=10)
            else:
                return {"status": "unsupported_method", "method": method}
            
            response_time = time.time() - start_time
            
            return {
                "method": method.upper(),
                "url": url,
                "status_code": response.status_code,
                "response_time": round(response_time, 3),
                "success": 200 <= response.status_code < 300,
                "auth_required": auth_required,
                "response_size": len(response.content) if response.content else 0
            }
            
        except requests.exceptions.Timeout:
            return {"method": method, "url": url, "status": "timeout", "auth_required": auth_required}
        except requests.exceptions.ConnectionError:
            return {"method": method, "url": url, "status": "connection_error", "auth_required": auth_required}
        except Exception as e:
            return {"method": method, "url": url, "status": "error", "error": str(e), "auth_required": auth_required}

    def test_core_endpoints(self):
        """Test core API endpoints"""
        print("Testing Core API Endpoints...")
        
        core_tests = [
            ("GET", f"{self.gateway_url}/", False),
            ("GET", f"{self.gateway_url}/health", False),
            ("GET", f"{self.gateway_url}/health/simple", False),
            ("GET", f"{self.gateway_url}/health/detailed", False),
            ("GET", f"{self.gateway_url}/metrics", False),
            ("GET", f"{self.agent_url}/", False),
            ("GET", f"{self.agent_url}/health", False),
            ("GET", f"{self.agent_url}/status", False),
        ]
        
        for method, url, auth_req in core_tests:
            result = self.test_endpoint(method, url, auth_required=auth_req)
            self.categorize_result(result, "Core API")

    def test_authentication_endpoints(self):
        """Test authentication endpoints"""
        print("Testing Authentication Endpoints...")
        
        auth_tests = [
            ("GET", f"{self.gateway_url}/v1/auth/status", True),
            ("GET", f"{self.gateway_url}/v1/auth/test", True),
            ("GET", f"{self.gateway_url}/v1/auth/config", True),
            ("GET", f"{self.gateway_url}/v1/auth/me", False),
            ("POST", f"{self.gateway_url}/auth/login", False, {"username": "demo", "password": "demo"}),
            ("GET", f"{self.gateway_url}/v1/auth/users", True),
            ("GET", f"{self.gateway_url}/v1/auth/sessions", True),
        ]
        
        for test in auth_tests:
            method, url = test[0], test[1]
            auth_req = test[2] if len(test) > 2 else True
            data = test[3] if len(test) > 3 else None
            
            result = self.test_endpoint(method, url, data, auth_req)
            self.categorize_result(result, "Authentication")

    def test_job_management_endpoints(self):
        """Test job management endpoints"""
        print("Testing Job Management Endpoints...")
        
        job_tests = [
            ("GET", f"{self.gateway_url}/v1/jobs", True),
            ("GET", f"{self.gateway_url}/v1/jobs/search", True),
            ("GET", f"{self.gateway_url}/v1/jobs/stats", True),
            ("POST", f"{self.gateway_url}/v1/jobs", True, {
                "title": "Test Job",
                "department": "Engineering",
                "location": "Remote",
                "experience_level": "Mid",
                "requirements": "Test requirements",
                "description": "Test description"
            }),
        ]
        
        for test in job_tests:
            method, url = test[0], test[1]
            auth_req = test[2] if len(test) > 2 else True
            data = test[3] if len(test) > 3 else None
            
            result = self.test_endpoint(method, url, data, auth_req)
            self.categorize_result(result, "Job Management")

    def test_candidate_management_endpoints(self):
        """Test candidate management endpoints"""
        print("Testing Candidate Management Endpoints...")
        
        candidate_tests = [
            ("GET", f"{self.gateway_url}/v1/candidates", True),
            ("GET", f"{self.gateway_url}/v1/candidates/search", True),
            ("GET", f"{self.gateway_url}/v1/candidates/stats", True),
            ("GET", f"{self.gateway_url}/v1/candidates/export", True),
        ]
        
        for method, url, auth_req in candidate_tests:
            result = self.test_endpoint(method, url, auth_required=auth_req)
            self.categorize_result(result, "Candidate Management")

    def test_ai_matching_endpoints(self):
        """Test AI matching endpoints"""
        print("Testing AI Matching Endpoints...")
        
        ai_tests = [
            ("GET", f"{self.gateway_url}/v1/match/1/top", True),
            ("GET", f"{self.gateway_url}/v1/match/cache-status", True),
            ("GET", f"{self.gateway_url}/v1/match/history", True),
            ("GET", f"{self.gateway_url}/v1/match/analytics", True),
            ("POST", f"{self.agent_url}/match", False, {"job_id": 1}),
            ("GET", f"{self.agent_url}/analyze/1", False),
        ]
        
        for test in ai_tests:
            method, url = test[0], test[1]
            auth_req = test[2] if len(test) > 2 else True
            data = test[3] if len(test) > 3 else None
            
            result = self.test_endpoint(method, url, data, auth_req)
            self.categorize_result(result, "AI Matching")

    def test_security_endpoints(self):
        """Test security endpoints"""
        print("Testing Security Endpoints...")
        
        security_tests = [
            ("GET", f"{self.gateway_url}/v1/security/status", True),
            ("GET", f"{self.gateway_url}/v1/security/rate-limit-status", True),
            ("GET", f"{self.gateway_url}/v1/security/headers", True),
            ("GET", f"{self.gateway_url}/v1/security/audit-log", True),
            ("GET", f"{self.gateway_url}/v1/security/policy", True),
        ]
        
        for method, url, auth_req in security_tests:
            result = self.test_endpoint(method, url, auth_required=auth_req)
            self.categorize_result(result, "Security")

    def test_monitoring_endpoints(self):
        """Test monitoring endpoints"""
        print("Testing Monitoring Endpoints...")
        
        monitoring_tests = [
            ("GET", f"{self.gateway_url}/monitoring/errors", False),
            ("GET", f"{self.gateway_url}/monitoring/dependencies", False),
            ("GET", f"{self.gateway_url}/monitoring/performance", True),
            ("GET", f"{self.gateway_url}/monitoring/alerts", True),
            ("GET", f"{self.agent_url}/metrics", False),
        ]
        
        for method, url, auth_req in monitoring_tests:
            result = self.test_endpoint(method, url, auth_required=auth_req)
            self.categorize_result(result, "Monitoring")

    def categorize_result(self, result: Dict, category: str):
        """Categorize test results"""
        result["category"] = category
        
        if "status" in result and result["status"] in ["timeout", "connection_error", "error"]:
            self.results["errors"].append(result)
        elif "status_code" in result:
            if result["status_code"] == 401 or result["status_code"] == 403:
                self.results["authentication_required"].append(result)
            elif 200 <= result["status_code"] < 300:
                self.results["functional"].append(result)
            else:
                self.results["non_functional"].append(result)
        else:
            self.results["missing"].append(result)

    def run_comprehensive_test(self):
        """Run comprehensive endpoint testing"""
        print("Starting Comprehensive Endpoint Testing...\n")
        
        # Test different categories
        self.test_core_endpoints()
        self.test_authentication_endpoints()
        self.test_job_management_endpoints()
        self.test_candidate_management_endpoints()
        self.test_ai_matching_endpoints()
        self.test_security_endpoints()
        self.test_monitoring_endpoints()
        
        return self.results

    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "="*80)
        print("COMPREHENSIVE ENDPOINT TEST REPORT")
        print("="*80)
        
        # Summary
        total_tests = sum(len(results) for results in self.results.values())
        print(f"\nTOTAL ENDPOINTS TESTED: {total_tests}")
        print(f"  - Functional: {len(self.results['functional'])}")
        print(f"  - Non-Functional: {len(self.results['non_functional'])}")
        print(f"  - Authentication Required: {len(self.results['authentication_required'])}")
        print(f"  - Errors/Missing: {len(self.results['errors'])}")
        
        # Priority 1: Functional Endpoints
        print(f"\n{'='*50}")
        print("PRIORITY 1: FUNCTIONAL ENDPOINTS")
        print(f"{'='*50}")
        
        categories = {}
        for endpoint in self.results['functional']:
            cat = endpoint.get('category', 'Unknown')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(endpoint)
        
        for category, endpoints in categories.items():
            print(f"\n{category} ({len(endpoints)} endpoints):")
            for ep in endpoints[:5]:  # Show top 5
                print(f"  ✅ {ep['method']} {ep['url']} - {ep['status_code']} ({ep.get('response_time', 0)}s)")
            if len(endpoints) > 5:
                print(f"  ... and {len(endpoints) - 5} more")
        
        # Priority 2: Authentication Required
        print(f"\n{'='*50}")
        print("PRIORITY 2: AUTHENTICATION REQUIRED")
        print(f"{'='*50}")
        
        auth_categories = {}
        for endpoint in self.results['authentication_required']:
            cat = endpoint.get('category', 'Unknown')
            if cat not in auth_categories:
                auth_categories[cat] = []
            auth_categories[cat].append(endpoint)
        
        for category, endpoints in auth_categories.items():
            print(f"\n{category} ({len(endpoints)} endpoints):")
            for ep in endpoints[:3]:
                print(f"  🔐 {ep['method']} {ep['url']} - {ep['status_code']}")
        
        # Priority 3: Non-Functional
        print(f"\n{'='*50}")
        print("PRIORITY 3: NON-FUNCTIONAL ENDPOINTS")
        print(f"{'='*50}")
        
        for endpoint in self.results['non_functional'][:10]:
            print(f"  ❌ {endpoint['method']} {endpoint['url']} - {endpoint['status_code']}")
        
        # Priority 4: Errors/Missing
        print(f"\n{'='*50}")
        print("PRIORITY 4: ERRORS/MISSING ENDPOINTS")
        print(f"{'='*50}")
        
        for endpoint in self.results['errors'][:10]:
            status = endpoint.get('status', 'unknown')
            print(f"  🚫 {endpoint['method']} {endpoint['url']} - {status}")
        
        # Performance Summary
        functional_times = [ep.get('response_time', 0) for ep in self.results['functional'] if 'response_time' in ep]
        if functional_times:
            avg_time = sum(functional_times) / len(functional_times)
            print(f"\nPERFORMANCE SUMMARY:")
            print(f"  Average Response Time: {avg_time:.3f}s")
            print(f"  Fastest Response: {min(functional_times):.3f}s")
            print(f"  Slowest Response: {max(functional_times):.3f}s")

def main():
    tester = EndpointTester()
    results = tester.run_comprehensive_test()
    tester.generate_report()

if __name__ == "__main__":
    main()