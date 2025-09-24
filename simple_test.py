#!/usr/bin/env python3
"""
BHIV HR Platform - Simple Test Suite
Tests database changes and service integration
"""

import requests
import time
from datetime import datetime

def test_service(name, url):
    """Test service health"""
    try:
        print(f"Testing {name}...")
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"  SUCCESS: {name} is responding")
            return True
        else:
            print(f"  FAILED: {name} returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"  FAILED: {name} - {str(e)}")
        return False

def test_database_endpoints():
    """Test database endpoints"""
    print("\nTesting Database Endpoints...")
    
    endpoints = [
        ("Database Health", "http://localhost:8000/database/health"),
        ("Jobs Count", "http://localhost:8000/database/jobs/count"),
        ("Candidates Count", "http://localhost:8000/database/candidates/count")
    ]
    
    results = []
    for name, url in endpoints:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"  SUCCESS: {name}")
                try:
                    data = response.json()
                    if 'count' in data:
                        print(f"    Count: {data['count']}")
                except:
                    pass
                results.append(True)
            else:
                print(f"  FAILED: {name} - Status {response.status_code}")
                results.append(False)
        except Exception as e:
            print(f"  FAILED: {name} - {str(e)}")
            results.append(False)
    
    return results

def main():
    print("BHIV HR Platform - Simple Test Suite")
    print("=" * 50)
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test core services
    print("Testing Core Services...")
    services = [
        ("Gateway Service", "http://localhost:8000/health"),
        ("AI Agent Service", "http://localhost:9000/health")
    ]
    
    service_results = []
    for name, url in services:
        result = test_service(name, url)
        service_results.append(result)
        time.sleep(1)
    
    # Test database endpoints if gateway is up
    db_results = []
    if service_results[0]:  # Gateway is up
        db_results = test_database_endpoints()
    
    # Test production services
    print("\nTesting Production Services...")
    prod_services = [
        ("Production Gateway", "https://bhiv-hr-gateway-901a.onrender.com/health"),
        ("Production Agent", "https://bhiv-hr-agent-o6nx.onrender.com/health")
    ]
    
    prod_results = []
    for name, url in prod_services:
        result = test_service(name, url)
        prod_results.append(result)
        time.sleep(1)
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    total_tests = len(service_results) + len(db_results) + len(prod_results)
    passed_tests = sum(service_results) + sum(db_results) + sum(prod_results)
    
    print(f"Passed: {passed_tests}/{total_tests}")
    print(f"Failed: {total_tests - passed_tests}/{total_tests}")
    
    if total_tests > 0:
        success_rate = (passed_tests / total_tests) * 100
        print(f"Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print("\nSUCCESS: Services are running well!")
        elif success_rate >= 60:
            print("\nWARNING: Some services need attention")
        else:
            print("\nERROR: Multiple service issues detected")
    
    # Specific results
    print(f"\nLocal Services: {sum(service_results)}/{len(service_results)} working")
    print(f"Database Endpoints: {sum(db_results)}/{len(db_results)} working")
    print(f"Production Services: {sum(prod_results)}/{len(prod_results)} working")

if __name__ == "__main__":
    main()