#!/usr/bin/env python3
"""
Post-Deployment Verification - Check if live endpoints match codebase
"""

import requests
import time
import json
from datetime import datetime

def wait_for_deployment(max_wait_minutes=5):
    """Wait for Render deployment to complete"""
    print("Waiting for Render deployment...")
    
    gateway_url = "https://bhiv-hr-gateway-46pz.onrender.com"
    agent_url = "https://bhiv-hr-agent-m1me.onrender.com"
    api_key = "Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
    
    for attempt in range(max_wait_minutes * 2):  # Check every 30 seconds
        try:
            # Test Gateway
            gateway_response = requests.get(f"{gateway_url}/health", 
                                          headers={"Authorization": api_key}, 
                                          timeout=10)
            
            # Test Agent  
            agent_response = requests.get(f"{agent_url}/health",
                                        headers={"Authorization": api_key},
                                        timeout=10)
            
            if gateway_response.status_code == 200 and agent_response.status_code == 200:
                print(f"✅ Services ready after {attempt * 30} seconds")
                return True
                
        except Exception as e:
            print(f"Attempt {attempt + 1}: Services not ready yet...")
            
        time.sleep(30)
    
    print("⚠️ Deployment verification timed out")
    return False

def verify_endpoint_matching():
    """Verify live endpoints match codebase"""
    print("\nVerifying endpoint matching...")
    
    gateway_url = "https://bhiv-hr-gateway-46pz.onrender.com"
    agent_url = "https://bhiv-hr-agent-m1me.onrender.com"
    api_key = "Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
    
    # Test key endpoints
    test_endpoints = [
        ("Gateway Root", "GET", f"{gateway_url}/", {}),
        ("Gateway Health", "GET", f"{gateway_url}/health", {}),
        ("Gateway Jobs", "GET", f"{gateway_url}/v1/jobs", {"Authorization": api_key}),
        ("Gateway Candidates", "GET", f"{gateway_url}/v1/candidates?limit=5", {"Authorization": api_key}),
        ("Agent Root", "GET", f"{agent_url}/", {}),
        ("Agent Health", "GET", f"{agent_url}/health", {}),
    ]
    
    results = []
    for name, method, url, headers in test_endpoints:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            status = "✅ OK" if response.status_code == 200 else f"❌ {response.status_code}"
            results.append(f"{name}: {status}")
        except Exception as e:
            results.append(f"{name}: ❌ ERROR - {str(e)[:50]}")
    
    return results

def main():
    print("BHIV HR Platform - Post-Deployment Verification")
    print("=" * 50)
    
    # Wait for deployment
    if wait_for_deployment():
        # Verify endpoints
        results = verify_endpoint_matching()
        
        print("\nEndpoint Verification Results:")
        for result in results:
            print(f"  {result}")
        
        # Check if all passed
        passed = sum(1 for r in results if "✅" in r)
        total = len(results)
        
        print(f"\nSummary: {passed}/{total} endpoints verified")
        
        if passed == total:
            print("🎉 DEPLOYMENT SUCCESSFUL - All endpoints working!")
            return True
        else:
            print("⚠️ Some endpoints need attention")
            return False
    else:
        print("❌ Deployment verification failed")
        return False

if __name__ == "__main__":
    main()