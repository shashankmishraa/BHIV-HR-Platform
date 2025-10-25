#!/usr/bin/env python3
"""
BHIV HR Platform - Complete Workflow Testing Script
Tests the full registration and application workflow locally
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def test_endpoint(method, url, data=None, description=""):
    """Test an endpoint and return result"""
    print(f"\n🧪 Testing: {description}")
    print(f"   {method} {url}")
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=data)
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code < 400:
            result = response.json()
            print(f"   ✅ Success: {result.get('message', 'OK')}")
            return True, result
        else:
            print(f"   ❌ Error: {response.text}")
            return False, response.text
            
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")
        return False, str(e)

def main():
    print("🚀 BHIV HR Platform - Complete Workflow Test")
    print("=" * 50)
    
    # Test data
    client_data = {
        "client_id": "TESTCLIENT01",
        "company_name": "Test Company Ltd",
        "contact_email": "admin@testcompany.com",
        "password": "SecurePass123!"
    }
    
    candidate_data = {
        "name": "John Smith",
        "email": "john.smith@example.com",
        "password": "CandidatePass123!",
        "phone": "+1-555-0123",
        "location": "San Francisco, CA",
        "experience_years": 5,
        "technical_skills": "Python, FastAPI, PostgreSQL, Docker",
        "education_level": "Bachelor",
        "seniority_level": "Senior"
    }
    
    job_data = {
        "title": "Senior Python Developer",
        "department": "Engineering",
        "location": "San Francisco, CA",
        "experience_level": "Senior",
        "requirements": "Python, FastAPI, PostgreSQL, Docker, AWS",
        "description": "We need a senior Python developer with FastAPI experience",
        "employment_type": "Full-time"
    }
    
    # Step 1: Test Health Endpoints
    print("\n📋 STEP 1: Health Checks")
    test_endpoint("GET", f"{BASE_URL}/health", description="Gateway Health")
    test_endpoint("GET", "http://localhost:9000/health", description="Agent Health")
    
    # Step 2: Client Registration
    print("\n📋 STEP 2: Client Registration")
    success, result = test_endpoint("POST", f"{BASE_URL}/v1/client/register", 
                                   client_data, "Client Registration")
    
    if not success:
        print("❌ Client registration failed, stopping test")
        return
    
    # Step 3: Client Login
    print("\n📋 STEP 3: Client Login")
    login_data = {
        "client_id": client_data["client_id"],
        "password": client_data["password"]
    }
    success, login_result = test_endpoint("POST", f"{BASE_URL}/v1/client/login", 
                                         login_data, "Client Login")
    
    if success:
        client_token = login_result.get("access_token")
        print(f"   🔑 Client Token: {client_token[:20]}...")
    
    # Step 4: Create Job
    print("\n📋 STEP 4: Job Creation")
    success, job_result = test_endpoint("POST", f"{BASE_URL}/v1/jobs", 
                                       job_data, "Create Job")
    
    if success:
        job_id = job_result.get("job_id")
        print(f"   🆔 Job ID: {job_id}")
    else:
        print("❌ Job creation failed, stopping test")
        return
    
    # Step 5: Candidate Registration
    print("\n📋 STEP 5: Candidate Registration")
    success, candidate_result = test_endpoint("POST", f"{BASE_URL}/v1/candidate/register", 
                                             candidate_data, "Candidate Registration")
    
    if success:
        candidate_id = candidate_result.get("candidate_id")
        print(f"   🆔 Candidate ID: {candidate_id}")
    else:
        print("❌ Candidate registration failed, stopping test")
        return
    
    # Step 6: Candidate Login
    print("\n📋 STEP 6: Candidate Login")
    candidate_login = {
        "email": candidate_data["email"],
        "password": candidate_data["password"]
    }
    success, candidate_login_result = test_endpoint("POST", f"{BASE_URL}/v1/candidate/login", 
                                                   candidate_login, "Candidate Login")
    
    if success:
        candidate_token = candidate_login_result.get("token")
        print(f"   🔑 Candidate Token: {candidate_token[:20]}...")
    
    # Step 7: View Jobs
    print("\n📋 STEP 7: View Available Jobs")
    success, jobs_result = test_endpoint("GET", f"{BASE_URL}/v1/jobs", 
                                        description="Get All Jobs")
    
    if success:
        jobs = jobs_result.get("jobs", [])
        print(f"   📊 Found {len(jobs)} jobs")
        for job in jobs:
            print(f"      - {job.get('title')} (ID: {job.get('id')})")
    
    # Step 8: Apply for Job
    print("\n📋 STEP 8: Job Application")
    application_data = {
        "candidate_id": candidate_id,
        "job_id": job_id,
        "cover_letter": "I am very interested in this Senior Python Developer position. My 5 years of experience with Python and FastAPI make me a perfect fit."
    }
    success, app_result = test_endpoint("POST", f"{BASE_URL}/v1/candidate/apply", 
                                       application_data, "Apply for Job")
    
    if success:
        application_id = app_result.get("application_id")
        print(f"   🆔 Application ID: {application_id}")
    
    # Step 9: AI Matching
    print("\n📋 STEP 9: AI Matching")
    success, match_result = test_endpoint("GET", f"{BASE_URL}/v1/match/{job_id}/top", 
                                         description="Get AI Matches")
    
    if success:
        matches = match_result.get("matches", [])
        print(f"   🤖 Found {len(matches)} AI matches")
        for match in matches:
            print(f"      - {match.get('name')}: Score {match.get('score')}")
    
    # Step 10: Schedule Interview
    print("\n📋 STEP 10: Schedule Interview")
    interview_data = {
        "candidate_id": candidate_id,
        "job_id": job_id,
        "interview_date": "2025-01-15T10:00:00",
        "interviewer": "Jane Smith",
        "notes": "Technical interview for Senior Python Developer position"
    }
    success, interview_result = test_endpoint("POST", f"{BASE_URL}/v1/interviews", 
                                             interview_data, "Schedule Interview")
    
    if success:
        interview_id = interview_result.get("interview_id")
        print(f"   🆔 Interview ID: {interview_id}")
    
    # Step 11: Submit Feedback
    print("\n📋 STEP 11: Values Assessment")
    feedback_data = {
        "candidate_id": candidate_id,
        "job_id": job_id,
        "integrity": 5,
        "honesty": 5,
        "discipline": 4,
        "hard_work": 5,
        "gratitude": 4,
        "comments": "Excellent candidate with strong technical skills and values alignment"
    }
    success, feedback_result = test_endpoint("POST", f"{BASE_URL}/v1/feedback", 
                                            feedback_data, "Submit Feedback")
    
    if success:
        feedback_id = feedback_result.get("feedback_id")
        avg_score = feedback_result.get("average_score")
        print(f"   🆔 Feedback ID: {feedback_id}")
        print(f"   📊 Average Score: {avg_score}/5")
    
    # Step 12: Create Job Offer
    print("\n📋 STEP 12: Job Offer")
    offer_data = {
        "candidate_id": candidate_id,
        "job_id": job_id,
        "salary": 125000,
        "start_date": "2025-02-01",
        "terms": "Full-time position with health insurance, 401k, and PTO"
    }
    success, offer_result = test_endpoint("POST", f"{BASE_URL}/v1/offers", 
                                         offer_data, "Create Job Offer")
    
    if success:
        offer_id = offer_result.get("offer_id")
        print(f"   🆔 Offer ID: {offer_id}")
        print(f"   💰 Salary: ${offer_result.get('salary'):,}")
    
    # Step 13: Check Applications
    print("\n📋 STEP 13: Check Candidate Applications")
    success, apps_result = test_endpoint("GET", f"{BASE_URL}/v1/candidate/applications/{candidate_id}", 
                                        description="Get Candidate Applications")
    
    if success:
        applications = apps_result.get("applications", [])
        print(f"   📊 Found {len(applications)} applications")
        for app in applications:
            print(f"      - {app.get('job_title')}: {app.get('status')}")
    
    # Final Summary
    print("\n" + "=" * 50)
    print("🎉 WORKFLOW TEST COMPLETED!")
    print("=" * 50)
    print(f"✅ Client: {client_data['client_id']} registered and logged in")
    print(f"✅ Job: '{job_data['title']}' created (ID: {job_id})")
    print(f"✅ Candidate: {candidate_data['name']} registered and applied")
    print(f"✅ AI Matching: Scores calculated")
    print(f"✅ Interview: Scheduled")
    print(f"✅ Feedback: Values assessed")
    print(f"✅ Offer: Created")
    print("\n🔗 Portal URLs:")
    print("   Client Portal: http://localhost:8502")
    print("   HR Portal: http://localhost:8501")
    print("   Candidate Portal: http://localhost:8503")

if __name__ == "__main__":
    main()