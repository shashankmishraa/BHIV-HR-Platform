#!/usr/bin/env python3
"""
Check Agent Service Status
"""

import requests
from datetime import datetime

AGENT_URL = "https://bhiv-hr-agent-m1me.onrender.com"

def check_agent_status():
    print("BHIV HR Platform - Agent Service Status Check")
    print("=" * 50)
    print(f"Agent URL: {AGENT_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test with different timeouts
    timeouts = [5, 15, 30, 60]
    
    for timeout in timeouts:
        print(f"Testing with {timeout}s timeout...")
        try:
            response = requests.get(f"{AGENT_URL}/health", timeout=timeout)
            if response.status_code == 200:
                print(f"SUCCESS: Agent responded in {timeout}s")
                print(f"Response: {response.json()}")
                return True
            else:
                print(f"FAIL: Status {response.status_code}")
        except requests.exceptions.Timeout:
            print(f"TIMEOUT: No response in {timeout}s")
        except Exception as e:
            print(f"ERROR: {str(e)}")
    
    print("\nAgent service appears to be down or very slow")
    return False

if __name__ == "__main__":
    check_agent_status()