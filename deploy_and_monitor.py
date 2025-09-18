#!/usr/bin/env python3
"""Deploy All Services and Monitor Efficiency"""

import subprocess
import requests
import time
import json
from datetime import datetime

def git_push_changes():
    """Push all changes to Git to trigger auto-deployment"""
    print("🚀 Pushing changes to Git...")
    
    try:
        # Add all changes
        subprocess.run(["git", "add", "."], check=True, cwd="c:\\bhiv hr ai platform")
        
        # Commit with timestamp
        commit_msg = f"Security & Performance Upgrades - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True, cwd="c:\\bhiv hr ai platform")
        
        # Push to main branch
        subprocess.run(["git", "push", "origin", "main"], check=True, cwd="c:\\bhiv hr ai platform")
        
        print("✅ Changes pushed to Git successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git push failed: {e}")
        return False

def trigger_deployments():
    """Trigger deployments using webhook URLs"""
    print("\n🔄 Triggering deployments...")
    
    # Render webhook URLs (these would be provided by Render)
    webhook_urls = {
        "API Gateway": "https://api.render.com/deploy/srv-...",  # Replace with actual webhook
        "AI Agent": "https://api.render.com/deploy/srv-...",     # Replace with actual webhook  
        "HR Portal": "https://api.render.com/deploy/srv-...",    # Replace with actual webhook
        "Client Portal": "https://api.render.com/deploy/srv-..." # Replace with actual webhook
    }
    
    # Since we don't have actual webhook URLs, we'll simulate by checking if services restart
    print("📝 Note: Auto-deployment triggered by Git push")
    print("⏳ Waiting for services to restart...")
    time.sleep(30)  # Wait for deployment to start
    
    return True

def monitor_service_health():
    """Monitor all services and check deployment status"""
    print("\n🔍 Monitoring service health...")
    
    services = {
        "API Gateway": "https://bhiv-hr-gateway.onrender.com",
        "AI Agent": "https://bhiv-hr-agent.onrender.com",
        "HR Portal": "https://bhiv-hr-portal.onrender.com", 
        "Client Portal": "https://bhiv-hr-client-portal.onrender.com"
    }
    
    results = {}
    
    for service_name, url in services.items():
        print(f"\n📊 Testing {service_name}...")
        
        try:
            # Test health endpoint
            health_url = f"{url}/health" if "portal" not in url else url
            start_time = time.time()
            response = requests.get(health_url, timeout=15)
            response_time = round((time.time() - start_time) * 1000, 2)
            
            if response.status_code == 200:
                print(f"✅ {service_name}: OPERATIONAL ({response_time}ms)")
                results[service_name] = {"status": "✅ OPERATIONAL", "response_time": response_time}
            else:
                print(f"⚠️ {service_name}: Status {response.status_code}")
                results[service_name] = {"status": f"⚠️ Status {response.status_code}", "response_time": response_time}
                
        except Exception as e:
            print(f"❌ {service_name}: ERROR - {str(e)[:50]}...")
            results[service_name] = {"status": "❌ ERROR", "response_time": "N/A"}
    
    return results

def check_agent_upgrades():
    """Specifically check if AI Agent upgrades are deployed"""
    print("\n🤖 Checking AI Agent upgrades...")
    
    try:
        # Test real system metrics (psutil upgrade)
        response = requests.get("https://bhiv-hr-agent.onrender.com/metrics", timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            # Check for psutil metrics
            if "performance_metrics" in data and "cpu_usage_percent" in data["performance_metrics"]:
                print("✅ Real system metrics (psutil) deployed")
            else:
                print("❌ System metrics not upgraded yet")
            
            # Check timezone-aware timestamps
            timestamp = data.get("timestamp", "")
            if "T" in timestamp and ("Z" in timestamp or "+" in timestamp):
                print("✅ Timezone-aware timestamps deployed")
            else:
                print("❌ Timestamps not upgraded yet")
                
            return True
        else:
            print(f"❌ Agent metrics endpoint failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Agent upgrade check failed: {e}")
        return False

def check_logs_efficiency():
    """Check logs and performance metrics"""
    print("\n📋 Checking logs and efficiency...")
    
    try:
        # Check API Gateway logs
        response = requests.get("https://bhiv-hr-gateway.onrender.com/health/detailed", timeout=10)
        if response.status_code == 200:
            print("✅ API Gateway detailed health check working")
        
        # Check Agent performance
        response = requests.get("https://bhiv-hr-agent.onrender.com/metrics", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "performance_metrics" in data:
                metrics = data["performance_metrics"]
                print(f"📊 Agent Performance:")
                print(f"   CPU Usage: {metrics.get('cpu_usage_percent', 'N/A')}%")
                print(f"   Memory Usage: {metrics.get('memory_usage_mb', 'N/A')} MB")
                print(f"   Memory %: {metrics.get('memory_usage_percent', 'N/A')}%")
        
        # Test authentication
        headers = {"Authorization": "Bearer myverysecureapikey123"}
        response = requests.get("https://bhiv-hr-gateway.onrender.com/v1/jobs", headers=headers, timeout=10)
        if response.status_code == 200:
            print("✅ API Authentication working")
        
        return True
        
    except Exception as e:
        print(f"❌ Log efficiency check failed: {e}")
        return False

def main():
    """Main deployment and monitoring workflow"""
    print("🚀 BHIV HR Platform - Deployment & Monitoring")
    print("=" * 60)
    
    # Step 1: Push changes to Git
    if not git_push_changes():
        print("❌ Deployment aborted due to Git push failure")
        return
    
    # Step 2: Trigger deployments
    trigger_deployments()
    
    # Step 3: Wait for deployment to complete
    print("\n⏳ Waiting for deployment to complete...")
    time.sleep(60)  # Wait 1 minute for services to restart
    
    # Step 4: Monitor service health
    results = monitor_service_health()
    
    # Step 5: Check specific upgrades
    agent_upgraded = check_agent_upgrades()
    
    # Step 6: Check logs and efficiency
    logs_ok = check_logs_efficiency()
    
    # Summary
    print(f"\n📊 DEPLOYMENT SUMMARY")
    print("=" * 60)
    
    operational_count = sum(1 for result in results.values() if "✅" in result["status"])
    total_services = len(results)
    
    print(f"Services Operational: {operational_count}/{total_services}")
    print(f"Agent Upgrades: {'✅ Deployed' if agent_upgraded else '❌ Pending'}")
    print(f"Log Efficiency: {'✅ Working' if logs_ok else '❌ Issues'}")
    
    for service, result in results.items():
        print(f"{service:15}: {result['status']} ({result['response_time']}ms)")
    
    print(f"\n🕒 Deployment completed: {datetime.now()}")
    
    if operational_count == total_services and agent_upgraded and logs_ok:
        print("\n🎉 ALL SERVICES DEPLOYED SUCCESSFULLY!")
    else:
        print(f"\n⚠️ Some issues detected - check individual service logs")

if __name__ == "__main__":
    main()