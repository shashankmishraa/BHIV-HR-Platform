#!/usr/bin/env python3
"""
BHIV HR Platform - Quick Start Script
Automated setup and verification for new users
"""

import subprocess
import time
import requests
import sys
import os

def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=os.path.dirname(os.path.dirname(__file__)))
        if result.returncode == 0:
            print(f"[SUCCESS] {description} completed successfully")
            return True
        else:
            print(f"[ERROR] {description} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"[ERROR] {description} failed: {str(e)}")
        return False

def check_service(url, name):
    """Check if a service is responding"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"[SUCCESS] {name} is running")
            return True
        else:
            print(f"[ERROR] {name} returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERROR] {name} is not accessible: {str(e)}")
        return False

def main():
    print("BHIV HR Platform - Quick Start")
    print("=" * 50)
    
    # Step 1: Check prerequisites
    print("\nStep 1: Checking Prerequisites")
    
    if not run_command("docker --version", "Checking Docker"):
        print("Please install Docker Desktop from https://docker.com/products/docker-desktop")
        return False
    
    if not run_command("docker-compose --version", "Checking Docker Compose"):
        print("Please install Docker Compose")
        return False
    
    # Step 2: Start services
    print("\nStep 2: Starting Services")
    
    if not run_command("docker-compose down --volumes", "Cleaning previous deployment"):
        print("Warning: Could not clean previous deployment")
    
    if not run_command("docker-compose up --build -d", "Building and starting services"):
        print("Failed to start services. Check Docker is running and ports are available.")
        return False
    
    # Step 3: Wait for services to be ready
    print("\nStep 3: Waiting for Services (30 seconds)")
    time.sleep(30)
    
    # Step 4: Verify services
    print("\nStep 4: Verifying Services")
    
    services = [
        ("http://localhost:8000/health", "Gateway API"),
        ("http://localhost:9000/health", "AI Agent"),
        ("http://localhost:8501", "Portal UI")
    ]
    
    all_services_ok = True
    for url, name in services:
        if not check_service(url, name):
            all_services_ok = False
    
    if not all_services_ok:
        print("\n[WARNING] Some services are not ready. Please wait a few more seconds and try accessing them manually.")
        return False
    
    # Step 5: Load sample data
    print("\nStep 5: Loading Sample Data")
    
    if not run_command("python scripts/create_sample_data.py", "Creating sample candidates"):
        print("Warning: Could not load sample data. You can add candidates manually.")
    
    # Step 6: Test workflow
    print("\nStep 6: Testing Complete Workflow")
    
    try:
        # Test AI matching
        response = requests.get(
            "http://localhost:8000/v1/match/1/top",
            headers={"X-API-KEY": "myverysecureapikey123"},
            timeout=10
        )
        if response.status_code == 200:
            print("[SUCCESS] AI matching system working")
        else:
            print("[ERROR] AI matching test failed")
    except Exception as e:
        print(f"[ERROR] AI matching test failed: {str(e)}")
    
    # Success message
    print("\n[SUCCESS] Setup Complete!")
    print("=" * 50)
    print("Access your BHIV HR Platform:")
    print("Portal UI: http://localhost:8501")
    print("API Docs: http://localhost:8000/docs")
    print("AI Agent: http://localhost:9000/docs")
    print("\nNext Steps:")
    print("1. Open the Portal UI to explore the interface")
    print("2. Create your first job")
    print("3. Add candidates and test AI matching")
    print("4. Schedule interviews and submit feedback")
    print("\nFor help, see the complete tutorial in README.md")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)