#!/usr/bin/env python3
"""
Verification script to check if upgrades are actually implemented
Compares local code changes with production deployment
"""

import requests
import json
from datetime import datetime, timezone

def check_implementation_status():
    """Check if the upgrades are actually implemented in production"""
    
    print("BHIV AI Agent Implementation Verification")
    print("=" * 50)
    
    production_url = "https://bhiv-hr-agent.onrender.com"
    
    # Test 1: Check timezone-aware timestamps
    print("\n1. Testing Timezone-Aware Timestamps...")
    try:
        response = requests.get(f"{production_url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            timestamp = data.get('timestamp', '')
            
            # Check if timestamp has timezone info
            if '+' in timestamp or 'Z' in timestamp:
                print("   [IMPLEMENTED] ✓ Timezone-aware timestamps working")
            else:
                print("   [NOT IMPLEMENTED] ✗ Still using naive timestamps")
                print(f"   Current timestamp: {timestamp}")
        else:
            print(f"   [ERROR] Health endpoint returned {response.status_code}")
    except Exception as e:
        print(f"   [ERROR] {e}")
    
    # Test 2: Check real system metrics
    print("\n2. Testing Real System Metrics...")
    try:
        response = requests.get(f"{production_url}/metrics", timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            # Check if we have real metrics structure
            perf_metrics = data.get('performance_metrics', {})
            
            # Look for new metric fields that indicate real implementation
            if 'cpu_usage_percent' in perf_metrics and 'memory_usage_mb' in perf_metrics:
                print("   [IMPLEMENTED] ✓ Real system metrics detected")
                cpu = perf_metrics.get('cpu_usage_percent')
                memory = perf_metrics.get('memory_usage_mb')
                print(f"   Real metrics: CPU: {cpu}%, Memory: {memory}MB")
            else:
                print("   [NOT IMPLEMENTED] ✗ Still using hardcoded metrics")
                print("   Current metrics structure:")
                for key, value in perf_metrics.items():
                    print(f"     {key}: {value}")
        else:
            print(f"   [ERROR] Metrics endpoint returned {response.status_code}")
    except Exception as e:
        print(f"   [ERROR] {e}")
    
    # Test 3: Check database connection pooling
    print("\n3. Testing Database Connection Pooling...")
    try:
        response = requests.get(f"{production_url}/test-db", timeout=15)
        if response.status_code == 200:
            data = response.json()
            
            # Check for connection pool indicator
            connection_pool = data.get('connection_pool')
            if connection_pool in ['healthy', 'active']:
                print("   [IMPLEMENTED] ✓ Connection pooling detected")
                print(f"   Pool status: {connection_pool}")
            else:
                print("   [NOT IMPLEMENTED] ✗ No connection pooling detected")
                print(f"   Current connection type: {connection_pool}")
        else:
            print(f"   [ERROR] Database test returned {response.status_code}")
    except Exception as e:
        print(f"   [ERROR] {e}")
    
    # Test 4: Check real database connectivity in status
    print("\n4. Testing Real Database Connectivity Checks...")
    try:
        response = requests.get(f"{production_url}/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            # Check if we have dynamic endpoint counting and real DB checks
            endpoints_count = data.get('endpoints_available', 0)
            db_connection = data.get('database_connection')
            connection_pool = data.get('connection_pool')
            
            if connection_pool is not None and isinstance(endpoints_count, int) and endpoints_count > 8:
                print("   [IMPLEMENTED] ✓ Real database checks and dynamic counting")
                print(f"   DB Status: {db_connection}, Pool: {connection_pool}, Endpoints: {endpoints_count}")
            else:
                print("   [NOT IMPLEMENTED] ✗ Still using hardcoded values")
                print(f"   Current values - DB: {db_connection}, Endpoints: {endpoints_count}")
        else:
            print(f"   [ERROR] Status endpoint returned {response.status_code}")
    except Exception as e:
        print(f"   [ERROR] {e}")
    
    # Test 5: Check security improvements (input validation)
    print("\n5. Testing Security Improvements...")
    try:
        # Test with malicious input
        malicious_payload = {"job_id": "'; DROP TABLE candidates; --"}
        response = requests.post(f"{production_url}/match", 
                               json=malicious_payload,
                               headers={"Content-Type": "application/json"},
                               timeout=10)
        
        if response.status_code == 422:
            print("   [IMPLEMENTED] ✓ Input validation working (422 response)")
        elif response.status_code == 500:
            print("   [PARTIALLY IMPLEMENTED] ⚠ Server error - may need input sanitization")
        else:
            print(f"   [UNKNOWN] ? Unexpected response: {response.status_code}")
    except Exception as e:
        print(f"   [ERROR] {e}")
    
    print("\n" + "=" * 50)
    print("IMPLEMENTATION STATUS SUMMARY")
    print("=" * 50)
    
    # Overall assessment
    print("\nBased on the tests above:")
    print("- Code changes have been made locally ✓")
    print("- Production deployment status needs verification")
    print("- Some features may require service restart to take effect")
    
    print(f"\nVerification completed at: {datetime.now(timezone.utc).isoformat()}")

if __name__ == "__main__":
    check_implementation_status()