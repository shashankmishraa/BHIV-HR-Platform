#!/usr/bin/env python3
"""
Simple Candidate Portal Testing
Tests candidate portal functionality without Unicode characters
"""

import psycopg2
import bcrypt
import requests
import json
from datetime import datetime
import uuid

# Database connection
DATABASE_URL = "postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu"
GATEWAY_URL = "https://bhiv-hr-gateway-46pz.onrender.com"

def check_database_schema():
    """Check database schema for candidates table"""
    print("Checking Database Schema...")
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Check candidates table structure
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'candidates'
            ORDER BY ordinal_position
        """)
        
        columns = cursor.fetchall()
        print(f"Candidates table has {len(columns)} columns:")
        
        for column in columns:
            print(f"  - {column[0]} ({column[1]}) {'NULL' if column[2] == 'YES' else 'NOT NULL'}")
        
        cursor.close()
        conn.close()
        return columns
        
    except Exception as e:
        print(f"Schema check failed: {e}")
        return None

def test_candidate_registration():
    """Test candidate registration through API"""
    print("\nTesting Candidate Registration...")
    
    # Generate unique test data
    unique_id = str(uuid.uuid4())[:8]
    test_data = {
        "name": f"Test Candidate {unique_id}",
        "email": f"test.{unique_id}@example.com",
        "password": f"TestPass123!{unique_id}",
        "phone": f"+1-555-{unique_id[:4]}",
        "location": f"Test City {unique_id[:4]}",
        "experience_years": 3,
        "technical_skills": "Python, JavaScript, React, SQL",
        "education_level": "Bachelor's",
        "seniority_level": "Mid"
    }
    
    try:
        response = requests.post(
            f"{GATEWAY_URL}/v1/candidate/register",
            json=test_data,
            timeout=15
        )
        
        print(f"Registration API Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Registration Response: {data}")
            
            if data.get("success"):
                candidate_id = data.get("candidate_id")
                print(f"SUCCESS: Candidate registered with ID {candidate_id}")
                return candidate_id, test_data
            else:
                print(f"FAILED: {data.get('error')}")
                return None, None
        else:
            print(f"FAILED: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return None, None
            
    except Exception as e:
        print(f"Registration test failed: {e}")
        return None, None

def test_candidate_login(test_data):
    """Test candidate login"""
    print("\nTesting Candidate Login...")
    
    try:
        login_data = {
            "email": test_data["email"],
            "password": test_data["password"]
        }
        
        response = requests.post(
            f"{GATEWAY_URL}/v1/candidate/login",
            json=login_data,
            timeout=15
        )
        
        print(f"Login API Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Login Response: {data}")
            
            if data.get("success"):
                token = data.get("token")
                candidate = data.get("candidate", {})
                print(f"SUCCESS: Login successful")
                print(f"Token present: {'Yes' if token else 'No'}")
                print(f"Candidate data: {candidate}")
                return token, candidate
            else:
                print(f"FAILED: {data.get('error')}")
                return None, None
        else:
            print(f"FAILED: HTTP {response.status_code}")
            return None, None
            
    except Exception as e:
        print(f"Login test failed: {e}")
        return None, None

def verify_database_data(candidate_id):
    """Verify data in database"""
    print(f"\nVerifying Database Data for Candidate ID {candidate_id}...")
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, email, phone, location, experience_years, 
                   technical_skills, education_level, seniority_level, status, created_at
            FROM candidates WHERE id = %s
        """, (candidate_id,))
        
        result = cursor.fetchone()
        
        if result:
            print("Database verification SUCCESS:")
            print(f"  ID: {result[0]}")
            print(f"  Name: {result[1]}")
            print(f"  Email: {result[2]}")
            print(f"  Phone: {result[3]}")
            print(f"  Location: {result[4]}")
            print(f"  Experience: {result[5]} years")
            print(f"  Skills: {result[6]}")
            print(f"  Education: {result[7]}")
            print(f"  Seniority: {result[8]}")
            print(f"  Status: {result[9]}")
            print(f"  Created: {result[10]}")
            
            cursor.close()
            conn.close()
            return True
        else:
            print("Database verification FAILED: No data found")
            cursor.close()
            conn.close()
            return False
            
    except Exception as e:
        print(f"Database verification failed: {e}")
        return False

def test_jobs_api():
    """Test jobs API"""
    print("\nTesting Jobs API...")
    
    try:
        response = requests.get(f"{GATEWAY_URL}/v1/jobs", timeout=10)
        
        print(f"Jobs API Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            jobs = data.get("jobs", [])
            print(f"SUCCESS: Found {len(jobs)} jobs")
            
            if jobs:
                print("Sample jobs:")
                for i, job in enumerate(jobs[:3]):
                    print(f"  {i+1}. {job.get('title')} - {job.get('department')} - {job.get('location')}")
            
            return jobs
        else:
            print(f"FAILED: HTTP {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Jobs API test failed: {e}")
        return []

def main():
    """Run all tests"""
    print("BHIV HR Platform - Candidate Portal Testing")
    print("=" * 50)
    
    # Test 1: Check database schema
    schema = check_database_schema()
    if not schema:
        print("Cannot proceed without database schema")
        return
    
    # Test 2: Registration
    candidate_id, test_data = test_candidate_registration()
    if not candidate_id:
        print("Registration failed - cannot proceed with other tests")
        return
    
    # Test 3: Database verification
    db_verified = verify_database_data(candidate_id)
    
    # Test 4: Login
    token, candidate_data = test_candidate_login(test_data)
    
    # Test 5: Jobs API
    jobs = test_jobs_api()
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    tests = [
        ("Database Schema Check", schema is not None),
        ("Candidate Registration", candidate_id is not None),
        ("Database Data Verification", db_verified),
        ("Candidate Login", token is not None),
        ("Jobs API", len(jobs) > 0)
    ]
    
    passed = 0
    for test_name, result in tests:
        status = "PASS" if result else "FAIL"
        print(f"{status} | {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("\nAll tests PASSED!")
        print("Candidate Portal is working correctly")
        print("Values are properly stored in database")
        print("Pipeline is functioning as expected")
    else:
        print("\nSome tests FAILED!")
        print("Check the output above for details")

if __name__ == "__main__":
    main()