import streamlit as st

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CareerLens AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# SESSION STATE
# ============================================================

if "role" not in st.session_state:
    st.session_state.role = "Job Seeker"

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- MAIN APP ---------- */

    .stApp {
        background: #080d18;
    }

    .main .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background: #0b1220;
        border-right: 1px solid #202c42;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }

    /* ---------- BRAND ---------- */

    .brand-box {
        text-align: center;
        padding: 10px 0 25px 0;
    }

    .brand-icon {
        font-size: 42px;
        margin-bottom: 5px;
    }

    .brand-name {
        font-size: 25px;
        font-weight: 800;
        color: #ffffff;
    }

    .brand-name span {
        color: #8b7cff;
    }

    .brand-subtitle {
        font-size: 12px;
        color: #7f8ba3;
        margin-top: 5px;
    }

    /* ---------- HERO ---------- */

    .hero-box {
        background: linear-gradient(
            135deg,
            #121c31 0%,
            #0d1627 100%
        );

        border: 1px solid #263550;
        border-radius: 24px;

        padding: 45px;

        margin-bottom: 35px;

        box-shadow: 0 15px 45px rgba(0,0,0,0.25);
    }

    .hero-small {
        color: #8b7cff;
        font-size: 14px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 12px;
    }

    .hero-title {
        color: #ffffff;
        font-size: 48px;
        font-weight: 800;
        line-height: 1.15;
    }

    .hero-gradient {
        background: linear-gradient(
            90deg,
            #8b7cff,
            #38bdf8
        );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-text {
        color: #9aa7bd;
        font-size: 17px;
        line-height: 1.7;
        max-width: 850px;
        margin-top: 18px;
    }

    /* ---------- SECTION ---------- */

    .section-title {
        color: #ffffff;
        font-size: 27px;
        font-weight: 750;
        margin-top: 25px;
    }

    .section-subtitle {
        color: #8996ac;
        font-size: 14px;
        margin-top: 5px;
        margin-bottom: 22px;
    }

    /* ---------- CARDS ---------- */

    .feature-card {
        background: #101929;
        border: 1px solid #243149;
        border-radius: 18px;

        padding: 24px;

        min-height: 155px;

        margin-bottom: 18px;

        transition: 0.2s;
    }

    .feature-icon {
        font-size: 30px;
        margin-bottom: 10px;
    }

    .feature-title {
        color: #ffffff;
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 7px;
    }

    .feature-description {
        color: #8d9ab0;
        font-size: 13px;
        line-height: 1.55;
    }

    /* ---------- METRIC CARDS ---------- */

    .metric-card {
        background: #101929;
        border: 1px solid #243149;
        border-radius: 18px;

        padding: 22px;

        text-align: center;

        margin-bottom: 20px;
    }

    .metric-title {
        color: #8996ac;
        font-size: 13px;
    }

    .metric-number {
        color: #ffffff;
        font-size: 30px;
        font-weight: 800;
        margin-top: 5px;
    }

    /* ---------- STATUS ---------- */

    .status-box {
        background: #0d2a20;
        border: 1px solid #1c5943;
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        color: #6ee7b7;
        font-size: 13px;
    }

    /* ---------- FOOTER ---------- */

    .footer {
        border-top: 1px solid #202c42;
        margin-top: 50px;
        padding-top: 25px;
        text-align: center;
        color: #66738a;
        font-size: 13px;
    }

    /* ---------- BUTTON ---------- */

    .stButton > button {
        border-radius: 10px;
        min-height: 42px;
        font-weight: 650;
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
        <div class="brand-box">
            <div class="brand-icon">🎯</div>

            <div class="brand-name">
                Career<span>Lens</span> AI
            </div>

            <div class="brand-subtitle">
                Career Intelligence Platform
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.caption("WORKSPACE")

    role = st.radio(
        "Choose workspace",
        ["Job Seeker", "Recruiter"],
        index=0 if st.session_state.role == "Job Seeker" else 1,
        label_visibility="collapsed"
    )

    st.session_state.role = role

    st.divider()

    if role == "Job Seeker":

        st.markdown("### 👨‍💻 Job Seeker")

        page = st.radio(
            "Job Seeker Navigation",
            [
                "Dashboard",
                "Resume Analyzer",
                "Job Analyzer",
                "Job Fraud Detection",
                "Job Matching",
                "Skill Gap Analysis",
                "Career Roadmap",
                "Application Tracker",
                "AI Career Assistant"
            ],
            label_visibility="collapsed"
        )

    else:

        st.markdown("### 🧑‍💼 Recruiter")

        page = st.radio(
            "Recruiter Navigation",
            [
                "Dashboard",
                "Create Job",
                "Bulk Resume Upload",
                "Candidate Ranking",
                "Candidate Comparison",
                "Shortlist",
                "Recruitment Pipeline",
                "Hiring Analytics",
                "AI Recruiter Assistant"
            ],
            label_visibility="collapsed"
        )

    st.divider()

    st.markdown(
        """
        <div class="status-box">
            ● System Online
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    st.caption("CareerLens AI")
    st.caption("AI • ML • NLP")

# ============================================================
# JOB SEEKER DASHBOARD
# ============================================================

if role == "Job Seeker" and page == "Dashboard":

    st.markdown(
        """
        <div class="hero-box">

            <div class="hero-small">
                AI Career Intelligence
            </div>

            <div class="hero-title">
                Understand Your Career.
                <br>
                <span class="hero-gradient">
                    Build Your Future.
                </span>
            </div>

            <div class="hero-text">
                CareerLens AI analyzes your resume, evaluates
                opportunities, detects potential job risks,
                identifies skill gaps and helps you build a
                personalized career roadmap.
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

    metrics = [
        ("Resume Score", "—"),
        ("Career Readiness", "—"),
        ("Job Matches", "0"),
        ("Applications", "0")
    ]

    for col, (title, value) in zip(
        [c1, c2, c3, c4],
        metrics
    ):

        with col:

            st.markdown(
                f"""
                <div class="metric-card">

                    <div class="metric-title">
                        {title}
                    </div>

                    <div class="metric-number">
                        {value}
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
        'AI-powered tools designed to help you make better career decisions.'
        '</div>',
        unsafe_allow_html=True
    )

    features = [
        (
            "📄",
            "Resume Intelligence",
            "Analyze your resume and extract skills, education, projects and experience."
        ),
        (
            "🔎",
            "Job Intelligence",
            "Understand job descriptions and identify important requirements."
        ),
        (
            "🛡️",
            "Job Fraud Detection",
            "Identify suspicious signals and potential risks in job postings."
        ),
        (
            "🎯",
            "AI Job Matching",
            "Measure how closely your profile matches a specific opportunity."
        ),
        (
            "🧩",
            "Skill Gap Analysis",
            "Discover the skills you need for your target career."
        ),
        (
            "🗺️",
            "Career Roadmap",
            "Create a personalized learning and career development path."
        )
    ]

    cols = st.columns(3)

    for i, (icon, title, description) in enumerate(features):

        with cols[i % 3]:

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

elif role == "Job Seeker" and page == "Resume Analyzer":

    st.markdown(
        '<div class="section-title">📄 Resume Analyzer</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Upload your resume and let CareerLens AI analyze it.'
        '</div>',
        unsafe_allow_html=True
    )

    resume = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx"]
    )

    if resume:

        st.success(f"Resume uploaded: {resume.name}")

        if st.button(
            "Analyze Resume",
            use_container_width=True
        ):

            st.info(
                "Resume parsing and AI scoring will be connected next."
            )

# ============================================================
# JOB ANALYZER
# ============================================================

elif role == "Job Seeker" and page == "Job Analyzer":

    st.markdown(
        '<div class="section-title">🔎 Job Analyzer</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Analyze a job opportunity before applying.'
        '</div>',
        unsafe_allow_html=True
    )

    job_url = st.text_input(
        "Job URL",
        placeholder="Paste job URL here..."
    )

    job_description = st.text_area(
        "Job Description",
        height=250,
        placeholder="Paste the complete job description here..."
    )

    if st.button(
        "Analyze Job",
        use_container_width=True
    ):

        if not job_url and not job_description:

            st.warning(
                "Please provide a job URL or job description."
            )

        else:

            st.info(
                "Job analysis engine will be connected next."
            )

# ============================================================
# FRAUD DETECTION
# ============================================================

elif role == "Job Seeker" and page == "Job Fraud Detection":

    st.markdown(
        '<div class="section-title">🛡️ Job Fraud Detection</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Check a job posting for suspicious characteristics.'
        '</div>',
        unsafe_allow_html=True
    )

    text = st.text_area(
        "Job Posting",
        height=280,
        placeholder="Paste job posting here..."
    )

    if st.button(
        "Check Job Safety",
        use_container_width=True
    ):

        if not text.strip():

            st.warning("Please enter a job posting.")

        else:

            st.info(
                "Fraud detection model will be connected next."
            )

# ============================================================
# JOB MATCHING
# ============================================================

elif role == "Job Seeker" and page == "Job Matching":

    st.markdown(
        '<div class="section-title">🎯 AI Job Matching</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Compare your profile with a job opportunity.'
        '</div>',
        unsafe_allow_html=True
    )

    job = st.text_area(
        "Job Description",
        height=280
    )

    if st.button(
        "Calculate Match",
        use_container_width=True
    ):

        if not job.strip():

            st.warning("Please enter a job description.")

        else:

            st.info(
                "Semantic matching model will be connected next."
            )

# ============================================================
# SKILL GAP
# ============================================================

elif role == "Job Seeker" and page == "Skill Gap Analysis":

    st.markdown(
        '<div class="section-title">🧩 Skill Gap Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Understand what skills you need to reach your target role.'
        '</div>',
        unsafe_allow_html=True
    )

    current = st.text_area(
        "Your Current Skills",
        placeholder="Python, SQL, HTML, Machine Learning..."
    )

    target = st.text_area(
        "Target Job Requirements",
        placeholder="Python, SQL, NLP, Docker..."
    )

    if st.button(
        "Analyze Skill Gap",
        use_container_width=True
    ):

        if not current or not target:

            st.warning(
                "Enter both your current skills and target requirements."
            )

        else:

            st.info(
                "Skill gap engine will be connected next."
            )

# ============================================================
# CAREER ROADMAP
# ============================================================

elif role == "Job Seeker" and page == "Career Roadmap":

    st.markdown(
        '<div class="section-title">🗺️ Career Roadmap</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Your personalized path toward your target career.'
        '</div>',
        unsafe_allow_html=True
    )

    target_role = st.text_input(
        "Target Career",
        placeholder="Machine Learning Engineer"
    )

    if st.button(
        "Generate Roadmap",
        use_container_width=True
    ):

        if not target_role:

            st.warning("Enter a target career.")

        else:

            steps = [
                "Build foundational knowledge",
                "Develop required technical skills",
                "Complete practical projects",
                "Build your portfolio",
                "Prepare for technical interviews",
                "Apply for relevant positions"
            ]

            for i, step in enumerate(steps, 1):

                st.markdown(
                    f"""
                    <div class="feature-card">

                        <div class="feature-title">
                            Step {i}
                        </div>

                        <div class="feature-description">
                            {step}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

# ============================================================
# APPLICATION TRACKER
# ============================================================

elif role == "Job Seeker" and page == "Application Tracker":

    st.markdown(
        '<div class="section-title">📋 Application Tracker</div>',
        unsafe_allow_html=True
    )

    st.info(
        "Your job applications will appear here once the database is connected."
    )

# ============================================================
# CAREER ASSISTANT
# ============================================================

elif role == "Job Seeker" and page == "AI Career Assistant":

    st.markdown(
        '<div class="section-title">🤖 AI Career Assistant</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Ask questions about your career, skills and job search.'
        '</div>',
        unsafe_allow_html=True
    )

    question = st.chat_input(
        "Ask CareerLens AI..."
    )

    if question:

        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            st.write(
                "The AI career assistant will be connected to "
                "the language model in the next phase."
            )

# ============================================================
# RECRUITER DASHBOARD
# ============================================================

elif role == "Recruiter" and page == "Dashboard":

    st.markdown(
        """
        <div class="hero-box">

            <div class="hero-small">
                AI Recruitment Intelligence
            </div>

            <div class="hero-title">
                Recruit Smarter.
                <br>
                <span class="hero-gradient">
                    Hire Better.
                </span>
            </div>

            <div class="hero-text">
                Upload hundreds of resumes, let CareerLens AI
                analyze candidate profiles, compare skills and
                experience, and create an intelligent shortlist.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    metrics = [
        ("Active Jobs", "0"),
        ("Candidates", "0"),
        ("Shortlisted", "0"),
        ("Interviews", "0")
    ]

    for col, (title, value) in zip(
        [c1, c2, c3, c4],
        metrics
    ):

        with col:

            st.markdown(
                f"""
                <div class="metric-card">

                    <div class="metric-title">
                        {title}
                    </div>

                    <div class="metric-number">
                        {value}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown(
        '<div class="section-title">Recruitment Intelligence</div>',
        unsafe_allow_html=True
    )

    recruiter_features = [
        (
            "📋",
            "Create Job",
            "Define skills, experience and hiring requirements."
        ),
        (
            "📂",
            "Bulk Resume Upload",
            "Upload 100 or more resumes at once."
        ),
        (
            "🧠",
            "AI Candidate Ranking",
            "Rank candidates according to the selected job."
        ),
        (
            "🔍",
            "Smart Filters",
            "Filter candidates by skills and experience."
        ),
        (
            "⚖️",
            "Candidate Comparison",
            "Compare shortlisted candidates side by side."
        ),
        (
            "📊",
            "Hiring Analytics",
            "Track your recruitment pipeline and performance."
        )
    ]

    cols = st.columns(3)

    for i, (icon, title, description) in enumerate(
        recruiter_features
    ):

        with cols[i % 3]:

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
# CREATE JOB
# ============================================================

elif role == "Recruiter" and page == "Create Job":

    st.markdown(
        '<div class="section-title">📋 Create Job</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Define the job requirements used by the AI ranking engine.'
        '</div>',
        unsafe_allow_html=True
    )

    job_title = st.text_input(
        "Job Title",
        placeholder="Machine Learning Engineer"
    )

    company = st.text_input(
        "Company"
    )

    skills = st.text_area(
        "Required Skills",
        placeholder="Python, SQL, Machine Learning, NLP..."
    )

    experience = st.number_input(
        "Minimum Experience",
        min_value=0,
        max_value=30,
        value=0
    )

    description = st.text_area(
        "Job Description",
        height=250
    )

    if st.button(
        "Create Job",
        use_container_width=True
    ):

        if not job_title:

            st.warning("Job title is required.")

        else:

            st.success(
                f"Job '{job_title}' created successfully."
            )

# ============================================================
# BULK RESUME UPLOAD
# ============================================================

elif role == "Recruiter" and page == "Bulk Resume Upload":

    st.markdown(
        '<div class="section-title">📂 Bulk Resume Upload</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Upload multiple candidate resumes for AI analysis.'
        '</div>',
        unsafe_allow_html=True
    )

    resumes = st.file_uploader(
        "Candidate Resumes",
        type=["pdf", "docx"],
        accept_multiple_files=True
    )

    if resumes:

        st.success(
            f"{len(resumes)} resume(s) uploaded."
        )

        if st.button(
            "Analyze Candidates",
            use_container_width=True
        ):

            st.info(
                "Resume parsing engine will be connected next."
            )

# ============================================================
# CANDIDATE RANKING
# ============================================================

elif role == "Recruiter" and page == "Candidate Ranking":

    st.markdown(
        '<div class="section-title">🧠 AI Candidate Ranking</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Choose exactly how many top candidates you want to review.'
        '</div>',
        unsafe_allow_html=True
    )

    top_n = st.selectbox(
        "Show Top Candidates",
        [
            5,
            10,
            20,
            30,
            50,
            100
        ]
    )

    min_score = st.slider(
        "Minimum Match Score",
        0,
        100,
        60
    )

    st.info(
        f"Configuration: Top {top_n} candidates • "
        f"Minimum score {min_score}%"
    )

    if st.button(
        "Rank Candidates",
        use_container_width=True
    ):

        st.info(
            "AI ranking engine will be connected after "
            "the resume parser and matching model."
        )

# ============================================================
# CANDIDATE COMPARISON
# ============================================================

elif role == "Recruiter" and page == "Candidate Comparison":

    st.markdown(
        '<div class="section-title">⚖️ Candidate Comparison</div>',
        unsafe_allow_html=True
    )

    st.info(
        "Select candidates from the ranking results to compare them here."
    )

# ============================================================
# SHORTLIST
# ============================================================

elif role == "Recruiter" and page == "Shortlist":

    st.markdown(
        '<div class="section-title">⭐ Shortlisted Candidates</div>',
        unsafe_allow_html=True
    )

    st.info(
        "Recruiter-selected candidates will appear here."
    )

# ============================================================
# PIPELINE
# ============================================================

elif role == "Recruiter" and page == "Recruitment Pipeline":

    st.markdown(
        '<div class="section-title">📊 Recruitment Pipeline</div>',
        unsafe_allow_html=True
    )

    columns = st.columns(4)

    stages = [
        ("Applied", 0),
        ("Shortlisted", 0),
        ("Interview", 0),
        ("Selected", 0)
    ]

    for col, (stage, count) in zip(columns, stages):

        with col:

            st.markdown(
                f"""
                <div class="metric-card">

                    <div class="metric-title">
                        {stage}
                    </div>

                    <div class="metric-number">
                        {count}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

# ============================================================
# ANALYTICS
# ============================================================

elif role == "Recruiter" and page == "Hiring Analytics":

    st.markdown(
        '<div class="section-title">📈 Hiring Analytics</div>',
        unsafe_allow_html=True
    )

    st.info(
        "Analytics will be populated from the recruitment database."
    )

# ============================================================
# RECRUITER AI
# ============================================================

elif role == "Recruiter" and page == "AI Recruiter Assistant":

    st.markdown(
        '<div class="section-title">🤖 AI Recruiter Assistant</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Ask questions about your candidate pool.'
        '</div>',
        unsafe_allow_html=True
    )

    question = st.chat_input(
        "Example: Show me the strongest Python candidates..."
    )

    if question:

        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            st.write(
                "The AI recruiter assistant will be connected "
                "to the candidate database and ranking engine."
            )

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

        🎯 <b>CareerLens AI</b>
        <br><br>
        AI-Powered Career Intelligence & Recruitment Platform
        <br>
        Final Year Project • AI • ML • NLP

    </div>
    """,
    unsafe_allow_html=True
)
