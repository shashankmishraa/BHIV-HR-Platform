#!/usr/bin/env python3
"""
Simple API Response Time Test
Test individual API calls to identify bottlenecks
"""

import requests
import time
from datetime import datetime

def test_single_api_call():
    """Test single API call response time"""
    api_base = "https://bhiv-hr-gateway.onrender.com"
    api_key = "myverysecureapikey123"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    print("Testing single API call response times...")
    print("=" * 50)
    
    # Test different endpoints
    endpoints = [
        ("/health", "Health Check"),
        ("/", "Root Endpoint"),
        ("/v1/match/1/top", "AI Matching"),
        ("/v1/match/cache-status", "Cache Status"),
        ("/test-candidates", "Database Test")
    ]
    
    for endpoint, description in endpoints:
        print(f"\nTesting {description} ({endpoint}):")
        
        for i in range(3):
            start_time = time.time()
            
            try:
                response = requests.get(f"{api_base}{endpoint}", headers=headers, timeout=30)
                end_time = time.time()
                response_time = end_time - start_time
                
                print(f"  Attempt {i+1}: {response_time:.3f}s - Status: {response.status_code}")
                
                if endpoint == "/v1/match/1/top" and response.status_code == 200:
                    data = response.json()
                    processing_time = data.get("processing_time", "unknown")
                    cache_hit = data.get("cache_hit", False)
                    precomputed = data.get("precomputed", False)
                    print(f"    Processing: {processing_time}, Cache: {cache_hit}, Precomputed: {precomputed}")
                
            except Exception as e:
                end_time = time.time()
                response_time = end_time - start_time
                print(f"  Attempt {i+1}: {response_time:.3f}s - ERROR: {e}")
            
            time.sleep(0.5)  # Brief pause between attempts

def test_cache_performance():
    """Test cache performance specifically"""
    api_base = "https://bhiv-hr-gateway.onrender.com"
    api_key = "myverysecureapikey123"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    print("\n" + "=" * 50)
    print("Testing Cache Performance")
    print("=" * 50)
    
    # Clear cache first
    try:
        response = requests.post(f"{api_base}/v1/match/cache-clear", headers=headers)
        print(f"Cache cleared: {response.status_code}")
    except Exception as e:
        print(f"Cache clear failed: {e}")
    
    # Test same query multiple times
    endpoint = "/v1/match/1/top"
    
    print(f"\nTesting repeated calls to {endpoint}:")
    
    for i in range(5):
        start_time = time.time()
        
        try:
            response = requests.get(f"{api_base}{endpoint}", headers=headers, timeout=30)
            end_time = time.time()
            response_time = end_time - start_time
            
            if response.status_code == 200:
                data = response.json()
                cache_hit = data.get("cache_hit", False)
                precomputed = data.get("precomputed", False)
                processing_time = data.get("processing_time", "unknown")
                
                print(f"  Call {i+1}: {response_time:.3f}s - Cache: {cache_hit}, Precomputed: {precomputed}, Processing: {processing_time}")
            else:
                print(f"  Call {i+1}: {response_time:.3f}s - Status: {response.status_code}")
                
        except Exception as e:
            end_time = time.time()
            response_time = end_time - start_time
            print(f"  Call {i+1}: {response_time:.3f}s - ERROR: {e}")
        
        time.sleep(0.2)

def main():
    print("API RESPONSE TIME ANALYSIS")
    print("=" * 50)
    print(f"Test started at: {datetime.now()}")
    
    test_single_api_call()
    test_cache_performance()
    
    print("\n" + "=" * 50)
    print("ANALYSIS COMPLETE")
    print("=" * 50)

if __name__ == "__main__":
    main()