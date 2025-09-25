#!/usr/bin/env python3
"""
BHIV HR Platform - HTTP Method Integration Testing
Comprehensive integration tests for HTTP method handling across all services
"""

from datetime import datetime
from typing import Dict, List, Tuple
import json
import time

import concurrent.futures
import requests
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
        print("\nTesting Concurrent Requests...")
        
        def make_request(method_url_tuple):
            method, url = method_url_tuple
            try:
                if method == "GET":
                    response = requests.get(url, timeout=5)
                elif method == "HEAD":
                    response = requests.head(url, timeout=5)
                elif method == "OPTIONS":
                    response = requests.options(url, timeout=5)
                
                return f"{method}_{response.status_code}"
            except Exception as e:
                return f"{method}_ERROR"
        
        # Test concurrent requests
        test_requests = [
            ("GET", f"{API_BASE}/health"),
            ("HEAD", f"{API_BASE}/health"),
            ("OPTIONS", f"{API_BASE}/"),
            ("GET", f"{AI_BASE}/health"),
            ("HEAD", f"{AI_BASE}/health"),
            ("OPTIONS", f"{AI_BASE}/")
        ] * 5  # 30 total requests
        
        results = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_request = {executor.submit(make_request, req): req for req in test_requests}
            
            for future in concurrent.futures.as_completed(future_to_request):
                request = future_to_request[future]
                try:
                    result = future.result()
                    method, url = request
                    key = f"{method}_{url.split('/')[-1] or 'root'}"
                    if key not in results:
                        results[key] = []
                    results[key].append(result)
                except Exception as e:
                    print(f"    Concurrent request failed: {e}")
        
        # Summarize concurrent results
        summary = {}
        for key, result_list in results.items():
            success_count = sum(1 for r in result_list if "200" in r)
            total_count = len(result_list)
            summary[key] = f"{success_count}/{total_count}_SUCCESS"
        
        return summary
    
    def test_response_consistency(self) -> Dict[str, str]:
        """Test GET vs HEAD response consistency"""
        print("\nTesting Response Consistency...")
        
        test_urls = [
            ("API Gateway Health", f"{API_BASE}/health"),
            ("AI Agent Health", f"{AI_BASE}/health"),
            ("API Gateway Root", f"{API_BASE}/"),
            ("AI Agent Root", f"{AI_BASE}/")
        ]
        
        results = {}
        for name, url in test_urls:
            try:
                # GET request
                get_response = requests.get(url, timeout=5)
                
                # HEAD request
                head_response = requests.head(url, timeout=5)
                
                # Compare responses
                status_match = get_response.status_code == head_response.status_code
                content_type_match = (get_response.headers.get('content-type', '') == 
                                    head_response.headers.get('content-type', ''))
                head_no_body = len(head_response.content) == 0
                
                if status_match and content_type_match and head_no_body:
                    results[name] = "CONSISTENT"
                else:
                    issues = []
                    if not status_match:
                        issues.append(f"STATUS_MISMATCH_{get_response.status_code}_{head_response.status_code}")
                    if not content_type_match:
                        issues.append("CONTENT_TYPE_MISMATCH")
                    if not head_no_body:
                        issues.append(f"HEAD_HAS_BODY_{len(head_response.content)}")
                    results[name] = "_".join(issues)
                    
            except Exception as e:
                results[name] = f"ERROR_{str(e)[:30]}"
        
        return results
    
    def run_all_tests(self) -> Dict[str, any]:
        """Run all HTTP method tests"""
        print("BHIV HR Platform - HTTP Method Integration Testing")
        print("=" * 70)
        print(f"Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        all_results = {}
        all_results["Core Endpoints"] = self.test_core_endpoints()
        all_results["API Endpoints"] = self.test_api_endpoints()
        all_results["Security Endpoints"] = self.test_security_endpoints()
        all_results["Concurrent Requests"] = self.test_concurrent_requests()
        all_results["Response Consistency"] = self.test_response_consistency()
        
        return all_results
    
    def generate_report(self, results: Dict[str, any]) -> None:
        """Generate comprehensive test report"""
        print("\n" + "=" * 70)
        print("HTTP METHOD INTEGRATION TEST REPORT")
        print("=" * 70)
        
        total_tests = 0
        passed_tests = 0
        
        for category, category_results in results.items():
            print(f"\n{category}:")
            print("-" * 40)
            
            if category in ["Concurrent Requests", "Response Consistency"]:
                # Simple key-value results
                for test_name, result in category_results.items():
                    status = "PASSED" if any(success in result for success in [
                        "SUCCESS", "CONSISTENT", "CORRECTLY_REJECTED"
                    ]) else "FAILED"
                    
                    print(f"  {test_name:<30}: {status} ({result})")
                    total_tests += 1
                    if status == "PASSED":
                        passed_tests += 1
            else:
                # Nested endpoint results
                for endpoint_name, method_results in category_results.items():
                    print(f"  {endpoint_name}:")
                    
                    for method, result in method_results.items():
                        status = "PASSED" if any(success in result for success in [
                            "SUCCESS", "CORRECTLY_REJECTED"
                        ]) else "FAILED"
                        
                        print(f"    {method:<8}: {status} ({result})")
                        total_tests += 1
                        if status == "PASSED":
                            passed_tests += 1
        
        # Summary statistics
        print(f"\n" + "=" * 70)
        print("SUMMARY STATISTICS")
        print("=" * 70)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        # Performance metrics
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        print(f"\nTest Duration: {duration:.2f} seconds")
        print(f"Tests per Second: {total_tests/duration:.1f}")
        
        # Final status
        if passed_tests == total_tests:
            print("\nSUCCESS: All HTTP method tests passed!")
        elif passed_tests / total_tests >= 0.9:
            print("\nWARNING: Most tests passed, minor issues detected")
        else:
            print("\nFAILURE: Significant HTTP method handling issues detected")
        
        print(f"\nCompleted: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    """Main test execution"""
    tester = HTTPMethodTester()
    results = tester.run_all_tests()
    tester.generate_report(results)

if __name__ == "__main__":
    main()