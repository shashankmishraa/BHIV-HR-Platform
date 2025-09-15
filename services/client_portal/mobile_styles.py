"""
Mobile Responsive Styles for BHIV Client Portal
Enterprise-grade responsive design with CSS media queries
"""

import streamlit as st

def inject_mobile_styles():
    """Inject mobile-responsive CSS styles"""
    
    mobile_css = """
    <style>
    /* Mobile-first responsive design */
    @media screen and (max-width: 768px) {
        /* Main container adjustments */
        .main .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            max-width: 100% !important;
        }
        
        /* Header adjustments */
        h1 {
            font-size: 1.5rem !important;
            line-height: 1.2 !important;
        }
        
        h2 {
            font-size: 1.3rem !important;
        }
        
        h3 {
            font-size: 1.1rem !important;
        }
        
        /* Form elements */
        .stTextInput > div > div > input {
            font-size: 16px !important; /* Prevents zoom on iOS */
        }
        
        .stSelectbox > div > div > select {
            font-size: 16px !important;
        }
        
        .stTextArea > div > div > textarea {
            font-size: 16px !important;
        }
        
        /* Button adjustments */
        .stButton > button {
            width: 100% !important;
            margin-bottom: 0.5rem !important;
            font-size: 14px !important;
            padding: 0.5rem 1rem !important;
        }
        
        /* Column layout adjustments */
        .row-widget.stHorizontal {
            flex-direction: column !important;
        }
        
        .row-widget.stHorizontal > div {
            width: 100% !important;
            margin-bottom: 1rem !important;
        }
        
        /* Sidebar adjustments */
        .css-1d391kg {
            width: 100% !important;
        }
        
        /* Metrics adjustments */
        .metric-container {
            margin-bottom: 1rem !important;
        }
        
        /* Expander adjustments */
        .streamlit-expanderHeader {
            font-size: 14px !important;
        }
        
        /* Table adjustments */
        .dataframe {
            font-size: 12px !important;
        }
        
        /* Alert adjustments */
        .stAlert {
            margin-bottom: 1rem !important;
        }
        
        /* Form container */
        .stForm {
            border: none !important;
            padding: 1rem !important;
        }
        
        /* Tab adjustments */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            font-size: 14px !important;
            padding: 0.5rem !important;
        }
    }
    
    /* Tablet adjustments */
    @media screen and (min-width: 769px) and (max-width: 1024px) {
        .main .block-container {
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }
        
        .row-widget.stHorizontal > div {
            min-width: 45% !important;
        }
    }
    
    /* Desktop optimizations */
    @media screen and (min-width: 1025px) {
        .main .block-container {
            max-width: 1200px !important;
        }
    }
    
    /* Touch-friendly improvements */
    @media (hover: none) and (pointer: coarse) {
        .stButton > button {
            min-height: 44px !important; /* Apple's recommended touch target */
        }
        
        .stSelectbox > div > div {
            min-height: 44px !important;
        }
        
        .stCheckbox > label {
            min-height: 44px !important;
            display: flex !important;
            align-items: center !important;
        }
    }
    
    /* Loading spinner adjustments */
    .stSpinner {
        text-align: center !important;
    }
    
    /* Progress bar adjustments */
    .stProgress > div > div {
        height: 8px !important;
    }
    
    /* Custom utility classes */
    .mobile-hidden {
        display: none !important;
    }
    
    @media screen and (min-width: 769px) {
        .mobile-hidden {
            display: block !important;
        }
        
        .desktop-hidden {
            display: none !important;
        }
    }
    
    /* Accessibility improvements */
    .stButton > button:focus {
        outline: 2px solid #0066cc !important;
        outline-offset: 2px !important;
    }
    
    /* High contrast mode support */
    @media (prefers-contrast: high) {
        .stButton > button {
            border: 2px solid currentColor !important;
        }
    }
    
    /* Reduced motion support */
    @media (prefers-reduced-motion: reduce) {
        * {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }
    
    /* Dark mode adjustments */
    @media (prefers-color-scheme: dark) {
        .stApp {
            background-color: #0e1117 !important;
        }
        
        .stButton > button {
            background-color: #262730 !important;
            color: #fafafa !important;
            border: 1px solid #464853 !important;
        }
    }
    </style>
    """
    
    st.markdown(mobile_css, unsafe_allow_html=True)

def add_mobile_navigation():
    """Add mobile-friendly navigation"""
    
    # Mobile navigation menu
    mobile_nav = """
    <style>
    .mobile-nav {
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background: #ffffff;
        border-bottom: 1px solid #e0e0e0;
        z-index: 1000;
        padding: 0.5rem;
    }
    
    @media screen and (max-width: 768px) {
        .mobile-nav {
            display: block;
        }
        
        .main {
            margin-top: 60px;
        }
    }
    
    .mobile-nav-toggle {
        background: none;
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
        float: right;
    }
    
    .mobile-nav-menu {
        display: none;
        position: absolute;
        top: 100%;
        left: 0;
        width: 100%;
        background: #ffffff;
        border-bottom: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .mobile-nav-menu.active {
        display: block;
    }
    
    .mobile-nav-item {
        display: block;
        padding: 1rem;
        text-decoration: none;
        color: #333;
        border-bottom: 1px solid #f0f0f0;
    }
    
    .mobile-nav-item:hover {
        background-color: #f5f5f5;
    }
    </style>
    
    <div class="mobile-nav">
        <span style="font-weight: bold;">🏢 BHIV Client Portal</span>
        <button class="mobile-nav-toggle" onclick="toggleMobileMenu()">☰</button>
        <div class="mobile-nav-menu" id="mobileMenu">
            <a href="#" class="mobile-nav-item" onclick="selectPage('job-posting')">📝 Job Posting</a>
            <a href="#" class="mobile-nav-item" onclick="selectPage('candidate-review')">👥 Candidate Review</a>
            <a href="#" class="mobile-nav-item" onclick="selectPage('match-results')">🎯 Match Results</a>
            <a href="#" class="mobile-nav-item" onclick="selectPage('reports')">📊 Reports</a>
        </div>
    </div>
    
    <script>
    function toggleMobileMenu() {
        const menu = document.getElementById('mobileMenu');
        menu.classList.toggle('active');
    }
    
    function selectPage(page) {
        // This would integrate with Streamlit's page selection
        toggleMobileMenu();
    }
    
    // Close menu when clicking outside
    document.addEventListener('click', function(event) {
        const nav = document.querySelector('.mobile-nav');
        const menu = document.getElementById('mobileMenu');
        if (!nav.contains(event.target)) {
            menu.classList.remove('active');
        }
    });
    </script>
    """
    
    st.markdown(mobile_nav, unsafe_allow_html=True)

def add_responsive_containers():
    """Add responsive container classes"""
    
    container_css = """
    <style>
    /* Responsive container system */
    .responsive-container {
        width: 100%;
        margin: 0 auto;
        padding: 0 1rem;
    }
    
    .responsive-grid {
        display: grid;
        gap: 1rem;
        grid-template-columns: 1fr;
    }
    
    @media screen and (min-width: 576px) {
        .responsive-grid-sm-2 {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    
    @media screen and (min-width: 768px) {
        .responsive-container {
            padding: 0 2rem;
        }
        
        .responsive-grid-md-2 {
            grid-template-columns: repeat(2, 1fr);
        }
        
        .responsive-grid-md-3 {
            grid-template-columns: repeat(3, 1fr);
        }
    }
    
    @media screen and (min-width: 992px) {
        .responsive-grid-lg-4 {
            grid-template-columns: repeat(4, 1fr);
        }
    }
    
    /* Responsive text */
    .text-responsive {
        font-size: clamp(0.875rem, 2.5vw, 1rem);
    }
    
    .heading-responsive {
        font-size: clamp(1.25rem, 4vw, 2rem);
    }
    
    /* Responsive spacing */
    .spacing-responsive {
        margin: clamp(0.5rem, 2vw, 1rem) 0;
    }
    </style>
    """
    
    st.markdown(container_css, unsafe_allow_html=True)

def check_mobile_device():
    """Check if user is on mobile device"""
    
    mobile_check = """
    <script>
    function isMobileDevice() {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    }
    
    function getScreenSize() {
        return {
            width: window.innerWidth,
            height: window.innerHeight,
            isMobile: window.innerWidth <= 768,
            isTablet: window.innerWidth > 768 && window.innerWidth <= 1024,
            isDesktop: window.innerWidth > 1024
        };
    }
    
    // Store device info in session storage
    sessionStorage.setItem('deviceInfo', JSON.stringify({
        isMobileDevice: isMobileDevice(),
        screenSize: getScreenSize()
    }));
    
    // Update on resize
    window.addEventListener('resize', function() {
        sessionStorage.setItem('deviceInfo', JSON.stringify({
            isMobileDevice: isMobileDevice(),
            screenSize: getScreenSize()
        }));
    });
    </script>
    """
    
    st.markdown(mobile_check, unsafe_allow_html=True)