import io
import os
from typing import Dict, List
import pandas as pd
import requests
import streamlit as st

API_BASE_URL = os.getenv("API_URL", "https://careerlens-ai-9dx8.onrender.com")

st.set_page_config(
    page_title="CareerLens AI | Career Intelligence Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Professional, Bubble-Rich, Sci-Fi Glassmorphism Styling ---
st.markdown(
    """
<style>
:root {
    --bg-dark: #070e18;
    --panel-bg: rgba(13, 25, 44, 0.75);
    --border-subtle: rgba(56, 189, 248, 0.15);
    --primary-cyan: #38bdf8;
    --primary-indigo: #818cf8;
    --primary-purple: #c084fc;
    --accent-emerald: #10b981;
}

/* Base Canvas & Gradient Atmosphere */
.stApp {
    background: radial-gradient(circle at 10% 15%, #0b1528 0%, #060b13 70%, #03070d 100%);
    color: #f1f5f9;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.block-container {
    max-width: 1400px;
    padding: 24px 32px 50px;
}

[data-testid="stSidebar"] {
    background: #060f1c;
    border-right: 1px solid rgba(255, 255, 255, 0.07);
}

/* Ambient Hero Card with Brain Logo */
.brand-hero {
    display: flex;
    align-items: center;
    gap: 22px;
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.95) 100%);
    border: 1px solid var(--border-subtle);
    border-radius: 26px;
    padding: 28px 36px;
    box-shadow: 0 16px 40px -10px rgba(0, 0, 0, 0.6), 0 0 25px rgba(56, 189, 248, 0.12);
    backdrop-filter: blur(16px);
    margin-bottom: 26px;
}

.brand-brain-glow {
    font-size: 3.4rem;
    background: radial-gradient(circle, rgba(56, 189, 248, 0.25) 0%, transparent 70%);
    padding: 12px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 30px rgba(56, 189, 248, 0.35);
}

.hero-title-text {
    font-size: 2.2rem;
    font-weight: 850;
    letter-spacing: -0.02em;
    background: linear-gradient(90deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    line-height: 1.15;
}

.hero-sub-text {
    font-size: 0.95rem;
    color: #94a3b8;
    margin-top: 5px;
    font-weight: 500;
}

/* Bubble Bento Cards */
.bubble-card {
    background: var(--panel-bg);
    border: 1px solid var(--border-subtle);
    border-radius: 20px;
    padding: 22px;
    backdrop-filter: blur(14px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
    margin-bottom: 16px;
}

/* Bubble Tags and Badges */
.tag-bubble {
    display: inline-flex;
    align-items: center;
    padding: 6px 14px;
    border-radius: 50px;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.02em;
    margin: 4px 4px 4px 0;
}
.tag-cyan {
    background: rgba(56, 189, 248, 0.12);
    color: #38bdf8;
    border: 1px solid rgba(56, 189, 248, 0.3);
}
.tag-indigo {
    background: rgba(129, 140, 248, 0.12);
    color: #818cf8;
    border: 1px solid rgba(129, 140, 248, 0.3);
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

/* Modern Bubble Buttons */
.stButton > button {
    border-radius: 35px !important;
    background: linear-gradient(135deg, #0284c7 0%, #4f46e5 50%, #7c3aed 100%) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 0.65rem 1.8rem !important;
    border: 1px solid rgba(255, 255, 255, 0.18) !important;
    box-shadow: 0 4px 18px rgba(79, 70, 229, 0.35) !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) scale(1.02) !important;
    box-shadow: 0 8px 25px rgba(56, 189, 248, 0.55) !important;
    border-color: rgba(255, 255, 255, 0.35) !important;
}

/* Status Indicator Dot */
.status-indicator {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 14px;
    border-radius: 50px;
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.3);
    color: #34d399;
    font-size: 0.8rem;
    font-weight: 700;
}
.pulse-dot {
    width: 8px;
    height: 8px;
    background-color: #10b981;
    border-radius: 50%;
    box-shadow: 0 0 10px #10b981;
}

/* Footer Styling */
.footer-text {
    text-align: center;
    color: #64748b;
    font-size: 0.85rem;
    padding-top: 35px;
    padding-bottom: 10px;
}
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# API INTEGRATION LAYER
# ============================================================

def api_analyze_resume(file) -> Dict:
    files = {"file": (file.name, file.getvalue(), file.type)}
    res = requests.post(f"{API_BASE_URL}/api/resume/analyze", files=files, timeout=60)
    res.raise_for_status()
    return res.json()

def api_match_job(resume_text: str, job_description: str) -> Dict:
    payload = {"resume_text": resume_text, "job_description": job_description}
    res = requests.post(f"{API_BASE_URL}/api/job/match", json=payload, timeout=30)
    res.raise_for_status()
    return res.json()

def api_detect_fraud(job_text: str) -> Dict:
    payload = {"text": job_text}
    res = requests.post(f"{API_BASE_URL}/api/job/fraud", json=payload, timeout=30)
    res.raise_for_status()
    return res.json()

def api_skill_gap(resume_text: str, target_job: str) -> Dict:
    payload = {"resume_text": resume_text, "target_job": target_job}
    res = requests.post(f"{API_BASE_URL}/api/skills/gap", json=payload, timeout=30)
    res.raise_for_status()
    return res.json()

def api_career_roadmap(resume_text: str, target_role: str) -> Dict:
    payload = {"resume_text": resume_text, "target_role": target_role}
    res = requests.post(f"{API_BASE_URL}/api/career/roadmap", json=payload, timeout=30)
    res.raise_for_status()
    return res.json()

def api_screen_candidates(files: List, job_description: str) -> List[Dict]:
    file_payload = [("files", (f.name, f.getvalue(), f.type)) for f in files]
    data_payload = {"job_description": job_description}
    res = requests.post(f"{API_BASE_URL}/api/recruiter/screen", files=file_payload, data=data_payload, timeout=120)
    res.raise_for_status()
    return res.json()

def api_chat_assistant(messages: List[Dict], resume_context: str = "") -> str:
    payload = {"messages": messages, "resume_context": resume_context}
    try:
        res = requests.post(f"{API_BASE_URL}/api/chat/ask", json=payload, timeout=30)
        if res.status_code == 200:
            return res.json().get("reply", "I am ready to help optimize your career trajectory.")
    except Exception:
        pass
    return "Focus on quantifiable impacts, clear technical competencies, and standard ATS formatting."

# ============================================================
# STATE SETUP & UI HELPERS
# ============================================================

if "active_portal" not in st.session_state:
    st.session_state.active_portal = "Candidate"
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "resume_analysis" not in st.session_state:
    st.session_state.resume_analysis = None
if "recruiter_df" not in st.session_state:
    st.session_state.recruiter_df = None
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [{
        "role": "assistant",
        "content": "Hello! I am your CareerLens Assistant. Ask me anything about resume optimization, skill positioning, or career trajectories."
    }]

def render_tag_cloud(skills: List[str], tag_class: str = "tag-cyan"):
    if not skills:
        st.caption("No competencies specified.")
        return
    html = "".join(f'<span class="tag-bubble {tag_class}">{skill}</span>' for skill in skills)
    st.markdown(html, unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 16px;">
        <div style="font-size: 48px; margin-bottom: 6px;">🧠</div>
        <h2 style="margin: 0; font-size: 1.5rem; background: linear-gradient(135deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">CareerLens AI</h2>
        <p style="color: #94a3b8; font-size: 0.8rem; margin-top: 4px;">Understand Your Career. Build Your Future.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation Bubbles
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("🚀 Candidate", use_container_width=True):
            st.session_state.active_portal = "Candidate"
    with col_nav2:
        if st.button("🏢 Recruiter", use_container_width=True):
            st.session_state.active_portal = "Recruiter"
            
    st.markdown("---")
    if st.button("💬 Launch Assistant", use_container_width=True):
        st.session_state.active_portal = "Assistant"

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Status Indicator Dot
    st.markdown("""
    <div style="text-align: center;">
        <span class="status-indicator"><span class="pulse-dot"></span> System Live</span>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# TOP HERO BANNER
# ============================================================

st.markdown("""
<div class="brand-hero">
    <div class="brand-brain-glow">🧠</div>
    <div>
        <h1 class="hero-title-text">CareerLens AI</h1>
        <div class="hero-sub-text">Understand Your Career • Build Your Future • Optimize Matching • Accelerate Hiring</div>
        <div style="margin-top: 10px;">
            <span class="tag-bubble tag-cyan">✦ Predictive Gap Analysis</span>
            <span class="tag-bubble tag-indigo">✦ Profile Intelligence</span>
            <span class="tag-bubble tag-purple">✦ Roadmapping Engine</span>
            <span class="tag-bubble tag-emerald">✦ Talent Discovery</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# 1. CANDIDATE WORKSPACE
# ============================================================

if st.session_state.active_portal == "Candidate":
    
    analysis = st.session_state.resume_analysis
    score_val = f"{analysis.get('resume_score', '—')}/100" if analysis else "—"
    readiness_val = f"{analysis.get('readiness', '—')}%" if analysis else "—"
    skills_count = len(analysis.get("skills", [])) if analysis else 0

    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.markdown(f"""
        <div class="bubble-card" style="text-align: center;">
            <span style="font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; font-weight: 700;">Resume Score</span><br>
            <b style="font-size: 2rem; color: #38bdf8;">{score_val}</b>
        </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"""
        <div class="bubble-card" style="text-align: center;">
            <span style="font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; font-weight: 700;">Career Readiness</span><br>
            <b style="font-size: 2rem; color: #818cf8;">{readiness_val}</b>
        </div>
        """, unsafe_allow_html=True)
    with col_m3:
        st.markdown(f"""
        <div class="bubble-card" style="text-align: center;">
            <span style="font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; font-weight: 700;">Skills Detected</span><br>
            <b style="font-size: 2rem; color: #c084fc;">{skills_count}</b>
        </div>
        """, unsafe_allow_html=True)

    tabs = st.tabs([
        "📄 Resume Profile",
        "🎯 Job Match",
        "⚡ Skill Gap",
        "🛡️ Credibility & Safety",
        "🗺️ Career Roadmap"
    ])

    # 1. Resume Profile
    with tabs[0]:
        st.markdown("#### Resume Intelligence")
        resume_file = st.file_uploader("Upload Resume Document", type=["pdf", "docx", "txt"], key="resume_upload")
        
        if resume_file and st.button("✨ Parse Resume", use_container_width=False):
            with st.spinner("Analyzing profile competencies..."):
                try:
                    result = api_analyze_resume(resume_file)
                    st.session_state.resume_analysis = result
                    st.session_state.resume_text = result.get("extracted_text", "")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Analysis notice: {exc}")

        if st.session_state.resume_analysis:
            res = st.session_state.resume_analysis
            st.markdown(f"""
            <div class="bubble-card">
                <h3 style="margin: 0; color: #38bdf8;">{res.get('name', 'Candidate Profile')}</h3>
                <p style="margin: 4px 0 12px 0; color: #94a3b8; font-size: 0.95rem;">
                    📧 {res.get('email', 'Identified')} &nbsp;|&nbsp; 📱 {res.get('phone', 'Identified')} &nbsp;|&nbsp; ⏳ {res.get('experience', 'Verified')}
                </p>
                <div style="margin-top: 10px;">
                    <span style="font-size: 0.85rem; color: #94a3b8; font-weight: 700; text-transform: uppercase;">Extracted Skills:</span><br>
                </div>
            </div>
            """, unsafe_allow_html=True)
            render_tag_cloud(res.get("skills", []), "tag-cyan")

    # 2. Job Match
    with tabs[1]:
        st.markdown("#### Discover Role Fit")
        job_desc = st.text_area("Target Job Description", height=150, placeholder="Paste target requirements here...")
        
        if st.button("Analyze Job Fit", key="btn_job_match"):
            if not st.session_state.resume_text:
                st.warning("Please upload and parse your resume first.")
            elif not job_desc.strip():
                st.warning("Please provide a job description.")
            else:
                with st.spinner("Evaluating role alignment..."):
                    try:
                        result = api_match_job(st.session_state.resume_text, job_desc)
                        overall = result.get("overall", 0)
                        
                        col_r1, col_r2 = st.columns([1, 2])
                        with col_r1:
                            st.markdown(f"""
                            <div class="bubble-card" style="text-align: center; padding: 24px;">
                                <span style="font-size: 0.85rem; color: #94a3b8; font-weight: 700; text-transform: uppercase;">Match Index</span><br>
                                <b style="font-size: 2.8rem; background: linear-gradient(135deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{overall}%</b>
                            </div>
                            """, unsafe_allow_html=True)
                            st.progress(overall / 100)
                        with col_r2:
                            st.markdown("##### Matched Competencies")
                            render_tag_cloud(result.get("matched", []), "tag-cyan")
                            st.markdown("<br>", unsafe_allow_html=True)
                            st.markdown("##### Missing Competencies")
                            render_tag_cloud(result.get("missing", []), "tag-purple")
                    except Exception as exc:
                        st.error(f"Evaluation notice: {exc}")

    # 3. Skill Gap
    with tabs[2]:
        st.markdown("#### Skill Gap Analysis")
        target_job = st.text_area("Target Role Specification", height=150, placeholder="Enter target skill requirements...")
        
        if st.button("Analyze Skill Gap", key="btn_skill_gap"):
            if not st.session_state.resume_text:
                st.warning("Please upload and parse your resume first.")
            elif not target_job.strip():
                st.warning("Please provide target role requirements.")
            else:
                with st.spinner("Calculating skill benchmarks..."):
                    try:
                        res = api_skill_gap(st.session_state.resume_text, target_job)
                        col_g1, col_g2 = st.columns(2)
                        with col_g1:
                            st.markdown("""
                            <div class="bubble-card">
                                <h4 style="margin-top: 0; color: #38bdf8;">Verified Core Strengths</h4>
                            </div>
                            """, unsafe_allow_html=True)
                            render_tag_cloud(res.get("matched", []), "tag-cyan")
                        with col_g2:
                            st.markdown("""
                            <div class="bubble-card">
                                <h4 style="margin-top: 0; color: #c084fc;">Priority Skill Targets</h4>
                            </div>
                            """, unsafe_allow_html=True)
                            render_tag_cloud(res.get("missing", []), "tag-purple")
                    except Exception as exc:
                        st.error(f"Analysis notice: {exc}")

    # 4. Credibility & Safety
    with tabs[3]:
        st.markdown("#### Opportunity Safety & Risk Intelligence")
        jobrisk = st.text_area("Job Posting / Offer Text", height=150, placeholder="Paste job advertisement to evaluate legitimacy...")
        
        if st.button("Run Safety Check", key="btn_risk"):
            if not jobrisk.strip():
                st.warning("Please enter a job posting to evaluate.")
            else:
                with st.spinner("Scanning verification indicators..."):
                    try:
                        res = api_detect_fraud(jobrisk)
                        level = res.get("level", "LOW RISK")
                        score = res.get("score", 0)
                        
                        st.markdown(f"""
                        <div class="bubble-card">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <h4 style="margin: 0; color: #34d399;">Safety Level: {level}</h4>
                                    <p style="margin: 4px 0 0 0; color: #94a3b8; font-size: 0.9rem;">Signals Identified: {res.get('signals', 0)}</p>
                                </div>
                                <div style="text-align: right;">
                                    <span style="font-size: 0.8rem; color: #94a3b8; text-transform: uppercase;">Risk Score</span><br>
                                    <b style="font-size: 1.5rem; color: #818cf8;">{score}/100</b>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    except Exception as exc:
                        st.error(f"Verification notice: {exc}")

    # 5. Career Roadmap
    with tabs[4]:
        st.markdown("#### Personalized Growth Trajectory")
        role_input = st.text_input("Aspirational Role", "Machine Learning Engineer")
        
        if st.button("Generate Roadmap", key="btn_roadmap"):
            with st.spinner("Synthesizing strategic growth roadmap..."):
                try:
                    res = api_career_roadmap(st.session_state.resume_text, role_input)
                    steps = res.get("steps", [])
                    for idx, step in enumerate(steps, 1):
                        st.markdown(f"""
                        <div class="bubble-card" style="margin-bottom: 12px;">
                            <span class="tag-bubble tag-indigo">STAGE {idx:02d}</span>
                            <div style="font-size: 1rem; color: #f1f5f9; font-weight: 600; margin-top: 6px;">{step}</div>
                        </div>
                        """, unsafe_allow_html=True)
                except Exception as exc:
                    st.error(f"Roadmap notice: {exc}")

# ============================================================
# 2. RECRUITER WORKSPACE
# ============================================================

elif st.session_state.active_portal == "Recruiter":
    st.markdown("""
    <div class="bubble-card">
        <h3 style="margin-top: 0; color: #818cf8;">🏢 Executive Talent Hub</h3>
        <p style="color: #94a3b8; font-size: 0.95rem; margin-bottom: 10px;">
            Screen and rank applicant pools with high-signal matching.
        </p>
        <div>
            <span class="tag-bubble tag-cyan">Batch Evaluation</span>
            <span class="tag-bubble tag-indigo">Semantic Ranking</span>
            <span class="tag-bubble tag-purple">High Precision</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    recruiter_job = st.text_area("Role Specifications & Technical Mandate", height=120, placeholder="Define role criteria...")
    recruiter_files = st.file_uploader("Applicant Resumes", type=["pdf", "docx", "txt"], accept_multiple_files=True)
    top_n = st.slider("Display Top Shortlisted Candidates", 1, 50, 10)

    if st.button("⚡ Rank Candidate Pool", key="btn_screen"):
        if not recruiter_job.strip() or not recruiter_files:
            st.warning("Please provide a job specification and candidate resumes.")
        else:
            with st.spinner("Processing candidate cohort..."):
                try:
                    candidates_data = api_screen_candidates(recruiter_files, recruiter_job)
                    st.session_state.recruiter_df = pd.DataFrame(candidates_data)
                    st.success(f"Ranked {len(candidates_data)} candidate profiles.")
                except Exception as exc:
                    st.error(f"Screening notice: {exc}")

    if st.session_state.recruiter_df is not None and not st.session_state.recruiter_df.empty:
        df = st.session_state.recruiter_df.head(int(top_n))
        st.markdown("#### Candidate Shortlist")
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button(
            "⬇️ Export Shortlist (CSV)",
            df.to_csv(index=False).encode("utf-8"),
            file_name="shortlist.csv",
            mime="text/csv",
            use_container_width=True,
        )

# ============================================================
# 3. AI CAREER ASSISTANT
# ============================================================

elif st.session_state.active_portal == "Assistant":
    st.markdown("""
    <div class="bubble-card">
        <h3 style="margin-top: 0; color: #c084fc;">💬 CareerLens AI Assistant</h3>
        <p style="color: #94a3b8; font-size: 0.95rem; margin-bottom: 0;">
            Ask anything regarding interview strategies, compensation benchmarks, or ATS optimization.
        </p>
    </div>
    """, unsafe_allow_html=True)

    faqs = [
        "How do I optimize my resume for ATS?",
        "What are the highest demand tech skills?",
        "How do I present leadership impact?"
    ]
    
    col_q1, col_q2, col_q3 = st.columns(3)
    chosen_faq = None
    if col_q1.button(faqs[0], key="faq_0", use_container_width=True):
        chosen_faq = faqs[0]
    if col_q2.button(faqs[1], key="faq_1", use_container_width=True):
        chosen_faq = faqs[1]
    if col_q3.button(faqs[2], key="faq_2", use_container_width=True):
        chosen_faq = faqs[2]

    st.markdown("<br>", unsafe_allow_html=True)

    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Ask a question about your career or resume...")
    active_prompt = chosen_faq or user_input

    if active_prompt:
        st.session_state.chat_messages.append({"role": "user", "content": active_prompt})
        with st.chat_message("user"):
            st.write(active_prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                ans = api_chat_assistant(st.session_state.chat_messages, resume_context=st.session_state.resume_text)
                st.write(ans)
        st.session_state.chat_messages.append({"role": "assistant", "content": ans})
        st.rerun()

# ============================================================
# GLOBAL FOOTER
# ============================================================

st.markdown("""
<div class="footer-text">
    CareerLens AI by Batch 2
</div>
""", unsafe_allow_html=True)
