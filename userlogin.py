import streamlit as st
import hashlib
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

# Configuration
USER_DATA_FILE = "users.json"

def load_users():
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_users(users):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed_password):
    return hash_password(password) == hashed_password

def validate_email(email):
    return "@" in email and "." in email.split("@")[1]

def validate_password(password):
    return len(password) >= 6

def signup_user(username, email, password):
    users = load_users()
    if username in users:
        return False, "Username already exists!"
    for user_data in users.values():
        if user_data.get("email") == email:
            return False, "Email already registered!"
    if not validate_email(email):
        return False, "Invalid email format!"
    if not validate_password(password):
        return False, "Password must be at least 6 characters long!"
    
    users[username] = {
        "email": email,
        "password": hash_password(password),
        "created_at": datetime.now().isoformat()
    }
    save_users(users)
    return True, "Account created successfully!"

def login_user(username, password):
    users = load_users()
    if username not in users:
        return False, "Username not found!"
    if verify_password(password, users[username]["password"]):
        return True, "Login successful!"
    else:
        return False, "Invalid password!"

def logout_user():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# --- Main app ---
def main():
    st.set_page_config(page_title="User Authentication", page_icon="🔐", layout="centered")
    
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""

    if st.session_state.logged_in:
        st.title(f"Welcome, {st.session_state.username}! 👋")
        st.success("You are successfully logged in!")

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
        st.subheader("Dashboard")
        st.write("This is your main dashboard. You can add your application content here!")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Projects", "5", "2")
        with col2:
            st.metric("Tasks Completed", "23", "5")
        with col3:
            st.metric("Score", "89%", "4%")

        st.markdown("---")
        if st.button("Logout", type="primary"):
            logout_user()

    else:
        st.title("🔐 User Authentication")

        tab1, tab2, tab3 = st.tabs(["Login", "Sign Up", "Google Login"])

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

        with tab3:
            st.subheader("Login with Google")

            from streamlit_authenticator import Authenticate
            import yaml

            config = {
                "credentials": {
                    "oauth2": {
                        "google": {
                            "client_id": GOOGLE_CLIENT_ID,
                            "client_secret": GOOGLE_CLIENT_SECRET
                        }
                    }
                },
                "cookie": {
                    "name": "auth",
                    "key": "some_signature_key",
                    "expiry_days": 1
                }
            }

            authenticator = Authenticate(
                credentials=None,
                cookie_name=config["cookie"]["name"],
                key=config["cookie"]["key"],
                expiry_days=config["cookie"]["expiry_days"],
                oauth_config=config["credentials"]
            )

            name, auth_status, username = authenticator.login("Login with Google", "main", oauth_provider="google")

            if auth_status:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Logged in as {username}")
                st.rerun()

        st.markdown("---")
        st.markdown("**Demo Info:**")
        st.markdown("- Minimum password length: 6 characters")
        st.markdown("- User data is stored in `users.json` file")
        st.markdown("- Passwords are hashed using SHA-256")

if __name__ == "__main__":
    main()
