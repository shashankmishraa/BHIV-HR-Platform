#!/usr/bin/env python3
"""
BHIV HR Platform - Issue Diagnosis Script
Systematically checks all components and identifies specific problems
"""

import requests
import os
import json
import time
from datetime import datetime

def check_service_health(service_name, url, timeout=10):
    """Check if a service is responding"""
    print(f"🔍 Checking {service_name}...")
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            print(f"  ✅ {service_name}: Online (Status: {response.status_code})")
            return True, response.json() if 'json' in response.headers.get('content-type', '') else response.text
        else:
            print(f"  ❌ {service_name}: Error {response.status_code}")
            return False, f"HTTP {response.status_code}: {response.text[:200]}"
    except requests.exceptions.ConnectTimeout:
        print(f"  ❌ {service_name}: Connection timeout")
        return False, "Connection timeout"
    except requests.exceptions.ConnectionError as e:
        print(f"  ❌ {service_name}: Connection failed")
        return False, f"Connection error: {str(e)}"
    except Exception as e:
        print(f"  ❌ {service_name}: Unexpected error")
        return False, f"Error: {str(e)}"

def test_ai_agent_endpoints():
    """Test AI agent specific endpoints"""
    print("\n🤖 Testing AI Agent Endpoints...")
    
    base_url = "https://bhiv-hr-agent.onrender.com"
    
    # Test health endpoint
    health_ok, health_data = check_service_health("AI Agent Health", f"{base_url}/health")
    
    if health_ok:
        # Test match endpoint
        print("🔍 Testing AI matching endpoint...")
        try:
            match_data = {"job_id": 1}
            response = requests.post(f"{base_url}/match", json=match_data, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                candidates = data.get("top_candidates", [])
                print(f"  ✅ AI Matching: Working ({len(candidates)} candidates)")
                return True
            else:
                print(f"  ❌ AI Matching: Failed {response.status_code}")
                print(f"  Error: {response.text}")
                return False
        except Exception as e:
            print(f"  ❌ AI Matching: Exception {str(e)}")
            return False
    
    return False

def test_gateway_endpoints():
    """Test gateway endpoints"""
    print("\n🌐 Testing Gateway Endpoints...")
    
    base_url = "https://bhiv-hr-gateway.onrender.com"
    api_key = "myverysecureapikey123"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    # Test health
    health_ok, _ = check_service_health("Gateway Health", f"{base_url}/health")
    
    if health_ok:
        # Test protected endpoint
        print("🔍 Testing protected endpoints...")
        try:
            response = requests.get(f"{base_url}/test-candidates", headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"  ✅ Database: Connected ({data.get('total_candidates', 0)} candidates)")
            else:
                print(f"  ❌ Database: Failed {response.status_code}")
        except Exception as e:
            print(f"  ❌ Database: Exception {str(e)}")
    
    return health_ok

def test_portal_connectivity():
    """Test portal connectivity to services"""
    print("\n🖥️ Testing Portal Connectivity...")
    
    # Test HR Portal
    portal_ok, _ = check_service_health("HR Portal", "https://bhiv-hr-portal.onrender.com")
    
    # Test Client Portal  
    client_ok, _ = check_service_health("Client Portal", "https://bhiv-hr-client-portal.onrender.com")
    
    return portal_ok and client_ok

def check_database_schema():
    """Check database schema issues"""
    print("\n🗄️ Checking Database Schema...")
    
    try:
        gateway_url = "https://bhiv-hr-gateway.onrender.com"
        api_key = "myverysecureapikey123"
        headers = {"Authorization": f"Bearer {api_key}"}
        
        # Test interview creation (this will fail if schema is wrong)
        interview_data = {
            "candidate_id": 1,
            "job_id": 1,
            "interview_date": "2025-01-15 10:00:00",
            "interviewer": "Test User",
            "notes": "Schema test"
        }
        
        response = requests.post(f"{gateway_url}/v1/interviews", 
                               json=interview_data, 
                               headers=headers, 
                               timeout=10)
        
        if response.status_code == 200:
            print("  ✅ Database Schema: Interview table OK")
            return True
        else:
            print(f"  ❌ Database Schema: Interview creation failed")
            print(f"  Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"  ❌ Database Schema: Exception {str(e)}")
        return False

def main():
    """Main diagnosis function"""
    print("🔍 BHIV HR Platform - System Diagnosis")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    issues = []
    
    # Test all components
    gateway_ok = test_gateway_endpoints()
    if not gateway_ok:
        issues.append("Gateway API not responding")
    
    ai_ok = test_ai_agent_endpoints()
    if not ai_ok:
        issues.append("AI Agent not working properly")
    
    portal_ok = test_portal_connectivity()
    if not portal_ok:
        issues.append("Portal services not accessible")
    
    schema_ok = check_database_schema()
    if not schema_ok:
        issues.append("Database schema issues")
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 DIAGNOSIS SUMMARY")
    print("=" * 60)
    
    if not issues:
        print("🎉 All systems operational!")
    else:
        print("❌ Issues found:")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
        
        print("\n🔧 Recommended fixes:")
        if "AI Agent not working properly" in issues:
            print("  - Check AI agent service deployment on Render")
            print("  - Verify AI agent is not sleeping (free tier limitation)")
            print("  - Test AI agent URL directly in browser")
        
        if "Database schema issues" in issues:
            print("  - Run database migration script")
            print("  - Check if interviewer column exists in interviews table")
        
        if "Gateway API not responding" in issues:
            print("  - Check gateway service deployment")
            print("  - Verify environment variables are set")
        
        if "Portal services not accessible" in issues:
            print("  - Check portal deployments on Render")
            print("  - Verify portal configuration")

if __name__ == "__main__":
    main()