#!/usr/bin/env python3
"""
Simple Environment Variable Validation Script
Ensures all services use consistent production API keys
"""

import os
import sys

def validate_environment_variables():
    """Validate environment variables for production deployment"""
    errors = []
    warnings = []
    
    # Required environment variables for production
    required_vars = {
        "API_KEY_SECRET": "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o",
        "JWT_SECRET": "prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA",
        "ENVIRONMENT": "production"
    }
    
    # Demo keys that should be rejected in production
    demo_keys = [
        "myverysecureapikey123",
        "demo",
        "test",
        "sample",
        "dev_fallback",
        "temp_dev_key"
    ]
    
    print("BHIV HR Platform - Environment Variable Validation")
    print("=" * 60)
    
    # Check required variables
    for var_name, expected_value in required_vars.items():
        current_value = os.getenv(var_name)
        
        if not current_value:
            errors.append(f"ERROR: {var_name} is not set")
            continue
        
        # Special validation for API_KEY_SECRET
        if var_name == "API_KEY_SECRET":
            if any(demo_key in current_value.lower() for demo_key in demo_keys):
                errors.append(f"ERROR: {var_name} contains demo/test value")
                continue
            
            if len(current_value) < 16:
                errors.append(f"ERROR: {var_name} is too short (minimum 16 characters)")
                continue
            
            if current_value == expected_value:
                print(f"OK: {var_name} - Production key configured correctly")
            else:
                warnings.append(f"WARNING: {var_name} - Using custom production key")
        
        # Special validation for JWT_SECRET
        elif var_name == "JWT_SECRET":
            if len(current_value) < 32:
                errors.append(f"ERROR: {var_name} is too short (minimum 32 characters)")
                continue
            
            if current_value == expected_value:
                print(f"OK: {var_name} - Production secret configured correctly")
            else:
                warnings.append(f"WARNING: {var_name} - Using custom production secret")
        
        # Environment validation
        elif var_name == "ENVIRONMENT":
            if current_value.lower() != "production":
                errors.append(f"ERROR: {var_name} must be 'production', got: {current_value}")
            else:
                print(f"OK: {var_name} - {current_value}")
    
    print()
    
    # Display warnings
    if warnings:
        print("WARNINGS:")
        for warning in warnings:
            print(f"  {warning}")
        print()
    
    # Display errors
    if errors:
        print("ERRORS:")
        for error in errors:
            print(f"  {error}")
        print()
        print("To fix these issues:")
        print("  1. Set API_KEY_SECRET=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o")
        print("  2. Set JWT_SECRET=prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA")
        print("  3. Set ENVIRONMENT=production")
        return False, errors
    
    print("SUCCESS: All environment variables are correctly configured!")
    return True, []

def check_service_compatibility():
    """Check if all services will use the same API key"""
    api_key = os.getenv("API_KEY_SECRET")
    jwt_secret = os.getenv("JWT_SECRET")
    environment = os.getenv("ENVIRONMENT", "development")
    
    print("Service Compatibility Check:")
    print("=" * 40)
    
    if api_key and jwt_secret:
        print(f"OK: All services will use API key: {api_key[:8]}...")
        print(f"OK: All services will use JWT secret: {jwt_secret[:8]}...")
        print(f"OK: Environment: {environment}")
        return True
    else:
        print("ERROR: Services will use different keys (fallback mode)")
        return False

def main():
    """Main validation function"""
    print("BHIV HR Platform - Environment Variable Validation")
    print("=" * 60)
    
    # Validate environment variables
    is_valid, errors = validate_environment_variables()
    
    # Check service compatibility
    compatibility_ok = check_service_compatibility()
    
    print("\n" + "=" * 60)
    
    if is_valid and compatibility_ok:
        print("SUCCESS: Environment is ready for production deployment!")
        print("  All services will use consistent API keys")
        print("  No demo keys detected")
        print("  Security configuration validated")
        return 0
    else:
        print("FAILED: Environment needs configuration updates")
        print("  Fix the errors above before deploying")
        return 1

if __name__ == "__main__":
    sys.exit(main())