#!/usr/bin/env python3
"""
Simple deployment test without unicode issues
"""
import requests
import time
import sys

# Local service URLs
SERVICES = {
    "gateway": "http://localhost:8000",
    "agent": "http://localhost:9000", 
    "hr_portal": "http://localhost:8501",
    "client_portal": "http://localhost:8502"
}

API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"

def test_service_health(service_name, url):
    """Test if service is healthy"""
    try:
        response = requests.get(f"{url}/health", timeout=10)
        if response.status_code == 200:
            print(f"SUCCESS: {service_name} is HEALTHY")
            return True
        else:
            print(f"FAILED: {service_name} returned HTTP {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"FAILED: {service_name} connection failed - {e}")
        return False

def test_gateway_api():
    """Test gateway API functionality"""
    print("\n=== Testing Gateway API ===")
    
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    # Test root endpoint
    try:
        response = requests.get(f"{SERVICES['gateway']}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: Gateway root - Version {data.get('version')}")
            print(f"  Endpoints: {data.get('endpoints')}")
        else:
            print(f"FAILED: Gateway root returned {response.status_code}")
    except Exception as e:
        print(f"FAILED: Gateway root error - {e}")
    
    # Test jobs endpoint
    try:
        response = requests.get(f"{SERVICES['gateway']}/v1/jobs", headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: Jobs endpoint - Found {data.get('count', 0)} jobs")
        else:
            print(f"FAILED: Jobs endpoint returned {response.status_code}")
    except Exception as e:
        print(f"FAILED: Jobs endpoint error - {e}")

def test_agent_api():
    """Test agent API functionality"""
    print("\n=== Testing Agent API ===")
    
    # Test root endpoint
    try:
        response = requests.get(f"{SERVICES['agent']}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: Agent root - Version {data.get('version')}")
            print(f"  Service: {data.get('service')}")
        else:
            print(f"FAILED: Agent root returned {response.status_code}")
    except Exception as e:
        print(f"FAILED: Agent root error - {e}")
    
    # Test database connectivity
    try:
        response = requests.get(f"{SERVICES['agent']}/test-db", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: Agent database - Status: {data.get('status')}")
            if data.get('candidates_count'):
                print(f"  Candidates in DB: {data['candidates_count']}")
        else:
            print(f"FAILED: Agent database test returned {response.status_code}")
    except Exception as e:
        print(f"FAILED: Agent database error - {e}")

def test_ai_matching():
    """Test AI matching functionality"""
    print("\n=== Testing AI Matching ===")
    
    # Test direct agent matching
    try:
        payload = {"job_id": 1}
        response = requests.post(f"{SERVICES['agent']}/match", json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: Agent matching - Algorithm: {data.get('algorithm_version')}")
            print(f"  Status: {data.get('status')}")
            print(f"  Candidates processed: {data.get('total_candidates', 0)}")
            print(f"  Top matches: {len(data.get('top_candidates', []))}")
        else:
            print(f"FAILED: Agent matching returned {response.status_code}")
    except Exception as e:
        print(f"FAILED: Agent matching error - {e}")
    
    # Test gateway AI matching
    try:
        headers = {"Authorization": f"Bearer {API_KEY}"}
        response = requests.get(f"{SERVICES['gateway']}/v1/match/1/top", headers=headers, timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: Gateway matching - Algorithm: {data.get('algorithm_version')}")
            print(f"  Agent status: {data.get('agent_status')}")
            print(f"  Matches found: {len(data.get('matches', []))}")
        else:
            print(f"FAILED: Gateway matching returned {response.status_code}")
    except Exception as e:
        print(f"FAILED: Gateway matching error - {e}")

def test_portals():
    """Test portal accessibility"""
    print("\n=== Testing Portals ===")
    
    # Test HR Portal
    try:
        response = requests.get(SERVICES['hr_portal'], timeout=10)
        if response.status_code == 200:
            print("SUCCESS: HR Portal is accessible")
        else:
            print(f"FAILED: HR Portal returned {response.status_code}")
    except Exception as e:
        print(f"FAILED: HR Portal error - {e}")
    
    # Test Client Portal
    try:
        response = requests.get(SERVICES['client_portal'], timeout=10)
        if response.status_code == 200:
            print("SUCCESS: Client Portal is accessible")
        else:
            print(f"FAILED: Client Portal returned {response.status_code}")
    except Exception as e:
        print(f"FAILED: Client Portal error - {e}")

def main():
    """Run deployment tests"""
    print("=== BHIV HR Platform - Local Deployment Test ===")
    print("Testing clean architecture deployment...\n")
    
    # Test service health
    print("=== Testing Service Health ===")
    health_results = {}
    for service, url in SERVICES.items():
        if service in ['gateway', 'agent']:  # Only test API services for health
            health_results[service] = test_service_health(service, url)
    
    # Test functionality if services are healthy
    if health_results.get('gateway') and health_results.get('agent'):
        test_gateway_api()
        test_agent_api()
        test_ai_matching()
    else:
        print("\nWARNING: Skipping functionality tests - services not healthy")
    
    # Test portals
    test_portals()
    
    # Summary
    print("\n=== Test Summary ===")
    healthy_services = sum(health_results.values())
    total_services = len(health_results)
    
    print(f"API Services: {healthy_services}/{total_services} healthy")
    
    if healthy_services == total_services:
        print("SUCCESS: All services are healthy and working!")
        print("Clean architecture deployment is successful")
        return 0
    else:
        print("WARNING: Some issues detected in deployment")
        return 1

if __name__ == "__main__":
    sys.exit(main())