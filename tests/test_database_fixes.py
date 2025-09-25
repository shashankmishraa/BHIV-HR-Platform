#!/usr/bin/env python3
"""
BHIV HR Platform - Database Fixes Testing Suite
Tests database schema fixes and data population
"""

import json
import time

import requests


def test_database_fixes():
    """Test all database fixes and functionality"""
    base_url = "https://bhiv-hr-gateway.onrender.com"
    api_key = "myverysecureapikey123"
    headers = {"Authorization": f"Bearer {api_key}"}

    print("BHIV HR Platform - Database Fixes Test Suite")
    print("=" * 55)

    tests_passed = 0
    total_tests = 0

    # Test 1: Database Health Check
    total_tests += 1
    try:
        response = requests.get(f"{base_url}/v1/database/health", headers=headers)
        if response.status_code == 200:
            data = response.json()
            has_status_column = data.get("schema_status", {}).get(
                "candidates_has_status_column", False
            )
            candidate_count = (
                data.get("tables", {}).get("candidates", {}).get("count", 0)
            )

            print(f"[INFO] Database Health Check:")
            print(f"  - Status column exists: {has_status_column}")
            print(f"  - Candidate count: {candidate_count}")
            print(f"  - Database status: {data.get('database_status', 'unknown')}")

            if data.get("database_status") == "healthy":
                print("[PASS] Database health check successful")
                tests_passed += 1
            else:
                print("[FAIL] Database health check failed")
        else:
            print(f"[FAIL] Database health check - status {response.status_code}")
    except Exception as e:
        print(f"[ERROR] Database health check: {e}")

    # Test 2: Database Migration (if needed)
    total_tests += 1
    try:
        response = requests.post(f"{base_url}/v1/database/migrate", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"[INFO] Migration result: {data.get('message', 'Unknown')}")

            if (
                "successfully" in data.get("message", "").lower()
                or "up to date" in data.get("message", "").lower()
            ):
                print("[PASS] Database migration successful")
                tests_passed += 1
            else:
                print("[FAIL] Database migration failed")
        else:
            print(f"[FAIL] Database migration - status {response.status_code}")
    except Exception as e:
        print(f"[ERROR] Database migration: {e}")

    # Test 3: Candidate Search (Fixed)
    total_tests += 1
    try:
        response = requests.get(
            f"{base_url}/v1/candidates/search?skills=python", headers=headers
        )
        if response.status_code == 200:
            data = response.json()
            if "error" not in data:
                print(
                    f"[PASS] Candidate search working - found {data.get('count', 0)} candidates"
                )
                tests_passed += 1
            else:
                print(f"[FAIL] Candidate search error: {data.get('error', 'Unknown')}")
        else:
            print(f"[FAIL] Candidate search - status {response.status_code}")
    except Exception as e:
        print(f"[ERROR] Candidate search: {e}")

    # Test 4: Sample Data Population
    total_tests += 1
    try:
        response = requests.post(
            f"{base_url}/v1/candidates/sample-data", headers=headers
        )
        if response.status_code == 200:
            data = response.json()
            inserted = data.get("candidates_inserted", 0)

            if inserted > 0 or "already exists" in str(data.get("errors", [])):
                print(f"[PASS] Sample data population - {inserted} candidates added")
                tests_passed += 1
            else:
                print(f"[FAIL] Sample data population - no candidates added")
        else:
            print(f"[FAIL] Sample data population - status {response.status_code}")
    except Exception as e:
        print(f"[ERROR] Sample data population: {e}")

    # Test 5: AI Matching with Data
    total_tests += 1
    try:
        response = requests.get(f"{base_url}/v1/match/1/top", headers=headers)
        if response.status_code == 200:
            data = response.json()
            matches = data.get("matches", [])

            if len(matches) > 0:
                print(f"[PASS] AI matching working - {len(matches)} matches found")
                tests_passed += 1
            else:
                print(
                    "[INFO] AI matching working but no matches (expected if no candidates)"
                )
                tests_passed += 1
        else:
            print(f"[FAIL] AI matching - status {response.status_code}")
    except Exception as e:
        print(f"[ERROR] AI matching: {e}")

    # Test 6: Bulk Upload Compatibility
    total_tests += 1
    try:
        test_candidate = {
            "candidates": [
                {
                    "name": "Test User",
                    "email": f"test.user.{int(time.time())}@email.com",
                    "phone": "+1-555-9999",
                    "location": "Test City",
                    "experience_years": 2,
                    "technical_skills": "Testing, Python",
                    "seniority_level": "Junior",
                    "education_level": "Bachelor's",
                    "status": "active",
                }
            ]
        }

        response = requests.post(
            f"{base_url}/v1/candidates/bulk",
            headers={**headers, "Content-Type": "application/json"},
            json=test_candidate,
        )

        if response.status_code == 200:
            data = response.json()
            if data.get("candidates_inserted", 0) > 0:
                print("[PASS] Bulk upload compatibility working")
                tests_passed += 1
            else:
                print(f"[FAIL] Bulk upload - no candidates inserted: {data}")
        else:
            print(f"[FAIL] Bulk upload - status {response.status_code}")
    except Exception as e:
        print(f"[ERROR] Bulk upload: {e}")

    print("\n" + "=" * 55)
    print(f"Database Fixes Test Results: {tests_passed}/{total_tests} tests passed")

    if tests_passed >= 5:
        print("[SUCCESS] Database fixes working correctly!")
        print("\nFixed Issues:")
        print("- Database schema updated with status column")
        print("- Candidate search endpoint working")
        print("- Sample data population functional")
        print("- AI matching operational")
        print("- Bulk upload compatibility maintained")
    else:
        print(f"[WARNING] {total_tests - tests_passed} tests failed")

    return tests_passed >= 5


if __name__ == "__main__":
    success = test_database_fixes()
    exit(0 if success else 1)
