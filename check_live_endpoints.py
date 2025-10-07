#!/usr/bin/env python3
"""
Direct Live Endpoint Check
"""

import requests

def check_gateway():
    """Check Gateway service"""
    try:
        # Test root endpoint
        response = requests.get("https://bhiv-hr-gateway-46pz.onrender.com/", timeout=10)
        print(f"Gateway root: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Gateway info: {data}")
        
        # Test docs endpoint
        docs_response = requests.get("https://bhiv-hr-gateway-46pz.onrender.com/docs", timeout=10)
        print(f"Gateway docs: {docs_response.status_code}")
        
    except Exception as e:
        print(f"Gateway error: {e}")

def check_agent():
    """Check Agent service"""
    try:
        # Test root endpoint
        response = requests.get("https://bhiv-hr-agent-m1me.onrender.com/", timeout=10)
        print(f"Agent root: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Agent info: {data}")
        
        # Test docs endpoint
        docs_response = requests.get("https://bhiv-hr-agent-m1me.onrender.com/docs", timeout=10)
        print(f"Agent docs: {docs_response.status_code}")
        
    except Exception as e:
        print(f"Agent error: {e}")

if __name__ == "__main__":
    print("Checking Live Services...")
    print("=" * 30)
    check_gateway()
    print()
    check_agent()