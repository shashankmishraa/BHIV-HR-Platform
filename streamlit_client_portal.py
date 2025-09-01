import streamlit as st
import pandas as pd

# Page config
st.set_page_config(
    page_title="BHIV Client Portal",
    page_icon="👥",
    layout="wide"
)

# Authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 Client Portal Login")
    
    access_code = st.text_input("Access Code", type="password")
    
    if st.button("Login", type="primary"):
        if access_code == "google123":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Invalid access code")
    
    st.info("Demo access code: **google123**")
    st.stop()

# Main portal
st.title("👥 BHIV Client Portal")
st.markdown("**Secure Client Interface for Job Posting and Candidate Review**")

# Sidebar
st.sidebar.title("Client Menu")
menu = st.sidebar.selectbox("Select Option", [
    "Dashboard",
    "Post Job",
    "View Candidates",
    "Match Results"
])

# Mock data
mock_matches = [
    {"name": "John Smith", "score": 95, "skills": "Python, React, SQL", "experience": 5},
    {"name": "Sarah Johnson", "score": 88, "skills": "Java, Spring, AWS", "experience": 3},
    {"name": "Mike Chen", "score": 82, "skills": "JavaScript, Node.js", "experience": 4}
]

if menu == "Dashboard":
    st.header("📊 Client Dashboard")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Posted Jobs", "3", "1")
    with col2:
        st.metric("Total Candidates", "15", "5")
    with col3:
        st.metric("Avg Match Score", "88%", "2%")
    
    st.subheader("Recent Job Posts")
    jobs_df = pd.DataFrame([
        {"Job Title": "Senior Developer", "Status": "Active", "Candidates": 8},
        {"Job Title": "Full Stack Engineer", "Status": "Active", "Candidates": 5},
        {"Job Title": "Backend Developer", "Status": "Closed", "Candidates": 2}
    ])
    st.dataframe(jobs_df, use_container_width=True)

elif menu == "Post Job":
    st.header("📝 Post New Job")
    
    with st.form("job_posting"):
        col1, col2 = st.columns(2)
        
        with col1:
            job_title = st.text_input("Job Title")
            department = st.selectbox("Department", ["Engineering", "Marketing", "Sales", "HR"])
            location = st.selectbox("Location", ["Remote", "New York", "San Francisco", "London"])
        
        with col2:
            experience_level = st.selectbox("Experience Level", ["Entry", "Mid", "Senior", "Lead"])
            salary_range = st.text_input("Salary Range")
            employment_type = st.selectbox("Employment Type", ["Full-time", "Part-time", "Contract"])
        
        job_description = st.text_area("Job Description", height=150)
        requirements = st.text_area("Requirements", height=100)
        
        if st.form_submit_button("Post Job", type="primary"):
            st.success(f"Job '{job_title}' posted successfully!")
            st.balloons()

elif menu == "View Candidates":
    st.header("👤 Candidate Pool")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        skill_filter = st.selectbox("Filter by Skill", ["All", "Python", "JavaScript", "Java"])
    with col2:
        exp_filter = st.selectbox("Experience", ["All", "0-2 years", "3-5 years", "6+ years"])
    with col3:
        location_filter = st.selectbox("Location", ["All", "Remote", "New York", "San Francisco"])
    
    st.subheader("Available Candidates")
    
    for candidate in mock_matches:
        with st.expander(f"👤 {candidate['name']} - Match Score: {candidate['score']}%"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Skills:** {candidate['skills']}")
                st.write(f"**Experience:** {candidate['experience']} years")
                
                # Progress bar for match score
                st.progress(candidate['score']/100)
            
            with col2:
                st.write("**Match Analysis:**")
                st.write("✅ Strong technical skills alignment")
                st.write("✅ Experience level matches requirements")
                st.write("✅ Available for immediate start")
                
                if st.button(f"Request Interview", key=f"interview_{candidate['name']}"):
                    st.success("Interview request sent!")

elif menu == "Match Results":
    st.header("🎯 AI Match Results")
    
    job_selection = st.selectbox("Select Job", [
        "Senior Developer Position",
        "Full Stack Engineer Role", 
        "Backend Developer Opening"
    ])
    
    st.subheader(f"Top Matches for: {job_selection}")
    
    for i, candidate in enumerate(mock_matches, 1):
        with st.container():
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            
            with col1:
                st.write(f"**#{i} {candidate['name']}**")
                st.write(f"Skills: {candidate['skills']}")
            
            with col2:
                st.metric("Match Score", f"{candidate['score']}%")
            
            with col3:
                st.write(f"**{candidate['experience']} years**")
                st.write("Experience")
            
            with col4:
                if st.button("Contact", key=f"contact_{i}"):
                    st.success("Contact request sent!")
            
            st.markdown("---")

# Logout
if st.sidebar.button("Logout"):
    st.session_state.authenticated = False
    st.rerun()

# Footer
st.markdown("---")
st.markdown("**BHIV Client Portal** - Secure access to top talent with AI-powered matching")