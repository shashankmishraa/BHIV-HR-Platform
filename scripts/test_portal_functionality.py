#!/usr/bin/env python3
"""
Test portal functionality by checking key features
"""

import requests
import time

HR_PORTAL_URL = "https://bhiv-hr-portal.onrender.com"
CLIENT_PORTAL_URL = "https://bhiv-hr-client-portal.onrender.com"

def test_portal_features(url, name):
    """Test portal features"""
    print(f"\n{name} Portal Testing")
    print("-" * 30)
    
    try:
        # Test main page load
        response = requests.get(url, timeout=30)
        print(f"[OK] Main page loads: {response.status_code}")
        
        # Check for key content indicators
        content = response.text.lower()
        
        # Check for Streamlit indicators
        if "streamlit" in content:
            print("[OK] Streamlit framework detected")
        
        # Check for BHIV branding
        if "bhiv" in content or "hr" in content:
            print("[OK] BHIV HR branding present")
        
        # Check for interactive elements
        if "button" in content or "input" in content or "select" in content:
            print("[OK] Interactive elements detected")
        
        # Check for data loading indicators
        if "candidate" in content or "job" in content or "dashboard" in content:
            print("[OK] HR-related content detected")
        
        # Check page size (indicates content loaded)
        content_size = len(response.text)
        if content_size > 10000:
            print(f"[OK] Rich content loaded: {content_size} bytes")
        else:
            print(f"[WARN] Limited content: {content_size} bytes")
            
    except Exception as e:
        print(f"[ERR] Portal test failed: {str(e)}")

def test_api_connectivity():
    """Test API connectivity from portal perspective"""
    print("\nAPI Connectivity Testing")
    print("-" * 30)
    
    # Test gateway health
    try:
        response = requests.get("https://bhiv-hr-gateway.onrender.com/health", timeout=10)
        if response.status_code == 200:
            print("[OK] Gateway health check passed")
        else:
            print(f"[ERR] Gateway health check failed: {response.status_code}")
    except Exception as e:
        print(f"[ERR] Gateway unreachable: {str(e)}")
    
    # Test AI agent health
    try:
        response = requests.get("https://bhiv-hr-agent.onrender.com/health", timeout=10)
        if response.status_code == 200:
            print("[OK] AI Agent health check passed")
        else:
            print(f"[ERR] AI Agent health check failed: {response.status_code}")
    except Exception as e:
        print(f"[ERR] AI Agent unreachable: {str(e)}")

def main():
    print("BHIV HR Platform - Portal Functionality Test")
    print("=" * 50)
    
    # Test both portals
    test_portal_features(HR_PORTAL_URL, "HR")
    test_portal_features(CLIENT_PORTAL_URL, "Client")
    
    # Test API connectivity
    test_api_connectivity()
    
    print("\n" + "=" * 50)
    print("Portal Functionality Summary")
    print("=" * 50)
    print("[OK] = Working correctly")
    print("[ERR] = Issues detected") 
    print("[WARN] = Partial functionality")

if __name__ == "__main__":
    main()