import streamlit as st

def landing_page():
    # Welcome message if user is logged in
    if "username" in st.session_state and st.session_state.username:
        st.markdown(f"""
            <div style="text-align: center; margin-top: 20px;">
                <h3 style="color:#F9F0B2; font-weight: 600;">Welcome, <span style="color:#F9F0B2;">{st.session_state.username}</span>! 👋</h3>
            </div>
        """, unsafe_allow_html=True)

    # Title and description section
    st.markdown("""
                <div style="text-align: center; padding: 20px 20px;">
        <h1 class="main-title">VyaPyaarAI</h1>
<h4 class="subtitle" style="color:#FFC7D8">Empowering your journey from idea to income</h4>
<div class="description">
    Choose your business path.<br>
            Fill in your region, interests, and budget.<br>
            Get smart AI-powered suggestions to help you succeed.
</div>

<style>
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}
     body {
                background-image: url('https://images.unsplash.com/photo-1557682260-96773eb01377');  /* Replace with your image */
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }
    .main-title, .subtitle, .description, h3 {
                color: white !important;
                text-shadow: 1px 1px 2px #000;
            }
    .stButton > button {
        background-color: white;
        color:#0E1117 ;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 90%;
    }

    .stButton > button:hover {
        background-color: #12213E;
        color: white;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }

    .main-title {
        font-size: 88px;
        font-weight: 900;
        margin-bottom: 10px;
        color: #2c3e50;
    }

    .subtitle {
        font-size: 20px;
        color: #F9F0B2;
        margin-bottom: 10px;
    }

    .description {
        font-size: 18px;
        color: #fff;
        line-height: 1.6;
        margin-bottom: 10px;
    }

    .main > div {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Center the buttons using 5 columns
    col1, col2, col3, col4, col5 = st.columns([1, 1.5, 1, 1.5, 1])

    with col2:
        if st.button("I want to start a business", key="start"):
            st.session_state.page = "chatbot"
            st.rerun()

    with col4:
        if st.button("I want to sell online", key="sell"):
            st.session_state.page = "sell_online"
            st.rerun()


def sell_online_page():
    st.markdown("""
    <div style="text-align: center; padding: 50px 20px;">
        <h1 class="main-title">Sell Online</h1>
        <p class="subtitle">Start your e-commerce journey!</p>
        <div class="description">
            🛒 This feature is coming soon!<br>
            We're working on creating an amazing online selling guide for you.
        </div>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("← Back to Home", key="back_home"):
            st.session_state.page = "landing"
            st.rerun()
