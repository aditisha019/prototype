import streamlit as st
import hashlib
import json
import os
from datetime import datetime, timedelta

# Configuration
USER_DATA_FILE = "users.json"
SESSION_TIMEOUT_MINUTES = 15  # 15 minute session timeout

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

def check_session_timeout():
    """Check if session has timed out"""
    if "last_activity" in st.session_state:
        last_activity = datetime.fromisoformat(st.session_state.last_activity)
        if datetime.now() - last_activity > timedelta(minutes=SESSION_TIMEOUT_MINUTES):
            logout_user()
            return False
    return True

def update_last_activity():
    """Update the last activity timestamp"""
    st.session_state.last_activity = datetime.now().isoformat()

def main():
    st.set_page_config(page_title="User Authentication", page_icon="🔐", layout="centered")
    
    # Initialize session state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "last_activity" not in st.session_state:
        st.session_state.last_activity = None

    # Check session timeout
    if st.session_state.logged_in and not check_session_timeout():
        return  # Session expired, user will be logged out

    # Main app logic
    if st.session_state.logged_in:
        # Update last activity on each interaction
        update_last_activity()
        
        # User is logged in - show dashboard
        st.title(f"Welcome, {st.session_state.username}! 👋")
        st.success("You are successfully logged in!")
        
        # User info
        users = load_users()
        user_info = users.get(st.session_state.username, {})
        
        st.subheader("Your Account Information")
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"**Username:** {st.session_state.username}")
            st.info(f"**Email:** {user_info.get('email', 'N/A')}")
        
        with col2:
            created_at = user_info.get('created_at', 'N/A')
            if created_at != 'N/A':
                created_date = datetime.fromisoformat(created_at).strftime("%B %d, %Y")
                st.info(f"**Member since:** {created_date}")
        
        st.markdown("---")
        
        # Dashboard content
        st.subheader("Dashboard")
        st.write("This is your main dashboard. You can add your application content here!")
        
        # Sample dashboard widgets
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Projects", "5", "2")
        
        with col2:
            st.metric("Tasks Completed", "23", "5")
        
        with col3:
            st.metric("Score", "89%", "4%")
        
        st.markdown("---")
        
        # Session timeout info
        if "last_activity" in st.session_state:
            last_activity = datetime.fromisoformat(st.session_state.last_activity)
            remaining_time = SESSION_TIMEOUT_MINUTES - (datetime.now() - last_activity).total_seconds() / 60
            if remaining_time > 0:
                st.info(f"Session will expire in {int(remaining_time)} minutes")
        
        # Logout button
        if st.button("Logout", type="primary"):
            logout_user()
    
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
                            st.session_state.last_activity = datetime.now().isoformat()
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
        st.markdown(f"- Sessions expire after {SESSION_TIMEOUT_MINUTES} minutes of inactivity")

if __name__ == "__main__":
    main()