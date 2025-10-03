#!/usr/bin/env python3
"""
BHIV HR Platform - Complete Endpoint Audit
Scans Gateway service code to verify all endpoints are present
"""

import re
import os

def extract_endpoints_from_code():
    """Extract all endpoints from Gateway main.py"""
    gateway_file = r"c:\BHIV-HR-Platform\services\gateway\app\main.py"
    
    if not os.path.exists(gateway_file):
        print(f"ERROR: Gateway file not found: {gateway_file}")
        return []
    
    with open(gateway_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract all @app.get, @app.post, @app.put, @app.delete decorators
    endpoint_patterns = [
        r'@app\.get\("([^"]+)"',
        r'@app\.post\("([^"]+)"',
        r'@app\.put\("([^"]+)"',
        r'@app\.delete\("([^"]+)"'
    ]
    
    endpoints = []
    for pattern in endpoint_patterns:
        matches = re.findall(pattern, content)
        for match in matches:
            method = pattern.split('.')[1].split('(')[0].upper()
            endpoints.append(f"{method} {match}")
    
    return sorted(endpoints)

def categorize_endpoints(endpoints):
    """Categorize endpoints by functionality"""
    categories = {
        "Core API Endpoints": [],
        "Job Management": [],
        "Candidate Management": [],
        "AI Matching Engine": [],
        "Assessment & Workflow": [],
        "Analytics & Statistics": [],
        "Client Portal API": [],
        "Security Testing": [],
        "CSP Management": [],
        "Two-Factor Authentication": [],
        "Password Management": [],
        "Monitoring": []
    }
    
    for endpoint in endpoints:
        method, path = endpoint.split(' ', 1)
        
        # Core endpoints
        if path in ['/', '/health', '/test-candidates']:
            categories["Core API Endpoints"].append(endpoint)
        
        # Job management
        elif '/v1/jobs' in path:
            categories["Job Management"].append(endpoint)
        
        # Candidate management
        elif '/v1/candidates' in path:
            categories["Candidate Management"].append(endpoint)
        
        # AI matching
        elif '/v1/match' in path:
            categories["AI Matching Engine"].append(endpoint)
        
        # Assessment & workflow
        elif any(x in path for x in ['/v1/feedback', '/v1/interviews', '/v1/offers']):
            categories["Assessment & Workflow"].append(endpoint)
        
        # Analytics
        elif any(x in path for x in ['/candidates/stats', '/v1/reports']):
            categories["Analytics & Statistics"].append(endpoint)
        
        # Client portal
        elif '/v1/client' in path:
            categories["Client Portal API"].append(endpoint)
        
        # Security testing
        elif '/v1/security' in path and 'csp' not in path and '2fa' not in path and 'password' not in path:
            categories["Security Testing"].append(endpoint)
        
        # CSP management
        elif '/v1/security/csp' in path or '/v1/security/test-csp-policy' in path:
            categories["CSP Management"].append(endpoint)
        
        # 2FA
        elif '/v1/2fa' in path:
            categories["Two-Factor Authentication"].append(endpoint)
        
        # Password management
        elif '/v1/password' in path:
            categories["Password Management"].append(endpoint)
        
        # Monitoring
        elif any(x in path for x in ['/metrics', '/health/detailed']):
            categories["Monitoring"].append(endpoint)
    
    return categories

def main():
    print("BHIV HR Platform - Complete Endpoint Audit")
    print("=" * 50)
    
    # Extract endpoints from code
    endpoints = extract_endpoints_from_code()
    
    if not endpoints:
        print("ERROR: No endpoints found!")
        return
    
    print(f"Total Endpoints Found: {len(endpoints)}")
    print()
    
    # Categorize endpoints
    categories = categorize_endpoints(endpoints)
    
    # Display by category
    total_categorized = 0
    for category, category_endpoints in categories.items():
        if category_endpoints:
            print(f"{category} ({len(category_endpoints)} endpoints):")
            for endpoint in category_endpoints:
                print(f"  + {endpoint}")
            print()
            total_categorized += len(category_endpoints)
    
    # Check for uncategorized endpoints
    uncategorized = []
    for endpoint in endpoints:
        found = False
        for category_endpoints in categories.values():
            if endpoint in category_endpoints:
                found = True
                break
        if not found:
            uncategorized.append(endpoint)
    
    if uncategorized:
        print(f"Uncategorized Endpoints ({len(uncategorized)}):")
        for endpoint in uncategorized:
            print(f"  - {endpoint}")
        print()
    
    # Summary
    print("SUMMARY:")
    print(f"Total Endpoints: {len(endpoints)}")
    print(f"Categorized: {total_categorized}")
    print(f"Uncategorized: {len(uncategorized)}")
    
    # Expected vs Actual
    expected_counts = {
        "Core API Endpoints": 3,
        "Job Management": 2,
        "Candidate Management": 5,
        "AI Matching Engine": 1,
        "Assessment & Workflow": 6,
        "Analytics & Statistics": 2,
        "Client Portal API": 1,
        "Security Testing": 7,
        "CSP Management": 4,
        "Two-Factor Authentication": 8,
        "Password Management": 6,
        "Monitoring": 3
    }
    
    print("\nEXPECTED vs ACTUAL:")
    total_expected = sum(expected_counts.values())
    for category, expected in expected_counts.items():
        actual = len(categories[category])
        status = "+" if actual == expected else "-"
        print(f"{status} {category}: {actual}/{expected}")
    
    print(f"\nTotal Expected: {total_expected}")
    print(f"Total Actual: {len(endpoints)}")
    print(f"Status: {'COMPLETE' if len(endpoints) >= total_expected else 'MISSING ENDPOINTS'}")
    
    return endpoints, categories

if __name__ == "__main__":
    main()