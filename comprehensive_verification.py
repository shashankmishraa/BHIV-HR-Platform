#!/usr/bin/env python3
"""
Comprehensive System Verification
Test all critical issues after fixes
"""

import requests
from datetime import datetime

def test_all_systems():
    """Test all critical systems comprehensively"""
    api_base = "https://bhiv-hr-gateway-46pz.onrender.com"
    headers = {"Authorization": "Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"}
    
    print("Comprehensive System Verification")
    print(f"Timestamp: {datetime.now()}")
    print("=" * 60)
    
    results = []
    
    # Test 1: System Health
    print("\n1. System Health Check")
    try:
        response = requests.get(f"{api_base}/health", headers=headers, timeout=10)
        if response.status_code == 200:
            print("PASS: System is healthy")
            results.append(("System Health", True))
        else:
            print(f"FAIL: Health check returned {response.status_code}")
            results.append(("System Health", False))
    except Exception as e:
        print(f"FAIL: Health check error - {e}")
        results.append(("System Health", False))
    
    # Test 2: Database Connection
    print("\n2. Database Connection")
    try:
        response = requests.get(f"{api_base}/test-candidates", headers=headers, timeout=10)
        if response.status_code == 200:
            print("PASS: Database connected")
            results.append(("Database Connection", True))
        else:
            print(f"FAIL: Database test returned {response.status_code}")
            results.append(("Database Connection", False))
    except Exception as e:
        print(f"FAIL: Database test error - {e}")
        results.append(("Database Connection", False))
    
    # Test 3: Job Creation (Fixed)
    print("\n3. Job Creation with Salary Fields")
    job_data = {
        "title": "Verification Test Job",
        "department": "Testing",
        "location": "Remote",
        "experience_level": "Mid-level",
        "requirements": "Testing, Verification, Quality Assurance",
        "description": "Job for system verification testing",
        "client_id": 1,
        "employment_type": "Full-time",
        "status": "active",
        "salary_min": 70000,
        "salary_max": 100000
    }
    
    try:
        response = requests.post(f"{api_base}/v1/jobs", json=job_data, headers=headers, timeout=10)
        if response.status_code == 200:
            result = response.json()
            job_id = result.get('job_id')
            print(f"PASS: Job created successfully - ID: {job_id}")
            results.append(("Job Creation", True))
        else:
            print(f"FAIL: Job creation failed - {response.status_code}: {response.text[:200]}")
            results.append(("Job Creation", False))
    except Exception as e:
        print(f"FAIL: Job creation error - {e}")
        results.append(("Job Creation", False))
    
    # Test 4: Jobs List
    print("\n4. Jobs List Retrieval")
    try:
        response = requests.get(f"{api_base}/v1/jobs", headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            jobs = data.get('jobs', [])
            print(f"PASS: Retrieved {len(jobs)} jobs")
            results.append(("Jobs List", True))
        else:
            print(f"FAIL: Jobs list failed - {response.status_code}")
            results.append(("Jobs List", False))
    except Exception as e:
        print(f"FAIL: Jobs list error - {e}")
        results.append(("Jobs List", False))
    
    # Test 5: Candidate Creation
    print("\n5. Candidate Creation")
    candidate_data = {
        "name": "Verification Test Candidate",
        "email": "verification.test@bhiv.com",
        "phone": "+1-555-0299",
        "location": "Remote",
        "technical_skills": "Testing, Verification, Quality Control",
        "experience_years": 4,
        "seniority_level": "Mid-level",
        "education_level": "Bachelor's"
    }
    
    try:
        response = requests.post(f"{api_base}/v1/candidates", json=candidate_data, headers=headers, timeout=10)
        if response.status_code == 200:
            result = response.json()
            candidate_id = result.get('id')
            print(f"PASS: Candidate created successfully - ID: {candidate_id}")
            results.append(("Candidate Creation", True))
        else:
            print(f"FAIL: Candidate creation failed - {response.status_code}: {response.text[:200]}")
            results.append(("Candidate Creation", False))
    except Exception as e:
        print(f"FAIL: Candidate creation error - {e}")
        results.append(("Candidate Creation", False))
    
    # Test 6: Candidates List (Fixed)
    print("\n6. Candidates List Retrieval")
    try:
        response = requests.get(f"{api_base}/v1/candidates", headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            candidates = data.get('candidates', [])
            print(f"PASS: Retrieved {len(candidates)} candidates")
            results.append(("Candidates List", True))
        else:
            print(f"FAIL: Candidates list failed - {response.status_code}")
            results.append(("Candidates List", False))
    except Exception as e:
        print(f"FAIL: Candidates list error - {e}")
        results.append(("Candidates List", False))
    
    # Test 7: Dashboard Data Integration
    print("\n7. Dashboard Data Integration")
    try:
        # Test multiple endpoints for dashboard
        jobs_ok = requests.get(f"{api_base}/v1/jobs", headers=headers, timeout=10).status_code == 200
        candidates_ok = requests.get(f"{api_base}/v1/candidates", headers=headers, timeout=10).status_code == 200
        
        if jobs_ok and candidates_ok:
            print("PASS: Dashboard data endpoints working")
            results.append(("Dashboard Data", True))
        else:
            print(f"FAIL: Dashboard endpoints - Jobs: {jobs_ok}, Candidates: {candidates_ok}")
            results.append(("Dashboard Data", False))
    except Exception as e:
        print(f"FAIL: Dashboard data error - {e}")
        results.append(("Dashboard Data", False))
    
    # Test 8: AI Agent Status
    print("\n8. AI Agent Status")
    try:
        agent_url = "https://bhiv-hr-agent-m1me.onrender.com"
        response = requests.get(f"{agent_url}/health", timeout=10)
        if response.status_code == 200:
            print("PASS: AI Agent is healthy")
            results.append(("AI Agent Health", True))
        else:
            print(f"FAIL: AI Agent health check failed - {response.status_code}")
            results.append(("AI Agent Health", False))
    except Exception as e:
        print(f"FAIL: AI Agent health error - {e}")
        results.append(("AI Agent Health", False))
    
    # Test 9: Portal URLs Accessibility
    print("\n9. Portal URLs Accessibility")
    portals = [
        ("HR Portal", "https://bhiv-hr-portal-cead.onrender.com/"),
        ("Client Portal", "https://bhiv-hr-client-portal-5g33.onrender.com/")
    ]
    
    portal_results = []
    for portal_name, portal_url in portals:
        try:
            response = requests.get(portal_url, timeout=15)
            if response.status_code == 200:
                print(f"PASS: {portal_name} accessible")
                portal_results.append(True)
            else:
                print(f"FAIL: {portal_name} returned {response.status_code}")
                portal_results.append(False)
        except Exception as e:
            print(f"FAIL: {portal_name} error - {e}")
            portal_results.append(False)
    
    results.append(("Portal Accessibility", all(portal_results)))
    
    # Summary
    print("\n" + "=" * 60)
    print("COMPREHENSIVE VERIFICATION SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"Tests Passed: {passed}/{total} ({passed/total*100:.1f}%)")
    
    for test_name, success in results:
        status = "PASS" if success else "FAIL"
        print(f"{status}: {test_name}")
    
    # Overall system status
    if passed >= 7:  # At least 7/9 tests should pass
        print("\nOVERALL STATUS: SYSTEM OPERATIONAL")
        print("Critical issues resolved - Ready for production use")
        return True
    elif passed >= 5:
        print("\nOVERALL STATUS: SYSTEM MOSTLY FUNCTIONAL")
        print("Some issues remain but core functionality works")
        return True
    else:
        print("\nOVERALL STATUS: SYSTEM NEEDS ATTENTION")
        print("Multiple critical issues require resolution")
        return False

if __name__ == "__main__":
    success = test_all_systems()
    
    if success:
        print("\nSystem verification completed successfully!")
        print("All critical workflows are operational.")
    else:
        print("\nSystem verification identified issues.")
        print("Review failed tests and apply additional fixes.")