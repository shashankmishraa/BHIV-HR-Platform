#!/usr/bin/env python3
"""Trigger Deployments and Monitor Status"""

import subprocess
import requests
import time
from datetime import datetime

def trigger_all_deployments():
    """Trigger deployments for all 4 services using curl"""
    
    triggers = {
        "HR Portal": "https://api.render.com/deploy/srv-d2s5vtje5dus73cr0s90?key=POyxo7foEVs",
        "Client Portal": "https://api.render.com/deploy/srv-d2s67pffte5s739kp99g?key=C04znxCoOwE", 
        "API Gateway": "https://api.render.com/deploy/srv-d2s0a6mmcj7s73fn3iqg?key=EwZutgywDXg",
        "AI Agent": "https://api.render.com/deploy/srv-d2s0dp3e5dus73cl3a20?key=w7R-2dV-_FE"
    }
    
    print("Triggering deployments for all services...")
    print("=" * 50)
    
    for service, url in triggers.items():
        print(f"Triggering {service}...")
        try:
            result = subprocess.run([
                "curl", "-X", "POST", url
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print(f"SUCCESS: {service} deployment triggered")
            else:
                print(f"ERROR: {service} trigger failed - {result.stderr}")
                
        except Exception as e:
            print(f"ERROR: {service} - {e}")
    
    print(f"\nAll deployment triggers sent at: {datetime.now()}")
    print("Waiting 2 minutes for deployments to start...")
    time.sleep(120)

def monitor_services():
    """Monitor all services after deployment"""
    
    services = {
        "API Gateway": "https://bhiv-hr-gateway.onrender.com/health",
        "AI Agent": "https://bhiv-hr-agent.onrender.com/health",
        "HR Portal": "https://bhiv-hr-portal.onrender.com",
        "Client Portal": "https://bhiv-hr-client-portal.onrender.com"
    }
    
    print("\nMonitoring service health...")
    print("=" * 50)
    
    results = {}
    
    for service_name, url in services.items():
        print(f"Testing {service_name}...")
        
        try:
            start_time = time.time()
            response = requests.get(url, timeout=15)
            response_time = round((time.time() - start_time) * 1000, 2)
            
            if response.status_code == 200:
                print(f"SUCCESS: {service_name} - {response_time}ms")
                results[service_name] = "OPERATIONAL"
            else:
                print(f"WARNING: {service_name} - Status {response.status_code}")
                results[service_name] = f"Status {response.status_code}"
                
        except Exception as e:
            print(f"ERROR: {service_name} - {str(e)[:50]}...")
            results[service_name] = "ERROR"
    
    return results

def check_agent_upgrades():
    """Check AI Agent upgrades specifically"""
    print("\nChecking AI Agent upgrades...")
    
    try:
        response = requests.get("https://bhiv-hr-agent.onrender.com/metrics", timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            if "performance_metrics" in data and "cpu_usage_percent" in data["performance_metrics"]:
                metrics = data["performance_metrics"]
                print("SUCCESS: Real system metrics deployed")
                print(f"  CPU: {metrics.get('cpu_usage_percent')}%")
                print(f"  Memory: {metrics.get('memory_usage_mb')} MB")
                return True
            else:
                print("WARNING: Metrics not upgraded yet")
                return False
        else:
            print(f"ERROR: Metrics endpoint returned {response.status_code}")
            return False
            
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_api_auth():
    """Test API authentication"""
    print("\nTesting API authentication...")
    
    try:
        headers = {"Authorization": "Bearer myverysecureapikey123"}
        response = requests.get("https://bhiv-hr-gateway.onrender.com/v1/jobs", headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("SUCCESS: API authentication working")
            return True
        else:
            print(f"WARNING: API returned {response.status_code}")
            return False
            
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def main():
    """Main deployment workflow"""
    print("BHIV HR Platform - Deployment Trigger")
    print(f"Started at: {datetime.now()}")
    print("=" * 50)
    
    # Step 1: Trigger all deployments
    trigger_all_deployments()
    
    # Step 2: Monitor services
    results = monitor_services()
    
    # Step 3: Check agent upgrades
    agent_upgraded = check_agent_upgrades()
    
    # Step 4: Test API
    api_working = test_api_auth()
    
    # Summary
    print(f"\nDEPLOYMENT SUMMARY")
    print("=" * 50)
    
    operational = sum(1 for status in results.values() if status == "OPERATIONAL")
    total = len(results)
    
    print(f"Services: {operational}/{total} operational")
    print(f"Agent Upgrades: {'DEPLOYED' if agent_upgraded else 'PENDING'}")
    print(f"API Auth: {'WORKING' if api_working else 'ISSUES'}")
    
    for service, status in results.items():
        print(f"{service:15}: {status}")
    
    print(f"\nCompleted: {datetime.now()}")
    
    if operational == total and agent_upgraded and api_working:
        print("\nALL DEPLOYMENTS SUCCESSFUL!")
    else:
        print("\nSome issues detected")

if __name__ == "__main__":
    main()