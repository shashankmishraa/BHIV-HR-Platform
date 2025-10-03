#!/usr/bin/env python3
"""
BHIV HR Platform - Thorough Endpoint Scanner
Scans Gateway and Agent service files to count all HTTP endpoints
"""

import re
import os

def scan_file_for_endpoints(file_path, service_name):
    """Scan a single file for all HTTP endpoints"""
    if not os.path.exists(file_path):
        print(f"ERROR: File not found: {file_path}")
        return []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all @app.method decorators
    patterns = [
        (r'@app\.get\("([^"]+)"', 'GET'),
        (r'@app\.post\("([^"]+)"', 'POST'),
        (r'@app\.put\("([^"]+)"', 'PUT'),
        (r'@app\.delete\("([^"]+)"', 'DELETE'),
        (r'@app\.patch\("([^"]+)"', 'PATCH')
    ]
    
    endpoints = []
    for pattern, method in patterns:
        matches = re.findall(pattern, content)
        for match in matches:
            endpoints.append({
                'method': method,
                'path': match,
                'endpoint': f"{method} {match}",
                'service': service_name
            })
    
    return endpoints

def extract_function_names(file_path):
    """Extract function names associated with endpoints"""
    if not os.path.exists(file_path):
        return {}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find @app.method("path") followed by function definition
    pattern = r'@app\.(get|post|put|delete|patch)\("([^"]+)"\)[^)]*\)\s*(?:async\s+)?def\s+(\w+)'
    matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
    
    endpoint_functions = {}
    for method, path, func_name in matches:
        endpoint_key = f"{method.upper()} {path}"
        endpoint_functions[endpoint_key] = func_name
    
    return endpoint_functions

def count_lines_in_file(file_path):
    """Count total lines in file"""
    if not os.path.exists(file_path):
        return 0
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return len(f.readlines())

def main():
    print("BHIV HR Platform - Thorough Endpoint Scanner")
    print("=" * 60)
    
    # File paths
    gateway_file = r"c:\BHIV-HR-Platform\services\gateway\app\main.py"
    agent_file = r"c:\BHIV-HR-Platform\services\agent\app.py"
    
    # Scan Gateway service
    print("SCANNING GATEWAY SERVICE...")
    print(f"File: {gateway_file}")
    gateway_endpoints = scan_file_for_endpoints(gateway_file, "Gateway")
    gateway_functions = extract_function_names(gateway_file)
    gateway_lines = count_lines_in_file(gateway_file)
    
    print(f"File size: {gateway_lines} lines")
    print(f"Endpoints found: {len(gateway_endpoints)}")
    print()
    
    # Scan Agent service
    print("SCANNING AGENT SERVICE...")
    print(f"File: {agent_file}")
    agent_endpoints = scan_file_for_endpoints(agent_file, "Agent")
    agent_functions = extract_function_names(agent_file)
    agent_lines = count_lines_in_file(agent_file)
    
    print(f"File size: {agent_lines} lines")
    print(f"Endpoints found: {len(agent_endpoints)}")
    print()
    
    # Detailed Gateway endpoints
    print("GATEWAY SERVICE ENDPOINTS:")
    print("-" * 40)
    for i, endpoint in enumerate(sorted(gateway_endpoints, key=lambda x: x['path']), 1):
        func_name = gateway_functions.get(endpoint['endpoint'], 'unknown')
        print(f"{i:2d}. {endpoint['method']:6s} {endpoint['path']:40s} -> {func_name}")
    
    print()
    
    # Detailed Agent endpoints
    print("AGENT SERVICE ENDPOINTS:")
    print("-" * 40)
    for i, endpoint in enumerate(sorted(agent_endpoints, key=lambda x: x['path']), 1):
        func_name = agent_functions.get(endpoint['endpoint'], 'unknown')
        print(f"{i:2d}. {endpoint['method']:6s} {endpoint['path']:40s} -> {func_name}")
    
    print()
    
    # Summary by HTTP method
    all_endpoints = gateway_endpoints + agent_endpoints
    method_counts = {}
    for endpoint in all_endpoints:
        method = endpoint['method']
        method_counts[method] = method_counts.get(method, 0) + 1
    
    print("SUMMARY BY HTTP METHOD:")
    print("-" * 30)
    for method, count in sorted(method_counts.items()):
        print(f"{method:8s}: {count:2d} endpoints")
    
    print()
    
    # Service breakdown
    print("SERVICE BREAKDOWN:")
    print("-" * 30)
    print(f"Gateway Service: {len(gateway_endpoints):2d} endpoints")
    print(f"Agent Service:   {len(agent_endpoints):2d} endpoints")
    print(f"Total:           {len(all_endpoints):2d} endpoints")
    
    print()
    
    # Path analysis
    print("PATH ANALYSIS:")
    print("-" * 30)
    path_prefixes = {}
    for endpoint in all_endpoints:
        path = endpoint['path']
        if path.startswith('/v1/'):
            prefix = '/v1/' + path.split('/')[2] if len(path.split('/')) > 2 else '/v1/'
        elif path == '/':
            prefix = 'root'
        else:
            prefix = '/' + path.split('/')[1] if len(path.split('/')) > 1 else 'other'
        
        path_prefixes[prefix] = path_prefixes.get(prefix, 0) + 1
    
    for prefix, count in sorted(path_prefixes.items()):
        print(f"{prefix:25s}: {count:2d} endpoints")
    
    print()
    
    # Verification
    print("VERIFICATION:")
    print("-" * 30)
    expected_gateway = 48  # Based on previous audit
    expected_agent = 5     # Based on previous audit
    expected_total = expected_gateway + expected_agent
    
    gateway_status = "OK" if len(gateway_endpoints) == expected_gateway else "FAIL"
    agent_status = "OK" if len(agent_endpoints) == expected_agent else "FAIL"
    total_status = "OK" if len(all_endpoints) == expected_total else "FAIL"
    
    print(f"Gateway: {gateway_status} {len(gateway_endpoints)}/{expected_gateway} endpoints")
    print(f"Agent:   {agent_status} {len(agent_endpoints)}/{expected_agent} endpoints")
    print(f"Total:   {total_status} {len(all_endpoints)}/{expected_total} endpoints")
    
    if len(all_endpoints) == expected_total:
        print("\nALL ENDPOINTS VERIFIED!")
    else:
        print(f"\nMISMATCH: Expected {expected_total}, Found {len(all_endpoints)}")
    
    return all_endpoints

if __name__ == "__main__":
    main()