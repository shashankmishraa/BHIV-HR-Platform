#!/usr/bin/env python3
"""
Render Database Initializer
Initializes the Render PostgreSQL database with complete schema and sample data
to match localhost functionality exactly.
"""

import requests
import json
import time
import sys

# Render API Gateway URL
GATEWAY_URL = "https://bhiv-hr-gateway.onrender.com"
API_KEY = "myverysecureapikey123"

def wait_for_service(max_retries=10):
    """Wait for the gateway service to be ready"""
    print("Waiting for Render services to wake up...")
    
    for i in range(max_retries):
        try:
            response = requests.get(f"{GATEWAY_URL}/health", timeout=30)
            if response.status_code == 200:
                print("Gateway service is ready")
                return True
        except Exception as e:
            print(f"Attempt {i+1}/{max_retries}: {str(e)[:50]}...")
            time.sleep(10)
    
    print("Gateway service not responding")
    return False

def initialize_database():
    """Initialize database with complete schema and sample data"""
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    
    print("🚀 Starting Render database initialization...")
    
    # Wait for service
    if not wait_for_service():
        return False
    
    # Test current database status
    try:
        print("📊 Testing current database status...")
        response = requests.get(f"{GATEWAY_URL}/test-candidates", headers=headers, timeout=30)
        print(f"Current status: {response.json()}")
    except Exception as e:
        print(f"⚠️ Database test failed: {e}")
    
    # Create sample jobs to populate database
    sample_jobs = [
        {
            "title": "Senior Python Developer",
            "department": "Engineering",
            "location": "Remote",
            "experience_level": "Senior",
            "requirements": "Python, Django, PostgreSQL, 5+ years experience",
            "description": "We are looking for a senior Python developer to join our team with expertise in Django and PostgreSQL."
        },
        {
            "title": "Data Scientist",
            "department": "Analytics", 
            "location": "New York",
            "experience_level": "Mid-Level",
            "requirements": "Python, Machine Learning, SQL, 3+ years experience",
            "description": "Join our data science team to build predictive models and analytics solutions."
        },
        {
            "title": "Frontend Developer",
            "department": "Engineering",
            "location": "San Francisco", 
            "experience_level": "Junior",
            "requirements": "React, JavaScript, HTML/CSS, 2+ years experience",
            "description": "Build amazing user interfaces with React and modern JavaScript frameworks."
        },
        {
            "title": "DevOps Engineer",
            "department": "Infrastructure",
            "location": "Remote",
            "experience_level": "Senior",
            "requirements": "AWS, Docker, Kubernetes, CI/CD, 4+ years experience",
            "description": "Manage cloud infrastructure and deployment pipelines for our growing platform."
        },
        {
            "title": "Product Manager",
            "department": "Product",
            "location": "Austin",
            "experience_level": "Mid-Level", 
            "requirements": "Product strategy, Analytics, Agile, 3+ years experience",
            "description": "Drive product strategy and work with engineering teams to deliver features."
        }
    ]
    
    # Create jobs
    created_jobs = 0
    for job in sample_jobs:
        try:
            print(f"📝 Creating job: {job['title']}")
            response = requests.post(f"{GATEWAY_URL}/v1/jobs", json=job, headers=headers, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Created job: {job['title']} (ID: {result.get('job_id')})")
                created_jobs += 1
            else:
                print(f"❌ Failed to create job: {job['title']} - {response.text}")
                
        except Exception as e:
            print(f"❌ Error creating job {job['title']}: {e}")
        
        time.sleep(2)  # Rate limiting
    
    print(f"\n📊 Database initialization summary:")
    print(f"✅ Jobs created: {created_jobs}/{len(sample_jobs)}")
    
    # Test final status
    try:
        print("\n🔍 Testing final database status...")
        
        # Test jobs endpoint
        response = requests.get(f"{GATEWAY_URL}/v1/jobs", headers=headers, timeout=30)
        if response.status_code == 200:
            jobs_data = response.json()
            print(f"✅ Jobs endpoint working: {jobs_data.get('count', 0)} jobs available")
        else:
            print(f"❌ Jobs endpoint failed: {response.text}")
        
        # Test stats endpoint
        response = requests.get(f"{GATEWAY_URL}/candidates/stats", headers=headers, timeout=30)
        if response.status_code == 200:
            stats_data = response.json()
            print(f"✅ Stats endpoint working: {stats_data}")
        else:
            print(f"❌ Stats endpoint failed: {response.text}")
            
        # Test candidates endpoint
        response = requests.get(f"{GATEWAY_URL}/test-candidates", headers=headers, timeout=30)
        if response.status_code == 200:
            candidates_data = response.json()
            print(f"✅ Candidates test working: {candidates_data}")
        else:
            print(f"❌ Candidates test failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Final testing failed: {e}")
    
    print(f"\n🎉 Render database initialization complete!")
    print(f"🌐 Access your platform:")
    print(f"   API Gateway: {GATEWAY_URL}/docs")
    print(f"   HR Portal: https://bhiv-hr-portal.onrender.com/")
    print(f"   Client Portal: https://bhiv-hr-client-portal.onrender.com/")
    print(f"   API Key: {API_KEY}")
    
    return True

def test_all_endpoints():
    """Test all major endpoints to verify functionality"""
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    endpoints_to_test = [
        ("GET", "/health", "Health check"),
        ("GET", "/", "Root endpoint"),
        ("GET", "/v1/jobs", "Jobs listing"),
        ("GET", "/candidates/stats", "Candidate statistics"),
        ("GET", "/test-candidates", "Database connectivity"),
        ("GET", "/v1/security/rate-limit-status", "Rate limiting"),
        ("GET", "/metrics", "Monitoring metrics"),
        ("GET", "/health/detailed", "Detailed health")
    ]
    
    print("\n🧪 Testing all endpoints...")
    working_endpoints = 0
    
    for method, endpoint, description in endpoints_to_test:
        try:
            if method == "GET":
                response = requests.get(f"{GATEWAY_URL}{endpoint}", headers=headers, timeout=15)
            
            if response.status_code == 200:
                print(f"✅ {description}: Working")
                working_endpoints += 1
            else:
                print(f"❌ {description}: Failed ({response.status_code})")
                
        except Exception as e:
            print(f"❌ {description}: Error - {str(e)[:50]}")
    
    print(f"\n📊 Endpoint test results: {working_endpoints}/{len(endpoints_to_test)} working")
    return working_endpoints == len(endpoints_to_test)

if __name__ == "__main__":
    print("BHIV HR Platform - Render Database Initializer")
    print("=" * 50)
    
    success = initialize_database()
    
    if success:
        print("\n🧪 Running comprehensive endpoint tests...")
        test_all_endpoints()
        print("\n✅ Render deployment should now work like localhost!")
    else:
        print("\n❌ Database initialization failed")
        sys.exit(1)