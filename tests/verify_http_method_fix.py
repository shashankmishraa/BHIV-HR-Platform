#!/usr/bin/env python3
"""
BHIV HR Platform - HTTP Method Fix Verification
Verifies that the HTTP method handling issue has been resolved
"""

import requests
import time
from datetime import datetime

def verify_http_method_fix():
    """Verify that HTTP method handling has been fixed"""
    print("BHIV HR Platform - HTTP Method Fix Verification")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test configuration
    services = [
        ("API Gateway", "http://localhost:8000"),
        ("AI Agent", "http://localhost:9000")
    ]
    
    all_tests_passed = True
    total_tests = 0
    passed_tests = 0
    
    for service_name, base_url in services:
        print(f"Testing {service_name} ({base_url})...")
        
        # Test 1: Service is running (GET request)
        try:
            response = requests.get(f"{base_url}/health", timeout=3)
            if response.status_code == 200:
                print(f"  + Service Running: GET /health returns 200")
                passed_tests += 1
            else:
                print(f"  - Service Issue: GET /health returns {response.status_code}")
                all_tests_passed = False
            total_tests += 1
        except Exception as e:
            print(f"  - Service Down: {str(e)}")
            all_tests_passed = False
            total_tests += 1
            continue
        
        # Test 2: HEAD request works (main fix verification)
        try:
            response = requests.head(f"{base_url}/health", timeout=3)
            if response.status_code == 200:
                if len(response.content) == 0:
                    print(f"  + HEAD Method Fixed: Returns 200 with no body")
                    passed_tests += 1
                else:
                    print(f"  ! HEAD Method Issue: Has body content ({len(response.content)} bytes)")
                    all_tests_passed = False
            else:
                print(f"  - HEAD Method Failed: Returns {response.status_code}")
                all_tests_passed = False
            total_tests += 1
        except Exception as e:
            print(f"  - HEAD Method Error: {str(e)}")
            all_tests_passed = False
            total_tests += 1
        
        # Test 3: OPTIONS request works
        try:
            response = requests.options(base_url, timeout=3)
            if response.status_code == 200:
                if 'Allow' in response.headers or 'Access-Control-Allow-Methods' in response.headers:
                    allow_header = response.headers.get('Allow', response.headers.get('Access-Control-Allow-Methods', ''))
                    print(f"  + OPTIONS Method Fixed: Returns 200 with Allow header")
                    print(f"    Allowed methods: {allow_header}")
                    passed_tests += 1
                else:
                    print(f"  ! OPTIONS Method Issue: Missing Allow header")
                    all_tests_passed = False
            else:
                print(f"  - OPTIONS Method Failed: Returns {response.status_code}")
                all_tests_passed = False
            total_tests += 1
        except Exception as e:
            print(f"  - OPTIONS Method Error: {str(e)}")
            all_tests_passed = False
            total_tests += 1
        
        # Test 4: Unsupported method returns 405
        try:
            response = requests.request("TRACE", base_url, timeout=3)
            if response.status_code == 405:
                if 'Allow' in response.headers:
                    print(f"  + Unsupported Methods: TRACE correctly rejected (405)")
                    passed_tests += 1
                else:
                    print(f"  ! Unsupported Methods: 405 but missing Allow header")
                    all_tests_passed = False
            else:
                print(f"  - Unsupported Methods: TRACE returns {response.status_code} (should be 405)")
                all_tests_passed = False
            total_tests += 1
        except Exception as e:
            print(f"  - Unsupported Methods Error: {str(e)}")
            all_tests_passed = False
            total_tests += 1
        
        # Test 5: GET/HEAD consistency
        try:
            get_response = requests.get(f"{base_url}/health", timeout=3)
            head_response = requests.head(f"{base_url}/health", timeout=3)
            
            if get_response.status_code == head_response.status_code:
                get_ct = get_response.headers.get('content-type', '')
                head_ct = head_response.headers.get('content-type', '')
                
                if get_ct == head_ct and len(head_response.content) == 0:
                    print(f"  + GET/HEAD Consistency: Status and headers match, HEAD has no body")
                    passed_tests += 1
                else:
                    print(f"  ! GET/HEAD Consistency: Headers or body mismatch")
                    all_tests_passed = False
            else:
                print(f"  - GET/HEAD Consistency: Status codes differ ({get_response.status_code} vs {head_response.status_code})")
                all_tests_passed = False
            total_tests += 1
        except Exception as e:
            print(f"  - GET/HEAD Consistency Error: {str(e)}")
            all_tests_passed = False
            total_tests += 1
        
        print()
    
    # Summary
    print("=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    print()
    
    if all_tests_passed and passed_tests == total_tests:
        print("SUCCESS: HTTP Method Handling Issue RESOLVED!")
        print()
        print("All HTTP methods are now properly handled:")
        print("   - HEAD requests return 200 with no body content")
        print("   - OPTIONS requests return 200 with proper CORS headers")
        print("   - Unsupported methods return 405 with Allow header")
        print("   - GET/HEAD responses are consistent")
        print()
        print("The following issues have been fixed:")
        print("   - No more 405 Method Not Allowed errors for HEAD requests")
        print("   - Monitoring tools can now use HEAD for health checks")
        print("   - CORS preflight requests work correctly")
        print("   - Log noise from unsupported methods reduced")
        print()
        print("RESOLUTION STATUS: COMPLETE")
        
    elif passed_tests > 0:
        print("PARTIAL SUCCESS: Some HTTP method handling works")
        print()
        print("Issues that may need attention:")
        if passed_tests < total_tests:
            print("   - Some services may need restart to pick up changes")
            print("   - Check middleware order in service configuration")
            print("   - Verify CORS middleware placement")
        print()
        print("Next steps:")
        print("   1. Restart services: docker-compose restart")
        print("   2. Run this verification again")
        print("   3. Check service logs for errors")
        print()
        print("RESOLUTION STATUS: IN PROGRESS")
        
    else:
        print("FAILURE: HTTP Method Handling Issue NOT RESOLVED")
        print()
        print("Possible causes:")
        print("   - Services not restarted after code changes")
        print("   - Middleware not properly configured")
        print("   - Services not running or accessible")
        print()
        print("Troubleshooting steps:")
        print("   1. Restart services: docker-compose restart")
        print("   2. Check service status: docker-compose ps")
        print("   3. Check service logs: docker-compose logs")
        print("   4. Verify middleware implementation")
        print()
        print("RESOLUTION STATUS: FAILED")
    
    print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return all_tests_passed

if __name__ == "__main__":
    success = verify_http_method_fix()
    exit(0 if success else 1)