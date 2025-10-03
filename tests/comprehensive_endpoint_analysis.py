#!/usr/bin/env python3
"""
BHIV HR Platform - Comprehensive Endpoint Analysis
Scans codebase and compares against requirements to identify gaps and extras
"""

import re
import os

def scan_gateway_endpoints():
    """Scan Gateway service for all endpoints"""
    gateway_file = r"c:\BHIV-HR-Platform\services\gateway\app\main.py"
    
    if not os.path.exists(gateway_file):
        return []
    
    with open(gateway_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    patterns = [
        (r'@app\.get\("([^"]+)"', 'GET'),
        (r'@app\.post\("([^"]+)"', 'POST'),
        (r'@app\.put\("([^"]+)"', 'PUT'),
        (r'@app\.delete\("([^"]+)"', 'DELETE')
    ]
    
    endpoints = []
    for pattern, method in patterns:
        matches = re.findall(pattern, content)
        for match in matches:
            endpoints.append(f"{method} {match}")
    
    return sorted(endpoints)

def scan_agent_endpoints():
    """Scan Agent service for all endpoints"""
    agent_file = r"c:\BHIV-HR-Platform\services\agent\app.py"
    
    if not os.path.exists(agent_file):
        return []
    
    with open(agent_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    patterns = [
        (r'@app\.get\("([^"]+)"', 'GET'),
        (r'@app\.post\("([^"]+)"', 'POST'),
        (r'@app\.put\("([^"]+)"', 'PUT'),
        (r'@app\.delete\("([^"]+)"', 'DELETE')
    ]
    
    endpoints = []
    for pattern, method in patterns:
        matches = re.findall(pattern, content)
        for match in matches:
            endpoints.append(f"{method} {match}")
    
    return sorted(endpoints)

def get_required_endpoints():
    """Define required endpoints based on HR platform requirements"""
    required = {
        "gateway": {
            "Core API": [
                "GET /",
                "GET /health", 
                "GET /test-candidates"
            ],
            "Job Management": [
                "GET /v1/jobs",
                "POST /v1/jobs"
            ],
            "Candidate Management": [
                "GET /v1/candidates",
                "GET /v1/candidates/{candidate_id}",
                "GET /v1/candidates/search",
                "POST /v1/candidates/bulk"
            ],
            "AI Matching": [
                "GET /v1/match/{job_id}/top"
            ],
            "Assessment & Workflow": [
                "POST /v1/feedback",
                "GET /v1/feedback",
                "GET /v1/interviews",
                "POST /v1/interviews",
                "GET /v1/offers",
                "POST /v1/offers"
            ],
            "Analytics": [
                "GET /candidates/stats",
                "GET /v1/reports/job/{job_id}/export.csv"
            ],
            "Client Portal": [
                "POST /v1/client/login"
            ],
            "Security (Basic)": [
                "GET /v1/security/rate-limit-status"
            ],
            "Monitoring": [
                "GET /metrics",
                "GET /health/detailed"
            ]
        },
        "agent": {
            "Core": [
                "GET /",
                "GET /health"
            ],
            "AI Processing": [
                "POST /match",
                "GET /analyze/{candidate_id}"
            ],
            "Diagnostics": [
                "GET /test-db"
            ]
        }
    }
    
    # Flatten required endpoints
    gateway_required = []
    agent_required = []
    
    for category, endpoints in required["gateway"].items():
        gateway_required.extend(endpoints)
    
    for category, endpoints in required["agent"].items():
        agent_required.extend(endpoints)
    
    return sorted(gateway_required), sorted(agent_required)

def get_optional_endpoints():
    """Define optional/advanced endpoints that are nice-to-have"""
    optional = {
        "gateway": [
            # Advanced Security
            "GET /v1/security/blocked-ips",
            "POST /v1/security/test-input-validation",
            "POST /v1/security/test-email-validation", 
            "POST /v1/security/test-phone-validation",
            "GET /v1/security/security-headers-test",
            "GET /v1/security/penetration-test-endpoints",
            
            # CSP Management
            "POST /v1/security/csp-report",
            "GET /v1/security/csp-violations",
            "GET /v1/security/csp-policies",
            "POST /v1/security/test-csp-policy",
            
            # Two-Factor Authentication
            "POST /v1/2fa/setup",
            "POST /v1/2fa/verify-setup",
            "POST /v1/2fa/login-with-2fa",
            "GET /v1/2fa/status/{client_id}",
            "POST /v1/2fa/disable",
            "POST /v1/2fa/regenerate-backup-codes",
            "GET /v1/2fa/test-token/{client_id}/{token}",
            "GET /v1/2fa/demo-setup",
            
            # Password Management
            "POST /v1/password/validate",
            "POST /v1/password/generate",
            "GET /v1/password/policy",
            "POST /v1/password/change",
            "GET /v1/password/strength-test",
            "GET /v1/password/security-tips",
            
            # Advanced Monitoring
            "GET /metrics/dashboard",
            
            # Advanced Candidate Management
            "GET /v1/candidates/job/{job_id}"
        ],
        "agent": []
    }
    
    return optional["gateway"], optional["agent"]

def analyze_endpoints():
    """Comprehensive endpoint analysis"""
    print("BHIV HR Platform - Comprehensive Endpoint Analysis")
    print("=" * 60)
    
    # Scan actual endpoints
    gateway_actual = scan_gateway_endpoints()
    agent_actual = scan_agent_endpoints()
    
    # Get required endpoints
    gateway_required, agent_required = get_required_endpoints()
    
    # Get optional endpoints
    gateway_optional, agent_optional = get_optional_endpoints()
    
    print(f"ACTUAL ENDPOINTS FOUND:")
    print(f"Gateway: {len(gateway_actual)} endpoints")
    print(f"Agent:   {len(agent_actual)} endpoints")
    print(f"Total:   {len(gateway_actual) + len(agent_actual)} endpoints")
    print()
    
    print(f"REQUIRED ENDPOINTS:")
    print(f"Gateway: {len(gateway_required)} endpoints")
    print(f"Agent:   {len(agent_required)} endpoints")
    print(f"Total:   {len(gateway_required) + len(agent_required)} endpoints")
    print()
    
    # GATEWAY ANALYSIS
    print("GATEWAY SERVICE ANALYSIS:")
    print("-" * 40)
    
    # Required endpoints check
    gateway_missing_required = []
    gateway_present_required = []
    
    for endpoint in gateway_required:
        if endpoint in gateway_actual:
            gateway_present_required.append(endpoint)
        else:
            gateway_missing_required.append(endpoint)
    
    # Optional endpoints check
    gateway_present_optional = []
    for endpoint in gateway_optional:
        if endpoint in gateway_actual:
            gateway_present_optional.append(endpoint)
    
    # Extra endpoints (not required or optional)
    all_known_gateway = set(gateway_required + gateway_optional)
    gateway_extra = [ep for ep in gateway_actual if ep not in all_known_gateway]
    
    print(f"Required Present: {len(gateway_present_required)}/{len(gateway_required)}")
    print(f"Optional Present: {len(gateway_present_optional)}/{len(gateway_optional)}")
    print(f"Extra Endpoints: {len(gateway_extra)}")
    print(f"Missing Required: {len(gateway_missing_required)}")
    
    if gateway_missing_required:
        print("\nMISSING REQUIRED GATEWAY ENDPOINTS:")
        for endpoint in gateway_missing_required:
            print(f"  - {endpoint}")
    
    if gateway_extra:
        print("\nEXTRA GATEWAY ENDPOINTS (not in spec):")
        for endpoint in gateway_extra:
            print(f"  + {endpoint}")
    
    print()
    
    # AGENT ANALYSIS
    print("AGENT SERVICE ANALYSIS:")
    print("-" * 40)
    
    # Required endpoints check
    agent_missing_required = []
    agent_present_required = []
    
    for endpoint in agent_required:
        if endpoint in agent_actual:
            agent_present_required.append(endpoint)
        else:
            agent_missing_required.append(endpoint)
    
    # Extra endpoints
    agent_extra = [ep for ep in agent_actual if ep not in agent_required]
    
    print(f"Required Present: {len(agent_present_required)}/{len(agent_required)}")
    print(f"Extra Endpoints: {len(agent_extra)}")
    print(f"Missing Required: {len(agent_missing_required)}")
    
    if agent_missing_required:
        print("\nMISSING REQUIRED AGENT ENDPOINTS:")
        for endpoint in agent_missing_required:
            print(f"  - {endpoint}")
    
    if agent_extra:
        print("\nEXTRA AGENT ENDPOINTS (not in spec):")
        for endpoint in agent_extra:
            print(f"  + {endpoint}")
    
    print()
    
    # OVERALL SUMMARY
    print("OVERALL SUMMARY:")
    print("-" * 30)
    
    total_required = len(gateway_required) + len(agent_required)
    total_present_required = len(gateway_present_required) + len(agent_present_required)
    total_missing = len(gateway_missing_required) + len(agent_missing_required)
    total_extra = len(gateway_extra) + len(agent_extra)
    total_optional = len(gateway_present_optional)
    
    print(f"Required Coverage: {total_present_required}/{total_required} ({(total_present_required/total_required)*100:.1f}%)")
    print(f"Missing Required: {total_missing}")
    print(f"Extra Endpoints: {total_extra}")
    print(f"Optional Features: {total_optional}")
    
    # STATUS
    if total_missing == 0:
        if total_extra == 0:
            status = "PERFECT - All required endpoints present, no extras"
        else:
            status = "COMPLETE+ - All required + extra features"
    else:
        status = f"INCOMPLETE - Missing {total_missing} required endpoints"
    
    print(f"Status: {status}")
    
    # RECOMMENDATIONS
    print("\nRECOMMENDATIONS:")
    print("-" * 30)
    
    if total_missing == 0:
        print("✓ All required endpoints are implemented")
        if total_optional > 20:
            print("✓ Excellent optional feature coverage")
        elif total_optional > 10:
            print("✓ Good optional feature coverage")
        else:
            print("- Consider adding optional features for enhanced functionality")
    else:
        print(f"! Implement {total_missing} missing required endpoints")
    
    if total_extra > 0:
        print(f"? Review {total_extra} extra endpoints - ensure they're needed")
    
    return {
        'gateway_actual': gateway_actual,
        'agent_actual': agent_actual,
        'gateway_required': gateway_required,
        'agent_required': agent_required,
        'gateway_missing': gateway_missing_required,
        'agent_missing': agent_missing_required,
        'gateway_extra': gateway_extra,
        'agent_extra': agent_extra,
        'status': status
    }

if __name__ == "__main__":
    analyze_endpoints()