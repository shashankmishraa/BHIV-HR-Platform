#!/usr/bin/env python3
"""
Comprehensive Endpoint Testing
Tests all API endpoints and portal functionalities on both localhost and Render
"""

import requests
import time
import json

# Configuration
LOCALHOST_URL = "http://localhost:8000"
RENDER_URL = "https://bhiv-hr-gateway.onrender.com"
API_KEY = "myverysecureapikey123"

def test_endpoint(base_url, endpoint, method="GET", headers=None, data=None, description=""):
    """Test a single endpoint"""
    if headers is None:
        headers = {"Authorization": f"Bearer {API_KEY}"}
    
    try:
        url = f"{base_url}{endpoint}"
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=30)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if "error" in str(result).lower() and "does not exist" in str(result):
                return "FAIL", f"Database error: {result}"
            return "PASS", result
        else:
            return "FAIL", f"Status {response.status_code}: {response.text[:100]}"
            
    except Exception as e:
        return "FAIL", f"Exception: {str(e)[:100]}"

def run_comprehensive_test(base_url, platform_name):
    """Run comprehensive test suite"""
    print(f"\n{'='*60}")
    print(f"TESTING {platform_name.upper()} - {base_url}")
    print(f"{'='*60}")
    
    # Test cases
    tests = [
        # Core API Endpoints
        ("GET", "/", "Root endpoint"),
        ("GET", "/health", "Health check"),
        ("GET", "/test-candidates", "Database connectivity"),
        
        # Job Management
        ("GET", "/v1/jobs", "List jobs"),
        ("POST", "/v1/jobs", "Create job", {
            "title": f"Test Job {platform_name}",
            "department": "Engineering", 
            "location": "Remote",
            "experience_level": "Mid",
            "requirements": "Python, FastAPI",
            "description": f"Test job created on {platform_name}"
        }),
        
        # Candidate Management
        ("GET", "/v1/candidates/job/1", "Get candidates by job"),
        ("GET", "/v1/candidates/search", "Search candidates"),
        ("GET", "/v1/candidates/search?skills=python", "Search candidates with skills"),
        
        # AI Matching
        ("GET", "/v1/match/1/top", "AI matching"),
        ("GET", "/v1/match/1/top?limit=5", "AI matching with limit"),
        
        # Analytics
        ("GET", "/candidates/stats", "Candidate statistics"),
        ("GET", "/v1/reports/job/1/export.csv", "Export job report"),
        
        # Security
        ("GET", "/v1/security/rate-limit-status", "Rate limit status"),
        ("GET", "/v1/security/blocked-ips", "Blocked IPs"),
        
        # Monitoring
        ("GET", "/metrics", "Prometheus metrics"),
        ("GET", "/health/detailed", "Detailed health"),
        ("GET", "/metrics/dashboard", "Metrics dashboard"),
        
        # Client Portal
        ("POST", "/v1/client/login", "Client login", {
            "client_id": "TECH001",
            "password": "google123"
        }, {"Content-Type": "application/json"}),
    ]
    
    results = {"PASS": 0, "FAIL": 0, "details": []}
    
    for test in tests:
        method, endpoint, description = test[:3]
        data = test[3] if len(test) > 3 else None
        custom_headers = test[4] if len(test) > 4 else None
        
        headers = {"Authorization": f"Bearer {API_KEY}"}
        if custom_headers:
            headers.update(custom_headers)
        if method == "POST" and "login" in endpoint:
            headers = custom_headers or {"Content-Type": "application/json"}
            
        status, result = test_endpoint(base_url, endpoint, method, headers, data, description)
        results[status] += 1
        results["details"].append({
            "endpoint": f"{method} {endpoint}",
            "description": description,
            "status": status,
            "result": str(result)[:200] if status == "FAIL" else "OK"
        })
        
        print(f"{status:4} | {method:4} | {endpoint:30} | {description}")
        time.sleep(0.5)  # Rate limiting
    
    print(f"\n{platform_name} Results: {results['PASS']} PASS, {results['FAIL']} FAIL")
    return results

def test_portals():
    """Test portal accessibility"""
    print(f"\n{'='*60}")
    print("TESTING PORTAL ACCESSIBILITY")
    print(f"{'='*60}")
    
    portals = [
        ("HR Portal", "https://bhiv-hr-portal.onrender.com/"),
        ("Client Portal", "https://bhiv-hr-client-portal.onrender.com/"),
        ("AI Agent", "https://bhiv-hr-agent.onrender.com/"),
    ]
    
    for name, url in portals:
        try:
            response = requests.get(url, timeout=30)
            status = "PASS" if response.status_code == 200 else "FAIL"
            print(f"{status:4} | {name:15} | {url}")
        except Exception as e:
            print(f"FAIL | {name:15} | {url} - {str(e)[:50]}")

if __name__ == "__main__":
    print("BHIV HR Platform - Comprehensive Endpoint Testing")
    print("Testing all endpoints and portal functionalities")
    
    # Test localhost
    localhost_results = run_comprehensive_test(LOCALHOST_URL, "Localhost")
    
    # Test Render
    render_results = run_comprehensive_test(RENDER_URL, "Render")
    
    # Test portals
    test_portals()
    
    # Summary
    print(f"\n{'='*60}")
    print("FINAL SUMMARY")
    print(f"{'='*60}")
    print(f"Localhost: {localhost_results['PASS']} PASS, {localhost_results['FAIL']} FAIL")
    print(f"Render:    {render_results['PASS']} PASS, {render_results['FAIL']} FAIL")
    
    # Check if they match
    if localhost_results['PASS'] == render_results['PASS']:
        print("✅ RENDER MATCHES LOCALHOST FUNCTIONALITY!")
    else:
        print("❌ RENDER DOES NOT MATCH LOCALHOST")
        print("\nDifferences:")
        for i, (local, render) in enumerate(zip(localhost_results['details'], render_results['details'])):
            if local['status'] != render['status']:
                print(f"  {local['endpoint']}: Local={local['status']}, Render={render['status']}")