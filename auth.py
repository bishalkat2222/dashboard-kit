import streamlit as st
import pandas as pd
from pathlib import Path
import os
import base64
from hmac import compare_digest

def make_hashed_password(password):
    """Hash a password for storing."""
    # Using base64 encoding instead of hashlib
    return base64.b64encode(password.encode()).decode()

def check_password(password, hashed_password):
    """Check hashed password against stored password."""
    return compare_digest(
        make_hashed_password(password),
        hashed_password
    )

def load_users():
    """Load users from CSV file."""
    users_file = Path("users.csv")
    if users_file.exists():
        return pd.read_csv(users_file)
    else:
        users = pd.DataFrame(columns=['email', 'password', 'name', 'role'])
        users.to_csv(users_file, index=False)
        return users

def save_users(users_df):
    """Save users to CSV file."""
    users_df.to_csv("users.csv", index=False)

def create_user(email, password, name):
    """Create a new user."""
    users_df = load_users()
    if email in users_df['email'].values:
        return False, "Email already exists"
    
    hashed_password = make_hashed_password(password)
    new_user = pd.DataFrame({
        'email': [email],
        'password': [hashed_password],
        'name': [name],
        'role': ['user']
    })
    users_df = pd.concat([users_df, new_user], ignore_index=True)
    save_users(users_df)
    return True, "User created successfully"

def authenticate_user(email, password):
    """Authenticate a user."""
    users_df = load_users()
    user = users_df[users_df['email'] == email]
    if user.empty:
        return False, "Email not found"
    
    if check_password(password, user['password'].iloc[0]):
        return True, user['name'].iloc[0]
    return False, "Incorrect password"

def create_admin_account():
    """Create admin account if it doesn't exist."""
    users_df = load_users()
    admin_email = "admin@example.com"
    
    if admin_email not in users_df['email'].values:
        admin_password = "admin123"
        hashed_password = make_hashed_password(admin_password)
        admin_user = pd.DataFrame({
            'email': [admin_email],
            'password': [hashed_password],
            'name': ['Admin'],
            'role': ['admin']
        })
        users_df = pd.concat([users_df, admin_user], ignore_index=True)
        save_users(users_df)
        print(f"""
        Admin account created:
        Email: {admin_email}
        Password: {admin_password}
        Please change these credentials after first login.
        """)

def login_page():
    """Display login page."""
    st.title("Welcome to YouTube Analytics Dashboard")
    
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_name' not in st.session_state:
        st.session_state.user_name = None

    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.header("Login")
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
            if login_email and login_password:
                success, result = authenticate_user(login_email, login_password)
                if success:
                    st.session_state.authenticated = True
                    st.session_state.user_name = result
                    st.success(f"Welcome back, {result}!")
                    st.rerun()
                else:
                    st.error(result)
            else:
                st.error("Please fill in all fields")

    with tab2:
        st.header("Sign Up")
        new_email = st.text_input("Email", key="signup_email")
        new_password = st.text_input("Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password")
        new_name = st.text_input("Full Name")
        
        if st.button("Sign Up"):
            if new_email and new_password and confirm_password and new_name:
                if new_password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    success, message = create_user(new_email, new_password, new_name)
                    if success:
                        st.success(message)
                        st.info("Please login with your new account")
                    else:
                        st.error(message)
            else:
                st.error("Please fill in all fields")

def logout():
    """Logout user."""
    if 'authenticated' in st.session_state:
        st.session_state.authenticated = False
    if 'user_name' in st.session_state:
        st.session_state.user_name = None

# Create admin account when module is loaded
create_admin_account() 