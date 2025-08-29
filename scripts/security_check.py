#!/usr/bin/env python3
"""
Security validation script for BHIV HR Platform
Checks for common security issues and misconfigurations
"""
import os
import re
import sys
from pathlib import Path

def check_environment_variables():
    """Check for required environment variables"""
    required_vars = [
        'DATABASE_URL',
        'API_KEY_SECRET',
        'POSTGRES_USER',
        'POSTGRES_PASSWORD'
    ]
    
    missing = []
    weak = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing.append(var)
        elif len(value) < 16:
            weak.append(var)
    
    if missing:
        print(f"❌ Missing environment variables: {', '.join(missing)}")
        return False
    
    if weak:
        print(f"⚠️ Weak credentials (< 16 chars): {', '.join(weak)}")
    
    print("✅ Environment variables configured")
    return True

def check_hardcoded_secrets():
    """Check for hardcoded secrets in code"""
    patterns = [
        r'password\s*=\s*["\'][^"\']{1,}["\']',
        r'api_key\s*=\s*["\'][^"\']{1,}["\']',
        r'secret\s*=\s*["\'][^"\']{1,}["\']',
        r'myverysecureapikey123',
        r'bhiv_pass'
    ]
    
    issues = []
    project_root = Path(__file__).parent.parent
    
    for file_path in project_root.rglob('*.py'):
        if 'security_check.py' in str(file_path):
            continue
            
        try:
            content = file_path.read_text()
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    issues.append(str(file_path))
                    break
        except:
            continue
    
    if issues:
        print(f"❌ Hardcoded secrets found in: {', '.join(issues)}")
        return False
    
    print("✅ No hardcoded secrets detected")
    return True

def check_docker_security():
    """Check Docker configuration security"""
    compose_files = ['docker-compose.yml', 'docker-compose.prod.yml']
    project_root = Path(__file__).parent.parent
    
    for compose_file in compose_files:
        file_path = project_root / compose_file
        if not file_path.exists():
            continue
            
        content = file_path.read_text()
        
        # Check for resource limits in production
        if 'prod' in compose_file:
            if 'limits:' not in content:
                print(f"⚠️ {compose_file}: Missing resource limits")
            else:
                print(f"✅ {compose_file}: Resource limits configured")
        
        # Check for hardcoded credentials
        if 'bhiv_pass' in content or 'myverysecureapikey123' in content:
            print(f"❌ {compose_file}: Contains hardcoded credentials")
            return False
    
    return True

def main():
    """Run security checks"""
    print("🔒 BHIV HR Platform Security Check")
    print("=" * 40)
    
    checks = [
        check_environment_variables,
        check_hardcoded_secrets,
        check_docker_security
    ]
    
    passed = 0
    for check in checks:
        if check():
            passed += 1
        print()
    
    print(f"Security Score: {passed}/{len(checks)}")
    
    if passed == len(checks):
        print("🎉 All security checks passed!")
        return 0
    else:
        print("⚠️ Security issues found. Please fix before production deployment.")
        return 1

if __name__ == "__main__":
    sys.exit(main())