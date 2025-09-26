#!/usr/bin/env python3

import requests
import time
import json
from datetime import datetime

def test_service_health(name, url, timeout=15, max_retries=5):
    """Test service health with retries"""
    print(f"🔍 Testing {name}...")
    
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(f"{url}/health", timeout=timeout)
            if response.status_code == 200:
                print(f"✅ {name}: Healthy (attempt {attempt})")
                return True, response.json()
            else:
                print(f"⚠️ {name}: Status {response.status_code} (attempt {attempt})")
        except Exception as e:
            print(f"⏳ {name}: Attempt {attempt}/{max_retries} - {str(e)}")
        
        if attempt < max_retries:
            time.sleep(10)
    
    print(f"❌ {name}: Failed after {max_retries} attempts")
    return False, None

def main():
    print("🚀 BHIV HR Platform Deployment Verification")
    print("=" * 50)
    
    services = {
        "Gateway": "https://bhiv-hr-gateway-46pz.onrender.com",
        "AI Agent": "https://bhiv-hr-agent-m1me.onrender.com",
        "HR Portal": "https://bhiv-hr-portal-cead.onrender.com",
        "Client Portal": "https://bhiv-hr-client-portal-5g33.onrender.com"
    }
    
    results = {}
    
    for name, url in services.items():
        success, data = test_service_health(name, url)
        results[name] = {
            "healthy": success,
            "url": url,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
    
    print("\n📊 Deployment Summary")
    print("=" * 30)
    
    healthy_count = 0
    for name, result in results.items():
        status = "✅ Healthy" if result["healthy"] else "❌ Unhealthy"
        print(f"{name}: {status}")
        if result["healthy"]:
            healthy_count += 1
    
    print(f"\nOverall Status: {healthy_count}/{len(services)} services healthy")
    
    if healthy_count == len(services):
        print("🎉 All services are operational!")
        return 0
    else:
        print("⚠️ Some services need attention")
        return 1

if __name__ == "__main__":
    exit(main())