#!/usr/bin/env python3
"""
BHIV HR Platform - Simple System Verification
Verifies credentials and basic functionality
"""

import os
import requests
import psycopg2
from datetime import datetime

def check_environment_variables():
    """Check environment variables"""
    print("Step 1: Checking Environment Variables...")
    
    required_vars = {
        "DATABASE_URL": os.getenv("DATABASE_URL"),
        "API_KEY_SECRET": os.getenv("API_KEY_SECRET"), 
        "JWT_SECRET": os.getenv("JWT_SECRET")
    }
    
    missing = []
    for var, value in required_vars.items():
        if not value:
            missing.append(var)
        else:
            print(f"  OK: {var} is set")
    
    if missing:
        print(f"  ERROR: Missing variables: {missing}")
        return False
    
    print("  PASS: All required environment variables are set")
    return True

def check_database_connection():
    """Test database connection"""
    print("\nStep 2: Testing Database Connection...")
    
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("  ERROR: DATABASE_URL not found")
        return False
    
    try:
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        print(f"  PASS: Connected to PostgreSQL")
        print(f"  Version: {version[:50]}...")
        return True
        
    except Exception as e:
        print(f"  ERROR: Database connection failed: {str(e)}")
        return False

def check_service_urls():
    """Test service URL accessibility"""
    print("\nStep 3: Testing Service URLs...")
    
    urls = {
        "Gateway": "https://bhiv-hr-gateway-46pz.onrender.com",
        "Agent": "https://bhiv-hr-agent-m1me.onrender.com",
        "Portal": "https://bhiv-hr-portal-cead.onrender.com", 
        "Client Portal": "https://bhiv-hr-client-portal-5g33.onrender.com"
    }
    
    all_accessible = True
    
    for name, url in urls.items():
        try:
            response = requests.get(f"{url}/health", timeout=10)
            if response.status_code < 400:
                print(f"  PASS: {name} accessible ({response.status_code})")
            else:
                print(f"  WARN: {name} returned {response.status_code}")
                all_accessible = False
        except Exception as e:
            print(f"  ERROR: {name} not accessible - {str(e)}")
            all_accessible = False
    
    return all_accessible

def check_api_authentication():
    """Test API authentication"""
    print("\nStep 4: Testing API Authentication...")
    
    api_key = os.getenv("API_KEY_SECRET")
    if not api_key:
        print("  ERROR: API_KEY_SECRET not found")
        return False
    
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        response = requests.get(
            "https://bhiv-hr-gateway-46pz.onrender.com/candidates",
            headers=headers,
            timeout=10
        )
        
        if response.status_code < 500:  # Allow 401/403 but not 500
            print(f"  PASS: API authentication working ({response.status_code})")
            return True
        else:
            print(f"  ERROR: API returned {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ERROR: API test failed - {str(e)}")
        return False

def main():
    """Run verification"""
    print("BHIV HR Platform - System Verification")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    tests = [
        check_environment_variables,
        check_database_connection, 
        check_service_urls,
        check_api_authentication
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"  ERROR: Test failed - {str(e)}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 50)
    print("VERIFICATION SUMMARY")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("STATUS: ALL SYSTEMS OPERATIONAL")
        return True
    else:
        print("STATUS: ISSUES DETECTED")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)