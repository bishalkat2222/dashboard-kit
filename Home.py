import streamlit as st
from auth import login_page

# Page config
st.set_page_config(
    page_title="YouTube Analytics Platform",
    page_icon="📊",
    layout="wide",
)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Navigation buttons
col1, col2, col3 = st.columns([6,1,1])
with col1:
    st.write("")  # Empty space
with col2:
    if st.button("Sign Up"):
        st.switch_page("pages/Signup.py")
with col3:
    if st.button("Sign In"):
        st.switch_page("pages/Login.py")

# Hero Section
st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <h1 style='font-size: 3.5rem;'>YouTube Analytics Platform</h1>
        <p style='font-size: 1.5rem; color: #666;'>
            Transform Your Channel's Performance with Advanced Analytics
        </p>
    </div>
""", unsafe_allow_html=True)

# Main Features Section
st.markdown("## 🚀 Key Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 📊 Comprehensive Analytics
    - Real-time performance tracking
    - Advanced metric visualization
    - Custom date range analysis
    - Trend identification
    """)

with col2:
    st.markdown("""
    ### 📈 Growth Insights
    - Subscriber growth tracking
    - Engagement rate analysis
    - Performance predictions
    - Goal setting and tracking
    """)

with col3:
    st.markdown("""
    ### 🎯 Strategic Tools
    - Content performance metrics
    - Audience behavior analysis
    - Statistical analysis
    - Seasonal pattern detection
    """)

# How It Works Section
st.markdown("## 🔄 How It Works")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    ### 1. Sign Up
    Create your account in minutes and connect your YouTube channel
    """)

with col2:
    st.markdown("""
    ### 2. Import Data
    Automatically sync your YouTube channel data
    """)

with col3:
    st.markdown("""
    ### 3. Analyze
    Get instant insights about your channel's performance
    """)

with col4:
    st.markdown("""
    ### 4. Optimize
    Make data-driven decisions to grow your channel
    """)

# Benefits Section
st.markdown("## 💪 Why Choose Us")

benefits = st.columns(2)

with benefits[0]:
    st.markdown("""
    ### For Content Creators
    - Track your channel's growth
    - Understand your audience
    - Optimize upload timing
    - Monitor engagement metrics
    - Set and track goals
    """)

with benefits[1]:
    st.markdown("""
    ### For Businesses
    - Brand performance tracking
    - Competitor analysis
    - ROI measurement
    - Content strategy insights
    - Team collaboration tools
    """)

# Call to Action
st.markdown("""
    <div style='text-align: center; padding: 2rem; background-color: #f0f2f6; border-radius: 10px; margin: 2rem 0;'>
        <h2>Ready to Transform Your YouTube Channel?</h2>
        <p style='font-size: 1.2rem; color: #666;'>Join thousands of content creators who are growing their channels with data-driven insights.</p>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([2,1,2])
with col2:
    if st.button("Get Started", type="primary", use_container_width=True):
        st.switch_page("pages/Signup.py")

# Footer
st.markdown("""
    <div style='text-align: center; padding: 2rem; color: #666;'>
        <p>© 2024 YouTube Analytics Platform. All rights reserved.</p>
    </div>
""", unsafe_allow_html=True) 