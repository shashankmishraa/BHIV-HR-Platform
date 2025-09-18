#!/usr/bin/env python3
"""
Test Real Data Implementation
Verify the AI matching system uses real candidate data
"""

import requests
import time
from datetime import datetime

def test_real_data_implementation():
    """Test that AI matching returns real candidate data"""
    
    # Test different scenarios
    test_cases = [
        {"job_id": 1, "limit": 5, "description": "Job ID 1 with 5 candidates"},
        {"job_id": 2, "limit": 10, "description": "Job ID 2 with 10 candidates"},
        {"job_id": 5, "limit": 3, "description": "Job ID 5 with 3 candidates"},
        {"job_id": 10, "limit": 8, "description": "Job ID 10 with 8 candidates"}
    ]
    
    print("TESTING REAL DATA IMPLEMENTATION")
    print("=" * 50)
    
    api_base = "https://bhiv-hr-gateway.onrender.com"
    headers = {"Authorization": "Bearer myverysecureapikey123"}
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['description']}")
        print("-" * 30)
        
        try:
            response = requests.get(
                f"{api_base}/v1/match/{test_case['job_id']}/top?limit={test_case['limit']}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check for real data indicators
                matches = data.get("matches", [])
                algorithm_version = data.get("algorithm_version", "")
                cache_hit = data.get("cache_hit", False)
                
                print(f"✓ Status: {response.status_code}")
                print(f"✓ Candidates returned: {len(matches)}")
                print(f"✓ Algorithm version: {algorithm_version}")
                print(f"✓ Cache hit: {cache_hit}")
                
                # Analyze candidate data quality
                if matches:
                    first_candidate = matches[0]
                    print(f"✓ First candidate: {first_candidate.get('name', 'N/A')}")
                    print(f"✓ Email: {first_candidate.get('email', 'N/A')}")
                    print(f"✓ Score: {first_candidate.get('score', 'N/A')}")
                    
                    # Check if it's fake pre-computed data
                    is_fake = (
                        first_candidate.get('name', '').startswith('Candidate ') or
                        first_candidate.get('email', '').startswith('candidate') and '@example.com' in first_candidate.get('email', '')
                    )
                    
                    if is_fake:
                        print("⚠️  WARNING: Still using fake pre-computed data")
                    else:
                        print("✓ Real candidate data detected")
                else:
                    print("⚠️  No candidates returned")
                    
            else:
                print(f"✗ Error: HTTP {response.status_code}")
                print(f"✗ Response: {response.text}")
                
        except Exception as e:
            print(f"✗ Exception: {e}")
        
        time.sleep(1)  # Brief pause between tests
    
    print("\n" + "=" * 50)
    print("REAL DATA IMPLEMENTATION TEST COMPLETE")

def test_cache_functionality():
    """Test caching functionality"""
    print("\nTESTING CACHE FUNCTIONALITY")
    print("=" * 30)
    
    api_base = "https://bhiv-hr-gateway.onrender.com"
    headers = {"Authorization": "Bearer myverysecureapikey123"}
    
    # Test same request multiple times to check caching
    endpoint = f"{api_base}/v1/match/1/top?limit=5"
    
    for i in range(3):
        print(f"\nRequest {i+1}:")
        try:
            start_time = time.time()
            response = requests.get(endpoint, headers=headers, timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                cache_hit = data.get("cache_hit", False)
                processing_time = data.get("processing_time", "unknown")
                
                print(f"  Response time: {response_time:.3f}s")
                print(f"  Processing time: {processing_time}")
                print(f"  Cache hit: {cache_hit}")
                
                if i == 0:
                    print("  (First request - should be cache miss)")
                else:
                    print("  (Subsequent request - should be cache hit)")
            else:
                print(f"  Error: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"  Exception: {e}")
        
        time.sleep(0.5)

def main():
    """Main test execution"""
    print(f"Test started at: {datetime.now()}")
    
    test_real_data_implementation()
    test_cache_functionality()
    
    print(f"\nTest completed at: {datetime.now()}")

if __name__ == "__main__":
    main()