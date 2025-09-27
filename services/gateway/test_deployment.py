#!/usr/bin/env python3
"""Test deployment fixes for BHIV HR Gateway"""

import sys
import os
import importlib.util

def test_imports():
    """Test all critical imports"""
    print("Testing imports...")
    
    # Test observability imports
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'shared'))
        from observability_simple import setup_simple_observability, MetricsCollector
        print("✅ observability_simple imported successfully")
    except ImportError as e:
        print(f"❌ observability_simple import failed: {e}")
    
    # Test metrics import
    try:
        from app.metrics import get_metrics_response, metrics_collector, metrics_middleware
        print("✅ app.metrics imported successfully")
    except ImportError as e:
        print(f"❌ app.metrics import failed: {e}")
    
    # Test config import
    try:
        from app.shared.config import get_settings, is_production
        print("✅ app.shared.config imported successfully")
    except ImportError as e:
        print(f"❌ app.shared.config import failed: {e}")
    
    # Test database import
    try:
        from app.shared.database import db_manager
        print("✅ app.shared.database imported successfully")
    except ImportError as e:
        print(f"❌ app.shared.database import failed: {e}")
    
    # Test module routers
    modules = ['core', 'auth', 'candidates', 'jobs', 'monitoring', 'workflows']
    for module in modules:
        try:
            spec = importlib.util.spec_from_file_location(
                f"app.modules.{module}.router",
                f"app/modules/{module}/router.py"
            )
            if spec and spec.loader:
                router_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(router_module)
                print(f"✅ {module} router imported successfully")
            else:
                print(f"❌ {module} router spec not found")
        except Exception as e:
            print(f"❌ {module} router import failed: {e}")

def test_main_app():
    """Test main app initialization"""
    print("\nTesting main app...")
    try:
        from app.main import app
        print("✅ Main app imported successfully")
        
        # Test if health endpoint exists
        routes = [route.path for route in app.routes]
        if "/health" in routes:
            print("✅ /health endpoint registered")
        else:
            print("❌ /health endpoint not found")
            
        if "/" in routes:
            print("✅ Root endpoint registered")
        else:
            print("❌ Root endpoint not found")
            
        print(f"✅ Total routes registered: {len(routes)}")
        
    except Exception as e:
        print(f"❌ Main app import failed: {e}")

if __name__ == "__main__":
    print("BHIV HR Gateway Deployment Test")
    print("=" * 40)
    
    test_imports()
    test_main_app()
    
    print("\n" + "=" * 40)
    print("Test complete. Check for any ❌ errors above.")