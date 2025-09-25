#!/usr/bin/env python3
"""
DETAILED ANALYSIS OF BHIV HR PLATFORM
Comprehensive analysis of all services, endpoints, and functionalities
"""

import requests
import json
import time
from datetime import datetime
import sys

# Configuration
BASE_URL = "http://localhost:8000"
AGENT_URL = "http://localhost:9000"
API_KEY = "myverysecureapikey123"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}


def log(message, level="INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {level}: {message}")


def test_endpoint_detailed(method, url, data=None, test_name=""):
    """Test endpoint with detailed response analysis"""
    try:
        start = time.time()

        if method == "GET":
            response = requests.get(url, headers=HEADERS, timeout=10)
        elif method == "POST":
            response = requests.post(url, headers=HEADERS, json=data, timeout=10)
        elif method == "PUT":
            response = requests.put(url, headers=HEADERS, json=data, timeout=10)

        duration = time.time() - start

        log(f"{test_name}")
        log(f"  Method: {method}")
        log(f"  URL: {url}")
        log(f"  Status: {response.status_code}")
        log(f"  Time: {duration*1000:.1f}ms")
        log(f"  Size: {len(response.content)} bytes")

        if response.status_code == 200:
            try:
                json_data = response.json()
                if isinstance(json_data, dict):
                    log(f"  Keys: {list(json_data.keys())}")
                elif isinstance(json_data, list):
                    log(f"  Items: {len(json_data)}")
            except:
                log(f"  Content: Non-JSON response")
        else:
            log(f"  Error: {response.text[:200]}")

        log("")
        return response

    except Exception as e:
        log(f"ERROR {test_name}: {str(e)}")
        log("")
        return None


def analyze_core_functionality():
    """Analyze core system functionality"""
    log("=" * 60)
    log("ANALYZING CORE FUNCTIONALITY")
    log("=" * 60)

    # Core endpoints
    test_endpoint_detailed("GET", f"{BASE_URL}/", test_name="Root Endpoint")
    test_endpoint_detailed("GET", f"{BASE_URL}/health", test_name="Health Check")
    test_endpoint_detailed(
        "GET", f"{BASE_URL}/test-candidates", test_name="Test Candidates"
    )

    # Job management
    test_endpoint_detailed("GET", f"{BASE_URL}/v1/jobs", test_name="List Jobs")

    # Candidate management
    test_endpoint_detailed(
        "GET", f"{BASE_URL}/v1/candidates", test_name="List Candidates"
    )

    # AI matching
    test_endpoint_detailed(
        "GET", f"{BASE_URL}/v1/match/1/top", test_name="AI Matching - Top Candidates"
    )
    test_endpoint_detailed(
        "GET", f"{BASE_URL}/v1/match/performance-test", test_name="AI Performance Test"
    )


def analyze_security_features():
    """Analyze security features"""
    log("=" * 60)
    log("ANALYZING SECURITY FEATURES")
    log("=" * 60)

    # Security endpoints
    test_endpoint_detailed(
        "GET", f"{BASE_URL}/v1/security/headers", test_name="Security Headers"
    )
    test_endpoint_detailed(
        "GET", f"{BASE_URL}/v1/security/status", test_name="Security Status"
    )
    test_endpoint_detailed(
        "GET", f"{BASE_URL}/v1/security/policy", test_name="Security Policy"
    )
    test_endpoint_detailed(
        "GET",
        f"{BASE_URL}/v1/security/rate-limit-status",
        test_name="Rate Limit Status",
    )

    # Password management
    test_endpoint_detailed(
        "GET", f"{BASE_URL}/v1/password/policy", test_name="Password Policy"
    )
    test_endpoint_detailed(
        "GET", f"{BASE_URL}/v1/password/generate", test_name="Generate Password"
    )
    test_endpoint_detailed(
        "POST",
        f"{BASE_URL}/v1/password/validate",
        {"password": "TestPassword123!"},
        test_name="Password Validation",
    )


def analyze_monitoring_system():
    """Analyze monitoring and metrics"""
    log("=" * 60)
    log("ANALYZING MONITORING SYSTEM")
    log("=" * 60)

    # Monitoring endpoints
    test_endpoint_detailed("GET", f"{BASE_URL}/metrics", test_name="Prometheus Metrics")
    test_endpoint_detailed(
        "GET", f"{BASE_URL}/health/detailed", test_name="Detailed Health Check"
    )
    test_endpoint_detailed(
        "GET", f"{BASE_URL}/monitoring/errors", test_name="Error Monitoring"
    )
    test_endpoint_detailed(
        "GET", f"{BASE_URL}/monitoring/dependencies", test_name="Dependencies Check"
    )


def analyze_agent_service():
    """Analyze AI Agent service"""
    log("=" * 60)
    log("ANALYZING AI AGENT SERVICE")
    log("=" * 60)

    # Agent endpoints
    test_endpoint_detailed("GET", f"{AGENT_URL}/", test_name="Agent Root")
    test_endpoint_detailed("GET", f"{AGENT_URL}/health", test_name="Agent Health")
    test_endpoint_detailed("GET", f"{AGENT_URL}/status", test_name="Agent Status")
    test_endpoint_detailed("GET", f"{AGENT_URL}/version", test_name="Agent Version")
    test_endpoint_detailed("GET", f"{AGENT_URL}/metrics", test_name="Agent Metrics")


def analyze_database_integration():
    """Analyze database integration"""
    log("=" * 60)
    log("ANALYZING DATABASE INTEGRATION")
    log("=" * 60)

    # Database endpoints
    test_endpoint_detailed(
        "GET", f"{BASE_URL}/v1/database/health", test_name="Database Health"
    )
    test_endpoint_detailed(
        "GET", f"{BASE_URL}/candidates/stats", test_name="Candidate Statistics"
    )


def test_api_functionality():
    """Test API functionality with real data"""
    log("=" * 60)
    log("TESTING API FUNCTIONALITY")
    log("=" * 60)

    # Test job creation with proper data
    job_data = {
        "title": "Senior Python Developer",
        "description": "We are looking for an experienced Python developer",
        "requirements": ["Python", "Django", "PostgreSQL"],
        "location": "Remote",
        "salary_range": "90000-130000",
        "company": "Tech Corp",
        "employment_type": "Full-time",
    }

    test_endpoint_detailed(
        "POST", f"{BASE_URL}/v1/jobs", job_data, test_name="Create Job with Full Data"
    )

    # Test candidate search
    search_data = {"query": "python developer", "limit": 10}
    test_endpoint_detailed(
        "POST",
        f"{BASE_URL}/v1/candidates/bulk",
        search_data,
        test_name="Bulk Candidate Search",
    )


def performance_analysis():
    """Analyze system performance"""
    log("=" * 60)
    log("PERFORMANCE ANALYSIS")
    log("=" * 60)

    endpoints = [
        (f"{BASE_URL}/health", "Health Check"),
        (f"{BASE_URL}/v1/candidates", "List Candidates"),
        (f"{BASE_URL}/v1/jobs", "List Jobs"),
        (f"{BASE_URL}/v1/match/1/top", "AI Matching"),
        (f"{AGENT_URL}/health", "Agent Health"),
    ]

    for url, name in endpoints:
        times = []
        for i in range(5):
            start = time.time()
            try:
                response = requests.get(url, headers=HEADERS, timeout=5)
                if response.status_code == 200:
                    times.append(time.time() - start)
            except:
                pass

        if times:
            avg_time = sum(times) / len(times) * 1000
            min_time = min(times) * 1000
            max_time = max(times) * 1000
            log(
                f"{name}: Avg={avg_time:.1f}ms, Min={min_time:.1f}ms, Max={max_time:.1f}ms"
            )


def check_service_health():
    """Check overall service health"""
    log("=" * 60)
    log("SERVICE HEALTH CHECK")
    log("=" * 60)

    services = [
        (f"{BASE_URL}/health", "API Gateway"),
        (f"{AGENT_URL}/health", "AI Agent"),
        ("http://localhost:8501", "HR Portal"),
        ("http://localhost:8502", "Client Portal"),
    ]

    for url, name in services:
        try:
            response = requests.get(url, timeout=5)
            status = (
                "HEALTHY"
                if response.status_code == 200
                else f"UNHEALTHY ({response.status_code})"
            )
            log(f"{name}: {status}")
        except Exception as e:
            log(f"{name}: OFFLINE ({str(e)})")


def main():
    """Run comprehensive analysis"""
    log("STARTING DETAILED ANALYSIS OF BHIV HR PLATFORM")
    log("=" * 60)

    start_time = time.time()

    # Run all analyses
    check_service_health()
    analyze_core_functionality()
    analyze_security_features()
    analyze_monitoring_system()
    analyze_agent_service()
    analyze_database_integration()
    test_api_functionality()
    performance_analysis()

    total_time = time.time() - start_time

    log("=" * 60)
    log("DETAILED ANALYSIS COMPLETE")
    log("=" * 60)
    log(f"Total Analysis Time: {total_time:.1f} seconds")
    log("Analysis complete. Check logs above for detailed findings.")


if __name__ == "__main__":
    main()
