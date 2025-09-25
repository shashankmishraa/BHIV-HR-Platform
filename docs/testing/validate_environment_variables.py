#!/usr/bin/env python3
"""
Environment Variable Validation Script
Ensures all services use consistent production API keys
"""

import os
import sys
from typing import Dict, List, Tuple


def validate_environment_variables() -> Tuple[bool, List[str]]:
    """
    Validate environment variables for production deployment

    Returns:
        Tuple[bool, List[str]]: (is_valid, error_messages)
    """
    errors = []
    warnings = []

    # Required environment variables for production
    required_vars = {
        "API_KEY_SECRET": "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o",
        "JWT_SECRET": "prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA",
        "ENVIRONMENT": "production",
    }

    # Optional but recommended variables
    optional_vars = {
        "DATABASE_URL": "postgresql://bhiv_user:bhiv_pass@db:5432/bhiv_hr",
        "CORS_ORIGINS": "https://bhiv-hr-portal.onrender.com,https://bhiv-hr-client-portal.onrender.com",
        "GATEWAY_URL": "https://bhiv-hr-gateway.onrender.com",
        "AGENT_URL": "https://bhiv-hr-agent.onrender.com",
    }

    # Demo keys that should be rejected in production
    demo_keys = [
        "myverysecureapikey123",
        "demo",
        "test",
        "sample",
        "dev_fallback",
        "temp_dev_key",
    ]

    print("🔍 Validating Environment Variables for Production Deployment")
    print("=" * 60)

    # Check required variables
    for var_name, expected_value in required_vars.items():
        current_value = os.getenv(var_name)

        if not current_value:
            errors.append(f"❌ {var_name} is not set")
            continue

        # Special validation for API_KEY_SECRET
        if var_name == "API_KEY_SECRET":
            if any(demo_key in current_value.lower() for demo_key in demo_keys):
                errors.append(
                    f"❌ {var_name} contains demo/test value: {current_value[:8]}..."
                )
                continue

            if len(current_value) < 16:
                errors.append(f"❌ {var_name} is too short (minimum 16 characters)")
                continue

            if current_value == expected_value:
                print(f"✅ {var_name}: Production key configured correctly")
            else:
                warnings.append(
                    f"⚠️  {var_name}: Using custom production key (not default)"
                )

        # Special validation for JWT_SECRET
        elif var_name == "JWT_SECRET":
            if len(current_value) < 32:
                errors.append(f"❌ {var_name} is too short (minimum 32 characters)")
                continue

            if current_value == expected_value:
                print(f"✅ {var_name}: Production secret configured correctly")
            else:
                warnings.append(
                    f"⚠️  {var_name}: Using custom production secret (not default)"
                )

        # Environment validation
        elif var_name == "ENVIRONMENT":
            if current_value.lower() != "production":
                errors.append(
                    f"❌ {var_name} must be 'production', got: {current_value}"
                )
            else:
                print(f"✅ {var_name}: {current_value}")

        else:
            print(f"✅ {var_name}: {current_value}")

    print()

    # Check optional variables
    print("📋 Optional Variables:")
    for var_name, expected_value in optional_vars.items():
        current_value = os.getenv(var_name)

        if current_value:
            print(f"✅ {var_name}: {current_value}")
        else:
            warnings.append(f"⚠️  {var_name} not set (using default: {expected_value})")

    print()

    # Display warnings
    if warnings:
        print("⚠️  Warnings:")
        for warning in warnings:
            print(f"   {warning}")
        print()

    # Display errors
    if errors:
        print("❌ Errors:")
        for error in errors:
            print(f"   {error}")
        print()
        print("🔧 To fix these issues:")
        print(
            "   1. Set API_KEY_SECRET=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
        )
        print(
            "   2. Set JWT_SECRET=prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA"
        )
        print("   3. Set ENVIRONMENT=production")
        print("   4. Update Render environment variables in dashboard")
        return False, errors

    print("🎉 All environment variables are correctly configured for production!")
    return True, []


def check_service_compatibility():
    """Check if all services will use the same API key"""
    api_key = os.getenv("API_KEY_SECRET")
    jwt_secret = os.getenv("JWT_SECRET")
    environment = os.getenv("ENVIRONMENT", "development")

    print("\n🔗 Service Compatibility Check:")
    print("=" * 40)

    services = [
        "Gateway Service",
        "Portal Service",
        "Client Portal Service",
        "Agent Service",
    ]

    if api_key and jwt_secret:
        print(f"✅ All services will use API key: {api_key[:8]}...")
        print(f"✅ All services will use JWT secret: {jwt_secret[:8]}...")
        print(f"✅ Environment: {environment}")
        print(f"✅ Services configured: {', '.join(services)}")
        return True
    else:
        print("❌ Services will use different keys (fallback mode)")
        return False


def generate_render_env_config():
    """Generate Render environment configuration"""
    print("\n📝 Render Environment Configuration:")
    print("=" * 40)
    print("Copy these to Render dashboard for all services:")
    print()

    config = {
        "API_KEY_SECRET": "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o",
        "JWT_SECRET": "prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA",
        "ENVIRONMENT": "production",
        "DATABASE_URL": "postgresql://bhiv_user:bhiv_pass@db:5432/bhiv_hr",
        "CORS_ORIGINS": "https://bhiv-hr-portal.onrender.com,https://bhiv-hr-client-portal.onrender.com",
        "GATEWAY_URL": "https://bhiv-hr-gateway.onrender.com",
        "AGENT_URL": "https://bhiv-hr-agent.onrender.com",
    }

    for key, value in config.items():
        print(f"{key}={value}")


def main():
    """Main validation function"""
    print("🚀 BHIV HR Platform - Environment Variable Validation")
    print("=" * 60)

    # Validate environment variables
    is_valid, errors = validate_environment_variables()

    # Check service compatibility
    compatibility_ok = check_service_compatibility()

    # Generate Render configuration
    generate_render_env_config()

    print("\n" + "=" * 60)

    if is_valid and compatibility_ok:
        print("🎉 SUCCESS: Environment is ready for production deployment!")
        print("   All services will use consistent API keys")
        print("   No demo keys detected")
        print("   Security configuration validated")
        return 0
    else:
        print("❌ FAILED: Environment needs configuration updates")
        print("   Fix the errors above before deploying")
        return 1


if __name__ == "__main__":
    sys.exit(main())
