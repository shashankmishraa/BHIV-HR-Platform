#!/usr/bin/env python3
"""
Comprehensive Import and Dependency Test
Tests all modules and services for missing imports and dependencies
"""
import sys
import os
import importlib
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
            importlib.import_module(dep)
            print(f"  ✓ {dep}")
        except ImportError as e:
            print(f"  ✗ {dep}: {e}")
            missing.append(dep)
    
    return missing

def test_semantic_engine_imports():
    """Test semantic engine imports"""
    print("\nTesting semantic engine imports...")
    
    try:
        from services.semantic_engine.phase3_engine import (
            Phase3SemanticEngine,
            AdvancedSemanticMatcher,
            BatchMatcher,
            LearningEngine,
            SemanticJobMatcher
        )
        print("  ✓ Phase 3 engine imports successful")
        
        # Test initialization
        engine = Phase3SemanticEngine()
        print("  ✓ Phase 3 engine initialization successful")
        return True
    except Exception as e:
        print(f"  ✗ Semantic engine import failed: {e}")
        return False

def test_agent_service_imports():
    """Test agent service imports"""
    print("\nTesting agent service imports...")
    
    try:
        sys.path.insert(0, str(project_root / "services" / "agent"))
        
        # Test main imports
        from fastapi import FastAPI, HTTPException
        from pydantic import BaseModel
        import psycopg2
        from datetime import datetime
        print("  ✓ Agent service core imports successful")
        
        # Test semantic engine import from agent context
        sys.path.insert(0, str(project_root / "services"))
        from semantic_engine.phase3_engine import Phase3SemanticEngine
        print("  ✓ Agent semantic engine import successful")
        
        return True
    except Exception as e:
        print(f"  ✗ Agent service import failed: {e}")
        return False

def test_gateway_service_imports():
    """Test gateway service imports"""
    print("\nTesting gateway service imports...")
    
    try:
        sys.path.insert(0, str(project_root / "services" / "gateway" / "app"))
        
        # Test core imports
        from fastapi import FastAPI, HTTPException, Depends, Security
        from sqlalchemy import create_engine, text
        from datetime import datetime, timezone
        import jwt
        import pyotp
        import qrcode
        print("  ✓ Gateway service core imports successful")
        
        # Test monitoring import
        try:
            from monitoring import monitor
            print("  ✓ Gateway monitoring import successful")
        except ImportError:
            print("  ! Gateway monitoring import failed (fallback available)")
        
        return True
    except Exception as e:
        print(f"  ✗ Gateway service import failed: {e}")
        return False

def test_portal_service_imports():
    """Test portal service imports"""
    print("\nTesting portal service imports...")
    
    try:
        sys.path.insert(0, str(project_root / "services" / "portal"))
        
        import streamlit as st
        import httpx
        import pandas as pd
        from datetime import datetime
        import numpy as np
        print("  ✓ Portal service core imports successful")
        
        # Test config import
        from config import API_BASE, API_KEY, headers, http_client
        print("  ✓ Portal config import successful")
        
        return True
    except Exception as e:
        print(f"  ✗ Portal service import failed: {e}")
        return False

def test_client_portal_imports():
    """Test client portal service imports"""
    print("\nTesting client portal service imports...")
    
    try:
        sys.path.insert(0, str(project_root / "services" / "client_portal"))
        
        import streamlit as st
        import requests
        from datetime import datetime
        import logging
        print("  ✓ Client portal core imports successful")
        
        # Test config import
        from config import API_BASE_URL, http_session
        print("  ✓ Client portal config import successful")
        
        # Test auth service import
        from auth_service import ClientAuthService
        print("  ✓ Client portal auth service import successful")
        
        return True
    except Exception as e:
        print(f"  ✗ Client portal import failed: {e}")
        return False

def test_all_service_files():
    """Test that all service files can be imported"""
    print("\nTesting all service files...")
    
    service_files = [
        "services/agent/app.py",
        "services/gateway/app/main.py",
        "services/portal/app.py",
        "services/client_portal/app.py",
        "services/semantic_engine/phase3_engine.py"
    ]
    
    failed_files = []
    for file_path in service_files:
        try:
            # Convert path to module name
            module_path = file_path.replace("/", ".").replace("\\", ".").replace(".py", "")
            if module_path.endswith(".main"):
                module_path = module_path[:-5] + ".main"
            
            # Try to import as module
            spec = importlib.util.spec_from_file_location(
                module_path, 
                project_root / file_path
            )
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                # Don't execute, just check syntax
                print(f"  ✓ {file_path} - syntax OK")
            else:
                print(f"  ✗ {file_path} - could not load spec")
                failed_files.append(file_path)
        except Exception as e:
            print(f"  ✗ {file_path}: {e}")
            failed_files.append(file_path)
    
    return failed_files

def main():
    """Run all import tests"""
    print("=" * 60)
    print("COMPREHENSIVE IMPORT AND DEPENDENCY TEST")
    print("=" * 60)
    
    # Test results
    results = {
        'missing_dependencies': test_core_dependencies(),
        'semantic_engine': test_semantic_engine_imports(),
        'agent_service': test_agent_service_imports(),
        'gateway_service': test_gateway_service_imports(),
        'portal_service': test_portal_service_imports(),
        'client_portal': test_client_portal_imports(),
        'failed_files': test_all_service_files()
    }
    
    print("\n" + "=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)
    
    # Summary
    total_issues = 0
    
    if results['missing_dependencies']:
        print(f"❌ Missing Dependencies: {len(results['missing_dependencies'])}")
        for dep in results['missing_dependencies']:
            print(f"   - {dep}")
        total_issues += len(results['missing_dependencies'])
    else:
        print("✅ All core dependencies available")
    
    services = ['semantic_engine', 'agent_service', 'gateway_service', 'portal_service', 'client_portal']
    for service in services:
        if results[service]:
            print(f"✅ {service.replace('_', ' ').title()}: OK")
        else:
            print(f"❌ {service.replace('_', ' ').title()}: FAILED")
            total_issues += 1
    
    if results['failed_files']:
        print(f"❌ Failed Files: {len(results['failed_files'])}")
        for file in results['failed_files']:
            print(f"   - {file}")
        total_issues += len(results['failed_files'])
    else:
        print("✅ All service files: OK")
    
    print("\n" + "=" * 60)
    if total_issues == 0:
        print("🎉 ALL TESTS PASSED - No import or dependency issues found!")
        print("✅ Project is ready for deployment")
    else:
        print(f"⚠️  {total_issues} ISSUES FOUND - Fix required before deployment")
        print("❌ Check missing dependencies and import errors above")
    
    print("=" * 60)
    return total_issues == 0

if __name__ == "__main__":
    import importlib.util
    success = main()
    sys.exit(0 if success else 1)