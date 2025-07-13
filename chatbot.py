import os
import streamlit as st
import google.generativeai as gen_ai

# Load Google API Key from Streamlit secrets
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# Configure Gemini API
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel("gemini-2.0-flash")

# System prompt defining bot behavior
SYSTEM_PROMPT = """
You are VyaPyaarAI – a friendly, experienced business mentor. 
You help people in India start a business, especially those who have limited ideas or want to take their business online.

First, ask users:
- Which state in India they are from (for region-specific ideas)
- Their budget (e.g., under ₹50,000, ₹50k–2L, ₹2L–5L, or more)
- Their interests (e.g., food, fashion, tech, education, etc.)

Then, based on their responses, suggest 3–5 business ideas that are:
1. Sustainable
2. Sellable online (on Amazon, Meesho, etc.)
3. Regionally relevant and budget-friendly

💬 IMPORTANT: Detect the user's language. If they write in Hindi, Tamil, Telugu, Bengali, or any Indian language, respond in the same language. Otherwise, use simple English.

Keep your tone encouraging, clear, and step-by-step when needed.
"""

GREETING = "👋 Namaste! I'm VyaPyaarAI, here to help you find the right business idea. Let's begin!"

def chatbot_page():
    if st.button("⬅️ Back to Home"):
        st.session_state.page = "landing"
        st.rerun()

    st.title("💬 VyaPyaarAI – Business Idea Chatbot")

    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[
            {"role": "user", "parts": [SYSTEM_PROMPT]},
            {"role": "model", "parts": [GREETING]}
        ])

    for message in st.session_state.chat_session.history:
        if message.role == "user" and SYSTEM_PROMPT.strip() in message.parts[0].text:
            continue

        with st.chat_message("assistant" if message.role == "model" else message.role):
            st.markdown(message.parts[0].text)

    user_input = st.chat_input("Type your business question here...")

    if user_input:
        st.chat_message("user").markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("VyaPyaarAI is thinking..."):
                response = st.session_state.chat_session.send_message(user_input)
                st.markdown(response.text)
