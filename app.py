import streamlit as st

# ============================================================
# CAREERLENS AI
# AI-Powered Career Intelligence Platform
# ============================================================

# ------------------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------------------

st.set_page_config(
    page_title="CareerLens AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------
# CUSTOM CSS
# ------------------------------------------------------------

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(90, 80, 200, 0.18),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(0, 180, 255, 0.12),
                transparent 30%
            ),
            #080b14;
        color: #f5f7ff;
    }

    /* ---------- MAIN CONTAINER ---------- */

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background: #0d111c;
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    /* ---------- BRAND ---------- */

    .brand {
        text-align: center;
        padding: 10px 0 25px 0;
    }

    .brand-icon {
        font-size: 42px;
        margin-bottom: 5px;
    }

    .brand-title {
        font-size: 26px;
        font-weight: 800;
        background: linear-gradient(
            90deg,
            #8b7cff,
            #4cc9ff
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .brand-subtitle {
        font-size: 12px;
        color: #8f98ad;
        margin-top: 3px;
    }

    /* ---------- HERO ---------- */

    .hero {
        padding: 42px;
        border-radius: 24px;
        margin-bottom: 30px;

        background:
            linear-gradient(
                135deg,
                rgba(98, 83, 255, 0.22),
                rgba(0, 181, 255, 0.10)
            );

        border: 1px solid rgba(255,255,255,0.09);

        box-shadow:
            0 20px 60px rgba(0,0,0,0.25);
    }

    .hero-title {
        font-size: 48px;
        font-weight: 850;
        line-height: 1.1;
        margin-bottom: 15px;
    }

    .gradient-text {
        background: linear-gradient(
            90deg,
            #9b8cff,
            #4dd8ff
        );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-description {
        font-size: 18px;
        color: #aeb7ca;
        max-width: 800px;
        line-height: 1.7;
    }

    /* ---------- SECTION TITLES ---------- */

    .section-title {
        font-size: 28px;
        font-weight: 750;
        margin-top: 25px;
        margin-bottom: 8px;
    }

    .section-subtitle {
        color: #8f98ad;
        margin-bottom: 22px;
    }

    /* ---------- CARDS ---------- */

    .card {
        background: rgba(18, 23, 37, 0.88);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 18px;
        padding: 24px;
        min-height: 175px;

        box-shadow:
            0 12px 35px rgba(0,0,0,0.18);

        transition: all 0.2s ease;
    }

    .card:hover {
        transform: translateY(-3px);
        border-color: rgba(130,120,255,0.35);
    }

    .card-icon {
        font-size: 30px;
        margin-bottom: 12px;
    }

    .card-title {
        font-size: 19px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .card-text {
        color: #929cb0;
        font-size: 14px;
        line-height: 1.6;
    }

    /* ---------- METRIC CARDS ---------- */

    .metric-card {
        background: #111726;
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
    }

    .metric-label {
        color: #8f98ad;
        font-size: 13px;
    }

    .metric-value {
        font-size: 34px;
        font-weight: 800;
        margin-top: 5px;
    }

    /* ---------- INPUTS ---------- */

    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div {
        background-color: #111726;
        border-color: rgba(255,255,255,0.08);
        border-radius: 12px;
    }

    /* ---------- BUTTONS ---------- */

    .stButton > button {
        width: 100%;
        border-radius: 12px;
        border: 1px solid rgba(140,130,255,0.35);
        background: linear-gradient(
            90deg,
            #6558e8,
            #438fe8
        );
        color: white;
        font-weight: 700;
        padding: 0.65rem 1rem;
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        border-color: rgba(255,255,255,0.5);
        transform: translateY(-1px);
    }

    /* ---------- BADGES ---------- */

    .badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 700;
        background: rgba(89, 213, 159, 0.12);
        color: #69e0aa;
        border: 1px solid rgba(89,213,159,0.2);
    }

    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        color: #687287;
        font-size: 13px;
        padding: 35px 0 10px 0;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">
            <div class="brand-icon">🎯</div>
            <div class="brand-title">CareerLens AI</div>
            <div class="brand-subtitle">
                Career Intelligence Platform
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    page = st.radio(
        "Navigation",
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

    st.caption("CareerLens AI")
    st.caption("Final Year Project")
    st.caption("AI & Machine Learning")

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
                CareerLens AI analyzes your resume, evaluates job
                opportunities, detects potential job risks,
                identifies skill gaps and builds a personalized
                career roadmap.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">Career Overview</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Your career intelligence at a glance.'
        '</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Career Readiness</div>
                <div class="metric-value">--</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Resume Score</div>
                <div class="metric-value">--</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Job Matches</div>
                <div class="metric-value">--</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Skill Gaps</div>
                <div class="metric-value">--</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("")

    st.markdown(
        '<div class="section-title">CareerLens Features</div>',
        unsafe_allow_html=True
    )

    features = [
        ("📄", "Resume Intelligence",
         "Extract skills, education, projects and experience from your resume."),

        ("🔎", "Job Intelligence",
         "Analyze job descriptions and identify important requirements."),

        ("🛡️", "Job Safety",
         "Analyze suspicious signals and estimate potential job fraud risk."),

        ("🎯", "Smart Matching",
         "Compare your resume with a target job using semantic similarity."),

        ("🧩", "Skill Gap Analysis",
         "Discover the skills you need to develop for your target role."),

        ("🗺️", "Career Roadmap",
         "Generate a personalized path from your current skills to your target career.")
    ]

    cols = st.columns(3)

    for i, (icon, title, text) in enumerate(features):

        with cols[i % 3]:

            st.markdown(
                f"""
                <div class="card">

                    <div class="card-icon">
                        {icon}
                    </div>

                    <div class="card-title">
                        {title}
                    </div>

                    <div class="card-text">
                        {text}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        if i in [2, 5]:
            st.markdown("")

# ============================================================
# RESUME ANALYZER
# ============================================================

elif page == "📄 Resume Analyzer":

    st.markdown(
        '<div class="section-title">📄 Resume Analyzer</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Upload your resume and let CareerLens analyze your professional profile.'
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
            f"Resume uploaded: {uploaded_file.name}"
        )

        if st.button("🚀 Analyze Resume"):

            with st.spinner("Analyzing your resume..."):
                st.info(
                    "Resume AI module will be connected here."
                )

# ============================================================
# JOB ANALYZER
# ============================================================

elif page == "🔎 Job Analyzer":

    st.markdown(
        '<div class="section-title">🔎 Job Analyzer</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Analyze a job URL or paste the complete job description.'
        '</div>',
        unsafe_allow_html=True
    )

    job_url = st.text_input(
        "Job URL",
        placeholder="https://example.com/job"
    )

    st.markdown("### OR")

    job_description = st.text_area(
        "Job Description",
        height=220,
        placeholder="Paste the job description here..."
    )

    if st.button("🔍 Analyze Job"):

        if not job_url and not job_description:

            st.warning(
                "Please provide a job URL or job description."
            )

        else:

            with st.spinner("Analyzing job opportunity..."):

                st.info(
                    "Job intelligence module will be connected here."
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
        'Evaluate potential warning signals in a job opportunity.'
        '</div>',
        unsafe_allow_html=True
    )

    fraud_url = st.text_input(
        "Job URL",
        placeholder="https://example.com/job"
    )

    fraud_text = st.text_area(
        "Job Description",
        height=200,
        placeholder="Paste the job description..."
    )

    if st.button("🛡️ Analyze Job Safety"):

        if not fraud_url and not fraud_text:

            st.warning(
                "Please provide a job URL or job description."
            )

        else:

            with st.spinner("Running fraud detection analysis..."):

                st.info(
                    "Fraud detection model will be connected here."
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
        'Measure how well your profile matches a target job.'
        '</div>',
        unsafe_allow_html=True
    )

    if st.button("🎯 Calculate Match"):

        with st.spinner("Calculating semantic match..."):

            st.info(
                "Matching engine will be connected here."
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
        'Discover which skills you need to reach your target role.'
        '</div>',
        unsafe_allow_html=True
    )

    st.info(
        "Skill gap engine will compare your resume skills "
        "against the target job requirements."
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
        'Your personalized path from current skills to your target career.'
        '</div>',
        unsafe_allow_html=True
    )

    roadmap_steps = [
        ("01", "Current Profile", "Analyze your existing skills."),
        ("02", "Identify Gaps", "Find the skills required for your target."),
        ("03", "Learning Plan", "Prioritize what to learn."),
        ("04", "Build Projects", "Apply your knowledge through projects."),
        ("05", "Job Ready", "Prepare for applications and interviews.")
    ]

    for number, title, description in roadmap_steps:

        st.markdown(
            f"""
            <div class="card" style="margin-bottom:12px;">

                <strong>{number} — {title}</strong>

                <div class="card-text">
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
        'Ask questions about your resume, target jobs, skills and career roadmap.'
        '</div>',
        unsafe_allow_html=True
    )

    if "messages" not in st.session_state:

        st.session_state.messages = []

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

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

        response = (
            "🤖 CareerLens AI is being connected to the "
            "personalized career intelligence engine. "
            "Once the AI backend is connected, I will analyze "
            "your resume, target job and skill profile."
        )

        with st.chat_message("assistant"):
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
        <strong>CareerLens AI</strong><br>
        AI-Powered Career Intelligence Platform<br><br>
        Final Year Project • Artificial Intelligence & Machine Learning
    </div>
    """,
    unsafe_allow_html=True
)
