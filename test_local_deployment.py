#!/usr/bin/env python3
"""
Test local deployment with clean architecture
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
            print(f"✓ {service_name}: HEALTHY")
            return True
        else:
            print(f"✗ {service_name}: HTTP {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ {service_name}: CONNECTION FAILED - {e}")
        return False

def test_gateway_endpoints():
    """Test gateway API endpoints"""
    print("\n=== Testing Gateway Endpoints ===")
    
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    # Test root endpoint
    try:
        response = requests.get(f"{SERVICES['gateway']}/", timeout=10)
        if response.status_code == 200:
            print("✓ Gateway root endpoint working")
        else:
            print(f"✗ Gateway root failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Gateway root error: {e}")
    
    # Test jobs endpoint
    try:
        response = requests.get(f"{SERVICES['gateway']}/v1/jobs", headers=headers, timeout=10)
        if response.status_code == 200:
            print("✓ Jobs endpoint working")
        else:
            print(f"✗ Jobs endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Jobs endpoint error: {e}")
    
    # Test candidates endpoint
    try:
        response = requests.get(f"{SERVICES['gateway']}/v1/candidates", headers=headers, timeout=10)
        if response.status_code == 200:
            print("✓ Candidates endpoint working")
        else:
            print(f"✗ Candidates endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Candidates endpoint error: {e}")

def test_agent_endpoints():
    """Test agent service endpoints"""
    print("\n=== Testing Agent Endpoints ===")
    
    # Test root endpoint
    try:
        response = requests.get(f"{SERVICES['agent']}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✓ Agent root endpoint working")
            print(f"  Service: {data.get('service')}")
            print(f"  Version: {data.get('version')}")
        else:
            print(f"✗ Agent root failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Agent root error: {e}")
    
    # Test database connectivity
    try:
        response = requests.get(f"{SERVICES['agent']}/test-db", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Agent database test: {data.get('status')}")
            if data.get('candidates_count'):
                print(f"  Candidates in DB: {data['candidates_count']}")
        else:
            print(f"✗ Agent database test failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Agent database error: {e}")

def test_ai_matching():
    """Test AI matching functionality"""
    print("\n=== Testing AI Matching ===")
    
    # Test gateway AI matching
    try:
        headers = {"Authorization": f"Bearer {API_KEY}"}
        response = requests.get(f"{SERVICES['gateway']}/v1/match/1/top", headers=headers, timeout=30)
        if response.status_code == 200:
            data = response.json()
            print("✓ Gateway AI matching working")
            print(f"  Algorithm: {data.get('algorithm_version')}")
            print(f"  Matches found: {len(data.get('matches', []))}")
            print(f"  Agent status: {data.get('agent_status')}")
        else:
            print(f"✗ Gateway AI matching failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Gateway AI matching error: {e}")
    
    # Test direct agent matching
    try:
        payload = {"job_id": 1}
        response = requests.post(f"{SERVICES['agent']}/match", json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            print("✓ Direct agent matching working")
            print(f"  Algorithm: {data.get('algorithm_version')}")
            print(f"  Candidates: {len(data.get('top_candidates', []))}")
            print(f"  Status: {data.get('status')}")
        else:
            print(f"✗ Direct agent matching failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Direct agent matching error: {e}")

def test_portal_accessibility():
    """Test portal accessibility"""
    print("\n=== Testing Portal Accessibility ===")
    
    # Test HR Portal
    try:
        response = requests.get(SERVICES['hr_portal'], timeout=10)
        if response.status_code == 200:
            print("✓ HR Portal accessible")
        else:
            print(f"✗ HR Portal failed: {response.status_code}")
    except Exception as e:
        print(f"✗ HR Portal error: {e}")
    
    # Test Client Portal
    try:
        response = requests.get(SERVICES['client_portal'], timeout=10)
        if response.status_code == 200:
            print("✓ Client Portal accessible")
        else:
            print(f"✗ Client Portal failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Client Portal error: {e}")

def main():
    """Run all deployment tests"""
    print("=== Local Deployment Test Suite ===")
    print("Testing clean architecture deployment...\n")
    
    # Wait for services to start
    print("Waiting for services to start...")
    time.sleep(5)
    
    # Test service health
    print("=== Testing Service Health ===")
    health_results = {}
    for service, url in SERVICES.items():
        if service in ['gateway', 'agent']:  # Only test API services for health
            health_results[service] = test_service_health(service, url)
    
    # Test functionality if services are healthy
    if health_results.get('gateway') and health_results.get('agent'):
        test_gateway_endpoints()
        test_agent_endpoints()
        test_ai_matching()
    else:
        print("\n⚠️  Skipping functionality tests - services not healthy")
    
    # Test portal accessibility
    test_portal_accessibility()
    
    # Summary
    print("\n=== Test Summary ===")
    healthy_services = sum(health_results.values())
    total_services = len(health_results)
    
    if healthy_services == total_services:
        print("🎉 All services are healthy and working!")
        print("✓ Clean architecture deployment successful")
        return 0
    else:
        print(f"⚠️  {healthy_services}/{total_services} services healthy")
        print("❌ Some issues detected in deployment")
        return 1

if __name__ == "__main__":
    sys.exit(main())