#!/usr/bin/env python3
import requests
import time

def test_portal(url, name):
    try:
        start_time = time.time()
        response = requests.get(url, timeout=10)
        response_time = (time.time() - start_time) * 1000
        
        if response.status_code == 200:
            print(f"PASS {name} ({response.status_code}) - {response_time:.0f}ms")
            print(f"     Content-Type: {response.headers.get('content-type', 'unknown')}")
            print(f"     Content-Length: {len(response.content)} bytes")
            return True
        else:
            print(f"FAIL {name} ({response.status_code}) - {response_time:.0f}ms")
            return False
    except Exception as e:
        print(f"ERROR {name} - {str(e)}")
        return False

def main():
    print("BHIV HR Platform - Portal Services Testing")
    print("=" * 50)
    
    portals = [
        ("https://bhiv-hr-portal-cead.onrender.com/", "HR Portal"),
        ("https://bhiv-hr-client-portal-5g33.onrender.com/", "Client Portal"),
    ]
    
    passed = 0
    total = len(portals)
    
    for url, name in portals:
        if test_portal(url, name):
            passed += 1
    
    print(f"\nPortal Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("STATUS: All portals operational")
    else:
        print("STATUS: Some portals may have issues")

if __name__ == "__main__":
    main()