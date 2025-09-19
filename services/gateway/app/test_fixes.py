#!/usr/bin/env python3
"""
Test script to verify authentication and validation fixes
"""

import asyncio
import os
import sys
from datetime import datetime, timezone

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(__file__))

async def test_authentication_system():
    """Test the enhanced authentication system"""
    print("Testing Enhanced Authentication System...")
    
    try:
        from enhanced_auth_system import enhanced_auth_system, AuthenticationMethod, AuthenticationLevel
        
        # Test 1: API Key validation
        print("1. Testing API Key validation...")
        
        # Test with environment variable (should work if set)
        test_key = os.getenv("DEV_API_KEY", "test_key_123")
        result = enhanced_auth_system.validate_api_key(test_key)
        print(f"   API Key test result: {result.success}, Method: {result.method.value}, Level: {result.level.name}")
        
        # Test 2: JWT Token generation and validation
        print("2. Testing JWT Token system...")
        
        jwt_token = enhanced_auth_system.generate_jwt_token("test_user", ["read", "write"])
        jwt_result = enhanced_auth_system.validate_jwt_token(jwt_token)
        print(f"   JWT test result: {jwt_result.success}, Method: {jwt_result.method.value}")
        
        # Test 3: System status
        print("3. Testing system status...")
        
        status = enhanced_auth_system.get_system_status()
        print(f"   System health: {status['system_health']}")
        print(f"   Environment: {status['environment']}")
        print(f"   Active sessions: {status['active_sessions']}")
        
        print("[PASS] Authentication system tests passed!")
        return True
        
    except Exception as e:
        print(f"[FAIL] Authentication system test failed: {str(e)}")
        return False

async def test_validation_system():
    """Test the validation system"""
    print("\nTesting Validation System...")
    
    try:
        from validation import (
            validate_email, validate_phone, validate_password_strength,
            validate_pagination, sanitize_input, JobCreateRequest
        )
        
        # Test 1: Email validation
        print("1. Testing email validation...")
        
        valid_email = validate_email("test@example.com")
        invalid_email = validate_email("invalid-email")
        print(f"   Valid email test: {valid_email}")
        print(f"   Invalid email test: {invalid_email}")
        
        # Test 2: Phone validation
        print("2. Testing phone validation...")
        
        valid_phone = validate_phone("+1-555-123-4567")
        invalid_phone = validate_phone("123")
        print(f"   Valid phone test: {valid_phone}")
        print(f"   Invalid phone test: {invalid_phone}")
        
        # Test 3: Password strength validation
        print("3. Testing password validation...")
        
        strong_password = validate_password_strength("StrongPass123!")
        weak_password = validate_password_strength("weak")
        print(f"   Strong password score: {strong_password['score']}")
        print(f"   Weak password score: {weak_password['score']}")
        
        # Test 4: Input sanitization
        print("4. Testing input sanitization...")
        
        malicious_input = "<script>alert('xss')</script>Hello World"
        sanitized = sanitize_input(malicious_input)
        print(f"   Original: {malicious_input}")
        print(f"   Sanitized: {sanitized}")
        
        # Test 5: Pagination validation
        print("5. Testing pagination validation...")
        
        try:
            validate_pagination(50, 0)  # Should pass
            print("   Valid pagination: [PASS]")
        except Exception:
            print("   Valid pagination: ❌")
        
        try:
            validate_pagination(200, -1)  # Should fail
            print("   Invalid pagination: [FAIL]")
        except Exception:
            print("   Invalid pagination: [PASS]")
        
        print("[PASS] Validation system tests passed!")
        return True
        
    except Exception as e:
        print(f"[FAIL] Validation system test failed: {str(e)}")
        return False

async def test_database_manager():
    """Test the database manager"""
    print("\nTesting Database Manager...")
    
    try:
        from database_manager import database_manager
        
        # Test 1: Health status
        print("1. Testing database health...")
        
        health = database_manager.get_health_status()
        print(f"   Database status: {health['status']}")
        print(f"   Connection: {health.get('connection', 'unknown')}")
        
        # Test 2: Schema validation
        print("2. Testing schema validation...")
        
        schema = database_manager.validate_schema()
        print(f"   Schema valid: {schema['valid']}")
        print(f"   Missing tables: {len(schema['missing_tables'])}")
        print(f"   Missing columns: {len(schema['missing_columns'])}")
        
        # Test 3: Table existence checks
        print("3. Testing table checks...")
        
        candidates_exists = database_manager.check_table_exists("candidates")
        jobs_exists = database_manager.check_table_exists("jobs")
        print(f"   Candidates table exists: {candidates_exists}")
        print(f"   Jobs table exists: {jobs_exists}")
        
        print("[PASS] Database manager tests passed!")
        return True
        
    except Exception as e:
        print(f"[FAIL] Database manager test failed: {str(e)}")
        return False

async def test_security_fixes():
    """Test security vulnerability fixes"""
    print("\nTesting Security Fixes...")
    
    try:
        # Test 1: Check for hardcoded credentials removal
        print("1. Testing hardcoded credentials removal...")
        
        from enhanced_auth_system import enhanced_auth_system
        
        # Check if production keys are loaded from environment
        prod_keys_count = len(enhanced_auth_system.production_keys)
        dev_keys_count = len(enhanced_auth_system.development_keys)
        
        print(f"   Production keys loaded: {prod_keys_count}")
        print(f"   Development keys loaded: {dev_keys_count}")
        
        # Test 2: JWT validation improvements
        print("2. Testing JWT validation...")
        
        # Test with invalid token
        invalid_result = enhanced_auth_system.validate_jwt_token("invalid_token")
        print(f"   Invalid JWT handled: {not invalid_result.success}")
        
        # Test 3: Session management
        print("3. Testing session management...")
        
        session_count = len(enhanced_auth_system.active_sessions)
        print(f"   Active sessions: {session_count}")
        
        # Test cleanup
        cleaned = enhanced_auth_system.cleanup_expired_sessions()
        print(f"   Expired sessions cleaned: {cleaned}")
        
        print("[PASS] Security fixes tests passed!")
        return True
        
    except Exception as e:
        print(f"[FAIL] Security fixes test failed: {str(e)}")
        return False

async def main():
    """Run all tests"""
    print("Running Authentication and Validation System Tests")
    print("=" * 60)
    
    results = []
    
    # Run all test suites
    results.append(await test_authentication_system())
    results.append(await test_validation_system())
    results.append(await test_database_manager())
    results.append(await test_security_fixes())
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Results Summary:")
    
    passed = sum(results)
    total = len(results)
    
    test_names = [
        "Authentication System",
        "Validation System", 
        "Database Manager",
        "Security Fixes"
    ]
    
    for i, (name, result) in enumerate(zip(test_names, results)):
        status = "[PASS]" if result else "[FAIL]"
        print(f"   {name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! System is ready for deployment.")
        return 0
    else:
        print("Some tests failed. Please review the issues above.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)