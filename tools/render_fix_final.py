#!/usr/bin/env python3
"""
Final Render Database Fix
Uses the new database initialization endpoint to fix Render deployment
"""

import requests
import time

GATEWAY_URL = "https://bhiv-hr-gateway.onrender.com"
API_KEY = "myverysecureapikey123"

def wait_for_deployment(max_wait=300):
    """Wait for Render to deploy the new code"""
    print("Waiting for Render auto-deployment to complete...")
    
    for i in range(max_wait // 10):
        try:
            response = requests.get(f"{GATEWAY_URL}/health", timeout=30)
            if response.status_code == 200:
                print(f"Service is responding (attempt {i+1})")
                return True
        except Exception as e:
            print(f"Waiting for deployment... ({i+1}/30)")
        
        time.sleep(10)
    
    return False

def initialize_render_database():
    """Initialize the Render database using the new endpoint"""
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    
    print("Initializing Render database schema...")
    
    try:
        # Call the new database initialization endpoint
        payload = {"action": "create_schema", "force": True}
        response = requests.post(f"{GATEWAY_URL}/admin/init-database", 
                               json=payload, 
                               headers=headers, 
                               timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            print(f"Database initialization successful: {result}")
            return True
        else:
            print(f"Database initialization failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"Database initialization error: {e}")
        return False

def verify_render_functionality():
    """Verify all endpoints are working on Render"""
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    tests = [
        ("GET", "/health", "Health check"),
        ("GET", "/v1/jobs", "Jobs listing"),
        ("GET", "/candidates/stats", "Statistics"),
        ("GET", "/test-candidates", "Database connectivity")
    ]
    
    print("Verifying Render functionality...")
    working = 0
    
    for method, endpoint, name in tests:
        try:
            response = requests.get(f"{GATEWAY_URL}{endpoint}", headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if "error" not in str(data).lower() and "does not exist" not in str(data):
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

def create_sample_job():
    """Create a sample job to test functionality"""
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    
    job_data = {
        "title": "Test Job - Render Fixed",
        "department": "Engineering",
        "location": "Remote",
        "experience_level": "Senior",
        "requirements": "Python, FastAPI, PostgreSQL",
        "description": "Test job created after fixing Render database schema"
    }
    
    try:
        response = requests.post(f"{GATEWAY_URL}/v1/jobs", 
                               json=job_data, 
                               headers=headers, 
                               timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f"Sample job created successfully: ID {result.get('job_id')}")
            return True
        else:
            print(f"Job creation failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"Job creation error: {e}")
        return False

if __name__ == "__main__":
    print("BHIV HR Platform - Final Render Fix")
    print("=" * 40)
    
    # Step 1: Wait for deployment
    if wait_for_deployment():
        print("Deployment detected, proceeding with database fix...")
        
        # Step 2: Initialize database
        time.sleep(30)  # Give deployment time to complete
        if initialize_render_database():
            print("Database initialization successful!")
            
            # Step 3: Verify functionality
            time.sleep(10)
            if verify_render_functionality():
                print("SUCCESS: All endpoints working!")
                
                # Step 4: Create test job
                if create_sample_job():
                    print("COMPLETE: Render deployment now matches localhost!")
                else:
                    print("WARNING: Job creation still has issues")
            else:
                print("WARNING: Some endpoints still failing")
        else:
            print("ERROR: Database initialization failed")
    else:
        print("ERROR: Deployment not detected")
    
    print("\nRender Platform Status:")
    print(f"API Gateway: {GATEWAY_URL}/docs")
    print("HR Portal: https://bhiv-hr-portal.onrender.com/")
    print("Client Portal: https://bhiv-hr-client-portal.onrender.com/")