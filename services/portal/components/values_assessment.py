"""Values assessment component"""

import streamlit as st
import pandas as pd
from datetime import datetime

def show_values_assessment():
    """Display values-based candidate assessment"""
    st.header("Values-Based Candidate Assessment")
    st.write("Assess candidates on our core organizational values")
    
    with st.form("feedback_form"):
        # Candidate Information
        st.subheader("📋 Candidate Information")
        col1, col2 = st.columns(2)
        
        with col1:
            candidate_name = st.text_input("Candidate Name", placeholder="Full name of the candidate")
            candidate_id = st.number_input("Candidate ID", min_value=1, step=1)
            job_title = st.text_input("Applied Position", placeholder="Position they applied for")
        
        with col2:
            reviewer_name = st.text_input("Reviewer Name", placeholder="Your full name")
            job_id = st.number_input("Job ID", min_value=1, step=1)
            interview_date = st.date_input("Interview Date")
        
        # Detailed Feedback
        st.subheader("📝 Interview Feedback")
        feedback_text = st.text_area("Detailed Feedback", placeholder="Provide comprehensive feedback about the candidate's performance, technical skills, communication, and overall fit...")
        
        # Values Assessment
        st.subheader("🏆 Values Assessment (1-5 scale)")
        st.write("Rate the candidate on each of our core organizational values:")
        
        values = {}
        value_descriptions = {
            "Integrity": "🔸 Moral uprightness, ethical behavior, and honesty in all actions",
            "Honesty": "🔸 Truthfulness, transparency, and sincerity in communication",
            "Discipline": "🔸 Self-control, consistency, and commitment to excellence",
            "Hard Work": "🔸 Dedication, perseverance, and going above and beyond expectations",
            "Gratitude": "🔸 Appreciation, humility, and recognition of others' contributions"
        }
        
        col1, col2 = st.columns(2)
        value_items = list(value_descriptions.items())
        
        for i, (value, description) in enumerate(value_items):
            if i < 3:
                with col1:
                    st.write(f"**{value}**")
                    st.caption(description)
                    values[value] = st.slider(f"{value}", 1, 5, 3, key=f"val_{i}")
                    st.markdown("---")
            else:
                with col2:
                    st.write(f"**{value}**")
                    st.caption(description)
                    values[value] = st.slider(f"{value}", 1, 5, 3, key=f"val_{i}")
                    st.markdown("---")
        
        # Overall Assessment
        st.subheader("📊 Overall Assessment")
        overall_recommendation = st.selectbox("Overall Recommendation", 
            ["Strongly Recommend", "Recommend", "Neutral", "Do Not Recommend", "Strongly Do Not Recommend"])
        
        submitted = st.form_submit_button("📤 Submit Assessment", use_container_width=True)
        
        if submitted and reviewer_name and candidate_name and feedback_text:
            # Calculate metrics
            avg_score = sum(values.values()) / len(values)
            top_value = max(values, key=values.get)
            lowest_value = min(values, key=values.get)
            
            st.success("✅ Values assessment submitted successfully!")
            
            # Display results
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Average Values Score", f"{avg_score:.1f}/5")
            with col2:
                st.metric("Highest Value", f"{top_value}")
                st.caption(f"Score: {values[top_value]}/5")
            with col3:
                st.metric("Development Area", f"{lowest_value}")
                st.caption(f"Score: {values[lowest_value]}/5")
            with col4:
                st.metric("Recommendation", overall_recommendation)
            
            # Values breakdown
            st.subheader("📊 Values Breakdown")
            values_df = pd.DataFrame([values]).T
            values_df.columns = ['Score']
            st.bar_chart(values_df)
            
            st.balloons()
        elif submitted:
            st.warning("⚠️ Please fill in all required fields")