"""
Enterprise-level fixes for BHIV HR Portal issues
"""
import streamlit as st
import time
import threading
from datetime import datetime
import httpx

class PortalEnhancements:
    def __init__(self):
        self.ai_status = "checking"
        self.last_health_check = 0
        self.health_check_interval = 30  # seconds
        
    def init_session_state(self):
        """Initialize session state for URL routing"""
        if 'current_step' not in st.session_state:
            # Get step from URL params
            query_params = st.experimental_get_query_params()
            st.session_state.current_step = query_params.get('step', ['dashboard'])[0]
    
    def update_url_params(self, step):
        """Update URL parameters for deep linking"""
        st.session_state.current_step = step
        st.experimental_set_query_params(step=step)
    
    def check_data_availability(self, data, data_type="candidates"):
        """Check if data is available for visualizations"""
        if not data or (isinstance(data, list) and len(data) == 0):
            return False, f"No {data_type} found"
        if isinstance(data, dict) and data.get('count', 0) == 0:
            return False, f"No {data_type} available"
        return True, "Data available"
    
    def render_empty_state_message(self, message_type="candidates"):
        """Render empty state with actionable message"""
        messages = {
            "candidates": {
                "title": "📊 No Candidates Data",
                "message": "Upload candidates to see visualizations and analytics",
                "action": "Go to 'Step 2: Upload Candidates' to add candidate data"
            },
            "jobs": {
                "title": "💼 No Jobs Data", 
                "message": "Create jobs to see job analytics",
                "action": "Go to 'Step 1: Create Job Positions' to add jobs"
            },
            "assessments": {
                "title": "📋 No Assessment Data",
                "message": "Complete assessments to see values analytics", 
                "action": "Go to 'Step 6: Submit Values Assessment' to add assessments"
            }
        }
        
        msg = messages.get(message_type, messages["candidates"])
        st.info(f"**{msg['title']}**")
        st.write(msg['message'])
        st.caption(f"💡 {msg['action']}")
    
    def create_conditional_button(self, label, data_count, tooltip_message="No data available"):
        """Create button that's disabled when no data"""
        if data_count == 0:
            st.button(label, disabled=True, help=tooltip_message, use_container_width=True)
            return False
        else:
            return st.button(label, use_container_width=True)
    
    def periodic_health_check(self, api_base):
        """Perform periodic health checks in background"""
        current_time = time.time()
        if current_time - self.last_health_check > self.health_check_interval:
            try:
                # Check AI service
                ai_response = httpx.get(f"http://agent:9000/health", timeout=3.0)
                if ai_response.status_code == 200:
                    self.ai_status = "online"
                else:
                    self.ai_status = "limited"
            except:
                self.ai_status = "offline"
            
            self.last_health_check = current_time
    
    def get_ai_status_display(self):
        """Get formatted AI status for display"""
        status_map = {
            "online": "✅ Talah AI: Online",
            "limited": "⚠️ Talah AI: Limited", 
            "offline": "❌ Talah AI: Offline",
            "checking": "🔄 Talah AI: Checking..."
        }
        return status_map.get(self.ai_status, "❓ Talah AI: Unknown")
    
    def validate_api_response(self, response_data, expected_fields=None):
        """Validate API response structure"""
        if not response_data:
            return False, "Empty response"
        
        if expected_fields:
            missing_fields = [field for field in expected_fields if field not in response_data]
            if missing_fields:
                return False, f"Missing fields: {missing_fields}"
        
        return True, "Valid response"
    
    def safe_chart_render(self, chart_data, chart_type="bar", empty_message="No data to display"):
        """Safely render charts with empty state handling"""
        has_data, message = self.check_data_availability(chart_data)
        
        if not has_data:
            self.render_empty_state_message()
            return False
        
        # Render chart based on type
        if chart_type == "bar":
            st.bar_chart(chart_data)
        elif chart_type == "line":
            st.line_chart(chart_data)
        elif chart_type == "area":
            st.area_chart(chart_data)
        
        return True

# Global instance
portal_enhancements = PortalEnhancements()