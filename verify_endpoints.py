#!/usr/bin/env python3
"""
Endpoint Verification Script
Counts endpoints in code files vs live services
"""

import requests
import re
import os

def count_gateway_endpoints():
    """Count endpoints in Gateway main.py"""
    gateway_file = "c:/BHIV-HR-Platform/services/gateway/app/main.py"
    
    with open(gateway_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count @app.get, @app.post, @app.put, @app.delete decorators
    endpoints = re.findall(r'@app\.(get|post|put|delete)\(', content)
    
    return len(endpoints)

def count_agent_endpoints():
    """Count endpoints in Agent app.py"""
    agent_file = "c:/BHIV-HR-Platform/services/agent/app.py"
    
    try:
        with open(agent_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        endpoints = re.findall(r'@app\.(get|post|put|delete)\(', content)
        return len(endpoints)
    except FileNotFoundError:
        return 0

def test_live_gateway():
    """Test live Gateway service endpoints"""
    try:
        response = requests.get("https://bhiv-hr-gateway-46pz.onrender.com/docs", timeout=10)
        if response.status_code == 200:
            # Count endpoints from OpenAPI docs
            content = response.text
            # Look for path definitions in the docs
            paths = re.findall(r'"(/[^"]*)":\s*{', content)
            return len(set(paths))  # Remove duplicates
        return 0
    except:
        return 0

def test_live_agent():
    """Test live Agent service endpoints"""
    try:
        response = requests.get("https://bhiv-hr-agent-m1me.onrender.com/docs", timeout=10)
        if response.status_code == 200:
            content = response.text
            paths = re.findall(r'"(/[^"]*)":\s*{', content)
            return len(set(paths))
        return 0
    except:
        return 0

def main():
    print("BHIV HR Platform Endpoint Verification")
    print("=" * 50)
    
    # Count code endpoints
    gateway_code = count_gateway_endpoints()
    agent_code = count_agent_endpoints()
    
    print(f"Code Files:")
    print(f"   Gateway endpoints: {gateway_code}")
    print(f"   Agent endpoints: {agent_code}")
    print(f"   Total code endpoints: {gateway_code + agent_code}")
    
    # Test live services
    print(f"\nLive Services:")
    gateway_live = test_live_gateway()
    agent_live = test_live_agent()
    
    print(f"   Gateway live endpoints: {gateway_live}")
    print(f"   Agent live endpoints: {agent_live}")
    print(f"   Total live endpoints: {gateway_live + agent_live}")
    
    # Comparison
    print(f"\nVerification:")
    gateway_match = "MATCH" if gateway_code == gateway_live else "MISMATCH"
    agent_match = "MATCH" if agent_code == agent_live else "MISMATCH"
    
    print(f"   Gateway match: {gateway_match} ({gateway_code} code vs {gateway_live} live)")
    print(f"   Agent match: {agent_match} ({agent_code} code vs {agent_live} live)")
    
    if gateway_code == gateway_live and agent_code == agent_live:
        print(f"\nResult: ENDPOINTS MATCH")
    else:
        print(f"\nResult: ENDPOINTS MISMATCH")

if __name__ == "__main__":
    main()