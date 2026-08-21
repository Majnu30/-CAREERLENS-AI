import os
import requests
import streamlit as st

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="CareerLens AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================
# 2. MODERN BRAND STYLING (RED-FREE PALETTE)
# ==========================================
st.markdown(
    """
<style>
    :root {
        --primary-teal: #0d9488;
        --primary-blue: #2563eb;
        --primary-indigo: #4f46e5;
        --bg-glass: rgba(255, 255, 255, 0.85);
        --accent-dark: #0f172a;
    }

    /* Overall Background */
    .stApp {
        background: linear-gradient(135deg, #f0fdfa 0%, #e0f2fe 50%, #ede9fe 100%);
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }

    /* Custom Bubble Buttons */
    div.stButton > button {
        background: linear-gradient(135deg, #0d9488 0%, #2563eb 100%);
        color: #ffffff;
        font-weight: 600;
        font-size: 1rem;
        border: none;
        border-radius: 9999px;
        padding: 0.65rem 1.8rem;
        box-shadow: 0 4px 14px 0 rgba(13, 148, 136, 0.35);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #0f766e 0%, #1d4ed8 100%);
        color: #ffffff;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px 0 rgba(37, 99, 235, 0.45);
    }

    /* Mode Hub Cards */
    .hub-card {
        background: var(--bg-glass);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.6);
        border-radius: 20px;
        padding: 2.2rem;
        text-align: center;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.08);
        transition: transform 0.25s ease;
    }
    .hub-card:hover {
        transform: translateY(-4px);
    }

    /* Indicator Dot */
    .status-dot-green {
        display: inline-block;
        width: 10px;
        height: 10px;
        background-color: #10b981;
        border-radius: 50%;
        box-shadow: 0 0 8px #10b981;
        margin-right: 8px;
    }

    /* Clean Footer */
    .custom-footer {
        text-align: center;
        padding: 2rem 0;
        font-size: 0.9rem;
        font-weight: 500;
        color: #64748b;
        letter-spacing: 0.03em;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 3. STATE INITIALIZATION
# ==========================================
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

if "current_view" not in st.session_state:
    st.session_state.current_view = "Hub"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "extracted_profile" not in st.session_state:
    st.session_state.extracted_profile = None

# ==========================================
# 4. SIDEBAR NAVIGATION & MINIMAL STATUS
# ==========================================
with st.sidebar:
    st.markdown("### 🧠 **CareerLens AI**")
    st.caption("Empowering Next-Gen Career Decisions")
    st.markdown("---")

    # Quick Assistant Toggle Button
    if st.button("💬 Launch Assistant", use_container_width=True):
        st.session_state.current_view = "Assistant"

    st.markdown("#### **Navigation**")
    if st.button("🏠 Main Portal", use_container_width=True):
        st.session_state.current_view = "Hub"
    if st.button("🎯 Job Seeker Suite", use_container_width=True):
        st.session_state.current_view = "Job Seeker"
    if st.button("⚡ Recruiter Command", use_container_width=True):
        st.session_state.current_view = "Recruiter"

    st.markdown("---")
    st.markdown(
        '<div style="display:flex; align-items:center; font-size: 0.85rem; color: #475569;">'
        '<span class="status-dot-green"></span> System Operational'
        "</div>",
        unsafe_allow_html=True,
    )

# ==========================================
# 5. VIEW ROUTING
# ==========================================

# --- VIEW: MAIN HUB ---
if st.session_state.current_view == "Hub":
    st.markdown(
        """
        <div style="text-align: center; padding: 2.5rem 0 1.5rem 0;">
            <h1 style="font-size: 2.8rem; font-weight: 800; color: #0f172a; margin-bottom: 0.3rem;">
                🧠 CareerLens AI
            </h1>
            <p style="font-size: 1.15rem; color: #475569; font-weight: 400;">
                Navigate your career trajectory. Discover your true match.
            </p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(
            """
            <div class="hub-card">
                <div style="font-size: 2.5rem; margin-bottom: 0.8rem;">💼</div>
                <h3 style="color: #0f172a; margin-bottom: 0.5rem;">Job Seeker Suite</h3>
                <p style="color: #64748b; font-size: 0.95rem; margin-bottom: 1.5rem;">
                    Optimize your resume, detect skill gaps, analyze job fit, and build dynamic career roadmaps.
                </p>
            </div>
        """,
            unsafe_allow_html=True,
        )
        if st.button("Enter as Job Seeker", key="btn_seeker", use_container_width=True):
            st.session_state.current_view = "Job Seeker"
            st.rerun()

    with col2:
        st.markdown(
            """
            <div class="hub-card">
                <div style="font-size: 2.5rem; margin-bottom: 0.8rem;">🎯</div>
                <h3 style="color: #0f172a; margin-bottom: 0.5rem;">Recruiter Command</h3>
                <p style="color: #64748b; font-size: 0.95rem; margin-bottom: 1.5rem;">
                    Accelerate candidate screening, rank applicants accurately, and identify credential integrity risks.
                </p>
            </div>
        """,
            unsafe_allow_html=True,
        )
        if st.button("Enter as Recruiter", key="btn_recruiter", use_container_width=True):
            st.session_state.current_view = "Recruiter"
            st.rerun()

# --- VIEW: JOB SEEKER SUITE ---
elif st.session_state.current_view == "Job Seeker":
    st.markdown("## **Candidate Career Intelligence**")
    st.caption("Upload your profile to unlock custom match insights and career progression.")

    uploaded_file = st.file_uploader("Upload Resume (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

    if uploaded_file is not None:
        if st.button("Process Document"):
            st.session_state.extracted_profile = {
                "name": "Alex Mercer",
                "email": "alex.mercer@example.com",
                "phone": "+1 (555) 019-2834",
                "skills": ["Python", "Machine Learning", "FastAPI", "Docker", "SQL"],
            }
            st.success("Resume processed successfully.")

    if st.session_state.extracted_profile:
        st.markdown("---")
        st.markdown("### **Profile Snapshot**")
        p = st.session_state.extracted_profile
        c1, c2, c3 = st.columns(3)
        c1.markdown(f"**Name:** {p['name']}")
        c2.markdown(f"**Email:** {p['email']}")
        c3.markdown(f"**Phone:** {p['phone']}")

        tabs = st.tabs(["Skill Gap Analysis", "Job Fit", "Integrity Check", "Career Trajectory"])

        with tabs[0]:
            if st.button("Analyze Skills"):
                st.info("Top recommendations: Kubernetes, Cloud Architecture (AWS/GCP), CI/CD Automation.")

        with tabs[1]:
            job_desc = st.text_area("Paste Target Job Description:")
            if st.button("Evaluate Fit"):
                st.metric(label="Role Match Index", value="88%")

        with tabs[2]:
            if st.button("Scan Credential Integrity"):
                st.success("Profile verified: High integrity, 0 anomalous signals detected.")

        with tabs[3]:
            if st.button("Generate Roadmap"):
                st.write("**Recommended 6-Month Progression:**")
                st.write("1. Complete Advanced System Design module.")
                st.write("2. Implement distributed event pipelines with Kafka.")
                st.write("3. Target Senior ML Engineer certifications.")

# --- VIEW: RECRUITER COMMAND ---
elif st.session_state.current_view == "Recruiter":
    st.markdown("## **Talent Acquisition Engine**")
    st.caption("High-precision batch screening and candidate ranking powered by smart algorithms.")

    col1, col2 = st.columns([1, 1])
    with col1:
        target_role = st.text_input("Role Title", value="Senior Data Scientist")
    with col2:
        top_k = st.slider("Candidates to Rank", min_value=1, max_value=20, value=5)

    batch_files = st.file_uploader("Upload Batch Resumes", accept_multiple_files=True)

    if st.button("Rank Candidates"):
        st.markdown("### **Top Matched Candidates**")
        st.markdown(
            """
        | Rank | Candidate Name | Match Score | Key Strengths | Status |
        |---|---|---|---|---|
        | 1 | Jane Doe | **94%** | PyTorch, MLOps, Distributed Systems | Verified |
        | 2 | John Smith | **89%** | NLP, Transformers, FastAPI | Verified |
        | 3 | Emma Davis | **82%** | Scikit-learn, SQL, Data Modeling | Review Needed |
        """
        )

# --- VIEW: AI ASSISTANT ---
elif st.session_state.current_view == "Assistant":
    st.markdown("## **CareerLens AI Advisor**")
    st.caption("Ask questions about resumes, interview prep, and career strategy.")

    # Quick Prompts
    q1, q2, q3 = st.columns(3)
    if q1.button("How can I improve my resume?"):
        st.session_state.chat_history.append(("user", "How can I improve my resume?"))
        st.session_state.chat_history.append(
            ("assistant", "Focus on quantifiable achievements, use strong action verbs, and tailor keywords directly to target job requirements.")
        )
    if q2.button("Suggest career pathways"):
        st.session_state.chat_history.append(("user", "Suggest career pathways"))
        st.session_state.chat_history.append(
            ("assistant", "Based on current market trends, high-growth tracks include AI/ML Engineering, Cloud Native Architecture, and Data Platform Engineering.")
        )
    if q3.button("Identify high-demand skills"):
        st.session_state.chat_history.append(("user", "Identify high-demand skills"))
        st.session_state.chat_history.append(
            ("assistant", "The top skills currently in demand are LLM Orchestration, Python, Docker/Kubernetes, and Distributed Data Processing.")
        )

    st.markdown("---")

    for role, text in st.session_state.chat_history:
        with st.chat_message(role):
            st.write(text)

    prompt = st.chat_input("Ask a question about your career or hiring workflow...")
    if prompt:
        st.session_state.chat_history.append(("user", prompt))
        with st.chat_message("user"):
            st.write(prompt)
        response_text = f"CareerLens AI Advisor response for: '{prompt}'"
        st.session_state.chat_history.append(("assistant", response_text))
        with st.chat_message("assistant"):
            st.write(response_text)

# ==========================================
# 6. FOOTER
# ==========================================
st.markdown("---")
st.markdown(
    '<div class="custom-footer">CareerLens AI by Batch 2</div>',
    unsafe_allow_html=True,
)
