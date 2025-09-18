#!/usr/bin/env python3
"""
Quick test script to verify the two specific fixes
"""

import requests
import json

API_BASE = "http://localhost:8000"
API_KEY = "myverysecureapikey123"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def test_fix_1_empty_candidates():
    """Test Fix 1: Empty candidates list should return 400"""
    print("Testing Fix 1: Empty Candidates List Validation")
    
    empty_data = {"candidates": []}
    
    try:
        response = requests.post(f"{API_BASE}/v1/candidates/bulk", headers=HEADERS, json=empty_data, timeout=10)
        print(f"  Status Code: {response.status_code}")
        print(f"  Response: {response.json()}")
        
        if response.status_code == 400:
            print("  ✅ FIXED: Correctly returns 400 for empty candidates list")
            return True
        else:
            print(f"  ❌ ISSUE: Expected 400, got {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ ERROR: {str(e)}")
        return False

def test_fix_2_interview_fields():
    """Test Fix 2: Interview creation with correct field names"""
    print("\nTesting Fix 2: Interview Field Names")
    
    interview_data = {
        "candidate_id": 1,
        "job_id": 1,
        "interview_date": "2025-02-01T10:00:00Z",
        "interviewer": "Test Interviewer",
        "notes": "Test interview"
    }
    
    try:
        response = requests.post(f"{API_BASE}/v1/interviews", headers=HEADERS, json=interview_data, timeout=10)
        print(f"  Status Code: {response.status_code}")
        print(f"  Response: {response.json()}")
        
        if response.status_code == 200:
            print("  ✅ FIXED: Interview creation works with correct field names")
            return True
        else:
            print(f"  ❌ ISSUE: Expected 200, got {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ ERROR: {str(e)}")
        return False

def main():
    print("BHIV HR Platform - Fix Verification")
    print("=" * 50)
    
    fix1_result = test_fix_1_empty_candidates()
    fix2_result = test_fix_2_interview_fields()
    
    print("\n" + "=" * 50)
    print("FIX VERIFICATION SUMMARY")
    print("=" * 50)
    
    print(f"Fix 1 - Empty Candidates Validation: {'PASSED' if fix1_result else 'FAILED'}")
    print(f"Fix 2 - Interview Field Names:      {'PASSED' if fix2_result else 'FAILED'}")
    
    if fix1_result and fix2_result:
        print("\n🎉 SUCCESS: Both fixes are working correctly!")
    else:
        print("\n⚠️  WARNING: Some fixes need additional work")

if __name__ == "__main__":
    main()