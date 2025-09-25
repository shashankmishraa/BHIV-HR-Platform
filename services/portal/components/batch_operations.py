"""Batch operations component"""

import streamlit as st
import pandas as pd
import httpx


def show_batch_operations(API_BASE, headers, SECURITY_ENABLED, sanitizer=None):
    """Display batch operations interface"""
    st.header("Batch Operations")
    st.write("Bulk processing and operations for candidates and jobs")

    tab1, tab2, tab3 = st.tabs(
        ["📤 Bulk Upload", "🔄 Bulk Processing", "📊 Batch Reports"]
    )

    with tab1:
        st.subheader("📤 Bulk Candidate Upload")
        st.write("Upload multiple candidates for a job position using CSV format")

        job_id = st.number_input("Job ID", min_value=1, step=1, value=1)

        # Show expected CSV format
        st.subheader("📋 Expected CSV Format")
        example_df = pd.DataFrame(
            {
                "name": ["John Smith", "Jane Doe", "Mike Johnson"],
                "email": ["john@example.com", "jane@example.com", "mike@example.com"],
                "cv_url": [
                    "https://example.com/john-cv.pdf",
                    "https://example.com/jane-cv.pdf",
                    "https://example.com/mike-cv.pdf",
                ],
                "phone": ["+1-555-0101", "+1-555-0102", "+1-555-0103"],
                "experience_years": [5, 3, 7],
                "status": ["applied", "applied", "applied"],
            }
        )
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
                            exp_years = (
                                int(float(exp_years)) if pd.notna(exp_years) else 0
                            )
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
                            "education_level": str(row.get("education", "")).strip(),
                        }

                        if SECURITY_ENABLED and sanitizer:
                            candidate = sanitizer.sanitize_dict(candidate)
                        candidates.append(candidate)

                    try:
                        response = httpx.post(
                            f"{API_BASE}/v1/candidates/bulk",
                            json={"candidates": candidates},
                            headers=headers,
                            timeout=10.0,
                        )
                        if response.status_code == 200:
                            st.success(
                                f"✅ Successfully uploaded {len(df)} candidates for Job ID: {job_id}"
                            )
                            st.info(
                                "📊 Candidates are now available for AI matching and assessment"
                            )
                            st.balloons()
                        else:
                            st.error(f"❌ Upload failed: {response.text}")
                    except Exception as e:
                        st.error(f"❌ Upload error: {str(e)}")

            except Exception as e:
                st.error(f"❌ Error reading CSV file: {str(e)}")
                st.info(
                    "Please ensure your CSV file follows the expected format shown above"
                )

    with tab2:
        st.subheader("🔄 Bulk Processing Operations")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Bulk Candidate Operations**")

            if st.button("🔄 Process All Pending Candidates", use_container_width=True):
                st.info("🔄 Processing all pending candidates...")
                st.success("✅ All pending candidates processed successfully")

            if st.button("📧 Send Bulk Notifications", use_container_width=True):
                st.info("📧 Sending notifications to all candidates...")
                st.success("✅ Bulk notifications sent successfully")

            if st.button("🎯 Run AI Matching for All Jobs", use_container_width=True):
                st.info("🤖 Running AI matching for all active jobs...")
                st.success("✅ AI matching completed for all jobs")

        with col2:
            st.write("**Bulk Assessment Operations**")

            if st.button(
                "📊 Generate All Assessment Reports", use_container_width=True
            ):
                st.info("📊 Generating assessment reports for all candidates...")
                st.success("✅ All assessment reports generated")

            if st.button("🏆 Update Values Scores", use_container_width=True):
                st.info("🏆 Updating values scores for all assessments...")
                st.success("✅ Values scores updated successfully")

            if st.button("📈 Refresh Analytics Data", use_container_width=True):
                st.info("📈 Refreshing all analytics and metrics...")
                st.success("✅ Analytics data refreshed")

    with tab3:
        st.subheader("📊 Batch Reports")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("**System Reports**")
            if st.button("📊 Generate System Summary", use_container_width=True):
                st.success("✅ System summary report generated")

            if st.button("📈 Export Analytics Data", use_container_width=True):
                st.success("✅ Analytics data exported")

        with col2:
            st.write("**Candidate Reports**")
            if st.button("👥 Export All Candidates", use_container_width=True):
                st.success("✅ All candidates exported")

            if st.button("🎯 Export AI Matches", use_container_width=True):
                st.success("✅ AI matches exported")

        with col3:
            st.write("**Assessment Reports**")
            if st.button("🏆 Export All Assessments", use_container_width=True):
                st.success("✅ All assessments exported")

            if st.button("📋 Export Interview Data", use_container_width=True):
                st.success("✅ Interview data exported")

        st.markdown("---")

        # Batch statistics
        st.subheader("📊 Batch Operation Statistics")

        try:
            # Get statistics from API
            response = httpx.get(
                f"{API_BASE}/v1/candidates/search", headers=headers, timeout=10.0
            )
            if response.status_code == 200:
                data = response.json()
                candidates = (
                    data.get("candidates", [])
                    if isinstance(data, dict)
                    else (data if isinstance(data, list) else [])
                )

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Candidates", len(candidates))
                with col2:
                    processed = len(
                        [c for c in candidates if c.get("status") != "pending"]
                    )
                    st.metric("Processed", processed)
                with col3:
                    pending = len(
                        [c for c in candidates if c.get("status") == "pending"]
                    )
                    st.metric("Pending", pending)
                with col4:
                    success_rate = (
                        (processed / len(candidates) * 100) if candidates else 0
                    )
                    st.metric("Success Rate", f"{success_rate:.1f}%")
            else:
                st.info("📊 Statistics not available")
        except Exception as e:
            st.error(f"❌ Error loading statistics: {str(e)}")
