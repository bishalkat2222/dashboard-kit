import streamlit as st
from auth import create_user

st.set_page_config(page_title="Sign Up - YouTube Analytics", layout="wide")

def signup_page():
    col1, col2, col3 = st.columns([1,2,1])
    
    with col2:
        st.markdown("""
            <div style='text-align: center; padding: 1rem;'>
                <h1>Create Your Account</h1>
                <p>Start analyzing your YouTube channel today</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("signup_form"):
            new_email = st.text_input("Email")
            new_password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            new_name = st.text_input("Full Name")
            
            if st.form_submit_button("Sign Up", use_container_width=True):
                if new_email and new_password and confirm_password and new_name:
                    if new_password != confirm_password:
                        st.error("Passwords do not match")
                    else:
                        success, message = create_user(new_email, new_password, new_name)
                        if success:
                            st.success(message)
                            st.info("Please sign in with your new account")
                            st.switch_page("pages/Login.py")
                        else:
                            st.error(message)
                else:
                    st.error("Please fill in all fields")
        
        st.markdown("""
            <div style='text-align: center; padding: 1rem;'>
                <p>Already have an account? <a href="Login">Sign in</a></p>
            </div>
        """, unsafe_allow_html=True)

signup_page() 