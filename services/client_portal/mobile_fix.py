"""
Mobile Responsiveness Fix for BHIV Client Portal
Minimal, effective CSS for mobile devices
"""

import streamlit as st

def apply_mobile_fixes():
    """Apply essential mobile responsiveness fixes"""
    
    mobile_css = """
    <style>
    /* Mobile responsiveness fixes */
    @media screen and (max-width: 768px) {
        .main .block-container {
            padding: 1rem !important;
            max-width: 100% !important;
        }
        
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select {
            font-size: 16px !important; /* Prevents iOS zoom */
        }
        
        .stButton > button {
            width: 100% !important;
            min-height: 44px !important; /* Touch-friendly */
            margin-bottom: 0.5rem !important;
        }
        
        .row-widget.stHorizontal {
            flex-direction: column !important;
        }
        
        .row-widget.stHorizontal > div {
            width: 100% !important;
            margin-bottom: 1rem !important;
        }
        
        /* Form improvements */
        .stForm {
            padding: 1rem !important;
        }
        
        /* Sidebar on mobile */
        .css-1d391kg {
            width: 100% !important;
        }
        
        /* Expander improvements */
        .streamlit-expanderHeader {
            font-size: 14px !important;
            padding: 0.5rem !important;
        }
        
        /* Metric containers */
        .metric-container {
            margin-bottom: 1rem !important;
        }
    }
    
    /* Tablet adjustments */
    @media screen and (min-width: 769px) and (max-width: 1024px) {
        .main .block-container {
            padding: 2rem !important;
        }
    }
    </style>
    """
    
    st.markdown(mobile_css, unsafe_allow_html=True)