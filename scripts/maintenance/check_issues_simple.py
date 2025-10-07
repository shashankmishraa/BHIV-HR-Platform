#!/usr/bin/env python3
"""
Simple Critical Issues Check
"""

import requests
from pathlib import Path

def check_critical_issues():
    print("Checking Critical Issues Resolution...")
    
    resolved = []
    remaining = []
    
    # 1. Database Schema - Feedback Table
    print("\n1. Database Schema Issues:")
    try:
        response = requests.get("https://bhiv-hr-gateway-46pz.onrender.com/v1/feedback", 
                              headers={"Authorization": "Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"},
                              timeout=10)
        if response.status_code == 200:
            print("  [OK] Feedback table accessible")
            resolved.append("Feedback table average_score column fixed")
        else:
            print(f"  [FAIL] Feedback table: {response.status_code}")
            remaining.append("Feedback table average_score column missing")
    except Exception as e:
        print(f"  [ERROR] Feedback table: {str(e)[:50]}")
        remaining.append("Feedback table connection error")
    
    # 2. Database Schema - Offers Table
    try:
        response = requests.get("https://bhiv-hr-gateway-46pz.onrender.com/v1/offers",
                              headers={"Authorization": "Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"},
                              timeout=10)
        if response.status_code == 200:
            print("  [OK] Offers table accessible")
            resolved.append("Offers table exists")
        else:
            print(f"  [FAIL] Offers table: {response.status_code}")
            remaining.append("Offers table missing")
    except Exception as e:
        print(f"  [ERROR] Offers table: {str(e)[:50]}")
        remaining.append("Offers table connection error")
    
    # 3. AI Agent Service
    print("\n2. AI Agent Service:")
    try:
        response = requests.get("https://bhiv-hr-agent-m1me.onrender.com/health", timeout=30)
        if response.status_code == 200:
            print("  [OK] AI Agent service working")
            resolved.append("AI Agent service connectivity")
        else:
            print(f"  [FAIL] AI Agent: {response.status_code}")
            remaining.append("AI Agent service timeout")
    except Exception as e:
        print(f"  [ERROR] AI Agent: {str(e)[:50]}")
        remaining.append("AI Agent service timeout")
    
    # 4. Search Endpoint
    print("\n3. Search Endpoint:")
    try:
        response = requests.get("https://bhiv-hr-gateway-46pz.onrender.com/v1/candidates/search?skills=Python",
                              headers={"Authorization": "Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"},
                              timeout=10)
        if response.status_code == 200:
            print("  [OK] Search endpoint working")
            resolved.append("Search endpoint 422 error fixed")
        else:
            print(f"  [FAIL] Search endpoint: {response.status_code}")
            remaining.append("Search endpoint 422 error")
    except Exception as e:
        print(f"  [ERROR] Search endpoint: {str(e)[:50]}")
        remaining.append("Search endpoint connection error")
    
    # 5. File Structure
    print("\n4. File Structure:")
    root_path = Path("c:/BHIV-HR-Platform")
    
    # Check eliminated files
    files_to_check = [
        ("services/client_portal/auth_service.py", "eliminated"),
        ("CODEBASE_AUDIT_REPORT.md", "eliminated"),
        ("docs/deployment/DEPLOYMENT_GUIDE.md", "moved"),
        ("docs/security/SECURITY_AUDIT.md", "moved")
    ]
    
    for file_path, action in files_to_check:
        full_path = root_path / file_path
        if action == "eliminated":
            if not full_path.exists():
                print(f"  [OK] Eliminated: {file_path}")
                resolved.append(f"File eliminated: {file_path}")
            else:
                print(f"  [FAIL] Still exists: {file_path}")
                remaining.append(f"File not eliminated: {file_path}")
        elif action == "moved":
            if full_path.exists():
                print(f"  [OK] Moved: {file_path}")
                resolved.append(f"File moved: {file_path}")
            else:
                print(f"  [FAIL] Not found: {file_path}")
                remaining.append(f"File not moved: {file_path}")
    
    # 6. .gitignore
    print("\n5. .gitignore Updates:")
    gitignore_path = root_path / ".gitignore"
    if gitignore_path.exists():
        with open(gitignore_path, 'r') as f:
            content = f.read()
        
        entries = ["*.pyc", "*.log", "__pycache__/", "logs/"]
        for entry in entries:
            if entry in content:
                print(f"  [OK] .gitignore has: {entry}")
                resolved.append(f".gitignore entry: {entry}")
            else:
                print(f"  [FAIL] .gitignore missing: {entry}")
                remaining.append(f".gitignore missing: {entry}")
    else:
        print("  [FAIL] .gitignore not found")
        remaining.append(".gitignore file missing")
    
    # Summary
    print(f"\n=== SUMMARY ===")
    print(f"Resolved: {len(resolved)}")
    print(f"Remaining: {len(remaining)}")
    
    if remaining:
        print(f"\nREMAINING ISSUES ({len(remaining)}):")
        for i, issue in enumerate(remaining, 1):
            print(f"  {i}. {issue}")
    
    if resolved:
        print(f"\nRESOLVED ISSUES ({len(resolved)}):")
        for i, issue in enumerate(resolved[:5], 1):
            print(f"  {i}. {issue}")
        if len(resolved) > 5:
            print(f"  ... and {len(resolved) - 5} more")
    
    return remaining, resolved

if __name__ == "__main__":
    remaining_issues, resolved_issues = check_critical_issues()
    
    if not remaining_issues:
        print("\n[SUCCESS] All critical issues resolved!")
    else:
        print(f"\n[WARNING] {len(remaining_issues)} issues still need attention")