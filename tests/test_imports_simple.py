#!/usr/bin/env python3
"""
Simple Import and Dependency Test
Tests all modules and services for missing imports and dependencies
"""
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "services"))

def test_core_dependencies():
    """Test core Python dependencies"""
    print("Testing core dependencies...")
    
    dependencies = [
        'fastapi', 'uvicorn', 'pydantic', 'psycopg2', 'sqlalchemy',
        'sentence_transformers', 'sklearn', 'numpy', 'torch',
        'streamlit', 'requests', 'httpx', 'pandas', 'bcrypt',
        'jwt', 'pyotp', 'qrcode', 'prometheus_client', 'psutil'
    ]
    
    missing = []
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"  [PASS] {dep}")
        except ImportError as e:
            print(f"  [FAIL] {dep}: {e}")
            missing.append(dep)
    
    return missing

def test_semantic_engine():
    """Test semantic engine imports"""
    print("\nTesting semantic engine...")
    
    try:
        from services.semantic_engine.phase3_engine import Phase3SemanticEngine
        print("  [PASS] Phase 3 engine import")
        
        engine = Phase3SemanticEngine()
        print("  [PASS] Phase 3 engine initialization")
        return True
    except Exception as e:
        print(f"  [FAIL] Semantic engine: {e}")
        return False

def test_agent_service():
    """Test agent service"""
    print("\nTesting agent service...")
    
    try:
        # Test basic imports
        import fastapi
        import psycopg2
        print("  [PASS] Agent core imports")
        
        # Test semantic engine import
        from services.semantic_engine.phase3_engine import Phase3SemanticEngine
        print("  [PASS] Agent semantic import")
        return True
    except Exception as e:
        print(f"  [FAIL] Agent service: {e}")
        return False

def test_gateway_service():
    """Test gateway service"""
    print("\nTesting gateway service...")
    
    try:
        import fastapi
        import sqlalchemy
        import jwt
        import pyotp
        print("  [PASS] Gateway core imports")
        return True
    except Exception as e:
        print(f"  [FAIL] Gateway service: {e}")
        return False

def test_portal_services():
    """Test portal services"""
    print("\nTesting portal services...")
    
    try:
        import streamlit
        import httpx
        import pandas
        import requests
        print("  [PASS] Portal core imports")
        
        import bcrypt
        print("  [PASS] Auth dependencies")
        return True
    except Exception as e:
        print(f"  [FAIL] Portal services: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("IMPORT AND DEPENDENCY TEST")
    print("=" * 50)
    
    # Run tests
    missing_deps = test_core_dependencies()
    semantic_ok = test_semantic_engine()
    agent_ok = test_agent_service()
    gateway_ok = test_gateway_service()
    portal_ok = test_portal_services()
    
    # Summary
    print("\n" + "=" * 50)
    print("RESULTS SUMMARY")
    print("=" * 50)
    
    total_issues = 0
    
    if missing_deps:
        print(f"[FAIL] Missing Dependencies: {len(missing_deps)}")
        for dep in missing_deps:
            print(f"   - {dep}")
        total_issues += len(missing_deps)
    else:
        print("[PASS] All dependencies available")
    
    services = [
        ("Semantic Engine", semantic_ok),
        ("Agent Service", agent_ok),
        ("Gateway Service", gateway_ok),
        ("Portal Services", portal_ok)
    ]
    
    for name, status in services:
        if status:
            print(f"[PASS] {name}")
        else:
            print(f"[FAIL] {name}")
            total_issues += 1
    
    print("\n" + "=" * 50)
    if total_issues == 0:
        print("SUCCESS: All imports and dependencies working!")
        print("Project is ready for deployment")
    else:
        print(f"FAILURE: {total_issues} issues found")
        print("Fix missing dependencies before deployment")
    
    print("=" * 50)
    return total_issues == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)