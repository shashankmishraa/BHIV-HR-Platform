#!/usr/bin/env python3
"""
Simple test suite for upgraded BHIV AI Agent functions
Tests security fixes, resource management, and performance improvements
"""

import requests
import json
import time
import sys
from datetime import datetime, timezone

# Test configuration
BASE_URL = "http://localhost:9000"

def test_health_endpoint():
    """Test health endpoint with timezone-aware datetime"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            timestamp = data.get('timestamp', '')
            if 'T' in timestamp and ('+' in timestamp or 'Z' in timestamp):
                print("[PASS] Health endpoint: Timezone-aware timestamp")
                return True
            else:
                print("[FAIL] Health endpoint: Timestamp not timezone-aware")
                return False
        else:
            print(f"[FAIL] Health endpoint: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERROR] Health endpoint: {e}")
        return False

def test_database_connectivity():
    """Test database connectivity with proper resource management"""
    print("Testing database connectivity...")
    try:
        response = requests.get(f"{BASE_URL}/test-db", timeout=15)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'connected':
                candidates_count = data.get('candidates_count', 0)
                connection_pool = data.get('connection_pool', 'unknown')
                print(f"[PASS] Database test: {candidates_count} candidates, pool: {connection_pool}")
                return True
            else:
                print(f"[FAIL] Database test: Status: {data.get('status')}")
                return False
        else:
            print(f"[FAIL] Database test: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERROR] Database test: {e}")
        return False

def test_status_endpoint():
    """Test status endpoint with real database checks"""
    print("Testing status endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            db_connection = data.get('database_connection')
            endpoints_count = data.get('endpoints_available', 0)
            connection_pool = data.get('connection_pool', 'unknown')
            
            if db_connection in ['active', 'error', 'disconnected']:
                print(f"[PASS] Status endpoint: DB: {db_connection}, Endpoints: {endpoints_count}, Pool: {connection_pool}")
                return True
            else:
                print(f"[FAIL] Status endpoint: Invalid DB status: {db_connection}")
                return False
        else:
            print(f"[FAIL] Status endpoint: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERROR] Status endpoint: {e}")
        return False

def test_metrics_endpoint():
    """Test metrics endpoint with real system metrics"""
    print("Testing metrics endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/metrics", timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            perf_metrics = data.get('performance_metrics', {})
            cpu_usage = perf_metrics.get('cpu_usage_percent')
            memory_usage = perf_metrics.get('memory_usage_mb')
            
            if isinstance(cpu_usage, (int, float)) and isinstance(memory_usage, (int, float)):
                print(f"[PASS] Metrics endpoint: CPU: {cpu_usage}%, Memory: {memory_usage}MB")
                return True
            else:
                print(f"[FAIL] Metrics endpoint: Invalid metrics format")
                return False
        else:
            print(f"[FAIL] Metrics endpoint: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERROR] Metrics endpoint: {e}")
        return False

def main():
    """Run all upgrade tests"""
    print("BHIV AI Agent Upgrade Tests")
    print("=" * 50)
    print(f"Testing against: {BASE_URL}")
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")
    print()
    
    tests = [
        ("Health Endpoint", test_health_endpoint),
        ("Database Connectivity", test_database_connectivity),
        ("Status Endpoint", test_status_endpoint),
        ("Metrics Endpoint", test_metrics_endpoint)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"Running {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"[ERROR] {test_name}: CRITICAL ERROR - {e}")
            results.append((test_name, False))
        print()
    
    # Summary
    print("=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: [{status}]")
    
    print()
    print(f"Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("All upgrade tests passed!")
        return 0
    else:
        print("Some tests failed. Check the output above.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)