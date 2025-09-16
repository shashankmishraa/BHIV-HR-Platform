#!/usr/bin/env python3
"""
Health monitoring script for BHIV HR Platform
"""

import requests
import time
import json
from datetime import datetime

def check_service_health(name, url, timeout=10):
    """Check individual service health"""
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            return {"service": name, "status": "healthy", "response_time": response.elapsed.total_seconds()}
        else:
            return {"service": name, "status": "unhealthy", "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"service": name, "status": "error", "error": str(e)}

def monitor_platform():
    """Monitor all platform services"""
    services = [
        ("Gateway", "http://localhost:8000/health"),
        ("AI Agent", "http://localhost:9000/health"),
        ("Database", "http://localhost:8000/test-db")
    ]
    
    results = []
    for name, url in services:
        result = check_service_health(name, url)
        results.append(result)
        
        status_icon = "PASS" if result["status"] == "healthy" else "FAIL"
        print(f"{status_icon} {name}: {result['status']}")
        
        if "response_time" in result:
            print(f"  Response time: {result['response_time']:.3f}s")
        if "error" in result:
            print(f"  Error: {result['error']}")
    
    return results

if __name__ == "__main__":
    print("BHIV HR Platform Health Check")
    print("=" * 40)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    results = monitor_platform()
    
    healthy_count = sum(1 for r in results if r["status"] == "healthy")
    total_count = len(results)
    
    print()
    print(f"Health Summary: {healthy_count}/{total_count} services healthy")
    
    if healthy_count == total_count:
        print("All services are healthy!")
        exit(0)
    else:
        print("Some services need attention")
        exit(1)