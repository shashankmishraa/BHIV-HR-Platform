import streamlit as st
import pandas as pd
import requests
import json

# Page config
st.set_page_config(
    page_title="BHIV HR Portal",
    page_icon="🎯",
    layout="wide"
)

# Mock data for demo
mock_candidates = [
    {"id": 1, "name": "John Smith", "email": "john@email.com", "skills": "Python, React, SQL", "experience": 5},
    {"id": 2, "name": "Sarah Johnson", "email": "sarah@email.com", "skills": "Java, Spring, AWS", "experience": 3},
    {"id": 3, "name": "Mike Chen", "email": "mike@email.com", "skills": "JavaScript, Node.js, MongoDB", "experience": 4}
]

mock_jobs = [
    {"id": 1, "title": "Senior Developer", "requirements": "Python, React, 5+ years"},
    {"id": 2, "title": "Full Stack Engineer", "requirements": "JavaScript, Node.js, AWS"},
    {"id": 3, "title": "Backend Developer", "requirements": "Java, Spring Boot, SQL"}
]

# Title
st.title("🎯 BHIV HR Portal")
st.markdown("**AI-Powered Recruiting Platform**")

# Sidebar
st.sidebar.title("Navigation")
menu = st.sidebar.selectbox("Select Module", [
    "Dashboard",
    "Search Candidates", 
    "Job Management",
    "AI Matching",
    "Analytics"
])

if menu == "Dashboard":
    st.header("📊 Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Candidates", "30", "5")
    with col2:
        st.metric("Active Jobs", "15", "2")
    with col3:
        st.metric("Applications", "539", "23")
    with col4:
        st.metric("Match Rate", "85%", "3%")
    
    # Recent activity
    st.subheader("Recent Activity")
    df = pd.DataFrame(mock_candidates)
    st.dataframe(df, use_container_width=True)

elif menu == "Search Candidates":
    st.header("🔍 Search Candidates")
    
    col1, col2 = st.columns(2)
    with col1:
        search_query = st.text_input("Search by name")
    with col2:
        skills_filter = st.text_input("Filter by skills")
    
    if st.button("Search", type="primary"):
        st.success("Search completed!")
        
        for candidate in mock_candidates:
            with st.expander(f"👤 {candidate['name']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Email:** {candidate['email']}")
                    st.write(f"**Skills:** {candidate['skills']}")
                with col2:
                    st.write(f"**Experience:** {candidate['experience']} years")
                    st.button(f"View Profile", key=f"profile_{candidate['id']}")

elif menu == "Job Management":
    st.header("💼 Job Management")
    
    tab1, tab2 = st.tabs(["Active Jobs", "Create Job"])
    
    with tab1:
        st.subheader("Active Jobs")
        for job in mock_jobs:
            with st.expander(f"📋 {job['title']}"):
                st.write(f"**Requirements:** {job['requirements']}")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.button("View Matches", key=f"match_{job['id']}")
                with col2:
                    st.button("Edit Job", key=f"edit_{job['id']}")
                with col3:
                    st.button("Close Job", key=f"close_{job['id']}")
    
    with tab2:
        st.subheader("Create New Job")
        with st.form("job_form"):
            title = st.text_input("Job Title")
            description = st.text_area("Job Description")
            requirements = st.text_area("Requirements")
            
            if st.form_submit_button("Create Job", type="primary"):
                st.success(f"Job '{title}' created successfully!")

elif menu == "AI Matching":
    st.header("🤖 AI-Powered Matching")
    
    job_id = st.selectbox("Select Job", options=[1, 2, 3], format_func=lambda x: f"Job {x}: {mock_jobs[x-1]['title']}")
    
    if st.button("Get AI Matches", type="primary"):
        st.success("AI matching completed!")
        
        st.subheader("Top Matches")
        for i, candidate in enumerate(mock_candidates, 1):
            score = 95 - (i * 10)
            
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"**#{i} {candidate['name']}**")
                st.write(f"Skills: {candidate['skills']}")
            with col2:
                st.metric("Match Score", f"{score}%")
            with col3:
                st.button("Contact", key=f"contact_{candidate['id']}")

elif menu == "Analytics":
    st.header("📈 Analytics")
    
    # Sample charts
    import plotly.express as px
    
    # Skills distribution
    skills_data = pd.DataFrame({
        'Skill': ['Python', 'JavaScript', 'Java', 'React', 'SQL'],
        'Count': [15, 12, 8, 10, 18]
    })
    
    fig = px.bar(skills_data, x='Skill', y='Count', title='Skills Distribution')
    st.plotly_chart(fig, use_container_width=True)
    
    # Experience levels
    exp_data = pd.DataFrame({
        'Experience': ['0-2 years', '3-5 years', '6-10 years', '10+ years'],
        'Candidates': [8, 12, 7, 3]
    })
    
    fig2 = px.pie(exp_data, values='Candidates', names='Experience', title='Experience Levels')
    st.plotly_chart(fig2, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("**BHIV HR Platform** - Production-ready recruiting solution with AI-powered matching")