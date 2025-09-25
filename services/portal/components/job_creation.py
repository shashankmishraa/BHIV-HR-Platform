"""Job creation component for BHIV HR Portal"""

import streamlit as st
import httpx
from datetime import datetime

def show_job_creation(API_BASE, headers, SECURITY_ENABLED, sanitizer=None, form_limiter=None):
    """Display job creation form"""
    st.header("Create New Job Position")
    
    with st.form("job_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Job Title", placeholder="e.g., Senior Software Engineer")
            department = st.selectbox("Department", ["Engineering", "Marketing", "Sales", "HR", "Operations"])
            location = st.text_input("Location", placeholder="e.g., Remote, New York, London")
        
        with col2:
            experience_level = st.selectbox("Experience Level", ["Entry-level", "Mid-level", "Senior-level", "Lead-level", "Executive-level"])
            employment_type = st.selectbox("Employment Type", ["Full-time", "Part-time", "Contract", "Intern"])
            client_id = st.number_input("Client ID", min_value=1, step=1, value=1)
        
        # Salary fields (required)
        st.subheader("💰 Salary Information (Required)")
        sal_col1, sal_col2 = st.columns(2)
        with sal_col1:
            salary_min = st.number_input("Minimum Salary ($)", min_value=0, max_value=10000000, value=50000, step=5000)
        with sal_col2:
            salary_max = st.number_input("Maximum Salary ($)", min_value=0, max_value=10000000, value=80000, step=5000)
        
        description = st.text_area("Job Description", placeholder="Describe the role, responsibilities, and requirements...")
        requirements = st.text_area("Key Requirements", placeholder="List the essential skills, experience, and qualifications...")
        
        submitted = st.form_submit_button("🚀 Create Job", use_container_width=True)
        
        if submitted and title and description:
            # Rate limiting protection
            session_id = st.session_state.get('session_id', 'anonymous')
            if SECURITY_ENABLED and form_limiter and not form_limiter.is_allowed(session_id):
                st.error("⚠️ Too many requests. Please wait before submitting again.")
            else:
                # Validate salary range
                if salary_max < salary_min:
                    st.error("❌ Maximum salary must be greater than or equal to minimum salary")
                    st.stop()
                
                # Prepare job data with proper validation
                job_data = {
                    "title": title.strip(),
                    "department": department,
                    "location": location.strip(),
                    "experience_level": experience_level,
                    "requirements": requirements.strip(),
                    "description": description.strip(),
                    "salary_min": int(salary_min),
                    "salary_max": int(salary_max),
                    "job_type": employment_type,
                    "company_id": str(client_id)
                }
                
                if SECURITY_ENABLED and sanitizer:
                    job_data = sanitizer.sanitize_dict(job_data)
            
                try:
                    response = httpx.post(f"{API_BASE}/v1/jobs", 
                                        json=job_data, 
                                        headers=headers, timeout=10.0)
                    if response.status_code == 200:
                        result = response.json()
                        job_id = result.get("job_id", "Unknown")
                        
                        display_data = {
                            "job_id": job_id,
                            "title": title,
                            "department": department,
                            "location": location,
                            "experience_level": experience_level,
                            "employment_type": employment_type,
                            "description": description,
                            "requirements": requirements,
                            "client_id": client_id,
                            "status": "active",
                            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        
                        st.success(f"✅ Job created successfully! Job ID: {job_id}")
                        st.json(display_data)
                        st.balloons()
                    else:
                        st.error(f"❌ Job creation failed: {response.text}")
                except Exception as e:
                    st.error(f"❌ Error creating job: {str(e)}")
        elif submitted:
            st.warning("⚠️ Please fill in all required fields")