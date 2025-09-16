#!/usr/bin/env python3
"""
BHIV HR Platform - Simple HTTP Methods Test
Quick test to verify HTTP method handling implementation
"""

import requests
from datetime import datetime

def test_local_implementation():
    """Test HTTP method handling on local FastAPI instances"""
    print("BHIV HR Platform - Simple HTTP Methods Test")
    print("=" * 50)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test endpoints
    endpoints = [
        ("API Gateway", "http://localhost:8000"),
        ("AI Agent", "http://localhost:9000")
    ]
    
    total_tests = 0
    passed_tests = 0
    
    for service_name, base_url in endpoints:
        print(f"Testing {service_name} ({base_url})...")
        
        # Test health endpoint
        health_url = f"{base_url}/health"
        
        # Test GET request
        try:
            get_response = requests.get(health_url, timeout=2)
            if get_response.status_code == 200:
                print(f"  GET /health: PASSED (200)")
                passed_tests += 1
            else:
                print(f"  GET /health: FAILED ({get_response.status_code})")
            total_tests += 1
        except Exception as e:
            print(f"  GET /health: ERROR - Service not running")
            total_tests += 1
        
        # Test HEAD request
        try:
            head_response = requests.head(health_url, timeout=2)
            if head_response.status_code == 200:
                print(f"  HEAD /health: PASSED (200)")
                if len(head_response.content) == 0:
                    print(f"    + No body content (correct)")
                else:
                    print(f"    ! Has body content ({len(head_response.content)} bytes)")
                passed_tests += 1
            else:
                print(f"  HEAD /health: FAILED ({head_response.status_code})")
            total_tests += 1
        except Exception as e:
            print(f"  HEAD /health: ERROR - Service not running")
            total_tests += 1
        
        # Test OPTIONS request
        try:
            options_response = requests.options(base_url, timeout=2)
            if options_response.status_code == 200:
                print(f"  OPTIONS /: PASSED (200)")
                if 'Allow' in options_response.headers:
                    print(f"    + Allow header: {options_response.headers['Allow']}")
                passed_tests += 1
            else:
                print(f"  OPTIONS /: FAILED ({options_response.status_code})")
            total_tests += 1
        except Exception as e:
            print(f"  OPTIONS /: ERROR - Service not running")
            total_tests += 1
        
        # Test unsupported method (TRACE)
        try:
            trace_response = requests.request("TRACE", base_url, timeout=2)
            if trace_response.status_code == 405:
                print(f"  TRACE /: CORRECTLY REJECTED (405)")
                passed_tests += 1
            else:
                print(f"  TRACE /: UNEXPECTED ({trace_response.status_code})")
            total_tests += 1
        except Exception as e:
            print(f"  TRACE /: ERROR - Service not running")
            total_tests += 1
        
        print()
    
    # Summary
    print("=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    
    if passed_tests == 0:
        print("\nINFO: No tests passed - services may not be running")
        print("To test the implementation:")
        print("1. Start services: docker-compose up -d")
        print("2. Run this test again")
    elif passed_tests == total_tests:
        print("\nSUCCESS: All HTTP method tests passed!")
    else:
        print(f"\nPARTIAL: {passed_tests}/{total_tests} tests passed")
    
    print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    test_local_implementation()