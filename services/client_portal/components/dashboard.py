"""Dashboard component for client portal"""

import streamlit as st

def show_dashboard():
    """Show client dashboard"""
    st.header("📊 Client Dashboard")
    st.info("Dashboard functionality integrated into main app")
    
    # Basic dashboard metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Active Jobs", "0")
    with col2:
        st.metric("Applications", "0")
    with col3:
        st.metric("Interviews", "0")
    
    return None