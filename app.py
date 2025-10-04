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

# Custom CSS for attractive design
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        letter-spacing: -0.02em;
    }
    
    .sub-header {
        font-size: 1.3rem;
        font-weight: 400;
        text-align: center;
        color: #64748b;
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    
    .section-header {
        font-size: 2rem;
        font-weight: 700;
        color: #1e293b;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        color: #1e293b;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        text-align: center;
        margin: 0.5rem;
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.15);
    }
    
    .metric-number {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 1rem;
        color: #64748b;
        font-weight: 500;
    }
    
    .resume-preview {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
        margin: 1rem 0;
    }
    
    .ai-badge {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 600;
        display: inline-block;
        margin: 0.25rem;
    }
    
    .cta-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 50px;
        text-decoration: none;
        font-weight: 600;
        font-size: 1.1rem;
        display: inline-block;
        margin: 0.5rem;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
    }
    
    .cta-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
    }
    
    .hero-section {
        background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
        padding: 3rem 2rem;
        border-radius: 25px;
        margin: 2rem 0;
        text-align: center;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        height: 8px;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    .skill-tag {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        margin: 0.2rem;
        display: inline-block;
    }
    
    .template-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        margin: 1rem;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .template-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }
    
    .template-card.selected {
        border: 3px solid #667eea;
        background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
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
        <h2 style="color: #667eea; margin: 0;">🚀 AI Resume Builder</h2>
        <p style="color: #64748b; margin: 0.5rem 0;">Powered by OpenAI GPT</p>
    </div>
    """, unsafe_allow_html=True)
    
    selected = option_menu(
        menu_title="Navigation",
        options=["Dashboard", "Personal Info", "Experience", "Education", "Skills", "Projects", "AI Assistant", "Templates", "Preview", "Export"],
        icons=["speedometer2", "person", "briefcase", "mortarboard", "tools", "folder", "robot", "layout", "eye", "download"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "#667eea", "font-size": "18px"},
            "nav-link": {
                "font-size": "14px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": "#667eea"},
        }
    )

# Dashboard Page
if selected == "Dashboard":
    st.markdown('<h1 class="main-header">AI Resume Builder</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Create professional, ATS-friendly resumes with the power of AI</p>', unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h2 style="color: #1e293b; margin-bottom: 1rem;">🎯 Why Choose Our AI Resume Builder?</h2>
        <p style="color: #64748b; font-size: 1.1rem; margin-bottom: 2rem;">
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
            <h3 style="color: #667eea; margin-bottom: 1rem;">🤖 AI-Powered Content</h3>
            <p>Generate professional content using OpenAI GPT-3.5. Get suggestions for skills, 
            experience descriptions, and achievement highlights.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #667eea; margin-bottom: 1rem;">📊 ATS Optimization</h3>
            <p>Our AI analyzes job descriptions and optimizes your resume to pass Applicant 
            Tracking Systems (ATS) used by 98% of companies.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #667eea; margin-bottom: 1rem;">🎨 Professional Templates</h3>
            <p>Choose from 50+ professionally designed templates that are both visually 
            appealing and ATS-friendly.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #667eea; margin-bottom: 1rem;">📱 Real-time Preview</h3>
            <p>See your resume come to life with real-time preview. Make changes and see 
            instant updates across all templates.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Progress Tracking
    st.markdown('<h2 class="section-header">📈 Resume Completion Progress</h2>', unsafe_allow_html=True)
    
    progress_data = {
        'Section': ['Personal Info', 'Experience', 'Education', 'Skills', 'Projects', 'Achievements'],
        'Completion': [80, 60, 70, 90, 40, 30]
    }
    
    df_progress = pd.DataFrame(progress_data)
    
    fig = px.bar(df_progress, x='Completion', y='Section', orientation='h',
                title="Resume Sections Completion",
                color='Completion',
                color_continuous_scale='viridis')
    
    fig.update_layout(
        height=400,
        showlegend=False,
        xaxis_title="Completion %",
        yaxis_title="Sections"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
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
            <h3 style="color: #667eea; margin-bottom: 1rem;">Basic Information</h3>
        </div>
        """, unsafe_allow_html=True)
        
        name = st.text_input("Full Name", value=st.session_state.resume_data['personal_info'].get('name', ''))
        email = st.text_input("Email", value=st.session_state.resume_data['personal_info'].get('email', ''))
        phone = st.text_input("Phone Number", value=st.session_state.resume_data['personal_info'].get('phone', ''))
        location = st.text_input("Location", value=st.session_state.resume_data['personal_info'].get('location', ''))
        
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #667eea; margin-bottom: 1rem;">Professional Summary</h3>
        </div>
        """, unsafe_allow_html=True)
        
        summary = st.text_area("Professional Summary", 
                             value=st.session_state.resume_data['personal_info'].get('summary', ''),
                             height=150,
                             help="Write a compelling 2-3 sentence summary of your professional background")
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #667eea; margin-bottom: 1rem;">Social Links</h3>
        </div>
        """, unsafe_allow_html=True)
        
        linkedin = st.text_input("LinkedIn URL", value=st.session_state.resume_data['personal_info'].get('linkedin', ''))
        github = st.text_input("GitHub URL", value=st.session_state.resume_data['personal_info'].get('github', ''))
        portfolio = st.text_input("Portfolio Website", value=st.session_state.resume_data['personal_info'].get('portfolio', ''))
        
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #667eea; margin-bottom: 1rem;">AI Assistant</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🤖 Generate Professional Summary", key="gen_summary"):
            if setup_openai():
                job_title = st.text_input("Your Job Title", placeholder="e.g., Software Engineer")
                if job_title:
                    prompt = f"Write a professional summary for a {job_title} with 2-3 sentences highlighting key skills and achievements"
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
            <h3 style="color: #667eea; margin-bottom: 1rem;">Add Work Experience</h3>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("experience_form"):
            job_title = st.text_input("Job Title")
            company = st.text_input("Company Name")
            location = st.text_input("Location")
            
            col_start, col_end = st.columns(2)
            with col_start:
                start_date = st.date_input("Start Date")
            with col_end:
                end_date = st.date_input("End Date", value=None)
            
            current_job = st.checkbox("Currently Working Here")
            
            description = st.text_area("Job Description", height=100,
                                     help="Describe your key responsibilities and achievements")
            
            achievements = st.text_area("Key Achievements", height=100,
                                      help="List your major accomplishments with metrics")
            
            if st.form_submit_button("➕ Add Experience"):
                if job_title and company and description:
                    experience = {
                        'job_title': job_title,
                        'company': company,
                        'location': location,
                        'start_date': start_date.strftime('%Y-%m-%d'),
                        'end_date': end_date.strftime('%Y-%m-%d') if end_date else None,
                        'current': current_job,
                        'description': description,
                        'achievements': achievements
                    }
                    st.session_state.resume_data['experience'].append(experience)
                    st.success("Experience added successfully!")
                    st.rerun()
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #667eea; margin-bottom: 1rem;">AI Assistant</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🤖 Generate Job Description"):
            if setup_openai():
                role = st.text_input("Job Role", placeholder="e.g., Software Engineer")
                if role:
                    prompt = f"Write a professional job description for a {role} highlighting key responsibilities and achievements with metrics"
                    ai_description = generate_ai_content(prompt)
                    if ai_description:
                        st.text_area("AI-Generated Description", value=ai_description, height=200)
        
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #667eea; margin-bottom: 1rem;">Experience List</h3>
        </div>
        """, unsafe_allow_html=True)
        
        for i, exp in enumerate(st.session_state.resume_data['experience']):
            with st.expander(f"{exp['job_title']} at {exp['company']}"):
                st.write(f"**Period:** {exp['start_date']} - {exp['end_date'] or 'Present'}")
                st.write(f"**Location:** {exp['location']}")
                st.write(f"**Description:** {exp['description']}")
                if exp['achievements']:
                    st.write(f"**Achievements:** {exp['achievements']}")
                
                if st.button(f"🗑️ Delete", key=f"del_exp_{i}"):
                    st.session_state.resume_data['experience'].pop(i)
                    st.rerun()

# Skills Page
elif selected == "Skills":
    st.markdown('<h2 class="section-header">🛠️ Skills & Technologies</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #667eea; margin-bottom: 1rem;">Add Skills</h3>
        </div>
        """, unsafe_allow_html=True)
        
        skill_categories = {
            'Programming Languages': ['Python', 'JavaScript', 'Java', 'C++', 'TypeScript', 'Go', 'Rust'],
            'Frameworks & Libraries': ['React', 'Node.js', 'Django', 'FastAPI', 'Spring Boot', 'Angular', 'Vue.js'],
            'Cloud & DevOps': ['AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Terraform', 'Jenkins'],
            'Databases': ['PostgreSQL', 'MongoDB', 'MySQL', 'Redis', 'Elasticsearch', 'Cassandra'],
            'AI/ML': ['TensorFlow', 'PyTorch', 'Scikit-learn', 'OpenAI API', 'Pandas', 'NumPy'],
            'Tools': ['Git', 'Linux', 'VS Code', 'Jira', 'Confluence', 'Slack', 'Figma']
        }
        
        selected_category = st.selectbox("Select Category", list(skill_categories.keys()))
        
        if selected_category:
            available_skills = skill_categories[selected_category]
            selected_skills = st.multiselect(
                f"Select {selected_category}",
                available_skills,
                default=st.session_state.resume_data['skills']
            )
            
            if st.button("💾 Save Skills"):
                st.session_state.resume_data['skills'] = selected_skills
                st.success("Skills saved successfully!")
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #667eea; margin-bottom: 1rem;">Skills Visualization</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.resume_data['skills']:
            # Create skills distribution chart
            skills_data = {
                'Category': ['Programming', 'Frameworks', 'Cloud', 'Databases', 'AI/ML', 'Tools'],
                'Count': [8, 6, 5, 4, 3, 2]  # Example data
            }
            
            df_skills = pd.DataFrame(skills_data)
            
            fig = px.pie(df_skills, values='Count', names='Category',
                        title="Skills Distribution",
                        color_discrete_sequence=px.colors.qualitative.Set3)
            
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #667eea; margin-bottom: 1rem;">Current Skills</h3>
        </div>
        """, unsafe_allow_html=True)
        
        for skill in st.session_state.resume_data['skills']:
            st.markdown(f'<span class="skill-tag">{skill}</span>', unsafe_allow_html=True)

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
            <h3 style="color: #667eea; margin-bottom: 1rem;">AI Content Generator</h3>
        </div>
        """, unsafe_allow_html=True)
        
        content_type = st.selectbox(
            "What would you like to generate?",
            ["Professional Summary", "Job Description", "Achievement Bullets", "Skills Suggestions", "Cover Letter"]
        )
        
        if content_type == "Professional Summary":
            job_title = st.text_input("Your Job Title")
            years_exp = st.number_input("Years of Experience", min_value=0, max_value=50)
            
            if st.button("🤖 Generate Summary"):
                prompt = f"Write a professional summary for a {job_title} with {years_exp} years of experience"
                ai_content = generate_ai_content(prompt)
                if ai_content:
                    st.text_area("Generated Summary", value=ai_content, height=200)
        
        elif content_type == "Job Description":
            role = st.text_input("Job Role")
            industry = st.text_input("Industry")
            
            if st.button("🤖 Generate Description"):
                prompt = f"Write a detailed job description for a {role} in the {industry} industry"
                ai_content = generate_ai_content(prompt)
                if ai_content:
                    st.text_area("Generated Description", value=ai_content, height=200)
        
        elif content_type == "Achievement Bullets":
            project = st.text_input("Project/Work Description")
            
            if st.button("🤖 Generate Achievements"):
                prompt = f"Write 3-5 achievement bullet points for this work: {project}. Include metrics and impact."
                ai_content = generate_ai_content(prompt)
                if ai_content:
                    st.text_area("Generated Achievements", value=ai_content, height=200)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #667eea; margin-bottom: 1rem;">Resume Analysis</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📊 Analyze Resume"):
            # Analyze resume completeness
            personal_score = len([v for v in st.session_state.resume_data['personal_info'].values() if v]) / 8 * 100
            experience_score = len(st.session_state.resume_data['experience']) * 20
            skills_score = len(st.session_state.resume_data['skills']) * 2
            
            total_score = min(100, (personal_score + experience_score + skills_score) / 3)
            
            st.metric("Resume Completeness", f"{total_score:.1f}%")
            
            # Progress bar
            st.markdown(f"""
            <div class="progress-bar" style="width: {total_score}%;"></div>
            """, unsafe_allow_html=True)
            
            # Suggestions
            suggestions = []
            if personal_score < 80:
                suggestions.append("Complete personal information")
            if experience_score < 60:
                suggestions.append("Add more work experience")
            if skills_score < 80:
                suggestions.append("Add more relevant skills")
            
            if suggestions:
                st.markdown("**Suggestions:**")
                for suggestion in suggestions:
                    st.markdown(f"• {suggestion}")
        
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #667eea; margin-bottom: 1rem;">ATS Optimization</h3>
        </div>
        """, unsafe_allow_html=True)
        
        job_description = st.text_area("Paste Job Description", height=150)
        
        if st.button("🎯 Optimize for ATS"):
            if job_description:
                prompt = f"Analyze this job description and suggest keywords to include in a resume: {job_description}"
                ai_suggestions = generate_ai_content(prompt)
                if ai_suggestions:
                    st.text_area("ATS Optimization Suggestions", value=ai_suggestions, height=200)

# Templates Page
elif selected == "Templates":
    st.markdown('<h2 class="section-header">🎨 Resume Templates</h2>', unsafe_allow_html=True)
    
    templates = {
        'Modern': {
            'description': 'Clean, modern design with subtle colors',
            'features': ['ATS-friendly', 'Mobile responsive', 'Professional']
        },
        'Creative': {
            'description': 'Bold design for creative professionals',
            'features': ['Eye-catching', 'Colorful', 'Unique']
        },
        'Minimal': {
            'description': 'Simple, elegant design',
            'features': ['Clean', 'Focused', 'Timeless']
        },
        'Technical': {
            'description': 'Perfect for tech professionals',
            'features': ['Code-friendly', 'Technical', 'Structured']
        }
    }
    
    cols = st.columns(2)
    
    for i, (template_name, template_info) in enumerate(templates.items()):
        with cols[i % 2]:
            is_selected = st.session_state.resume_data['template'] == template_name.lower()
            
            st.markdown(f"""
            <div class="template-card {'selected' if is_selected else ''}" onclick="selectTemplate('{template_name.lower()}')">
                <h3 style="color: #667eea; margin-bottom: 1rem;">{template_name}</h3>
                <p style="color: #64748b; margin-bottom: 1rem;">{template_info['description']}</p>
                <div style="margin-bottom: 1rem;">
            """, unsafe_allow_html=True)
            
            for feature in template_info['features']:
                st.markdown(f'<span class="ai-badge">{feature}</span>', unsafe_allow_html=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True)
            
            if st.button(f"Select {template_name}", key=f"select_{template_name.lower()}"):
                st.session_state.resume_data['template'] = template_name.lower()
                st.success(f"{template_name} template selected!")
                st.rerun()

# Preview Page
elif selected == "Preview":
    st.markdown('<h2 class="section-header">👁️ Resume Preview</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="resume-preview">
            <h2 style="color: #1e293b; text-align: center; margin-bottom: 2rem;">
                {name}
            </h2>
            <div style="text-align: center; margin-bottom: 2rem; color: #64748b;">
                {email} | {phone} | {location}
            </div>
            
            <h3 style="color: #667eea; border-bottom: 2px solid #667eea; padding-bottom: 0.5rem;">
                Professional Summary
            </h3>
            <p style="margin-bottom: 2rem;">{summary}</p>
            
            <h3 style="color: #667eea; border-bottom: 2px solid #667eea; padding-bottom: 0.5rem;">
                Work Experience
            </h3>
        """.format(
            name=st.session_state.resume_data['personal_info'].get('name', 'Your Name'),
            email=st.session_state.resume_data['personal_info'].get('email', 'your.email@example.com'),
            phone=st.session_state.resume_data['personal_info'].get('phone', '+1 (555) 123-4567'),
            location=st.session_state.resume_data['personal_info'].get('location', 'Your Location'),
            summary=st.session_state.resume_data['personal_info'].get('summary', 'Your professional summary will appear here.')
        ), unsafe_allow_html=True)
        
        for exp in st.session_state.resume_data['experience']:
            st.markdown(f"""
            <div style="margin-bottom: 1.5rem;">
                <h4 style="color: #1e293b; margin: 0;">{exp['job_title']}</h4>
                <p style="color: #667eea; margin: 0.25rem 0; font-weight: 600;">{exp['company']}</p>
                <p style="color: #64748b; margin: 0.25rem 0; font-size: 0.9rem;">
                    {exp['start_date']} - {exp['end_date'] or 'Present'} | {exp['location']}
                </p>
                <p style="margin: 0.5rem 0;">{exp['description']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
            <h3 style="color: #667eea; border-bottom: 2px solid #667eea; padding-bottom: 0.5rem;">
                Skills
            </h3>
            <div style="margin-bottom: 2rem;">
        """, unsafe_allow_html=True)
        
        for skill in st.session_state.resume_data['skills']:
            st.markdown(f'<span class="skill-tag">{skill}</span>', unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #667eea; margin-bottom: 1rem;">Preview Options</h3>
        </div>
        """, unsafe_allow_html=True)
        
        template_preview = st.selectbox("Template", ["Modern", "Creative", "Minimal", "Technical"])
        
        if st.button("🔄 Refresh Preview"):
            st.rerun()
        
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #667eea; margin-bottom: 1rem;">Quick Stats</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.metric("Sections Completed", f"{len([k for k, v in st.session_state.resume_data.items() if v])}/6")
        st.metric("Experience Entries", len(st.session_state.resume_data['experience']))
        st.metric("Skills Listed", len(st.session_state.resume_data['skills']))

# Export Page
elif selected == "Export":
    st.markdown('<h2 class="section-header">📥 Export Resume</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #667eea; margin-bottom: 1rem;">Export Options</h3>
        </div>
        """, unsafe_allow_html=True)
        
        export_format = st.selectbox("Export Format", ["PDF", "Word Document", "Plain Text", "JSON"])
        
        if st.button("📄 Generate PDF"):
            # Create PDF using reportlab
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []
            
            # Add content to PDF
            personal_info = st.session_state.resume_data['personal_info']
            
            # Name
            name_style = ParagraphStyle('NameStyle', parent=styles['Heading1'], fontSize=24, spaceAfter=30)
            story.append(Paragraph(personal_info.get('name', 'Your Name'), name_style))
            
            # Contact info
            contact_info = f"{personal_info.get('email', '')} | {personal_info.get('phone', '')} | {personal_info.get('location', '')}"
            story.append(Paragraph(contact_info, styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Summary
            if personal_info.get('summary'):
                story.append(Paragraph("Professional Summary", styles['Heading2']))
                story.append(Paragraph(personal_info['summary'], styles['Normal']))
                story.append(Spacer(1, 20))
            
            # Experience
            if st.session_state.resume_data['experience']:
                story.append(Paragraph("Work Experience", styles['Heading2']))
                for exp in st.session_state.resume_data['experience']:
                    story.append(Paragraph(f"{exp['job_title']} at {exp['company']}", styles['Heading3']))
                    story.append(Paragraph(f"{exp['start_date']} - {exp['end_date'] or 'Present'}", styles['Normal']))
                    story.append(Paragraph(exp['description'], styles['Normal']))
                    story.append(Spacer(1, 12))
            
            # Skills
            if st.session_state.resume_data['skills']:
                story.append(Paragraph("Skills", styles['Heading2']))
                skills_text = ", ".join(st.session_state.resume_data['skills'])
                story.append(Paragraph(skills_text, styles['Normal']))
            
            doc.build(story)
            buffer.seek(0)
            
            st.download_button(
                label="📥 Download PDF",
                data=buffer.getvalue(),
                file_name=f"resume_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf"
            )
        
        if st.button("📄 Generate Word Document"):
            st.info("Word document generation coming soon!")
        
        if st.button("📄 Export as JSON"):
            json_data = json.dumps(st.session_state.resume_data, indent=2)
            st.download_button(
                label="📥 Download JSON",
                data=json_data,
                file_name=f"resume_data_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #667eea; margin-bottom: 1rem;">Export Summary</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Resume statistics
        total_sections = len(st.session_state.resume_data)
        completed_sections = len([k for k, v in st.session_state.resume_data.items() if v])
        
        st.metric("Completion Rate", f"{(completed_sections/total_sections)*100:.1f}%")
        st.metric("Experience Entries", len(st.session_state.resume_data['experience']))
        st.metric("Skills Count", len(st.session_state.resume_data['skills']))
        
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #667eea; margin-bottom: 1rem;">Tips for Export</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        - **PDF Format**: Best for ATS systems and general applications
        - **Word Format**: Good for manual editing and customization
        - **Plain Text**: Useful for online applications and email
        - **JSON Format**: For data backup and integration with other tools
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; padding: 2rem;">
    <p>🚀 <strong>AI Resume Builder</strong> - Built with Streamlit & OpenAI</p>
    <p>Created by <strong>Saurabh Parthe</strong> | 
    <a href="https://github.com/parthesaurabh1616/AI_RESUME_BUILDER" style="color: #667eea;">GitHub Repository</a></p>
</div>
""", unsafe_allow_html=True)
