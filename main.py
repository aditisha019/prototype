import streamlit as st
from pages import landing_page, sell_online_page
from auth import main as auth_main
from datetime import datetime, timedelta

# Session timeout configuration (should match auth.py)
SESSION_TIMEOUT_MINUTES = 15

def logout_user():
    """Logout user by clearing session state"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def check_session_timeout():
    """Check if session has timed out (consistent with auth.py)"""
    if "last_activity" in st.session_state and st.session_state.last_activity:
        try:
            last_activity = datetime.fromisoformat(st.session_state.last_activity)
            if datetime.now() - last_activity > timedelta(minutes=SESSION_TIMEOUT_MINUTES):
                st.warning("Session expired due to inactivity. Please log in again.")
                logout_user()
                return False
        except Exception as e:
            st.error(f"Session error: {str(e)}")
            logout_user()
            return False
    return True

def update_last_activity():
    """Update the last activity timestamp (consistent with auth.py)"""
    st.session_state.last_activity = datetime.now().isoformat()

# Initialize session state (consistent with auth.py)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "last_activity" not in st.session_state:
    st.session_state.last_activity = None

# Check session timeout if logged in
if st.session_state.logged_in:
    if not check_session_timeout():
        st.stop()  # Stop execution if session expired
    update_last_activity()  # Update activity on each page load

# Routing logic
if not st.session_state.logged_in:
    auth_main()  # Show authentication pages
else:
    # Initialize page state if not exists
    if "page" not in st.session_state:
        st.session_state.page = "landing"

    # Show session timeout info
    if "last_activity" in st.session_state and st.session_state.last_activity:
        last_activity = datetime.fromisoformat(st.session_state.last_activity)
        remaining_time = SESSION_TIMEOUT_MINUTES - (datetime.now() - last_activity).total_seconds() / 60
        if remaining_time > 0:
            st.sidebar.info(f"Session expires in {int(remaining_time)} minutes")

    # Add logout button to sidebar
    st.sidebar.button("Logout", on_click=logout_user, key="logout_button")

    # Page routing
    if st.session_state.page == "landing":
        landing_page()
    elif st.session_state.page == "chatbot":
        from chatbot import chatbot_page
        chatbot_page()
    elif st.session_state.page == "sell_online":
        sell_online_page()