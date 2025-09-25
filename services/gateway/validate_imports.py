#!/usr/bin/env python3
"""Import validation script for BHIV HR Platform Gateway"""

import sys
import os

# Set test environment variables
os.environ['DATABASE_URL'] = 'postgresql://test:test@localhost:5432/test'
os.environ['API_KEY_SECRET'] = 'test_api_key_secret'
os.environ['JWT_SECRET'] = 'test_jwt_secret'
os.environ['ENVIRONMENT'] = 'test'

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def test_imports():
    """Test all critical imports"""
    print("Testing imports...")
    
    try:
        # Test shared modules
        print("[OK] Testing shared modules...")
        from app.shared.models import JobCreate, CandidateCreate, WorkflowStatus
        from app.shared.validation import ValidationUtils
        from app.shared.security import security_manager
        from app.shared.config import get_settings
        from app.shared.database import db_manager
        print("[OK] Shared modules imported successfully")
        
        # Test workflow engine
        print("[OK] Testing workflow engine...")
        from app.workflow_engine import workflow_engine, create_job_posting_workflow
        print("[OK] Workflow engine imported successfully")
        
        # Test metrics
        print("[OK] Testing metrics...")
        from app.metrics import metrics_collector, metrics_middleware
        print("[OK] Metrics imported successfully")
        
        # Test module routers
        print("[OK] Testing module routers...")
        from app.modules.core import router as core_router
        from app.modules.candidates import router as candidates_router
        from app.modules.jobs import router as jobs_router
        from app.modules.auth import router as auth_router
        from app.modules.workflows import router as workflows_router
        from app.modules.monitoring import router as monitoring_router
        print("[OK] All module routers imported successfully")
        
        # Test main application
        print("[OK] Testing main application...")
        from app.main import app
        print("[OK] Main application imported successfully")
        
        print("\n[SUCCESS] ALL IMPORTS SUCCESSFUL!")
        print("[SUCCESS] Import structure is correctly configured")
        return True
        
    except ImportError as e:
        print(f"[ERROR] Import error: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)