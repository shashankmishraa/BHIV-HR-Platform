#!/usr/bin/env python3
"""
Security validation script to detect CWE-798 and other vulnerabilities
"""
import os
import re
import sys
from pathlib import Path

def check_hardcoded_credentials():
    """Check for hardcoded credentials in codebase"""
    issues = []
    
    # Patterns to detect hardcoded credentials
    patterns = [
        r'myverysecureapikey123',
        r'demo123',
        r'password\s*=\s*["\'][^"\']+["\']',
        r'api_key\s*=\s*["\'][^"\']+["\']',
        r'secret\s*=\s*["\'][^"\']+["\']'
    ]
    
    # Scan source files
    for file_path in Path('.').rglob('*.py'):
        if 'security_check.py' in str(file_path):
            continue
            
        try:
            content = file_path.read_text(encoding='utf-8')
            for pattern in patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    issues.append(f"CWE-798: Hardcoded credential in {file_path}: {matches}")
        except Exception:
            continue
    
    return issues

def main():
    """Run security checks"""
    print("Running security validation...")
    
    issues = check_hardcoded_credentials()
    
    if issues:
        print("Security issues found:")
        for issue in issues:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print("No hardcoded credentials detected")
        print("Security validation passed")

if __name__ == "__main__":
    main()