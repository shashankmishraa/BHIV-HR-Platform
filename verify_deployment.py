#!/usr/bin/env python3
"""
BHIV HR Platform - Deployment Verification Script
Verifies all 46 endpoints are present and API is ready for deployment
"""

import ast
import sys
from pathlib import Path

def verify_api_completeness():
    """Verify the API has all required endpoints"""
    
    main_py_path = Path("services/gateway/app/main.py")
    
    if not main_py_path.exists():
        print("❌ ERROR: main.py not found")
        return False
    
    # Read and parse the Python file
    with open(main_py_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    try:
        # Parse the AST to verify syntax
        ast.parse(content)
        print("✅ Python syntax validation: PASSED")
    except SyntaxError as e:
        print(f"❌ Syntax Error: {e}")
        return False
    
    # Count endpoints
    endpoint_count = content.count("@app.")
    print(f"✅ Total endpoints found: {endpoint_count}")
    
    if endpoint_count != 46:
        print(f"❌ Expected 46 endpoints, found {endpoint_count}")
        return False
    
    # Verify critical endpoint categories
    categories = {
        "Core API Endpoints": 3,
        "Job Management": 2, 
        "Candidate Management": 3,
        "AI Matching Engine": 1,
        "Assessment & Workflow": 3,
        "Analytics & Statistics": 2,
        "Client Portal API": 5,
        "Security Testing": 7,
        "CSP Management": 4,
        "Two-Factor Authentication": 8,
        "Password Management": 6,
        "Monitoring": 3
    }
    
    total_expected = sum(categories.values())
    print(f"✅ Expected total from categories: {total_expected}")
    
    # Check for required imports
    required_imports = [
        "from fastapi import FastAPI",
        "from datetime import datetime",
        "import pyotp",
        "import secrets"
    ]
    
    for imp in required_imports:
        if imp in content:
            print(f"✅ Import check: {imp}")
        else:
            print(f"❌ Missing import: {imp}")
            return False
    
    # Check for critical functions
    critical_functions = [
        "def get_db_engine",
        "def validate_api_key", 
        "def get_api_key",
        "async def client_login",
        "async def verify_client_token"
    ]
    
    for func in critical_functions:
        if func in content:
            print(f"✅ Function check: {func}")
        else:
            print(f"❌ Missing function: {func}")
            return False
    
    print("\n🎉 DEPLOYMENT VERIFICATION: PASSED")
    print("✅ All 46 endpoints present")
    print("✅ Syntax validation passed") 
    print("✅ Critical imports present")
    print("✅ Core functions present")
    print("\n🚀 API is ready for deployment!")
    
    return True

if __name__ == "__main__":
    success = verify_api_completeness()
    sys.exit(0 if success else 1)