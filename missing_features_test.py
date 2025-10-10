#!/usr/bin/env python3
import requests
import time

GATEWAY_URL = "https://bhiv-hr-gateway-46pz.onrender.com"
AGENT_URL = "https://bhiv-hr-agent-m1me.onrender.com"
API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def test_missing_endpoint(url, name):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            print(f"FOUND {name} - Working")
            return True
        elif response.status_code == 404:
            print(f"MISSING {name} - Not implemented")
            return False
        else:
            print(f"ERROR {name} - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"ERROR {name} - {str(e)}")
        return False

def main():
    print("Testing for Missing Features in Live Services")
    print("=" * 50)
    
    # Test endpoints mentioned in code but not verified in testing
    missing_endpoints = [
        # Password generation endpoint
        (f"{GATEWAY_URL}/v1/password/generate", "Password Generation"),
        
        # More 2FA endpoints
        (f"{GATEWAY_URL}/v1/2fa/verify-setup", "2FA Verify Setup"),
        (f"{GATEWAY_URL}/v1/2fa/login-with-2fa", "2FA Login"),
        (f"{GATEWAY_URL}/v1/2fa/disable", "2FA Disable"),
        (f"{GATEWAY_URL}/v1/2fa/regenerate-backup-codes", "2FA Backup Codes"),
        
        # CSP endpoints
        (f"{GATEWAY_URL}/v1/security/csp-policies", "CSP Policies"),
        (f"{GATEWAY_URL}/v1/security/csp-violations", "CSP Violations"),
        
        # Password change
        (f"{GATEWAY_URL}/v1/password/change", "Password Change"),
        
        # Offers endpoint
        (f"{GATEWAY_URL}/v1/offers", "Job Offers"),
    ]
    
    print("\nTesting potentially missing endpoints:")
    for url, name in missing_endpoints:
        test_missing_endpoint(url, name)
    
    # Test POST endpoints that might be missing
    print("\nTesting POST endpoints:")
    
    # Test password generation POST
    try:
        response = requests.post(f"{GATEWAY_URL}/v1/password/generate", 
                               headers=HEADERS, json={"length": 12}, timeout=10)
        if response.status_code == 200:
            print("FOUND Password Generation POST - Working")
        else:
            print(f"MISSING Password Generation POST - Status {response.status_code}")
    except Exception as e:
        print(f"ERROR Password Generation POST - {str(e)}")
    
    # Test 2FA verify
    try:
        response = requests.post(f"{GATEWAY_URL}/v1/2fa/verify-setup", 
                               headers=HEADERS, json={"user_id": "test", "totp_code": "123456"}, timeout=10)
        if response.status_code in [200, 401]:  # 401 is expected for wrong code
            print("FOUND 2FA Verify POST - Working")
        else:
            print(f"MISSING 2FA Verify POST - Status {response.status_code}")
    except Exception as e:
        print(f"ERROR 2FA Verify POST - {str(e)}")

if __name__ == "__main__":
    main()