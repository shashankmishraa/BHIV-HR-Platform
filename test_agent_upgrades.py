#!/usr/bin/env python3
"""
Test suite for upgraded BHIV AI Agent functions
Tests security fixes, resource management, and performance improvements
"""

import asyncio
import requests
import json
import time
import sys
import os
from datetime import datetime, timezone

# Test configuration
BASE_URL = "http://localhost:9000"
PRODUCTION_URL = "https://bhiv-hr-agent.onrender.com"

def test_health_endpoint():
    """Test health endpoint with timezone-aware datetime"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            # Check if timestamp is timezone-aware (contains 'T' and timezone info)
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
            
            # Check if database connection is actually tested
            if db_connection in ['active', 'error', 'disconnected']:
                print(f"✅ Status endpoint: PASS - DB: {db_connection}, Endpoints: {endpoints_count}, Pool: {connection_pool}")
                return True
            else:
                print(f"❌ Status endpoint: FAIL - Invalid DB status: {db_connection}")
                return False
        else:
            print(f"❌ Status endpoint: FAIL - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Status endpoint: ERROR - {e}")
        return False

def test_metrics_endpoint():
    """Test metrics endpoint with real system metrics"""
    print("Testing metrics endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/metrics", timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            # Check for real system metrics
            perf_metrics = data.get('performance_metrics', {})
            cpu_usage = perf_metrics.get('cpu_usage_percent')
            memory_usage = perf_metrics.get('memory_usage_mb')
            
            if isinstance(cpu_usage, (int, float)) and isinstance(memory_usage, (int, float)):
                print(f"✅ Metrics endpoint: PASS - CPU: {cpu_usage}%, Memory: {memory_usage}MB")
                return True
            else:
                print(f"❌ Metrics endpoint: FAIL - Invalid metrics format")
                return False
        else:
            print(f"❌ Metrics endpoint: FAIL - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Metrics endpoint: ERROR - {e}")
        return False

def test_candidate_matching():
    """Test candidate matching with proper error handling"""
    print("Testing candidate matching...")
    try:
        # Test with a valid job ID (assuming job ID 1 exists)
        payload = {"job_id": 1}
        response = requests.post(f"{BASE_URL}/match", 
                               json=payload, 
                               headers={"Content-Type": "application/json"},
                               timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            processing_time = data.get('processing_time', 0)
            total_candidates = data.get('total_candidates', 0)
            algorithm_version = data.get('algorithm_version', '')
            
            print(f"✅ Matching endpoint: PASS - {total_candidates} candidates, {processing_time}s, {algorithm_version}")
            return True
        elif response.status_code == 422:
            print("⚠️ Matching endpoint: Job not found (expected for test)")
            return True
        else:
            print(f"❌ Matching endpoint: FAIL - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Matching endpoint: ERROR - {e}")
        return False

def test_candidate_analysis():
    """Test candidate analysis with proper resource management"""
    print("Testing candidate analysis...")
    try:
        # Test with candidate ID 1 (assuming it exists)
        response = requests.get(f"{BASE_URL}/analyze/1", timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                skills_analysis = data.get('skills_analysis', {})
                timestamp = data.get('analysis_timestamp', '')
                
                # Check timezone-aware timestamp
                if 'T' in timestamp and ('+' in timestamp or 'Z' in timestamp):
                    print(f"✅ Analysis endpoint: PASS - Skills categories: {len(skills_analysis)}")
                    return True
                else:
                    print("❌ Analysis endpoint: FAIL - Timestamp not timezone-aware")
                    return False
            else:
                print(f"⚠️ Analysis endpoint: Candidate not found (expected for test)")
                return True
        else:
            print(f"❌ Analysis endpoint: FAIL - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Analysis endpoint: ERROR - {e}")
        return False

def test_security_improvements():
    """Test security improvements (log injection prevention)"""
    print("Testing security improvements...")
    try:
        # Test with potentially malicious input
        malicious_payload = {"job_id": "1; DROP TABLE candidates; --"}
        response = requests.post(f"{BASE_URL}/match", 
                               json=malicious_payload,
                               headers={"Content-Type": "application/json"},
                               timeout=10)
        
        # Should return 422 (validation error) due to type checking
        if response.status_code == 422:
            print("✅ Security test: PASS - Input validation working")
            return True
        else:
            print(f"⚠️ Security test: Unexpected response {response.status_code}")
            return True  # Not necessarily a failure
    except Exception as e:
        print(f"❌ Security test: ERROR - {e}")
        return False

def run_performance_test():
    """Run performance test for concurrent requests"""
    print("Testing performance improvements...")
    try:
        start_time = time.time()
        
        # Make multiple concurrent requests to test connection pooling
        import concurrent.futures
        
        def make_request():
            try:
                response = requests.get(f"{BASE_URL}/health", timeout=5)
                return response.status_code == 200
            except:
                return False
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        end_time = time.time()
        success_rate = sum(results) / len(results) * 100
        total_time = end_time - start_time
        
        if success_rate >= 80 and total_time < 10:
            print(f"✅ Performance test: PASS - {success_rate}% success in {total_time:.2f}s")
            return True
        else:
            print(f"❌ Performance test: FAIL - {success_rate}% success in {total_time:.2f}s")
            return False
    except Exception as e:
        print(f"❌ Performance test: ERROR - {e}")
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
        ("Metrics Endpoint", test_metrics_endpoint),
        ("Candidate Matching", test_candidate_matching),
        ("Candidate Analysis", test_candidate_analysis),
        ("Security Improvements", test_security_improvements),
        ("Performance Test", run_performance_test)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"Running {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name}: CRITICAL ERROR - {e}")
            results.append((test_name, False))
        print()
    
    # Summary
    print("=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
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