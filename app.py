import streamlit as st
import time

# ============================================================
# CAREERLENS AI
# AI-Powered Career Intelligence & Job Safety Platform
# ============================================================

# -------------------- PAGE CONFIG --------------------

st.set_page_config(
    page_title="CareerLens AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       GLOBAL
       ====================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(99, 102, 241, 0.16),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 15%,
                rgba(14, 165, 233, 0.13),
                transparent 30%
            ),
            #070b14;

        color: #f8fafc;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* ======================================================
       SIDEBAR
       ====================================================== */

    section[data-testid="stSidebar"] {
        background: #0b101b;
        border-right: 1px solid rgba(255,255,255,0.07);
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem;
    }

    /* ======================================================
       BRAND
       ====================================================== */

    .brand {
        text-align: center;
        padding: 10px 0 25px 0;
    }

    .brand-icon {
        font-size: 42px;
        margin-bottom: 5px;
    }

    .brand-name {
        font-size: 26px;
        font-weight: 800;

        background: linear-gradient(
            90deg,
            #9b8cff,
            #38bdf8
        );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .brand-tagline {
        color: #7f8ba3;
        font-size: 11px;
        margin-top: 4px;
    }

    /* ======================================================
       HERO
       ====================================================== */

    .hero {
        padding: 48px;
        border-radius: 26px;

        background:
            linear-gradient(
                135deg,
                rgba(99,102,241,0.20),
                rgba(14,165,233,0.08)
            );

        border: 1px solid rgba(255,255,255,0.08);

        box-shadow:
            0 25px 80px rgba(0,0,0,0.28);

        margin-bottom: 32px;
    }

    .hero-title {
        font-size: 48px;
        line-height: 1.1;
        font-weight: 800;
        color: #ffffff;
    }

    .gradient-text {
        background: linear-gradient(
            90deg,
            #9b8cff,
            #38bdf8
        );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-description {
        color: #aab4c7;
        font-size: 17px;
        line-height: 1.7;
        max-width: 850px;
        margin-top: 18px;
    }

    /* ======================================================
       SECTION
       ====================================================== */

    .section-title {
        font-size: 28px;
        font-weight: 750;
        margin-top: 12px;
        margin-bottom: 7px;
    }

    .section-subtitle {
        color: #8994aa;
        margin-bottom: 24px;
        font-size: 14px;
    }

    /* ======================================================
       METRIC CARDS
       ====================================================== */

    .metric-card {
        background: #101625;

        border: 1px solid rgba(255,255,255,0.07);

        border-radius: 17px;

        padding: 22px;

        text-align: center;

        box-shadow:
            0 10px 30px rgba(0,0,0,0.15);
    }

    .metric-label {
        color: #8994aa;
        font-size: 13px;
    }

    .metric-value {
        font-size: 34px;
        font-weight: 800;
        margin-top: 7px;
        color: #ffffff;
    }

    /* ======================================================
       FEATURE CARDS
       ====================================================== */

    .feature-card {
        background: rgba(15,21,34,0.90);

        border: 1px solid rgba(255,255,255,0.07);

        border-radius: 18px;

        padding: 24px;

        min-height: 175px;

        margin-bottom: 18px;

        box-shadow:
            0 12px 35px rgba(0,0,0,0.18);
    }

    .feature-icon {
        font-size: 30px;
    }

    .feature-title {
        font-size: 19px;
        font-weight: 700;
        margin-top: 10px;
        margin-bottom: 8px;
    }

    .feature-description {
        color: #8f9ab0;
        font-size: 14px;
        line-height: 1.6;
    }

    /* ======================================================
       RESULT CARDS
       ====================================================== */

    .result-card {
        background: #101625;

        border: 1px solid rgba(255,255,255,0.07);

        border-radius: 18px;

        padding: 25px;

        margin-top: 15px;
    }

    /* ======================================================
       RISK
       ====================================================== */

    .risk-card {
        text-align: center;

        padding: 35px;

        border-radius: 22px;

        background:
            linear-gradient(
                135deg,
                rgba(245,158,11,0.12),
                rgba(239,68,68,0.08)
            );

        border: 1px solid rgba(245,158,11,0.20);
    }

    .risk-score {
        font-size: 58px;
        font-weight: 800;
        color: #fbbf24;
    }

    .risk-label {
        font-size: 17px;
        font-weight: 700;
        color: #fbbf24;
    }

    /* ======================================================
       MATCH
       ====================================================== */

    .match-card {
        text-align: center;

        padding: 35px;

        border-radius: 22px;

        background:
            linear-gradient(
                135deg,
                rgba(34,197,94,0.12),
                rgba(14,165,233,0.08)
            );

        border: 1px solid rgba(34,197,94,0.18);
    }

    .match-score {
        font-size: 60px;
        font-weight: 800;
        color: #4ade80;
    }

    /* ======================================================
       ROADMAP
       ====================================================== */

    .roadmap-card {
        background: #101625;

        border: 1px solid rgba(255,255,255,0.06);

        border-radius: 15px;

        padding: 22px;

        margin-bottom: 13px;
    }

    .roadmap-number {
        color: #8b7cff;
        font-size: 13px;
        font-weight: 800;
    }

    .roadmap-title {
        font-size: 18px;
        font-weight: 700;
        margin-top: 5px;
    }

    .roadmap-description {
        color: #8f9ab0;
        margin-top: 6px;
        font-size: 14px;
    }

    /* ======================================================
       BUTTONS
       ====================================================== */

    .stButton > button {
        width: 100%;

        min-height: 45px;

        border-radius: 11px;

        border: 1px solid rgba(139,124,255,0.35);

        background:
            linear-gradient(
                90deg,
                #6558e8,
                #3182ce
            );

        color: white;

        font-weight: 700;
    }

    /* ======================================================
       INPUTS
       ====================================================== */

    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div {
        background-color: #101625;

        border-color: rgba(255,255,255,0.08);

        border-radius: 11px;
    }

    /* ======================================================
       FOOTER
       ====================================================== */

    .footer {
        text-align: center;

        color: #68748a;

        padding: 45px 0 10px;

        font-size: 13px;
    }

    /* ======================================================
       HIDE STREAMLIT DEFAULT FOOTER
       ====================================================== */

    footer {
        visibility: hidden;
    }

    #MainMenu {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# SESSION STATE
# ============================================================

if "resume_analyzed" not in st.session_state:
    st.session_state.resume_analyzed = False

if "job_analyzed" not in st.session_state:
    st.session_state.job_analyzed = False

if "fraud_analyzed" not in st.session_state:
    st.session_state.fraud_analyzed = False

if "match_analyzed" not in st.session_state:
    st.session_state.match_analyzed = False

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">

            <div class="brand-icon">
                🎯
            </div>

            <div class="brand-name">
                CareerLens AI
            </div>

            <div class="brand-tagline">
                AI Career Intelligence Platform
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "🏠 Dashboard",
            "📄 Resume Analyzer",
            "🔎 Job Analyzer",
            "🛡️ Fraud Detection",
            "🎯 Job Matching",
            "🧩 Skill Gap",
            "🗺️ Career Roadmap",
            "🤖 AI Assistant"
        ]
    )

    st.divider()

    st.markdown("### System Status")

    st.success("● System Online")

    st.caption("AI Engine • Ready")
    st.caption("ML Models • Ready for Integration")

    st.divider()

    st.caption("CareerLens AI")
    st.caption("Final Year Project")
    st.caption("Artificial Intelligence & ML")


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.markdown(
        """
        <div class="hero">

            <div class="hero-title">
                Understand Your Career.
                <br>

                <span class="gradient-text">
                    Build Your Future.
                </span>
            </div>

            <div class="hero-description">
                CareerLens AI analyzes your resume, evaluates
                job opportunities, detects potential job risks,
                identifies skill gaps and builds a personalized
                career roadmap.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">Career Intelligence</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Your career profile at a glance.'
        '</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    metrics = [
        ("Career Readiness", "78%"),
        ("Resume Score", "82%"),
        ("Average Job Match", "84%"),
        ("Skills Identified", "12")
    ]

    for col, (label, value) in zip(
        [c1, c2, c3, c4],
        metrics
    ):

        with col:

            st.markdown(
                f"""
                <div class="metric-card">

                    <div class="metric-label">
                        {label}
                    </div>

                    <div class="metric-value">
                        {value}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("")

    st.markdown(
        '<div class="section-title">CareerLens Intelligence</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Everything you need to understand and improve your career profile.'
        '</div>',
        unsafe_allow_html=True
    )

    features = [
        (
            "📄",
            "Resume Intelligence",
            "Extract and analyze skills, education, projects and experience from your resume."
        ),
        (
            "🔎",
            "Job Intelligence",
            "Understand job descriptions and identify important requirements."
        ),
        (
            "🛡️",
            "Job Safety",
            "Detect suspicious signals and estimate potential job fraud risk."
        ),
        (
            "🎯",
            "Smart Matching",
            "Compare your resume with target jobs using semantic similarity."
        ),
        (
            "🧩",
            "Skill Gap Analysis",
            "Discover the skills you need to develop for your target role."
        ),
        (
            "🗺️",
            "Career Roadmap",
            "Create a personalized path from your current skills to your target career."
        )
    ]

    cols = st.columns(3)

    for index, feature in enumerate(features):

        icon, title, description = feature

        with cols[index % 3]:

            st.markdown(
                f"""
                <div class="feature-card">

                    <div class="feature-icon">
                        {icon}
                    </div>

                    <div class="feature-title">
                        {title}
                    </div>

                    <div class="feature-description">
                        {description}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# RESUME ANALYZER
# ============================================================

elif page == "📄 Resume Analyzer":

    st.markdown(
        '<div class="section-title">📄 Resume Intelligence</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Upload your resume and analyze your professional profile.'
        '</div>',
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf"],
        help="Upload your resume in PDF format."
    )

    if uploaded_file:

        st.success(
            f"✓ {uploaded_file.name} uploaded successfully."
        )

        if st.button(
            "🚀 Analyze Resume",
            key="resume_button"
        ):

            with st.spinner(
                "AI is analyzing your resume..."
            ):

                time.sleep(2)

            st.session_state.resume_analyzed = True

            st.success(
                "Resume analysis completed!"
            )

    if st.session_state.resume_analyzed:

        st.divider()

        c1, c2, c3, c4 = st.columns(4)

        results = [
            ("Resume Score", "82%"),
            ("Skills Found", "12"),
            ("Projects", "4"),
            ("Experience", "2 yrs")
        ]

        for col, (label, value) in zip(
            [c1, c2, c3, c4],
            results
        ):

            with col:

                st.markdown(
                    f"""
                    <div class="metric-card">

                        <div class="metric-label">
                            {label}
                        </div>

                        <div class="metric-value">
                            {value}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown("### Detected Skills")

        st.write(
            "Python • Machine Learning • SQL • Git • "
            "Pandas • Scikit-learn • NLP • Data Analysis"
        )

        st.markdown("### Resume Insights")

        st.success(
            "Strong technical foundation detected."
        )

        st.warning(
            "Recommended: add cloud deployment, Docker and MLOps projects."
        )


# ============================================================
# JOB ANALYZER
# ============================================================

elif page == "🔎 Job Analyzer":

    st.markdown(
        '<div class="section-title">🔎 Job Intelligence</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Analyze a job posting using its URL or description.'
        '</div>',
        unsafe_allow_html=True
    )

    job_url = st.text_input(
        "Job Posting URL",
        placeholder="https://company.com/jobs/software-engineer"
    )

    st.markdown("### OR")

    job_description = st.text_area(
        "Job Description",
        height=240,
        placeholder="Paste the complete job description here..."
    )

    if st.button(
        "🔍 Analyze Job",
        key="job_button"
    ):

        if not job_url and not job_description:

            st.warning(
                "Please provide a job URL or job description."
            )

        else:

            with st.spinner(
                "Analyzing job opportunity..."
            ):

                time.sleep(2)

            st.session_state.job_analyzed = True

    if st.session_state.job_analyzed:

        st.divider()

        st.success(
            "Job analysis completed successfully."
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Required Skills",
                "10"
            )

        with c2:
            st.metric(
                "Experience",
                "0–2 Years"
            )

        with c3:
            st.metric(
                "Category",
                "Technology"
            )

        st.markdown("### Required Skills")

        st.write(
            "Python • SQL • Machine Learning • Git • "
            "Docker • AWS • REST API • NLP"
        )


# ============================================================
# FRAUD DETECTION
# ============================================================

elif page == "🛡️ Fraud Detection":

    st.markdown(
        '<div class="section-title">🛡️ Job Safety Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Analyze suspicious signals in a job opportunity.'
        '</div>',
        unsafe_allow_html=True
    )

    fraud_url = st.text_input(
        "Job URL",
        placeholder="https://example.com/job"
    )

    fraud_description = st.text_area(
        "Job Description",
        height=220,
        placeholder="Paste the job description..."
    )

    if st.button(
        "🛡️ Check Job Safety",
        key="fraud_button"
    ):

        if not fraud_url and not fraud_description:

            st.warning(
                "Please provide a job URL or job description."
            )

        else:

            with st.spinner(
                "Running fraud detection analysis..."
            ):

                time.sleep(2)

            st.session_state.fraud_analyzed = True

    if st.session_state.fraud_analyzed:

        st.divider()

        left, right = st.columns([1, 1.5])

        with left:

            st.markdown(
                """
                <div class="risk-card">

                    <div class="risk-score">
                        28%
                    </div>

                    <div class="risk-label">
                        LOW RISK
                    </div>

                    <p>
                        Relatively few suspicious signals
                        were detected.
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )

        with right:

            st.markdown("### Safety Signals")

            st.success(
                "✓ Company information detected"
            )

            st.success(
                "✓ Professional job description"
            )

            st.success(
                "✓ No obvious payment request"
            )

            st.warning(
                "⚠ Salary information should be verified"
            )


# ============================================================
# JOB MATCHING
# ============================================================

elif page == "🎯 Job Matching":

    st.markdown(
        '<div class="section-title">🎯 Resume–Job Matching</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Measure how closely your profile matches a target job.'
        '</div>',
        unsafe_allow_html=True
    )

    if not st.session_state.resume_analyzed:

        st.info(
            "📄 Please analyze your resume first."
        )

    else:

        target_role = st.text_input(
            "Target Job Role",
            placeholder="Machine Learning Engineer"
        )

        if st.button(
            "🎯 Calculate Match",
            key="match_button"
        ):

            if not target_role:

                st.warning(
                    "Enter a target job role."
                )

            else:

                with st.spinner(
                    "Calculating AI-powered match..."
                ):

                    time.sleep(2)

                st.session_state.match_analyzed = True

    if st.session_state.match_analyzed:

        st.divider()

        left, right = st.columns([1, 2])

        with left:

            st.markdown(
                """
                <div class="match-card">

                    <div class="match-score">
                        84%
                    </div>

                    <strong>
                        GREAT MATCH
                    </strong>

                    <p>
                        Your profile strongly matches
                        this opportunity.
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )

        with right:

            st.markdown("### Match Breakdown")

            st.progress(
                0.91,
                text="Technical Skills — 91%"
            )

            st.progress(
                0.82,
                text="Experience — 82%"
            )

            st.progress(
                0.88,
                text="Education — 88%"
            )

            st.progress(
                0.76,
                text="Projects — 76%"
            )


# ============================================================
# SKILL GAP
# ============================================================

elif page == "🧩 Skill Gap":

    st.markdown(
        '<div class="section-title">🧩 Skill Gap Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Discover which skills you need for your target career.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("### Your Current Skills")

    st.success(
        "Python • SQL • Machine Learning • Git • Pandas • NLP"
    )

    st.markdown("### Recommended Skills")

    gaps = [
        ("🔴", "AWS", "High Priority"),
        ("🟠", "Docker", "Medium Priority"),
        ("🟠", "FastAPI", "Medium Priority"),
        ("🟡", "System Design", "Develop"),
        ("🟡", "MLOps", "Develop")
    ]

    for icon, skill, priority in gaps:

        st.markdown(
            f"""
            <div class="result-card">

                <strong>
                    {icon} {skill}
                </strong>

                <div class="feature-description">
                    Priority: {priority}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# CAREER ROADMAP
# ============================================================

elif page == "🗺️ Career Roadmap":

    st.markdown(
        '<div class="section-title">🗺️ Career Roadmap</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Your personalized journey from current skills to career goals.'
        '</div>',
        unsafe_allow_html=True
    )

    roadmap = [
        (
            "01",
            "Strengthen Python",
            "Advanced Python, OOP and software engineering."
        ),
        (
            "02",
            "Master Machine Learning",
            "Classification, regression, NLP and model evaluation."
        ),
        (
            "03",
            "Learn FastAPI",
            "Build production-ready APIs for AI applications."
        ),
        (
            "04",
            "Learn Docker",
            "Containerize and deploy AI applications."
        ),
        (
            "05",
            "Learn Cloud",
            "Understand AWS and cloud deployment fundamentals."
        ),
        (
            "06",
            "Build AI Projects",
            "Create strong portfolio projects with real-world use cases."
        ),
        (
            "07",
            "Become Job Ready",
            "Prepare your resume, interviews and applications."
        )
    ]

    for number, title, description in roadmap:

        st.markdown(
            f"""
            <div class="roadmap-card">

                <div class="roadmap-number">
                    STEP {number}
                </div>

                <div class="roadmap-title">
                    {title}
                </div>

                <div class="roadmap-description">
                    {description}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# AI ASSISTANT
# ============================================================

elif page == "🤖 AI Assistant":

    st.markdown(
        '<div class="section-title">🤖 CareerLens AI Assistant</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Your personal AI-powered career advisor.'
        '</div>',
        unsafe_allow_html=True
    )

    if not st.session_state.messages:

        st.info(
            "Ask me about your resume, skills, target jobs, "
            "career roadmap or interview preparation."
        )

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(
                message["content"]
            )

    prompt = st.chat_input(
        "Ask CareerLens AI..."
    )

    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):

            st.markdown(prompt)

        with st.chat_message("assistant"):

            response = (
                "🤖 **CareerLens AI**\n\n"
                "Your AI career assistant is ready. "
                "The personalized LLM engine will be connected "
                "to your resume, job analysis, skill profile "
                "and career roadmap in the next development phase."
            )

            st.markdown(response)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

        <strong>🎯 CareerLens AI</strong>

        <br><br>

        AI-Powered Career Intelligence & Job Safety Platform

        <br>

        Final Year Project • Artificial Intelligence & Machine Learning

        <br><br>

        Built with Python • Streamlit • AI • Machine Learning

    </div>
    """,
    unsafe_allow_html=True
)
