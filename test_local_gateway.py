#!/usr/bin/env python3
"""Test Local Gateway Routes"""

import requests
import json
import time

def test_local_gateway():
    """Test gateway routes locally"""
    base_url = "http://localhost:8000"
    
    # Test endpoints that HR portal needs
    test_endpoints = [
        {"method": "GET", "path": "/", "expected_status": 200},
        {"method": "GET", "path": "/health", "expected_status": 200},
        {"method": "GET", "path": "/v1/candidates", "expected_status": 200},
        {"method": "GET", "path": "/v1/jobs", "expected_status": 200},
        {"method": "GET", "path": "/v1/interviews", "expected_status": 200},
        {"method": "GET", "path": "/v1/analytics/dashboard", "expected_status": 200},
        {"method": "GET", "path": "/metrics", "expected_status": 200},
        {"method": "GET", "path": "/health/detailed", "expected_status": 200},
        {"method": "GET", "path": "/v1/database/health", "expected_status": 200},
    ]
    
    print("=== LOCAL GATEWAY ROUTE VERIFICATION ===")
    print(f"Testing: {base_url}")
    
    results = []
    
    for test in test_endpoints:
        try:
            url = f"{base_url}{test['path']}"
            
            if test['method'] == 'GET':
                response = requests.get(url, timeout=5)
            elif test['method'] == 'POST':
                response = requests.post(url, timeout=5)
            
            status_ok = response.status_code == test['expected_status']
            
            result = {
                "endpoint": test['path'],
                "method": test['method'],
                "status_code": response.status_code,
                "expected": test['expected_status'],
                "success": status_ok,
                "response_time": response.elapsed.total_seconds()
            }
            
            if status_ok:
                print(f"OK {test['method']} {test['path']} - {response.status_code} ({response.elapsed.total_seconds():.3f}s)")
            else:
                print(f"FAIL {test['method']} {test['path']} - {response.status_code} (expected {test['expected_status']})")
            
            results.append(result)
            
        except Exception as e:
            print(f"ERROR {test['method']} {test['path']} - {str(e)}")
            results.append({
                "endpoint": test['path'],
                "method": test['method'],
                "success": False,
                "error": str(e)
            })
    
    # Summary
    successful = sum(1 for r in results if r.get('success', False))
    total = len(results)
    success_rate = (successful / total) * 100
    
    print(f"\n=== SUMMARY ===")
    print(f"Total endpoints tested: {total}")
    print(f"Successful: {successful}")
    print(f"Failed: {total - successful}")
    print(f"Success rate: {success_rate:.1f}%")
    
    return success_rate >= 90

def test_production_gateway():
    """Test production gateway routes"""
    base_url = "https://bhiv-hr-gateway-901a.onrender.com"
    
    # Test critical endpoints
    test_endpoints = [
        {"method": "GET", "path": "/", "expected_status": 200},
        {"method": "GET", "path": "/health", "expected_status": 200},
        {"method": "GET", "path": "/v1/candidates", "expected_status": 200},
        {"method": "GET", "path": "/v1/jobs", "expected_status": 200},
    ]
    
    print("\n=== PRODUCTION GATEWAY VERIFICATION ===")
    print(f"Testing: {base_url}")
    
    results = []
    
    for test in test_endpoints:
        try:
            url = f"{base_url}{test['path']}"
            response = requests.get(url, timeout=10)
            
            status_ok = response.status_code == test['expected_status']
            
            if status_ok:
                print(f"OK {test['method']} {test['path']} - {response.status_code}")
            else:
                print(f"FAIL {test['method']} {test['path']} - {response.status_code}")
                if response.status_code == 404:
                    print(f"  Response: {response.text[:100]}")
            
            results.append({"success": status_ok})
            
        except Exception as e:
            print(f"ERROR {test['method']} {test['path']} - {str(e)}")
            results.append({"success": False})
    
    successful = sum(1 for r in results if r.get('success', False))
    total = len(results)
    success_rate = (successful / total) * 100
    
    print(f"Production success rate: {success_rate:.1f}%")
    return success_rate >= 75

if __name__ == "__main__":
    print("Testing gateway routes...")
    
    # Test production first
    prod_ok = test_production_gateway()
    
    if not prod_ok:
        print("\nProduction gateway has issues. Testing local setup...")
        # Could test local if needed
        print("Local testing would require starting the server first.")
    else:
        print("\nProduction gateway is working correctly!")