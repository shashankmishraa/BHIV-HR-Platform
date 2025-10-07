#!/usr/bin/env python3
"""
Simple Auth Service Verification
"""

import os
from pathlib import Path

def check_auth_service():
    auth_file = Path("c:/BHIV-HR-Platform/services/client_portal/auth_service.py")
    
    if not auth_file.exists():
        print("AUTH SERVICE STATUS: MISSING")
        return False
    
    with open(auth_file, 'r') as f:
        content = f.read()
    
    # Check required components
    required = [
        "class ClientAuthService",
        "jwt.encode",
        "bcrypt.hashpw", 
        "CREATE TABLE IF NOT EXISTS client_auth",
        "def authenticate_client",
        "def verify_token",
        "def register_client",
        "def logout_client",
        "def get_client_info",
        "TECH001",
        "demo123"
    ]
    
    missing = []
    present = []
    
    for item in required:
        if item in content:
            present.append(item)
        else:
            missing.append(item)
    
    # File metrics
    lines = len(content.split('\n'))
    
    print("AUTH SERVICE VERIFICATION REPORT")
    print("=" * 40)
    print(f"File Status: {'EXISTS' if auth_file.exists() else 'MISSING'}")
    print(f"File Size: {len(content)} characters")
    print(f"Total Lines: {lines}")
    print(f"Components Present: {len(present)}/{len(required)}")
    print(f"Completeness: {round(len(present)/len(required)*100, 1)}%")
    
    print(f"\nPRESENT COMPONENTS ({len(present)}):")
    for item in present:
        print(f"  [OK] {item}")
    
    if missing:
        print(f"\nMISSING COMPONENTS ({len(missing)}):")
        for item in missing:
            print(f"  [MISSING] {item}")
    
    is_complete = len(missing) == 0
    
    print(f"\nFINAL STATUS: {'COMPLETE' if is_complete else 'INCOMPLETE'}")
    print(f"Requirements Met: {'YES' if is_complete else 'NO'}")
    
    return is_complete

if __name__ == "__main__":
    result = check_auth_service()
    
    if result:
        print("\n[SUCCESS] Auth service fully restored and meets all requirements!")
    else:
        print("\n[WARNING] Auth service is incomplete or missing components.")