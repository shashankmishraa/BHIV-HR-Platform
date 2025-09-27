#!/usr/bin/env python3
"""Simple deployment test for BHIV HR Gateway"""

import sys
import os

def test_imports():
    """Test all critical imports"""
    print("Testing imports...")
    
    # Test observability imports
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'shared'))
        from observability_simple import setup_simple_observability, MetricsCollector
        print("OK: observability_simple imported successfully")
    except ImportError as e:
        print(f"ERROR: observability_simple import failed: {e}")
    
    # Test metrics import
    try:
        from app.metrics import get_metrics_response, metrics_collector, metrics_middleware
        print("OK: app.metrics imported successfully")
    except ImportError as e:
        print(f"ERROR: app.metrics import failed: {e}")
    
    # Test config import
    try:
        from app.shared.config import get_settings, is_production
        print("OK: app.shared.config imported successfully")
    except ImportError as e:
        print(f"ERROR: app.shared.config import failed: {e}")
    
    # Test database import
    try:
        from app.shared.database import db_manager
        print("OK: app.shared.database imported successfully")
    except ImportError as e:
        print(f"ERROR: app.shared.database import failed: {e}")

def test_main_app():
    """Test main app initialization"""
    print("\nTesting main app...")
    try:
        from app.main import app
        print("OK: Main app imported successfully")
        
        # Test if health endpoint exists
        routes = [route.path for route in app.routes]
        if "/health" in routes:
            print("OK: /health endpoint registered")
        else:
            print("ERROR: /health endpoint not found")
            
        if "/" in routes:
            print("OK: Root endpoint registered")
        else:
            print("ERROR: Root endpoint not found")
            
        print(f"OK: Total routes registered: {len(routes)}")
        
    except Exception as e:
        print(f"ERROR: Main app import failed: {e}")

if __name__ == "__main__":
    print("BHIV HR Gateway Deployment Test")
    print("=" * 40)
    
    test_imports()
    test_main_app()
    
    print("\n" + "=" * 40)
    print("Test complete.")