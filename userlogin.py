import streamlit as st
import hashlib
import json
import os
from datetime import datetime

# Configuration
USER_DATA_FILE = "users.json"

def load_users():
    """Load users from JSON file"""
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_users(users):
    """Save users to JSON file"""
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed_password):
    """Verify password against hash"""
    return hash_password(password) == hashed_password

def validate_email(email):
    """Basic email validation"""
    return "@" in email and "." in email.split("@")[1]

def validate_password(password):
    """Password validation - at least 6 characters"""
    return len(password) >= 6

def signup_user(username, email, password):
    """Register a new user"""
    users = load_users()
    
    # Check if username already exists
    if username in users:
        return False, "Username already exists!"
    
    # Check if email already exists
    for user_data in users.values():
        if user_data.get("email") == email:
            return False, "Email already registered!"
    
    # Validate email
    if not validate_email(email):
        return False, "Invalid email format!"
    
    # Validate password
    if not validate_password(password):
        return False, "Password must be at least 6 characters long!"
    
    # Save new user
    users[username] = {
        "email": email,
        "password": hash_password(password),
        "created_at": datetime.now().isoformat()
    }
    
    save_users(users)
    return True, "Account created successfully!"

def login_user(username, password):
    """Authenticate user login"""
    users = load_users()
    
    if username not in users:
        return False, "Username not found!"
    
    if verify_password(password, users[username]["password"]):
        return True, "Login successful!"
    else:
        return False, "Invalid password!"

def logout_user():
    """Logout user by clearing session state"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def main():
    st.set_page_config(page_title="User Authentication", page_icon="🔐", layout="centered")
    
    # Initialize session state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""
    
    # Main app logic
    if st.session_state.logged_in:
        # User is logged in - redirect to landing page
        st.success(f"Welcome, {st.session_state.username}! Redirecting to landing page...")
        
        # Add a small delay and then switch to landing page
        import time
        time.sleep(1)
        
        # Navigate to landing page
        st.switch_page("pages/landingpage.py")
    
    else:
        # User is not logged in - show login/signup
        st.title("🔐 User Authentication")
        
        # Create tabs for Login and Signup
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            st.subheader("Login to Your Account")
            
            with st.form("login_form"):
                username = st.text_input("Username", placeholder="Enter your username")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                
                login_button = st.form_submit_button("Login", type="primary")
                
                if login_button:
                    if username and password:
                        success, message = login_user(username, password)
                        if success:
                            st.session_state.logged_in = True
                            st.session_state.username = username
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                    else:
                        st.error("Please fill in all fields!")
        
        with tab2:
            st.subheader("Create New Account")
            
            with st.form("signup_form"):
                new_username = st.text_input("Username", placeholder="Choose a username")
                new_email = st.text_input("Email", placeholder="Enter your email")
                new_password = st.text_input("Password", type="password", placeholder="Create a password")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
                
                signup_button = st.form_submit_button("Sign Up", type="primary")
                
                if signup_button:
                    if new_username and new_email and new_password and confirm_password:
                        if new_password != confirm_password:
                            st.error("Passwords do not match!")
                        else:
                            success, message = signup_user(new_username, new_email, new_password)
                            if success:
                                st.success(message)
                                st.info("You can now login with your new account!")
                            else:
                                st.error(message)
                    else:
                        st.error("Please fill in all fields!")
        
        # Additional info
        st.markdown("---")
        st.markdown("**Demo Info:**")
        st.markdown("- Minimum password length: 6 characters")
        st.markdown("- User data is stored in `users.json` file")
        st.markdown("- Passwords are hashed using SHA-256")

if __name__ == "__main__":
    main()
