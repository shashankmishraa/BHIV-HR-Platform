#!/usr/bin/env python3
"""
BHIV HR Platform - HTTP Methods Testing Script
Tests HTTP method handling including HEAD, OPTIONS, and unsupported methods
"""

from datetime import datetime
import time

import requests
API_BASE = "http://localhost:8000"
AI_BASE = "http://localhost:9000"
API_KEY = "myverysecureapikey123"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def test_head_requests():
    """Test HEAD request handling"""
    print("Testing HEAD Requests...")
    
    endpoints = [
        ("API Gateway Root", f"{API_BASE}/"),
        ("API Gateway Health", f"{API_BASE}/health"),
        ("API Gateway Test Candidates", f"{API_BASE}/test-candidates"),
        ("API Gateway HTTP Methods Test", f"{API_BASE}/http-methods-test"),
        ("AI Agent Root", f"{AI_BASE}/"),
        ("AI Agent Health", f"{AI_BASE}/health"),
        ("AI Agent Test DB", f"{AI_BASE}/test-db"),
        ("AI Agent HTTP Methods Test", f"{AI_BASE}/http-methods-test")
    ]
    
    results = {}
    for name, url in endpoints:
        try:
            # Test HEAD request
            if "test-candidates" in url or "test-db" in url:
                response = requests.head(url, headers=HEADERS, timeout=5)
            else:
                response = requests.head(url, timeout=5)
            
            if response.status_code == 200:
                results[name] = "HEAD_SUCCESS"
                print(f"  {name}: HEAD SUCCESS (Status: {response.status_code})")
                
                # Verify no body content in HEAD response
                if len(response.content) == 0:
                    print(f"    + No body content (correct for HEAD)")
                else:
                    print(f"    ! Body content present: {len(response.content)} bytes")
                
                # Check important headers
                if 'content-type' in response.headers:
                    print(f"    + Content-Type: {response.headers['content-type']}")
                
            else:
                results[name] = f"HEAD_ERROR_{response.status_code}"
                print(f"  {name}: HEAD ERROR (Status: {response.status_code})")
                
        except Exception as e:
            results[name] = f"HEAD_FAILED: {str(e)}"
            print(f"  {name}: HEAD FAILED - {str(e)}")
    
    return results

def test_options_requests():
    """Test OPTIONS request handling"""
    print("\nTesting OPTIONS Requests...")
    
    endpoints = [
        ("API Gateway Root", f"{API_BASE}/"),
        ("API Gateway Health", f"{API_BASE}/health"),
        ("API Gateway HTTP Methods Test", f"{API_BASE}/http-methods-test"),
        ("AI Agent Root", f"{AI_BASE}/"),
        ("AI Agent Health", f"{AI_BASE}/health"),
        ("AI Agent HTTP Methods Test", f"{AI_BASE}/http-methods-test")
    ]
    
    results = {}
    for name, url in endpoints:
        try:
            response = requests.options(url, timeout=5)
            
            if response.status_code == 200:
                results[name] = "OPTIONS_SUCCESS"
                print(f"  {name}: OPTIONS SUCCESS (Status: {response.status_code})")
                
                # Check CORS headers
                if 'Access-Control-Allow-Methods' in response.headers:
                    methods = response.headers['Access-Control-Allow-Methods']
                    print(f"    + Allowed Methods: {methods}")
                
                if 'Allow' in response.headers:
                    allow_methods = response.headers['Allow']
                    print(f"    + Allow Header: {allow_methods}")
                
                # Verify no body content in OPTIONS response
                if len(response.content) == 0:
                    print(f"    + No body content (correct for OPTIONS)")
                
            else:
                results[name] = f"OPTIONS_ERROR_{response.status_code}"
                print(f"  {name}: OPTIONS ERROR (Status: {response.status_code})")
                
        except Exception as e:
            results[name] = f"OPTIONS_FAILED: {str(e)}"
            print(f"  {name}: OPTIONS FAILED - {str(e)}")
    
    return results

def test_unsupported_methods():
    """Test handling of unsupported HTTP methods"""
    print("\nTesting Unsupported Methods...")
    
    unsupported_methods = ["TRACE", "CONNECT", "CUSTOM"]
    endpoints = [
        ("API Gateway Root", f"{API_BASE}/"),
        ("AI Agent Root", f"{AI_BASE}/")
    ]
    
    results = {}
    for method in unsupported_methods:
        for name, url in endpoints:
            test_name = f"{name} - {method}"
            try:
                response = requests.request(method, url, timeout=5)
                
                if response.status_code == 405:
                    results[test_name] = "CORRECTLY_REJECTED"
                    print(f"  {test_name}: CORRECTLY REJECTED (405)")
                    
                    # Check Allow header
                    if 'Allow' in response.headers:
                        allow_methods = response.headers['Allow']
                        print(f"    + Allow Header: {allow_methods}")
                    
                else:
                    results[test_name] = f"UNEXPECTED_STATUS_{response.status_code}"
                    print(f"  {test_name}: UNEXPECTED STATUS {response.status_code}")
                    
            except Exception as e:
                results[test_name] = f"TEST_FAILED: {str(e)}"
                print(f"  {test_name}: TEST FAILED - {str(e)}")
    
    return results

def test_method_consistency():
    """Test that GET and HEAD return consistent headers"""
    print("\nTesting GET vs HEAD Consistency...")
    
    endpoints = [
        ("API Gateway Health", f"{API_BASE}/health"),
        ("AI Agent Health", f"{AI_BASE}/health")
    ]
    
    results = {}
    for name, url in endpoints:
        try:
            # GET request
            get_response = requests.get(url, timeout=5)
            
            # HEAD request  
            head_response = requests.head(url, timeout=5)
            
            if get_response.status_code == head_response.status_code:
                results[name] = "CONSISTENT_STATUS"
                print(f"  {name}: CONSISTENT STATUS ({get_response.status_code})")
                
                # Check Content-Type consistency
                get_ct = get_response.headers.get('content-type', '')
                head_ct = head_response.headers.get('content-type', '')
                
                if get_ct == head_ct:
                    print(f"    + Content-Type consistent: {get_ct}")
                else:
                    print(f"    ! Content-Type mismatch: GET={get_ct}, HEAD={head_ct}")
                
                # Verify HEAD has no body
                if len(head_response.content) == 0:
                    print(f"    + HEAD response has no body")
                else:
                    print(f"    ! HEAD response has body: {len(head_response.content)} bytes")
                
            else:
                results[name] = f"INCONSISTENT_STATUS_GET_{get_response.status_code}_HEAD_{head_response.status_code}"
                print(f"  {name}: INCONSISTENT STATUS - GET: {get_response.status_code}, HEAD: {head_response.status_code}")
                
        except Exception as e:
            results[name] = f"CONSISTENCY_TEST_FAILED: {str(e)}"
            print(f"  {name}: CONSISTENCY TEST FAILED - {str(e)}")
    
    return results

def test_cors_preflight():
    """Test CORS preflight requests"""
    print("\nTesting CORS Preflight...")
    
    endpoints = [
        ("API Gateway", f"{API_BASE}/"),
        ("AI Agent", f"{AI_BASE}/")
    ]
    
    results = {}
    for name, url in endpoints:
        try:
            # CORS preflight request
            headers = {
                "Origin": "https://example.com",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type, Authorization"
            }
            
            response = requests.options(url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                results[name] = "CORS_SUCCESS"
                print(f"  {name}: CORS PREFLIGHT SUCCESS")
                
                # Check CORS headers
                cors_headers = [
                    "Access-Control-Allow-Origin",
                    "Access-Control-Allow-Methods", 
                    "Access-Control-Allow-Headers"
                ]
                
                for header in cors_headers:
                    if header in response.headers:
                        print(f"    + {header}: {response.headers[header]}")
                    else:
                        print(f"    ! Missing {header}")
                
            else:
                results[name] = f"CORS_ERROR_{response.status_code}"
                print(f"  {name}: CORS PREFLIGHT ERROR (Status: {response.status_code})")
                
        except Exception as e:
            results[name] = f"CORS_FAILED: {str(e)}"
            print(f"  {name}: CORS PREFLIGHT FAILED - {str(e)}")
    
    return results

def test_performance_impact():
    """Test performance impact of method handling"""
    print("\nTesting Performance Impact...")
    
    endpoints = [
        ("API Gateway Health GET", f"{API_BASE}/health", "GET"),
        ("API Gateway Health HEAD", f"{API_BASE}/health", "HEAD"),
        ("AI Agent Health GET", f"{AI_BASE}/health", "GET"),
        ("AI Agent Health HEAD", f"{AI_BASE}/health", "HEAD")
    ]
    
    results = {}
    for name, url, method in endpoints:
        try:
            # Measure response time
            start_time = time.time()
            
            if method == "GET":
                response = requests.get(url, timeout=5)
            elif method == "HEAD":
                response = requests.head(url, timeout=5)
            
            end_time = time.time()
            response_time = (end_time - start_time) * 1000  # Convert to milliseconds
            
            if response.status_code == 200:
                results[name] = f"SUCCESS_{response_time:.2f}ms"
                print(f"  {name}: SUCCESS ({response_time:.2f}ms)")
            else:
                results[name] = f"ERROR_{response.status_code}_{response_time:.2f}ms"
                print(f"  {name}: ERROR {response.status_code} ({response_time:.2f}ms)")
                
        except Exception as e:
            results[name] = f"PERFORMANCE_TEST_FAILED: {str(e)}"
            print(f"  {name}: PERFORMANCE TEST FAILED - {str(e)}")
    
    return results

def main():
    """Run all HTTP method tests"""
    print("BHIV HR Platform - HTTP Methods Testing")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run all tests
    test_results = {}
    test_results["HEAD Requests"] = test_head_requests()
    test_results["OPTIONS Requests"] = test_options_requests()
    test_results["Unsupported Methods"] = test_unsupported_methods()
    test_results["Method Consistency"] = test_method_consistency()
    test_results["CORS Preflight"] = test_cors_preflight()
    test_results["Performance Impact"] = test_performance_impact()
    
    # Summary
    print("\n" + "=" * 60)
    print("HTTP METHODS TEST SUMMARY")
    print("=" * 60)
    
    total_tests = 0
    passed_tests = 0
    
    for category, results in test_results.items():
        print(f"\n{category}:")
        category_passed = 0
        category_total = len(results)
        
        for test_name, result in results.items():
            status = "PASSED" if any(success in result for success in [
                "SUCCESS", "CORRECTLY_REJECTED", "CONSISTENT", "CORS_SUCCESS"
            ]) else "FAILED"
            
            print(f"  {test_name:<40}: {status}")
            
            if status == "PASSED":
                category_passed += 1
                passed_tests += 1
            
            total_tests += 1
        
        print(f"  Category Summary: {category_passed}/{category_total} passed")
    
    print(f"\nOverall Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("SUCCESS: All HTTP method tests passed!")
    elif passed_tests == 0:
        print("INFO: Services may not be running - start services and retry")
    else:
        print("WARNING: Some HTTP method tests failed")
    
    print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()