"""Job monitoring component"""

import streamlit as st
import httpx

def show_job_monitor(API_BASE, headers):
    """Display live client job postings monitor"""
    st.header("🔄 Live Client Job Postings")
    st.info("📊 Real-time view of all jobs posted by clients across the platform")
    
    try:
        response = httpx.get(f"{API_BASE}/v1/jobs", headers=headers, timeout=10.0)
        if response.status_code == 200:
            jobs_data = response.json()
            jobs = jobs_data.get('jobs', [])
            
            if jobs:
                # Group jobs by client
                client_jobs = {}
                for job in jobs:
                    client_id = job.get('client_id', 'Unknown')
                    if client_id not in client_jobs:
                        client_jobs[client_id] = []
                    client_jobs[client_id].append(job)
                
                # Display summary
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Jobs", len(jobs))
                with col2:
                    st.metric("Active Clients", len(client_jobs))
                with col3:
                    recent_jobs = sum(1 for job in jobs if job.get('created_at', '').startswith('2025'))
                    st.metric("Recent Jobs", recent_jobs)
                
                st.markdown("---")
                
                # Display jobs by client
                for client_id, job_list in sorted(client_jobs.items()):
                    st.subheader(f"🏢 Client {client_id} ({len(job_list)} jobs)")
                    
                    for job in job_list:
                        with st.expander(f"💼 {job.get('title', 'Untitled Job')} - {job.get('department', 'N/A')}"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.write(f"**Job ID:** {job.get('id', 'N/A')}")
                                st.write(f"**Department:** {job.get('department', 'N/A')}")
                                st.write(f"**Location:** {job.get('location', 'N/A')}")
                                st.write(f"**Experience:** {job.get('experience_level', 'N/A')}")
                            
                            with col2:
                                st.write(f"**Type:** {job.get('employment_type', 'N/A')}")
                                st.write(f"**Status:** {job.get('status', 'active')}")
                                st.write(f"**Posted:** {job.get('created_at', 'Unknown')}")
                            
                            if job.get('description'):
                                st.write("**Description:**")
                                st.write(job.get('description', '')[:300] + "...")
                            
                            # Action buttons
                            btn_col1, btn_col2, btn_col3 = st.columns(3)
                            with btn_col1:
                                if st.button(f"🎯 Get AI Matches", key=f"match_{job.get('id')}"):
                                    st.info(f"Getting AI matches for Job {job.get('id')}...")
                            with btn_col2:
                                if st.button(f"👥 View Candidates", key=f"candidates_{job.get('id')}"):
                                    st.info(f"Viewing candidates for Job {job.get('id')}...")
                            with btn_col3:
                                if st.button(f"📊 Analytics", key=f"analytics_{job.get('id')}"):
                                    st.info(f"Loading analytics for Job {job.get('id')}...")
            else:
                st.info("📊 No jobs found. Clients haven't posted any jobs yet.")
        else:
            st.error(f"❌ Failed to load jobs: {response.status_code}")
    except Exception as e:
        st.error(f"❌ Error loading jobs: {str(e)}")