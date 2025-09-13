#!/usr/bin/env python3
"""
Quick verification script for BHIV HR Platform fixes
Tests both AI agent connectivity and database schema
"""

import requests
import os
import json
from datetime import datetime

def test_ai_matching():
    """Test AI matching functionality"""
    print("🤖 Testing AI Matching...")
    
    agent_url = "https://bhiv-hr-agent.onrender.com"
    
    try:
        # Test health endpoint
        response = requests.get(f"{agent_url}/health", timeout=10)
        if response.status_code == 200:
            print("  ✅ AI Agent health check passed")
            
            # Test matching endpoint
            match_data = {"job_id": 1}
            response = requests.post(f"{agent_url}/match", json=match_data, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                candidates = data.get("top_candidates", [])
                print(f"  ✅ AI Matching working: {len(candidates)} candidates returned")
                return True
            else:
                print(f"  ❌ AI Matching failed: {response.status_code}")
                print(f"  Error: {response.text}")
        else:
            print(f"  ❌ AI Agent health check failed: {response.status_code}")
            
    except Exception as e:
        print(f"  ❌ AI Agent connection error: {str(e)}")
    
    return False

def test_interview_scheduling():
    """Test interview scheduling functionality"""
    print("📅 Testing Interview Scheduling...")
    
    gateway_url = "https://bhiv-hr-gateway.onrender.com"
    api_key = "myverysecureapikey123"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        # Test creating an interview
        interview_data = {
            "candidate_id": 1,
            "job_id": 1,
            "interview_date": "2025-01-15 10:00:00",
            "interviewer": "Test Interviewer",
            "notes": "Test interview scheduling"
        }
        
        response = requests.post(f"{gateway_url}/v1/interviews", 
                               json=interview_data, 
                               headers=headers, 
                               timeout=10)
        
        if response.status_code == 200:
            print("  ✅ Interview scheduling working")
            
            # Test retrieving interviews
            response = requests.get(f"{gateway_url}/v1/interviews", 
                                  headers=headers, 
                                  timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                interviews = data.get("interviews", [])
                print(f"  ✅ Interview retrieval working: {len(interviews)} interviews found")
                return True
            else:
                print(f"  ❌ Interview retrieval failed: {response.status_code}")
        else:
            print(f"  ❌ Interview scheduling failed: {response.status_code}")
            print(f"  Error: {response.text}")
            
    except Exception as e:
        print(f"  ❌ Interview scheduling error: {str(e)}")
    
    return False

def test_system_health():
    """Test overall system health"""
    print("🏥 Testing System Health...")
    
    services = {
        "API Gateway": "https://bhiv-hr-gateway.onrender.com/health",
        "AI Agent": "https://bhiv-hr-agent.onrender.com/health",
        "HR Portal": "https://bhiv-hr-portal.onrender.com",
        "Client Portal": "https://bhiv-hr-client-portal.onrender.com"
    }
    
    results = {}
    
    for service, url in services.items():
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"  ✅ {service}: Online")
                results[service] = True
            else:
                print(f"  ❌ {service}: Error {response.status_code}")
                results[service] = False
        except Exception as e:
            print(f"  ❌ {service}: Connection failed")
            results[service] = False
    
    return results

def main():
    """Main verification function"""
    print("🔍 BHIV HR Platform - Fix Verification")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    # Test system health
    health_results = test_system_health()
    print()
    
    # Test AI matching (Issue 1 fix)
    ai_working = test_ai_matching()
    print()
    
    # Test interview scheduling (Issue 2 fix)
    interview_working = test_interview_scheduling()
    print()
    
    # Summary
    print("=" * 50)
    print("🎯 Verification Summary:")
    print()
    
    all_services_up = all(health_results.values())
    print(f"System Health: {'✅ All services online' if all_services_up else '❌ Some services down'}")
    print(f"AI Matching: {'✅ Working' if ai_working else '❌ Not working'}")
    print(f"Interview Scheduling: {'✅ Working' if interview_working else '❌ Not working'}")
    
    if all_services_up and ai_working and interview_working:
        print("\n🎉 All fixes verified successfully!")
        print("\nThe platform is ready for use:")
        print("- HR Portal: https://bhiv-hr-portal.onrender.com")
        print("- Client Portal: https://bhiv-hr-client-portal.onrender.com")
        print("- API Docs: https://bhiv-hr-gateway.onrender.com/docs")
    else:
        print("\n⚠️ Some issues remain:")
        
        if not all_services_up:
            print("- Check service deployment status on Render")
        if not ai_working:
            print("- AI Agent connection or matching logic needs attention")
        if not interview_working:
            print("- Database schema or interview API needs attention")

if __name__ == "__main__":
    main()