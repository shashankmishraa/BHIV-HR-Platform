#!/usr/bin/env python3
"""
Simple Render Database Initializer - No Unicode
"""

import requests
import json
import time
import sys

GATEWAY_URL = "https://bhiv-hr-gateway.onrender.com"
API_KEY = "myverysecureapikey123"

def wait_for_service(max_retries=10):
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
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    
    print("Starting Render database initialization...")
    
    if not wait_for_service():
        return False
    
    # Test current status
    try:
        print("Testing current database status...")
        response = requests.get(f"{GATEWAY_URL}/test-candidates", headers=headers, timeout=30)
        print(f"Current status: {response.json()}")
    except Exception as e:
        print(f"Database test failed: {e}")
    
    # Create sample jobs
    sample_jobs = [
        {
            "title": "Senior Python Developer",
            "department": "Engineering",
            "location": "Remote",
            "experience_level": "Senior",
            "requirements": "Python, Django, PostgreSQL, 5+ years experience",
            "description": "We are looking for a senior Python developer to join our team."
        },
        {
            "title": "Data Scientist",
            "department": "Analytics", 
            "location": "New York",
            "experience_level": "Mid-Level",
            "requirements": "Python, Machine Learning, SQL, 3+ years experience",
            "description": "Join our data science team to build predictive models."
        },
        {
            "title": "Frontend Developer",
            "department": "Engineering",
            "location": "San Francisco", 
            "experience_level": "Junior",
            "requirements": "React, JavaScript, HTML/CSS, 2+ years experience",
            "description": "Build amazing user interfaces with React."
        },
        {
            "title": "DevOps Engineer",
            "department": "Infrastructure",
            "location": "Remote",
            "experience_level": "Senior",
            "requirements": "AWS, Docker, Kubernetes, CI/CD, 4+ years experience",
            "description": "Manage cloud infrastructure and deployment pipelines."
        }
    ]
    
    # Create jobs
    created_jobs = 0
    for job in sample_jobs:
        try:
            print(f"Creating job: {job['title']}")
            response = requests.post(f"{GATEWAY_URL}/v1/jobs", json=job, headers=headers, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                print(f"Created job: {job['title']} (ID: {result.get('job_id')})")
                created_jobs += 1
            else:
                print(f"Failed to create job: {job['title']} - {response.text}")
                
        except Exception as e:
            print(f"Error creating job {job['title']}: {e}")
        
        time.sleep(2)
    
    print(f"Jobs created: {created_jobs}/{len(sample_jobs)}")
    
    # Test final status
    try:
        print("Testing final database status...")
        
        response = requests.get(f"{GATEWAY_URL}/v1/jobs", headers=headers, timeout=30)
        if response.status_code == 200:
            jobs_data = response.json()
            print(f"Jobs endpoint working: {jobs_data.get('count', 0)} jobs available")
        
        response = requests.get(f"{GATEWAY_URL}/candidates/stats", headers=headers, timeout=30)
        if response.status_code == 200:
            stats_data = response.json()
            print(f"Stats endpoint working: {stats_data}")
            
    except Exception as e:
        print(f"Final testing failed: {e}")
    
    print("Database initialization complete!")
    print(f"API Gateway: {GATEWAY_URL}/docs")
    print(f"HR Portal: https://bhiv-hr-portal.onrender.com/")
    print(f"Client Portal: https://bhiv-hr-client-portal.onrender.com/")
    
    return True

if __name__ == "__main__":
    print("BHIV HR Platform - Render Database Initializer")
    print("=" * 50)
    
    success = initialize_database()
    
    if success:
        print("Render deployment should now work like localhost!")
    else:
        print("Database initialization failed")
        sys.exit(1)