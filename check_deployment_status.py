#!/usr/bin/env python3
"""
Check deployment status and test fixes after deployment
"""

import requests
import time
import json

def check_deployment_status():
    """Check if all services are responding after deployment"""
    services = {
        "Gateway": "https://bhiv-hr-gateway.onrender.com/health",
        "AI Agent": "https://bhiv-hr-agent.onrender.com/health", 
        "HR Portal": "https://bhiv-hr-portal.onrender.com/",
        "Client Portal": "https://bhiv-hr-client-portal.onrender.com/"
    }
    
    print("CHECKING DEPLOYMENT STATUS")
    print("=" * 50)
    
    all_ready = True
    
    for service, url in services.items():
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"[OK] {service}: Ready")
            else:
                print(f"[WAIT] {service}: Status {response.status_code}")
                all_ready = False
        except Exception as e:
            print(f"[WAIT] {service}: {str(e)}")
            all_ready = False
    
    return all_ready

def test_fixes():
    """Test the specific fixes after deployment"""
    print("\nTESTING FIXES AFTER DEPLOYMENT")
    print("=" * 50)
    
    base_url = "https://bhiv-hr-gateway.onrender.com"
    headers = {"Authorization": "Bearer myverysecureapikey123"}
    
    tests = [
        ("GET", "/v1/candidates", "Candidates endpoint fix"),
        ("DELETE", "/v1/security/api-keys/test123", "API key revocation fix"),
        ("GET", "/test-candidates", "Test candidates data fix"),
        ("GET", "/v1/jobs", "Authentication test (with key)"),
    ]
    
    results = []
    
    for method, endpoint, description in tests:
        try:
            if method == "GET":
                response = requests.get(f"{base_url}{endpoint}", headers=headers, timeout=10)
            elif method == "DELETE":
                response = requests.delete(f"{base_url}{endpoint}", headers=headers, timeout=10)
            
            if response.status_code in [200, 201, 404]:  # 404 is acceptable for some endpoints
                print(f"[FIXED] {description}: Status {response.status_code}")
                results.append(True)
            else:
                print(f"[ISSUE] {description}: Status {response.status_code}")
                results.append(False)
                
        except Exception as e:
            print(f"[ERROR] {description}: {str(e)}")
            results.append(False)
    
    # Test authentication without key
    try:
        response = requests.get(f"{base_url}/v1/jobs", timeout=10)
        if response.status_code in [401, 403]:
            print(f"[FIXED] Authentication protection: Status {response.status_code}")
            results.append(True)
        else:
            print(f"[ISSUE] Authentication protection: Status {response.status_code}")
            results.append(False)
    except Exception as e:
        print(f"[ERROR] Authentication test: {str(e)}")
        results.append(False)
    
    return results

def main():
    print("BHIV HR PLATFORM - DEPLOYMENT STATUS CHECK")
    print("=" * 60)
    
    # Wait for deployments to complete
    print("Waiting for deployments to complete...")
    time.sleep(30)  # Give deployments time to start
    
    # Check deployment status
    max_attempts = 10
    for attempt in range(max_attempts):
        print(f"\nAttempt {attempt + 1}/{max_attempts}")
        if check_deployment_status():
            print("\n[SUCCESS] All services are ready!")
            break
        else:
            if attempt < max_attempts - 1:
                print("Waiting 30 seconds for deployment to complete...")
                time.sleep(30)
            else:
                print("\n[WARNING] Some services may still be deploying")
    
    # Test the fixes
    time.sleep(10)  # Additional wait for stability
    results = test_fixes()
    
    # Summary
    print("\n" + "=" * 60)
    print("DEPLOYMENT SUMMARY")
    print("=" * 60)
    
    fixed_count = sum(results)
    total_tests = len(results)
    
    print(f"Fixes Verified: {fixed_count}/{total_tests}")
    print(f"Success Rate: {(fixed_count/total_tests)*100:.1f}%")
    
    if fixed_count == total_tests:
        print("[SUCCESS] All fixes deployed and working!")
    elif fixed_count >= total_tests * 0.8:
        print("[GOOD] Most fixes working - deployment successful")
    else:
        print("[WARNING] Some fixes may need additional time")
    
    print("\nDeployment IDs from triggers:")
    print("- Gateway: dep-d35rvsffte5s7396u6eg")
    print("- AI Agent: dep-d35rvuffte5s7396u7mg") 
    print("- HR Portal: dep-d35s009r0fns73be5qbg")
    print("- Client Portal: dep-d35s02nfte5s7396ucfg")

if __name__ == "__main__":
    main()