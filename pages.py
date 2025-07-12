import streamlit as st
import google.generativeai as genai
import pandas as pd
from datetime import datetime

def landing_page():
    st.title("Business Guide Dashboard")
    st.write("Welcome to your personalized business guide!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("I want to start a business", help="Get AI-powered business ideas"):
            st.session_state.current_page = "business_guide"
            st.rerun()
    
    with col2:
        if st.button("I want to sell online", help="Learn how to sell products online"):
            st.info("This feature is coming soon!")
    
    st.markdown("---")
    st.write("""
    ### How it works:
    1. Click on "I want to start a business" to get AI-powered business ideas
    2. Our system will analyze current trends and suggest eco-friendly options
    3. You can download the recommendations for future reference
    """)

def business_guide_page():
    st.title("AI Business Guide")
    st.write("Get personalized business ideas based on trends, demand, and your region.")
    
    # User inputs
    with st.form("business_form"):
        region = st.selectbox("Your Region", 
                            ["North America", "Europe", "Asia", "South America", 
                             "Africa", "Australia", "Middle East"])
        
        interests = st.multiselect("Your Interests (optional)", 
                                 ["Technology", "Fashion", "Food", "Health", 
                                  "Home Goods", "Sustainability", "Education"])
        
        budget = st.select_slider("Estimated Budget", 
                                options=["Under $1k", "$1k-$5k", "$5k-$20k", "$20k-$100k", "Over $100k"])
        
        eco_focus = st.checkbox("Focus on eco-friendly/sustainable products", value=True)
        
        submitted = st.form_submit_button("Generate Business Ideas")
    
    if submitted:
        with st.spinner("Analyzing trends and generating ideas..."):
            try:
                # Initialize Gemini API - YOU NEED TO ADD YOUR OWN API KEY HERE
                genai.configure(api_key="YOUR_GEMINI_API_KEY")  # Replace with your actual API key
                
                model = genai.GenerativeModel('gemini-pro')
                
                # Create prompt
                prompt = f"""
                Suggest 5 specific business ideas for someone in {region} with these characteristics:
                - Interests: {', '.join(interests) if interests else 'Not specified'}
                - Budget: {budget}
                - Eco-focus: {'Yes' if eco_focus else 'No'}
                
                For each idea, provide:
                1. A brief description
                2. Why it's suitable for the region
                3. Market potential
                4. Eco-friendly aspects (if applicable)
                5. Startup requirements
                
                Present the information in a clear, structured format suitable for display in a web app.
                """
                
                response = model.generate_content(prompt)
                
                # Display results
                st.subheader("Recommended Business Ideas")
                st.markdown(response.text)
                
                # Download option
                st.download_button(
                    label="Download Recommendations",
                    data=response.text,
                    file_name=f"business_ideas_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("Please make sure you have a valid Gemini API key configured.")
