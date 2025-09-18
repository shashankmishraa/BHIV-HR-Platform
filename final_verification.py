#!/usr/bin/env python3
"""
Final verification after dependency fix deployment
"""

import requests
import time
import json

def wait_and_verify():
    """Wait for deployment and verify upgrades"""
    
    print("FINAL DEPLOYMENT VERIFICATION")
    print("=" * 40)
    print("Deployment ID: dep-d360bbbipnbc739sg4gg")
    print("Waiting 3 minutes for Agent service deployment...")
    
    # Wait for deployment
    time.sleep(180)
    
    agent_url = "https://bhiv-hr-agent.onrender.com"
    
    print("\nVerifying Agent Service Upgrades:")
    print("-" * 35)
    
    # Test 1: Timezone-aware timestamps
    try:
        response = requests.get(f"{agent_url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            timestamp = data.get('timestamp', '')
            
            if '+' in timestamp or 'Z' in timestamp:
                print("✓ Timezone-aware timestamps: WORKING")
            else:
                print("✗ Timezone-aware timestamps: FAILED")
                print(f"  Current: {timestamp}")
        else:
            print(f"✗ Health endpoint: ERROR {response.status_code}")
    except Exception as e:
        print(f"✗ Health check failed: {e}")
    
    # Test 2: Real system metrics
    try:
        response = requests.get(f"{agent_url}/metrics", timeout=10)
        if response.status_code == 200:
            data = response.json()
            perf_metrics = data.get('performance_metrics', {})
            
            if 'cpu_usage_percent' in perf_metrics:
                cpu = perf_metrics.get('cpu_usage_percent')
                memory = perf_metrics.get('memory_usage_mb')
                print(f"✓ Real system metrics: WORKING")
                print(f"  CPU: {cpu}%, Memory: {memory}MB")
            else:
                print("✗ Real system metrics: FAILED")
                print("  Still using hardcoded values")
        else:
            print(f"✗ Metrics endpoint: ERROR {response.status_code}")
    except Exception as e:
        print(f"✗ Metrics check failed: {e}")
    
    # Test 3: Enhanced status endpoint
    try:
        response = requests.get(f"{agent_url}/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            endpoints = data.get('endpoints_available', 0)
            pool_status = data.get('connection_pool')
            
            if pool_status is not None:
                print(f"✓ Enhanced status endpoint: WORKING")
                print(f"  Endpoints: {endpoints}, Pool: {pool_status}")
            else:
                print("✗ Enhanced status endpoint: FAILED")
        else:
            print(f"✗ Status endpoint: ERROR {response.status_code}")
    except Exception as e:
        print(f"✗ Status check failed: {e}")
    
    print("\n" + "=" * 40)
    print("DEPLOYMENT SUMMARY")
    print("=" * 40)
    print("All security and performance upgrades should now be active:")
    print("- Log injection prevention")
    print("- Real system metrics monitoring") 
    print("- Database connection pooling")
    print("- Timezone-aware timestamps")
    print("- Enhanced error handling")
    print("- Async batch processing")

if __name__ == "__main__":
    wait_and_verify()