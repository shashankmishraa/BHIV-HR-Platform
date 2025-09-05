#!/usr/bin/env python3
"""
Test script to verify job creation endpoint fix
"""

import requests
import json

# Configuration
API_BASE = "http://localhost:8000"
RENDER_API_BASE = "https://bhiv-hr-gateway.onrender.com"
API_KEY = "myverysecureapikey123"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def test_job_creation_localhost():
    """Test job creation on localhost"""
    print("Testing job creation on localhost...")
    
    # This is the exact data structure that the client portal sends
    job_data = {
        "title": "AI/ML Developer",
        "description": "An AIML Developer designs, develops, and deploys machine learning models and AI applications to solve practical business and technology challenges.",
        "client_id": 1,
        "requirements": "Proficiency in Python and machine learning frameworks (TensorFlow, PyTorch, Keras), expertise in data analysis and statistical methods, experience with large datasets, problem-solving, and strong communication abilities.",
        "location": "Remote",
        "department": "Engineering",
        "experience_level": "Mid",
        "employment_type": "Full-time",
        "status": "active"
    }
    
    try:
        response = requests.post(f"{API_BASE}/v1/jobs", headers=HEADERS, json=job_data, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS: Job created with ID {result.get('job_id')}")
            return True
        else:
            print(f"❌ FAILED: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def test_job_creation_render():
    """Test job creation on Render"""
    print("\nTesting job creation on Render...")
    
    # This is the exact data structure that the client portal sends
    job_data = {
        "title": "AI/ML Developer",
        "description": "An AIML Developer designs, develops, and deploys machine learning models and AI applications to solve practical business and technology challenges.",
        "client_id": 1,
        "requirements": "Proficiency in Python and machine learning frameworks (TensorFlow, PyTorch, Keras), expertise in data analysis and statistical methods, experience with large datasets, problem-solving, and strong communication abilities.",
        "location": "Remote",
        "department": "Engineering",
        "experience_level": "Mid",
        "employment_type": "Full-time",
        "status": "active"
    }
    
    try:
        response = requests.post(f"{RENDER_API_BASE}/v1/jobs", headers=HEADERS, json=job_data, timeout=15)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS: Job created with ID {result.get('job_id')}")
            return True
        else:
            print(f"❌ FAILED: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def test_minimal_job_creation():
    """Test job creation with minimal required fields only"""
    print("\nTesting minimal job creation...")
    
    # Only required fields
    job_data = {
        "title": "Minimal Test Job",
        "description": "Test job with minimal fields",
        "department": "Engineering",
        "location": "Remote",
        "experience_level": "Mid",
        "requirements": "Basic requirements"
    }
    
    try:
        response = requests.post(f"{API_BASE}/v1/jobs", headers=HEADERS, json=job_data, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS: Minimal job created with ID {result.get('job_id')}")
            return True
        else:
            print(f"❌ FAILED: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def main():
    print("BHIV HR Platform - Job Creation Fix Test")
    print("=" * 50)
    
    results = []
    
    # Test localhost
    results.append(test_job_creation_localhost())
    
    # Test minimal fields
    results.append(test_minimal_job_creation())
    
    # Test Render (optional)
    try:
        results.append(test_job_creation_render())
    except:
        print("Render test skipped (service may be unavailable)")
    
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Job creation endpoint is fixed.")
    else:
        print("⚠️ Some tests failed. Check the output above.")

if __name__ == "__main__":
    main()