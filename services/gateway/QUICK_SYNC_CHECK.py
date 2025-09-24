#!/usr/bin/env python3
"""
BHIV HR Platform - Quick Service Sync Check
Minimal verification to check if services are in sync after database changes
"""

import requests
import json
from datetime import datetime

def check_service_sync():
    """Quick check of service synchronization"""
    
    # Service endpoints
    services = {
        "Gateway": "https://bhiv-hr-gateway-901a.onrender.com",
        "AI Agent": "https://bhiv-hr-agent-o6nx.onrender.com", 
        "HR Portal": "https://bhiv-hr-portal-xk2k.onrender.com",
        "Client Portal": "https://bhiv-hr-client-portal-zdbt.onrender.com"
    }
    
    api_key = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    print("🔍 BHIV HR Platform - Quick Service Sync Check")
    print("=" * 50)
    print(f"⏰ Timestamp: {datetime.now().isoformat()}")
    print()
    
    results = {}
    
    # 1. Check service health
    print("1️⃣ Service Health Check:")
    for name, url in services.items():
        try:
            response = requests.get(f"{url}/health", timeout=10)
            if response.status_code == 200:
                print(f"  ✅ {name}: Healthy")
                results[name] = "healthy"
            else:
                print(f"  ❌ {name}: Unhealthy (HTTP {response.status_code})")
                results[name] = "unhealthy"
        except Exception as e:
            print(f"  ❌ {name}: Unreachable ({str(e)[:50]}...)")
            results[name] = "unreachable"
    
    print()
    
    # 2. Check database integration
    print("2️⃣ Database Integration Check:")
    gateway_url = services["Gateway"]
    
    db_tests = {
        "Database Health": f"{gateway_url}/v1/health",
        "Candidates": f"{gateway_url}/v1/candidates",
        "Jobs": f"{gateway_url}/v1/jobs", 
        "Interviews": f"{gateway_url}/v1/interviews",
        "Database Stats": f"{gateway_url}/v1/stats"
    }
    
    db_results = {}
    for test_name, url in db_tests.items():
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if test_name == "Database Stats":
                    stats = data.get("database_statistics", {})
                    print(f"  ✅ {test_name}: {stats}")
                elif test_name == "Database Health":
                    status = data.get("database_status", "unknown")
                    print(f"  ✅ {test_name}: {status}")
                else:
                    count = len(data.get(test_name.lower(), []))
                    print(f"  ✅ {test_name}: {count} records")
                db_results[test_name] = "success"
            else:
                print(f"  ❌ {test_name}: Failed (HTTP {response.status_code})")
                db_results[test_name] = "failed"
        except Exception as e:
            print(f"  ❌ {test_name}: Error ({str(e)[:30]}...)")
            db_results[test_name] = "error"
    
    print()
    
    # 3. Check AI matching integration
    print("3️⃣ AI Matching Integration:")
    try:
        # Test gateway AI endpoint
        response = requests.get(f"{gateway_url}/v1/match/1/top?limit=3", headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            matches = len(data.get("matches", []))
            algorithm = data.get("algorithm_version", "unknown")
            print(f"  ✅ Gateway AI Matching: {matches} matches, {algorithm}")
        else:
            print(f"  ❌ Gateway AI Matching: Failed (HTTP {response.status_code})")
        
        # Test agent service
        agent_url = services["AI Agent"]
        response = requests.get(f"{agent_url}/health", timeout=10)
        if response.status_code == 200:
            print(f"  ✅ AI Agent Service: Healthy")
        else:
            print(f"  ❌ AI Agent Service: Unhealthy")
            
    except Exception as e:
        print(f"  ❌ AI Matching: Error ({str(e)[:50]}...)")
    
    print()
    
    # 4. Test CRUD operation
    print("4️⃣ CRUD Operation Test:")
    try:
        # Test job creation
        job_data = {
            "title": "Sync Test Job",
            "department": "Testing", 
            "location": "Remote",
            "experience_level": "Mid-Level",
            "requirements": "Sync testing",
            "description": "Test job for sync verification"
        }
        
        response = requests.post(
            f"{gateway_url}/v1/jobs",
            headers={**headers, "Content-Type": "application/json"},
            json=job_data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            job_id = result.get("job_id")
            print(f"  ✅ Job Creation: Success (ID: {job_id})")
            
            # Verify job appears in list
            response = requests.get(f"{gateway_url}/v1/jobs", headers=headers, timeout=10)
            if response.status_code == 200:
                jobs = response.json().get("jobs", [])
                job_found = any(job.get("id") == job_id for job in jobs)
                print(f"  ✅ Job Retrieval: {'Found' if job_found else 'Not Found'} in list")
            else:
                print(f"  ❌ Job Retrieval: Failed")
        else:
            print(f"  ❌ Job Creation: Failed (HTTP {response.status_code})")
            
    except Exception as e:
        print(f"  ❌ CRUD Test: Error ({str(e)[:50]}...)")
    
    print()
    
    # 5. Summary
    print("📊 SYNC STATUS SUMMARY:")
    healthy_services = sum(1 for status in results.values() if status == "healthy")
    total_services = len(results)
    
    db_success = sum(1 for status in db_results.values() if status == "success")
    db_total = len(db_results)
    
    print(f"  🏥 Services Health: {healthy_services}/{total_services}")
    print(f"  🗄️ Database Tests: {db_success}/{db_total}")
    
    if healthy_services == total_services and db_success >= db_total * 0.8:
        print("  🎯 Overall Status: ✅ SERVICES IN SYNC")
        return True
    else:
        print("  🎯 Overall Status: ⚠️ SYNC ISSUES DETECTED")
        return False

if __name__ == "__main__":
    try:
        sync_status = check_service_sync()
        exit(0 if sync_status else 1)
    except Exception as e:
        print(f"❌ Sync check failed: {e}")
        exit(2)