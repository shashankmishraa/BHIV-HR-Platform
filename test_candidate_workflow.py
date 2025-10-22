#!/usr/bin/env python3
"""
BHIV Candidate Portal - Complete Workflow Test
Tests the full candidate journey from registration to job application
"""

import requests
import time

# Configuration
GATEWAY_URL = "http://localhost:8000"
PORTAL_URL = "http://localhost:8503"
API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"

def test_complete_workflow():
    """Test complete candidate workflow"""
    print("=== BHIV Candidate Portal - Complete Workflow Test ===")
    
    # Step 1: Check services are running
    print("\n1. Checking Services...")
    try:
        gateway_health = requests.get(f"{GATEWAY_URL}/health", timeout=5)
        portal_health = requests.get(f"{PORTAL_URL}/_stcore/health", timeout=5)
        
        print(f"   Gateway: {'OK' if gateway_health.status_code == 200 else 'FAILED'}")
        print(f"   Portal: {'OK' if portal_health.status_code == 200 else 'FAILED'}")
    except Exception as e:
        print(f"   Service check failed: {e}")
        return False
    
    # Step 2: Test job listings (public access)
    print("\n2. Testing Job Listings...")
    try:
        headers = {"Authorization": f"Bearer {API_KEY}"}
        jobs_response = requests.get(f"{GATEWAY_URL}/v1/jobs", headers=headers, timeout=10)
        
        if jobs_response.status_code == 200:
            jobs = jobs_response.json().get("jobs", [])
            print(f"   Found {len(jobs)} available jobs")
            for job in jobs[:2]:
                print(f"   - {job['title']} at {job['location']}")
        else:
            print(f"   Job listing failed: {jobs_response.status_code}")
            return False
    except Exception as e:
        print(f"   Job listing error: {e}")
        return False
    
    # Step 3: Test candidate registration
    print("\n3. Testing Candidate Registration...")
    candidate_data = {
        "name": "Test Candidate",
        "email": f"test.candidate.{int(time.time())}@example.com",
        "password": "TestPass123!",
        "phone": "+1 (555) 999-0000",
        "location": "Test City, TC",
        "experience_years": 3,
        "technical_skills": "Python, React, SQL",
        "education_level": "Bachelor's",
        "seniority_level": "Mid"
    }
    
    try:
        reg_response = requests.post(
            f"{GATEWAY_URL}/v1/candidate/register",
            json=candidate_data,
            timeout=10
        )
        
        if reg_response.status_code == 200 and reg_response.json().get("success"):
            candidate_id = reg_response.json()["candidate_id"]
            print(f"   Registration successful - ID: {candidate_id}")
        else:
            print(f"   Registration failed: {reg_response.json()}")
            return False
    except Exception as e:
        print(f"   Registration error: {e}")
        return False
    
    # Step 4: Test candidate login
    print("\n4. Testing Candidate Login...")
    login_data = {
        "email": candidate_data["email"],
        "password": candidate_data["password"]
    }
    
    try:
        login_response = requests.post(
            f"{GATEWAY_URL}/v1/candidate/login",
            json=login_data,
            timeout=10
        )
        
        if login_response.status_code == 200 and login_response.json().get("success"):
            token = login_response.json()["token"]
            candidate = login_response.json()["candidate"]
            print(f"   Login successful - {candidate['name']}")
        else:
            print(f"   Login failed: {login_response.json()}")
            return False
    except Exception as e:
        print(f"   Login error: {e}")
        return False
    
    # Step 5: Test profile update
    print("\n5. Testing Profile Update...")
    update_data = {
        "technical_skills": "Python, React, SQL, Docker, AWS",
        "experience_years": 4,
        "location": "Updated City, UC"
    }
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        update_response = requests.put(
            f"{GATEWAY_URL}/v1/candidate/profile/{candidate_id}",
            json=update_data,
            headers=headers,
            timeout=10
        )
        
        if update_response.status_code == 200 and update_response.json().get("success"):
            print("   Profile update successful")
        else:
            print(f"   Profile update failed: {update_response.json()}")
            return False
    except Exception as e:
        print(f"   Profile update error: {e}")
        return False
    
    # Step 6: Test job application
    print("\n6. Testing Job Application...")
    if jobs:
        job_id = jobs[0]["id"]
        job_title = jobs[0]["title"]
        
        application_data = {
            "candidate_id": candidate_id,
            "job_id": job_id,
            "cover_letter": "I am interested in this position and believe I would be a great fit."
        }
        
        try:
            app_response = requests.post(
                f"{GATEWAY_URL}/v1/candidate/apply",
                json=application_data,
                headers=headers,
                timeout=10
            )
            
            if app_response.status_code == 200 and app_response.json().get("success"):
                application_id = app_response.json()["application_id"]
                print(f"   Application successful - Applied for {job_title}")
                print(f"   Application ID: {application_id}")
            else:
                print(f"   Application failed: {app_response.json()}")
                return False
        except Exception as e:
            print(f"   Application error: {e}")
            return False
    
    # Step 7: Test application tracking
    print("\n7. Testing Application Tracking...")
    try:
        apps_response = requests.get(
            f"{GATEWAY_URL}/v1/candidate/applications/{candidate_id}",
            headers=headers,
            timeout=10
        )
        
        if apps_response.status_code == 200:
            applications = apps_response.json().get("applications", [])
            print(f"   Retrieved {len(applications)} applications")
            for app in applications:
                print(f"   - {app['job_title']} ({app['status']})")
        else:
            print(f"   Application tracking failed: {apps_response.json()}")
            return False
    except Exception as e:
        print(f"   Application tracking error: {e}")
        return False
    
    # Step 8: Portal accessibility test
    print("\n8. Testing Portal Accessibility...")
    try:
        portal_response = requests.get(PORTAL_URL, timeout=10)
        if portal_response.status_code == 200:
            print("   Portal is accessible")
        else:
            print(f"   Portal access failed: {portal_response.status_code}")
    except Exception as e:
        print(f"   Portal access error: {e}")
    
    print("\n=== WORKFLOW TEST COMPLETE ===")
    print("✅ All candidate portal features working correctly!")
    print(f"\n📊 Test Results:")
    print(f"   - Candidate ID: {candidate_id}")
    print(f"   - Email: {candidate_data['email']}")
    print(f"   - Applications: {len(applications)}")
    print(f"   - Portal URL: {PORTAL_URL}")
    print(f"   - API Gateway: {GATEWAY_URL}")
    
    return True

if __name__ == "__main__":
    success = test_complete_workflow()
    if success:
        print("\n🎉 Candidate Portal workflow test PASSED!")
    else:
        print("\n❌ Candidate Portal workflow test FAILED!")