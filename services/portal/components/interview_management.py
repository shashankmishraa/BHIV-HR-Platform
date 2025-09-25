"""Interview management component"""

import streamlit as st
import httpx
from datetime import datetime

def show_interview_management(API_BASE, headers, SECURITY_ENABLED, sanitizer=None):
    """Display interview management system"""
    st.header("Interview Management System")
    st.write("Schedule, track, and manage candidate interviews")
    
    tab1, tab2 = st.tabs(["📅 Schedule Interview", "📋 View Interviews"])
    
    with tab1:
        st.subheader("Schedule New Interview")
        
        with st.form("interview_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                candidate_id = st.number_input("Candidate ID", min_value=1, step=1)
                candidate_name = st.text_input("Candidate Name")
                job_id = st.number_input("Job ID", min_value=1, step=1, value=1)
            
            with col2:
                interview_date = st.date_input("Interview Date")
                interview_time = st.time_input("Interview Time")
                interviewer = st.text_input("Interviewer Name")
            
            submitted = st.form_submit_button("📅 Schedule Interview", use_container_width=True)
            
            if submitted and candidate_name and interviewer:
                interview_data = {
                    "candidate_id": candidate_id,
                    "job_id": job_id,
                    "interview_date": f"{interview_date} {interview_time}",
                    "interviewer": interviewer,
                    "notes": f"Interview scheduled for {candidate_name}"
                }
                
                if SECURITY_ENABLED and sanitizer:
                    interview_data = sanitizer.sanitize_dict(interview_data)
                
                try:
                    response = httpx.post(f"{API_BASE}/v1/interviews", 
                                        json=interview_data, 
                                        headers=headers, timeout=10.0)
                    if response.status_code == 200:
                        st.success(f"✅ Interview scheduled for {candidate_name}!")
                        st.balloons()
                    else:
                        st.error(f"❌ Failed to schedule: {response.text}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
            elif submitted:
                st.warning("⚠️ Please fill in candidate name and interviewer")
    
    with tab2:
        st.subheader("Scheduled Interviews")
        
        try:
            response = httpx.get(f"{API_BASE}/v1/interviews", headers=headers, timeout=10.0)
            if response.status_code == 200:
                data = response.json()
                interviews = data.get('interviews', [])
                
                if interviews:
                    for interview in interviews:
                        interview_date = interview.get('interview_date', 'Unknown')
                        if 'T' in interview_date:
                            interview_date = interview_date.split('T')[0]
                        
                        with st.expander(f"📅 {interview.get('candidate_name', 'Unknown')} - {interview_date}"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f"**Candidate:** {interview.get('candidate_name', 'Unknown')}")
                                st.write(f"**Date:** {interview_date}")
                                st.write(f"**Job:** {interview.get('job_title', 'Unknown')}")
                            with col2:
                                st.write(f"**Interviewer:** {interview.get('interviewer', 'Unknown')}")
                                st.write(f"**Status:** {interview.get('status', 'Unknown')}")
                                st.write(f"**ID:** {interview.get('id', 'N/A')}")
                else:
                    st.info("📅 No interviews scheduled yet")
            else:
                st.error(f"❌ Failed to load interviews: {response.status_code}")
        except Exception as e:
            st.error(f"❌ Error loading interviews: {str(e)}")