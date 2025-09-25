"""Simplified BHIV HR Portal - Reduced complexity version"""

from datetime import datetime
import os
import httpx
import pandas as pd
import streamlit as st

# Import components
from components.job_creation import show_job_creation
from components.dashboard import show_dashboard

# Page config
favicon_path = os.path.join(os.path.dirname(__file__), "static", "favicon.ico")
page_icon = favicon_path if os.path.exists(favicon_path) else "🎯"

st.set_page_config(
    page_title="BHIV HR Platform v3.2.0", 
    page_icon=page_icon, 
    layout="wide"
)

# Security setup
try:
    from security_config import secure_api
    from input_sanitizer import sanitizer
    from sql_protection import sql_guard
    from rate_limiter import form_limiter
    SECURITY_ENABLED = True
    headers = secure_api.get_headers()
except ImportError:
    SECURITY_ENABLED = False
    API_KEY = os.getenv("API_KEY_SECRET", "temp_dev_key")
    headers = {"Authorization": f"Bearer {API_KEY}"}

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

# Sidebar
st.sidebar.title("🧭 HR Navigation")

menu = st.sidebar.selectbox("Select HR Task", [
    "📈 Dashboard Overview",
    "🏢 Step 1: Create Job Positions",
    "📤 Step 2: Upload Candidates",
    "🔍 Step 3: Search & Filter Candidates"
])

# Main content routing
if menu == "🏢 Step 1: Create Job Positions":
    show_job_creation(API_BASE, headers, SECURITY_ENABLED, 
                     sanitizer if SECURITY_ENABLED else None, 
                     form_limiter if SECURITY_ENABLED else None)

elif menu == "📈 Dashboard Overview":
    show_dashboard(API_BASE, headers)

elif menu == "📤 Step 2: Upload Candidates":
    st.header("Bulk Candidate Upload")
    st.write("Upload multiple candidates for a job position using CSV format")
    
    job_id = st.number_input("Job ID", min_value=1, step=1, value=1)
    uploaded_file = st.file_uploader("Choose CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.dataframe(df, use_container_width=True)
            
            if st.button("📤 Upload Candidates", use_container_width=True):
                candidates = []
                for _, row in df.iterrows():
                    candidate = {
                        "name": str(row.get("name", "")).strip(),
                        "email": str(row.get("email", "")).strip(),
                        "job_id": job_id
                    }
                    candidates.append(candidate)
                
                try:
                    response = httpx.post(f"{API_BASE}/v1/candidates/bulk", 
                                        json={"candidates": candidates}, 
                                        headers=headers, timeout=10.0)
                    if response.status_code == 200:
                        st.success(f"✅ Successfully uploaded {len(df)} candidates")
                        st.balloons()
                    else:
                        st.error(f"❌ Upload failed: {response.text}")
                except Exception as e:
                    st.error(f"❌ Upload error: {str(e)}")
        except Exception as e:
            st.error(f"❌ Error reading CSV file: {str(e)}")

elif menu == "🔍 Step 3: Search & Filter Candidates":
    st.header("Advanced Candidate Search & Filtering")
    
    search_query = st.text_input("🔍 Search Candidates", placeholder="Search by name, skills...")
    search_clicked = st.button("🔍 Search Candidates", use_container_width=True)
    
    if search_clicked and search_query:
        try:
            params = {"q": search_query.strip()}
            response = httpx.get(f"{API_BASE}/v1/candidates/search", 
                               params=params, headers=headers, timeout=10.0)
            
            if response.status_code == 200:
                data = response.json()
                candidates = data.get("candidates", [])
                st.success(f"✅ Found {len(candidates)} candidates")
                
                for candidate in candidates:
                    with st.expander(f"👥 {candidate['name']}"):
                        st.write(f"**Email:** {candidate['email']}")
                        st.write(f"**Experience:** {candidate.get('experience_years', 0)} years")
            else:
                st.error(f"❌ Search failed: {response.text}")
        except Exception as e:
            st.error(f"❌ Search error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("*Powered by Advanced AI | Built with Values*")