import io
import os
from typing import Dict, List
import pandas as pd
import requests
import streamlit as st

API_BASE_URL = os.getenv("API_URL", "https://careerlens-ai-9dx8.onrender.com")

st.set_page_config(
    page_title="CareerLens AI",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Modern, Bubble-Rich, Sci-Fi UI Styling (Zero Red, Briefcase Branding) ---
st.markdown(
    """
<style>
:root{
    --bg:#07111f;
    --panel:rgba(13, 26, 43, 0.85);
    --border:#213754;
    --text:#f4f7fb;
    --purple:#8b7cff;
    --cyan:#38bdf8;
    --green:#4ade80;
    --indigo:#6366f1;
}

.stApp{
    background:
        radial-gradient(circle at 15% 0%,rgba(139,124,255,.14),transparent 28%),
        radial-gradient(circle at 90% 5%,rgba(56,189,248,.10),transparent 25%),
        var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.block-container{
    max-width:1450px;
    padding:24px 34px 50px;
}

[data-testid="stSidebar"]{
    background:#081526;
    border-right:1px solid #1b304b;
}

h1,h2,h3,h4{
    color:var(--text)!important;
}

p,label,.stMarkdown{
    color:#b8c6d8;
}

/* Briefcase Brand Header */
.brand-container {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 8px;
}

.brand-briefcase {
    font-size: 32px;
    filter: drop-shadow(0 0 10px rgba(56, 189, 248, 0.5));
}

.brand{
    font-size:24px;
    font-weight:850;
    color:white;
    letter-spacing:-.5px;
    margin: 0;
}

.brand span{
    background:linear-gradient(90deg,var(--purple),var(--cyan));
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.brand-sub{
    font-size:10px;
    letter-spacing:2px;
    color:#70849e;
    margin-top:2px;
}

/* Minimal Green Status Dot */
.status-dot-container {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    font-weight: 700;
    color: #4ade80;
    margin-top: 10px;
}

.status-dot {
    width: 9px;
    height: 9px;
    background-color: #4ade80;
    border-radius: 50%;
    box-shadow: 0 0 10px #4ade80;
    display: inline-block;
}

/* Ambient Hero Card */
.hero{
    background:
        linear-gradient(135deg,rgba(139,124,255,.12),rgba(56,189,248,.04)),
        linear-gradient(135deg,#0d1d34,#0b1728);
    border:1px solid #28425f;
    border-radius:24px;
    padding:36px;
    margin-bottom:24px;
    box-shadow:0 24px 70px rgba(0,0,0,.20);
}

.kicker{
    color:var(--cyan);
    font-size:12px;
    font-weight:800;
    letter-spacing:2.4px;
}

.hero h1{
    font-size:clamp(32px,4vw,52px);
    line-height:1.1;
    letter-spacing:-1.5px;
    margin:10px 0;
}

.hero h1 span{
    background:linear-gradient(90deg,var(--purple),var(--cyan));
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.hero p{
    max-width:820px;
    font-size:15px;
    line-height:1.65;
    color:#a8b9cd;
}

/* Bold Metric Highlights */
.metric-box {
    background: rgba(13, 26, 43, 0.9);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 22px;
    text-align: center;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
}

.metric-label {
    font-size: 0.85rem;
    color: #94a3b8;
    text-transform: uppercase;
    font-weight: 800;
    letter-spacing: 1.2px;
}

.metric-value-cyan {
    font-size: 2.4rem;
    font-weight: 900;
    color: #38bdf8;
    line-height: 1.2;
    margin: 6px 0;
    text-shadow: 0 0 15px rgba(56, 189, 248, 0.35);
}

.metric-value-indigo {
    font-size: 2.4rem;
    font-weight: 900;
    color: #818cf8;
    line-height: 1.2;
    margin: 6px 0;
    text-shadow: 0 0 15px rgba(129, 140, 248, 0.35);
}

.metric-value-purple {
    font-size: 2.4rem;
    font-weight: 900;
    color: #c084fc;
    line-height: 1.2;
    margin: 6px 0;
    text-shadow: 0 0 15px rgba(192, 132, 252, 0.35);
}

/* Bubble Bento Cards */
.panel{
    background:rgba(13,26,43,.82);
    border:1px solid var(--border);
    border-radius:18px;
    padding:20px;
    margin:12px 0;
}

/* Bubble Badges & Tags */
.skill, .tag-bubble{
    display:inline-flex;
    align-items: center;
    background:rgba(139,124,255,.12);
    color:#d9d4ff;
    border:1px solid rgba(139,124,255,.3);
    border-radius:999px;
    padding:6px 14px;
    margin:4px;
    font-size:12px;
    font-weight: 700;
    letter-spacing: 0.02em;
}

.tag-cyan {
    background: rgba(56, 189, 248, 0.12);
    color: #38bdf8;
    border: 1px solid rgba(56, 189, 248, 0.35);
}

.tag-purple {
    background: rgba(192, 132, 252, 0.12);
    color: #c084fc;
    border: 1px solid rgba(192, 132, 252, 0.35);
}

.tag-emerald {
    background: rgba(74, 222, 128, 0.12);
    color: #4ade80;
    border: 1px solid rgba(74, 222, 128, 0.35);
}

/* Bubble Buttons */
.stButton > button {
    border-radius: 50px !important;
    background: linear-gradient(135deg, #0284c7 0%, #4f46e5 50%, #7c3aed 100%) !important;
    color: #ffffff !important;
    font-weight: 800 !important;
    font-size: 0.95rem !important;
    padding: 0.65rem 1.8rem !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    box-shadow: 0 4px 18px rgba(79, 70, 229, 0.35) !important;
    transition: all 0.25s ease-in-out !important;
}

.stButton > button:hover {
    transform: translateY(-2px) scale(1.02) !important;
    box-shadow: 0 8px 25px rgba(56, 189, 248, 0.55) !important;
    border-color: rgba(255, 255, 255, 0.35) !important;
}

/* Clean Professional Footer */
.footer{
    text-align:center;
    color:#7186a1;
    font-size:12px;
    padding:35px 0 10px;
}
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# API CALLS
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
    res = requests.post(
        f"{API_BASE_URL}/api/recruiter/screen",
        files=file_payload,
        data=data_payload,
        timeout=120,
    )
    res.raise_for_status()
    return res.json()

def api_chat_assistant(messages: List[Dict], resume_context: str = "") -> str:
    payload = {"messages": messages, "resume_context": resume_context}
    try:
        res = requests.post(f"{API_BASE_URL}/api/chat/ask", json=payload, timeout=30)
        if res.status_code == 200:
            return res.json().get("reply", "I am ready to help optimize your career path.")
    except Exception:
        pass
    return "Focus on quantifiable achievements, matching core job description keywords, and maintaining clean ATS formatting."

# ============================================================
# STATE & HELPERS
# ============================================================

if "users_db" not in st.session_state:
    st.session_state.users_db = {}
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False
if "username" not in st.session_state:
    st.session_state.username = "Guest"
if "workspace" not in st.session_state:
    st.session_state.workspace = "Job Seeker"
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "resume_analysis" not in st.session_state:
    st.session_state.resume_analysis = None
if "recruiter_df" not in st.session_state:
    st.session_state.recruiter_df = None

def show_skills(skills, tag_style="tag-cyan"):
    if not skills:
        st.caption("No skills detected.")
        return
    html = "".join(f'<span class="tag-bubble {tag_style}">{skill}</span>' for skill in skills)
    st.markdown(html, unsafe_allow_html=True)

# ============================================================
# AUTHENTICATION DIALOGS (STRICT REGISTRATION & POPUPS)
# ============================================================

@st.dialog("🔐 Sign In to CareerLens")
def open_signin_dialog():
    st.markdown("Enter your registered credentials to access your saved profile and workspace.")
    login_user = st.text_input("Username / Email", key="popup_login_user")
    login_pass = st.text_input("Password", type="password", key="popup_login_pass")

    if st.button("Sign In", use_container_width=True, key="btn_confirm_signin"):
        if not login_user.strip() or not login_pass.strip():
            st.warning("Please fill in both fields.")
        elif login_user not in st.session_state.users_db:
            st.error("Account not found. Please click 'Register' first.")
        elif st.session_state.users_db[login_user] != login_pass:
            st.error("Incorrect password. Please try again.")
        else:
            st.session_state.username = login_user.split("@")[0].capitalize()
            st.session_state.is_logged_in = True
            st.success("Signed in successfully!")
            st.rerun()

@st.dialog("📝 Create Your Account")
def open_register_dialog():
    st.markdown("Register your details to save your skills, career roadmaps, and profile metrics.")
    reg_name = st.text_input("Full Name", placeholder="e.g. Alex Mercer", key="popup_reg_name")
    reg_user = st.text_input("Username or Email", placeholder="e.g. alex.mercer", key="popup_reg_user")
    reg_pass = st.text_input("Create Password", type="password", placeholder="••••••••", key="popup_reg_pass")

    if st.button("Complete Registration", use_container_width=True, key="btn_confirm_register"):
        if not reg_user.strip() or not reg_pass.strip():
            st.warning("Username and password are required.")
        elif reg_user in st.session_state.users_db:
            st.warning("Username already registered. Please sign in.")
        else:
            st.session_state.users_db[reg_user] = reg_pass
            st.session_state.username = reg_name.strip() if reg_name.strip() else reg_user.split("@")[0].capitalize()
            st.session_state.is_logged_in = True
            st.success("Account created successfully!")
            st.rerun()

# ============================================================
# GATEWAY SCREEN (TRENDY WELCOME TAG & POPUP ACTION BUTTONS)
# ============================================================

if not st.session_state.is_logged_in:
    st.markdown(
        """
        <div style="text-align:center; padding: 35px 0 15px;">
            <div style="font-size: 58px; filter: drop-shadow(0 0 16px rgba(56, 189, 248, 0.6));">💼</div>
            <h1 style="font-size: 3rem; margin: 10px 0 0 0; background: linear-gradient(90deg, #8b7cff, #38bdf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900;">CareerLens AI</h1>
            <p style="color: #94a3b8; font-size: 1.05rem; margin-top: 4px;">Next-Gen Career Intelligence Platform</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_l1, col_l2, col_l3 = st.columns([1, 1.6, 1])
    with col_l2:
        st.markdown(
            """
            <div class="panel" style="padding: 30px; text-align: center;">
                <span class="tag-bubble tag-cyan" style="font-size: 0.85rem; padding: 6px 18px; margin-bottom: 12px;">✦ YOUR CAREER LAUNCHPAD ✦</span>
                <h3 style="margin: 8px 0 0 0; color: #f4f7fb;">Build Your Future With Evidence</h3>
                <p style="color: #94a3b8; font-size: 0.92rem; margin-top: 6px; margin-bottom: 22px;">
                    Select an entry method below to begin evaluating your credentials, role alignment, and growth trajectory.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col_b1, col_b2, col_b3 = st.columns(3)
        with col_b1:
            if st.button("🔐 Sign In", use_container_width=True, key="btn_open_signin"):
                open_signin_dialog()
        with col_b2:
            if st.button("📝 Register", use_container_width=True, key="btn_open_register"):
                open_register_dialog()
        with col_b3:
            if st.button("🚀 Guest", use_container_width=True, key="btn_direct_guest"):
                st.session_state.username = "Guest Explorer"
                st.session_state.is_logged_in = True
                st.rerun()

    st.markdown("""
    <div class="footer">
        <b>CareerLens AI by Batch 2</b>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        """
        <div class="brand-container">
            <span class="brand-briefcase">💼</span>
            <div>
                <div class="brand">Career<span>Lens</span> AI</div>
                <div class="brand-sub">CAREER INTELLIGENCE PLATFORM</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # User Profile Pill & Logout
    st.markdown(
        f"""
        <div style="background: rgba(139, 124, 255, 0.12); border: 1px solid rgba(139, 124, 255, 0.3); border-radius: 14px; padding: 10px 14px; margin: 10px 0 14px 0; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div style="font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; font-weight: 700;">Active User</div>
                <div style="font-size: 0.95rem; font-weight: 800; color: #38bdf8;">{st.session_state.username}</div>
            </div>
            <span class="tag-bubble tag-emerald" style="margin: 0; font-size: 0.7rem; padding: 4px 10px;">Online</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Log Out", use_container_width=True):
        st.session_state.is_logged_in = False
        st.session_state.username = "Guest"
        st.session_state.resume_text = ""
        st.session_state.resume_analysis = None
        st.session_state.recruiter_df = None
        st.rerun()

    st.divider()

    # Workspace Switcher via Bubble Buttons
    col_w1, col_w2 = st.columns(2)
    with col_w1:
        if st.button("👨‍💻 Candidate", use_container_width=True):
            st.session_state.workspace = "Job Seeker"
    with col_w2:
        if st.button("🏢 Recruiter", use_container_width=True):
            st.session_state.workspace = "Recruiter"

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Career Assistant Launcher Button
    if st.button("💼 Career Assistant", use_container_width=True):
        st.session_state.workspace = "Assistant"

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Minimalist Green Status Dot
    st.markdown(
        """
        <div class="status-dot-container">
            <span class="status-dot"></span> System Live
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# 1. CANDIDATE WORKSPACE
# ============================================================

if st.session_state.workspace == "Job Seeker":

    st.markdown(
        """
        <section class="hero">
            <div class="kicker">AI CAREER INTELLIGENCE</div>
            <h1>Understand Your Career.<br><span>Build Your Future.</span></h1>
            <p>Accelerate your career trajectory with automated resume parsing, semantic job fit matching, skill gap discovery, and step-by-step career roadmaps.</p>
            <div style="margin-top: 14px;">
                <span class="tag-bubble tag-cyan">✦ Predictive Gap Analysis</span>
                <span class="tag-bubble tag-purple">✦ Profile Intelligence</span>
                <span class="tag-bubble tag-emerald">✦ Growth Trajectory</span>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    analysis = st.session_state.resume_analysis
    score_val = f"{analysis.get('resume_score', '—')}/100" if analysis else "—"
    readiness_val = f"{analysis.get('readiness', '—')}%" if analysis else "—"
    skills_count = f"{len(analysis.get('skills', []))}" if analysis else "0"

    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Resume Score</div>
            <div class="metric-value-cyan"><b>{score_val}</b></div>
            <span class="tag-bubble tag-cyan">AI Assessment</span>
        </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Career Readiness</div>
            <div class="metric-value-indigo"><b>{readiness_val}</b></div>
            <span class="tag-bubble tag-indigo">Profile Strength</span>
        </div>
        """, unsafe_allow_html=True)
    with col_m3:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Skills Detected</div>
            <div class="metric-value-purple"><b>{skills_count}</b></div>
            <span class="tag-bubble tag-purple">Extracted Stack</span>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    tabs = st.tabs([
        "📄 Resume Intelligence",
        "🎯 Job Match",
        "🛡️ Fraud Risk",
        "🧩 Skill Gap",
        "🗺️ Career Roadmap"
    ])

    # 1. Resume Intelligence
    with tabs[0]:
        st.subheader("Resume Intelligence")
        resume_file = st.file_uploader(
            "Upload Resume Document", type=["pdf", "docx", "txt"], key="resume_upload"
        )

        if resume_file and st.button("Analyze Resume", use_container_width=True):
            with st.spinner("Analyzing resume profile..."):
                try:
                    result = api_analyze_resume(resume_file)
                    st.session_state.resume_analysis = result
                    st.session_state.resume_text = result.get("extracted_text", "")
                    st.success("Resume processed successfully!")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Analysis error: {exc}")

        if st.session_state.resume_analysis:
            res = st.session_state.resume_analysis
            st.markdown(
                f"""
                <div class="panel">
                    <h3 style="margin: 0; color: #38bdf8; font-weight: 800;">{res.get('name', 'Candidate Profile')}</h3>
                    <p style="margin: 6px 0 0 0; color: #b8c6d8;">
                        📧 <b>Email:</b> {res.get('email', 'Not detected')} &nbsp;|&nbsp; 
                        📱 <b>Phone:</b> {res.get('phone', 'Not detected')} &nbsp;|&nbsp; 
                        ⏳ <b>Experience:</b> <b>{res.get('experience', 'Identified')}</b>
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("#### Extracted Competencies")
            show_skills(res.get("skills", []), "tag-cyan")

    # 2. Job Match
    with tabs[1]:
        st.subheader("Semantic Job Matching")
        job_desc = st.text_area("Paste Target Job Description", height=180, key="jobmatch")

        if st.button("Analyze Job Fit", use_container_width=True):
            if not st.session_state.resume_text:
                st.warning("Please upload and analyze your resume first.")
            elif not job_desc.strip():
                st.warning("Please enter a job description.")
            else:
                with st.spinner("Evaluating semantic role alignment..."):
                    try:
                        result = api_match_job(st.session_state.resume_text, job_desc)
                        overall_score = result.get("overall", 0)
                        
                        col_s1, col_s2, col_s3 = st.columns(3)
                        with col_s1:
                            st.markdown(f"""
                            <div class="metric-box">
                                <div class="metric-label">Overall Match</div>
                                <div class="metric-value-cyan"><b>{overall_score}%</b></div>
                            </div>
                            """, unsafe_allow_html=True)
                        with col_s2:
                            st.markdown(f"""
                            <div class="metric-box">
                                <div class="metric-label">Semantic Alignment</div>
                                <div class="metric-value-indigo"><b>{result.get('semantic', 0)}%</b></div>
                            </div>
                            """, unsafe_allow_html=True)
                        with col_s3:
                            st.markdown(f"""
                            <div class="metric-box">
                                <div class="metric-label">Skill Overlap</div>
                                <div class="metric-value-purple"><b>{result.get('skill_match', 0)}%</b></div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                        st.progress(overall_score / 100)
                        
                        st.markdown("#### Matched Skills")
                        show_skills(result.get("matched", []), "tag-cyan")
                        
                        st.markdown("#### Missing Skills")
                        show_skills(result.get("missing", []), "tag-purple")
                    except Exception as exc:
                        st.error(f"Matching error: {exc}")

    # 3. Fraud Risk
    with tabs[2]:
        st.subheader("Job Safety & Risk Intelligence")
        jobrisk = st.text_area("Paste Job Advertisement / Offer", height=180, key="risk")

        if st.button("Analyze Safety Risk", use_container_width=True):
            if not jobrisk.strip():
                st.warning("Enter a job advertisement to evaluate.")
            else:
                with st.spinner("Evaluating scam signals & offer credibility..."):
                    try:
                        res = api_detect_fraud(jobrisk)
                        col_f1, col_f2, col_f3 = st.columns(3)
                        with col_f1:
                            st.markdown(f"""
                            <div class="metric-box">
                                <div class="metric-label">Risk Score</div>
                                <div class="metric-value-cyan"><b>{res.get('score', 0)}/100</b></div>
                            </div>
                            """, unsafe_allow_html=True)
                        with col_f2:
                            st.markdown(f"""
                            <div class="metric-box">
                                <div class="metric-label">Risk Level</div>
                                <div class="metric-value-indigo"><b>{res.get('level', 'LOW RISK')}</b></div>
                            </div>
                            """, unsafe_allow_html=True)
                        with col_f3:
                            st.markdown(f"""
                            <div class="metric-box">
                                <div class="metric-label">Signals Detected</div>
                                <div class="metric-value-purple"><b>{res.get('signals', 0)}</b></div>
                            </div>
                            """, unsafe_allow_html=True)

                        if res.get("level") == "HIGH RISK":
                            st.warning("⚠️ High risk patterns detected in this job posting.")
                        else:
                            st.success("✅ Low risk detected. Posting appears legitimate.")
                    except Exception as exc:
                        st.error(f"Risk evaluation error: {exc}")

    # 4. Skill Gap
    with tabs[3]:
        st.subheader("Skill Gap Analysis")
        target_job = st.text_area("Target Job Specification", height=180, key="gap")

        if st.button("Analyze Skill Gap", use_container_width=True):
            if not st.session_state.resume_text:
                st.warning("Upload your resume first.")
            elif not target_job.strip():
                st.warning("Enter target job requirements.")
            else:
                with st.spinner("Calculating skill gap matrix..."):
                    try:
                        res = api_skill_gap(st.session_state.resume_text, target_job)
                        col_g1, col_g2 = st.columns(2)
                        with col_g1:
                            st.markdown("#### Verified Strengths")
                            show_skills(res.get("matched", []), "tag-cyan")
                        with col_g2:
                            st.markdown("#### Missing Skills to Prioritize")
                            show_skills(res.get("missing", []), "tag-purple")
                    except Exception as exc:
                        st.error(f"Skill gap error: {exc}")

    # 5. Career Roadmap
    with tabs[4]:
        st.subheader("Personalized Career Trajectory")
        role = st.text_input("Aspirational Target Role", "Machine Learning Engineer")

        if st.button("Generate Career Roadmap", use_container_width=True):
            with st.spinner("Synthesizing step-by-step career roadmap..."):
                try:
                    res = api_career_roadmap(st.session_state.resume_text, role)
                    steps = res.get("steps", [])
                    for idx, step in enumerate(steps, 1):
                        st.markdown(
                            f"""
                            <div class="panel">
                                <span class="tag-bubble tag-cyan">STEP {idx:02d}</span>
                                <div style="font-size: 1.1rem; font-weight: 800; color: #f4f7fb; margin-top: 8px;">{step}</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                except Exception as exc:
                    st.error(f"Roadmap error: {exc}")

# ============================================================
# 2. RECRUITER WORKSPACE
# ============================================================

elif st.session_state.workspace == "Recruiter":
    st.markdown(
        """
        <section class="hero">
            <div class="kicker">RECRUITMENT INTELLIGENCE</div>
            <h1>Screen Smarter.<br><span>Hire with Evidence.</span></h1>
            <p>Accelerate talent acquisition with automated semantic screening, candidate ranking, and instant qualification benchmarking.</p>
            <div style="margin-top: 14px;">
                <span class="tag-bubble tag-cyan">✦ Bulk Parsing</span>
                <span class="tag-bubble tag-purple">✦ Candidate Ranking</span>
                <span class="tag-bubble tag-emerald">✦ Precision Fit</span>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    recruiter_job = st.text_area("Job Requirements & Qualifications", height=180, key="recruiter_job")
    recruiter_files = st.file_uploader(
        "Candidate Resumes",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        key="candidate_files",
    )
    top_n = st.number_input("Shortlist Size", min_value=1, max_value=100, value=10)

    if st.button("⚡ Screen & Rank Candidates", use_container_width=True):
        if not recruiter_job.strip() or not recruiter_files:
            st.warning("Please provide a job description and candidate resumes.")
        else:
            with st.spinner("Ranking candidate cohort..."):
                try:
                    candidates_data = api_screen_candidates(recruiter_files, recruiter_job)
                    st.session_state.recruiter_df = pd.DataFrame(candidates_data)
                    st.success(f"Successfully ranked {len(candidates_data)} candidates!")
                except Exception as exc:
                    st.error(f"Screening error: {exc}")

    if st.session_state.recruiter_df is not None and not st.session_state.recruiter_df.empty:
        df = st.session_state.recruiter_df.head(int(top_n))
        st.markdown("#### Candidate Shortlist")
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button(
            "⬇️ Download Shortlist (CSV)",
            df.to_csv(index=False).encode("utf-8"),
            file_name="shortlist.csv",
            mime="text/csv",
            use_container_width=True,
        )

# ============================================================
# 3. AI CAREER ASSISTANT
# ============================================================

elif st.session_state.workspace == "Assistant":
    st.markdown(
        """
        <section class="hero">
            <div class="kicker">CAREER ASSISTANT</div>
            <h1>AI Career Advisory.<br><span>Real-Time Insights.</span></h1>
            <p>Ask anything about resume positioning, ATS compliance, interview strategies, or industry salary benchmarks.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [{
            "role": "assistant",
            "content": "Hello! Ask me anything about resume optimization, ATS keywords, interview preparation, or skill roadmaps."
        }]

    st.markdown("#### Quick Questions")
    q_cols = st.columns(3)
    faqs = [
        "How do I optimize my resume for ATS?",
        "How do I present my technical skills?",
        "What makes a project stand out?",
    ]

    chosen_faq = None
    for i, faq in enumerate(faqs):
        if q_cols[i].button(faq, key=f"btn_faq_{i}", use_container_width=True):
            chosen_faq = faq

    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Ask a question about your resume or career...")
    active_prompt = chosen_faq or user_input

    if active_prompt:
        st.session_state.chat_messages.append({"role": "user", "content": active_prompt})
        with st.chat_message("user"):
            st.write(active_prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                ans = api_chat_assistant(
                    st.session_state.chat_messages,
                    resume_context=st.session_state.resume_text,
                )
                st.write(ans)
        st.session_state.chat_messages.append({"role": "assistant", "content": ans})
        st.rerun()

# ============================================================
# FOOTER
# ============================================================
st.divider()
st.markdown(
    """
    <div class="footer">
        <b>CareerLens AI by Batch 2</b>
    </div>
    """,
    unsafe_allow_html=True,
)
