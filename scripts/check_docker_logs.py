#!/usr/bin/env python3
"""Check Docker deployment logs for gateway service issues"""

import subprocess
import sys
import json
from datetime import datetime

def run_command(cmd):
    """Run command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", "Command timed out", 1
    except Exception as e:
        return "", str(e), 1

def check_docker_status():
    """Check Docker container status"""
    print("🔍 Checking Docker container status...")
    
    # Check if containers are running
    stdout, stderr, code = run_command("docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'")
    if code == 0:
        print("Running containers:")
        print(stdout)
    else:
        print(f"Error checking containers: {stderr}")
    
    # Check all containers (including stopped)
    stdout, stderr, code = run_command("docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Image}}'")
    if code == 0:
        print("\nAll containers:")
        print(stdout)

def check_gateway_logs():
    """Check gateway service logs"""
    print("\n🔍 Checking gateway service logs...")
    
    # Try different container names
    container_names = [
        "bhiv-hr-platform-gateway-1",
        "gateway",
        "bhiv_hr_platform_gateway_1",
        "bhiv-hr-platform_gateway_1"
    ]
    
    for container_name in container_names:
        print(f"\nTrying container: {container_name}")
        stdout, stderr, code = run_command(f"docker logs --tail=50 {container_name}")
        
        if code == 0:
            print(f"✅ Found logs for {container_name}:")
            print("=" * 60)
            print(stdout)
            if stderr:
                print("\nSTDERR:")
                print(stderr)
            print("=" * 60)
            return True
        else:
            print(f"❌ No container found: {container_name}")
    
    return False

def check_compose_logs():
    """Check docker-compose logs"""
    print("\n🔍 Checking docker-compose logs...")
    
    stdout, stderr, code = run_command("docker-compose -f docker-compose.production.yml logs gateway --tail=50")
    if code == 0:
        print("Gateway service logs:")
        print("=" * 60)
        print(stdout)
        if stderr:
            print("\nSTDERR:")
            print(stderr)
        print("=" * 60)
    else:
        print(f"Error getting compose logs: {stderr}")

def check_health():
    """Check service health"""
    print("\n🔍 Checking service health...")
    
    # Try to curl the health endpoint
    stdout, stderr, code = run_command("curl -s http://localhost:8000/health")
    if code == 0:
        print("Health endpoint response:")
        print(stdout)
    else:
        print(f"Health check failed: {stderr}")

def analyze_import_issues():
    """Check for common import issues"""
    print("\n🔍 Analyzing potential import issues...")
    
    # Check if the workflow_engine import is causing issues
    print("Checking workflow_engine import...")
    stdout, stderr, code = run_command("python -c 'import sys; sys.path.append(\"services/gateway\"); from app.workflow_engine import workflow_engine'")
    if code != 0:
        print(f"❌ workflow_engine import failed: {stderr}")
        
        # Try alternative import
        stdout2, stderr2, code2 = run_command("python -c 'import sys; sys.path.append(\"services/gateway/app\"); from workflow_engine import workflow_engine'")
        if code2 != 0:
            print(f"❌ Alternative workflow_engine import also failed: {stderr2}")
        else:
            print("✅ Alternative import works")
    else:
        print("✅ workflow_engine import works")

def main():
    """Main diagnostic function"""
    print("🚀 Docker Gateway Service Diagnostic")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    check_docker_status()
    
    # Try to get logs from different sources
    if not check_gateway_logs():
        check_compose_logs()
    
    check_health()
    analyze_import_issues()
    
    print("\n" + "=" * 50)
    print("Diagnostic complete. Check the logs above for import errors or startup issues.")

if __name__ == "__main__":
    main()