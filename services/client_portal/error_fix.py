"""
Contextual Error Handler for BHIV Client Portal
Specific error messages with actionable solutions
"""

import streamlit as st
import requests

def handle_api_error(error, context="", retry_func=None):
    """Handle API errors with specific, contextual messages"""
    
    if isinstance(error, requests.exceptions.Timeout):
        st.error("⏱️ **Network Timeout**")
        st.info(f"The {context} request timed out. The server may be busy.")
        if retry_func and st.button("🔄 Retry", key=f"retry_timeout_{context}"):
            retry_func()
    
    elif isinstance(error, requests.exceptions.ConnectionError):
        st.error("🌐 **Connection Failed**")
        st.info(f"Cannot connect to server for {context}. Check your internet connection.")
        if retry_func and st.button("🔄 Try Again", key=f"retry_conn_{context}"):
            retry_func()
    
    elif isinstance(error, requests.exceptions.HTTPError):
        status_code = getattr(error.response, 'status_code', 0) if hasattr(error, 'response') else 0
        
        if status_code == 401:
            st.error("🔐 **Authentication Failed**")
            st.info("Your session token has expired. Please log in again.")
            if st.button("🔑 Login Again", key=f"login_{context}"):
                # Clear session and force re-login
                for key in ['client_authenticated', 'client_token', 'refresh_token']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
        
        elif status_code == 403:
            st.error("🚫 **Access Denied**")
            st.info(f"You don't have permission to {context}.")
        
        elif status_code == 404:
            st.error("🔍 **Not Found**")
            st.info(f"The {context} endpoint was not found. The service may be down.")
        
        elif status_code == 429:
            st.error("⏳ **Rate Limited**")
            st.info("Too many requests. Please wait before trying again.")
        
        elif status_code >= 500:
            st.error("🔧 **Server Error**")
            st.info(f"Server error during {context}. Please try again later.")
            if retry_func and st.button("🔄 Retry", key=f"retry_server_{context}"):
                retry_func()
        
        else:
            st.error(f"❌ **HTTP {status_code} Error**")
            st.info(f"Unexpected error during {context}.")
    
    else:
        st.error("❌ **Unexpected Error**")
        st.info(f"An unexpected error occurred during {context}: {str(error)}")
        if retry_func and st.button("🔄 Try Again", key=f"retry_general_{context}"):
            retry_func()

def show_cached_data_fallback(data_type):
    """Show cached data when offline"""
    if data_type == "jobs" and st.session_state.get('cached_jobs'):
        st.info("💾 **Offline Mode**: Showing cached jobs")
        with st.expander("📁 Cached Jobs"):
            for job in st.session_state['cached_jobs'][:5]:
                st.write(f"• {job.get('title', 'Unknown')} (ID: {job.get('id', 'N/A')})")
    else:
        st.warning("⚠️ **No Cached Data Available**")
        st.info("Connect to the internet to load fresh data.")