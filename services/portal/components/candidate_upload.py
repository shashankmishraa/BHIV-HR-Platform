"""Candidate upload component"""

import streamlit as st
import pandas as pd
import httpx

def show_candidate_upload(API_BASE, headers, SECURITY_ENABLED, sanitizer=None):
    """Display candidate upload interface"""
    st.header("Bulk Candidate Upload")
    st.write("Upload multiple candidates for a job position using CSV format")
    
    job_id = st.number_input("Job ID", min_value=1, step=1, value=1)
    
    # Show expected CSV format
    st.subheader("📋 Expected CSV Format")
    example_df = pd.DataFrame({
        'name': ['John Smith', 'Jane Doe', 'Mike Johnson'],
        'email': ['john@example.com', 'jane@example.com', 'mike@example.com'],
        'cv_url': ['https://example.com/john-cv.pdf', 'https://example.com/jane-cv.pdf', 'https://example.com/mike-cv.pdf'],
        'phone': ['+1-555-0101', '+1-555-0102', '+1-555-0103'],
        'experience_years': [5, 3, 7],
        'status': ['applied', 'applied', 'applied']
    })
    st.dataframe(example_df, use_container_width=True)
    
    # File upload
    uploaded_file = st.file_uploader("Choose CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.write("**Preview of uploaded data:**")
            st.dataframe(df, use_container_width=True)
            
            if st.button("📤 Upload Candidates", use_container_width=True):
                # Process and upload to API with enhanced data
                candidates = []
                for _, row in df.iterrows():
                    # Clean and validate data
                    exp_years = row.get("experience_years", 0)
                    try:
                        exp_years = int(float(exp_years)) if pd.notna(exp_years) else 0
                    except (ValueError, TypeError):
                        exp_years = 0
                    
                    candidate = {
                        "name": str(row.get("name", "")).strip(),
                        "email": str(row.get("email", "")).strip(),
                        "cv_url": str(row.get("cv_url", "")).strip(),
                        "phone": str(row.get("phone", "")).strip(),
                        "experience_years": exp_years,
                        "status": str(row.get("status", "applied")).strip(),
                        "job_id": job_id,
                        "location": str(row.get("location", "")).strip(),
                        "technical_skills": str(row.get("skills", "")).strip(),
                        "designation": str(row.get("designation", "")).strip(),
                        "education_level": str(row.get("education", "")).strip()
                    }
                    
                    if SECURITY_ENABLED and sanitizer:
                        candidate = sanitizer.sanitize_dict(candidate)
                    candidates.append(candidate)
                
                try:
                    response = httpx.post(f"{API_BASE}/v1/candidates/bulk", 
                                        json={"candidates": candidates}, 
                                        headers=headers, timeout=10.0)
                    if response.status_code == 200:
                        st.success(f"✅ Successfully uploaded {len(df)} candidates for Job ID: {job_id}")
                        st.info("📊 Candidates are now available for AI matching and assessment")
                        st.balloons()
                    else:
                        st.error(f"❌ Upload failed: {response.text}")
                except Exception as e:
                    st.error(f"❌ Upload error: {str(e)}")
                
        except Exception as e:
            st.error(f"❌ Error reading CSV file: {str(e)}")
            st.info("Please ensure your CSV file follows the expected format shown above")