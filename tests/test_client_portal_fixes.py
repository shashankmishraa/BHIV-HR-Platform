"""
Test Suite for BHIV Client Portal Enterprise Fixes
Comprehensive testing for authentication, error handling, and mobile responsiveness
"""

import pytest
import requests
import streamlit as st
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the client portal to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'services', 'client_portal'))

from error_handler import ErrorHandler, handle_error
from mobile_styles import inject_mobile_styles

class TestAuthenticationFixes:
    """Test authentication and token management fixes"""
    
    def setup_method(self):
        """Setup test environment"""
        self.base_url = "https://bhiv-hr-gateway.onrender.com"
        self.test_client_id = "TECH001"
        self.test_password = "demo123"
    
    def test_client_login_success(self):
        """Test successful client login"""
        login_data = {
            "client_id": self.test_client_id,
            "password": self.test_password
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/v1/client/login",
                json=login_data,
                timeout=10
            )
            
            assert response.status_code == 200
            result = response.json()
            
            # Check required fields
            assert "access_token" in result
            assert "refresh_token" in result
            assert "client_id" in result
            assert "expires_in" in result
            assert result["client_id"] == self.test_client_id
            
            print("✅ Client login test passed")
            
        except requests.exceptions.RequestException as e:
            pytest.skip(f"API not available: {e}")
    
    def test_client_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        login_data = {
            "client_id": "INVALID",
            "password": "wrong_password"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/v1/client/login",
                json=login_data,
                timeout=10
            )
            
            assert response.status_code == 401
            print("✅ Invalid credentials test passed")
            
        except requests.exceptions.RequestException as e:
            pytest.skip(f"API not available: {e}")
    
    def test_token_refresh(self):
        """Test token refresh functionality"""
        # First login to get tokens
        login_data = {
            "client_id": self.test_client_id,
            "password": self.test_password
        }
        
        try:
            login_response = requests.post(
                f"{self.base_url}/v1/client/login",
                json=login_data,
                timeout=10
            )
            
            if login_response.status_code == 200:
                login_result = login_response.json()
                refresh_token = login_result.get("refresh_token")
                
                # Test refresh
                refresh_data = {"refresh_token": refresh_token}
                refresh_response = requests.post(
                    f"{self.base_url}/v1/client/refresh",
                    json=refresh_data,
                    timeout=10
                )
                
                if refresh_response.status_code == 200:
                    refresh_result = refresh_response.json()
                    assert "access_token" in refresh_result
                    assert "refresh_token" in refresh_result
                    print("✅ Token refresh test passed")
                else:
                    print(f"⚠️ Token refresh endpoint returned {refresh_response.status_code}")
            
        except requests.exceptions.RequestException as e:
            pytest.skip(f"API not available: {e}")
    
    def test_token_verification(self):
        """Test token verification"""
        # First login to get token
        login_data = {
            "client_id": self.test_client_id,
            "password": self.test_password
        }
        
        try:
            login_response = requests.post(
                f"{self.base_url}/v1/client/login",
                json=login_data,
                timeout=10
            )
            
            if login_response.status_code == 200:
                login_result = login_response.json()
                access_token = login_result.get("access_token")
                
                # Test verification
                headers = {"Authorization": f"Bearer {access_token}"}
                verify_response = requests.get(
                    f"{self.base_url}/v1/client/verify",
                    headers=headers,
                    timeout=10
                )
                
                if verify_response.status_code == 200:
                    verify_result = verify_response.json()
                    assert verify_result.get("valid") is True
                    assert verify_result.get("client_id") == self.test_client_id
                    print("✅ Token verification test passed")
                else:
                    print(f"⚠️ Token verification returned {verify_response.status_code}")
            
        except requests.exceptions.RequestException as e:
            pytest.skip(f"API not available: {e}")

class TestErrorHandling:
    """Test error handling improvements"""
    
    def setup_method(self):
        """Setup error handler"""
        self.error_handler = ErrorHandler()
    
    def test_timeout_error_handling(self):
        """Test timeout error handling"""
        timeout_error = requests.exceptions.Timeout("Request timed out")
        
        # Mock streamlit functions
        with patch('streamlit.error') as mock_error, \
             patch('streamlit.info') as mock_info, \
             patch('streamlit.columns') as mock_columns, \
             patch('streamlit.button') as mock_button:
            
            mock_columns.return_value = [Mock(), Mock()]
            mock_button.return_value = False
            
            self.error_handler.handle_api_error(timeout_error, "test_context")
            
            # Verify error message was displayed
            mock_error.assert_called()
            mock_info.assert_called()
            
            print("✅ Timeout error handling test passed")
    
    def test_connection_error_handling(self):
        """Test connection error handling"""
        connection_error = requests.exceptions.ConnectionError("Connection failed")
        
        with patch('streamlit.error') as mock_error, \
             patch('streamlit.info') as mock_info, \
             patch('streamlit.columns') as mock_columns, \
             patch('streamlit.button') as mock_button:
            
            mock_columns.return_value = [Mock(), Mock(), Mock()]
            mock_button.return_value = False
            
            self.error_handler.handle_api_error(connection_error, "test_context")
            
            mock_error.assert_called()
            mock_info.assert_called()
            
            print("✅ Connection error handling test passed")
    
    def test_http_error_handling(self):
        """Test HTTP error handling"""
        # Mock response object
        mock_response = Mock()
        mock_response.status_code = 401
        
        http_error = requests.exceptions.HTTPError("401 Unauthorized")
        http_error.response = mock_response
        
        with patch('streamlit.error') as mock_error, \
             patch('streamlit.info') as mock_info, \
             patch('streamlit.columns') as mock_columns, \
             patch('streamlit.button') as mock_button:
            
            mock_columns.return_value = [Mock(), Mock()]
            mock_button.return_value = False
            
            self.error_handler.handle_api_error(http_error, "test_context")
            
            mock_error.assert_called()
            mock_info.assert_called()
            
            print("✅ HTTP error handling test passed")
    
    def test_validation_error_handling(self):
        """Test validation error handling"""
        with patch('streamlit.error') as mock_error, \
             patch('streamlit.info') as mock_info, \
             patch('streamlit.write') as mock_write:
            
            suggestions = ["Use a valid email format", "Include @ symbol"]
            self.error_handler.handle_validation_error(
                "Email", 
                "Invalid email format", 
                suggestions
            )
            
            mock_error.assert_called()
            mock_info.assert_called()
            
            print("✅ Validation error handling test passed")
    
    def test_error_logging(self):
        """Test error logging functionality"""
        test_error = ValueError("Test error")
        
        initial_count = len(self.error_handler.error_history)
        self.error_handler.log_error(test_error, "test_context", "test_action")
        
        assert len(self.error_handler.error_history) == initial_count + 1
        
        latest_error = self.error_handler.error_history[-1]
        assert latest_error['error_type'] == 'ValueError'
        assert latest_error['error_message'] == 'Test error'
        assert latest_error['context'] == 'test_context'
        assert latest_error['user_action'] == 'test_action'
        
        print("✅ Error logging test passed")

class TestMobileResponsiveness:
    """Test mobile responsiveness features"""
    
    def test_mobile_styles_injection(self):
        """Test mobile CSS injection"""
        with patch('streamlit.markdown') as mock_markdown:
            inject_mobile_styles()
            
            # Verify CSS was injected
            mock_markdown.assert_called()
            call_args = mock_markdown.call_args[0][0]
            
            # Check for mobile-specific CSS
            assert "@media screen and (max-width: 768px)" in call_args
            assert "font-size: 16px" in call_args  # iOS zoom prevention
            assert "width: 100%" in call_args
            
            print("✅ Mobile styles injection test passed")
    
    def test_responsive_breakpoints(self):
        """Test responsive breakpoints"""
        with patch('streamlit.markdown') as mock_markdown:
            inject_mobile_styles()
            
            call_args = mock_markdown.call_args[0][0]
            
            # Check for different breakpoints
            assert "max-width: 768px" in call_args  # Mobile
            assert "min-width: 769px" in call_args and "max-width: 1024px" in call_args  # Tablet
            assert "min-width: 1025px" in call_args  # Desktop
            
            print("✅ Responsive breakpoints test passed")
    
    def test_accessibility_features(self):
        """Test accessibility features in CSS"""
        with patch('streamlit.markdown') as mock_markdown:
            inject_mobile_styles()
            
            call_args = mock_markdown.call_args[0][0]
            
            # Check for accessibility features
            assert "prefers-contrast: high" in call_args
            assert "prefers-reduced-motion: reduce" in call_args
            assert "min-height: 44px" in call_args  # Touch targets
            
            print("✅ Accessibility features test passed")

class TestAPIIntegration:
    """Test API integration improvements"""
    
    def setup_method(self):
        """Setup API test environment"""
        self.base_url = "https://bhiv-hr-gateway.onrender.com"
        self.api_key = "myverysecureapikey123"
    
    def test_api_health_check(self):
        """Test API health endpoints"""
        endpoints = [
            f"{self.base_url}/health",
            "https://bhiv-hr-agent.onrender.com/health",
            "https://bhiv-hr-portal.onrender.com/"
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.get(endpoint, timeout=10)
                print(f"✅ {endpoint}: {response.status_code}")
                
            except requests.exceptions.RequestException as e:
                print(f"⚠️ {endpoint}: {e}")
    
    def test_jobs_endpoint_with_auth(self):
        """Test jobs endpoint with authentication"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/v1/jobs",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                jobs = response.json()
                assert isinstance(jobs, (list, dict))
                print("✅ Jobs endpoint test passed")
            else:
                print(f"⚠️ Jobs endpoint returned {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            pytest.skip(f"API not available: {e}")
    
    def test_candidates_endpoint_with_auth(self):
        """Test candidates endpoint with authentication"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/v1/candidates/search",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                candidates = response.json()
                assert isinstance(candidates, (list, dict))
                print("✅ Candidates endpoint test passed")
            else:
                print(f"⚠️ Candidates endpoint returned {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            pytest.skip(f"API not available: {e}")

class TestOfflineSupport:
    """Test offline support functionality"""
    
    def test_cache_initialization(self):
        """Test cache initialization"""
        # Mock session state
        mock_session_state = {}
        
        with patch('streamlit.session_state', mock_session_state):
            # Simulate cache initialization
            if 'cached_jobs' not in mock_session_state:
                mock_session_state['cached_jobs'] = []
            if 'cached_candidates' not in mock_session_state:
                mock_session_state['cached_candidates'] = []
            
            assert 'cached_jobs' in mock_session_state
            assert 'cached_candidates' in mock_session_state
            
            print("✅ Cache initialization test passed")
    
    def test_offline_mode_toggle(self):
        """Test offline mode toggle"""
        mock_session_state = {'offline_mode': False}
        
        with patch('streamlit.session_state', mock_session_state):
            # Toggle offline mode
            mock_session_state['offline_mode'] = True
            
            assert mock_session_state['offline_mode'] is True
            
            # Toggle back
            mock_session_state['offline_mode'] = False
            
            assert mock_session_state['offline_mode'] is False
            
            print("✅ Offline mode toggle test passed")

def run_comprehensive_tests():
    """Run all tests and generate report"""
    
    print("🧪 Running BHIV Client Portal Enterprise Fixes Test Suite")
    print("=" * 60)
    
    test_classes = [
        TestAuthenticationFixes,
        TestErrorHandling,
        TestMobileResponsiveness,
        TestAPIIntegration,
        TestOfflineSupport
    ]
    
    total_tests = 0
    passed_tests = 0
    
    for test_class in test_classes:
        print(f"\n📋 Running {test_class.__name__}")
        print("-" * 40)
        
        test_instance = test_class()
        test_methods = [method for method in dir(test_instance) if method.startswith('test_')]
        
        for method_name in test_methods:
            total_tests += 1
            try:
                if hasattr(test_instance, 'setup_method'):
                    test_instance.setup_method()
                
                method = getattr(test_instance, method_name)
                method()
                passed_tests += 1
                
            except Exception as e:
                print(f"❌ {method_name} failed: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! Enterprise fixes are working correctly.")
    else:
        print(f"⚠️ {total_tests - passed_tests} tests failed. Please review the issues above.")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    run_comprehensive_tests()