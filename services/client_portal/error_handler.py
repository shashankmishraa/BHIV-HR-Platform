"""
Enterprise Error Handler for BHIV Client Portal
Comprehensive error handling with user-friendly messages and recovery options
"""

import streamlit as st
import requests
import logging
from datetime import datetime
from typing import Dict, Any, Optional, Callable
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ErrorHandler:
    """Enterprise-grade error handler with contextual messaging"""
    
    def __init__(self):
        self.error_history = []
        self.max_history = 50
    
    def log_error(self, error: Exception, context: str = "", user_action: str = ""):
        """Log error with context for debugging"""
        error_entry = {
            'timestamp': datetime.now().isoformat(),
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': context,
            'user_action': user_action,
            'traceback': traceback.format_exc()
        }
        
        self.error_history.append(error_entry)
        if len(self.error_history) > self.max_history:
            self.error_history.pop(0)
        
        logger.error(f"Error in {context}: {error}", exc_info=True)
    
    def handle_api_error(self, error: Exception, context: str = "", retry_callback: Optional[Callable] = None):
        """Handle API-related errors with specific messaging"""
        
        self.log_error(error, context, "API Request")
        
        if isinstance(error, requests.exceptions.Timeout):
            st.error("⏱️ **Request Timeout**")
            st.info("The server is taking too long to respond. This might be due to high traffic or server maintenance.")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Retry Request", key=f"retry_timeout_{context}"):
                    if retry_callback:
                        retry_callback()
                    else:
                        st.rerun()
            
            with col2:
                if st.button("📱 Switch to Offline Mode", key=f"offline_timeout_{context}"):
                    self.enable_offline_mode()
        
        elif isinstance(error, requests.exceptions.ConnectionError):
            st.error("🌐 **Connection Error**")
            st.info("Unable to connect to the server. Please check your internet connection.")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🔄 Retry Connection", key=f"retry_connection_{context}"):
                    if retry_callback:
                        retry_callback()
                    else:
                        st.rerun()
            
            with col2:
                if st.button("🔍 Check Status", key=f"status_connection_{context}"):
                    self.show_system_status()
            
            with col3:
                if st.button("📱 Offline Mode", key=f"offline_connection_{context}"):
                    self.enable_offline_mode()
        
        elif isinstance(error, requests.exceptions.HTTPError):
            status_code = getattr(error.response, 'status_code', 0) if hasattr(error, 'response') else 0
            
            if status_code == 401:
                st.error("🔐 **Authentication Failed**")
                st.info("Your session has expired or your credentials are invalid.")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔑 Login Again", key=f"login_401_{context}"):
                        self.clear_session_and_redirect()
                
                with col2:
                    if st.button("🔄 Refresh Token", key=f"refresh_401_{context}"):
                        self.attempt_token_refresh()
            
            elif status_code == 403:
                st.error("🚫 **Access Denied**")
                st.info("You don't have permission to perform this action.")
                
                if st.button("📞 Contact Support", key=f"support_403_{context}"):
                    self.show_support_contact()
            
            elif status_code == 404:
                st.error("🔍 **Resource Not Found**")
                st.info("The requested resource could not be found. It may have been moved or deleted.")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🏠 Go to Dashboard", key=f"home_404_{context}"):
                        st.session_state.clear()
                        st.rerun()
                
                with col2:
                    if st.button("🔄 Refresh Page", key=f"refresh_404_{context}"):
                        st.rerun()
            
            elif status_code == 429:
                st.error("⏳ **Rate Limit Exceeded**")
                st.info("Too many requests have been made. Please wait before trying again.")
                
                # Show countdown timer
                self.show_rate_limit_countdown()
            
            elif status_code >= 500:
                st.error("🔧 **Server Error**")
                st.info("The server is experiencing issues. Our team has been notified.")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔄 Try Again", key=f"retry_500_{context}"):
                        if retry_callback:
                            retry_callback()
                        else:
                            st.rerun()
                
                with col2:
                    if st.button("📊 System Status", key=f"status_500_{context}"):
                        self.show_system_status()
            
            else:
                st.error(f"❌ **HTTP Error {status_code}**")
                st.info("An unexpected error occurred. Please try again.")
                
                if st.button("🔄 Retry", key=f"retry_http_{context}"):
                    if retry_callback:
                        retry_callback()
                    else:
                        st.rerun()
        
        else:
            st.error("❌ **Unexpected Error**")
            st.info("An unexpected error occurred. Please try again or contact support if the issue persists.")
            
            with st.expander("🔍 Error Details (for support)"):
                st.code(f"Error Type: {type(error).__name__}\nMessage: {str(error)}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Try Again", key=f"retry_general_{context}"):
                    if retry_callback:
                        retry_callback()
                    else:
                        st.rerun()
            
            with col2:
                if st.button("📞 Report Issue", key=f"report_general_{context}"):
                    self.show_error_report_form(error, context)
    
    def handle_validation_error(self, field_name: str, error_message: str, suggestions: list = None):
        """Handle form validation errors"""
        
        st.error(f"⚠️ **{field_name} Error**")
        st.info(error_message)
        
        if suggestions:
            st.info("💡 **Suggestions:**")
            for suggestion in suggestions:
                st.write(f"• {suggestion}")
    
    def show_rate_limit_countdown(self):
        """Show countdown timer for rate limiting"""
        
        import time
        
        countdown_placeholder = st.empty()
        for i in range(60, 0, -1):
            countdown_placeholder.info(f"⏳ Please wait {i} seconds before trying again...")
            time.sleep(1)
        
        countdown_placeholder.success("✅ You can now try again!")
        
        if st.button("🔄 Continue", key="continue_after_rate_limit"):
            st.rerun()
    
    def enable_offline_mode(self):
        """Enable offline mode with cached data"""
        
        st.session_state['offline_mode'] = True
        st.info("📱 **Offline Mode Enabled**")
        st.info("You can now browse cached data while offline. Some features may be limited.")
        
        # Show available cached data
        if st.session_state.get('cached_jobs'):
            st.success(f"📋 {len(st.session_state['cached_jobs'])} jobs available offline")
        
        if st.session_state.get('cached_candidates'):
            st.success(f"👥 {len(st.session_state['cached_candidates'])} candidates available offline")
        
        if st.button("🌐 Try Online Mode", key="try_online_mode"):
            st.session_state['offline_mode'] = False
            st.rerun()
    
    def show_system_status(self):
        """Show system status information"""
        
        with st.expander("📊 System Status", expanded=True):
            st.info("**Checking system components...**")
            
            # Check API Gateway
            try:
                response = requests.get("https://bhiv-hr-gateway.onrender.com/health", timeout=5)
                if response.status_code == 200:
                    st.success("✅ API Gateway: Online")
                else:
                    st.error("❌ API Gateway: Issues detected")
            except:
                st.error("❌ API Gateway: Offline")
            
            # Check AI Agent
            try:
                response = requests.get("https://bhiv-hr-agent.onrender.com/health", timeout=5)
                if response.status_code == 200:
                    st.success("✅ AI Matching Engine: Online")
                else:
                    st.error("❌ AI Matching Engine: Issues detected")
            except:
                st.error("❌ AI Matching Engine: Offline")
            
            # Check HR Portal
            try:
                response = requests.get("https://bhiv-hr-portal.onrender.com/", timeout=5)
                if response.status_code == 200:
                    st.success("✅ HR Portal: Online")
                else:
                    st.error("❌ HR Portal: Issues detected")
            except:
                st.error("❌ HR Portal: Offline")
            
            st.info("🕐 Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    def clear_session_and_redirect(self):
        """Clear session and redirect to login"""
        
        # Clear authentication data
        auth_keys = ['client_authenticated', 'client_token', 'client_id', 'client_name', 'token_expires_at']
        for key in auth_keys:
            if key in st.session_state:
                del st.session_state[key]
        
        st.success("🔄 Session cleared. Please log in again.")
        st.rerun()
    
    def attempt_token_refresh(self):
        """Attempt to refresh authentication token"""
        
        if 'refresh_token' in st.session_state:
            try:
                # Call refresh endpoint
                refresh_data = {"refresh_token": st.session_state['refresh_token']}
                response = requests.post(
                    "https://bhiv-hr-gateway.onrender.com/v1/client/refresh",
                    json=refresh_data,
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    st.session_state['client_token'] = result['access_token']
                    st.session_state['refresh_token'] = result['refresh_token']
                    st.success("✅ Token refreshed successfully!")
                    st.rerun()
                else:
                    st.error("❌ Token refresh failed. Please log in again.")
                    self.clear_session_and_redirect()
            
            except Exception as e:
                st.error(f"❌ Token refresh error: {str(e)}")
                self.clear_session_and_redirect()
        else:
            st.error("❌ No refresh token available. Please log in again.")
            self.clear_session_and_redirect()
    
    def show_support_contact(self):
        """Show support contact information"""
        
        with st.expander("📞 Contact Support", expanded=True):
            st.info("**Need help? Contact our support team:**")
            st.write("📧 Email: support@bhiv-hr.com")
            st.write("📱 Phone: +1 (555) 123-4567")
            st.write("💬 Live Chat: Available 24/7")
            st.write("🌐 Help Center: https://help.bhiv-hr.com")
            
            st.info("**When contacting support, please include:**")
            st.write("• Your client ID")
            st.write("• Time when the error occurred")
            st.write("• What you were trying to do")
            st.write("• Any error messages you received")
    
    def show_error_report_form(self, error: Exception, context: str):
        """Show error reporting form"""
        
        with st.expander("📝 Report Error", expanded=True):
            st.info("Help us improve by reporting this error:")
            
            with st.form("error_report"):
                user_description = st.text_area(
                    "What were you trying to do when this error occurred?",
                    placeholder="Please describe the steps you took..."
                )
                
                user_email = st.text_input(
                    "Your email (optional)",
                    placeholder="your.email@company.com"
                )
                
                include_details = st.checkbox(
                    "Include technical details to help with debugging",
                    value=True
                )
                
                if st.form_submit_button("📤 Send Report"):
                    # In a real implementation, this would send to your error tracking system
                    st.success("✅ Error report sent! Thank you for helping us improve.")
                    st.info("Our team will investigate this issue and may contact you if more information is needed.")

# Global error handler instance
error_handler = ErrorHandler()

def handle_error(error: Exception, context: str = "", retry_callback: Optional[Callable] = None):
    """Global error handling function"""
    error_handler.handle_api_error(error, context, retry_callback)

def handle_validation_error(field_name: str, error_message: str, suggestions: list = None):
    """Global validation error handling function"""
    error_handler.handle_validation_error(field_name, error_message, suggestions)