#!/usr/bin/env python3
"""
Complete deployment script for BHIV HR Platform fixes
Handles AI agent connectivity, database schema, and verification
"""

import requests
import os
import time
import json
from datetime import datetime

def test_service_health(service_name, url, timeout=10):
    """Test if a service is healthy"""
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            print(f"  ✅ {service_name}: Online")
            return True, response.json() if 'json' in response.headers.get('content-type', '') else None
        else:
            print(f"  ❌ {service_name}: HTTP {response.status_code}")
            return False, None
    except Exception as e:
        print(f"  ❌ {service_name}: {str(e)}")
        return False, None

def test_ai_agent():
    """Test AI agent functionality"""
    print("\n🤖 Testing AI Agent...")
    
    agent_url = "https://bhiv-hr-agent.onrender.com"
    
    # Test health
    health_ok, _ = test_service_health("AI Agent Health", f"{agent_url}/health")
    
    if health_ok:
        # Test matching
        try:
            print("  🔍 Testing AI matching...")
            match_data = {"job_id": 1}
            response = requests.post(f"{agent_url}/match", json=match_data, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                candidates = data.get("top_candidates", [])
                print(f"  ✅ AI Matching: Working ({len(candidates)} candidates)")
                return True
            else:
                print(f"  ❌ AI Matching: Failed {response.status_code}")
                return False
        except Exception as e:
            print(f"  ❌ AI Matching: {str(e)}")
            return False
    
    return False

def test_gateway_with_fallback():
    """Test gateway AI fallback functionality"""
    print("\n🌐 Testing Gateway AI Fallback...")
    
    gateway_url = "https://bhiv-hr-gateway.onrender.com"
    api_key = "myverysecureapikey123"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        # Test AI matching through gateway
        match_data = {"job_id": 1}
        response = requests.post(f"{gateway_url}/v1/match", 
                               json=match_data, 
                               headers=headers, 
                               timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            candidates = data.get("top_candidates", [])
            ai_analysis = data.get("ai_analysis", "")
            
            print(f"  ✅ Gateway AI Matching: Working ({len(candidates)} candidates)")
            print(f"  📊 Analysis: {ai_analysis}")
            return True
        else:
            print(f"  ❌ Gateway AI Matching: Failed {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Gateway AI Matching: {str(e)}")
        return False

def test_interview_scheduling():
    """Test interview scheduling"""
    print("\n📅 Testing Interview Scheduling...")
    
    gateway_url = "https://bhiv-hr-gateway.onrender.com"
    api_key = "myverysecureapikey123"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        # Test creating an interview
        interview_data = {
            "candidate_id": 1,
            "job_id": 1,
            "interview_date": "2025-01-20 14:00:00",
            "interviewer": "Test Interviewer",
            "notes": "Deployment test interview"
        }
        
        response = requests.post(f"{gateway_url}/v1/interviews", 
                               json=interview_data, 
                               headers=headers, 
                               timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            interview_id = data.get("interview_id")
            print(f"  ✅ Interview Scheduling: Working (ID: {interview_id})")
            
            # Test retrieving interviews
            response = requests.get(f"{gateway_url}/v1/interviews", 
                                  headers=headers, 
                                  timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                interviews = data.get("interviews", [])
                print(f"  ✅ Interview Retrieval: Working ({len(interviews)} interviews)")
                return True
            else:
                print(f"  ❌ Interview Retrieval: Failed {response.status_code}")
                return False
        else:
            print(f"  ❌ Interview Scheduling: Failed {response.status_code}")
            print(f"  Error: {response.text}")
            return False
    except Exception as e:
        print(f"  ❌ Interview Scheduling: {str(e)}")
        return False

def test_all_services():
    """Test all services"""
    print("\n🏥 Testing All Services...")
    
    services = {
        "Gateway": "https://bhiv-hr-gateway.onrender.com/health",
        "AI Agent": "https://bhiv-hr-agent.onrender.com/health",
        "HR Portal": "https://bhiv-hr-portal.onrender.com",
        "Client Portal": "https://bhiv-hr-client-portal.onrender.com"
    }
    
    results = {}
    for service, url in services.items():
        health_ok, _ = test_service_health(service, url)
        results[service] = health_ok
    
    return results

def wake_up_services():
    """Wake up services that might be sleeping"""
    print("\n⏰ Waking up services...")
    
    services = [
        "https://bhiv-hr-gateway.onrender.com/health",
        "https://bhiv-hr-agent.onrender.com/health",
        "https://bhiv-hr-portal.onrender.com",
        "https://bhiv-hr-client-portal.onrender.com"
    ]
    
    for url in services:
        try:
            print(f"  🔄 Pinging {url.split('/')[2]}...")
            requests.get(url, timeout=5)
            time.sleep(2)
        except:
            pass
    
    print("  ✅ Services pinged, waiting for startup...")
    time.sleep(10)

def main():
    """Main deployment function"""
    print("🚀 BHIV HR Platform - Complete Fix Deployment")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    # Step 1: Wake up services
    wake_up_services()
    
    # Step 2: Test all services
    service_results = test_all_services()
    
    # Step 3: Test AI agent
    ai_working = test_ai_agent()
    
    # Step 4: Test gateway fallback
    gateway_ai_working = test_gateway_with_fallback()
    
    # Step 5: Test interview scheduling
    interview_working = test_interview_scheduling()
    
    # Summary
    print("\n" + "=" * 60)
    print("🎯 DEPLOYMENT SUMMARY")
    print("=" * 60)
    
    all_services_up = all(service_results.values())
    
    print(f"Service Health: {'✅ All online' if all_services_up else '❌ Some offline'}")
    for service, status in service_results.items():
        print(f"  - {service}: {'✅' if status else '❌'}")
    
    print(f"\nAI Agent Direct: {'✅ Working' if ai_working else '❌ Not working'}")
    print(f"Gateway AI Fallback: {'✅ Working' if gateway_ai_working else '❌ Not working'}")
    print(f"Interview Scheduling: {'✅ Working' if interview_working else '❌ Not working'}")
    
    # Overall status
    if all_services_up and gateway_ai_working and interview_working:
        print("\n🎉 ALL SYSTEMS OPERATIONAL!")
        print("\n✅ Issues Fixed:")
        print("  - AI agent connectivity (with fallback)")
        print("  - Interview scheduling database schema")
        print("  - Service health monitoring")
        
        print("\n🌐 Platform Ready:")
        print("  - HR Portal: https://bhiv-hr-portal.onrender.com")
        print("  - Client Portal: https://bhiv-hr-client-portal.onrender.com")
        print("  - API Docs: https://bhiv-hr-gateway.onrender.com/docs")
        
    else:
        print("\n⚠️ SOME ISSUES REMAIN:")
        
        if not all_services_up:
            print("  - Service deployment issues")
        if not gateway_ai_working:
            print("  - AI matching not working properly")
        if not interview_working:
            print("  - Interview scheduling still has issues")
        
        print("\n🔧 Recommended Actions:")
        print("  1. Check Render deployment logs")
        print("  2. Verify environment variables")
        print("  3. Run database migration manually")
        print("  4. Contact support if issues persist")

if __name__ == "__main__":
    main()