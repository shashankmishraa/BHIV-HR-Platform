#!/usr/bin/env python3
"""
Test Search Endpoint Directly
"""

import requests

def test_search_endpoint():
    print("Testing search endpoint...")
    
    # Test different variations
    test_cases = [
        "https://bhiv-hr-gateway-46pz.onrender.com/v1/candidates/search",
        "https://bhiv-hr-gateway-46pz.onrender.com/v1/candidates/search?skills=Python",
        "https://bhiv-hr-gateway-46pz.onrender.com/v1/candidates/search?location=New York",
        "https://bhiv-hr-gateway-46pz.onrender.com/v1/candidates/search?experience_min=2"
    ]
    
    headers = {"Authorization": "Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"}
    
    for i, url in enumerate(test_cases, 1):
        print(f"\nTest {i}: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"  Status: {response.status_code}")
            if response.status_code != 200:
                print(f"  Error: {response.text[:200]}")
            else:
                data = response.json()
                print(f"  Success: Found {data.get('count', 0)} candidates")
        except Exception as e:
            print(f"  Exception: {str(e)[:100]}")

if __name__ == "__main__":
    test_search_endpoint()