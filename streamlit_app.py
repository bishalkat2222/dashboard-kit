import streamlit as st
from auth import login_page

# Page config
st.set_page_config(
    page_title="YouTube Analytics Platform",
    page_icon="📊",
    layout="wide",
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem;
    }
    .stButton>button {
        background-color: #FF0000;
        color: white;
        border-radius: 20px;
        padding: 0.5rem 2rem;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #CC0000;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .hero-text {
        font-size: 4rem;
        font-weight: 700;
        background: linear-gradient(45deg, #FF0000, #FF6B6B);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .feature-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
        transition: transform 0.3s ease;
    }
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    /* Dark theme adjustments */
    .stApp {
        background-color: #0E1117;
    }
    
    /* Enhanced feature cards */
    .feature-card {
        background-color: #1E2329;
        color: #E6E6E6;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        margin: 1rem 0;
        transition: all 0.3s ease;
        border: 1px solid #2E3338;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 20px rgba(0,0,0,0.3);
        border-color: #FF0000;
    }
    .feature-card h3 {
        color: #FF0000;
        margin-bottom: 1rem;
    }
    .feature-card ul {
        list-style-type: none;
        padding-left: 0;
    }
    .feature-card li {
        margin: 0.8rem 0;
        padding-left: 1.5rem;
        position: relative;
    }
    .feature-card li:before {
        content: "→";
        color: #FF0000;
        position: absolute;
        left: 0;
    }
    
    /* Enhanced buttons */
    .stButton>button {
        background: linear-gradient(45deg, #FF0000, #FF6B6B);
        color: white;
        border-radius: 25px;
        padding: 0.6rem 2.5rem;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(45deg, #CC0000, #FF4444);
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(255,0,0,0.2);
    }
    
    /* Enhanced hero section */
    .hero-text {
        font-size: 4.5rem;
        font-weight: 800;
        background: linear-gradient(45deg, #FF0000, #FF6B6B);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
    
    /* Steps section */
    .step-card {
        background-color: #1E2329;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #2E3338;
        transition: all 0.3s ease;
    }
    .step-card:hover {
        transform: translateY(-3px);
        border-color: #FF0000;
    }
    .step-number {
        font-size: 2rem;
        font-weight: 700;
        color: #FF0000;
        margin-bottom: 0.5rem;
    }
    
    /* Call to action section */
    .cta-section {
        background: linear-gradient(135deg, #1E2329, #2E3338);
        padding: 3rem;
        border-radius: 20px;
        margin: 3rem 0;
        border: 1px solid #FF0000;
    }
    
    /* Footer */
    .footer {
        border-top: 1px solid #2E3338;
        margin-top: 3rem;
        padding: 2rem 0;
        color: #888;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Navigation buttons - replace the current navigation section with this:
st.markdown("""
    <div style='position: absolute; right: 20px; top: 20px; display: flex; gap: 10px;'>
        <a href="Signup" target="_self" style='
            text-decoration: none;
            color: white;
            background: transparent;
            padding: 8px 25px;
            border: 2px solid #FF0000;
            border-radius: 25px;
            font-weight: 600;
            transition: all 0.3s ease;
            display: inline-block;
            hover: {
                background: #FF0000;
                transform: translateY(-2px);
            }
        '>Sign Up</a>
        <a href="Login" target="_self" style='
            text-decoration: none;
            color: white;
            background: #FF0000;
            padding: 8px 25px;
            border: 2px solid #FF0000;
            border-radius: 25px;
            font-weight: 600;
            transition: all 0.3s ease;
            display: inline-block;
            hover: {
                background: #CC0000;
                transform: translateY(-2px);
            }
        '>Sign In</a>
    </div>
""", unsafe_allow_html=True)

# Add some spacing after the navigation
st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)

# Hero Section with gradient text
st.markdown("""
    <div style='text-align: center; padding: 3rem 0;'>
        <h1 class='hero-text'>Transform Your YouTube Success</h1>
        <p style='font-size: 1.5rem; color: #666; margin-top: 1rem;'>
            Powerful analytics and insights to grow your channel
        </p>
    </div>
""", unsafe_allow_html=True)

# Features Section with cards
st.markdown("## 🚀 Key Features")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class='feature-card'>
        <h3>📊 Comprehensive Analytics</h3>
        <ul>
            <li>Real-time performance tracking</li>
            <li>Advanced metric visualization</li>
            <li>Custom date range analysis</li>
            <li>Trend identification</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='feature-card'>
        <h3>📈 Growth Insights</h3>
        <ul>
            <li>Subscriber growth tracking</li>
            <li>Engagement rate analysis</li>
            <li>Performance predictions</li>
            <li>Goal setting and tracking</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='feature-card'>
        <h3>🎯 Strategic Tools</h3>
        <ul>
            <li>Content performance metrics</li>
            <li>Audience behavior analysis</li>
            <li>Statistical analysis</li>
            <li>Seasonal pattern detection</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# How It Works Section with numbered steps
st.markdown("## 🔄 How It Works")
steps = st.columns(4)

for i, (title, desc) in enumerate([
    ("Sign Up", "Create your account in minutes"),
    ("Import Data", "Connect your YouTube channel"),
    ("Analyze", "Get instant insights"),
    ("Optimize", "Grow your channel")
], 1):
    with steps[i-1]:
        st.markdown(f"""
        <div style='text-align: center; padding: 1rem;'>
            <h3 style='color: #FF0000;'>{i}. {title}</h3>
            <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)

# Benefits Section with two columns
st.markdown("## 💪 Why Choose Us")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class='feature-card'>
        <h3>For Content Creators</h3>
        <ul>
            <li>Track your channel's growth</li>
            <li>Understand your audience</li>
            <li>Optimize upload timing</li>
            <li>Monitor engagement metrics</li>
            <li>Set and track goals</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='feature-card'>
        <h3>For Businesses</h3>
        <ul>
            <li>Brand performance tracking</li>
            <li>Competitor analysis</li>
            <li>ROI measurement</li>
            <li>Content strategy insights</li>
            <li>Team collaboration tools</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Update the CTA section to use dark theme colors
st.markdown("""
    <div class='cta-section'>
        <h2 style='color: #FFFFFF; text-align: center; font-size: 2.5rem;'>Ready to Transform Your YouTube Channel?</h2>
        <p style='font-size: 1.2rem; color: #CCCCCC; text-align: center; margin: 1rem 0;'>
            Join thousands of content creators who are growing their channels with data-driven insights
        </p>
    </div>
""", unsafe_allow_html=True)

# Centered Get Started button
col1, col2, col3 = st.columns([2,1,2])
with col2:
    if st.button("Get Started", type="primary", use_container_width=True, key="cta_button"):
        st.switch_page("pages/Signup.py")

# Divider before footer
st.markdown("<hr style='border: none; border-top: 1px solid #2E3338; margin: 3rem 0;'>", unsafe_allow_html=True)

# Create three columns for the footer sections
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<h4 style='color: #FFFFFF; margin-bottom: 1rem;'>Resources</h4>", unsafe_allow_html=True)
    st.markdown("""
        <div style='margin-bottom: 2rem;'>
            <a href="#" style='color: #888888; text-decoration: none; display: block; margin: 0.5rem 0;'>Documentation</a>
            <a href="#" style='color: #888888; text-decoration: none; display: block; margin: 0.5rem 0;'>Blog</a>
            <a href="#" style='color: #888888; text-decoration: none; display: block; margin: 0.5rem 0;'>Case Studies</a>
            <a href="#" style='color: #888888; text-decoration: none; display: block; margin: 0.5rem 0;'>Help Center</a>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("<h4 style='color: #FFFFFF; margin-bottom: 1rem;'>Company</h4>", unsafe_allow_html=True)
    st.markdown("""
        <div style='margin-bottom: 2rem;'>
            <a href="#" style='color: #888888; text-decoration: none; display: block; margin: 0.5rem 0;'>About Us</a>
            <a href="#" style='color: #888888; text-decoration: none; display: block; margin: 0.5rem 0;'>Careers</a>
            <a href="#" style='color: #888888; text-decoration: none; display: block; margin: 0.5rem 0;'>Contact</a>
            <a href="#" style='color: #888888; text-decoration: none; display: block; margin: 0.5rem 0;'>Partners</a>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("<h4 style='color: #FFFFFF; margin-bottom: 1rem;'>Legal</h4>", unsafe_allow_html=True)
    st.markdown("""
        <div style='margin-bottom: 2rem;'>
            <a href="#" style='color: #888888; text-decoration: none; display: block; margin: 0.5rem 0;'>Privacy Policy</a>
            <a href="#" style='color: #888888; text-decoration: none; display: block; margin: 0.5rem 0;'>Terms of Service</a>
            <a href="#" style='color: #888888; text-decoration: none; display: block; margin: 0.5rem 0;'>Cookie Policy</a>
            <a href="#" style='color: #888888; text-decoration: none; display: block; margin: 0.5rem 0;'>Security</a>
        </div>
    """, unsafe_allow_html=True)

# Bottom footer
st.markdown("""
    <div style='text-align: center; padding: 2rem 0; border-top: 1px solid #2E3338; margin-top: 2rem;'>
        <p style='color: #888888; margin-bottom: 0.5rem;'>© 2024 YouTube Analytics Platform. All rights reserved.</p>
        <p style='color: #888888; font-size: 0.8rem;'>Made with <span style='color: #FF0000;'>❤️</span> for content creators</p>
    </div>
""", unsafe_allow_html=True) 