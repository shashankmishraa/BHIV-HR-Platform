#!/usr/bin/env python3
"""
Security Fixes Testing Script
Tests the enhanced security configuration and error handling
"""

import os
import sys
import importlib.util
import traceback
from typing import Dict, Any, List

class SecurityTestRunner:
    """Test runner for security fixes"""
    
    def __init__(self):
        self.test_results = []
        self.passed = 0
        self.failed = 0
    
    def run_test(self, test_name: str, test_func) -> bool:
        """Run a single test and record results"""
        try:
            print(f"\nTesting: {test_name}")
            result = test_func()
            if result:
                print(f"PASSED: {test_name}")
                self.passed += 1
                self.test_results.append({"test": test_name, "status": "PASSED", "error": None})
                return True
            else:
                print(f"FAILED: {test_name}")
                self.failed += 1
                self.test_results.append({"test": test_name, "status": "FAILED", "error": "Test returned False"})
                return False
        except Exception as e:
            print(f"ERROR: {test_name} - {str(e)}")
            self.failed += 1
            self.test_results.append({"test": test_name, "status": "ERROR", "error": str(e)})
            return False
    
    def test_security_manager_import(self) -> bool:
        """Test if security manager can be imported"""
        try:
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'services', 'shared'))
            from security_manager import SecurityManager, APIKeyManager
            
            # Test initialization with development environment
            os.environ['ENVIRONMENT'] = 'development'
            security_mgr = SecurityManager()
            
            print(f"  - Security Manager initialized for {security_mgr.config.environment.value}")
            print(f"  - API Key length: {len(security_mgr.config.api_key)} characters")
            print(f"  - JWT Secret length: {len(security_mgr.config.jwt_secret)} characters")
            
            return True
        except Exception as e:
            print(f"  - Import error: {e}")
            return False
    
    def test_portal_security_config(self) -> bool:
        """Test portal security configuration"""
        try:
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'services', 'portal'))
            
            # Set development environment
            os.environ['ENVIRONMENT'] = 'development'
            os.environ.pop('API_KEY_SECRET', None)  # Remove to test fallback
            
            from security_config import secure_api
            
            headers = secure_api.get_headers()
            print(f"  - Headers generated: {list(headers.keys())}")
            print(f"  - API key type: {'fallback' if 'temp_' in headers['Authorization'] else 'configured'}")
            
            return 'Authorization' in headers and headers['Authorization'].startswith('Bearer ')
        except Exception as e:
            print(f"  - Portal security error: {e}")
            return False
    
    def test_client_auth_service(self) -> bool:
        """Test client authentication service"""
        try:
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'services', 'client_portal'))
            
            # Set development environment
            os.environ['ENVIRONMENT'] = 'development'
            os.environ.pop('JWT_SECRET', None)  # Remove to test fallback
            
            from auth_service import ClientAuthService
            
            # This should not raise an error in development
            auth_service = ClientAuthService()
            
            print(f"  - JWT Secret length: {len(auth_service.jwt_secret)} characters")
            print(f"  - JWT Algorithm: {auth_service.jwt_algorithm}")
            print(f"  - Token expiry: {auth_service.token_expiry_hours} hours")
            
            return True
        except Exception as e:
            print(f"  - Client auth error: {e}")
            return False
    
    def test_demo_key_handling(self) -> bool:
        """Test demo key detection and handling"""
        try:
            # Test with demo key in development
            os.environ['ENVIRONMENT'] = 'development'
            os.environ['API_KEY_SECRET'] = 'myverysecureapikey123'
            
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'services', 'shared'))
            
            # Reload the module to test with demo key
            import importlib
            if 'security_manager' in sys.modules:
                importlib.reload(sys.modules['security_manager'])
            
            from security_manager import SecurityManager
            
            security_mgr = SecurityManager()
            
            # Should generate a fallback key, not use demo key
            api_key = security_mgr.config.api_key
            print(f"  - Demo key replaced with: {api_key[:20]}...")
            
            return api_key != 'myverysecureapikey123' and 'temp_dev_key_' in api_key
        except Exception as e:
            print(f"  - Demo key handling error: {e}")
            return False
    
    def test_production_validation(self) -> bool:
        """Test production environment validation"""
        try:
            # Test production environment without proper secrets
            os.environ['ENVIRONMENT'] = 'production'
            os.environ.pop('API_KEY_SECRET', None)
            os.environ.pop('JWT_SECRET', None)
            
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'services', 'shared'))
            
            # Reload the module to test production validation
            import importlib
            if 'security_manager' in sys.modules:
                importlib.reload(sys.modules['security_manager'])
            
            try:
                from security_manager import SecurityManager
                SecurityManager()
                print("  - Production validation failed - should have raised error")
                return False
            except ValueError as e:
                print(f"  - Production validation working: {str(e)[:100]}...")
                return "required for production" in str(e)
        except Exception as e:
            print(f"  - Production validation error: {e}")
            return False
    
    def test_fallback_mechanisms(self) -> bool:
        """Test fallback mechanisms work properly"""
        try:
            # Reset environment for clean test
            os.environ['ENVIRONMENT'] = 'development'
            os.environ.pop('API_KEY_SECRET', None)
            os.environ.pop('JWT_SECRET', None)
            
            # Test portal fallback
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'services', 'portal'))
            
            # Reload modules for clean test
            import importlib
            modules_to_reload = ['security_config']
            for module in modules_to_reload:
                if module in sys.modules:
                    importlib.reload(sys.modules[module])
            
            from security_config import secure_api
            headers = secure_api.get_headers()
            
            print(f"  - Fallback headers generated successfully")
            print(f"  - Authorization header present: {'Authorization' in headers}")
            
            return 'Authorization' in headers
        except Exception as e:
            print(f"  - Fallback mechanism error: {e}")
            return False
    
    def test_environment_detection(self) -> bool:
        """Test environment detection works correctly"""
        try:
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'services', 'shared'))
            
            # Test different environments
            environments = ['development', 'staging', 'production']
            results = []
            
            for env in environments:
                os.environ['ENVIRONMENT'] = env
                os.environ['API_KEY_SECRET'] = 'test_key_for_' + env
                os.environ['JWT_SECRET'] = 'test_jwt_for_' + env
                
                # Reload module for each environment test
                import importlib
                if 'security_manager' in sys.modules:
                    importlib.reload(sys.modules['security_manager'])
                
                from security_manager import SecurityManager
                security_mgr = SecurityManager()
                
                detected_env = security_mgr.config.environment.value
                results.append(detected_env == env)
                print(f"  - Environment {env}: {'✓' if detected_env == env else '✗'}")
            
            return all(results)
        except Exception as e:
            print(f"  - Environment detection error: {e}")
            return False
    
    def run_all_tests(self):
        """Run all security tests"""
        print("BHIV HR Platform - Security Fixes Testing")
        print("=" * 50)
        
        # Define tests
        tests = [
            ("Security Manager Import", self.test_security_manager_import),
            ("Portal Security Config", self.test_portal_security_config),
            ("Client Auth Service", self.test_client_auth_service),
            ("Demo Key Handling", self.test_demo_key_handling),
            ("Production Validation", self.test_production_validation),
            ("Fallback Mechanisms", self.test_fallback_mechanisms),
            ("Environment Detection", self.test_environment_detection),
        ]
        
        # Run tests
        for test_name, test_func in tests:
            self.run_test(test_name, test_func)
        
        # Print summary
        print("\n" + "=" * 50)
        print(f"TEST SUMMARY")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Success Rate: {(self.passed / (self.passed + self.failed) * 100):.1f}%")
        
        if self.failed == 0:
            print("\nALL SECURITY TESTS PASSED!")
            print("Security fixes are working correctly")
            print("Fallback mechanisms are functional")
            print("Environment detection is working")
            print("Production validation is active")
        else:
            print(f"\n{self.failed} tests failed. Review the errors above.")
        
        return self.failed == 0

def main():
    """Main test execution"""
    # Clean up environment for testing
    test_env_vars = ['API_KEY_SECRET', 'JWT_SECRET', 'ENVIRONMENT']
    original_values = {}
    
    for var in test_env_vars:
        original_values[var] = os.environ.get(var)
    
    try:
        runner = SecurityTestRunner()
        success = runner.run_all_tests()
        
        if success:
            print("\nSecurity fixes are ready for deployment!")
            return 0
        else:
            print("\nSome security tests failed. Please review and fix.")
            return 1
    
    finally:
        # Restore original environment
        for var, value in original_values.items():
            if value is not None:
                os.environ[var] = value
            else:
                os.environ.pop(var, None)

if __name__ == "__main__":
    exit(main())