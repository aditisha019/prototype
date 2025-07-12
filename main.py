import streamlit as st
from auth import authenticate_user, create_user, initialize_db
from pages import landing_page, business_guide_page

def main():
    # Initialize database
    initialize_db()
    
    # Set page config
    st.set_page_config(
        page_title="Business Guide App",
        page_icon="🚀",
        layout="wide"
    )
    
    # Check if user is logged in
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        show_auth_page()
    else:
        show_main_app()

def show_auth_page():
    st.title("Welcome to Business Guide")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                if authenticate_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Invalid username or password")
    
    with tab2:
        with st.form("signup_form"):
            new_username = st.text_input("Choose a username")
            new_password = st.text_input("Choose a password", type="password")
            confirm_password = st.text_input("Confirm password", type="password")
            submit = st.form_submit_button("Create Account")
            
            if submit:
                if new_password != confirm_password:
                    st.error("Passwords don't match")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters")
                else:
                    if create_user(new_username, new_password):
                        st.success("Account created successfully! Please login.")
                    else:
                        st.error("Username already exists")

def show_main_app():
    st.sidebar.title(f"Welcome, {st.session_state.username}!")
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
    
    page = st.sidebar.radio("Navigate", ["Home", "AI Business Guide"])
    
    if page == "Home":
        landing_page()
    elif page == "AI Business Guide":
        business_guide_page()

if __name__ == "__main__":
    main()
