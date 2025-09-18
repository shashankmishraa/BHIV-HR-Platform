#!/usr/bin/env python3
"""Final System Integration Test - All Services"""

import requests
import json
from datetime import datetime

def test_all_services():
    """Test all 5 services in production"""
    
    services = {
        "API Gateway": "https://bhiv-hr-gateway.onrender.com",
        "AI Agent": "https://bhiv-hr-agent.onrender.com", 
        "HR Portal": "https://bhiv-hr-portal.onrender.com",
        "Client Portal": "https://bhiv-hr-client-portal.onrender.com"
    }
    
    print("🚀 BHIV HR Platform - Final System Test")
    print("=" * 50)
    
    results = {}
    
    for service_name, url in services.items():
        print(f"\n🔍 Testing {service_name}...")
        
        try:
            # Test health endpoint
            health_url = f"{url}/health" if "portal" not in url else url
            response = requests.get(health_url, timeout=15)
            
            if response.status_code == 200:
                print(f"✅ {service_name}: OPERATIONAL")
                results[service_name] = "✅ OPERATIONAL"
            else:
                print(f"⚠️ {service_name}: Status {response.status_code}")
                results[service_name] = f"⚠️ Status {response.status_code}"
                
        except Exception as e:
            print(f"❌ {service_name}: ERROR - {str(e)[:50]}...")
            results[service_name] = "❌ ERROR"
    
    # Test API Authentication
    print(f"\n🔐 Testing API Authentication...")
    try:
        headers = {"Authorization": "Bearer myverysecureapikey123"}
        response = requests.get(f"{services['API Gateway']}/v1/jobs", headers=headers, timeout=10)
        if response.status_code == 200:
            print("✅ API Authentication: WORKING")
            results["Authentication"] = "✅ WORKING"
        else:
            print(f"⚠️ API Authentication: Status {response.status_code}")
            results["Authentication"] = f"⚠️ Status {response.status_code}"
    except Exception as e:
        print(f"❌ API Authentication: ERROR")
        results["Authentication"] = "❌ ERROR"
    
    # Summary
    print(f"\n📊 FINAL SYSTEM STATUS")
    print("=" * 50)
    for service, status in results.items():
        print(f"{service:20}: {status}")
    
    operational_count = sum(1 for status in results.values() if "✅" in status)
    total_count = len(results)
    
    print(f"\n🎯 System Health: {operational_count}/{total_count} services operational")
    print(f"📅 Test completed: {datetime.now()}")
    
    if operational_count == total_count:
        print("\n🎉 ALL SYSTEMS OPERATIONAL - PLATFORM READY!")
    else:
        print(f"\n⚠️ {total_count - operational_count} services need attention")

if __name__ == "__main__":
    test_all_services()