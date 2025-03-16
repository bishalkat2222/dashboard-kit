import streamlit as st
from auth import authenticate_user

st.set_page_config(page_title="Sign In - YouTube Analytics", layout="wide")

def login_page():
    col1, col2, col3 = st.columns([1,2,1])
    
    with col2:
        st.markdown("""
            <div style='text-align: center; padding: 1rem;'>
                <h1>Welcome Back!</h1>
                <p>Sign in to access your dashboard</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            login_email = st.text_input("Email")
            login_password = st.text_input("Password", type="password")
            
            if st.form_submit_button("Sign In", use_container_width=True):
                if login_email and login_password:
                    success, result = authenticate_user(login_email, login_password)
                    if success:
                        st.session_state.authenticated = True
                        st.session_state.user_name = result
                        st.success(f"Welcome back, {result}!")
                        st.switch_page("pages/Dashboard.py")
                    else:
                        st.error(result)
                else:
                    st.error("Please fill in all fields")
        
        st.markdown("""
            <div style='text-align: center; padding: 1rem;'>
                <p>Don't have an account? <a href="Signup">Sign up</a></p>
            </div>
        """, unsafe_allow_html=True)

login_page() 