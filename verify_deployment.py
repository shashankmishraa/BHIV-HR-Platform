#!/usr/bin/env python3
"""
Minimal deployment verification script
Checks if the schema endpoint is available in production
"""

import requests
import json

def test_schema_endpoint():
    """Test if schema endpoint is available"""
    url = "https://bhiv-hr-gateway-46pz.onrender.com/v1/database/schema"
    headers = {
        "Authorization": "Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Schema endpoint is working!")
            print(f"Schema Version: {data.get('schema_version', 'unknown')}")
            print(f"Total Tables: {data.get('total_tables', 0)}")
            print(f"Phase 3 Enabled: {data.get('phase3_enabled', False)}")
            return True
        else:
            print(f"Schema endpoint failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"Connection failed: {e}")
        return False

def test_root_endpoint():
    """Test root endpoint for endpoint count"""
    url = "https://bhiv-hr-gateway-46pz.onrender.com/"
    
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            data = response.json()
            endpoint_count = data.get('endpoints', 0)
            print(f"Root endpoint working - {endpoint_count} endpoints reported")
            return endpoint_count
        else:
            print(f"Root endpoint failed: {response.status_code}")
            return 0
    except Exception as e:
        print(f"Root endpoint connection failed: {e}")
        return 0

if __name__ == "__main__":
    print("Verifying Render deployment...")
    
    # Test root endpoint
    endpoint_count = test_root_endpoint()
    
    # Test schema endpoint
    schema_working = test_schema_endpoint()
    
    print("\nSummary:")
    print(f"Endpoint Count: {endpoint_count}")
    print(f"Schema Endpoint: {'Working' if schema_working else 'Not Available'}")
    
    if endpoint_count == 50 and schema_working:
        print("Deployment is up to date!")
    else:
        print("Deployment needs update - redeploy on Render")