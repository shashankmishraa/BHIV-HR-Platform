#!/usr/bin/env python3
"""
Quick Deployment Status Checker
"""

import requests
import json

# Service URLs
services = {
    'Gateway': 'https://bhiv-hr-gateway.onrender.com/health',
    'Agent': 'https://bhiv-hr-agent.onrender.com/health', 
    'Portal': 'https://bhiv-hr-portal.onrender.com',
    'Client Portal': 'https://bhiv-hr-client-portal.onrender.com'
}

print("BHIV HR Platform - Deployment Status Check")
print("=" * 50)

for service_name, url in services.items():
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"ONLINE  | {service_name}")
        else:
            print(f"ISSUES  | {service_name} ({response.status_code})")
    except Exception as e:
        print(f"OFFLINE | {service_name} - {str(e)}")

print("\nDeployment IDs from triggers:")
print("HR Portal: dep-d3664qffte5s739fok10")
print("Client Portal: dep-d3664t1r0fns73blk250") 
print("Gateway: dep-d3664vjuibrs73dq2am0")
print("Agent: dep-d366523ipnbc73a19l2g")