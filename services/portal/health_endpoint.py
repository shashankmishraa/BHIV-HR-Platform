"""
Health endpoint for Streamlit HR Portal
"""
import streamlit as st
from datetime import datetime

def add_health_endpoint():
    """Add health check functionality to Streamlit app"""
    
    # Check if we're accessing the health endpoint
    query_params = st.experimental_get_query_params()
    
    if 'health' in query_params or st.session_state.get('health_check', False):
        st.json({
            "status": "healthy",
            "service": "BHIV HR Portal",
            "version": "3.2.0",
            "timestamp": datetime.now().isoformat(),
            "streamlit_version": st.__version__,
            "type": "streamlit_app"
        })
        st.stop()

# Add this to the main portal app
if __name__ == "__main__":
    add_health_endpoint()