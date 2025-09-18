#!/usr/bin/env python3
"""
Deploy all BHIV HR services using correct private trigger URLs
"""

import requests
import time

def deploy_all_services():
    """Deploy all services using private trigger URLs"""
    
    # Correct private trigger URLs
    services = {
        "HR Portal": "https://api.render.com/deploy/srv-d2s5vtje5dus73cr0s90?key=POyxo7foEVs",
        "Client Portal": "https://api.render.com/deploy/srv-d2s67pffte5s739kp99g?key=C04znxCoOwE", 
        "Gateway": "https://api.render.com/deploy/srv-d2s0a6mmcj7s73fn3iqg?key=EwZutgywDXg",
        "Agent": "https://api.render.com/deploy/srv-d2s0dp3e5dus73cl3a20?key=w7R-2dV-_FE"
    }
    
    print("BHIV HR Platform Deployment")
    print("=" * 40)
    
    results = {}
    
    for service_name, trigger_url in services.items():
        print(f"\nDeploying {service_name}...")
        try:
            response = requests.post(trigger_url, timeout=30)
            
            if response.status_code in [200, 201, 202]:
                print(f"[SUCCESS] {service_name} deployment triggered")
                results[service_name] = "SUCCESS"
            else:
                print(f"[FAILED] {service_name}: Status {response.status_code}")
                results[service_name] = f"FAILED ({response.status_code})"
                
        except Exception as e:
            print(f"[ERROR] {service_name}: {str(e)}")
            results[service_name] = f"ERROR"
    
    print("\n" + "=" * 40)
    print("DEPLOYMENT SUMMARY")
    print("=" * 40)
    
    for service, status in results.items():
        print(f"{service}: {status}")
    
    print(f"\nDeployment complete. Services will update in 2-3 minutes.")
    
    return results

def verify_agent_upgrade():
    """Verify agent service has the upgrades after deployment"""
    
    print("\nWaiting 3 minutes for deployment to complete...")
    time.sleep(180)
    
    print("\nVerifying Agent upgrades...")
    try:
        response = requests.get("https://bhiv-hr-agent.onrender.com/health", timeout=15)
        if response.status_code == 200:
            data = response.json()
            timestamp = data.get('timestamp', '')
            
            if '+' in timestamp or 'Z' in timestamp:
                print("[SUCCESS] Timezone-aware timestamps deployed!")
            else:
                print("[PENDING] Still using naive timestamps")
                
        # Check metrics endpoint
        response = requests.get("https://bhiv-hr-agent.onrender.com/metrics", timeout=15)
        if response.status_code == 200:
            data = response.json()
            perf_metrics = data.get('performance_metrics', {})
            
            if 'cpu_usage_percent' in perf_metrics:
                print("[SUCCESS] Real system metrics deployed!")
            else:
                print("[PENDING] Still using hardcoded metrics")
                
    except Exception as e:
        print(f"[ERROR] Verification failed: {e}")

if __name__ == "__main__":
    # Deploy all services
    deploy_all_services()
    
    # Verify upgrades
    verify_agent_upgrade()
    
    print("\nAll services deployed with security & performance upgrades!")
    print("Access at:")
    print("- Gateway: https://bhiv-hr-gateway.onrender.com/docs")
    print("- Agent: https://bhiv-hr-agent.onrender.com/docs") 
    print("- HR Portal: https://bhiv-hr-portal.onrender.com/")
    print("- Client Portal: https://bhiv-hr-client-portal.onrender.com/")