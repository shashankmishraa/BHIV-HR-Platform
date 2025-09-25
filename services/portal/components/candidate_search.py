"""Candidate search and filtering component"""

import streamlit as st
import httpx

def show_candidate_search(API_BASE, headers, SECURITY_ENABLED, sql_guard=None):
    """Display advanced candidate search and filtering"""
    st.header("Advanced Candidate Search & Filtering")
    st.write("Search and filter candidates using AI-powered semantic search and advanced filters")
    
    # Search and filter controls
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_query = st.text_input("🔍 Search Candidates", placeholder="Search by name, skills, experience, location...")
    
    with col2:
        job_filter = st.selectbox("Filter by Job", ["All Jobs", "Job ID 1 - Software Engineer", "Job ID 2 - AI/ML Intern"])
    
    # Advanced filters
    st.subheader("🔧 Advanced Filters")
    
    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)
    
    with filter_col1:
        experience_filter = st.selectbox("Experience Level", ["Any", "0-2 years", "2-5 years", "5+ years"])
        seniority_filter = st.multiselect("Seniority Level", ["Entry-level", "Mid-level", "Senior", "Lead"], default=[])
    
    with filter_col2:
        education_filter = st.multiselect("Education Level", ["Bachelors", "Masters", "PhD", "Diploma"], default=[])
        location_filter = st.multiselect("Location", ["Mumbai", "Bangalore", "Delhi", "Pune", "Chennai", "Remote"], default=[])
    
    with filter_col3:
        skills_filter = st.multiselect("Technical Skills", ["Python", "JavaScript", "Java", "React", "AWS", "Docker", "SQL"], default=[])
        values_filter = st.slider("Minimum Values Score", 1.0, 5.0, 3.0, 0.1)
    
    with filter_col4:
        status_filter = st.multiselect("Candidate Status", ["Applied", "Screened", "Interviewed", "Offered", "Hired"], default=["Applied"])
        sort_by = st.selectbox("Sort By", ["AI Score (High to Low)", "Experience (High to Low)", "Values Score (High to Low)", "Name (A-Z)"])
    
    # Search button
    search_clicked = st.button("🔍 Search Candidates", use_container_width=True)
    
    # Show default message when page loads
    if not search_clicked:
        st.info("👆 Enter search criteria and click 'Search Candidates' to find candidates")
    
    if search_clicked:
        # Check if any meaningful search criteria is provided
        has_criteria = (
            search_query.strip() or 
            skills_filter or 
            location_filter or 
            seniority_filter or 
            education_filter or 
            experience_filter != "Any"
        )
        
        if not has_criteria:
            st.warning("⚠️ Please enter search criteria (name, skills, location, etc.) to search for candidates.")
            st.info("💡 Try searching by name, selecting skills, or choosing location filters.")
        else:
            with st.spinner("🔄 Searching candidates with real API..."):
                try:
                    # Build and validate search parameters
                    params = {"job_id": 1}
                    if search_query.strip():
                        params["q"] = search_query.strip()
                    if skills_filter:
                        params["skills"] = ",".join(skills_filter)
                    if location_filter:
                        params["location"] = ",".join(location_filter)
                    if experience_filter != "Any":
                        if "0-2" in experience_filter:
                            params["experience_min"] = 0
                        elif "2-5" in experience_filter:
                            params["experience_min"] = 2
                        elif "5+" in experience_filter:
                            params["experience_min"] = 5
                    
                    # Validate against SQL injection
                    if SECURITY_ENABLED and sql_guard:
                        params = sql_guard.validate_search_params(params)
                    
                    # Make API call
                    response = httpx.get(f"{API_BASE}/v1/candidates/search", 
                                       params=params, 
                                       headers=headers, 
                                       timeout=10.0)
                    
                    if response.status_code == 200:
                        data = response.json()
                        candidates = data.get("candidates", [])
                        count = data.get("count", 0)
                        
                        st.success(f"✅ Found {count} candidates matching your criteria")
                        
                        if candidates:
                            for candidate in candidates:
                                with st.expander(f"👥 {candidate['name']} - Experience: {candidate['experience_years']} years"):
                                    col1, col2, col3 = st.columns(3)
                                    
                                    with col1:
                                        st.write(f"**Email:** {candidate['email']}")
                                        st.write(f"**Phone:** {candidate['phone']}")
                                        st.write(f"**Location:** {candidate['location']}")
                                    
                                    with col2:
                                        st.write(f"**Experience:** {candidate['experience_years']} years")
                                        st.write(f"**Seniority:** {candidate['seniority_level']}")
                                        st.write(f"**Status:** {candidate['status']}")
                                    
                                    with col3:
                                        st.write("**Technical Skills:**")
                                        st.write(candidate['technical_skills'])
                        else:
                            st.warning("⚠️ No candidates match your search criteria.")
                    else:
                        st.error(f"❌ Search failed: {response.text}")
                        
                except Exception as e:
                    st.error(f"❌ Search error: {str(e)}")