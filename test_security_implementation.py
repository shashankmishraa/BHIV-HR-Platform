#!/usr/bin/env python3
"""
Test security implementation
"""
import os
import sys

def test_security_modules():
    """Test if security modules can be imported"""
    try:
        sys.path.append('services/portal')
        from security_config import secure_api
        from input_sanitizer import sanitizer
        from sql_protection import sql_guard
        from rate_limiter import form_limiter
        print("All security modules imported successfully")
        return True
    except ImportError as e:
        print(f"Security module import failed: {e}")
        return False

def test_input_sanitization():
    """Test input sanitization"""
    try:
        sys.path.append('services/portal')
        from input_sanitizer import sanitizer
        
        # Test XSS prevention
        malicious_input = "<script>alert('xss')</script>Hello"
        sanitized = sanitizer.sanitize_string(malicious_input)
        
        if "<script>" not in sanitized:
            print("XSS protection working")
            return True
        else:
            print("XSS protection failed")
            return False
    except Exception as e:
        print(f"Sanitization test failed: {e}")
        return False

def test_sql_protection():
    """Test SQL injection protection"""
    try:
        sys.path.append('services/portal')
        from sql_protection import sql_guard
        
        # Test SQL injection detection
        malicious_query = "'; DROP TABLE users; --"
        is_malicious = sql_guard.is_sql_injection_attempt(malicious_query)
        
        if is_malicious:
            print("SQL injection detection working")
            return True
        else:
            print("SQL injection detection failed")
            return False
    except Exception as e:
        print(f"SQL protection test failed: {e}")
        return False

def main():
    """Run security tests"""
    print("Testing security implementation...")
    
    # Setup test environment
    import secrets
    os.environ["API_KEY_SECRET"] = secrets.token_urlsafe(32)
    os.environ["DEMO_PASSWORD"] = "secure_demo_password"
    os.environ["TOTP_SECRET"] = secrets.token_urlsafe(16)
    
    tests = [
        test_security_modules,
        test_input_sanitization,
        test_sql_protection
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print(f"\nSecurity tests: {passed}/{len(tests)} passed")
    
    if passed == len(tests):
        print("Security implementation working correctly")
    else:
        print("Some security features may not be working")

if __name__ == "__main__":
    main()