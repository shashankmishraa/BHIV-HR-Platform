#!/usr/bin/env python3
"""
Check deployment logs and identify errors
"""

import requests
import json

def check_service_errors():
    """Check each service for deployment errors"""
    
    services = {
        "Gateway": "https://bhiv-hr-gateway.onrender.com",
        "Agent": "https://bhiv-hr-agent.onrender.com", 
        "Portal": "https://bhiv-hr-portal.onrender.com",
        "Client Portal": "https://bhiv-hr-client-portal.onrender.com"
    }
    
    print("DEPLOYMENT ERROR CHECK")
    print("=" * 40)
    
    for service_name, base_url in services.items():
        print(f"\n{service_name}:")
        print("-" * 20)
        
        # Check basic health
        try:
            response = requests.get(f"{base_url}/health", timeout=10)
            if response.status_code == 200:
                print(f"  Health: OK")
                data = response.json()
                version = data.get('version', 'unknown')
                timestamp = data.get('timestamp', 'unknown')
                print(f"  Version: {version}")
                print(f"  Timestamp: {timestamp}")
            else:
                print(f"  Health: ERROR {response.status_code}")
        except Exception as e:
            print(f"  Health: FAILED - {str(e)[:50]}")
        
        # Check if service has logs endpoint
        try:
            response = requests.get(f"{base_url}/", timeout=5)
            if response.status_code == 200:
                print(f"  Root: OK")
            else:
                print(f"  Root: ERROR {response.status_code}")
        except Exception as e:
            print(f"  Root: FAILED - {str(e)[:50]}")

def check_agent_specific_errors():
    """Check agent service for specific upgrade errors"""
    
    print("\nAGENT SERVICE DETAILED CHECK")
    print("=" * 40)
    
    agent_url = "https://bhiv-hr-agent.onrender.com"
    
    # Check if psutil is available
    try:
        response = requests.get(f"{agent_url}/metrics", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("Metrics endpoint response:")
            print(json.dumps(data, indent=2)[:500] + "...")
        else:
            print(f"Metrics endpoint error: {response.status_code}")
            print(f"Response: {response.text[:200]}")
    except Exception as e:
        print(f"Metrics check failed: {e}")
    
    # Check status endpoint
    try:
        response = requests.get(f"{agent_url}/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("\nStatus endpoint response:")
            print(json.dumps(data, indent=2))
        else:
            print(f"Status endpoint error: {response.status_code}")
    except Exception as e:
        print(f"Status check failed: {e}")

def check_missing_dependencies():
    """Check for missing dependencies that might cause deployment issues"""
    
    print("\nDEPENDENCY CHECK")
    print("=" * 20)
    
    # Check if agent service can import required modules
    agent_url = "https://bhiv-hr-agent.onrender.com"
    
    try:
        # Try to access an endpoint that uses psutil
        response = requests.get(f"{agent_url}/metrics", timeout=10)
        if response.status_code == 500:
            print("ERROR: Likely missing psutil dependency")
            print("Response:", response.text[:200])
        elif response.status_code == 200:
            data = response.json()
            if 'error' in data:
                print("ERROR in metrics:", data.get('error'))
            else:
                print("Metrics endpoint working")
    except Exception as e:
        print(f"Dependency check failed: {e}")

if __name__ == "__main__":
    check_service_errors()
    check_agent_specific_errors() 
    check_missing_dependencies()
    
    print("\nPOSSIBLE ISSUES:")
    print("1. Missing psutil dependency in requirements.txt")
    print("2. Import errors preventing service startup")
    print("3. Code not fully deployed yet")
    print("4. Service needs manual restart")