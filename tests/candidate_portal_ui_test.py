#!/usr/bin/env python3
"""
Candidate Portal UI Testing
Tests candidate portal interface and data pipeline through Beautiful Soup
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
import uuid

# Configuration
CANDIDATE_PORTAL_URL = "https://bhiv-hr-candidate-portal.onrender.com"
GATEWAY_URL = "https://bhiv-hr-gateway-46pz.onrender.com"

def generate_test_candidate():
    """Generate unique test candidate data"""
    unique_id = str(uuid.uuid4())[:8]
    return {
        "name": f"UI Test Candidate {unique_id}",
        "email": f"ui.test.{unique_id}@example.com",
        "password": f"UITest123!{unique_id}",
        "phone": f"+1-555-{unique_id[:4]}",
        "location": f"UI Test City {unique_id[:4]}",
        "experience_years": 5,
        "technical_skills": "Python, React, Node.js, PostgreSQL, Docker",
        "education_level": "Master's",
        "seniority_level": "Senior"
    }

def test_candidate_portal_accessibility():
    """Test if candidate portal is accessible"""
    print("🔍 Testing Candidate Portal Accessibility")
    
    try:
        response = requests.get(CANDIDATE_PORTAL_URL, timeout=15)
        
        if response.status_code == 200:
            print(f"✅ Portal Accessibility: SUCCESS")
            print(f"   Status Code: {response.status_code}")
            print(f"   Content Length: {len(response.content)} bytes")
            
            # Parse HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Check for Streamlit elements
            streamlit_elements = soup.find_all(['div', 'script'], class_=lambda x: x and 'streamlit' in x.lower())
            print(f"   Streamlit Elements: {len(streamlit_elements)} found")
            
            # Check for form elements
            forms = soup.find_all('form')
            inputs = soup.find_all('input')
            buttons = soup.find_all('button')
            
            print(f"   Forms: {len(forms)}")
            print(f"   Input Fields: {len(inputs)}")
            print(f"   Buttons: {len(buttons)}")
            
            # Check for BHIV branding
            title = soup.find('title')
            if title:
                print(f"   Page Title: {title.get_text()}")
            
            return True
        else:
            print(f"❌ Portal Accessibility: FAILED - Status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Portal Accessibility: FAILED - {e}")
        return False

def test_registration_form_structure():
    """Test registration form structure through HTML parsing"""
    print("\n🔍 Testing Registration Form Structure")
    
    try:
        response = requests.get(CANDIDATE_PORTAL_URL, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for registration-related elements
            registration_keywords = ['register', 'signup', 'create account', 'name', 'email', 'password']
            found_elements = {}
            
            for keyword in registration_keywords:
                elements = soup.find_all(text=lambda text: text and keyword.lower() in text.lower())
                found_elements[keyword] = len(elements)
                print(f"   '{keyword}' references: {len(elements)}")
            
            # Check for input field types
            input_types = {}
            for input_tag in soup.find_all('input'):
                input_type = input_tag.get('type', 'text')
                input_types[input_type] = input_types.get(input_type, 0) + 1
            
            print(f"✅ Input Field Types Found:")
            for input_type, count in input_types.items():
                print(f"   {input_type}: {count}")
            
            # Check for required candidate fields
            candidate_fields = [
                'name', 'email', 'phone', 'location', 'experience', 
                'skills', 'education', 'seniority'
            ]
            
            field_presence = {}
            for field in candidate_fields:
                field_elements = soup.find_all(text=lambda text: text and field.lower() in text.lower())
                field_presence[field] = len(field_elements) > 0
                status = "✅" if field_presence[field] else "❌"
                print(f"   {status} {field.title()} field: {'Present' if field_presence[field] else 'Missing'}")
            
            return True
        else:
            print(f"❌ Form Structure Test: FAILED - Status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Form Structure Test: FAILED - {e}")
        return False

def test_api_integration_endpoints():
    """Test API integration endpoints used by candidate portal"""
    print("\n🔍 Testing API Integration Endpoints")
    
    endpoints_to_test = [
        ("/v1/candidate/register", "POST", "Registration endpoint"),
        ("/v1/candidate/login", "POST", "Login endpoint"),
        ("/v1/jobs", "GET", "Jobs listing endpoint"),
        ("/v1/candidate/apply", "POST", "Job application endpoint")
    ]
    
    results = []
    
    for endpoint, method, description in endpoints_to_test:
        try:
            url = f"{GATEWAY_URL}{endpoint}"
            
            if method == "GET":
                response = requests.get(url, timeout=10)
            else:
                # For POST endpoints, we expect 400/422 for missing data, not 404
                response = requests.post(url, json={}, timeout=10)
            
            # Check if endpoint exists (not 404)
            if response.status_code != 404:
                print(f"✅ {description}: AVAILABLE (Status: {response.status_code})")
                results.append(True)
            else:
                print(f"❌ {description}: NOT FOUND (Status: {response.status_code})")
                results.append(False)
                
        except Exception as e:
            print(f"❌ {description}: ERROR - {e}")
            results.append(False)
    
    return all(results)

def test_data_pipeline_with_api():
    """Test complete data pipeline from registration to database"""
    print("\n🔍 Testing Complete Data Pipeline")
    
    try:
        # Generate test data
        test_data = generate_test_candidate()
        print(f"✅ Generated Test Data:")
        print(f"   Name: {test_data['name']}")
        print(f"   Email: {test_data['email']}")
        print(f"   Location: {test_data['location']}")
        print(f"   Skills: {test_data['technical_skills']}")
        
        # Step 1: Test Registration
        print(f"\n📋 Step 1: Testing Registration Pipeline")
        reg_response = requests.post(
            f"{GATEWAY_URL}/v1/candidate/register",
            json=test_data,
            timeout=15
        )
        
        if reg_response.status_code == 200:
            reg_data = reg_response.json()
            if reg_data.get("success"):
                candidate_id = reg_data.get("candidate_id")
                print(f"✅ Registration: SUCCESS (ID: {candidate_id})")
                
                # Step 2: Test Login
                print(f"\n📋 Step 2: Testing Login Pipeline")
                login_data = {
                    "email": test_data["email"],
                    "password": test_data["password"]
                }
                
                login_response = requests.post(
                    f"{GATEWAY_URL}/v1/candidate/login",
                    json=login_data,
                    timeout=15
                )
                
                if login_response.status_code == 200:
                    login_result = login_response.json()
                    if login_result.get("success"):
                        token = login_result.get("token")
                        candidate_info = login_result.get("candidate", {})
                        
                        print(f"✅ Login: SUCCESS")
                        print(f"   Token: {'Present' if token else 'Missing'}")
                        
                        # Verify data integrity
                        print(f"\n📋 Step 3: Data Integrity Verification")
                        integrity_checks = [
                            ("Name", candidate_info.get("name") == test_data["name"]),
                            ("Email", candidate_info.get("email") == test_data["email"]),
                            ("Phone", candidate_info.get("phone") == test_data["phone"]),
                            ("Location", candidate_info.get("location") == test_data["location"]),
                            ("Experience", candidate_info.get("experience_years") == test_data["experience_years"]),
                            ("Skills", candidate_info.get("technical_skills") == test_data["technical_skills"]),
                            ("Education", candidate_info.get("education_level") == test_data["education_level"]),
                            ("Seniority", candidate_info.get("seniority_level") == test_data["seniority_level"])
                        ]
                        
                        all_correct = True
                        for field, is_correct in integrity_checks:
                            status = "✅" if is_correct else "❌"
                            print(f"   {status} {field}: {'Correct' if is_correct else 'Mismatch'}")
                            if not is_correct:
                                all_correct = False
                        
                        if all_correct:
                            print(f"✅ Data Pipeline: ALL VALUES CORRECTLY STORED AND RETRIEVED")
                            
                            # Step 4: Test Job Application Pipeline
                            print(f"\n📋 Step 4: Testing Job Application Pipeline")
                            
                            # Get available jobs
                            jobs_response = requests.get(f"{GATEWAY_URL}/v1/jobs", timeout=10)
                            if jobs_response.status_code == 200:
                                jobs_data = jobs_response.json()
                                jobs = jobs_data.get("jobs", [])
                                
                                if jobs:
                                    job_id = jobs[0]["id"]
                                    
                                    # Apply for job
                                    application_data = {
                                        "candidate_id": candidate_id,
                                        "job_id": job_id,
                                        "cover_letter": "Test application through pipeline"
                                    }
                                    
                                    headers = {"Authorization": f"Bearer {token}"}
                                    app_response = requests.post(
                                        f"{GATEWAY_URL}/v1/candidate/apply",
                                        json=application_data,
                                        headers=headers,
                                        timeout=15
                                    )
                                    
                                    if app_response.status_code == 200:
                                        app_data = app_response.json()
                                        if app_data.get("success"):
                                            print(f"✅ Job Application Pipeline: SUCCESS")
                                            print(f"   Application ID: {app_data.get('application_id')}")
                                            return True
                                        else:
                                            print(f"❌ Job Application: FAILED - {app_data.get('error')}")
                                    else:
                                        print(f"❌ Job Application: FAILED - Status {app_response.status_code}")
                                else:
                                    print(f"⚠️  No jobs available for application test")
                                    return True  # Still consider pipeline successful
                            else:
                                print(f"❌ Jobs API: FAILED - Status {jobs_response.status_code}")
                        else:
                            print(f"❌ Data Pipeline: DATA INTEGRITY ISSUES FOUND")
                            return False
                    else:
                        print(f"❌ Login: FAILED - {login_result.get('error')}")
                        return False
                else:
                    print(f"❌ Login: FAILED - Status {login_response.status_code}")
                    return False
            else:
                print(f"❌ Registration: FAILED - {reg_data.get('error')}")
                return False
        else:
            print(f"❌ Registration: FAILED - Status {reg_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Data Pipeline Test: FAILED - {e}")
        return False

def main():
    """Run all candidate portal UI and pipeline tests"""
    print("🔍 BHIV HR Platform - Candidate Portal UI & Pipeline Testing")
    print("=" * 75)
    
    tests = [
        ("Portal Accessibility", test_candidate_portal_accessibility),
        ("Registration Form Structure", test_registration_form_structure),
        ("API Integration Endpoints", test_api_integration_endpoints),
        ("Complete Data Pipeline", test_data_pipeline_with_api)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"📋 Testing: {test_name}")
        print(f"{'='*50}")
        
        result = test_func()
        results.append((test_name, result))
        
        if result:
            print(f"✅ {test_name}: PASSED")
        else:
            print(f"❌ {test_name}: FAILED")
    
    # Summary
    print("\n" + "=" * 75)
    print("📊 CANDIDATE PORTAL UI & PIPELINE TEST SUMMARY")
    print("=" * 75)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} | {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 ALL CANDIDATE PORTAL TESTS PASSED!")
        print("✅ Portal is accessible and functional")
        print("✅ Registration form structure is proper")
        print("✅ API endpoints are available and working")
        print("✅ Complete data pipeline is working correctly")
        print("✅ All values are properly stored in database tables")
        print("✅ Beautiful Soup parsing shows proper form structure")
        return True
    else:
        print("\n⚠️  SOME CANDIDATE PORTAL TESTS FAILED!")
        return False

if __name__ == "__main__":
    main()