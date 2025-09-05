#!/usr/bin/env python3
"""
Direct Database Schema Creator for Render
Creates database tables directly via API endpoint
"""

import requests
import time

GATEWAY_URL = "https://bhiv-hr-gateway.onrender.com"
API_KEY = "myverysecureapikey123"

def create_database_schema():
    """Create database schema via API endpoint"""
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    
    print("Creating database schema on Render...")
    
    # Wait for service to wake up
    print("Waking up Render services...")
    try:
        response = requests.get(f"{GATEWAY_URL}/health", timeout=60)
        print(f"Gateway status: {response.json()}")
    except Exception as e:
        print(f"Service wake up failed: {e}")
        return False
    
    # Create schema via direct database endpoint
    schema_payload = {
        "action": "create_schema",
        "force": True
    }
    
    try:
        print("Creating database tables...")
        response = requests.post(f"{GATEWAY_URL}/admin/init-database", 
                               json=schema_payload, 
                               headers=headers, 
                               timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            print(f"Schema creation result: {result}")
            return True
        else:
            print(f"Schema creation failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"Schema creation error: {e}")
        return False

def populate_sample_data():
    """Populate database with sample data"""
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    
    # Sample jobs data
    jobs = [
        {
            "title": "Senior Python Developer",
            "department": "Engineering",
            "location": "Remote",
            "experience_level": "Senior",
            "requirements": "Python, Django, PostgreSQL, 5+ years experience",
            "description": "Senior Python developer position with Django and PostgreSQL expertise required."
        },
        {
            "title": "Data Scientist",
            "department": "Analytics",
            "location": "New York",
            "experience_level": "Mid-Level", 
            "requirements": "Python, Machine Learning, SQL, 3+ years experience",
            "description": "Data scientist role focusing on machine learning and predictive analytics."
        },
        {
            "title": "Frontend Developer",
            "department": "Engineering",
            "location": "San Francisco",
            "experience_level": "Junior",
            "requirements": "React, JavaScript, HTML/CSS, 2+ years experience", 
            "description": "Frontend developer position working with React and modern JavaScript."
        }
    ]
    
    created_count = 0
    for job in jobs:
        try:
            print(f"Creating job: {job['title']}")
            response = requests.post(f"{GATEWAY_URL}/v1/jobs", 
                                   json=job, 
                                   headers=headers, 
                                   timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                print(f"Created: {job['title']} (ID: {result.get('job_id')})")
                created_count += 1
            else:
                print(f"Failed: {job['title']} - {response.text}")
                
        except Exception as e:
            print(f"Error creating {job['title']}: {e}")
        
        time.sleep(1)
    
    print(f"Created {created_count}/{len(jobs)} jobs")
    return created_count > 0

def verify_functionality():
    """Verify all endpoints are working"""
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    tests = [
        ("GET", "/health", "Health check"),
        ("GET", "/v1/jobs", "Jobs listing"),
        ("GET", "/candidates/stats", "Statistics"),
        ("GET", "/test-candidates", "Database test")
    ]
    
    print("Verifying functionality...")
    working = 0
    
    for method, endpoint, name in tests:
        try:
            response = requests.get(f"{GATEWAY_URL}{endpoint}", headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if "error" not in str(data).lower():
                    print(f"PASS: {name}")
                    working += 1
                else:
                    print(f"FAIL: {name} - {data}")
            else:
                print(f"FAIL: {name} - Status {response.status_code}")
        except Exception as e:
            print(f"FAIL: {name} - {e}")
    
    print(f"Working endpoints: {working}/{len(tests)}")
    return working == len(tests)

if __name__ == "__main__":
    print("BHIV HR Platform - Render Schema Creator")
    print("=" * 45)
    
    # Step 1: Create schema
    if create_database_schema():
        print("Schema creation successful!")
        
        # Step 2: Populate data
        time.sleep(5)
        if populate_sample_data():
            print("Data population successful!")
            
            # Step 3: Verify
            time.sleep(3)
            if verify_functionality():
                print("SUCCESS: Render deployment now matches localhost!")
            else:
                print("WARNING: Some endpoints still have issues")
        else:
            print("WARNING: Data population failed")
    else:
        print("ERROR: Schema creation failed")
        
    print("\nRender Platform URLs:")
    print(f"API Docs: {GATEWAY_URL}/docs")
    print("HR Portal: https://bhiv-hr-portal.onrender.com/")
    print("Client Portal: https://bhiv-hr-client-portal.onrender.com/")