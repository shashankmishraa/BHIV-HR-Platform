#!/usr/bin/env python3
"""
Check what version is actually deployed on Render
"""

import requests
import json

def main():
    print("Checking deployed version...")
    
    try:
        # Check root endpoint
        response = requests.get("https://bhiv-hr-gateway.onrender.com/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"Deployed version: {data.get('version', 'Unknown')}")
            print(f"Reported endpoints: {data.get('endpoints', 'Unknown')}")
            print(f"Service: {data.get('service', 'Unknown')}")
        
        # Check docs to see actual endpoints
        print("\nChecking /docs endpoint...")
        docs_response = requests.get("https://bhiv-hr-gateway.onrender.com/docs", timeout=10)
        print(f"Docs status: {docs_response.status_code}")
        print(f"Docs size: {len(docs_response.text)} bytes")
        
        # Try to get OpenAPI spec
        print("\nChecking OpenAPI spec...")
        openapi_response = requests.get("https://bhiv-hr-gateway.onrender.com/openapi.json", timeout=10)
        if openapi_response.status_code == 200:
            spec = openapi_response.json()
            paths = list(spec.get('paths', {}).keys())
            print(f"Actual endpoints in OpenAPI: {len(paths)}")
            print("First 10 endpoints:")
            for path in paths[:10]:
                print(f"  {path}")
            if len(paths) > 10:
                print(f"  ... and {len(paths) - 10} more")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()