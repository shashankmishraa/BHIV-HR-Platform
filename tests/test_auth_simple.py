#!/usr/bin/env python3
"""
Simple Auth Test - Direct function testing
"""

import jwt
import os

def test_jwt_verification():
    """Test JWT token verification directly"""
    print("Testing JWT Token Verification")
    print("=" * 40)
    
    # Test token from auth service
    test_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRfaWQiOiJURVNUQ0xJRU5UIiwiY29tcGFueV9uYW1lIjoiVGVzdCBDb21wYW55IEx0ZCIsImV4cCI6MTc1OTkxNjk4MCwiaWF0IjoxNzU5ODMwNTgwLCJpc3MiOiJiaGl2X2hyX3BsYXRmb3JtIn0.xT0wSEdbLMYlqMNpGdxbAm9Km-Uw790KGaPRCPqZu5k"
    jwt_secret = "fallback_jwt_secret_key_for_client_auth_2025"
    
    try:
        payload = jwt.decode(test_token, jwt_secret, algorithms=["HS256"])
        print(f"Token verification: SUCCESS")
        print(f"Client ID: {payload.get('client_id')}")
        print(f"Company: {payload.get('company_name')}")
        return True
    except jwt.ExpiredSignatureError:
        print("Token verification: EXPIRED")
        return False
    except jwt.InvalidTokenError as e:
        print(f"Token verification: INVALID - {e}")
        return False
    except Exception as e:
        print(f"Token verification: ERROR - {e}")
        return False

if __name__ == "__main__":
    test_jwt_verification()