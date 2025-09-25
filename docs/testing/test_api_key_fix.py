#!/usr/bin/env python3
"""
Test API Key Authentication Fix
Tests the corrected API key against the Gateway service
"""

import requests
import json

# Correct production API key
PRODUCTION_API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
GATEWAY_URL = "https://bhiv-hr-gateway.onrender.com"


def test_api_endpoints():
    """Test key endpoints with correct API key"""

    headers = {
        "Authorization": f"Bearer {PRODUCTION_API_KEY}",
        "Content-Type": "application/json",
    }

    endpoints = [
        "/health",
        "/v1/jobs",
        "/v1/candidates",
        "/v1/security/status",
        "/v1/match/1/top",
    ]

    print("Testing API Key Authentication Fix")
    print("=" * 50)
    print(f"API Key: {PRODUCTION_API_KEY[:20]}...")
    print(f"Gateway URL: {GATEWAY_URL}")
    print()

    results = []

    for endpoint in endpoints:
        url = f"{GATEWAY_URL}{endpoint}"
        try:
            print(f"Testing: {endpoint}")
            response = requests.get(url, headers=headers, timeout=10)

            status = (
                "SUCCESS"
                if response.status_code == 200
                else f"FAILED ({response.status_code})"
            )
            print(f"  Status: {status}")

            if response.status_code == 200:
                data = response.json()
                if "message" in data:
                    print(f"  Message: {data['message']}")
                elif "status" in data:
                    print(f"  Service Status: {data['status']}")
            else:
                print(f"  Error: {response.text[:100]}")

            results.append(
                {
                    "endpoint": endpoint,
                    "status_code": response.status_code,
                    "success": response.status_code == 200,
                }
            )

        except Exception as e:
            print(f"  ERROR: {str(e)}")
            results.append(
                {
                    "endpoint": endpoint,
                    "status_code": 0,
                    "success": False,
                    "error": str(e),
                }
            )

        print()

    # Summary
    successful = sum(1 for r in results if r["success"])
    total = len(results)

    print("Test Summary")
    print("=" * 50)
    print(f"Successful: {successful}/{total}")
    print(f"Success Rate: {(successful/total)*100:.1f}%")

    if successful == total:
        print("ALL TESTS PASSED - API Key authentication is working!")
    else:
        print("Some tests failed - Check API key configuration")

    return results


if __name__ == "__main__":
    test_api_endpoints()
