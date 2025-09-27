#!/usr/bin/env python3
"""Simple API Test"""

import requests
import os

def test_api():
    api_key = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
    gateway_url = "https://bhiv-hr-gateway-46pz.onrender.com"
    
    headers = {"Authorization": f"Bearer {api_key}"}
    
    print("Testing API Endpoints...")
    
    # Test health endpoints
    endpoints = [
        f"{gateway_url}/health",
        f"{gateway_url}/",
        f"{gateway_url}/system/modules",
        f"{gateway_url}/candidates",
        f"{gateway_url}/jobs"
    ]
    
    results = []
    
    for endpoint in endpoints:
        try:
            if "candidates" in endpoint or "jobs" in endpoint:
                response = requests.get(endpoint, headers=headers, timeout=10)
            else:
                response = requests.get(endpoint, timeout=10)
            
            success = response.status_code < 500
            results.append(success)
            
            status = "PASS" if success else "FAIL"
            print(f"  {status}: {endpoint.split('/')[-1] or 'root'} ({response.status_code})")
            
        except Exception as e:
            results.append(False)
            print(f"  ERROR: {endpoint.split('/')[-1] or 'root'} - {str(e)}")
    
    passed = sum(results)
    total = len(results)
    
    print(f"\nResults: {passed}/{total} endpoints working")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed >= total * 0.8:  # 80% success rate
        print("STATUS: API OPERATIONAL")
        return True
    else:
        print("STATUS: ISSUES DETECTED")
        return False

if __name__ == "__main__":
    success = test_api()
    exit(0 if success else 1)