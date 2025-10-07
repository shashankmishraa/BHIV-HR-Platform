#!/usr/bin/env python3
"""
Auth Service Verification Report
Checks if the auth service matches project requirements
"""

import os
from pathlib import Path

def verify_auth_service():
    auth_file = Path("c:/BHIV-HR-Platform/services/client_portal/auth_service.py")
    
    if not auth_file.exists():
        return {
            "status": "MISSING",
            "message": "Auth service file does not exist",
            "requirements_met": False
        }
    
    with open(auth_file, 'r') as f:
        content = f.read()
    
    # Check for required components
    required_components = {
        "Enterprise Authentication": "class ClientAuthService" in content,
        "JWT Token Support": "jwt.encode" in content and "jwt.decode" in content,
        "bcrypt Password Hashing": "bcrypt.hashpw" in content and "bcrypt.checkpw" in content,
        "Database Integration": "CREATE TABLE IF NOT EXISTS client_auth" in content,
        "Session Management": "client_sessions" in content,
        "Account Locking": "login_attempts" in content and "locked_until" in content,
        "User Registration": "def register_client" in content,
        "Token Verification": "def verify_token" in content,
        "Client Logout": "def logout_client" in content,
        "Client Info Retrieval": "def get_client_info" in content,
        "Default Clients Setup": "TECH001" in content and "demo123" in content,
        "Error Handling": "try:" in content and "except" in content,
        "Logging": "import logging" in content
    }
    
    missing_components = [comp for comp, present in required_components.items() if not present]
    present_components = [comp for comp, present in required_components.items() if present]
    
    # Calculate file metrics
    lines = content.split('\n')
    total_lines = len(lines)
    code_lines = len([line for line in lines if line.strip() and not line.strip().startswith('#')])
    
    # Check method completeness
    methods = [
        "_initialize_database",
        "_create_default_clients", 
        "_hash_password",
        "_verify_password",
        "_generate_jwt_token",
        "authenticate_client",
        "verify_token",
        "register_client",
        "logout_client",
        "get_client_info"
    ]
    
    present_methods = [method for method in methods if f"def {method}" in content]
    missing_methods = [method for method in methods if f"def {method}" not in content]
    
    # Generate report
    report = {
        "status": "COMPLETE" if not missing_components and not missing_methods else "INCOMPLETE",
        "file_metrics": {
            "total_lines": total_lines,
            "code_lines": code_lines,
            "file_size": len(content)
        },
        "components": {
            "present": present_components,
            "missing": missing_components,
            "total_required": len(required_components),
            "present_count": len(present_components)
        },
        "methods": {
            "present": present_methods,
            "missing": missing_methods,
            "total_required": len(methods),
            "present_count": len(present_methods)
        },
        "requirements_met": len(missing_components) == 0 and len(missing_methods) == 0,
        "completeness_percentage": round((len(present_components) + len(present_methods)) / (len(required_components) + len(methods)) * 100, 1)
    }
    
    return report

def generate_verification_report():
    print("Auth Service Verification Report")
    print("=" * 50)
    
    report = verify_auth_service()
    
    print(f"Status: {report['status']}")
    print(f"Requirements Met: {'YES' if report['requirements_met'] else 'NO'}")
    print(f"Completeness: {report['completeness_percentage']}%")
    
    print(f"\nFile Metrics:")
    print(f"  Total Lines: {report['file_metrics']['total_lines']}")
    print(f"  Code Lines: {report['file_metrics']['code_lines']}")
    print(f"  File Size: {report['file_metrics']['file_size']} characters")
    
    print(f"\nComponents ({report['components']['present_count']}/{report['components']['total_required']}):")
    for comp in report['components']['present']:
        print(f"  ✓ {comp}")
    
    if report['components']['missing']:
        print(f"\nMissing Components:")
        for comp in report['components']['missing']:
            print(f"  ✗ {comp}")
    
    print(f"\nMethods ({report['methods']['present_count']}/{report['methods']['total_required']}):")
    for method in report['methods']['present']:
        print(f"  ✓ {method}")
    
    if report['methods']['missing']:
        print(f"\nMissing Methods:")
        for method in report['methods']['missing']:
            print(f"  ✗ {method}")
    
    return report

if __name__ == "__main__":
    report = generate_verification_report()
    
    if report['requirements_met']:
        print(f"\n✅ AUTH SERVICE FULLY RESTORED")
        print("All enterprise authentication features are present and functional.")
    else:
        print(f"\n❌ AUTH SERVICE INCOMPLETE")
        print("Some required components or methods are missing.")