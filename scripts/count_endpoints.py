#!/usr/bin/env python3
"""
Count all endpoints in the gateway
"""

import re

def count_endpoints():
    with open('c:\\bhiv hr ai platform\\services\\gateway\\app\\main.py', 'r') as f:
        content = f.read()
    
    # Find all @app.get, @app.post, @app.put, @app.delete decorators
    endpoints = re.findall(r'@app\.(get|post|put|delete)\(["\']([^"\']+)["\']', content)
    
    print("BHIV HR Platform - Total Endpoints Count")
    print("=" * 50)
    
    by_method = {}
    by_category = {
        "Core": [],
        "Job Management": [],
        "Candidate Management": [],
        "AI Matching": [],
        "Interview Management": [],
        "Client Portal": [],
        "Analytics": [],
        "Monitoring": []
    }
    
    for method, path in endpoints:
        method = method.upper()
        if method not in by_method:
            by_method[method] = []
        by_method[method].append(path)
        
        # Categorize endpoints
        if path in ["/", "/health", "/test-candidates"]:
            by_category["Core"].append(f"{method} {path}")
        elif "/jobs" in path:
            by_category["Job Management"].append(f"{method} {path}")
        elif "/candidates" in path:
            by_category["Candidate Management"].append(f"{method} {path}")
        elif "/match" in path:
            by_category["AI Matching"].append(f"{method} {path}")
        elif "/interviews" in path:
            by_category["Interview Management"].append(f"{method} {path}")
        elif "/client" in path:
            by_category["Client Portal"].append(f"{method} {path}")
        elif "/stats" in path:
            by_category["Analytics"].append(f"{method} {path}")
        elif "/metrics" in path or "/health/detailed" in path:
            by_category["Monitoring"].append(f"{method} {path}")
    
    print(f"TOTAL ENDPOINTS: {len(endpoints)}")
    print()
    
    print("BY HTTP METHOD:")
    for method, paths in by_method.items():
        print(f"  {method}: {len(paths)}")
    print()
    
    print("BY CATEGORY:")
    for category, endpoints_list in by_category.items():
        if endpoints_list:
            print(f"  {category}: {len(endpoints_list)}")
            for endpoint in endpoints_list:
                print(f"    - {endpoint}")
    print()
    
    print("COMPLETE ENDPOINT LIST:")
    for i, (method, path) in enumerate(endpoints, 1):
        print(f"{i:2d}. {method.upper()} {path}")

if __name__ == "__main__":
    count_endpoints()