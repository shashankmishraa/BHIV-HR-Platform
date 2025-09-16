#!/usr/bin/env python3
"""
BHIV HR Platform - HTTP Method Integration Testing
Comprehensive integration tests for HTTP method handling across all services
"""

import requests
import json
import time
import concurrent.futures
from datetime import datetime
from typing import Dict, List, Tuple

# Configuration
API_BASE = "http://localhost:8000"
AI_BASE = "http://localhost:9000"
API_KEY = "myverysecureapikey123"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

class HTTPMethodTester:
    """Comprehensive HTTP method testing class"""
    
    def __init__(self):
        self.results = {}
        self.start_time = datetime.now()
    
    def test_endpoint_methods(self, name: str, url: str, methods: List[str], 
                            requires_auth: bool = False) -> Dict[str, str]:
        """Test multiple HTTP methods on a single endpoint"""
        endpoint_results = {}
        headers = HEADERS if requires_auth else {}
        
        for method in methods:
            try:
                if method == "GET":
                    response = requests.get(url, headers=headers, timeout=5)
                elif method == "HEAD":
                    response = requests.head(url, headers=headers, timeout=5)
                elif method == "OPTIONS":
                    response = requests.options(url, headers=headers, timeout=5)
                elif method == "POST":
                    response = requests.post(url, headers=headers, json={}, timeout=5)
                elif method == "PUT":
                    response = requests.put(url, headers=headers, json={}, timeout=5)
                elif method == "DELETE":
                    response = requests.delete(url, headers=headers, timeout=5)
                else:
                    # Unsupported method
                    response = requests.request(method, url, headers=headers, timeout=5)
                
                # Analyze response
                if method in ["GET", "POST", "PUT", "DELETE"] and response.status_code in [200, 201, 404, 422]:
                    endpoint_results[method] = f"SUCCESS_{response.status_code}"
                elif method == "HEAD" and response.status_code == 200:
                    # Verify HEAD response has no body
                    if len(response.content) == 0:
                        endpoint_results[method] = "SUCCESS_NO_BODY"
                    else:
                        endpoint_results[method] = f"SUCCESS_WITH_BODY_{len(response.content)}"
                elif method == "OPTIONS" and response.status_code == 200:
                    # Check for proper CORS headers
                    if 'Allow' in response.headers or 'Access-Control-Allow-Methods' in response.headers:
                        endpoint_results[method] = "SUCCESS_WITH_CORS"
                    else:
                        endpoint_results[method] = "SUCCESS_NO_CORS"
                elif method not in ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"] and response.status_code == 405:
                    endpoint_results[method] = "CORRECTLY_REJECTED_405"
                else:
                    endpoint_results[method] = f"UNEXPECTED_{response.status_code}"
                    
            except Exception as e:
                endpoint_results[method] = f"ERROR_{str(e)[:50]}"
        
        return endpoint_results
    
    def test_core_endpoints(self) -> Dict[str, Dict[str, str]]:
        """Test core endpoints across both services"""
        print("Testing Core Endpoints...")
        
        core_endpoints = [
            ("API Gateway Root", f"{API_BASE}/", ["GET", "HEAD", "OPTIONS", "TRACE"], False),
            ("API Gateway Health", f"{API_BASE}/health", ["GET", "HEAD", "OPTIONS"], False),
            ("API Gateway Test Candidates", f"{API_BASE}/test-candidates", ["GET", "HEAD"], True),
            ("API Gateway HTTP Methods Test", f"{API_BASE}/http-methods-test", ["GET", "HEAD", "OPTIONS"], True),
            ("AI Agent Root", f"{AI_BASE}/", ["GET", "HEAD", "OPTIONS", "TRACE"], False),
            ("AI Agent Health", f"{AI_BASE}/health", ["GET", "HEAD", "OPTIONS"], False),
            ("AI Agent Test DB", f"{AI_BASE}/test-db", ["GET", "HEAD"], False),
            ("AI Agent HTTP Methods Test", f"{AI_BASE}/http-methods-test", ["GET", "HEAD", "OPTIONS"], False)
        ]
        
        results = {}
        for name, url, methods, requires_auth in core_endpoints:
            print(f"  Testing {name}...")
            results[name] = self.test_endpoint_methods(name, url, methods, requires_auth)
        
        return results
    
    def test_api_endpoints(self) -> Dict[str, Dict[str, str]]:
        """Test API endpoints with different methods"""
        print("\nTesting API Endpoints...")
        
        api_endpoints = [
            ("Jobs List", f"{API_BASE}/v1/jobs", ["GET", "HEAD", "POST", "PATCH"], True),
            ("Candidates Search", f"{API_BASE}/v1/candidates/search", ["GET", "HEAD", "POST"], True),
            ("Match Candidates", f"{API_BASE}/v1/match/1/top", ["GET", "HEAD", "POST"], True),
            ("Candidate Stats", f"{API_BASE}/candidates/stats", ["GET", "HEAD", "PUT"], True)
        ]
        
        results = {}
        for name, url, methods, requires_auth in api_endpoints:
            print(f"  Testing {name}...")
            results[name] = self.test_endpoint_methods(name, url, methods, requires_auth)
        
        return results
    
    def test_security_endpoints(self) -> Dict[str, Dict[str, str]]:
        """Test security-related endpoints"""
        print("\nTesting Security Endpoints...")
        
        security_endpoints = [
            ("Rate Limit Status", f"{API_BASE}/v1/security/rate-limit-status", ["GET", "HEAD", "POST"], True),
            ("Security Headers Test", f"{API_BASE}/v1/security/security-headers-test", ["GET", "HEAD"], True),
            ("2FA Setup", f"{API_BASE}/v1/2fa/setup", ["POST", "GET", "HEAD"], True),
            ("Password Validation", f"{API_BASE}/v1/password/validate", ["POST", "GET", "HEAD"], True)
        ]
        
        results = {}
        for name, url, methods, requires_auth in security_endpoints:
            print(f"  Testing {name}...")
            results[name] = self.test_endpoint_methods(name, url, methods, requires_auth)
        
        return results
    
    def test_concurrent_requests(self) -> Dict[str, str]:
        """Test concurrent HTTP method requests"""
        print(\"\\nTesting Concurrent Requests...\")
        
        def make_request(method_url_tuple):\n            method, url = method_url_tuple\n            try:\n                if method == \"GET\":\n                    response = requests.get(url, timeout=5)\n                elif method == \"HEAD\":\n                    response = requests.head(url, timeout=5)\n                elif method == \"OPTIONS\":\n                    response = requests.options(url, timeout=5)\n                \n                return f\"{method}_{response.status_code}\"\n            except Exception as e:\n                return f\"{method}_ERROR\"\n        \n        # Test concurrent requests\n        test_requests = [\n            (\"GET\", f\"{API_BASE}/health\"),\n            (\"HEAD\", f\"{API_BASE}/health\"),\n            (\"OPTIONS\", f\"{API_BASE}/\"),\n            (\"GET\", f\"{AI_BASE}/health\"),\n            (\"HEAD\", f\"{AI_BASE}/health\"),\n            (\"OPTIONS\", f\"{AI_BASE}/\")\n        ] * 5  # 30 total requests\n        \n        results = {}\n        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:\n            future_to_request = {executor.submit(make_request, req): req for req in test_requests}\n            \n            for future in concurrent.futures.as_completed(future_to_request):\n                request = future_to_request[future]\n                try:\n                    result = future.result()\n                    method, url = request\n                    key = f\"{method}_{url.split('/')[-1] or 'root'}\"\n                    if key not in results:\n                        results[key] = []\n                    results[key].append(result)\n                except Exception as e:\n                    print(f\"    Concurrent request failed: {e}\")\n        \n        # Summarize concurrent results\n        summary = {}\n        for key, result_list in results.items():\n            success_count = sum(1 for r in result_list if \"200\" in r)\n            total_count = len(result_list)\n            summary[key] = f\"{success_count}/{total_count}_SUCCESS\"\n        \n        return summary\n    \n    def test_response_consistency(self) -> Dict[str, str]:\n        \"\"\"Test GET vs HEAD response consistency\"\"\"\n        print(\"\\nTesting Response Consistency...\")\n        \n        test_urls = [\n            (\"API Gateway Health\", f\"{API_BASE}/health\"),\n            (\"AI Agent Health\", f\"{AI_BASE}/health\"),\n            (\"API Gateway Root\", f\"{API_BASE}/\"),\n            (\"AI Agent Root\", f\"{AI_BASE}/\")\n        ]\n        \n        results = {}\n        for name, url in test_urls:\n            try:\n                # GET request\n                get_response = requests.get(url, timeout=5)\n                \n                # HEAD request\n                head_response = requests.head(url, timeout=5)\n                \n                # Compare responses\n                status_match = get_response.status_code == head_response.status_code\n                content_type_match = (get_response.headers.get('content-type', '') == \n                                    head_response.headers.get('content-type', ''))\n                head_no_body = len(head_response.content) == 0\n                \n                if status_match and content_type_match and head_no_body:\n                    results[name] = \"CONSISTENT\"\n                else:\n                    issues = []\n                    if not status_match:\n                        issues.append(f\"STATUS_MISMATCH_{get_response.status_code}_{head_response.status_code}\")\n                    if not content_type_match:\n                        issues.append(\"CONTENT_TYPE_MISMATCH\")\n                    if not head_no_body:\n                        issues.append(f\"HEAD_HAS_BODY_{len(head_response.content)}\")\n                    results[name] = \"_\".join(issues)\n                    \n            except Exception as e:\n                results[name] = f\"ERROR_{str(e)[:30]}\"\n        \n        return results\n    \n    def run_all_tests(self) -> Dict[str, any]:\n        \"\"\"Run all HTTP method tests\"\"\"\n        print(\"BHIV HR Platform - HTTP Method Integration Testing\")\n        print(\"=\" * 70)\n        print(f\"Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\")\n        print()\n        \n        all_results = {}\n        all_results[\"Core Endpoints\"] = self.test_core_endpoints()\n        all_results[\"API Endpoints\"] = self.test_api_endpoints()\n        all_results[\"Security Endpoints\"] = self.test_security_endpoints()\n        all_results[\"Concurrent Requests\"] = self.test_concurrent_requests()\n        all_results[\"Response Consistency\"] = self.test_response_consistency()\n        \n        return all_results\n    \n    def generate_report(self, results: Dict[str, any]) -> None:\n        \"\"\"Generate comprehensive test report\"\"\"\n        print(\"\\n\" + \"=\" * 70)\n        print(\"HTTP METHOD INTEGRATION TEST REPORT\")\n        print(\"=\" * 70)\n        \n        total_tests = 0\n        passed_tests = 0\n        \n        for category, category_results in results.items():\n            print(f\"\\n{category}:\")\n            print(\"-\" * 40)\n            \n            if category in [\"Concurrent Requests\", \"Response Consistency\"]:\n                # Simple key-value results\n                for test_name, result in category_results.items():\n                    status = \"PASSED\" if any(success in result for success in [\n                        \"SUCCESS\", \"CONSISTENT\", \"CORRECTLY_REJECTED\"\n                    ]) else \"FAILED\"\n                    \n                    print(f\"  {test_name:<30}: {status} ({result})\")\n                    total_tests += 1\n                    if status == \"PASSED\":\n                        passed_tests += 1\n            else:\n                # Nested endpoint results\n                for endpoint_name, method_results in category_results.items():\n                    print(f\"  {endpoint_name}:\")\n                    \n                    for method, result in method_results.items():\n                        status = \"PASSED\" if any(success in result for success in [\n                            \"SUCCESS\", \"CORRECTLY_REJECTED\"\n                        ]) else \"FAILED\"\n                        \n                        print(f\"    {method:<8}: {status} ({result})\")\n                        total_tests += 1\n                        if status == \"PASSED\":\n                            passed_tests += 1\n        \n        # Summary statistics\n        print(f\"\\n\" + \"=\" * 70)\n        print(\"SUMMARY STATISTICS\")\n        print(\"=\" * 70)\n        print(f\"Total Tests: {total_tests}\")\n        print(f\"Passed: {passed_tests}\")\n        print(f\"Failed: {total_tests - passed_tests}\")\n        print(f\"Success Rate: {(passed_tests/total_tests)*100:.1f}%\")\n        \n        # Performance metrics\n        end_time = datetime.now()\n        duration = (end_time - self.start_time).total_seconds()\n        print(f\"\\nTest Duration: {duration:.2f} seconds\")\n        print(f\"Tests per Second: {total_tests/duration:.1f}\")\n        \n        # Final status\n        if passed_tests == total_tests:\n            print(\"\\n🎉 SUCCESS: All HTTP method tests passed!\")\n        elif passed_tests / total_tests >= 0.9:\n            print(\"\\n⚠️  WARNING: Most tests passed, minor issues detected\")\n        else:\n            print(\"\\n❌ FAILURE: Significant HTTP method handling issues detected\")\n        \n        print(f\"\\nCompleted: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\")\n\ndef main():\n    \"\"\"Main test execution\"\"\"\n    tester = HTTPMethodTester()\n    results = tester.run_all_tests()\n    tester.generate_report(results)\n\nif __name__ == \"__main__\":\n    main()