#!/usr/bin/env python3
"""
Quick Deploy Script - Push and verify deployment
"""

import subprocess
import time
import requests
import sys

def run_command(cmd):
    """Run shell command and return result"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_service_health(name, url):
    """Check if service is healthy"""
    try:
        response = requests.get(f"{url}/health", timeout=10)
        if response.status_code == 200:
            print(f"✅ {name}: Healthy")
            return True
        else:
            print(f"❌ {name}: Unhealthy ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ {name}: Error - {str(e)}")
        return False

def main():
    print("🚀 Quick Deploy & Health Check")
    print("=" * 50)
    
    # 1. Add and commit changes
    print("📝 Adding changes...")
    success, stdout, stderr = run_command("git add .")
    if not success:
        print(f"❌ Git add failed: {stderr}")
        return 1
    
    # 2. Commit with timestamp
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"🚀 Quick deploy - {timestamp}"
    
    print("💾 Committing changes...")
    success, stdout, stderr = run_command(f'git commit -m "{commit_msg}"')
    if not success and "nothing to commit" not in stderr:
        print(f"❌ Git commit failed: {stderr}")
        return 1
    
    # 3. Push to main
    print("📤 Pushing to main...")
    success, stdout, stderr = run_command("git push origin main")
    if not success:
        print(f"❌ Git push failed: {stderr}")
        return 1
    
    print("✅ Code pushed successfully!")
    
    # 4. Wait for deployment
    print("⏳ Waiting for Render deployment (60 seconds)...")
    time.sleep(60)
    
    # 5. Health checks
    print("🔍 Running health checks...")
    
    services = {
        "Gateway": "https://bhiv-hr-gateway-901a.onrender.com",
        "AI Agent": "https://bhiv-hr-agent-o6nx.onrender.com"
    }
    
    all_healthy = True
    for name, url in services.items():
        if not check_service_health(name, url):
            all_healthy = False
    
    # 6. Final status
    if all_healthy:
        print("\n🎉 Deployment successful! All services are healthy.")
        print("🔗 Gateway: https://bhiv-hr-gateway-901a.onrender.com")
        print("🔗 AI Agent: https://bhiv-hr-agent-o6nx.onrender.com")
        return 0
    else:
        print("\n❌ Deployment completed but some services are unhealthy.")
        return 1

if __name__ == "__main__":
    sys.exit(main())