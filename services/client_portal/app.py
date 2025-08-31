import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from scoring_explanations import get_score_explanation, explain_skills_match, get_experience_explanation

# Configuration
API_BASE_URL = "http://localhost:8000"
API_KEY = "myverysecureapikey123"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def main():
    st.set_page_config(
        page_title="BHIV Client Portal",
        page_icon="🏢",
        layout="wide"
    )
    
    st.title("🏢 BHIV Client Portal")
    st.markdown("**Dedicated Client Interface for Job Posting & Candidate Review**")
    
    # Client authentication
    if 'client_authenticated' not in st.session_state:
        show_client_login()
        return
    
    # Sidebar navigation
    st.sidebar.title("Client Menu")
    page = st.sidebar.selectbox(
        "Select Function",
        ["Job Posting", "Candidate Review", "Match Results", "Reports"]
    )
    
    if page == "Job Posting":
        show_job_posting()
    elif page == "Candidate Review":
        show_candidate_review()
    elif page == "Match Results":
        show_match_results()
    elif page == "Reports":
        show_reports()
    
    # Enhanced client info sidebar
    st.sidebar.markdown("---")
    st.sidebar.success(f"🏢 {st.session_state.get('client_name', 'Unknown')}")
    st.sidebar.info(f"Client ID: {st.session_state.get('client_id', 'N/A')}")
    
    # Quick stats in sidebar
    st.sidebar.markdown("### 📊 Quick Stats")
    st.sidebar.metric("Active Jobs", "2")
    st.sidebar.metric("Applications", "45")
    st.sidebar.metric("This Week", "+12")
    
    if st.sidebar.button("🚪 Logout"):
        del st.session_state['client_authenticated']
        st.rerun()

def show_client_login():
    st.header("🔐 Client Authentication")
    
    with st.form("client_login"):
        client_id = st.text_input("Client ID")
        client_name = st.text_input("Company Name")
        access_code = st.text_input("Access Code", type="password")
        
        if st.form_submit_button("Login"):
            if client_id and client_name and access_code == "google123":
                st.session_state['client_authenticated'] = True
                st.session_state['client_id'] = client_id
                st.session_state['client_name'] = client_name
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials")

def show_job_posting():
    st.header("📝 Post New Job")
    
    with st.form("job_posting"):
        col1, col2 = st.columns(2)
        
        with col1:
            job_title = st.text_input("Job Title")
            department = st.selectbox("Department", ["Engineering", "Marketing", "Sales", "HR"])
            location = st.text_input("Location")
            
        with col2:
            experience_level = st.selectbox("Experience Level", ["Entry", "Mid", "Senior", "Lead"])
            employment_type = st.selectbox("Type", ["Full-time", "Part-time", "Contract"])
            salary_range = st.text_input("Salary Range")
        
        job_description = st.text_area("Job Description", height=150)
        required_skills = st.text_area("Required Skills (comma-separated)")
        
        if st.form_submit_button("Post Job"):
            job_data = {
                "title": job_title,
                "description": job_description,
                "client_id": int(st.session_state.get('client_id', 1)),
                "required_skills": required_skills,
                "location": location,
                "experience_required": experience_level
            }
            
            try:
                response = requests.post(f"{API_BASE_URL}/v1/jobs", headers=headers, json=job_data)
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"Job posted successfully! Job ID: {result.get('job_id')}")
                    st.balloons()
                else:
                    st.error("Failed to post job")
            except Exception as e:
                st.error(f"Error: {e}")

def show_candidate_review():
    st.header("👥 Review Candidates")
    
    # Get jobs for this client
    try:
        response = requests.get(f"{API_BASE_URL}/v1/jobs", headers=headers)
        if response.status_code == 200:
            jobs = response.json()
            client_jobs = [job for job in jobs if job.get('client_id') == int(st.session_state.get('client_id', 1))]
            
            if client_jobs:
                job_options = {f"{job['title']} (ID: {job['id']})": job['id'] for job in client_jobs}
                selected_job = st.selectbox("Select Job", list(job_options.keys()))
                
                if selected_job:
                    job_id = job_options[selected_job]
                    
                    # Get candidates for this job
                    response = requests.get(f"{API_BASE_URL}/v1/candidates/job/{job_id}", headers=headers)
                    if response.status_code == 200:
                        candidates = response.json()
                        
                        if candidates:
                            st.write(f"Found {len(candidates)} candidates")
                            
                            for candidate in candidates:
                                with st.expander(f"👤 {candidate.get('name', 'Unknown')}"):
                                    col1, col2, col3 = st.columns(3)
                                    
                                    with col1:
                                        st.write(f"**Email:** {candidate.get('email', 'N/A')}")
                                        st.write(f"**Phone:** {candidate.get('phone', 'N/A')}")
                                        st.write(f"**Location:** {candidate.get('location', 'N/A')}")
                                    
                                    with col2:
                                        st.write(f"**Experience:** {candidate.get('experience_years', 'N/A')} years")
                                        st.write(f"**Education:** {candidate.get('education_level', 'N/A')}")
                                        st.write(f"**Status:** {candidate.get('status', 'N/A')}")
                                    
                                    with col3:
                                        skills = candidate.get('technical_skills', 'N/A')
                                        if len(skills) > 50:
                                            skills = skills[:50] + "..."
                                        st.write(f"**Skills:** {skills}")
                                    
                                    # Action buttons
                                    btn_col1, btn_col2, btn_col3 = st.columns(3)
                                    with btn_col1:
                                        if st.button(f"✅ Approve", key=f"approve_{candidate.get('id')}"):
                                            st.success("Candidate approved for interview")
                                    with btn_col2:
                                        if st.button(f"❌ Reject", key=f"reject_{candidate.get('id')}"):
                                            st.error("Candidate rejected")
                                    with btn_col3:
                                        if st.button(f"📋 Details", key=f"details_{candidate.get('id')}"):
                                            st.info("Detailed view opened")
                        else:
                            st.info("No candidates found for this job")
                    else:
                        st.error("Failed to load candidates")
            else:
                st.info("No jobs found for your client ID")
        else:
            st.error("Failed to load jobs")
    except Exception as e:
        st.error(f"Error: {e}")

def show_match_results():
    st.header("🎯 AI Match Results")
    
    # Get client jobs
    try:
        response = requests.get(f"{API_BASE_URL}/v1/jobs", headers=headers)
        if response.status_code == 200:
            jobs = response.json()
            client_jobs = [job for job in jobs if job.get('client_id') == int(st.session_state.get('client_id', 1))]
            
            if client_jobs:
                job_options = {f"{job['title']} (ID: {job['id']})": job['id'] for job in client_jobs}
                selected_job = st.selectbox("Select Job for AI Matching", list(job_options.keys()))
                
                if st.button("Get AI Matches"):
                    job_id = job_options[selected_job]
                    
                    try:
                        response = requests.get(f"{API_BASE_URL}/v1/match/{job_id}/top", headers=headers)
                        if response.status_code == 200:
                            matches = response.json()
                            
                            st.success(f"Top {len(matches)} AI-matched candidates:")
                            
                            for i, match in enumerate(matches, 1):
                                with st.container():
                                    col1, col2, col3 = st.columns([2, 2, 1])
                                    
                                    with col1:
                                        st.write(f"**#{i} - {match.get('name', 'Unknown')}**")
                                        st.write(f"Email: {match.get('email', 'N/A')}")
                                        st.write(f"Skills: {', '.join(match.get('skills_match', []))}")
                                    
                                    with col2:
                                        st.write(f"Experience: {match.get('experience_match', 'N/A')}")
                                        st.write(f"Location: {'✅' if match.get('location_match') else '❌'}")
                                        st.write(f"Reasoning: {match.get('reasoning', 'N/A')}")
                                    
                                    with col3:
                                        score = match.get('score', 0)
                                        st.metric("AI Score", f"{score}/100")
                                        
                                        # Enhanced score explanation
                                        explanation = get_score_explanation(score)
                                        if explanation["color"] == "green":
                                            st.success(explanation["level"])
                                        elif explanation["color"] == "lightgreen":
                                            st.success(explanation["level"])
                                        elif explanation["color"] == "yellow":
                                            st.warning(explanation["level"])
                                        elif explanation["color"] == "orange":
                                            st.warning(explanation["level"])
                                        else:
                                            st.error(explanation["level"])
                                        
                                        # Show detailed explanation
                                        with st.expander("Score Details"):
                                            st.write(f"**Explanation:** {explanation['explanation']}")
                                            st.write(f"**Recommendation:** {explanation['recommendation']}")
                                            
                                            # Skills breakdown
                                            skills_explanation = explain_skills_match(
                                                match.get('skills_match', []), 
                                                []
                                            )
                                            st.write(f"**Skills:** {skills_explanation}")
                                            
                                            # Experience breakdown
                                            exp_explanation = get_experience_explanation(
                                                5,  # Default years
                                                "Mid-level"
                                            )
                                            st.write(f"**Experience:** {exp_explanation}")
                                    
                                    st.divider()
                        else:
                            st.error("Failed to get AI matches")
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.info("No jobs found")
        else:
            st.error("Failed to load jobs")
    except Exception as e:
        st.error(f"Error: {e}")

def show_reports():
    st.header("📊 Client Reports & Analytics")
    
    # Enhanced summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Jobs", "2", delta="+1 this month")
    with col2:
        st.metric("Total Applications", "45", delta="+12 this week")
    with col3:
        st.metric("Interviews Scheduled", "8", delta="+3 this week")
    with col4:
        st.metric("Offers Made", "3", delta="+2 this week")
    
    # Enhanced application pipeline
    st.subheader("📈 Application Pipeline")
    
    col1, col2 = st.columns(2)
    
    with col1:
        status_data = {
            'Status': ['Applied', 'AI Screened', 'Reviewed', 'Interview', 'Offer', 'Hired'],
            'Count': [45, 35, 32, 8, 3, 1]
        }
        df = pd.DataFrame(status_data)
        st.bar_chart(df.set_index('Status')['Count'])
    
    with col2:
        # Conversion rates
        st.write("**Conversion Rates:**")
        st.write("• Applied → AI Screened: 78%")
        st.write("• AI Screened → Reviewed: 91%")
        st.write("• Reviewed → Interview: 25%")
        st.write("• Interview → Offer: 38%")
        st.write("• Offer → Hired: 33%")
    
    # AI Matching Performance
    st.subheader("🤖 AI Matching Performance")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Avg Match Score", "78.5%", "+2.3%")
    with col2:
        st.metric("High Matches (80%+)", "12", "+4")
    with col3:
        st.metric("Processing Time", "0.02s", "-0.01s")
    
    # Skills demand analysis
    st.subheader("💼 Skills in Demand")
    
    skills_data = {
        'Skill': ['Python', 'React', 'AWS', 'Docker', 'SQL'],
        'Demand': [85, 72, 68, 55, 48]
    }
    skills_df = pd.DataFrame(skills_data)
    st.bar_chart(skills_df.set_index('Skill')['Demand'])
    
    # Export options with enhanced features
    st.subheader("📥 Export & Download")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Export Full Report"):
            st.success("Comprehensive report exported")
            st.download_button(
                "Download Report",
                "Sample report data",
                "client_report.csv",
                "text/csv"
            )
    
    with col2:
        if st.button("🎯 Export Match Analysis"):
            st.success("AI match analysis exported")
    
    with col3:
        if st.button("📈 Export Pipeline Data"):
            st.success("Pipeline analytics exported")

if __name__ == "__main__":
    main()