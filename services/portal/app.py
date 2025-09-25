"""BHIV HR Portal - Modular Architecture v3.2.0"""

# pyright: reportMissingImports=false

from datetime import datetime
import os
import httpx
import pandas as pd
import streamlit as st
import uuid
import secrets

# Import components
from components.job_creation import show_job_creation
from components.dashboard import show_dashboard
from components.candidate_search import show_candidate_search
from components.candidate_upload import show_candidate_upload
from components.ai_matching import show_ai_matching
from components.interview_management import show_interview_management
from components.values_assessment import show_values_assessment
from components.export_reports import show_export_reports
from components.job_monitor import show_job_monitor
from components.batch_operations import show_batch_operations

# Page config
favicon_path = os.path.join(os.path.dirname(__file__), "static", "favicon.ico")
page_icon = favicon_path if os.path.exists(favicon_path) else "🎯"

st.set_page_config(
    page_title="BHIV HR Platform v3.2.0", page_icon=page_icon, layout="wide"
)

# Initialize unique session values
if "session_id" not in st.session_state:
    st.session_state.session_id = f"portal_{uuid.uuid4().hex[:8]}"
if "user_token" not in st.session_state:
    st.session_state.user_token = secrets.token_urlsafe(16)
if "request_count" not in st.session_state:
    st.session_state.request_count = 0

# Enhanced security setup with graceful fallback
try:
    from security_config import secure_api
    from input_sanitizer import sanitizer
    from sql_protection import sql_guard
    from rate_limiter import form_limiter

    SECURITY_ENABLED = True
    headers = secure_api.get_headers()
except ImportError:
    SECURITY_ENABLED = False
    # Enhanced API key management
    API_KEY = os.getenv("API_KEY_SECRET")
    if not API_KEY:
        environment = os.getenv("ENVIRONMENT", "development").lower()
        if environment == "production":
            st.error("🔒 API_KEY_SECRET required for production")
            st.stop()
        else:
            API_KEY = f"dev_{secrets.token_urlsafe(24)}"
            st.warning("🔧 Using development API key")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "X-Session-ID": st.session_state.session_id,
        "X-User-Token": st.session_state.user_token,
    }

# Environment setup
environment = os.getenv("ENVIRONMENT", "development").lower()
if environment == "production":
    default_agent_url = "https://bhiv-hr-agent-o6nx.onrender.com"
    default_gateway_url = "https://bhiv-hr-gateway-901a.onrender.com"
else:
    default_agent_url = "http://agent:9000"
    default_gateway_url = "http://gateway:8000"

AGENT_URL = os.getenv("AGENT_SERVICE_URL", default_agent_url)
API_BASE = os.getenv("GATEWAY_URL", default_gateway_url)

# Header
st.title("🎯 BHIV HR Portal")
st.markdown("**Values-Driven Recruiting Platform - HR Dashboard**")

# Sidebar with enhanced status
st.sidebar.title("🧭 HR Navigation")

# Show session info
with st.sidebar:
    st.markdown("---")
    st.markdown("**🔍 Session Status**")
    st.caption(f"Session: {st.session_state.session_id}")
    st.caption(f"Requests: {st.session_state.request_count}")

    # API Connection Status
    try:
        st.session_state.request_count += 1
        response = httpx.get(f"{API_BASE}/health", headers=headers, timeout=5.0)
        if response.status_code == 200:
            st.success("✅ API Connected")
        else:
            st.error("❌ API Unavailable")
    except:
        st.warning("⚠️ API Not Ready")

menu = st.sidebar.selectbox(
    "Select HR Task",
    [
        "📈 Dashboard Overview",
        "🏢 Step 1: Create Job Positions",
        "📤 Step 2: Upload Candidates",
        "🔍 Step 3: Search & Filter Candidates",
        "🎯 Step 4: AI Shortlist & Matching",
        "📅 Step 5: Schedule Interviews",
        "📊 Step 6: Submit Values Assessment",
        "🏆 Step 7: Export Assessment Reports",
        "🔄 Live Client Jobs Monitor",
        "📁 Batch Operations",
    ],
)

# Main content routing
if menu == "🏢 Step 1: Create Job Positions":
    show_job_creation(
        API_BASE,
        headers,
        SECURITY_ENABLED,
        sanitizer if SECURITY_ENABLED else None,
        form_limiter if SECURITY_ENABLED else None,
    )

elif menu == "📈 Dashboard Overview":
    show_dashboard(API_BASE, headers)

elif menu == "📤 Step 2: Upload Candidates":
    show_candidate_upload(
        API_BASE, headers, SECURITY_ENABLED, sanitizer if SECURITY_ENABLED else None
    )

elif menu == "🔍 Step 3: Search & Filter Candidates":
    show_candidate_search(
        API_BASE, headers, SECURITY_ENABLED, sql_guard if SECURITY_ENABLED else None
    )

elif menu == "🎯 Step 4: AI Shortlist & Matching":
    show_ai_matching(API_BASE, AGENT_URL, headers)

elif menu == "📅 Step 5: Schedule Interviews":
    show_interview_management(
        API_BASE, headers, SECURITY_ENABLED, sanitizer if SECURITY_ENABLED else None
    )

elif menu == "📊 Step 6: Submit Values Assessment":
    show_values_assessment()

elif menu == "🏆 Step 7: Export Assessment Reports":
    show_export_reports(API_BASE, headers)

elif menu == "🔄 Live Client Jobs Monitor":
    show_job_monitor(API_BASE, headers)

elif menu == "📁 Batch Operations":
    show_batch_operations(
        API_BASE, headers, SECURITY_ENABLED, sanitizer if SECURITY_ENABLED else None
    )

# Enhanced Footer with System Status
st.markdown("---")

# System status footer
footer_col1, footer_col2, footer_col3, footer_col4 = st.columns(4)

with footer_col1:
    st.markdown("**🎯 BHIV HR Platform**")
    st.caption("Values-Driven Recruiting with AI")

with footer_col2:
    st.markdown("**🤖 AI Status**")
    try:
        ai_response = httpx.get(f"{AGENT_URL}/health", timeout=3.0)
        if ai_response.status_code == 200:
            st.caption("✅ Talah AI: Online")
        else:
            st.caption("⚠️ Talah AI: Limited")
    except:
        st.caption("❌ Talah AI: Offline")

with footer_col3:
    st.markdown("**📊 Data Status**")
    st.caption(f"✅ Session: {st.session_state.session_id[:8]}")

with footer_col4:
    st.markdown("**🔒 Security**")
    security_status = "Enhanced" if SECURITY_ENABLED else "Basic"
    st.caption(f"🔒 {security_status} Mode")

st.markdown(
    "*Powered by Advanced Semantic AI + MDVP Compliance | Built with Integrity, Honesty, Discipline, Hard Work & Gratitude | © 2025*"
)
st.caption(
    f"📊 Session ID: {st.session_state.session_id} | Requests: {st.session_state.request_count} | Token: {st.session_state.user_token[:8]}..."
)
