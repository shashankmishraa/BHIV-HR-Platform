#!/usr/bin/env python3
"""
Setup environment variables for testing
"""
import os
import secrets

def setup_test_environment():
    """Setup test environment variables"""
    # Generate secure API key for testing
    test_api_key = secrets.token_urlsafe(32)
    
    # Set environment variables
    os.environ["API_KEY_SECRET"] = test_api_key
    os.environ["DEMO_PASSWORD"] = "secure_demo_password"
    os.environ["TOTP_SECRET"] = secrets.token_urlsafe(16)
    
    print("Environment variables set for testing:")
    print(f"API_KEY_SECRET: {test_api_key[:10]}...")
    print("DEMO_PASSWORD: secure_demo_password")
    print(f"TOTP_SECRET: {os.environ['TOTP_SECRET'][:10]}...")

if __name__ == "__main__":
    setup_test_environment()