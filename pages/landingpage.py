import streamlit as st
import google.generativeai as genai
import pandas as pd
import json
from datetime import datetime
import io
import base64
from fpdf import FPDF
import plotly.express as px
import plotly.graph_objects as go

# Configure Streamlit page
st.set_page_config(
    page_title="AI Business Guide", 
    page_icon="🚀", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .option-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        cursor: pointer;
        transition: transform 0.3s ease;
    }
    
    .option-card:hover {
        transform: translateY(-5px);
    }
    
    .eco-badge {
        background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        color: white;
        font-size: 0.8rem;
        margin: 0.2rem;
        display: inline-block;
    }
    
    .trend-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .download-section {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'analysis_data' not in st.session_state:
    st.session_state.analysis_data = None
if 'gemini_api_key' not in st.session_state:
    st.session_state.gemini_api_key = None

# Configure Gemini API
def configure_gemini():
    if st.session_state.gemini_api_key:
        try:
            genai.configure(api_key=st.session_state.gemini_api_key)
            return True
        except Exception as e:
            st.error(f"Error configuring Gemini API: {e}")
            return False
    return False

# Generate AI recommendations using Gemini
def generate_ai_recommendations(prompt, analysis_type):
    if not configure_gemini():
        return generate_mock_response(analysis_type)
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        enhanced_prompt = f"""
        You are an expert business consultant specializing in sustainable and eco-friendly businesses.
        
        Context: User is in Vellore, Tamil Nadu, India and wants to start a sustainable business.
        
        Please provide detailed recommendations for: {analysis_type}
        
        Requirements:
        1. Focus on eco-friendly, sustainable, or recyclable products/services
        2. Include market analysis for the Tamil Nadu region
        3. Provide specific startup costs in Indian Rupees
        4. Include target audience and marketing strategies
        5. Mention environmental impact and sustainability benefits
        6. Suggest local suppliers or resources where possible
        
        User Request: {prompt}
        
        Format the response with clear headings and bullet points for easy reading.
        """
        
        response = model.generate_content(enhanced_prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating AI recommendations: {e}")
        return generate_mock_response(analysis_type)

# Mock response for when API is not available
def generate_mock_response(analysis_type):
    mock_responses = {
        'Trend Analysis': """
# 📈 Market Trend Analysis for 2025

## Top 5 Trending Eco-Friendly Business Ideas:

1. **Biodegradable Packaging Solutions**
   - Market size: ₹2.5 Cr in Tamil Nadu
   - Startup cost: ₹5-8 Lakhs
   - Target: E-commerce, restaurants, retailers

2. **Organic Waste Management Systems**
   - Market size: ₹1.8 Cr
   - Startup cost: ₹3-5 Lakhs
   - Target: Residential complexes, offices

3. **Solar-Powered Water Purification**
   - Market size: ₹4.2 Cr
   - Startup cost: ₹8-12 Lakhs
   - Target: Rural areas, educational institutions

4. **Eco-Friendly Cleaning Products**
   - Market size: ₹1.2 Cr
   - Startup cost: ₹2-4 Lakhs
   - Target: Households, offices, hospitals

5. **Sustainable Fashion Accessories**
   - Market size: ₹3.5 Cr
   - Startup cost: ₹4-7 Lakhs
   - Target: Young professionals, students

## Key Market Insights:
- 67% increase in eco-conscious consumers in Tamil Nadu
- Government incentives for sustainable businesses
- Rising demand for locally-made eco products
- Educational institutions driving sustainable innovation
        """,
        'Eco-Friendly Products': """
# 🌱 Sustainable Product Opportunities

## Innovation Product Ideas:

1. **Bamboo-based Home Products**
   - Products: Toothbrushes, kitchen utensils, storage containers
   - Profit margin: 40-60%
   - Local suppliers: Kerala bamboo farms

2. **Recycled Paper Stationery**
   - Products: Notebooks, gift wrapping, office supplies
   - Eco-impact: 70% less water usage
   - Target: Students, offices

3. **Organic Cotton Bags**
   - Products: Shopping bags, produce bags
   - Cost: ₹15-25 per bag
   - Selling price: ₹50-80 per bag

4. **Compostable Food Packaging**
   - Products: Plates, cups, food containers
   - Biodegradable: 90 days
   - Market demand: High in urban areas

5. **Solar-Powered Gadgets**
   - Products: Phone chargers, LED lights, fans
   - ROI: 200-300% within 2 years
   - Government subsidies available

## Sustainability Features:
- 100% biodegradable materials
- Minimal packaging waste
- Local sourcing reduces carbon footprint
- Circular economy principles
        """,
        'Regional Insights': """
# 🌍 Vellore Regional Business Insights

## Local Market Characteristics:

### Educational Hub
- VIT University: 40,000+ students
- Young consumer base (18-25 years)
- High awareness of sustainability

### Agricultural Economy
- Strong connection to sustainable farming
- Access to organic raw materials
- Traditional eco-friendly practices

### Growing IT Sector
- Increasing environmental awareness
- Higher disposable income
- Tech-savvy consumers

## Best Business Opportunities:

1. **Student-Focused Eco Products**
   - Sustainable stationery, reusable items
   - Market size: ₹50 lakhs annually
   - Low competition

2. **Organic Food Distribution**
   - Farm-to-table delivery services
   - Tie-ups with local farmers
   - Growing demand: 25% YoY

3. **Eco-Tourism Services**
   - Sustainable travel experiences
   - Local heritage tours
   - Adventure tourism with eco-focus

4. **Green Technology Solutions**
   - Solar installations
   - Waste management systems
   - Water conservation solutions

## Local Resources:
- Agricultural raw materials readily available
- Skilled artisan workforce
- Government support for sustainable initiatives
- University partnerships for R&D
        """,
        'Custom Analysis': """
# 🤖 Comprehensive Business Analysis

## AI-Generated Business Plan for Sustainable Ventures

### Top 5 Recommended Businesses:

1. **Eco-Friendly Food Packaging Startup**
   - Investment: ₹8-12 lakhs
   - ROI: 35-40% annually
   - Break-even: 18 months
   - Target: Restaurants, cloud kitchens

2. **Organic Waste to Energy Plant**
   - Investment: ₹15-25 lakhs
   - ROI: 25-30% annually
   - Break-even: 24 months
   - Target: Residential complexes

3. **Sustainable Fashion E-commerce**
   - Investment: ₹5-8 lakhs
   - ROI: 45-50% annually
   - Break-even: 12 months
   - Target: Millennials, Gen Z

4. **Solar Solutions Provider**
   - Investment: ₹10-15 lakhs
   - ROI: 30-35% annually
   - Break-even: 20 months
   - Target: Residential, commercial

5. **Eco-Tourism Platform**
   - Investment: ₹3-5 lakhs
   - ROI: 40-45% annually
   - Break-even: 15 months
   - Target: Travelers, adventure seekers

## Implementation Timeline:
- **Month 1-2**: Business registration, permits
- **Month 3-4**: Product development, testing
- **Month 5-6**: Marketing, team building
- **Month 7-8**: Launch, customer acquisition
- **Month 9-12**: Scale operations, expansion

## Financial Projections:
- **Year 1**: ₹5-8 lakhs revenue
- **Year 2**: ₹12-18 lakhs revenue
- **Year 3**: ₹25-35 lakhs revenue
        """
    }
    return mock_responses.get(analysis_type, "Analysis not available.")

# Create PDF report
def create_pdf_report(analysis_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"AI Business Guide Report - {analysis_data['type']}", ln=True)
    pdf.ln(10)
    
    pdf.set_font("Arial", size=12)
    # Convert markdown to plain text for PDF
    content = analysis_data['content'].replace('#', '').replace('*', '')
    lines = content.split('\n')
    
    for line in lines:
        if line.strip():
            pdf.cell(0, 6, line.encode('latin-1', 'replace').decode('latin-1'), ln=True)
    
    return pdf.output(dest='S').encode('latin-1')

# Download functions
def get_download_link(data, filename, text):
    b64 = base64.b64encode(data).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">{text}</a>'

# Main app logic
def main():
    # Sidebar for API key
    with st.sidebar:
        st.header("🔧 Configuration")
        api_key = st.text_input("Enter Gemini API Key (Optional)", type="password", 
                               help="Enter your Google Gemini API key for enhanced AI recommendations")
        if api_key:
            st.session_state.gemini_api_key = api_key
            st.success("API Key configured!")
        else:
            st.info("Using mock responses without API key")
        
        st.header("📊 Quick Stats")
        st.metric("Eco-Businesses Analyzed", "150+")
        st.metric("Success Rate", "85%")
        st.metric("Avg. ROI", "35%")

    # Home page
    if st.session_state.page == 'home':
        st.markdown("""
        <div class="main-header">
            <h1>🚀 Your Business Journey Starts Here</h1>
            <p>Choose your path to entrepreneurial success with AI-powered guidance</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🏢 I Want to Start a Business", key="start_business", use_container_width=True):
                st.session_state.page = 'ai_guide'
                st.rerun()
        
        with col2:
            if st.button("🛒 I Want to Sell Online", key="sell_online", use_container_width=True):
                st.session_state.page = 'sell_online'
                st.rerun()
        
        # Features section
        st.markdown("## ✨ What You'll Get")
        
        feat_col1, feat_col2, feat_col3 = st.columns(3)
        
        with feat_col1:
            st.markdown("""
            ### 🤖 AI-Powered Insights
            - Market trend analysis
            - Personalized recommendations
            - Real-time data processing
            """)
        
        with feat_col2:
            st.markdown("""
            ### 🌱 Eco-Friendly Focus
            - Sustainable business ideas
            - Environmental impact analysis
            - Green technology solutions
            """)
        
        with feat_col3:
            st.markdown("""
            ### 📍 Regional Expertise
            - Local market insights
            - Cultural preferences
            - Resource availability
            """)

    # AI Guide page
    elif st.session_state.page == 'ai_guide':
        st.markdown("""
        <div class="main-header">
            <h1>🤖 AI Business Guide</h1>
            <p>Discover eco-friendly product ideas tailored to your region</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("← Back to Home", key="back_home"):
            st.session_state.page = 'home'
            st.rerun()
        
        st.markdown("## How would you like to get started?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📈 Trend Analysis", key="trend", use_container_width=True):
                show_analysis("Trend Analysis")
            
            if st.button("🌱 Eco-Friendly Ideas", key="eco", use_container_width=True):
                show_analysis("Eco-Friendly Products")
        
        with col2:
            if st.button("🌍 Regional Insights", key="regional", use_container_width=True):
                show_analysis("Regional Insights")
            
            if st.button("🤖 Custom Analysis", key="custom", use_container_width=True):
                show_analysis("Custom Analysis")
        
        # Display analysis results
        if st.session_state.analysis_data:
            st.markdown("---")
            st.markdown("## 📊 Analysis Results")
            
            # Display the analysis
            st.markdown(st.session_state.analysis_data['content'])
            
            # Download section
            st.markdown("""
            <div class="download-section">
                <h3>📥 Download Your Business Plan</h3>
                <p>Get your personalized business recommendations in multiple formats</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📄 Download PDF Report", key="pdf"):
                    pdf_data = create_pdf_report(st.session_state.analysis_data)
                    st.download_button(
                        label="Click to Download PDF",
                        data=pdf_data,
                        file_name=f"business_plan_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf"
                    )
            
            with col2:
                if st.button("📊 Download CSV Data", key="csv"):
                    # Create sample business data
                    df = pd.DataFrame({
                        'Business_Idea': ['Eco Packaging', 'Solar Solutions', 'Organic Food', 'Waste Management'],
                        'Investment_Required': ['₹5-8 Lakhs', '₹10-15 Lakhs', '₹3-5 Lakhs', '₹8-12 Lakhs'],
                        'Expected_ROI': ['35-40%', '30-35%', '40-45%', '25-30%'],
                        'Market_Size': ['₹2.5 Cr', '₹4.2 Cr', '₹1.8 Cr', '₹3.1 Cr']
                    })
                    csv_data = df.to_csv(index=False)
                    st.download_button(
                        label="Click to Download CSV",
                        data=csv_data,
                        file_name=f"business_data_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
            
            with col3:
                if st.button("💾 Download JSON Data", key="json"):
                    json_data = json.dumps(st.session_state.analysis_data, indent=2)
                    st.download_button(
                        label="Click to Download JSON",
                        data=json_data,
                        file_name=f"business_analysis_{datetime.now().strftime('%Y%m%d')}.json",
                        mime="application/json"
                    )

    # Sell Online page (placeholder)
    elif st.session_state.page == 'sell_online':
        st.markdown("""
        <div class="main-header">
            <h1>🛒 Sell Online Guide</h1>
            <p>Start your e-commerce journey with expert guidance</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("← Back to Home", key="back_home_sell"):
            st.session_state.page = 'home'
            st.rerun()
        
        st.info("🚧 Online selling guide coming soon! This will include platform recommendations, setup guides, and marketing strategies.")

def show_analysis(analysis_type):
    """Generate and display analysis results"""
    with st.spinner(f"🤖 AI is analyzing {analysis_type.lower()} and generating recommendations..."):
        # Generate prompt based on analysis type
        prompts = {
            'Trend Analysis': "Analyze current market trends for 2025 and suggest 5 eco-friendly business ideas with high demand and low environmental impact for Tamil Nadu, India.",
            'Eco-Friendly Products': "Suggest 7 innovative eco-friendly product ideas that promote sustainability and use recyclable materials, suitable for the Indian market.",
            'Regional Insights': "Provide business insights specific to Vellore, Tamil Nadu, India including local market demands and sustainable business opportunities.",
            'Custom Analysis': "Create a comprehensive business analysis with market trends, eco-friendly opportunities, and regional insights for Tamil Nadu with detailed business plans."
        }
        
        # Generate AI recommendations
        response = generate_ai_recommendations(prompts[analysis_type], analysis_type)
        
        # Store in session state
        st.session_state.analysis_data = {
            'type': analysis_type,
            'content': response,
            'timestamp': datetime.now().isoformat()
        }
    
    st.success(f"✅ {analysis_type} completed! Scroll down to see results.")

if __name__ == "__main__":
    main()
