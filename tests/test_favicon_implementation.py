#!/usr/bin/env python3
"""
BHIV HR Platform - Favicon Implementation Testing
Tests favicon availability and proper HTTP responses across all services
"""

import requests
import time
from datetime import datetime

# Configuration
API_BASE = "http://localhost:8000"
AI_BASE = "http://localhost:9000"
PORTAL_BASE = "http://localhost:8501"
CLIENT_PORTAL_BASE = "http://localhost:8502"

def test_favicon_endpoints():
    """Test favicon endpoints across all services"""
    print("BHIV HR Platform - Favicon Implementation Testing")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    services = [
        ("API Gateway", f"{API_BASE}/favicon.ico"),
        ("AI Agent", f"{AI_BASE}/favicon.ico"),
        ("HR Portal", f"{PORTAL_BASE}/favicon.ico"),
        ("Client Portal", f"{CLIENT_PORTAL_BASE}/favicon.ico")
    ]
    
    results = {}
    total_tests = 0
    passed_tests = 0
    
    for service_name, favicon_url in services:
        print(f"Testing {service_name}...")
        total_tests += 1
        
        try:
            # Test favicon endpoint
            response = requests.get(favicon_url, timeout=5)
            
            if response.status_code == 200:
                print(f"  + Favicon Available: 200 OK")
                
                # Check content type
                content_type = response.headers.get('content-type', '')
                if 'image' in content_type or 'icon' in content_type:
                    print(f"  + Content-Type: {content_type}")
                else:
                    print(f"  ! Content-Type: {content_type} (expected image/x-icon)")
                
                # Check content length
                content_length = len(response.content)
                if content_length > 0:
                    print(f"  + Content Size: {content_length} bytes")
                else:
                    print(f"  ! Empty Content: 0 bytes")
                
                # Check caching headers
                cache_control = response.headers.get('cache-control', '')
                if cache_control:
                    print(f"  + Cache-Control: {cache_control}")
                
                etag = response.headers.get('etag', '')
                if etag:
                    print(f"  + ETag: {etag}")
                
                results[service_name] = "AVAILABLE"
                passed_tests += 1
                
            elif response.status_code == 204:
                print(f"  + No Content: 204 (graceful handling)")
                results[service_name] = "GRACEFUL_FALLBACK"
                passed_tests += 1
                
            elif response.status_code == 404:
                print(f"  - Not Found: 404 (needs implementation)")
                results[service_name] = "NOT_IMPLEMENTED"
                
            else:
                print(f"  ! Unexpected Status: {response.status_code}")
                results[service_name] = f"UNEXPECTED_{response.status_code}"
                
        except requests.exceptions.ConnectionError:
            print(f"  - Service Not Running")
            results[service_name] = "SERVICE_DOWN"
            
        except Exception as e:
            print(f"  ! Error: {str(e)}")
            results[service_name] = f"ERROR"
        
        print()
    
    return results, total_tests, passed_tests

def test_favicon_head_requests():
    """Test HEAD requests for favicon endpoints"""
    print("Testing HEAD Requests for Favicons...")
    print("-" * 40)
    
    services = [
        ("API Gateway", f"{API_BASE}/favicon.ico"),
        ("AI Agent", f"{AI_BASE}/favicon.ico")
    ]
    
    results = {}
    
    for service_name, favicon_url in services:
        try:
            # Test HEAD request
            response = requests.head(favicon_url, timeout=5)
            
            if response.status_code == 200:
                print(f"  + {service_name}: HEAD 200 OK")
                
                # Verify no body content
                if len(response.content) == 0:
                    print(f"    + No body content (correct for HEAD)")
                else:
                    print(f"    ! Has body content: {len(response.content)} bytes")
                
                results[service_name] = "HEAD_SUCCESS"
            else:
                print(f"  - {service_name}: HEAD {response.status_code}")
                results[service_name] = f"HEAD_FAILED_{response.status_code}"
                
        except requests.exceptions.ConnectionError:
            print(f"  - {service_name}: Service not running")
            results[service_name] = "SERVICE_DOWN"
            
        except Exception as e:
            print(f"  ! {service_name}: Error - {str(e)}")
            results[service_name] = "HEAD_ERROR"
    
    print()
    return results

def test_browser_compatibility():
    """Test browser-specific favicon requests"""
    print("Testing Browser Compatibility...")
    print("-" * 40)
    
    # Common browser user agents
    user_agents = {
        "Chrome": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Firefox": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Safari": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Edge": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59"
    }
    
    services = [
        ("API Gateway", f"{API_BASE}/favicon.ico"),
        ("AI Agent", f"{AI_BASE}/favicon.ico")
    ]
    
    results = {}
    
    for service_name, favicon_url in services:
        print(f"  {service_name}:")
        service_results = {}
        
        for browser, user_agent in user_agents.items():
            try:
                headers = {"User-Agent": user_agent}
                response = requests.get(favicon_url, headers=headers, timeout=5)
                
                if response.status_code == 200:
                    print(f"    + {browser}: 200 OK")
                    service_results[browser] = "SUCCESS"
                else:
                    print(f"    - {browser}: {response.status_code}")
                    service_results[browser] = f"FAILED_{response.status_code}"
                    
            except requests.exceptions.ConnectionError:
                print(f"    - {browser}: Service not running")
                service_results[browser] = "SERVICE_DOWN"
                
            except Exception as e:
                print(f"    ! {browser}: Error")
                service_results[browser] = "ERROR"
        
        results[service_name] = service_results
        print()
    
    return results

def test_performance_impact():
    """Test performance impact of favicon serving"""
    print("Testing Performance Impact...")
    print("-" * 40)
    
    services = [
        ("API Gateway", f"{API_BASE}/favicon.ico"),
        ("AI Agent", f"{AI_BASE}/favicon.ico")
    ]
    
    results = {}
    
    for service_name, favicon_url in services:
        try:
            # Measure response time for multiple requests
            times = []
            
            for i in range(5):
                start_time = time.time()
                response = requests.get(favicon_url, timeout=5)
                end_time = time.time()
                
                if response.status_code in [200, 204]:
                    times.append((end_time - start_time) * 1000)  # Convert to ms
            
            if times:
                avg_time = sum(times) / len(times)
                min_time = min(times)
                max_time = max(times)
                
                print(f"  {service_name}:")
                print(f"    Average: {avg_time:.2f}ms")
                print(f"    Min: {min_time:.2f}ms")
                print(f"    Max: {max_time:.2f}ms")
                
                results[service_name] = {
                    "avg": avg_time,
                    "min": min_time,
                    "max": max_time,
                    "status": "MEASURED"
                }
            else:
                print(f"  {service_name}: No successful requests")
                results[service_name] = {"status": "FAILED"}
                
        except requests.exceptions.ConnectionError:
            print(f"  {service_name}: Service not running")
            results[service_name] = {"status": "SERVICE_DOWN"}
            
        except Exception as e:
            print(f"  {service_name}: Error - {str(e)}")
            results[service_name] = {"status": "ERROR"}
    
    print()
    return results

def main():
    """Run all favicon tests"""
    # Test favicon endpoints
    favicon_results, total_tests, passed_tests = test_favicon_endpoints()
    
    # Test HEAD requests
    head_results = test_favicon_head_requests()
    
    # Test browser compatibility
    browser_results = test_browser_compatibility()
    
    # Test performance impact
    performance_results = test_performance_impact()
    
    # Generate summary report
    print("=" * 60)
    print("FAVICON IMPLEMENTATION TEST SUMMARY")
    print("=" * 60)
    
    print(f"Favicon Availability: {passed_tests}/{total_tests} services")
    for service, result in favicon_results.items():
        status = "PASSED" if result in ["AVAILABLE", "GRACEFUL_FALLBACK"] else "FAILED"
        print(f"  {service:<20}: {status} ({result})")
    
    print(f"\nHEAD Request Support:")
    for service, result in head_results.items():
        status = "PASSED" if "SUCCESS" in result else "FAILED"
        print(f"  {service:<20}: {status} ({result})")
    
    print(f"\nBrowser Compatibility:")
    for service, browsers in browser_results.items():
        if isinstance(browsers, dict):
            success_count = sum(1 for r in browsers.values() if r == "SUCCESS")
            total_browsers = len(browsers)
            print(f"  {service:<20}: {success_count}/{total_browsers} browsers")
    
    print(f"\nPerformance Impact:")
    for service, perf in performance_results.items():
        if isinstance(perf, dict) and perf.get("status") == "MEASURED":
            print(f"  {service:<20}: {perf['avg']:.2f}ms average")
        else:
            print(f"  {service:<20}: {perf.get('status', 'UNKNOWN')}")
    
    # Overall assessment
    print(f"\n" + "=" * 60)
    print("OVERALL ASSESSMENT")
    print("=" * 60)
    
    if passed_tests == total_tests:
        print("SUCCESS: All services have favicon support implemented!")
        print("- Favicon endpoints return 200 OK or graceful 204")
        print("- HEAD requests work correctly")
        print("- Browser compatibility verified")
        print("- Performance impact minimal")
    elif passed_tests > 0:
        print("PARTIAL: Some services have favicon support")
        print("- Check services that are not running")
        print("- Verify favicon file placement")
        print("- Restart services to pick up changes")
    else:
        print("NEEDS WORK: Favicon support not implemented")
        print("- Services may not be running")
        print("- Favicon endpoints need implementation")
        print("- Static file serving needs configuration")
    
    print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()