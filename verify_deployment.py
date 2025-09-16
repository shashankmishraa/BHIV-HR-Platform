#!/usr/bin/env python3
"""
Quick Deployment Verification
Tests core functionality to ensure deployment is working
"""

import requests
import time
from datetime import datetime

def test_core_services():
    """Test core services are responding"""
    services = [
        ("Gateway", "http://localhost:8000/health"),
        ("AI Agent", "http://localhost:9000/health"),
        ("Gateway API", "http://localhost:8000/"),
        ("Agent API", "http://localhost:9000/")
    ]
    
    print("Testing Core Services...")
    all_good = True
    
    for name, url in services:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✓ {name}: OK")
            else:
                print(f"✗ {name}: HTTP {response.status_code}")
                all_good = False
        except Exception as e:
            print(f"✗ {name}: ERROR - {str(e)}")
            all_good = False
    
    return all_good

def test_database_connectivity():
    """Test database connectivity"""
    print("\nTesting Database Connectivity...")
    
    try:
        headers = {"Authorization": "Bearer myverysecureapikey123"}
        response = requests.get("http://localhost:8000/test-candidates", headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            count = data.get('total_candidates', 0)
            print(f"✓ Database: Connected ({count} candidates)")
            return True
        else:
            print(f"✗ Database: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Database: ERROR - {str(e)}")
        return False

def test_authentication():
    """Test client authentication"""
    print("\nTesting Authentication...")
    
    try:
        login_data = {"client_id": "TECH001", "password": "demo123"}
        response = requests.post(
            "http://localhost:8000/v1/client/login",
            json=login_data,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'access_token' in data:
                print("✓ Authentication: Working")
                return True
            else:
                print("✗ Authentication: No token returned")
                return False
        else:
            print(f"✗ Authentication: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Authentication: ERROR - {str(e)}")
        return False

def test_ai_matching():
    """Test AI matching functionality"""
    print("\nTesting AI Matching...")
    
    try:
        match_data = {"job_id": 1}
        response = requests.post(
            "http://localhost:9000/match",
            json=match_data,
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            candidates = data.get('top_candidates', [])
            print(f"✓ AI Matching: Working ({len(candidates)} candidates)")
            return True
        else:
            print(f"✗ AI Matching: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ AI Matching: ERROR - {str(e)}")
        return False

def test_job_management():
    """Test job management"""
    print("\nTesting Job Management...")
    
    try:
        headers = {"Authorization": "Bearer myverysecureapikey123"}
        response = requests.get("http://localhost:8000/v1/jobs", headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            jobs = data.get('jobs', [])
            print(f"✓ Job Management: Working ({len(jobs)} jobs)")
            return True
        else:
            print(f"✗ Job Management: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Job Management: ERROR - {str(e)}")
        return False

def main():
    """Run deployment verification"""
    print("BHIV HR Platform - Deployment Verification")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 50)
    
    tests = [
        ("Core Services", test_core_services),
        ("Database", test_database_connectivity),
        ("Authentication", test_authentication),
        ("AI Matching", test_ai_matching),
        ("Job Management", test_job_management)
    ]
    
    results = []
    for test_name, test_func in tests:
        success = test_func()
        results.append((test_name, success))
    
    # Summary
    print("\n" + "=" * 50)
    print("VERIFICATION SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "PASS" if success else "FAIL"
        print(f"{status} {test_name}")
    
    print("-" * 50)
    print(f"Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 DEPLOYMENT VERIFIED! All systems operational.")
        print("\nAccess URLs:")
        print("• HR Portal: http://localhost:8501")
        print("• Client Portal: http://localhost:8502")
        print("• API Docs: http://localhost:8000/docs")
        print("• AI Agent: http://localhost:9000/docs")
        return 0
    else:
        print("\n⚠️ DEPLOYMENT ISSUES DETECTED!")
        print("Check the failed tests above and ensure all services are running.")
        return 1

if __name__ == "__main__":
    exit(main())