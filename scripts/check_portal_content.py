#!/usr/bin/env python3
"""
Check portal content after deployment
"""

import requests

def check_portal_content():
    portals = [
        ("HR Portal", "https://bhiv-hr-portal.onrender.com"),
        ("Client Portal", "https://bhiv-hr-client-portal.onrender.com")
    ]
    
    print("Portal Content Check After Deployment")
    print("=" * 50)
    
    for name, url in portals:
        try:
            response = requests.get(url, timeout=15)
            content_size = len(response.text)
            
            print(f"\n{name}:")
            print(f"  Status: {response.status_code}")
            print(f"  Content Size: {content_size} bytes")
            
            if content_size > 5000:
                print(f"  Status: [OK] Full content loaded")
            elif content_size > 1000:
                print(f"  Status: [PARTIAL] Some content loaded")
            else:
                print(f"  Status: [LIMITED] Minimal content")
                
            # Check for key indicators
            content = response.text.lower()
            if "streamlit" in content:
                print(f"  Framework: Streamlit detected")
            if "bhiv" in content:
                print(f"  Branding: BHIV detected")
            if "dashboard" in content or "portal" in content:
                print(f"  Features: Dashboard elements detected")
                
        except Exception as e:
            print(f"\n{name}: ERROR - {str(e)}")

if __name__ == "__main__":
    check_portal_content()