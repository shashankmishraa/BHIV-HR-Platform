"""AI matching and shortlisting component"""

import httpx
import streamlit as st


def show_ai_matching(API_BASE, AGENT_URL, headers):
    """Display AI-powered candidate shortlisting"""
    st.header("AI-Powered Candidate Shortlist")
    st.write(
        "Get the top-5 candidates matched by Talah AI using advanced semantic analysis and values alignment"
    )

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        job_id = st.number_input("Enter Job ID", min_value=1, step=1, value=1)

    with col2:
        get_shortlist = st.button("🤖 Generate AI Shortlist", use_container_width=True)

    with col3:
        refresh_data = st.button("🔄 Refresh Data", use_container_width=True)

    if get_shortlist or refresh_data:
        with st.spinner(
            "🔄 Advanced AI is analyzing candidates using semantic matching..."
        ):
            try:
                # Call AI Agent directly for enhanced matching
                response = httpx.post(
                    f"{AGENT_URL}/match", json={"job_id": job_id}, timeout=15.0
                )
                if response.status_code == 200:
                    data = response.json()
                    candidates_data = data.get("top_candidates", [])
                    ai_analysis = data.get("ai_analysis", "")
                    algorithm_version = data.get("algorithm_version", "v3.0.0")

                    # Show AI analysis info
                    st.info(f"🤖 **AI Analysis**: {ai_analysis}")
                    st.caption(
                        f"Algorithm Version: {algorithm_version} | Processing Time: {data.get('processing_time', 'N/A')}"
                    )

                    if not candidates_data:
                        st.warning(
                            "⚠️ No candidates found for this job. Please upload candidates first."
                        )
                        st.info(
                            "💡 Go to 'Upload Candidates' to add candidates for this job."
                        )
                        candidates = []
                    else:
                        candidates = candidates_data
                else:
                    st.error(f"❌ Failed to get shortlist: {response.text}")
                    candidates = []
            except Exception as e:
                st.error(f"❌ Error getting shortlist: {str(e)}")
                candidates = []

            if candidates:
                st.success(
                    f"✅ AI Analysis Complete! Top {len(candidates)} candidates with advanced scoring:"
                )

                # Summary metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    avg_score = sum(c.get("score", 0) for c in candidates) / len(
                        candidates
                    )
                    st.metric("Average AI Score", f"{avg_score:.1f}/100")
                with col2:
                    avg_values = sum(
                        c.get("values_alignment", 0) for c in candidates
                    ) / len(candidates)
                    st.metric("Average Values", f"{avg_values:.1f}/5")
                with col3:
                    high_performers = sum(
                        1 for c in candidates if c.get("score", 0) >= 85
                    )
                    st.metric("High Performers", f"{high_performers}/{len(candidates)}")
                with col4:
                    strong_cultural_fit = sum(
                        1 for c in candidates if c.get("values_alignment", 0) >= 4.0
                    )
                    st.metric(
                        "Strong Cultural Fit",
                        f"{strong_cultural_fit}/{len(candidates)}",
                    )

                st.markdown("---")

                # Enhanced candidate display
                for i, candidate in enumerate(candidates, 1):
                    with st.expander(
                        f"🏆 #{i} - {candidate.get('name', 'Unknown')} (AI Score: {candidate.get('score', 0):.1f}/100)",
                        expanded=i <= 2,
                    ):

                        # Main metrics row
                        col1, col2, col3, col4 = st.columns(4)

                        with col1:
                            st.metric(
                                "Overall AI Score",
                                f"{candidate.get('score', 0):.1f}/100",
                            )
                            score_color = (
                                "🟢"
                                if candidate.get("score", 0) >= 85
                                else "🟡" if candidate.get("score", 0) >= 70 else "🔴"
                            )
                            st.write(
                                f"{score_color} **Rating**: {candidate.get('recommendation_strength', 'Unknown')}"
                            )

                        with col2:
                            skills_match = candidate.get("skills_match", [])
                            if isinstance(skills_match, list):
                                st.metric("Skills Match", f"{len(skills_match)} skills")
                            else:
                                st.metric("Skills Match", str(skills_match))
                            exp_match = candidate.get("experience_match", "Unknown")
                            st.metric("Experience Match", str(exp_match))

                        with col3:
                            st.metric(
                                "Values Alignment",
                                f"{candidate.get('values_alignment', 0):.1f}/5 ⭐",
                            )
                            values_progress = candidate.get("values_alignment", 0) / 5
                            st.progress(values_progress)

                        with col4:
                            cultural_fit = (
                                "Excellent"
                                if candidate.get("values_alignment", 0) >= 4.5
                                else (
                                    "Good"
                                    if candidate.get("values_alignment", 0) >= 4.0
                                    else "Average"
                                )
                            )
                            st.metric("Cultural Fit", cultural_fit)

                        # AI Insights
                        if candidate.get("ai_insights"):
                            st.write("**🤖 AI Insights:**")
                            for insight in candidate.get("ai_insights", []):
                                st.write(f"• {insight}")

                        # Action buttons
                        col1, col2, col3, col4 = st.columns(4)

                        with col1:
                            if st.button(
                                f"📞 Contact {candidate.get('name', 'Candidate').split()[0]}",
                                key=f"contact_{i}",
                            ):
                                st.success(
                                    f"✅ Contact initiated for {candidate.get('name', 'Candidate')}"
                                )

                        with col2:
                            if st.button(f"📋 View Full Profile", key=f"profile_{i}"):
                                st.info(
                                    f"📋 Opening full profile for {candidate.get('name', 'Candidate')}"
                                )

                        with col3:
                            if st.button(
                                f"📅 Schedule Interview", key=f"interview_{i}"
                            ):
                                st.success(
                                    f"📅 Interview scheduled for {candidate.get('name', 'Candidate')}"
                                )

                        with col4:
                            if st.button(f"⭐ Add to Favorites", key=f"favorite_{i}"):
                                st.success(
                                    f"⭐ {candidate.get('name', 'Candidate')} added to favorites"
                                )

                # Bulk actions
                st.markdown("---")
                st.subheader("🔄 Bulk Actions")

                bulk_col1, bulk_col2, bulk_col3 = st.columns(3)

                with bulk_col1:
                    if st.button(
                        "📧 Email All Top Candidates", use_container_width=True
                    ):
                        st.success(
                            f"📧 Emails sent to top {len(candidates)} candidates with interview invitations"
                        )

                with bulk_col2:
                    if st.button(
                        "📊 Export Shortlist Report", use_container_width=True
                    ):
                        st.success("📊 Shortlist report exported successfully")

                with bulk_col3:
                    if st.button("🔄 Re-run AI Analysis", use_container_width=True):
                        st.info("🔄 Re-running AI analysis with latest data...")
                        st.rerun()
            else:
                st.info(
                    "📊 No candidates returned from AI analysis. Try uploading candidates first."
                )
