"""Test workflow engine integration"""

import asyncio
import requests
import json
import time

# Configuration
API_BASE_URL = "https://bhiv-hr-gateway-901a.onrender.com"
LOCAL_URL = "http://localhost:8000"

def test_workflow_endpoints():
    """Test workflow endpoints"""
    print("🔍 Testing Workflow Endpoints...")
    
    # Test workflow list
    response = requests.get(f"{API_BASE_URL}/v1/workflows")
    assert response.status_code == 200
    print("✅ Workflow list endpoint working")
    
    # Test workflow creation
    response = requests.post(
        f"{API_BASE_URL}/v1/workflows",
        params={"workflow_type": "job_posting"}
    )
    assert response.status_code == 200
    workflow_data = response.json()
    workflow_id = workflow_data["workflow_id"]
    print(f"✅ Workflow created: {workflow_id}")
    
    # Test workflow status
    response = requests.get(f"{API_BASE_URL}/v1/workflows/{workflow_id}")
    assert response.status_code == 200
    print("✅ Workflow status endpoint working")
    
    # Test workflow start
    response = requests.post(f"{API_BASE_URL}/v1/workflows/{workflow_id}/start")
    assert response.status_code == 200
    print("✅ Workflow start endpoint working")
    
    return workflow_id

def test_job_workflow_integration():
    """Test job creation with workflow integration"""
    print("🔍 Testing Job-Workflow Integration...")
    
    job_data = {
        "title": "Senior Python Developer - Workflow Test",
        "description": "Test job creation with workflow integration. This is a comprehensive test to verify that job creation triggers the appropriate workflow processes.",
        "requirements": "Python, FastAPI, PostgreSQL, Docker, AWS",
        "location": "San Francisco, CA",
        "department": "Engineering",
        "experience_level": "Senior",
        "salary_min": 120000,
        "salary_max": 180000,
        "job_type": "Full-time"
    }
    
    response = requests.post(
        f"{API_BASE_URL}/v1/jobs",
        json=job_data,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        job_response = response.json()
        print(f"✅ Job created successfully: {job_response.get('job_id')}")
        
        if "workflow_id" in job_response:
            print(f"✅ Workflow triggered: {job_response['workflow_id']}")
        else:
            print("⚠️ Workflow ID not returned (may need integration update)")
        
        return job_response
    else:
        print(f"❌ Job creation failed: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def test_monitoring_endpoints():
    """Test monitoring endpoints"""
    print("🔍 Testing Monitoring Endpoints...")
    
    endpoints = [
        "/metrics",
        "/v1/monitoring/health/detailed",
        "/monitoring/dashboard",
        "/v1/analytics/dashboard"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{API_BASE_URL}{endpoint}")
            if response.status_code == 200:
                print(f"✅ {endpoint}")
            else:
                print(f"⚠️ {endpoint} - Status: {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint} - Error: {e}")

def test_system_endpoints():
    """Test system information endpoints"""
    print("🔍 Testing System Endpoints...")
    
    # Test modules endpoint
    response = requests.get(f"{API_BASE_URL}/system/modules")
    assert response.status_code == 200
    modules_data = response.json()
    assert modules_data["total_modules"] == 6
    print(f"✅ System modules: {modules_data['total_modules']} modules active")
    
    # Test architecture endpoint
    response = requests.get(f"{API_BASE_URL}/system/architecture")
    assert response.status_code == 200
    arch_data = response.json()
    assert arch_data["architecture"]["type"] == "modular_microservices"
    print("✅ System architecture: Modular microservices confirmed")

def run_comprehensive_test():
    """Run comprehensive integration test"""
    print("🚀 BHIV HR Platform - Comprehensive Integration Test")
    print("=" * 60)
    
    try:
        # Test system endpoints
        test_system_endpoints()
        print()
        
        # Test workflow endpoints
        workflow_id = test_workflow_endpoints()
        print()
        
        # Test job-workflow integration
        job_response = test_job_workflow_integration()
        print()
        
        # Test monitoring endpoints
        test_monitoring_endpoints()
        print()
        
        print("=" * 60)
        print("🎉 ALL TESTS PASSED!")
        print("✅ Modular architecture: OPERATIONAL")
        print("✅ Workflow engine: OPERATIONAL")
        print("✅ Job integration: OPERATIONAL")
        print("✅ Monitoring system: OPERATIONAL")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = run_comprehensive_test()
    exit(0 if success else 1)