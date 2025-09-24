#!/usr/bin/env python3
"""Verify Gateway Routes After Deployment"""

import requests
import json
import time

def test_gateway_routes():
    """Test all critical gateway routes"""
    base_url = "https://bhiv-hr-gateway-901a.onrender.com"
    
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
    
    print("=== GATEWAY ROUTE VERIFICATION ===")
    print(f"Testing: {base_url}")
    
    results = []
    
    for test in test_endpoints:
        try:
            url = f"{base_url}{test['path']}"
            
            if test['method'] == 'GET':
                response = requests.get(url, timeout=10)
            elif test['method'] == 'POST':
                response = requests.post(url, timeout=10)
            
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
                print(f"✅ {test['method']} {test['path']} - {response.status_code} ({response.elapsed.total_seconds():.3f}s)")
            else:
                print(f"❌ {test['method']} {test['path']} - {response.status_code} (expected {test['expected_status']})")
            
            results.append(result)
            
        except Exception as e:
            print(f"❌ {test['method']} {test['path']} - ERROR: {str(e)}")
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
    
    if success_rate >= 90:
        print("🟢 Gateway routes are working correctly!")
        return True
    else:
        print("🔴 Gateway has route issues that need fixing")
        return False

if __name__ == "__main__":
    test_gateway_routes()