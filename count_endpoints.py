#!/usr/bin/env python3
"""
Simple endpoint counter
"""
import re

def count_endpoints_in_file(filepath):
    """Count endpoints in a Python file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all @app.method patterns
        patterns = [
            r'@app\.get\(',
            r'@app\.post\(',
            r'@app\.put\(',
            r'@app\.delete\(',
            r'@app\.patch\('
        ]
        
        endpoints = []
        for pattern in patterns:
            matches = re.findall(pattern, content)
            endpoints.extend(matches)
        
        # Find route paths
        route_patterns = r'@app\.(get|post|put|delete|patch)\("([^"]+)"'
        routes = re.findall(route_patterns, content)
        
        print(f"Found {len(routes)} endpoints in {filepath}:")
        for method, path in routes:
            print(f"  {method.upper()} {path}")
        
        return len(routes)
        
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return 0

if __name__ == "__main__":
    # Count Gateway endpoints
    gateway_file = "services/gateway/app/main.py"
    gateway_count = count_endpoints_in_file(gateway_file)
    
    # Count AI Agent endpoints  
    agent_file = "services/agent/app.py"
    agent_count = count_endpoints_in_file(agent_file)
    
    total = gateway_count + agent_count
    percentage = (total / 122) * 100
    
    print(f"\n=== ENDPOINT SUMMARY ===")
    print(f"Gateway Service: {gateway_count} endpoints")
    print(f"AI Agent Service: {agent_count} endpoints")
    print(f"Total Implemented: {total} endpoints")
    print(f"Target: 122 endpoints")
    print(f"Completion: {percentage:.1f}%")
    print(f"Remaining: {122 - total} endpoints")