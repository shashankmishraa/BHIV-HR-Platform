#!/usr/bin/env python3
"""
BHIV HR Platform - Edge Cases Testing
Tests edge cases and error conditions
"""

import requests
import json

API_BASE = "http://localhost:8000"
API_KEY = "myverysecureapikey123"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}


def test_empty_candidates_list():
    """Test bulk upload with empty candidates list"""
    print("Testing Empty Candidates List Validation...")

    # Test with empty list
    empty_data = {"candidates": []}

    try:
        response = requests.post(
            f"{API_BASE}/v1/candidates/bulk",
            headers=HEADERS,
            json=empty_data,
            timeout=10,
        )
        if response.status_code == 400:
            result = response.json()
            if "Candidates list cannot be empty" in result.get("detail", ""):
                print("  Empty candidates list: PASSED - Correctly returns 400")
                return True
            else:
                print(
                    f"  Empty candidates list: FAILED - Wrong error message: {result.get('detail')}"
                )
                return False
        else:
            print(
                f"  Empty candidates list: FAILED - Expected 400, got {response.status_code}"
            )
            return False
    except Exception as e:
        print(f"  Empty candidates list: FAILED - {str(e)}")
        return False


def test_interview_field_names():
    """Test interview creation with correct field names"""
    print("Testing Interview Field Names...")

    # Test with correct field name (interview_date)
    interview_data = {
        "candidate_id": 1,
        "job_id": 1,
        "interview_date": "2025-02-01T10:00:00Z",
        "interviewer": "Test Interviewer",
        "notes": "Test interview",
    }

    try:
        response = requests.post(
            f"{API_BASE}/v1/interviews",
            headers=HEADERS,
            json=interview_data,
            timeout=10,
        )
        if response.status_code == 200:
            result = response.json()
            print(
                f"  Interview creation: PASSED - Created interview ID {result.get('interview_id')}"
            )
            return True
        else:
            print(f"  Interview creation: FAILED - Status {response.status_code}")
            print(f"    Response: {response.text}")
            return False
    except Exception as e:
        print(f"  Interview creation: FAILED - {str(e)}")
        return False


def main():
    """Run edge case tests"""
    print("BHIV HR Platform - Edge Cases Testing")
    print("=" * 50)

    results = []
    results.append(("Empty Candidates List", test_empty_candidates_list()))
    results.append(("Interview Field Names", test_interview_field_names()))

    print("\n" + "=" * 50)
    print("EDGE CASES TEST SUMMARY")
    print("=" * 50)

    passed = 0
    for test_name, result in results:
        status = "PASSED" if result else "FAILED"
        print(f"{test_name:<25}: {status}")
        if result:
            passed += 1

    print(f"\nOverall: {passed}/{len(results)} edge case tests passed")

    if passed == len(results):
        print("SUCCESS: All edge cases handled correctly!")
    else:
        print("WARNING: Some edge cases need attention")


if __name__ == "__main__":
    main()
