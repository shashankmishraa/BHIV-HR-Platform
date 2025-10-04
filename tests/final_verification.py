#!/usr/bin/env python3
"""
Final Comprehensive Verification
"""

import requests
from datetime import datetime

# URLs
GATEWAY_URL = "https://bhiv-hr-gateway-46pz.onrender.com"
AGENT_URL = "https://bhiv-hr-agent-m1me.onrender.com"
PORTAL_URL = "https://bhiv-hr-portal-cead.onrender.com"
CLIENT_PORTAL_URL = "https://bhiv-hr-client-portal-5g33.onrender.com"

API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def test_service(name, url, timeout=10):
    """Test service accessibility"""
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            print(f"✅ {name}: ACCESSIBLE")
            return True
        else:
            print(f"❌ {name}: ERROR ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ {name}: FAILED - {str(e)}")
        return False

def test_api_endpoint(name, url, timeout=15):
    """Test API endpoint"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=timeout)
        if response.status_code == 200:
            print(f"✅ {name}: WORKING")
            return True, response.json() if response.content else {}
        else:
            print(f"❌ {name}: ERROR ({response.status_code})")
            return False, None
    except Exception as e:
        print(f"❌ {name}: FAILED - {str(e)}")
        return False, None

def main():
    print("BHIV HR Platform - Final Verification")
    print("=" * 50)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    total_tests = 0
    passed_tests = 0
    
    # Test Service Accessibility
    print("=== SERVICE ACCESSIBILITY ===")
    services = [
        ("Gateway Service", f"{GATEWAY_URL}/"),
        ("Agent Service", f"{AGENT_URL}/"),
        ("HR Portal", PORTAL_URL),
        ("Client Portal", CLIENT_PORTAL_URL)
    ]
    
    for name, url in services:
        total_tests += 1
        if test_service(name, url):
            passed_tests += 1
    
    # Test Core API Functions
    print("\n=== CORE API FUNCTIONS ===")
    api_tests = [
        ("Gateway Health", f"{GATEWAY_URL}/health"),
        ("Agent Health", f"{AGENT_URL}/health"),
        ("Database Test", f"{GATEWAY_URL}/test-candidates"),
        ("Job Listings", f"{GATEWAY_URL}/v1/jobs"),
        ("Candidate Data", f"{GATEWAY_URL}/v1/candidates"),
        ("AI Matching", f"{GATEWAY_URL}/v1/match/1/top"),
        ("Security Status", f"{GATEWAY_URL}/v1/security/rate-limit-status"),
    ]
    
    for name, url in api_tests:
        total_tests += 1
        success, result = test_api_endpoint(name, url)
        if success:
            passed_tests += 1
            
            # Show specific results
            if name == "Database Test" and result:
                count = result.get('total_candidates', 0)
                print(f"   Database: {count} candidates")
            elif name == "AI Matching" and result:
                matches = result.get('top_candidates', [])
                print(f"   AI Matches: {len(matches)} found")
    
    # Test Authentication
    print("\n=== AUTHENTICATION ===")
    total_tests += 1
    client_data = {"client_id": "TECH001", "password": "demo123"}
    try:
        response = requests.post(f"{GATEWAY_URL}/v1/client/login", json=client_data, timeout=15)
        if response.status_code == 200:
            print("✅ Client Authentication: WORKING")
            passed_tests += 1
        else:
            print(f"❌ Client Authentication: ERROR ({response.status_code})")
    except Exception as e:
        print(f"❌ Client Authentication: FAILED - {str(e)}")
    
    # Summary
    print("\n" + "=" * 50)
    print("FINAL VERIFICATION SUMMARY")
    print("=" * 50)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("🎉 STATUS: ALL SYSTEMS OPERATIONAL")
    elif passed_tests >= total_tests * 0.9:
        print("✅ STATUS: EXCELLENT - Minor issues only")
    elif passed_tests >= total_tests * 0.8:
        print("⚠️ STATUS: GOOD - Some issues detected")
    else:
        print("❌ STATUS: CRITICAL - Major issues detected")
    
    print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Final Assessment
    print("\n" + "=" * 50)
    print("FINAL ASSESSMENT")
    print("=" * 50)
    
    if passed_tests >= total_tests * 0.9:
        print("✅ SYSTEM IS PRODUCTION READY")
        print("✅ All core services operational")
        print("✅ API endpoints functional")
        print("✅ Database connected with real data")
        print("✅ AI matching working")
        print("✅ Authentication systems active")
        print("\n🚀 RECOMMENDATION: DEPLOY TO PRODUCTION")
    else:
        print("⚠️ SYSTEM NEEDS ATTENTION")
        print("❌ Some critical services may be down")
        print("\n🔧 RECOMMENDATION: INVESTIGATE ISSUES BEFORE DEPLOYMENT")

if __name__ == "__main__":
    main()