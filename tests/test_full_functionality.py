#!/usr/bin/env python3
"""
BHIV HR Platform - Complete Functionality Test Suite
Tests all core features and endpoints to verify system health
"""

import requests
import json
import time
from datetime import datetime

# Configuration
API_BASE = "http://localhost:8000"
AI_BASE = "http://localhost:9000"
API_KEY = "myverysecureapikey123"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def test_service_health():
    """Test all service health endpoints"""
    print("🔍 Testing Service Health...")
    
    services = [
        ("API Gateway", f"{API_BASE}/health"),
        ("AI Agent", f"{AI_BASE}/health"),
        ("API Root", f"{API_BASE}/")
    ]
    
    results = {}
    for name, url in services:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                results[name] = "✅ Healthy"
                print(f"  {name}: ✅ Healthy")
            else:
                results[name] = f"❌ Status {response.status_code}"
                print(f"  {name}: ❌ Status {response.status_code}")
        except Exception as e:
            results[name] = f"❌ Error: {str(e)}"
            print(f"  {name}: ❌ Error: {str(e)}")
    
    return results

def test_authentication():
    """Test API authentication"""
    print("\n🔐 Testing Authentication...")
    
    # Test with valid API key
    try:
        response = requests.get(f"{API_BASE}/candidates/stats", headers=HEADERS, timeout=5)
        if response.status_code == 200:
            print("  Valid API Key: ✅ Accepted")
            return True
        else:
            print(f"  Valid API Key: ❌ Status {response.status_code}")
            return False
    except Exception as e:
        print(f"  Authentication Test: ❌ Error: {str(e)}")
        return False

def test_job_management():
    """Test job creation and retrieval"""
    print("\n💼 Testing Job Management...")
    
    # Create test job
    job_data = {
        "title": "Senior Python Developer",
        "description": "Looking for experienced Python developer with AI/ML skills",
        "client_id": 1,
        "department": "Engineering",
        "location": "Remote",
        "experience_level": "Senior",
        "employment_type": "Full-time",
        "requirements": "5+ years Python, FastAPI, PostgreSQL",
        "status": "active"
    }
    
    try:
        # Create job
        response = requests.post(f"{API_BASE}/v1/jobs", headers=HEADERS, json=job_data, timeout=10)
        if response.status_code == 200:
            job_result = response.json()
            job_id = job_result.get("job_id")
            print(f"  Job Creation: ✅ Created job ID {job_id}")
            
            # List jobs
            response = requests.get(f"{API_BASE}/v1/jobs", headers=HEADERS, timeout=10)
            if response.status_code == 200:
                jobs = response.json()
                print(f"  Job Listing: ✅ Found {jobs.get('count', 0)} jobs")
                return job_id
            else:
                print(f"  Job Listing: ❌ Status {response.status_code}")
                return None
        else:
            print(f"  Job Creation: ❌ Status {response.status_code}")
            return None
    except Exception as e:
        print(f"  Job Management: ❌ Error: {str(e)}")
        return None

def test_candidate_management():
    """Test candidate upload and search"""
    print("\n👥 Testing Candidate Management...")
    
    # Test candidate upload
    candidates_data = {
        "candidates": [
            {
                "name": "Test Candidate 1",
                "email": "test1@example.com",
                "phone": "+1-555-0101",
                "location": "New York",
                "experience_years": 5,
                "technical_skills": "Python, FastAPI, PostgreSQL, Docker",
                "seniority_level": "Senior",
                "education_level": "Masters",
                "job_id": 1,
                "status": "applied"
            },
            {
                "name": "Test Candidate 2", 
                "email": "test2@example.com",
                "phone": "+1-555-0102",
                "location": "San Francisco",
                "experience_years": 3,
                "technical_skills": "Python, React, MongoDB",
                "seniority_level": "Mid-level",
                "education_level": "Bachelors",
                "job_id": 1,
                "status": "applied"
            }
        ]
    }
    
    try:
        # Upload candidates
        response = requests.post(f"{API_BASE}/v1/candidates/bulk", headers=HEADERS, json=candidates_data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"  Candidate Upload: ✅ Uploaded {result.get('count', 0)} candidates")
            
            # Test candidate search
            response = requests.get(f"{API_BASE}/v1/candidates/search?job_id=1&skills=Python", headers=HEADERS, timeout=10)
            if response.status_code == 200:
                search_result = response.json()
                print(f"  Candidate Search: ✅ Found {search_result.get('count', 0)} candidates")
                return True
            else:
                print(f"  Candidate Search: ❌ Status {response.status_code}")
                return False
        else:
            print(f"  Candidate Upload: ❌ Status {response.status_code}")
            return False
    except Exception as e:
        print(f"  Candidate Management: ❌ Error: {str(e)}")
        return False

def test_ai_matching():
    """Test AI matching functionality"""
    print("\n🤖 Testing AI Matching...")
    
    try:
        response = requests.get(f"{API_BASE}/v1/match/1/top", headers=HEADERS, timeout=15)
        if response.status_code == 200:
            result = response.json()
            candidates = result.get("top_candidates", [])
            print(f"  AI Matching: ✅ Generated {len(candidates)} top candidates")
            return True
        else:
            print(f"  AI Matching: ❌ Status {response.status_code}")
            return False
    except Exception as e:
        print(f"  AI Matching: ❌ Error: {str(e)}")
        return False

def test_values_assessment():
    """Test values assessment functionality"""
    print("\n🏆 Testing Values Assessment...")
    
    feedback_data = {
        "candidate_id": 1,
        "reviewer": "Test Reviewer",
        "feedback_text": "Excellent candidate with strong technical skills and values alignment",
        "values_scores": {
            "integrity": 5,
            "honesty": 4,
            "discipline": 5,
            "hard_work": 5,
            "gratitude": 4
        }
    }
    
    try:
        response = requests.post(f"{API_BASE}/v1/feedback", headers=HEADERS, json=feedback_data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"  Values Assessment: ✅ Submitted feedback ID {result.get('feedback_id')}")
            if "values_profile" in result:
                profile = result["values_profile"]
                print(f"    - Values Average: {profile.get('values_average', 'N/A')}")
                print(f"    - Recommendation: {profile.get('recommendation', 'N/A')}")
            return True
        else:
            print(f"  Values Assessment: ❌ Status {response.status_code}")
            return False
    except Exception as e:
        print(f"  Values Assessment: ❌ Error: {str(e)}")
        return False

def test_interview_scheduling():
    """Test interview scheduling"""
    print("\n📅 Testing Interview Scheduling...")
    
    interview_data = {
        "candidate_id": 1,
        "job_id": 1,
        "interview_date": "2025-02-01T10:00:00Z",
        "interviewer": "Tech Lead"
    }
    
    try:
        response = requests.post(f"{API_BASE}/v1/interviews", headers=HEADERS, json=interview_data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"  Interview Scheduling: ✅ Scheduled interview ID {result.get('interview_id')}")
            return True
        else:
            print(f"  Interview Scheduling: ❌ Status {response.status_code}")
            return False
    except Exception as e:
        print(f"  Interview Scheduling: ❌ Error: {str(e)}")
        return False

def test_offer_management():
    """Test offer management"""
    print("\n💰 Testing Offer Management...")
    
    offer_data = {
        "candidate_id": 1,
        "job_id": 1,
        "salary": 120000,
        "status": "sent"
    }
    
    try:
        response = requests.post(f"{API_BASE}/v1/offers", headers=HEADERS, json=offer_data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"  Offer Management: ✅ Created offer ID {result.get('offer_id')}")
            return True
        else:
            print(f"  Offer Management: ❌ Status {response.status_code}")
            return False
    except Exception as e:
        print(f"  Offer Management: ❌ Error: {str(e)}")
        return False

def test_statistics():
    """Test statistics endpoint"""
    print("\n📊 Testing Statistics...")
    
    try:
        response = requests.get(f"{API_BASE}/candidates/stats", headers=HEADERS, timeout=10)
        if response.status_code == 200:
            stats = response.json()
            print(f"  Statistics: ✅ Retrieved stats")
            print(f"    - Total Candidates: {stats.get('total_candidates', 0)}")
            print(f"    - Total Jobs: {stats.get('total_jobs', 0)}")
            print(f"    - Total Feedback: {stats.get('total_feedback', 0)}")
            return True
        else:
            print(f"  Statistics: ❌ Status {response.status_code}")
            return False
    except Exception as e:
        print(f"  Statistics: ❌ Error: {str(e)}")
        return False

def run_full_test_suite():
    """Run complete functionality test suite"""
    print("🎯 BHIV HR Platform - Complete Functionality Test")
    print("=" * 60)
    print(f"Test Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    test_results = {}
    
    # Run all tests
    test_results["Service Health"] = test_service_health()
    test_results["Authentication"] = test_authentication()
    test_results["Job Management"] = test_job_management()
    test_results["Candidate Management"] = test_candidate_management()
    test_results["AI Matching"] = test_ai_matching()
    test_results["Values Assessment"] = test_values_assessment()
    test_results["Interview Scheduling"] = test_interview_scheduling()
    test_results["Offer Management"] = test_offer_management()
    test_results["Statistics"] = test_statistics()
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results.items():
        if isinstance(result, bool):
            status = "✅ PASSED" if result else "❌ FAILED"
            if result:
                passed += 1
        elif isinstance(result, dict):
            # Service health results
            healthy_services = sum(1 for v in result.values() if "✅" in str(v))
            total_services = len(result)
            status = f"✅ {healthy_services}/{total_services} services healthy"
            if healthy_services == total_services:
                passed += 1
        else:
            status = "❌ FAILED"
        
        print(f"{test_name:<25}: {status}")
    
    print(f"\nOverall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - System is fully functional!")
    else:
        print("⚠️  Some tests failed - Check service connectivity")
    
    print(f"\nTest Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    run_full_test_suite()