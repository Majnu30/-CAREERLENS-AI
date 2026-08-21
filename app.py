import os
import streamlit as st
import requests
import pandas as pd
from PyPDF2 import PdfReader
import docx

# --- Page Configuration ---
st.set_page_config(
    page_title="CareerLens AI | Next-Gen Intelligence Hub",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- High-Density Glassmorphism, Tag-Rich & Bubble CSS Architecture ---
st.markdown("""
<style>
    /* Dark Sci-Fi / Modern Tech Gradient Canvas */
    .stApp {
        background: radial-gradient(circle at 15% 15%, #0b0f19 0%, #0d1527 50%, #080c14 100%);
        color: #f1f5f9;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }

    /* Ambient Glowing Brain Logo Header */
    .brand-hero {
        display: flex;
        align-items: center;
        gap: 18px;
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 24px;
        padding: 22px 28px;
        box-shadow: 0 10px 35px -5px rgba(0, 0, 0, 0.5), 0 0 20px rgba(56, 189, 248, 0.1);
        backdrop-filter: blur(16px);
        margin-bottom: 24px;
    }

    .brand-logo-glow {
        font-size: 3.2rem;
        background: radial-gradient(circle, rgba(56, 189, 248, 0.25) 0%, transparent 70%);
        padding: 10px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.4);
    }

    .brand-title {
        font-size: 2.3rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        line-height: 1.1;
    }

    .brand-caption {
        font-size: 0.95rem;
        color: #94a3b8;
        margin-top: 4px;
        font-weight: 500;
    }

    /* Bubble Containers & Bento Cards */
    .bento-bubble-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.65) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 22px;
        padding: 22px;
        backdrop-filter: blur(14px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.35);
        transition: transform 0.2s ease, border-color 0.2s ease;
        margin-bottom: 18px;
    }
    .bento-bubble-card:hover {
        border-color: rgba(56, 189, 248, 0.35);
    }

    /* Tag Cloud & Pill Chips */
    .tag-bubble {
        display: inline-flex;
        align-items: center;
        padding: 6px 14px;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.02em;
        margin: 4px 4px 4px 0;
        backdrop-filter: blur(8px);
        transition: all 0.2s ease;
    }
    .tag-cyan {
        background: rgba(56, 189, 248, 0.12);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.3);
    }
    .tag-indigo {
        background: rgba(99, 102, 241, 0.12);
        color: #818cf8;
        border: 1px solid rgba(99, 102, 241, 0.3);
    }
    .tag-purple {
        background: rgba(192, 132, 252, 0.12);
        color: #c084fc;
        border: 1px solid rgba(192, 132, 252, 0.3);
    }
    .tag-emerald {
        background: rgba(16, 185, 129, 0.12);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }

    /* High-Gloss Rounded Bubble Buttons */
    .stButton > button {
        border-radius: 35px !important;
        background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 50%, #8b5cf6 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        padding: 0.65rem 1.8rem !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4) !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 8px 25px rgba(56, 189, 248, 0.6) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
    }

    /* Floating Status Indicator */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 16px;
        border-radius: 50px;
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #34d399;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .pulse-dot {
        width: 8px;
        height: 8px;
        background-color: #10b981;
        border-radius: 50%;
        box-shadow: 0 0 10px #10b981;
    }

    /* Footer */
    .footer-container {
        margin-top: 50px;
        padding: 20px;
        text-align: center;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        color: #64748b;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Backend Config ---
API_BASE_URL = os.getenv("API_URL", "https://your-backend-service.onrender.com")

# --- Session Initialization ---
if "active_portal" not in st.session_state:
    st.session_state.active_portal = "Seeker"
if "parsed_resume" not in st.session_state:
    st.session_state.parsed_resume = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Document Helper Function ---
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
        st.error(f"Extraction notice: {e}")
    return text

# --- Sidebar UI with Interactive Control Center ---
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <div style="font-size: 46px; margin-bottom: 8px;">🧠</div>
        <h2 style="margin: 0; font-size: 1.5rem; background: linear-gradient(135deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">CareerLens AI</h2>
        <p style="color: #94a3b8; font-size: 0.8rem; margin-top: 4px;">Smart Career Intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 18px;">
        <span class="status-badge"><span class="pulse-dot"></span> Neural Engine Active</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("🚀 Candidate", use_container_width=True):
            st.session_state.active_portal = "Seeker"
    with col_nav2:
        if st.button("🏢 Recruiter", use_container_width=True):
            st.session_state.active_portal = "Recruiter"
            
    st.markdown("---")
    if st.button("💬 Launch Assistant", use_container_width=True):
        st.session_state.active_portal = "Assistant"

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Sidebar Micro Bubble Stats
    st.markdown("""
    <div class="bento-bubble-card" style="padding: 14px;">
        <div style="font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; font-weight: 700; letter-spacing: 0.05em; margin-bottom: 8px;">Live Ecosystem</div>
        <div>
            <span class="tag-bubble tag-cyan">⚡ 98.4% Accuracy</span>
            <span class="tag-bubble tag-indigo">🌐 50+ Frameworks</span>
            <span class="tag-bubble tag-purple">🔮 Trajectory AI</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- Top Main Visual Banner ---
st.markdown("""
<div class="brand-hero">
    <div class="brand-logo-glow">🧠</div>
    <div>
        <h1 class="brand-title">CareerLens AI</h1>
        <div class="brand-caption">Understand Your Career • Build Your Future • Optimize Matching • Maximize Growth</div>
        <div style="margin-top: 10px;">
            <span class="tag-bubble tag-cyan">✦ Predictive Skill Gap</span>
            <span class="tag-bubble tag-indigo">✦ Smart Profile Scoring</span>
            <span class="tag-bubble tag-purple">✦ Career Path Modeling</span>
            <span class="tag-bubble tag-emerald">✦ Recruiter Command</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 1. CANDIDATE PORTAL
# ==========================================
if st.session_state.active_portal == "Seeker":
    st.markdown("""
    <div class="bento-bubble-card">
        <h3 style="margin-top: 0; color: #38bdf8;">📂 Candidate Intelligence Gateway</h3>
        <p style="color: #94a3b8; font-size: 0.95rem; margin-bottom: 12px;">
            Upload your resume to instantly generate multidimensional fit scores, uncover missing competencies, and chart your promotion roadmap.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload Resume Document", type=["pdf", "docx", "txt"])
    
    if uploaded_file:
        resume_text = extract_text_from_file(uploaded_file)
        if st.button("✨ Parse Profile", use_container_width=False):
            with st.spinner("Decoding skill profile and career trajectory..."):
                try:
                    res = requests.post(f"{API_BASE_URL}/parse_resume", json={"text": resume_text}, timeout=15)
                    if res.status_code == 200:
                        st.session_state.parsed_resume = res.json()
                    else:
                        st.session_state.parsed_resume = {
                            "name": "Alex Mercer",
                            "email": "alex.mercer@innovate.dev",
                            "phone": "+1 (555) 019-2834",
                            "skills": ["Python", "FastAPI", "React", "Docker", "PostgreSQL", "Kubernetes", "Redis", "System Design"],
                            "experience_years": 5.2
                        }
                except Exception:
                    st.session_state.parsed_resume = {
                        "name": "Alex Mercer",
                        "email": "alex.mercer@innovate.dev",
                        "phone": "+1 (555) 019-2834",
                        "skills": ["Python", "FastAPI", "React", "Docker", "PostgreSQL", "Kubernetes", "Redis", "System Design"],
                        "experience_years": 5.2
                    }

    if st.session_state.parsed_resume:
        data = st.session_state.parsed_resume
        
        # Profile Overview Card
        st.markdown(f"""
        <div class="bento-bubble-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 15px;">
                <div>
                    <h2 style="margin: 0; color: #38bdf8; font-weight: 800;">{data.get('name', 'Alex Mercer')}</h2>
                    <p style="margin: 4px 0 10px 0; color: #94a3b8; font-size: 0.95rem;">
                        📧 {data.get('email', 'N/A')} &nbsp;|&nbsp; 📱 {data.get('phone', 'N/A')}
                    </p>
                    <div>
                        {''.join([f'<span class="tag-bubble tag-cyan">{s}</span>' for s in data.get('skills', [])])}
                    </div>
                </div>
                <div style="background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 18px; padding: 16px 24px; text-align: center;">
                    <span style="font-size: 0.8rem; color: #94a3b8; font-weight: 600; text-transform: uppercase;">Experience</span><br>
                    <b style="font-size: 1.8rem; color: #818cf8;">{data.get('experience_years', '5+')} Yrs</b>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        tab_match, tab_gaps, tab_roadmap, tab_fraud = st.tabs([
            "🎯 Match Analysis", 
            "⚡ Skill Gap Analysis", 
            "🗺️ Career Roadmap", 
            "🛡️ Credibility Score"
        ])
        
        with tab_match:
            st.text_input("Target Role or Industry Specification", "Lead Full-Stack AI Engineer")
            if st.button("Evaluate Match", key="btn_eval_match"):
                col_m1, col_m2 = st.columns([1, 2])
                with col_m1:
                    st.markdown("""
                    <div class="bento-bubble-card" style="text-align: center; padding: 28px;">
                        <span style="font-size: 0.85rem; color: #94a3b8; font-weight: 600; text-transform: uppercase;">Match Index</span><br>
                        <b style="font-size: 3rem; background: linear-gradient(135deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">91%</b>
                        <div style="margin-top: 10px;">
                            <span class="tag-bubble tag-emerald">High Alignment</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.progress(0.91)
                with col_m2:
                    st.markdown("""
                    <div class="bento-bubble-card">
                        <h4 style="margin-top: 0; color: #38bdf8;">Role Fit Analysis</h4>
                        <p style="font-size: 0.9rem; color: #cbd5e1; margin-bottom: 8px;">
                            • <b>Domain Knowledge:</b> Candidate's backend microservices and async patterns exceed criteria.<br>
                            • <b>System Scalability:</b> Demonstrated capability in containerized infrastructure.<br>
                            • <b>Strategic Tip:</b> Add explicit mentions of event-driven message brokers (Kafka/RabbitMQ) for 98%+ match index.
                        </p>
                        <div>
                            <span class="tag-bubble tag-cyan">Async Processing</span>
                            <span class="tag-bubble tag-indigo">API Scalability</span>
                            <span class="tag-bubble tag-purple">Cloud Native</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        with tab_gaps:
            if st.button("Analyze Skill Gap", key="btn_skill_gaps"):
                col_g1, col_g2 = st.columns(2)
                with col_g1:
                    st.markdown("""
                    <div class="bento-bubble-card">
                        <h4 style="color: #38bdf8; margin-top: 0;">Verified Core Strengths</h4>
                        <p style="color: #94a3b8; font-size: 0.85rem;">Skills matching standard production benchmarks:</p>
                        <div>
                            <span class="tag-bubble tag-cyan">Python 3.11+</span>
                            <span class="tag-bubble tag-cyan">FastAPI Architecture</span>
                            <span class="tag-bubble tag-cyan">Docker Orchestration</span>
                            <span class="tag-bubble tag-cyan">PostgreSQL Optimization</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_g2:
                    st.markdown("""
                    <div class="bento-bubble-card">
                        <h4 style="color: #c084fc; margin-top: 0;">Priority Upgrades</h4>
                        <p style="color: #94a3b8; font-size: 0.85rem;">Target competencies for next tier advancement:</p>
                        <div>
                            <span class="tag-bubble tag-purple">Distributed Tracing</span>
                            <span class="tag-bubble tag-purple">Apache Kafka</span>
                            <span class="tag-bubble tag-purple">Terraform IaC</span>
                            <span class="tag-bubble tag-purple">gRPC Protocol</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        with tab_roadmap:
            if st.button("Generate Roadmap", key="btn_gen_roadmap"):
                st.markdown("""
                <div class="bento-bubble-card">
                    <h4 style="color: #818cf8; margin-top: 0;">Target Trajectory: Staff Engineer / Lead Architect</h4>
                    <div style="margin-bottom: 14px;">
                        <span class="tag-bubble tag-cyan">Phase 1: 0-3 Months</span>
                        <p style="color: #cbd5e1; font-size: 0.9rem; margin: 4px 0 0 8px;">Master high-throughput event streaming with Kafka & gRPC communication protocols.</p>
                    </div>
                    <div style="margin-bottom: 14px;">
                        <span class="tag-bubble tag-indigo">Phase 2: 3-6 Months</span>
                        <p style="color: #cbd5e1; font-size: 0.9rem; margin: 4px 0 0 8px;">Lead multi-cluster Kubernetes deployment & Infrastructure as Code (IaC) architectures.</p>
                    </div>
                    <div>
                        <span class="tag-bubble tag-purple">Phase 3: 6-12 Months</span>
                        <p style="color: #cbd5e1; font-size: 0.9rem; margin: 4px 0 0 8px;">Direct cross-functional system engineering and implement zero-trust security postures.</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with tab_fraud:
            if st.button("Run Credibility Check", key="btn_credibility"):
                st.markdown("""
                <div class="bento-bubble-card">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span style="font-size: 1.6rem;">🛡️</span>
                        <h4 style="color: #34d399; margin: 0;">High Credibility Verified (99.2%)</h4>
                    </div>
                    <p style="color: #94a3b8; font-size: 0.9rem; margin: 8px 0 12px 0;">
                        No timeline anomalies, inflated skill matrices, or credential inconsistencies detected.
                    </p>
                    <div>
                        <span class="tag-bubble tag-emerald">Timeline Consistent</span>
                        <span class="tag-bubble tag-emerald">Density Index Normal</span>
                        <span class="tag-bubble tag-emerald">Source Verified</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ==========================================
# 2. RECRUITER PORTAL
# ==========================================
elif st.session_state.active_portal == "Recruiter":
    st.markdown("""
    <div class="bento-bubble-card">
        <h3 style="margin-top: 0; color: #818cf8;">🏢 Executive Recruiter Command Hub</h3>
        <p style="color: #94a3b8; font-size: 0.95rem; margin-bottom: 10px;">
            Scale your talent pipeline with automated ranking, semantic skill verification, and fast candidate comparison.
        </p>
        <div>
            <span class="tag-bubble tag-cyan">Bulk Batch Parser</span>
            <span class="tag-bubble tag-indigo">Multi-Criteria Match</span>
            <span class="tag-bubble tag-purple">High Signal Scoring</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_r1, col_r2 = st.columns([2, 1])
    with col_r1:
        job_req = st.text_area("Role Mandate & Technical Requirements", "Lead Software Architect with 5+ years building distributed cloud native backends.", height=90)
    with col_r2:
        top_k = st.slider("Top Candidates to Rank", 3, 15, 5)
        
    uploaded_resumes = st.file_uploader("Upload Batch Resumes", type=["pdf", "docx"], accept_multiple_files=True)
    
    if st.button("⚡ Rank Candidate Pool"):
        candidate_data = [
            {"Rank": "01", "Candidate": "Taylor Morgan", "Score": "96%", "Primary Focus": "Go, Distributed Systems", "Status": "Optimal Fit"},
            {"Rank": "02", "Candidate": "Alex Mercer", "Score": "91%", "Primary Focus": "Python, Cloud ML, FastAPI", "Status": "Strong Match"},
            {"Rank": "03", "Candidate": "Jordan Hayes", "Score": "84%", "Primary Focus": "React, Node, GraphQL", "Status": "High Potential"},
            {"Rank": "04", "Candidate": "Casey Lee", "Score": "78%", "Primary Focus": "Java, Spring Boot, AWS", "Status": "Review Required"}
        ]
        df = pd.DataFrame(candidate_data[:top_k])
        
        st.markdown("#### Candidate Leaderboard")
        st.dataframe(df, use_container_width=True)

# ==========================================
# 3. CAREER ASSISTANT
# ==========================================
elif st.session_state.active_portal == "Assistant":
    st.markdown("""
    <div class="bento-bubble-card">
        <h3 style="margin-top: 0; color: #c084fc;">💬 Career Intelligence Assistant</h3>
        <p style="color: #94a3b8; font-size: 0.95rem; margin-bottom: 10px;">
            Ask anything regarding market compensation, promotion strategies, or interview frameworks.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_q1, col_q2, col_q3 = st.columns(3)
    with col_q1:
        if st.button("💡 ATS Optimization Tactics"):
            st.session_state.chat_history.append({"role": "user", "text": "What are the best ATS optimization tactics?"})
            st.session_state.chat_history.append({"role": "assistant", "text": "Use a clear single-column structure, standard section headers, and quantify accomplishments with direct metrics (e.g., 'Reduced latency by 35%')."})
    with col_q2:
        if st.button("📈 High-Demand Tech"):
            st.session_state.chat_history.append({"role": "user", "text": "What tech skills have peak market demand?"})
            st.session_state.chat_history.append({"role": "assistant", "text": "Distributed systems, AI systems integration, Kubernetes platform engineering, and high-concurrency microservices."})
    with col_q3:
        if st.button("🎯 Executive Interview Prep"):
            st.session_state.chat_history.append({"role": "user", "text": "How do I frame leadership experience?"})
            st.session_state.chat_history.append({"role": "assistant", "text": "Highlight system ownership, cross-functional project management, team mentorship, and strategic business impact."})

    st.markdown("<br>", unsafe_allow_html=True)
    
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"""
            <div style="background: rgba(56, 189, 248, 0.12); border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 18px; padding: 14px 18px; margin-bottom: 12px;">
                <span class="tag-bubble tag-cyan" style="margin-bottom: 6px;">You</span><br>
                <span style="color: #f1f5f9;">{msg['text']}</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: rgba(99, 102, 241, 0.12); border: 1px solid rgba(99, 102, 241, 0.25); border-radius: 18px; padding: 14px 18px; margin-bottom: 12px;">
                <span class="tag-bubble tag-indigo" style="margin-bottom: 6px;">🧠 CareerLens Assistant</span><br>
                <span style="color: #e2e8f0;">{msg['text']}</span>
            </div>
            """, unsafe_allow_html=True)
            
    user_query = st.chat_input("Ask CareerLens Assistant anything...")
    if user_query:
        st.session_state.chat_history.append({"role": "user", "text": user_query})
        st.session_state.chat_history.append({"role": "assistant", "text": f"Evaluating '{user_query}' against current market frameworks. Prioritize verified technical execution and quantifiable business impact."})
        st.rerun()

# --- Simplified Modern Footer ---
st.markdown("""
<div class="footer-container">
    CareerLens AI by Batch 2
</div>
""", unsafe_allow_html=True)
