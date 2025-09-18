#!/usr/bin/env python3
"""
Simple Test for Real Data Implementation
"""

import requests
import json

def test_ai_matching():
    """Test AI matching endpoint"""
    
    print("TESTING AI MATCHING IMPLEMENTATION")
    print("=" * 50)
    
    api_base = "https://bhiv-hr-gateway.onrender.com"
    headers = {"Authorization": "Bearer myverysecureapikey123"}
    
    # Test different job IDs
    test_jobs = [1, 2, 5, 10]
    
    for job_id in test_jobs:
        print(f"\nTesting Job ID {job_id}:")
        
        try:
            response = requests.get(
                f"{api_base}/v1/match/{job_id}/top?limit=5",
                headers=headers,
                timeout=10
            )
            
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                matches = data.get("matches", [])
                algorithm_version = data.get("algorithm_version", "")
                
                print(f"  Candidates: {len(matches)}")
                print(f"  Algorithm: {algorithm_version}")
                
                if matches:
                    first = matches[0]
                    name = first.get("name", "N/A")
                    email = first.get("email", "N/A")
                    
                    print(f"  First candidate: {name}")
                    print(f"  Email: {email}")
                    
                    # Check if fake data
                    is_fake = (name.startswith("Candidate ") or 
                              email.startswith("candidate") and "@example.com" in email)
                    
                    if is_fake:
                        print("  WARNING: Fake data detected")
                    else:
                        print("  SUCCESS: Real data detected")
                else:
                    print("  No candidates returned")
            else:
                print(f"  Error: {response.text}")
                
        except Exception as e:
            print(f"  Exception: {str(e)}")

def test_current_system():
    """Test what's currently deployed"""
    
    print("\n\nTESTING CURRENT DEPLOYMENT")
    print("=" * 50)
    
    api_base = "https://bhiv-hr-gateway.onrender.com"
    headers = {"Authorization": "Bearer myverysecureapikey123"}
    
    # Test root endpoint
    try:
        response = requests.get(f"{api_base}/", headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"API Version: {data.get('version', 'unknown')}")
            print(f"Endpoints: {data.get('endpoints', 'unknown')}")
        else:
            print(f"Root endpoint error: {response.status_code}")
    except Exception as e:
        print(f"Root endpoint exception: {e}")
    
    # Test AI matching
    try:
        response = requests.get(f"{api_base}/v1/match/1/top", headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"AI Matching works: {len(data.get('matches', []))} candidates")
            print(f"Current algorithm: {data.get('algorithm_version', 'unknown')}")
        else:
            print(f"AI matching error: {response.status_code}")
    except Exception as e:
        print(f"AI matching exception: {e}")

if __name__ == "__main__":
    test_current_system()
    test_ai_matching()