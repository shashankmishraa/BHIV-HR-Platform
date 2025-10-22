#!/usr/bin/env python3
"""
Simple Client Login Test
Tests the client login endpoint functionality
"""

import requests
import json

def test_client_login():
    """Test client login endpoint"""
    url = "https://bhiv-hr-gateway-46pz.onrender.com/v1/client/login"
    
    # Test data
    login_data = {
        "client_id": "TECH001",
        "password": "demo123"
    }
    
    print("Testing Client Login Endpoint...")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(login_data, indent=2)}")
    
    try:
        response = requests.post(
            url,
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        try:
            response_data = response.json()
            print(f"Response Body: {json.dumps(response_data, indent=2)}")
            
            if response_data.get('success'):
                print("\n✅ LOGIN SUCCESS!")
                print(f"Client ID: {response_data.get('client_id')}")
                print(f"Company: {response_data.get('company_name')}")
                print(f"Token: {response_data.get('access_token', 'N/A')[:50]}...")
            else:
                print(f"\n❌ LOGIN FAILED: {response_data.get('error')}")
                
        except json.JSONDecodeError:
            print(f"Response Text: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_client_login()