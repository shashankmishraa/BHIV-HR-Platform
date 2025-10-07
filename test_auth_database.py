#!/usr/bin/env python3
"""
Test Auth Service Database Integration
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'services', 'client_portal'))

def test_auth_database():
    """Test auth service database operations"""
    print("Testing Auth Service Database Integration")
    print("=" * 50)
    
    try:
        from auth_service import ClientAuthService
        
        # Initialize service
        auth_service = ClientAuthService()
        print("Auth service initialized with database connection")
        
        # Test database connection by checking client info
        client_info = auth_service.get_client_info("TECH001")
        if client_info:
            print(f"Database connection successful - Found client: {client_info['company_name']}")
            
            # Test authentication with correct credentials
            auth_result = auth_service.authenticate_client("TECH001", "demo123")
            if auth_result.get('success'):
                print(f"Authentication successful: {auth_result['client_id']}")
                
                # Test token verification
                token = auth_result.get('token')
                if token:
                    verify_result = auth_service.verify_token(token)
                    if verify_result.get('success'):
                        print(f"Token verification successful: {verify_result['client_id']}")
                    else:
                        print(f"Token verification failed: {verify_result.get('error')}")
                        
                    # Test logout
                    logout_success = auth_service.logout_client(token)
                    print(f"Logout test: {'Success' if logout_success else 'Failed'}")
                    
            else:
                print(f"Authentication failed: {auth_result.get('error')}")
                
                # Let's try to register the client again to ensure it exists
                register_result = auth_service.register_client(
                    "TECH001", 
                    "TechCorp Solutions", 
                    "admin@techcorp.com", 
                    "demo123"
                )
                print(f"Registration attempt: {register_result}")
                
        else:
            print("No client found - attempting to create default clients")
            
            # Try to register a test client
            register_result = auth_service.register_client(
                "TECH001", 
                "TechCorp Solutions", 
                "admin@techcorp.com", 
                "demo123"
            )
            print(f"Registration result: {register_result}")
            
            if register_result.get('success'):
                # Try authentication again
                auth_result = auth_service.authenticate_client("TECH001", "demo123")
                print(f"Authentication after registration: {auth_result}")
        
        print("\nDatabase integration test completed")
        return True
        
    except Exception as e:
        print(f"Test error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_auth_database()
    sys.exit(0 if success else 1)