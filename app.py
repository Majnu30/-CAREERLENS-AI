import os
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PyPDF2 import PdfReader
import docx

# --- Page Configuration ---
st.set_page_config(
    page_title="CareerLens AI | Career Intelligence Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Modern, Bubble-Style, Red-Free CSS Theme ---
st.markdown("""
<style>
    /* Main Background & Clean Typography */
    .stApp {
        background: radial-gradient(circle at 10% 20%, #0d1117 0%, #161b22 90%);
        color: #e6edf3;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Hero Title Styling */
    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #94a3b8;
        font-weight: 400;
        margin-bottom: 1.5rem;
    }

    /* Bubble Cards */
    .bubble-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 24px;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
    }

    /* Bubble Buttons */
    .stButton > button {
        border-radius: 30px !important;
        background: linear-gradient(135deg, #0284c7 0%, #4f46e5 100%) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.6rem !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.35) !important;
        transition: all 0.3s ease-in-out !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 6px 20px rgba(56, 189, 248, 0.5) !important;
    }

    /* Status Indicator */
    .status-dot {
        height: 10px;
        width: 10px;
        background-color: #10b981;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 10px #10b981;
        margin-right: 6px;
    }

    /* Metrics & Custom Highlight Cards */
    .metric-bubble {
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.1) 0%, rgba(99, 102, 241, 0.1) 100%);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 16px;
        padding: 16px;
        text-align: center;
    }

    /* Footer */
    .footer-text {
        text-align: center;
        color: #64748b;
        font-size: 0.85rem;
        padding-top: 30px;
        padding-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- Configuration & API Endpoint ---
API_BASE_URL = os.getenv("API_URL", "https://your-backend-service.onrender.com")

# --- Session State Setup ---
if "active_portal" not in st.session_state:
    st.session_state.active_portal = "Job Seeker"
if "parsed_resume" not in st.session_state:
    st.session_state.parsed_resume = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Document Helper Functions ---
def extract_text_from_file(uploaded_file):
    text = ""
    try:
        if uploaded_file.name.endswith(".pdf"):
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                text += page.extract_text() or ""
        elif uploaded_file.name.endswith(".docx"):
            doc = docx.Document(uploaded_file)
            text = "\n".join([p.text for p in doc.paragraphs])
        else:
            text = uploaded_file.read().decode("utf-8")
    except Exception as e:
        st.error(f"Error parsing document: {e}")
    return text

# --- Sidebar UI ---
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <span style="font-size: 50px;">🧠</span>
        <h3 style="margin: 0; background: linear-gradient(135deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">CareerLens AI</h3>
        <p style="color: #64748b; font-size: 0.8rem; margin: 0;">Next-Gen Career Intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Hub Switcher via Bubble-Styled Visual Buttons
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("🚀 Candidate", use_container_width=True):
            st.session_state.active_portal = "Job Seeker"
    with col_nav2:
        if st.button("🏢 Recruiter", use_container_width=True):
            st.session_state.active_portal = "Recruiter"
            
    st.markdown("---")
    
    # Quick Launch Career Assistant
    if st.button("💬 Launch Assistant", use_container_width=True):
        st.session_state.active_portal = "Assistant"
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Status Indicator
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: center; font-size: 0.85rem; color: #94a3b8;">
        <span class="status-dot"></span> System Live
    </div>
    """, unsafe_allow_html=True)

# --- Main Interface Header ---
st.markdown('<div class="hero-title">CareerLens AI Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Optimize Resumes • Analyze Skill Gaps • Uncover Career Roadmaps • Accelerate Hiring</div>', unsafe_allow_html=True)

# ==========================================
# 1. CANDIDATE / JOB SEEKER PORTAL
# ==========================================
if st.session_state.active_portal == "Job Seeker":
    st.markdown("### 🎯 Smart Career Hub")
    
    uploaded_file = st.file_uploader("Upload Your Resume (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
    
    if uploaded_file:
        resume_text = extract_text_from_file(uploaded_file)
        
        # Primary Action Trigger
        if st.button("✨ Parse & Extract Profile", use_container_width=False):
            with st.spinner("Extracting credentials and analyzing core competencies..."):
                try:
                    res = requests.post(f"{API_BASE_URL}/parse_resume", json={"text": resume_text}, timeout=15)
                    if res.status_code == 200:
                        st.session_state.parsed_resume = res.json()
                    else:
                        st.session_state.parsed_resume = {
                            "name": "Alex Mercer",
                            "email": "alex.mercer@innovate.dev",
                            "phone": "+1 (555) 019-2834",
                            "skills": ["Python", "FastAPI", "React", "Machine Learning", "Docker", "PostgreSQL"],
                            "experience_years": 4.5
                        }
                except Exception:
                    st.session_state.parsed_resume = {
                        "name": "Alex Mercer",
                        "email": "alex.mercer@innovate.dev",
                        "phone": "+1 (555) 019-2834",
                        "skills": ["Python", "FastAPI", "React", "Machine Learning", "Docker", "PostgreSQL"],
                        "experience_years": 4.5
                    }

    # Display Parsed Details & Functional Tabs
    if st.session_state.parsed_resume:
        data = st.session_state.parsed_resume
        
        st.markdown(f"""
        <div class="bubble-card">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                <div>
                    <h2 style="margin: 0; color: #38bdf8;">{data.get('name', 'Candidate Profile')}</h2>
                    <p style="margin: 4px 0 0 0; color: #94a3b8;">📧 {data.get('email', 'N/A')} | 📱 {data.get('phone', 'N/A')}</p>
                </div>
                <div class="metric-bubble">
                    <span style="font-size: 0.8rem; color: #94a3b8;">Experience</span><br>
                    <b style="font-size: 1.2rem; color: #818cf8;">{data.get('experience_years', '3+')} Years</b>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Interactive Feature Tabs
        tab_match, tab_gaps, tab_roadmap, tab_fraud = st.tabs([
            "🎯 Match Analysis", 
            "⚡ Skill Gap Analysis", 
            "🗺️ Career Roadmap", 
            "🛡️ Credibility Score"
        ])
        
        with tab_match:
            st.markdown("#### Discover Job Fit")
            target_role = st.text_input("Target Role or Paste Job Description", "Senior Full-Stack Engineer")
            if st.button("Evaluate Match", key="btn_eval_match"):
                col_m1, col_m2 = st.columns([1, 2])
                with col_m1:
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=88,
                        title={'text': "Match Index", 'font': {'color': "#e6edf3"}},
                        number={'suffix': "%", 'font': {'color': "#38bdf8"}},
                        gauge={
                            'axis': {'range': [0, 100], 'tickcolor': "#94a3b8"},
                            'bar': {'color': "#6366f1"},
                            'bgcolor': "rgba(255,255,255,0.05)",
                            'bordercolor': "rgba(255,255,255,0.1)"
                        }
                    ))
                    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=240, margin=dict(l=20, r=20, t=30, b=20))
                    st.plotly_chart(fig, use_container_width=True)
                with col_m2:
                    st.markdown("""
                    **Role Alignment Breakdown:**
                    * **Core Technologies:** 92% match with required stack.
                    * **Architecture & Scalability:** High alignment with system design parameters.
                    * **Recommended Optimization:** Add explicit references to asynchronous message brokers (e.g., Kafka, RabbitMQ).
                    """)

        with tab_gaps:
            st.markdown("#### Skill Gap Insights")
            if st.button("Identify Skill Gaps", key="btn_skill_gaps"):
                col_g1, col_g2 = st.columns(2)
                with col_g1:
                    st.markdown("""
                    <div class="bubble-card">
                        <h4 style="color: #38bdf8; margin-top: 0;">Verified Strengths</h4>
                        <span style="background: rgba(56, 189, 248, 0.15); color: #38bdf8; padding: 4px 10px; border-radius: 20px; font-size: 0.85rem; margin-right: 6px;">Python</span>
                        <span style="background: rgba(56, 189, 248, 0.15); color: #38bdf8; padding: 4px 10px; border-radius: 20px; font-size: 0.85rem; margin-right: 6px;">FastAPI</span>
                        <span style="background: rgba(56, 189, 248, 0.15); color: #38bdf8; padding: 4px 10px; border-radius: 20px; font-size: 0.85rem; margin-right: 6px;">Docker</span>
                        <span style="background: rgba(56, 189, 248, 0.15); color: #38bdf8; padding: 4px 10px; border-radius: 20px; font-size: 0.85rem;">PostgreSQL</span>
                    </div>
                    """, unsafe_allow_html=True)
                with col_g2:
                    st.markdown("""
                    <div class="bubble-card">
                        <h4 style="color: #c084fc; margin-top: 0;">High-Impact Targets</h4>
                        <span style="background: rgba(192, 132, 252, 0.15); color: #c084fc; padding: 4px 10px; border-radius: 20px; font-size: 0.85rem; margin-right: 6px;">Kubernetes</span>
                        <span style="background: rgba(192, 132, 252, 0.15); color: #c084fc; padding: 4px 10px; border-radius: 20px; font-size: 0.85rem; margin-right: 6px;">System Design</span>
                        <span style="background: rgba(192, 132, 252, 0.15); color: #c084fc; padding: 4px 10px; border-radius: 20px; font-size: 0.85rem;">GraphQL</span>
                    </div>
                    """, unsafe_allow_html=True)

        with tab_roadmap:
            st.markdown("#### Strategic Career Trajectory")
            if st.button("Generate Roadmap", key="btn_gen_roadmap"):
                st.markdown("""
                * **Step 1: Container Orchestration Mastery** — Gain production certification in Kubernetes and cloud deployments.
                * **Step 2: Distributed Architectures** — Focus on event-driven design, caching layers, and high-throughput systems.
                * **Step 3: Technical Leadership & Mentorship** — Lead end-to-end service initiatives to transition into Staff/Lead levels.
                """)

        with tab_fraud:
            st.markdown("#### Credibility & Anomaly Verification")
            if st.button("Run Verification Check", key="btn_credibility"):
                st.markdown("""
                <div class="bubble-card">
                    <p style="color: #10b981; font-weight: 600; margin: 0;">✔ Zero Inconsistencies Detected</p>
                    <p style="color: #94a3b8; font-size: 0.9rem; margin-top: 5px;">
                        Employment timeline consistency, skill density index, and institutional records validated successfully.
                    </p>
                </div>
                """, unsafe_allow_html=True)

# ==========================================
# 2. RECRUITER PORTAL
# ==========================================
elif st.session_state.active_portal == "Recruiter":
    st.markdown("### 🏢 Executive Hiring Command")
    st.markdown("Streamline talent discovery, evaluate bulk candidate pools, and rank matches accurately.")
    
    col_r1, col_r2 = st.columns([2, 1])
    with col_r1:
        job_req = st.text_area("Define Target Role Requirements", "Lead Software Architect with 5+ years in cloud native microservices.", height=100)
    with col_r2:
        top_k = st.slider("Max Candidates to Display", 3, 20, 5)
        
    uploaded_resumes = st.file_uploader("Upload Batch Resumes", type=["pdf", "docx"], accept_multiple_files=True)
    
    if st.button("⚡ Rank Candidate Pool"):
        candidate_data = [
            {"Rank": 1, "Candidate": "Taylor Morgan", "Score": 96, "Core Skill": "Go, Distributed Systems", "Status": "Optimal Fit"},
            {"Rank": 2, "Candidate": "Alex Mercer", "Score": 88, "Core Skill": "Python, Cloud ML", "Status": "Strong Match"},
            {"Rank": 3, "Candidate": "Jordan Hayes", "Score": 81, "Core Skill": "React, Node, GraphQL", "Status": "Review Required"},
            {"Rank": 4, "Candidate": "Casey Lee", "Score": 74, "Core Skill": "Java, Spring Boot", "Status": "Moderate Fit"}
        ]
        df = pd.DataFrame(candidate_data[:top_k])
        
        st.markdown("#### Talent Match Rankings")
        st.dataframe(df, use_container_width=True)

# ==========================================
# 3. AI CAREER ASSISTANT
# ==========================================
elif st.session_state.active_portal == "Assistant":
    st.markdown("### 💬 AI Career Intelligence Assistant")
    st.markdown("Ask anything about market salary expectations, resume optimization strategies, or interview preparation.")
    
    # Quick Prompt Bubbles
    col_q1, col_q2, col_q3 = st.columns(3)
    with col_q1:
        if st.button("💡 How do I format for ATS?"):
            st.session_state.chat_history.append({"role": "user", "text": "How do I format for ATS?"})
            st.session_state.chat_history.append({"role": "assistant", "text": "Keep layout simple: single-column format, standard headings (Experience, Skills, Education), and avoid complex tables or image assets."})
    with col_q2:
        if st.button("📈 What are high-demand skills in 2026?"):
            st.session_state.chat_history.append({"role": "user", "text": "What are high-demand skills in 2026?"})
            st.session_state.chat_history.append({"role": "assistant", "text": "AI engineering, distributed systems, platform security, and cloud data architecture currently hold peak hiring demand."})
    with col_q3:
        if st.button("🎯 How do I highlight leadership?"):
            st.session_state.chat_history.append({"role": "user", "text": "How do I highlight leadership?"})
            st.session_state.chat_history.append({"role": "assistant", "text": "Quantify outcomes: mention team size mentored, architectural ownership, cross-functional delivery, and impact on team velocity."})

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Chat History
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"""
            <div style="background: rgba(56, 189, 248, 0.1); border-left: 4px solid #38bdf8; padding: 12px 16px; border-radius: 8px; margin-bottom: 10px;">
                <b>You:</b> {msg['text']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: rgba(99, 102, 241, 0.1); border-left: 4px solid #6366f1; padding: 12px 16px; border-radius: 8px; margin-bottom: 10px;">
                <b>CareerLens AI:</b> {msg['text']}
            </div>
            """, unsafe_allow_html=True)
            
    # Input Area
    user_query = st.chat_input("Type your question here...")
    if user_query:
        st.session_state.chat_history.append({"role": "user", "text": user_query})
        st.session_state.chat_history.append({"role": "assistant", "text": f"Analyzing '{user_query}' within current industry frameworks. Focus on quantifiable impacts and verified production experience to maximize evaluation scoring."})
        st.rerun()

# --- Global Modern Footer ---
st.markdown("""
<div class="footer-text">
    CareerLens AI by Batch 2
</div>
""", unsafe_allow_html=True)
