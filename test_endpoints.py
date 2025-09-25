#!/usr/bin/env python3
"""Simple endpoint testing tool"""

import httpx
import json
import time

def test_endpoints():
    """Test key endpoints"""
    
    gateway_url = "https://bhiv-hr-gateway-901a.onrender.com"
    agent_url = "https://bhiv-hr-agent-o6nx.onrender.com"
    
    api_key = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    endpoints = [
        # Gateway Core
        ("GET", f"{gateway_url}/health"),
        ("GET", f"{gateway_url}/docs"),
        ("GET", f"{gateway_url}/v1/jobs"),
        ("GET", f"{gateway_url}/v1/candidates"),
        ("GET", f"{gateway_url}/health/detailed"),
        ("GET", f"{gateway_url}/monitoring/errors"),
        ("GET", f"{gateway_url}/metrics"),
        
        # Agent Core
        ("GET", f"{agent_url}/health"),
        ("GET", f"{agent_url}/docs"),
        ("GET", f"{agent_url}/v1/analytics/performance"),
    ]
    
    results = {"functional": [], "non_functional": []}
    
    print("Testing Live Service Endpoints...")
    print("=" * 50)
    
    for method, url in endpoints:
        try:
            start_time = time.time()
            
            if method == "GET":
                response = httpx.get(url, headers=headers, timeout=10.0)
            else:
                response = httpx.post(url, headers=headers, timeout=10.0)
            
            response_time = time.time() - start_time
            
            status = "PASS" if 200 <= response.status_code < 300 else "FAIL"
            print(f"{status}: {method} {url} - {response.status_code} ({response_time:.2f}s)")
            
            result = {
                "method": method,
                "url": url,
                "status_code": response.status_code,
                "response_time": response_time,
                "success": 200 <= response.status_code < 300
            }
            
            if result["success"]:
                results["functional"].append(result)
            else:
                results["non_functional"].append(result)
                
        except Exception as e:
            print(f"ERROR: {method} {url} - {str(e)}")
            results["non_functional"].append({
                "method": method,
                "url": url,
                "error": str(e),
                "success": False
            })
    
    print("\n" + "=" * 50)
    print("SUMMARY:")
    total = len(results["functional"]) + len(results["non_functional"])
    functional = len(results["functional"])
    success_rate = (functional / total * 100) if total > 0 else 0
    
    print(f"Total Endpoints: {total}")
    print(f"Functional: {functional} ({success_rate:.1f}%)")
    print(f"Non-Functional: {len(results['non_functional'])}")
    
    if results["non_functional"]:
        print("\nNON-FUNCTIONAL ENDPOINTS:")
        for endpoint in results["non_functional"]:
            print(f"  {endpoint['method']} {endpoint['url']}")
            if 'status_code' in endpoint:
                print(f"    Status: {endpoint['status_code']}")
            if 'error' in endpoint:
                print(f"    Error: {endpoint['error']}")
    
    # Save results
    with open("endpoint_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    return results

if __name__ == "__main__":
    test_endpoints()