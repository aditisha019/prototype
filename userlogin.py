import streamlit as st
import hashlib
import json
import os
from datetime import datetime
import requests
import base64
from urllib.parse import urlencode

# Configuration
USER_DATA_FILE = "users.json"

# Google OAuth Configuration (Replace with your actual credentials)
GOOGLE_CLIENT_ID = "your_google_client_id"
GOOGLE_CLIENT_SECRET = "your_google_client_secret"
GOOGLE_REDIRECT_URI = "http://localhost:8501"

def inject_custom_css():
    """Inject custom CSS for improved UI/UX"""
    theme = st.session_state.get('theme', 'light')
    
    if theme == 'dark':
        css = """
        <style>
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 10px;
            text-align: center;
            color: white;
            margin-bottom: 2rem;
        }
        .auth-container {
            background: #1e1e1e;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            margin: 1rem 0;
        }
        .metric-card {
            background: #2d2d2d;
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 4px solid #667eea;
            margin: 0.5rem 0;
        }
        .google-btn {
            background: #4285f4;
            color: white;
            padding: 0.75rem 2rem;
            border-radius: 25px;
            border: none;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            width: 100%;
        }
        .theme-toggle {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            background: #2d2d2d;
            border: none;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            transition: all 0.3s;
        }
        .welcome-card {
            background: #2d2d2d;
            padding: 2rem;
            border-radius: 15px;
            margin: 1rem 0;
            border: 1px solid #404040;
        }
        </style>
        """
    else:
        css = """
        <style>
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 10px;
            text-align: center;
            color: white;
            margin-bottom: 2rem;
        }
        .auth-container {
            background: white;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            margin: 1rem 0;
            border: 1px solid #e0e0e0;
        }
        .metric-card {
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 4px solid #667eea;
            margin: 0.5rem 0;
        }
        .google-btn {
            background: #4285f4;
            color: white;
            padding: 0.75rem 2rem;
            border-radius: 25px;
            border: none;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            width: 100%;
        }
        .theme-toggle {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            background: #f8f9fa;
            border: 1px solid #e0e0e0;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            transition: all 0.3s;
        }
        .welcome-card {
            background: #f8f9fa;
            padding: 2rem;
            border-radius: 15px;
            margin: 1rem 0;
            border: 1px solid #e0e0e0;
        }
        </style>
        """
    
    st.markdown(css, unsafe_allow_html=True)

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
    """Password validation - at least 8 characters with mixed case"""
    return len(password) >= 8 and any(c.isupper() for c in password) and any(c.islower() for c in password)

def get_google_auth_url():
    """Generate Google OAuth URL"""
    params = {
        'client_id': GOOGLE_CLIENT_ID,
        'redirect_uri': GOOGLE_REDIRECT_URI,
        'scope': 'openid email profile',
        'response_type': 'code',
        'access_type': 'offline',
        'prompt': 'consent'
    }
    return f"https://accounts.google.com/o/oauth2/auth?{urlencode(params)}"

def handle_google_callback(code):
    """Handle Google OAuth callback"""
    try:
        # Exchange code for tokens
        token_data = {
            'client_id': GOOGLE_CLIENT_ID,
            'client_secret': GOOGLE_CLIENT_SECRET,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': GOOGLE_REDIRECT_URI,
        }
        
        response = requests.post('https://oauth2.googleapis.com/token', data=token_data)
        tokens = response.json()
        
        # Get user info
        headers = {'Authorization': f"Bearer {tokens['access_token']}"}
        user_response = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', headers=headers)
        user_info = user_response.json()
        
        return user_info
    except Exception as e:
        return None

def signup_user(username, email, password):
    """Register a new user"""
    users = load_users()
    
    if username in users:
        return False, "Username already exists!"
    
    for user_data in users.values():
        if user_data.get("email") == email:
            return False, "Email already registered!"
    
    if not validate_email(email):
        return False, "Invalid email format!"
    
    if not validate_password(password):
        return False, "Password must be at least 8 characters with uppercase and lowercase letters!"
    
    users[username] = {
        "email": email,
        "password": hash_password(password),
        "created_at": datetime.now().isoformat(),
        "auth_method": "email"
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

def login_google_user(user_info):
    """Login or register user via Google"""
    users = load_users()
    username = user_info['email'].split('@')[0]
    
    # Check if user exists
    existing_user = None
    for user, data in users.items():
        if data.get('email') == user_info['email']:
            existing_user = user
            break
    
    if existing_user:
        return True, existing_user, "Google login successful!"
    else:
        # Create new user
        counter = 1
        original_username = username
        while username in users:
            username = f"{original_username}{counter}"
            counter += 1
        
        users[username] = {
            "email": user_info['email'],
            "name": user_info.get('name', ''),
            "picture": user_info.get('picture', ''),
            "created_at": datetime.now().isoformat(),
            "auth_method": "google"
        }
        
        save_users(users)
        return True, username, "Google account created and logged in!"

def logout_user():
    """Logout user by clearing session state"""
    for key in list(st.session_state.keys()):
        if key != 'theme':  # Preserve theme setting
            del st.session_state[key]
    st.rerun()

def render_theme_toggle():
    """Render theme toggle button"""
    theme = st.session_state.get('theme', 'light')
    
    # Create a container for the toggle button
    toggle_container = st.container()
    
    with toggle_container:
        col1, col2, col3 = st.columns([4, 1, 1])
        
        with col3:
            if st.button("🌙" if theme == 'light' else "☀️", key="theme_toggle"):
                st.session_state.theme = 'dark' if theme == 'light' else 'light'
                st.rerun()

def render_header():
    """Render main header"""
    st.markdown("""
    <div class="main-header">
        <h1>🔐 SecureAuth Pro</h1>
        <p>Advanced Authentication System</p>
    </div>
    """, unsafe_allow_html=True)

def render_dashboard():
    """Render user dashboard"""
    users = load_users()
    user_info = users.get(st.session_state.username, {})
    
    # Welcome section
    st.markdown(f"""
    <div class="welcome-card">
        <h2>Welcome back, {st.session_state.username}! 👋</h2>
        <p>You're successfully logged in to your secure dashboard.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # User info cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h4>📧 Email</h4>
            <p>{user_info.get('email', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        auth_method = user_info.get('auth_method', 'email')
        st.markdown(f"""
        <div class="metric-card">
            <h4>🔑 Authentication</h4>
            <p>{"Google OAuth" if auth_method == 'google' else "Email & Password"}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        created_at = user_info.get('created_at', 'N/A')
        if created_at != 'N/A':
            created_date = datetime.fromisoformat(created_at).strftime("%B %d, %Y")
        else:
            created_date = 'N/A'
        
        st.markdown(f"""
        <div class="metric-card">
            <h4>📅 Member Since</h4>
            <p>{created_date}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if user_info.get('name'):
            st.markdown(f"""
            <div class="metric-card">
                <h4>👤 Full Name</h4>
                <p>{user_info.get('name')}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Dashboard metrics
    st.markdown("---")
    st.subheader("📊 Dashboard Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Projects", "12", "3")
    
    with col2:
        st.metric("Tasks Completed", "89", "15")
    
    with col3:
        st.metric("Success Rate", "94%", "2%")
    
    with col4:
        st.metric("Team Members", "7", "1")
    
    # Recent activity
    st.markdown("---")
    st.subheader("📈 Recent Activity")
    
    activity_data = [
        {"time": "2 hours ago", "action": "Completed project review", "status": "success"},
        {"time": "5 hours ago", "action": "Updated user permissions", "status": "info"},
        {"time": "1 day ago", "action": "Created new workspace", "status": "success"},
        {"time": "2 days ago", "action": "Invited team member", "status": "info"},
    ]
    
    for activity in activity_data:
        status_emoji = "✅" if activity["status"] == "success" else "ℹ️"
        st.markdown(f"{status_emoji} **{activity['time']}** - {activity['action']}")
    
    # Logout button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚪 Logout", type="primary", use_container_width=True):
            logout_user()

def render_auth_forms():
    """Render authentication forms"""
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Sign Up"])
    
    with tab1:
        st.markdown("### Welcome Back!")
        st.markdown("Sign in to your account to continue")
        
        # Google Login Button
        google_auth_url = get_google_auth_url()
        st.markdown(f"""
        <div style="margin: 1rem 0;">
            <a href="{google_auth_url}" target="_blank">
                <button class="google-btn">
                    <svg width="18" height="18" viewBox="0 0 24 24">
                        <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                        <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                        <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                        <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                    </svg>
                    Continue with Google
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**OR**")
        
        with st.form("login_form"):
            username = st.text_input("👤 Username", placeholder="Enter your username")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            
            col1, col2 = st.columns(2)
            with col1:
                remember_me = st.checkbox("Remember me")
            with col2:
                st.markdown("[Forgot password?](#)")
            
            login_button = st.form_submit_button("🔑 Login", type="primary", use_container_width=True)
            
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
        st.markdown("### Create Your Account")
        st.markdown("Join thousands of users already using our platform")
        
        with st.form("signup_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_username = st.text_input("👤 Username", placeholder="Choose a username")
                new_password = st.text_input("🔒 Password", type="password", placeholder="Create a strong password")
            
            with col2:
                new_email = st.text_input("📧 Email", placeholder="Enter your email")
                confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Confirm your password")
            
            terms = st.checkbox("I agree to the Terms of Service and Privacy Policy")
            
            signup_button = st.form_submit_button("📝 Create Account", type="primary", use_container_width=True)
            
            if signup_button:
                if not terms:
                    st.error("Please accept the terms and conditions!")
                elif new_username and new_email and new_password and confirm_password:
                    if new_password != confirm_password:
                        st.error("Passwords do not match!")
                    else:
                        success, message = signup_user(new_username, new_email, new_password)
                        if success:
                            st.success(message)
                            st.info("🎉 You can now login with your new account!")
                        else:
                            st.error(message)
                else:
                    st.error("Please fill in all fields!")
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="SecureAuth Pro",
        page_icon="🔐",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Initialize session state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "theme" not in st.session_state:
        st.session_state.theme = "light"
    
    # Inject custom CSS
    inject_custom_css()
    
    # Render theme toggle
    render_theme_toggle()
    
    # Handle Google OAuth callback
    query_params = st.query_params
    if "code" in query_params:
        user_info = handle_google_callback(query_params["code"])
        if user_info:
            success, username, message = login_google_user(user_info)
            if success:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(message)
                st.rerun()
        else:
            st.error("Google authentication failed!")
    
    # Render header
    render_header()
    
    # Main app logic
    if st.session_state.logged_in:
        render_dashboard()
    else:
        render_auth_forms()
        
        # Additional info
        st.markdown("---")
        st.markdown("### 🔒 Security Features")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**🛡️ Secure Authentication**")
            st.markdown("SHA-256 password hashing")
        
        with col2:
            st.markdown("**🔐 OAuth Integration**")
            st.markdown("Google Sign-In support")
        
        with col3:
            st.markdown("**🌙 Theme Support**")
            st.markdown("Light and dark modes")

if __name__ == "__main__":
    main()
