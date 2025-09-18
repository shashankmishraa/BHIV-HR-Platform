#!/usr/bin/env python3
"""Monitor Deployment Status - Simple Version"""

import requests
import time
import json
from datetime import datetime

def monitor_all_services():
    """Monitor all services after deployment"""
    print("BHIV HR Platform - Deployment Monitoring")
    print("=" * 50)
    
    services = {
        "API Gateway": "https://bhiv-hr-gateway.onrender.com",
        "AI Agent": "https://bhiv-hr-agent.onrender.com",
        "HR Portal": "https://bhiv-hr-portal.onrender.com", 
        "Client Portal": "https://bhiv-hr-client-portal.onrender.com"
    }
    
    print("Waiting 30 seconds for deployment to start...")
    time.sleep(30)
    
    results = {}
    
    for service_name, url in services.items():
        print(f"\nTesting {service_name}...")
        
        try:
            health_url = f"{url}/health" if "portal" not in url else url
            start_time = time.time()
            response = requests.get(health_url, timeout=15)
            response_time = round((time.time() - start_time) * 1000, 2)
            
            if response.status_code == 200:
                print(f"SUCCESS: {service_name} - {response_time}ms")
                results[service_name] = {"status": "OPERATIONAL", "time": response_time}
            else:
                print(f"WARNING: {service_name} - Status {response.status_code}")
                results[service_name] = {"status": f"Status {response.status_code}", "time": response_time}
                
        except Exception as e:
            print(f"ERROR: {service_name} - {str(e)[:50]}...")
            results[service_name] = {"status": "ERROR", "time": "N/A"}
    
    return results

def check_agent_upgrades():
    """Check if AI Agent upgrades are deployed"""
    print("\nChecking AI Agent upgrades...")
    
    try:
        response = requests.get("https://bhiv-hr-agent.onrender.com/metrics", timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            # Check for psutil metrics
            if "performance_metrics" in data and "cpu_usage_percent" in data["performance_metrics"]:
                print("SUCCESS: Real system metrics (psutil) deployed")
                
                # Show actual metrics
                metrics = data["performance_metrics"]
                print(f"  CPU Usage: {metrics.get('cpu_usage_percent', 'N/A')}%")
                print(f"  Memory Usage: {metrics.get('memory_usage_mb', 'N/A')} MB")
                print(f"  Memory Percent: {metrics.get('memory_usage_percent', 'N/A')}%")
                return True
            else:
                print("WARNING: System metrics not upgraded yet")
                return False
                
    except Exception as e:
        print(f"ERROR: Agent upgrade check failed - {e}")
        return False

def test_api_functionality():
    """Test API functionality with authentication"""
    print("\nTesting API functionality...")
    
    try:
        # Test authentication
        headers = {"Authorization": "Bearer myverysecureapikey123"}
        response = requests.get("https://bhiv-hr-gateway.onrender.com/v1/jobs", headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("SUCCESS: API Authentication working")
            return True
        else:
            print(f"WARNING: API returned status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"ERROR: API test failed - {e}")
        return False

def main():
    """Main monitoring workflow"""
    print(f"Deployment started at: {datetime.now()}")
    
    # Monitor services
    results = monitor_all_services()
    
    # Check agent upgrades
    agent_upgraded = check_agent_upgrades()
    
    # Test API
    api_working = test_api_functionality()
    
    # Summary
    print(f"\nDEPLOYMENT SUMMARY")
    print("=" * 50)
    
    operational_count = sum(1 for result in results.values() if result["status"] == "OPERATIONAL")
    total_services = len(results)
    
    print(f"Services Operational: {operational_count}/{total_services}")
    print(f"Agent Upgrades: {'DEPLOYED' if agent_upgraded else 'PENDING'}")
    print(f"API Functionality: {'WORKING' if api_working else 'ISSUES'}")
    
    for service, result in results.items():
        print(f"{service:15}: {result['status']} ({result['time']}ms)")
    
    print(f"\nMonitoring completed: {datetime.now()}")
    
    if operational_count == total_services and agent_upgraded and api_working:
        print("\nALL SERVICES DEPLOYED SUCCESSFULLY!")
    else:
        print(f"\nSome issues detected - check individual services")

if __name__ == "__main__":
    main()