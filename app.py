"""
TalentTalk - AI-Powered Interview System
Main application with authentication and navigation.
"""

import streamlit as st
import auth
import os
import sys

# Page configuration
st.set_page_config(
    page_title="TalentTalk - AI Interview System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize authentication
auth.init_session_state()

# Check if user is authenticated
if not auth.is_authenticated():
    auth.render_login_page()
else:
    # User is authenticated - show navigation
    
    # Sidebar navigation
    st.sidebar.title("🎯 TalentTalk")
    st.sidebar.markdown("---")
    
    # Navigation menu
    st.sidebar.header("Navigation")
    page = st.sidebar.radio(
        "Choose Interview Type:",
        [
            "🏠 Home",
            "💬 Text Interview",
            "🎤 Voice Interview (Whisper)",
            "☁️ Voice Interview (AssemblyAI)"
        ],
        label_visibility="collapsed"
    )
    
    # Logout button
    auth.render_logout_button()
    
    # Main content area
    if page == "🏠 Home":
        # Home page
        st.title("Welcome to TalentTalk!")
        st.markdown("### AI-Powered Interview System")
        
        # Welcome message
        user_info = st.session_state.user_info
        st.success(f"👋 Hello, **{user_info['name']}**! Welcome back.")
        
        # Introduction
        st.markdown("---")
        st.markdown("""
        ## About TalentTalk
        
        TalentTalk is an advanced AI-powered interview system that conducts technical interviews,
        evaluates candidate responses, and generates comprehensive reports.
        
        ### 🌟 Key Features
        
        - **Multiple Interview Modes**: Choose between text-based or voice-based interviews
        - **Dynamic Resume Analysis**: Upload any resume for personalized questions
        - **Customizable Questions**: Upload your own interview questions or use defaults
        - **Voice Interaction**: Speak with the AI interviewer using Whisper (local) or AssemblyAI (cloud)
        - **Automatic Evaluation**: Get detailed scoring and feedback on performance
        - **Professional Reports**: Generate comprehensive HR reports with PDF export
        
        ### 📋 Interview Types
        
        #### 💬 Text Interview
        - Type your responses in a chat interface
        - Best for: Quick interviews, detailed written responses
        - No special setup required
        
        #### 🎤 Voice Interview (Whisper)
        - Local speech recognition using OpenAI Whisper
        - Best for: Privacy-conscious interviews, offline operation
        - Requires: Microphone access
        
        #### ☁️ Voice Interview (AssemblyAI)
        - Cloud-based speech recognition
        - Best for: High-accuracy transcription, real-time processing
        - Requires: AssemblyAI API key, microphone access
        
        ### 🚀 Getting Started
        
        1. Select an interview type from the sidebar
        2. Configure interview settings (position, company, etc.)
        3. Upload your resume or use the default
        4. Start the interview and answer questions
        5. Receive evaluation and download your report
        
        ### ⚙️ Interview Configuration
        
        Each interview type allows you to customize:
        - **Interviewer Mode**: Friendly, Formal, or Technical
        - **Position**: Job title for the interview
        - **Company Name**: Company conducting the interview
        - **Number of Questions**: Technical questions to ask
        - **Follow-up Questions**: Additional clarification questions
        
        ### 📊 Evaluation & Reports
        
        After completing your interview, you'll receive:
        - ✅ Detailed evaluation of each response
        - 📈 Overall performance scoring
        - 💡 Strengths and areas for improvement
        - 📄 Professional PDF report for download
        
        ---
        
        **Ready to start?** Choose an interview type from the sidebar! 👈
        """)
        
        # System status
        st.markdown("---")
        st.markdown("### 🔧 System Status")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Authentication", "✅ Active")
        
        with col2:
            # Check if required directories exist
            dirs_exist = all([
                os.path.exists("generated_reports"),
                os.path.exists("uploaded_resumes"),
                os.path.exists("uploaded_questions")
            ])
            st.metric("Directories", "✅ Ready" if dirs_exist else "⚠️ Check Setup")
        
        with col3:
            # Check if .env file exists
            env_exists = os.path.exists(".env")
            st.metric("API Keys", "✅ Configured" if env_exists else "⚠️ Setup .env")
        
        if not env_exists:
            st.warning(
                "⚠️ **API Keys Not Configured**: "
                "Please create a `.env` file based on `.env.example` and add your API keys."
            )
    
    elif page == "💬 Text Interview":
        st.info("🔄 Loading Text Interview...")
        # Import and run text interview app
        try:
            # Add authentication check at the top of the imported module
            exec(open("text_interview_app.py").read())
        except Exception as e:
            st.error(f"❌ Error loading Text Interview: {str(e)}")
            st.info("Make sure all dependencies are installed and API keys are configured.")
    
    elif page == "🎤 Voice Interview (Whisper)":
        st.info("🔄 Loading Voice Interview (Whisper)...")
        # Import and run whisper voice interview app
        try:
            exec(open("voice_interview_app_whisper.py").read())
        except Exception as e:
            st.error(f"❌ Error loading Voice Interview (Whisper): {str(e)}")
            st.info("Make sure all dependencies are installed and API keys are configured.")
    
    elif page == "☁️ Voice Interview (AssemblyAI)":
        st.info("🔄 Loading Voice Interview (AssemblyAI)...")
        # Import and run AssemblyAI voice interview app
        try:
            exec(open("voice_interview_app_assemblyai.py").read())
        except Exception as e:
            st.error(f"❌ Error loading Voice Interview (AssemblyAI): {str(e)}")
            st.info("Make sure all dependencies are installed and API keys are configured.")
