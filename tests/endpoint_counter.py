#!/usr/bin/env python3
"""
Count actual endpoints in the codebase
"""

import re
import os

def count_gateway_endpoints():
    """Count endpoints in gateway service"""
    gateway_file = "c:\\BHIV-HR-Platform\\services\\gateway\\app\\main.py"
    
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

def count_agent_endpoints():
    """Count endpoints in agent service"""
    agent_file = "c:\\BHIV-HR-Platform\\services\\agent\\app.py"
    
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

def main():
    print("BHIV HR Platform - Endpoint Counter")
    print("=" * 50)
    
    gateway_endpoints = count_gateway_endpoints()
    agent_endpoints = count_agent_endpoints()
    
    print(f"GATEWAY ENDPOINTS ({len(gateway_endpoints)}):")
    for i, endpoint in enumerate(gateway_endpoints, 1):
        print(f"  {i:2d}. {endpoint}")
    
    print(f"\nAGENT ENDPOINTS ({len(agent_endpoints)}):")
    for i, endpoint in enumerate(agent_endpoints, 1):
        print(f"  {i:2d}. {endpoint}")
    
    print(f"\nTOTAL ENDPOINTS: {len(gateway_endpoints) + len(agent_endpoints)}")
    print(f"Gateway: {len(gateway_endpoints)}")
    print(f"Agent: {len(agent_endpoints)}")

if __name__ == "__main__":
    main()