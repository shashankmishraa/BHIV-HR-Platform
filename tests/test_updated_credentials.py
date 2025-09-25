#!/usr/bin/env python3
"""
BHIV HR Platform - Updated Credentials Validation Test
Tests all services with new production credentials and URLs
"""

import requests
import json
import time
from datetime import datetime

# Updated Production URLs
GATEWAY_URL = "https://bhiv-hr-gateway-901a.onrender.com"
AGENT_URL = "https://bhiv-hr-agent-o6nx.onrender.com"
PORTAL_URL = "https://bhiv-hr-portal-xk2k.onrender.com"
CLIENT_PORTAL_URL = "https://bhiv-hr-client-portal-zdbt.onrender.com"

# Updated Production API Key
API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"


def test_service_health(service_name, url):
    """Test service health endpoint"""
    try:
        response = requests.get(f"{url}/health", timeout=10)
        if response.status_code == 200:
            print(f"PASS {service_name} Health: ({response.status_code})")
            return True
        else:
            print(f"FAIL {service_name} Health: ({response.status_code})")
            return False
    except Exception as e:
        print(f"ERROR {service_name} Health: {str(e)}")
        return False


def test_authenticated_endpoint(service_name, url, endpoint):
    """Test authenticated endpoint with API key"""
    try:
        headers = {"Authorization": f"Bearer {API_KEY}"}
        response = requests.get(f"{url}{endpoint}", headers=headers, timeout=10)
        if response.status_code in [200, 201]:
            print(f"PASS {service_name} Auth: ({response.status_code})")
            return True
        else:
            print(f"FAIL {service_name} Auth: ({response.status_code})")
            return False
    except Exception as e:
        print(f"ERROR {service_name} Auth: {str(e)}")
        return False


def test_web_interface(service_name, url):
    """Test web interface accessibility"""
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            print(f"PASS {service_name} Web: ({response.status_code})")
            return True
        else:
            print(f"FAIL {service_name} Web: ({response.status_code})")
            return False
    except Exception as e:
        print(f"ERROR {service_name} Web: {str(e)}")
        return False


def main():
    """Run comprehensive validation tests"""
    print("BHIV HR Platform - Updated Credentials Validation")
    print("=" * 60)
    print(f"Test Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    results = []

    # Test Gateway Service
    print("Testing Gateway Service...")
    gateway_health = test_service_health("Gateway", GATEWAY_URL)
    gateway_auth = test_authenticated_endpoint("Gateway", GATEWAY_URL, "/v1/jobs")
    results.extend([gateway_health, gateway_auth])
    print()

    # Test Agent Service
    print("Testing Agent Service...")
    agent_health = test_service_health("Agent", AGENT_URL)
    agent_auth = test_authenticated_endpoint("Agent", AGENT_URL, "/candidates/match")
    results.extend([agent_health, agent_auth])
    print()

    # Test Portal Service
    print("Testing Portal Service...")
    portal_web = test_web_interface("Portal", PORTAL_URL)
    results.append(portal_web)
    print()

    # Test Client Portal Service
    print("Testing Client Portal Service...")
    client_portal_web = test_web_interface("Client Portal", CLIENT_PORTAL_URL)
    results.append(client_portal_web)
    print()

    # Summary
    print("Test Summary")
    print("=" * 30)
    passed = sum(results)
    total = len(results)
    success_rate = (passed / total) * 100

    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success Rate: {success_rate:.1f}%")
    print()

    if success_rate >= 80:
        print("VALIDATION SUCCESSFUL - Services are operational!")
    else:
        print("VALIDATION ISSUES - Some services need attention")

    print()
    print("Service URLs:")
    print(f"Gateway:       {GATEWAY_URL}")
    print(f"Agent:         {AGENT_URL}")
    print(f"Portal:        {PORTAL_URL}")
    print(f"Client Portal: {CLIENT_PORTAL_URL}")

    return success_rate >= 80


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
