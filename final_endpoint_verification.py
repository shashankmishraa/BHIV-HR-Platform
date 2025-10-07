#!/usr/bin/env python3
"""
Final Endpoint Verification Report
Comprehensive check of code vs live endpoints
"""

import requests
import re

def count_code_endpoints():
    """Count endpoints in code files"""
    
    # Gateway endpoints
    gateway_file = "c:/BHIV-HR-Platform/services/gateway/app/main.py"
    with open(gateway_file, 'r', encoding='utf-8') as f:
        gateway_content = f.read()
    
    gateway_endpoints = re.findall(r'@app\.(get|post|put|delete)\(', gateway_content)
    
    # Agent endpoints  
    agent_file = "c:/BHIV-HR-Platform/services/agent/app.py"
    with open(agent_file, 'r', encoding='utf-8') as f:
        agent_content = f.read()
    
    agent_endpoints = re.findall(r'@app\.(get|post|put|delete)\(', agent_content)
    
    return len(gateway_endpoints), len(agent_endpoints)

def check_live_services():
    """Check live service status and endpoint counts"""
    
    # Gateway check
    try:
        gateway_response = requests.get("https://bhiv-hr-gateway-46pz.onrender.com/", timeout=10)
        if gateway_response.status_code == 200:
            gateway_data = gateway_response.json()
            gateway_live_count = gateway_data.get('endpoints', 0)
            gateway_status = "LIVE"
        else:
            gateway_live_count = 0
            gateway_status = f"ERROR {gateway_response.status_code}"
    except:
        gateway_live_count = 0
        gateway_status = "OFFLINE"
    
    # Agent check
    try:
        agent_response = requests.get("https://bhiv-hr-agent-m1me.onrender.com/", timeout=10)
        if agent_response.status_code == 200:
            agent_data = agent_response.json()
            # Count endpoints from service info
            agent_live_count = len(agent_data.get('endpoints', {}))
            agent_status = "LIVE"
        else:
            agent_live_count = 0
            agent_status = f"ERROR {agent_response.status_code}"
    except:
        agent_live_count = 0
        agent_status = "OFFLINE"
    
    return gateway_live_count, gateway_status, agent_live_count, agent_status

def main():
    print("BHIV HR Platform - Final Endpoint Verification")
    print("=" * 55)
    
    # Count code endpoints
    gateway_code, agent_code = count_code_endpoints()
    total_code = gateway_code + agent_code
    
    print("CODE FILES:")
    print(f"  Gateway Service: {gateway_code} endpoints")
    print(f"  Agent Service:   {agent_code} endpoints")
    print(f"  Total Code:      {total_code} endpoints")
    
    # Check live services
    gateway_live, gateway_status, agent_live, agent_status = check_live_services()
    total_live = gateway_live + agent_live
    
    print(f"\nLIVE SERVICES:")
    print(f"  Gateway Service: {gateway_live} endpoints ({gateway_status})")
    print(f"  Agent Service:   {agent_live} endpoints ({agent_status})")
    print(f"  Total Live:      {total_live} endpoints")
    
    # Verification
    print(f"\nVERIFICATION:")
    gateway_match = "MATCH" if gateway_code == gateway_live else "MISMATCH"
    agent_match = "MATCH" if agent_code == agent_live else "MISMATCH"
    
    print(f"  Gateway: {gateway_match} ({gateway_code} code vs {gateway_live} live)")
    print(f"  Agent:   {agent_match} ({agent_code} code vs {agent_live} live)")
    
    # Final status
    if gateway_code == gateway_live and agent_code == agent_live:
        print(f"\nRESULT: ENDPOINTS VERIFIED - ALL MATCH")
    else:
        print(f"\nRESULT: VERIFICATION FAILED - MISMATCH DETECTED")
        
    # Additional info
    print(f"\nSERVICE STATUS:")
    print(f"  Gateway: {gateway_status}")
    print(f"  Agent:   {agent_status}")
    
    # README verification
    print(f"\nREADME CLAIMS:")
    print(f"  Claims 53 total endpoints (48 Gateway + 5 Agent)")
    print(f"  Actual: {total_code} total endpoints ({gateway_code} Gateway + {agent_code} Agent)")
    
    readme_accurate = (total_code == 53 and gateway_code == 48 and agent_code == 5)
    print(f"  README Accuracy: {'CORRECT' if readme_accurate else 'NEEDS UPDATE'}")

if __name__ == "__main__":
    main()