import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import openai
import os
from datetime import datetime
import json
import base64
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import requests
from PIL import Image
import io

# Page configuration
st.set_page_config(
    page_title="AI Resume Builder - Saurabh Parthe",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/parthesaurabh1616/AI_RESUME_BUILDER',
        'Report a bug': "https://github.com/parthesaurabh1616/AI_RESUME_BUILDER/issues",
        'About': "AI-Powered Resume Builder - Building the future with AI! 🚀"
    }
)

# Custom CSS for attractive black and purple design
st.markdown("""
<style>
    /* Dark theme base */
    .stApp {
        background-color: #0a0a0a;
        color: #ffffff;
    }
    
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #8b5cf6 0%, #a855f7 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        letter-spacing: -0.02em;
        text-shadow: 0 0 30px rgba(139, 92, 246, 0.5);
    }
    
    .sub-header {
        font-size: 1.3rem;
        font-weight: 400;
        text-align: center;
        color: #a78bfa;
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    
    .section-header {
        font-size: 2rem;
        font-weight: 700;
        color: #ffffff;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
        text-align: center;
        background: linear-gradient(90deg, #8b5cf6, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d1b69 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        color: #ffffff;
        box-shadow: 0 10px 30px rgba(139, 92, 246, 0.3);
        border: 1px solid #4c1d95;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(139, 92, 246, 0.5);
        border-color: #8b5cf6;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d1b69 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.3);
        text-align: center;
        margin: 0.5rem;
        border: 1px solid #4c1d95;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(139, 92, 246, 0.5);
    }
    
    .metric-number {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 1rem;
        color: #a78bfa;
        font-weight: 500;
    }
    
    .resume-preview {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d1b69 100%);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(139, 92, 246, 0.3);
        border: 1px solid #4c1d95;
        margin: 1rem 0;
        color: #ffffff;
    }
    
    .ai-badge {
        background: linear-gradient(45deg, #8b5cf6, #a855f7);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 600;
        display: inline-block;
        margin: 0.25rem;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
    }
    
    .cta-button {
        background: linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 50px;
        text-decoration: none;
        font-weight: 600;
        font-size: 1.1rem;
        display: inline-block;
        margin: 0.5rem;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4);
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
    }
    
    .cta-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(139, 92, 246, 0.6);
    }
    
    .hero-section {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d1b69 100%);
        padding: 3rem 2rem;
        border-radius: 25px;
        margin: 2rem 0;
        text-align: center;
        border: 1px solid #4c1d95;
        box-shadow: 0 20px 40px rgba(139, 92, 246, 0.3);
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #8b5cf6 0%, #a855f7 100%);
        height: 8px;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    .skill-tag {
        background: linear-gradient(45deg, #8b5cf6, #a855f7);
        color: white;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        margin: 0.2rem;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3);
    }
    
    .template-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d1b69 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.3);
        margin: 1rem;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        border: 1px solid #4c1d95;
        color: #ffffff;
    }
    
    .template-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(139, 92, 246, 0.5);
        border-color: #8b5cf6;
    }
    
    .template-card.selected {
        border: 3px solid #8b5cf6;
        background: linear-gradient(135deg, #2d1b69 0%, #4c1d95 100%);
    }
    
    /* COMPLETE UI VISIBILITY FIX - All text visible with proper contrast */
    
    /* Navigation Menu Styling */
    .stApp [data-testid="stSidebar"] {
        background-color: #1a1a1a !important;
    }
    
    .stApp [data-testid="stSidebar"] .css-1d391kg {
        background-color: #1a1a1a !important;
    }
    
    .stApp [data-testid="stSidebar"] .css-1d391kg .css-1v0mbdj {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Navigation Menu Items */
    .stApp [data-testid="stSidebar"] .css-1d391kg .css-1v0mbdj a {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    .stApp [data-testid="stSidebar"] .css-1d391kg .css-1v0mbdj a:hover {
        color: #8b5cf6 !important;
    }
    
    /* Main Content Area */
    .stApp .main .block-container {
        background-color: #0a0a0a !important;
        color: #ffffff !important;
    }
    
    /* All Headings */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    
    /* All Paragraphs and Text */
    .stApp p, .stApp div, .stApp span {
        color: #ffffff !important;
    }
    
    /* Form Elements */
    .stSelectbox > div > div {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #8b5cf6 !important;
        border-radius: 8px !important;
    }
    
    .stSelectbox label {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    .stTextInput > div > div > input {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #8b5cf6 !important;
        border-radius: 8px !important;
        padding: 8px !important;
    }
    
    .stTextInput label {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    .stTextArea > div > div > textarea {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #8b5cf6 !important;
        border-radius: 8px !important;
        padding: 8px !important;
    }
    
    .stTextArea label {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    .stDateInput > div > div > input {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #8b5cf6 !important;
        border-radius: 8px !important;
        padding: 8px !important;
    }
    
    .stDateInput label {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    .stCheckbox label {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    .stCheckbox > div > div {
        background-color: #ffffff !important;
        border: 2px solid #8b5cf6 !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3) !important;
        font-weight: 600 !important;
        padding: 0.5rem 1rem !important;
        font-size: 1rem !important;
    }
    
    .stButton > button:hover {
        box-shadow: 0 6px 20px rgba(139, 92, 246, 0.5) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Calendar Dropdown */
    .stDateInput > div > div > div {
        background-color: #ffffff !important;
        border: 2px solid #8b5cf6 !important;
        border-radius: 8px !important;
    }
    
    /* Calendar Widget */
    .stDateInput .css-1d391kg {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* Multiselect styling */
    .stMultiSelect > div > div {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #8b5cf6 !important;
        border-radius: 8px !important;
    }
    
    .stMultiSelect label {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Form styling */
    .stForm {
        background-color: #1a1a1a !important;
        border: 2px solid #8b5cf6 !important;
        border-radius: 15px !important;
        padding: 1rem !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #2d1b69 !important;
        color: #ffffff !important;
        border: 1px solid #8b5cf6 !important;
        border-radius: 8px !important;
    }
    
    .streamlit-expanderContent {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #8b5cf6 !important;
        border-radius: 8px !important;
    }
    
    /* Metric Cards */
    .stMetric {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #8b5cf6 !important;
        border-radius: 8px !important;
    }
    
    .stMetric > div {
        color: #ffffff !important;
    }
    
    .stMetric label {
        color: #ffffff !important;
    }
    
    /* Number Input */
    .stNumberInput > div > div > input {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #8b5cf6 !important;
        border-radius: 8px !important;
    }
    
    .stNumberInput label {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Download button styling */
    .download-button {
        background: linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 1rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4) !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
    }
    
    .download-button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 35px rgba(139, 92, 246, 0.6) !important;
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #8b5cf6 !important;
    }
    
    .stError {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #ff6b6b !important;
    }
    
    .stWarning {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #ffa500 !important;
    }
    
    .stInfo {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #8b5cf6 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'resume_data' not in st.session_state:
    st.session_state.resume_data = {
        'personal_info': {},
        'experience': [],
        'education': [],
        'skills': [],
        'projects': [],
        'achievements': [],
        'template': 'modern'
    }

if 'current_step' not in st.session_state:
    st.session_state.current_step = 1

if 'ai_suggestions' not in st.session_state:
    st.session_state.ai_suggestions = {}

# OpenAI API Key setup
def setup_openai():
    if 'openai_api_key' not in st.session_state:
        st.session_state.openai_api_key = os.getenv('OPENAI_API_KEY')
    
    if not st.session_state.openai_api_key:
        st.session_state.openai_api_key = st.text_input(
            "Enter your OpenAI API Key:",
            type="password",
            help="Get your API key from https://platform.openai.com/api-keys"
        )
    
    if st.session_state.openai_api_key:
        openai.api_key = st.session_state.openai_api_key
        return True
    return False

# AI-powered content generation
def generate_ai_content(prompt, max_tokens=500):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional resume writing expert. Generate high-quality, ATS-friendly content."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"AI generation failed: {str(e)}")
        return ""

# Navigation
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="color: #8b5cf6; margin: 0;">🚀 AI Resume Builder</h2>
        <p style="color: #a78bfa; margin: 0.5rem 0;">Powered by OpenAI GPT</p>
    </div>
    """, unsafe_allow_html=True)
    
    selected = option_menu(
        menu_title="Navigation",
        options=["Dashboard", "Personal Info", "Experience", "Education", "Skills", "Projects", "AI Assistant", "Templates", "Preview", "Export"],
        icons=["speedometer2", "person", "briefcase", "mortarboard", "tools", "folder", "robot", "layout", "eye", "download"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#1a1a1a"},
            "icon": {"color": "#8b5cf6", "font-size": "18px"},
            "nav-link": {
                "font-size": "14px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#2d1b69",
            },
            "nav-link-selected": {"background-color": "#8b5cf6"},
        }
    )

# Dashboard Page
if selected == "Dashboard":
    st.markdown('<h1 class="main-header">AI Resume Builder</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Create professional, ATS-friendly resumes with the power of AI</p>', unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h2 style="color: #ffffff; margin-bottom: 1rem;">🎯 Why Choose Our AI Resume Builder?</h2>
        <p style="color: #a78bfa; font-size: 1.1rem; margin-bottom: 2rem;">
            Our AI-powered platform analyzes job descriptions, suggests improvements, and creates 
            professional resumes that pass ATS systems and impress recruiters.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">95%</div>
            <div class="metric-label">ATS Pass Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">50+</div>
            <div class="metric-label">Templates</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">10K+</div>
            <div class="metric-label">Resumes Created</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">4.9</div>
            <div class="metric-label">User Rating</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Features Section
    st.markdown('<h2 class="section-header">🚀 Key Features</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #8b5cf6; margin-bottom: 1rem;">🤖 AI-Powered Content</h3>
            <p>Generate professional content using OpenAI GPT-3.5. Get suggestions for skills, 
            experience descriptions, and achievement highlights.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #8b5cf6; margin-bottom: 1rem;">📊 ATS Optimization</h3>
            <p>Our AI analyzes job descriptions and optimizes your resume to pass Applicant 
            Tracking Systems (ATS) used by 98% of companies.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #8b5cf6; margin-bottom: 1rem;">🎨 Professional Templates</h3>
            <p>Choose from 50+ professionally designed templates that are both visually 
            appealing and ATS-friendly.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #8b5cf6; margin-bottom: 1rem;">📱 Real-time Preview</h3>
            <p>See your resume come to life with real-time preview. Make changes and see 
            instant updates across all templates.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown('<h2 class="section-header">⚡ Quick Actions</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚀 Start Building Resume", key="start_build", use_container_width=True):
            st.session_state.current_step = 2
            st.rerun()
    
    with col2:
        if st.button("🤖 AI Content Generator", key="ai_gen", use_container_width=True):
            st.session_state.current_step = 7
            st.rerun()
    
    with col3:
        if st.button("👁️ Preview Resume", key="preview", use_container_width=True):
            st.session_state.current_step = 9
            st.rerun()

# Personal Info Page
elif selected == "Personal Info":
    st.markdown('<h2 class="section-header">👤 Personal Information</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #8b5cf6; margin-bottom: 1rem;">Basic Information</h3>
        </div>
        """, unsafe_allow_html=True)
        
        name = st.text_input("Full Name", value=st.session_state.resume_data['personal_info'].get('name', ''))
        email = st.text_input("Email", value=st.session_state.resume_data['personal_info'].get('email', ''))
        phone = st.text_input("Phone Number", value=st.session_state.resume_data['personal_info'].get('phone', ''))
        location = st.text_input("Location", value=st.session_state.resume_data['personal_info'].get('location', ''))
        
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #8b5cf6; margin-bottom: 1rem;">Professional Summary</h3>
        </div>
        """, unsafe_allow_html=True)
        
        summary = st.text_area("Professional Summary", 
                             value=st.session_state.resume_data['personal_info'].get('summary', ''),
                             height=150,
                             help="Write a compelling 2-3 sentence summary of your professional background")
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #8b5cf6; margin-bottom: 1rem;">Social Links</h3>
        </div>
        """, unsafe_allow_html=True)
        
        linkedin = st.text_input("LinkedIn URL", value=st.session_state.resume_data['personal_info'].get('linkedin', ''))
        github = st.text_input("GitHub URL", value=st.session_state.resume_data['personal_info'].get('github', ''))
        portfolio = st.text_input("Portfolio Website", value=st.session_state.resume_data['personal_info'].get('portfolio', ''))
        
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #8b5cf6; margin-bottom: 1rem;">AI Assistant</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🤖 Generate Professional Summary", key="gen_summary"):
            if setup_openai():
                job_title = st.selectbox("Select Your Role", [
                    "Software Engineer", "Full Stack Developer", "Frontend Developer", 
                    "Backend Developer", "Cloud Engineer", "DevOps Engineer", 
                    "Data Scientist", "Machine Learning Engineer", "Product Manager",
                    "UI/UX Designer", "Mobile Developer", "System Administrator"
                ])
                if job_title:
                    role_prompts = {
                        "Software Engineer": f"Write a professional summary for a Software Engineer with 2-3 sentences highlighting key skills and achievements",
                        "Full Stack Developer": f"Write a professional summary for a Full Stack Developer with 2-3 sentences emphasizing both frontend and backend technologies",
                        "Cloud Engineer": f"Write a professional summary for a Cloud Engineer with 2-3 sentences highlighting cloud platforms and infrastructure expertise",
                        "DevOps Engineer": f"Write a professional summary for a DevOps Engineer with 2-3 sentences focusing on CI/CD pipelines and automation"
                    }
                    prompt = role_prompts.get(job_title, f"Write a professional summary for a {job_title} with 2-3 sentences highlighting key skills and achievements")
                    ai_summary = generate_ai_content(prompt)
                    if ai_summary:
                        st.session_state.resume_data['personal_info']['summary'] = ai_summary
                        st.success("AI-generated summary created!")
                        st.rerun()
    
    # Save data
    if st.button("💾 Save Personal Information", key="save_personal"):
        st.session_state.resume_data['personal_info'] = {
            'name': name,
            'email': email,
            'phone': phone,
            'location': location,
            'summary': summary,
            'linkedin': linkedin,
            'github': github,
            'portfolio': portfolio
        }
        st.success("Personal information saved successfully!")

# Experience Page
elif selected == "Experience":
    st.markdown('<h2 class="section-header">💼 Work Experience</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #8b5cf6; margin-bottom: 1rem;">Add Work Experience</h3>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("experience_form"):
            job_title = st.text_input("Job Title", placeholder="e.g., Senior Software Engineer")
            company = st.text_input("Company Name", placeholder="e.g., Tech Corp Inc.")
            location = st.text_input("Location", placeholder="e.g., San Francisco, CA")
            
            col_start, col_end = st.columns(2)
            with col_start:
                start_date = st.date_input("Start Date")
            with col_end:
                end_date = st.date_input("End Date", value=None)
            
            current_job = st.checkbox("Currently Working Here")
            
            description = st.text_area("Job Description", height=100,
                                    help="Describe your main responsibilities and achievements",
                                    placeholder="e.g., Led development of microservices architecture, improved system performance by 40%")
            
            achievements = st.text_area("Key Achievements", height=100,
                                      help="List your major accomplishments and contributions",
                                      placeholder="e.g., • Reduced deployment time by 50%\n• Led team of 5 developers\n• Implemented CI/CD pipeline")
            
            technologies = st.text_input("Technologies Used", placeholder="e.g., Python, React, AWS, Docker, Kubernetes")
            
            if st.form_submit_button("➕ Add Experience"):
                if job_title and company:
                    experience = {
                        'job_title': job_title,
                        'company': company,
                        'location': location,
                        'start_date': start_date.strftime('%Y-%m-%d'),
                        'end_date': end_date.strftime('%Y-%m-%d') if end_date else None,
                        'current': current_job,
                        'description': description,
                        'achievements': achievements,
                        'technologies': technologies
                    }
                    st.session_state.resume_data['experience'].append(experience)
                    st.success("Work experience added successfully!")
                    st.rerun()
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #8b5cf6; margin-bottom: 1rem;">Experience List</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.resume_data['experience']:
            for i, exp in enumerate(st.session_state.resume_data['experience']):
                with st.expander(f"{exp['job_title']} at {exp['company']}"):
                    st.write(f"**Period:** {exp['start_date']} - {exp['end_date'] or 'Present'}")
                    st.write(f"**Location:** {exp['location']}")
                    if exp['description']:
                        st.write(f"**Description:** {exp['description']}")
                    if exp['achievements']:
                        st.write(f"**Achievements:** {exp['achievements']}")
                    if exp['technologies']:
                        st.write(f"**Technologies:** {exp['technologies']}")
                    
                    if st.button(f"🗑️ Delete", key=f"del_exp_{i}"):
                        st.session_state.resume_data['experience'].pop(i)
                        st.rerun()
        else:
            st.info("No work experience yet. Add your first job!")

# Education Page
elif selected == "Education":
    st.markdown('<h2 class="section-header">🎓 Education</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #8b5cf6; margin-bottom: 1rem;">Add Education</h3>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("education_form"):
            degree = st.text_input("Degree/Qualification", placeholder="e.g., Bachelor of Technology in Computer Science")
            institution = st.text_input("Institution Name", placeholder="e.g., University of Technology")
            location = st.text_input("Location", placeholder="e.g., New York, NY")
            
            col_start, col_end = st.columns(2)
            with col_start:
                start_date = st.date_input("Start Date")
            with col_end:
                end_date = st.date_input("End Date", value=None)
            
            current_study = st.checkbox("Currently Studying")
            
            gpa = st.text_input("GPA/Score (Optional)", placeholder="e.g., 3.8/4.0")
            
            achievements = st.text_area("Academic Achievements", height=100,
                                      help="List your academic accomplishments, honors, or relevant coursework",
                                      placeholder="e.g., Dean's List, Academic Excellence Award, Relevant Coursework: Data Structures, Algorithms")
            
            if st.form_submit_button("➕ Add Education"):
                if degree and institution:
                    education = {
                        'degree': degree,
                        'institution': institution,
                        'location': location,
                        'start_date': start_date.strftime('%Y-%m-%d'),
                        'end_date': end_date.strftime('%Y-%m-%d') if end_date else None,
                        'current': current_study,
                        'gpa': gpa,
                        'achievements': achievements
                    }
                    st.session_state.resume_data['education'].append(education)
                    st.success("Education added successfully!")
                    st.rerun()
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #8b5cf6; margin-bottom: 1rem;">Education List</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.resume_data['education']:
            for i, edu in enumerate(st.session_state.resume_data['education']):
                with st.expander(f"{edu['degree']} at {edu['institution']}"):
                    st.write(f"**Period:** {edu['start_date']} - {edu['end_date'] or 'Present'}")
                    st.write(f"**Location:** {edu['location']}")
                    if edu['gpa']:
                        st.write(f"**GPA:** {edu['gpa']}")
                    if edu['achievements']:
                        st.write(f"**Achievements:** {edu['achievements']}")
                    
                    if st.button(f"🗑️ Delete", key=f"del_edu_{i}"):
                        st.session_state.resume_data['education'].pop(i)
                        st.rerun()
        else:
            st.info("No education entries yet. Add your first education entry!")

# Skills Page
elif selected == "Skills":
    st.markdown('<h2 class="section-header">🛠️ Skills & Technologies</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #8b5cf6; margin-bottom: 1rem;">Add Skills</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Free text input for skills
        skills_input = st.text_area(
            "Enter your skills (one per line or comma-separated)", 
            height=150,
            placeholder="Python\nJavaScript\nReact\nAWS\nDocker\nKubernetes\nMachine Learning\nData Analysis",
            help="Enter each skill on a new line or separate with commas"
        )
        
        if st.button("💾 Save Skills"):
            if skills_input:
                # Parse skills from input
                skills_list = []
                for line in skills_input.split('\n'):
                    if ',' in line:
                        skills_list.extend([skill.strip() for skill in line.split(',') if skill.strip()])
                    else:
                        if line.strip():
                            skills_list.append(line.strip())
                
                st.session_state.resume_data['skills'] = skills_list
                st.success(f"Saved {len(skills_list)} skills successfully!")
                st.rerun()
        
        # Quick add common skills
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #8b5cf6; margin-bottom: 1rem;">Quick Add Common Skills</h3>
        </div>
        """, unsafe_allow_html=True)
        
        skill_categories = {
            'Programming Languages': ['Python', 'JavaScript', 'Java', 'C++', 'TypeScript', 'Go', 'Rust', 'C#', 'PHP', 'Ruby', 'Swift', 'Kotlin'],
            'Frameworks & Libraries': ['React', 'Node.js', 'Django', 'FastAPI', 'Spring Boot', 'Angular', 'Vue.js', 'Express.js', 'Flask', 'Laravel', 'Rails', 'ASP.NET'],
            'Cloud & DevOps': ['AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Terraform', 'Jenkins', 'GitLab CI', 'GitHub Actions', 'Ansible', 'Prometheus', 'Grafana'],
            'Databases': ['PostgreSQL', 'MongoDB', 'MySQL', 'Redis', 'Elasticsearch', 'Cassandra', 'DynamoDB', 'Firebase', 'SQLite', 'Oracle', 'SQL Server'],
            'AI/ML': ['TensorFlow', 'PyTorch', 'Scikit-learn', 'OpenAI API', 'Pandas', 'NumPy', 'Keras', 'Hugging Face', 'LangChain', 'OpenCV', 'NLTK', 'SpaCy'],
            'Tools': ['Git', 'Linux', 'VS Code', 'Jira', 'Confluence', 'Slack', 'Figma', 'Postman', 'Docker Desktop', 'IntelliJ IDEA', 'Eclipse', 'Xcode'],
            'Web Technologies': ['HTML5', 'CSS3', 'Bootstrap', 'Tailwind CSS', 'SASS', 'Webpack', 'Vite', 'Next.js', 'Nuxt.js', 'Svelte', 'jQuery'],
            'Mobile Development': ['React Native', 'Flutter', 'Ionic', 'Xamarin', 'Cordova', 'PhoneGap', 'Android Studio', 'Xcode', 'Expo']
        }
        
        selected_category = st.selectbox("Select Category to Add", ["Select a category..."] + list(skill_categories.keys()))
        
        if selected_category != "Select a category...":
            available_skills = skill_categories[selected_category]
            selected_skills = st.multiselect(
                f"Select {selected_category} to add",
                available_skills
            )
            
            if st.button(f"➕ Add Selected {selected_category}"):
                if selected_skills:
                    current_skills = st.session_state.resume_data['skills']
                    new_skills = [skill for skill in selected_skills if skill not in current_skills]
                    st.session_state.resume_data['skills'].extend(new_skills)
                    st.success(f"Added {len(new_skills)} new skills!")
                    st.rerun()
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #8b5cf6; margin-bottom: 1rem;">Current Skills</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.resume_data['skills']:
            for skill in st.session_state.resume_data['skills']:
                st.markdown(f'<span class="skill-tag">{skill}</span>', unsafe_allow_html=True)
        else:
            st.info("No skills added yet. Select skills from the categories!")

# Projects Page
elif selected == "Projects":
    st.markdown('<h2 class="section-header">🚀 Projects</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #8b5cf6; margin-bottom: 1rem;">Add Project</h3>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("project_form"):
            project_name = st.text_input("Project Name", placeholder="e.g., E-Commerce Platform")
            description = st.text_area("Project Description", height=100, 
                                     placeholder="Brief description of what the project does and its purpose")
            
            col_tech, col_date = st.columns(2)
            with col_tech:
                technologies = st.text_input("Technologies Used", placeholder="React, Node.js, MongoDB, AWS")
            with col_date:
                project_date = st.date_input("Project Date")
            
            github_url = st.text_input("GitHub URL (Optional)", placeholder="https://github.com/username/project")
            live_url = st.text_input("Live Demo URL (Optional)", placeholder="https://project-demo.com")
            
            features = st.text_area("Key Features", height=100,
                                  help="List the main features and functionalities",
                                  placeholder="User authentication, Payment processing, Real-time chat, Admin dashboard")
            
            if st.form_submit_button("➕ Add Project"):
                if project_name and description:
                    project = {
                        'name': project_name,
                        'description': description,
                        'technologies': technologies,
                        'date': project_date.strftime('%Y-%m-%d'),
                        'github_url': github_url,
                        'live_url': live_url,
                        'features': features
                    }
                    st.session_state.resume_data['projects'].append(project)
                    st.success("Project added successfully!")
                    st.rerun()
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #8b5cf6; margin-bottom: 1rem;">Projects List</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.resume_data['projects']:
            for i, project in enumerate(st.session_state.resume_data['projects']):
                with st.expander(f"{project['name']}"):
                    st.write(f"**Date:** {project['date']}")
                    st.write(f"**Description:** {project['description']}")
                    if project['technologies']:
                        st.write(f"**Technologies:** {project['technologies']}")
                    if project['features']:
                        st.write(f"**Features:** {project['features']}")
                    if project['github_url']:
                        st.write(f"**GitHub:** {project['github_url']}")
                    if project['live_url']:
                        st.write(f"**Live Demo:** {project['live_url']}")
                    
                    if st.button(f"🗑️ Delete", key=f"del_proj_{i}"):
                        st.session_state.resume_data['projects'].pop(i)
                        st.rerun()
        else:
            st.info("No projects added yet. Add your first project!")

# AI Assistant Page
elif selected == "AI Assistant":
    st.markdown('<h2 class="section-header">🤖 AI Assistant</h2>', unsafe_allow_html=True)
    
    if not setup_openai():
        st.warning("Please enter your OpenAI API key in the sidebar to use AI features.")
        st.stop()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #8b5cf6; margin-bottom: 1rem;">AI Content Generator</h3>
        </div>
        """, unsafe_allow_html=True)
        
        content_type = st.selectbox(
            "What would you like to generate?",
            ["Professional Summary", "Job Description", "Achievement Bullets", "Skills Suggestions", "Cover Letter"]
        )
        
        if content_type == "Professional Summary":
            job_title = st.selectbox("Select Your Role", [
                "Software Engineer", "Full Stack Developer", "Frontend Developer", 
                "Backend Developer", "Cloud Engineer", "DevOps Engineer", 
                "Data Scientist", "Machine Learning Engineer", "Product Manager",
                "UI/UX Designer", "Mobile Developer", "System Administrator",
                "Cybersecurity Engineer", "Blockchain Developer", "Game Developer",
                "Technical Writer", "Solutions Architect", "QA Engineer",
                "Business Analyst", "Project Manager", "Scrum Master",
                "Database Administrator", "Network Engineer", "IT Support Specialist"
            ])
            years_exp = st.number_input("Years of Experience", min_value=0, max_value=50)
            
            if st.button("🤖 Generate Summary"):
                role_prompts = {
                    "Software Engineer": f"Write a professional summary for a Software Engineer with {years_exp} years of experience. Focus on programming languages, software development methodologies, problem-solving skills, and technical achievements.",
                    "Full Stack Developer": f"Write a professional summary for a Full Stack Developer with {years_exp} years of experience. Emphasize both frontend and backend technologies, database management, API development, and full-stack project delivery.",
                    "Cloud Engineer": f"Write a professional summary for a Cloud Engineer with {years_exp} years of experience. Highlight cloud platforms (AWS, Azure, GCP), infrastructure as code, containerization, and cloud architecture expertise.",
                    "DevOps Engineer": f"Write a professional summary for a DevOps Engineer with {years_exp} years of experience. Focus on CI/CD pipelines, automation, monitoring, infrastructure management, and deployment strategies.",
                    "Data Scientist": f"Write a professional summary for a Data Scientist with {years_exp} years of experience. Emphasize statistical analysis, machine learning, data visualization, and business intelligence skills.",
                    "Machine Learning Engineer": f"Write a professional summary for a Machine Learning Engineer with {years_exp} years of experience. Highlight ML model development, deep learning, MLOps, and AI system deployment.",
                    "Cybersecurity Engineer": f"Write a professional summary for a Cybersecurity Engineer with {years_exp} years of experience. Focus on security protocols, threat analysis, vulnerability assessment, and security implementation.",
                    "Blockchain Developer": f"Write a professional summary for a Blockchain Developer with {years_exp} years of experience. Emphasize smart contracts, decentralized applications, cryptocurrency technologies, and blockchain architecture.",
                    "Game Developer": f"Write a professional summary for a Game Developer with {years_exp} years of experience. Highlight game engines, programming languages, game design, and interactive development.",
                    "Technical Writer": f"Write a professional summary for a Technical Writer with {years_exp} years of experience. Focus on documentation, technical communication, content creation, and knowledge management.",
                    "Solutions Architect": f"Write a professional summary for a Solutions Architect with {years_exp} years of experience. Emphasize system design, architecture planning, technology integration, and enterprise solutions.",
                    "QA Engineer": f"Write a professional summary for a QA Engineer with {years_exp} years of experience. Focus on testing methodologies, quality assurance, automation testing, and software validation."
                }
                
                prompt = role_prompts.get(job_title, f"Write a professional summary for a {job_title} with {years_exp} years of experience")
                ai_content = generate_ai_content(prompt)
                if ai_content:
                    st.text_area("Generated Summary", value=ai_content, height=200)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #8b5cf6; margin-bottom: 1rem;">Resume Analysis</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📊 Analyze Resume"):
            personal_score = len([v for v in st.session_state.resume_data['personal_info'].values() if v]) / 8 * 100
            experience_score = len(st.session_state.resume_data['experience']) * 20
            skills_score = len(st.session_state.resume_data['skills']) * 2
            education_score = len(st.session_state.resume_data['education']) * 25
            projects_score = len(st.session_state.resume_data['projects']) * 15
            
            total_score = min(100, (personal_score + experience_score + skills_score + education_score + projects_score) / 5)
            
            st.metric("Resume Completeness", f"{total_score:.1f}%")
            
            st.markdown(f"""
            <div class="progress-bar" style="width: {total_score}%;"></div>
            """, unsafe_allow_html=True)
            
            suggestions = []
            if personal_score < 80:
                suggestions.append("Complete personal information")
            if experience_score < 60:
                suggestions.append("Add more work experience")
            if skills_score < 80:
                suggestions.append("Add more relevant skills")
            if education_score < 50:
                suggestions.append("Add education details")
            if projects_score < 60:
                suggestions.append("Add more projects")
            
            if suggestions:
                st.markdown("**Suggestions:**")
                for suggestion in suggestions:
                    st.markdown(f"• {suggestion}")

# Preview Page
elif selected == "Preview":
    st.markdown('<h2 class="section-header">👁️ Resume Preview</h2>', unsafe_allow_html=True)
    
    # Resume preview
    st.markdown("""
    <div class="resume-preview">
        <h2 style="color: #8b5cf6; text-align: center; margin-bottom: 2rem;">RESUME PREVIEW</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Personal Information
    personal_info = st.session_state.resume_data['personal_info']
    if any(personal_info.values()):
        st.markdown("### 👤 Personal Information")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if personal_info.get('name'):
                st.write(f"**Name:** {personal_info['name']}")
            if personal_info.get('email'):
                st.write(f"**Email:** {personal_info['email']}")
        
        with col2:
            if personal_info.get('phone'):
                st.write(f"**Phone:** {personal_info['phone']}")
            if personal_info.get('location'):
                st.write(f"**Location:** {personal_info['location']}")
        
        with col3:
            if personal_info.get('linkedin'):
                st.write(f"**LinkedIn:** {personal_info['linkedin']}")
            if personal_info.get('github'):
                st.write(f"**GitHub:** {personal_info['github']}")
        
        if personal_info.get('summary'):
            st.markdown("### 📝 Professional Summary")
            st.write(personal_info['summary'])
    
    # Work Experience
    if st.session_state.resume_data['experience']:
        st.markdown("### 💼 Work Experience")
        for exp in st.session_state.resume_data['experience']:
            st.markdown(f"**{exp['job_title']}** at {exp['company']}")
            st.write(f"*{exp['start_date']} - {exp['end_date'] or 'Present'} | {exp['location']}*")
            if exp['description']:
                st.write(f"**Description:** {exp['description']}")
            if exp['achievements']:
                st.write(f"**Achievements:** {exp['achievements']}")
            if exp['technologies']:
                st.write(f"**Technologies:** {exp['technologies']}")
            st.markdown("---")
    
    # Education
    if st.session_state.resume_data['education']:
        st.markdown("### 🎓 Education")
        for edu in st.session_state.resume_data['education']:
            st.markdown(f"**{edu['degree']}**")
            st.write(f"*{edu['institution']} | {edu['start_date']} - {edu['end_date'] or 'Present'}*")
            if edu['location']:
                st.write(f"**Location:** {edu['location']}")
            if edu['gpa']:
                st.write(f"**GPA:** {edu['gpa']}")
            if edu['achievements']:
                st.write(f"**Achievements:** {edu['achievements']}")
            st.markdown("---")
    
    # Skills
    if st.session_state.resume_data['skills']:
        st.markdown("### 🛠️ Skills")
        skills_text = ", ".join(st.session_state.resume_data['skills'])
        st.write(skills_text)
        st.markdown("---")
    
    # Projects
    if st.session_state.resume_data['projects']:
        st.markdown("### 🚀 Projects")
        for project in st.session_state.resume_data['projects']:
            st.markdown(f"**{project['name']}**")
            st.write(f"*{project['date']}*")
            st.write(f"**Description:** {project['description']}")
            if project['technologies']:
                st.write(f"**Technologies:** {project['technologies']}")
            if project['features']:
                st.write(f"**Features:** {project['features']}")
            if project['github_url']:
                st.write(f"**GitHub:** {project['github_url']}")
            if project['live_url']:
                st.write(f"**Live Demo:** {project['live_url']}")
            st.markdown("---")
    
    # Download button
    st.markdown("""
    <div style="text-align: center; margin-top: 2rem;">
        <button onclick="window.print()" class="cta-button">🖨️ Print Preview</button>
    </div>
    """, unsafe_allow_html=True)

# Templates Page
elif selected == "Templates":
    st.markdown('<h2 class="section-header">🎨 Resume Templates</h2>', unsafe_allow_html=True)
    
    templates = {
        'Modern': {
            'description': 'Clean, modern design with purple accents',
            'features': ['ATS-friendly', 'Mobile responsive', 'Professional'],
            'image': 'https://via.placeholder.com/300x400/8b5cf6/ffffff?text=Modern+Template',
            'preview': 'Modern template with clean lines and purple highlights'
        },
        'Creative': {
            'description': 'Bold design for creative professionals',
            'features': ['Eye-catching', 'Colorful', 'Unique'],
            'image': 'https://via.placeholder.com/300x400/a855f7/ffffff?text=Creative+Template',
            'preview': 'Creative template with bold colors and unique layout'
        },
        'Minimal': {
            'description': 'Simple, elegant design',
            'features': ['Clean', 'Focused', 'Timeless'],
            'image': 'https://via.placeholder.com/300x400/c084fc/ffffff?text=Minimal+Template',
            'preview': 'Minimal template with focus on content'
        },
        'Technical': {
            'description': 'Perfect for tech professionals',
            'features': ['Code-friendly', 'Technical', 'Structured'],
            'image': 'https://via.placeholder.com/300x400/4c1d95/ffffff?text=Technical+Template',
            'preview': 'Technical template optimized for developers'
        }
    }
    
    cols = st.columns(2)
    
    for i, (template_name, template_info) in enumerate(templates.items()):
        with cols[i % 2]:
            is_selected = st.session_state.resume_data['template'] == template_name.lower()
            
            st.markdown(f"""
            <div class="template-card {'selected' if is_selected else ''}">
                <h3 style="color: #8b5cf6; margin-bottom: 1rem;">{template_name}</h3>
                <img src="{template_info['image']}" style="width: 100%; height: 200px; object-fit: cover; border-radius: 10px; margin-bottom: 1rem;">
                <p style="color: #a78bfa; margin-bottom: 1rem;">{template_info['description']}</p>
                <div style="margin-bottom: 1rem;">
            """, unsafe_allow_html=True)
            
            for feature in template_info['features']:
                st.markdown(f'<span class="ai-badge">{feature}</span>', unsafe_allow_html=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True)
            
            if st.button(f"Select {template_name}", key=f"select_{template_name.lower()}"):
                st.session_state.resume_data['template'] = template_name.lower()
                st.success(f"{template_name} template selected!")
                st.rerun()

# Export Page
elif selected == "Export":
    st.markdown('<h2 class="section-header">📥 Export Resume</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #8b5cf6; margin-bottom: 1rem;">Export Options</h3>
        </div>
        """, unsafe_allow_html=True)
        
        export_format = st.selectbox("Export Format", ["PDF", "Word Document", "Plain Text", "JSON"])
        
        if st.button("📄 Generate PDF"):
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
            styles = getSampleStyleSheet()
            story = []
            
            # Custom styles for professional resume
            title_style = ParagraphStyle(
                'TitleStyle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=12,
                textColor=colors.HexColor('#8b5cf6'),
                alignment=1
            )
            
            header_style = ParagraphStyle(
                'HeaderStyle',
                parent=styles['Heading2'],
                fontSize=14,
                spaceAfter=6,
                spaceBefore=12,
                textColor=colors.HexColor('#8b5cf6'),
                borderWidth=1,
                borderColor=colors.HexColor('#8b5cf6'),
                borderPadding=6
            )
            
            # Add content to PDF
            personal_info = st.session_state.resume_data['personal_info']
            
            # Name
            story.append(Paragraph(personal_info.get('name', 'Your Name'), title_style))
            
            # Contact info
            contact_parts = []
            if personal_info.get('email'):
                contact_parts.append(personal_info['email'])
            if personal_info.get('phone'):
                contact_parts.append(personal_info['phone'])
            if personal_info.get('location'):
                contact_parts.append(personal_info['location'])
            
            contact_info = " | ".join(contact_parts)
            story.append(Paragraph(contact_info, styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Professional Summary
            if personal_info.get('summary'):
                story.append(Paragraph("PROFESSIONAL SUMMARY", header_style))
                story.append(Paragraph(personal_info['summary'], styles['Normal']))
                story.append(Spacer(1, 15))
            
            # Work Experience
            if st.session_state.resume_data['experience']:
                story.append(Paragraph("WORK EXPERIENCE", header_style))
                for exp in st.session_state.resume_data['experience']:
                    # Job title and company
                    job_info = f"<b>{exp['job_title']}</b> at <b>{exp['company']}</b>"
                    story.append(Paragraph(job_info, styles['Normal']))
                    
                    # Dates and location
                    date_info = f"{exp['start_date']} - {exp['end_date'] or 'Present'}"
                    if exp['location']:
                        date_info += f" | {exp['location']}"
                    story.append(Paragraph(date_info, styles['Normal']))
                    
                    # Description
                    if exp['description']:
                        story.append(Paragraph(f"<b>Description:</b> {exp['description']}", styles['Normal']))
                    
                    # Achievements
                    if exp['achievements']:
                        story.append(Paragraph(f"<b>Achievements:</b> {exp['achievements']}", styles['Normal']))
                    
                    # Technologies
                    if exp['technologies']:
                        story.append(Paragraph(f"<b>Technologies:</b> {exp['technologies']}", styles['Normal']))
                    
                    story.append(Spacer(1, 10))
            
            # Education
            if st.session_state.resume_data['education']:
                story.append(Paragraph("EDUCATION", header_style))
                for edu in st.session_state.resume_data['education']:
                    # Degree and institution
                    edu_info = f"<b>{edu['degree']}</b> - {edu['institution']}"
                    story.append(Paragraph(edu_info, styles['Normal']))
                    
                    # Dates and location
                    date_info = f"{edu['start_date']} - {edu['end_date'] or 'Present'}"
                    if edu['location']:
                        date_info += f" | {edu['location']}"
                    story.append(Paragraph(date_info, styles['Normal']))
                    
                    # GPA
                    if edu['gpa']:
                        story.append(Paragraph(f"<b>GPA:</b> {edu['gpa']}", styles['Normal']))
                    
                    # Achievements
                    if edu['achievements']:
                        story.append(Paragraph(f"<b>Achievements:</b> {edu['achievements']}", styles['Normal']))
                    
                    story.append(Spacer(1, 10))
            
            # Projects
            if st.session_state.resume_data['projects']:
                story.append(Paragraph("PROJECTS", header_style))
                for project in st.session_state.resume_data['projects']:
                    # Project name and date
                    project_info = f"<b>{project['name']}</b> ({project['date']})"
                    story.append(Paragraph(project_info, styles['Normal']))
                    
                    # Description
                    if project['description']:
                        story.append(Paragraph(f"<b>Description:</b> {project['description']}", styles['Normal']))
                    
                    # Technologies
                    if project['technologies']:
                        story.append(Paragraph(f"<b>Technologies:</b> {project['technologies']}", styles['Normal']))
                    
                    # Features
                    if project['features']:
                        story.append(Paragraph(f"<b>Features:</b> {project['features']}", styles['Normal']))
                    
                    # URLs
                    urls = []
                    if project['github_url']:
                        urls.append(f"GitHub: {project['github_url']}")
                    if project['live_url']:
                        urls.append(f"Live Demo: {project['live_url']}")
                    
                    if urls:
                        story.append(Paragraph(f"<b>Links:</b> {' | '.join(urls)}", styles['Normal']))
                    
                    story.append(Spacer(1, 10))
            
            # Skills
            if st.session_state.resume_data['skills']:
                story.append(Paragraph("TECHNICAL SKILLS", header_style))
                skills_text = " • ".join(st.session_state.resume_data['skills'])
                story.append(Paragraph(skills_text, styles['Normal']))
                story.append(Spacer(1, 15))
            
            # Social Links
            social_links = []
            if personal_info.get('linkedin'):
                social_links.append(f"LinkedIn: {personal_info['linkedin']}")
            if personal_info.get('github'):
                social_links.append(f"GitHub: {personal_info['github']}")
            if personal_info.get('portfolio'):
                social_links.append(f"Portfolio: {personal_info['portfolio']}")
            
            if social_links:
                story.append(Paragraph("SOCIAL LINKS", header_style))
                story.append(Paragraph(" | ".join(social_links), styles['Normal']))
            
            doc.build(story)
            buffer.seek(0)
            
            st.download_button(
                label="📥 Download Professional PDF",
                data=buffer.getvalue(),
                file_name=f"resume_{personal_info.get('name', 'candidate').replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf"
            )
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #8b5cf6; margin-bottom: 1rem;">Export Summary</h3>
        </div>
        """, unsafe_allow_html=True)
        
        total_sections = len(st.session_state.resume_data)
        completed_sections = len([k for k, v in st.session_state.resume_data.items() if v])
        
        st.metric("Completion Rate", f"{(completed_sections/total_sections)*100:.1f}%")
        st.metric("Skills Count", len(st.session_state.resume_data['skills']))

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #a78bfa; padding: 2rem;">
    <p>🚀 <strong>AI Resume Builder</strong> - Built with Streamlit & OpenAI</p>
    <p>Created by <strong>Saurabh Parthe</strong> | 
    <a href="https://github.com/parthesaurabh1616/AI_RESUME_BUILDER" style="color: #8b5cf6;">GitHub Repository</a></p>
</div>
""", unsafe_allow_html=True)
