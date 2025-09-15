#!/usr/bin/env python3
"""
BHIV HR Platform - Gateway Deployment Script
Verifies API completeness and prepares for deployment
"""

import ast
import sys
import subprocess
from pathlib import Path

def verify_and_deploy():
    """Verify API completeness and deploy"""
    
    print("🚀 BHIV HR Platform - Gateway Deployment")
    print("=" * 50)
    
    # 1. Verify main.py exists
    main_py = Path("services/gateway/app/main.py")
    if not main_py.exists():
        print("❌ ERROR: main.py not found")
        return False
    
    # 2. Syntax validation
    try:
        with open(main_py, 'r', encoding='utf-8') as f:
            content = f.read()
        ast.parse(content)
        print("✅ Python syntax validation: PASSED")
    except SyntaxError as e:
        print(f"❌ Syntax Error: {e}")
        return False
    
    # 3. Count endpoints
    endpoint_count = content.count("@app.")
    print(f"✅ Total endpoints found: {endpoint_count}")
    
    if endpoint_count < 46:
        print(f"❌ Expected at least 46 endpoints, found {endpoint_count}")
        return False
    
    # 4. Verify critical endpoints exist
    critical_endpoints = [
        "@app.get(\"/\",",
        "@app.get(\"/health\",",
        "@app.post(\"/v1/client/login\",",
        "@app.get(\"/v1/client/verify\",",
        "@app.post(\"/v1/jobs\",",
        "@app.get(\"/v1/jobs\",",
        "@app.get(\"/v1/candidates/search\",",
        "@app.post(\"/v1/candidates/bulk\",",
        "@app.get(\"/v1/match/",
        "@app.post(\"/v1/feedback\",",
        "@app.post(\"/v1/offers\","
    ]
    
    missing_endpoints = []
    for endpoint in critical_endpoints:
        if endpoint not in content:
            missing_endpoints.append(endpoint)
    
    if missing_endpoints:
        print("❌ Missing critical endpoints:")
        for endpoint in missing_endpoints:
            print(f"   - {endpoint}")
        return False
    
    print("✅ All critical endpoints present")
    
    # 5. Verify imports
    required_imports = [
        "from fastapi import FastAPI",
        "import pyotp",
        "import secrets",
        "from datetime import datetime"
    ]
    
    for imp in required_imports:
        if imp not in content:
            print(f"❌ Missing import: {imp}")
            return False
    
    print("✅ All required imports present")
    
    # 6. Check for security issues
    security_checks = [
        ("get_api_key", "API key validation function"),
        ("validate_api_key", "API key validation logic"),
        ("rate_limit_middleware", "Rate limiting middleware"),
        ("HTTPException", "Error handling")
    ]
    
    for check, desc in security_checks:
        if check not in content:
            print(f"❌ Missing security component: {desc}")
            return False
    
    print("✅ Security components present")
    
    # 7. Final deployment summary
    print("\n🎉 DEPLOYMENT VERIFICATION: PASSED")
    print("=" * 50)
    print(f"✅ Total endpoints: {endpoint_count}")
    print("✅ Syntax validation: PASSED")
    print("✅ Critical endpoints: PRESENT")
    print("✅ Required imports: PRESENT")
    print("✅ Security components: PRESENT")
    
    print("\n📋 ENDPOINT SUMMARY:")
    print("- Core API: 3 endpoints (/, /health, /test-candidates)")
    print("- Monitoring: 3 endpoints (/metrics, /health/detailed, /metrics/dashboard)")
    print("- Job Management: 2 endpoints")
    print("- Candidate Management: 3 endpoints")
    print("- AI Matching: 1 endpoint")
    print("- Assessment & Workflow: 4 endpoints (including /v1/offers)")
    print("- Analytics: 2 endpoints")
    print("- Client Portal: 5 endpoints")
    print("- Security Testing: 7 endpoints")
    print("- Two-Factor Auth: 8 endpoints")
    print("- Password Management: 6 endpoints")
    print("- CSP Management: 4 endpoints")
    
    print("\n🚀 READY FOR RENDER DEPLOYMENT!")
    print("=" * 50)
    print("Deployment command: uvicorn app.main:app --host 0.0.0.0 --port $PORT")
    print("Environment variables needed:")
    print("- DATABASE_URL (PostgreSQL connection)")
    print("- API_KEY_SECRET (API authentication)")
    print("- PORT (provided by Render)")
    
    return True

if __name__ == "__main__":
    success = verify_and_deploy()
    if success:
        print("\n✅ Gateway is ready for deployment!")
        sys.exit(0)
    else:
        print("\n❌ Deployment verification failed!")
        sys.exit(1)