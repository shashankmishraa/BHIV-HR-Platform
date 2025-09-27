"""Dashboard component for HR portal"""

import streamlit as st

def show_dashboard(api_base, headers):
    """Show HR dashboard"""
    st.header("📈 HR Dashboard Overview")
    st.info("Dashboard functionality integrated into main app")
    
    # Basic metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Active Jobs", "0")
    with col2:
        st.metric("Candidates", "0") 
    with col3:
        st.metric("Interviews", "0")