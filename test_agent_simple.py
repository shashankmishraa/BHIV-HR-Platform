#!/usr/bin/env python3
"""
Simple Agent Test - Test agent without semantic engine
"""

import sys
import os

# Add the agent directory to Python path
agent_path = os.path.join(os.path.dirname(__file__), 'services', 'agent')
sys.path.insert(0, agent_path)

def test_agent_imports():
    """Test if agent can import without semantic engine"""
    print("Testing agent imports...")
    
    try:
        # Test basic imports
        from datetime import datetime, timezone
        from typing import List, Dict, Any
        import asyncio
        import json
        import logging
        import os
        import re
        import sys
        print("✅ Basic imports successful")
        
        # Test FastAPI imports
        from fastapi import FastAPI, HTTPException, Request, Response
        from fastapi.middleware.cors import CORSMiddleware
        from fastapi.responses import PlainTextResponse, FileResponse
        from pydantic import BaseModel
        print("✅ FastAPI imports successful")
        
        # Test database imports
        import psycopg2
        print("✅ Database imports successful")
        
        # Test psutil import
        import psutil
        print("✅ psutil import successful")
        
        # Test semantic engine imports (should fallback gracefully)
        try:
            from semantic_engine import SemanticJobMatcher, AdvancedSemanticMatcher, BatchMatcher, SemanticProcessor
            print("✅ Semantic engine imports successful")
            semantic_available = True
        except ImportError as e:
            print(f"⚠️ Semantic engine not available (expected): {e}")
            semantic_available = False
        
        return True, semantic_available
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False, False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False, False

def test_database_connection():
    """Test database connection"""
    print("\nTesting database connection...")
    
    try:
        import psycopg2
        
        # Try local database connection
        conn = psycopg2.connect(
            host="localhost",
            database="bhiv_hr_nqzb",
            user="bhiv_user",
            password="B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J",
            port="5432"
        )
        
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            
        conn.close()
        print("✅ Database connection successful")
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def main():
    print("BHIV Agent - Simple Test")
    print("=" * 40)
    
    # Test imports
    imports_ok, semantic_ok = test_agent_imports()
    
    # Test database
    db_ok = test_database_connection()
    
    # Summary
    print("\n" + "=" * 40)
    print("TEST SUMMARY")
    print("=" * 40)
    
    print(f"Imports: {'✅ OK' if imports_ok else '❌ FAILED'}")
    print(f"Semantic Engine: {'✅ Available' if semantic_ok else '⚠️ Fallback mode'}")
    print(f"Database: {'✅ Connected' if db_ok else '❌ Connection failed'}")
    
    if imports_ok and db_ok:
        print("\n🎉 Agent should be able to start!")
        print("💡 Run: docker-compose restart agent")
    else:
        print("\n🚨 Agent has issues that need fixing")
        if not imports_ok:
            print("   - Fix missing Python dependencies")
        if not db_ok:
            print("   - Check database container status")

if __name__ == "__main__":
    main()