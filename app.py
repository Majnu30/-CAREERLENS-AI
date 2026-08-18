import streamlit as st

# ============================================================
# CAREERLENS AI
# AI-Powered Career Intelligence & Recruitment Platform
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
    st.session_state.role = None

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ================= GLOBAL ================= */

    .stApp {
        background-color: #080d18;
        color: #ffffff;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* ================= SIDEBAR ================= */

    section[data-testid="stSidebar"] {
        background-color: #0d1422;
        border-right: 1px solid #202b40;
    }

    /* ================= BRAND ================= */

    .brand {
        text-align: center;
        padding: 10px 0 25px 0;
    }

    .brand-icon {
        font-size: 42px;
    }

    .brand-title {
        font-size: 25px;
        font-weight: 800;

        background: linear-gradient(
            90deg,
            #8b7cff,
            #38bdf8
        );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .brand-subtitle {
        color: #7f8ba3;
        font-size: 12px;
        margin-top: 5px;
    }

    /* ================= HERO ================= */

    .hero {
        padding: 45px;
        border-radius: 25px;

        background:
            linear-gradient(
                135deg,
                #121b30,
                #0e1728
            );

        border: 1px solid #25324a;

        margin-bottom: 30px;
    }

    .hero-title {
        font-size: 48px;
        font-weight: 800;
        line-height: 1.15;
    }

    .gradient-text {
        background: linear-gradient(
            90deg,
            #8b7cff,
            #38bdf8
        );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-description {
        max-width: 850px;
        margin-top: 18px;

        color: #9aa6bb;

        font-size: 17px;
        line-height: 1.7;
    }

    /* ================= SECTION ================= */

    .section-title {
        font-size: 28px;
        font-weight: 750;
        margin-top: 25px;
        margin-bottom: 6px;
    }

    .section-description {
        color: #8995aa;
        margin-bottom: 25px;
    }

    /* ================= CARDS ================= */

    .card {
        background-color: #111a2b;

        border: 1px solid #25324a;

        border-radius: 18px;

        padding: 25px;

        margin-bottom: 18px;
    }

    .card-icon {
        font-size: 30px;
    }

    .card-title {
        font-size: 19px;
        font-weight: 700;

        margin-top: 10px;
        margin-bottom: 8px;
    }

    .card-text {
        color: #929eb3;

        font-size: 14px;

        line-height: 1.6;
    }

    /* ================= METRIC ================= */

    .metric-card {
        background-color: #111a2b;

        border: 1px solid #25324a;

        border-radius: 17px;

        padding: 20px;

        text-align: center;
    }

    .metric-label {
        color: #8995aa;

        font-size: 13px;
    }

    .metric-value {
        color: #ffffff;

        font-size: 32px;

        font-weight: 800;

        margin-top: 5px;
    }

    /* ================= BUTTONS ================= */

    .stButton > button {
        border-radius: 10px;

        min-height: 42px;

        font-weight: 700;
    }

    /* ================= FOOTER ================= */

    .footer {
        text-align: center;

        color: #66738a;

        margin-top: 50px;

        padding: 30px 0;

        border-top: 1px solid #1d2739;
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

            <div class="brand-icon">
                🎯
            </div>

            <div class="brand-title">
                CareerLens AI
            </div>

            <div class="brand-subtitle">
                Career Intelligence Platform
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # --------------------------------------------------------
    # ROLE SELECTION
    # --------------------------------------------------------

    selected_role = st.radio(
        "WORKSPACE",
        [
            "Job Seeker",
            "Recruiter"
        ],
        index=0 if st.session_state.role != "Recruiter"
        else 1
    )

    st.session_state.role = selected_role

    st.divider()

    # --------------------------------------------------------
    # JOB SEEKER NAVIGATION
    # --------------------------------------------------------

    if selected_role == "Job Seeker":

        st.markdown("### Job Seeker")

        page = st.radio(
            "Navigation",
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
            ]
        )

    # --------------------------------------------------------
    # RECRUITER NAVIGATION
    # --------------------------------------------------------

    else:

        st.markdown("### Recruiter")

        page = st.radio(
            "Navigation",
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
            ]
        )

    st.divider()

    st.success("System Online")

    st.caption("CareerLens AI")
    st.caption("AI + ML Recruitment Platform")


# ============================================================
# PAGE HEADER
# ============================================================

st.markdown(
    f"""
    <div style="
        color:#6f7d94;
        font-size:13px;
        margin-bottom:10px;
    ">
        {selected_role} Workspace
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# JOB SEEKER DASHBOARD
# ============================================================

if selected_role == "Job Seeker" and page == "Dashboard":

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
                CareerLens AI helps you understand your resume,
                discover suitable opportunities, detect risky
                job postings, identify skill gaps and build a
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
        '<div class="section-description">'
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

    for column, (label, value) in zip(
        [c1, c2, c3, c4],
        metrics
    ):

        with column:

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

    st.markdown(
        '<div class="section-title">Career Intelligence Tools</div>',
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
            "Analyze job descriptions and identify important requirements."
        ),
        (
            "🛡️",
            "Job Fraud Detection",
            "Identify suspicious signals in job opportunities."
        ),
        (
            "🎯",
            "AI Job Matching",
            "Compare your resume against job opportunities."
        ),
        (
            "🧩",
            "Skill Gap Analysis",
            "Discover skills required for your target career."
        ),
        (
            "🗺️",
            "Career Roadmap",
            "Build a personalized path toward your career goal."
        )
    ]

    columns = st.columns(3)

    for index, feature in enumerate(features):

        icon, title, description = feature

        with columns[index % 3]:

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
                        {description}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# RESUME ANALYZER
# ============================================================

elif selected_role == "Job Seeker" and page == "Resume Analyzer":

    st.markdown(
        '<div class="section-title">📄 Resume Analyzer</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Upload your resume for AI-powered analysis.'
        '</div>',
        unsafe_allow_html=True
    )

    resume = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx"],
        key="jobseeker_resume"
    )

    if resume:

        st.success(
            f"Uploaded: {resume.name}"
        )

        if st.button(
            "Analyze Resume",
            use_container_width=True
        ):

            st.info(
                "Resume parsing engine will be connected in the next phase."
            )


# ============================================================
# JOB ANALYZER
# ============================================================

elif selected_role == "Job Seeker" and page == "Job Analyzer":

    st.markdown(
        '<div class="section-title">🔎 Job Analyzer</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Analyze a job opportunity before applying.'
        '</div>',
        unsafe_allow_html=True
    )

    job_url = st.text_input(
        "Job URL",
        placeholder="https://company.com/jobs/example"
    )

    job_description = st.text_area(
        "Job Description",
        height=250,
        placeholder="Paste the job description here..."
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
                "Job analysis engine will be connected in the next phase."
            )


# ============================================================
# FRAUD DETECTION
# ============================================================

elif selected_role == "Job Seeker" and page == "Job Fraud Detection":

    st.markdown(
        '<div class="section-title">🛡️ Job Fraud Detection</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Check whether a job posting contains suspicious signals.'
        '</div>',
        unsafe_allow_html=True
    )

    fraud_text = st.text_area(
        "Paste Job Description",
        height=280,
        placeholder="Paste the complete job posting here..."
    )

    if st.button(
        "Analyze Job Safety",
        use_container_width=True
    ):

        if not fraud_text.strip():

            st.warning(
                "Please enter a job description."
            )

        else:

            st.info(
                "Fraud detection model will be connected in the ML phase."
            )


# ============================================================
# JOB MATCHING
# ============================================================

elif selected_role == "Job Seeker" and page == "Job Matching":

    st.markdown(
        '<div class="section-title">🎯 AI Job Matching</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Find how closely a job matches your profile.'
        '</div>',
        unsafe_allow_html=True
    )

    job_text = st.text_area(
        "Paste Job Description",
        height=280
    )

    if st.button(
        "Calculate Match",
        use_container_width=True
    ):

        if not job_text.strip():

            st.warning(
                "Please enter a job description."
            )

        else:

            st.info(
                "Semantic matching model will be connected in the next phase."
            )


# ============================================================
# SKILL GAP
# ============================================================

elif selected_role == "Job Seeker" and page == "Skill Gap Analysis":

    st.markdown(
        '<div class="section-title">🧩 Skill Gap Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Discover the skills you need to develop.'
        '</div>',
        unsafe_allow_html=True
    )

    st.info(
        "Your current skills and target-job requirements will "
        "be compared by the AI engine."
    )


# ============================================================
# CAREER ROADMAP
# ============================================================

elif selected_role == "Job Seeker" and page == "Career Roadmap":

    st.markdown(
        '<div class="section-title">🗺️ Career Roadmap</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Your personalized journey toward your target career.'
        '</div>',
        unsafe_allow_html=True
    )

    roadmap = [
        ("01", "Analyze Your Profile"),
        ("02", "Choose Target Career"),
        ("03", "Identify Skill Gaps"),
        ("04", "Build Required Skills"),
        ("05", "Complete Practical Projects"),
        ("06", "Prepare for Interviews"),
        ("07", "Apply for Relevant Jobs")
    ]

    for number, title in roadmap:

        st.markdown(
            f"""
            <div class="card">

                <div style="
                    color:#8b7cff;
                    font-weight:700;
                    font-size:13px;
                ">
                    STEP {number}
                </div>

                <div class="card-title">
                    {title}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# APPLICATION TRACKER
# ============================================================

elif selected_role == "Job Seeker" and page == "Application Tracker":

    st.markdown(
        '<div class="section-title">📋 Application Tracker</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Track your job applications.'
        '</div>',
        unsafe_allow_html=True
    )

    st.info(
        "Your applications will appear here once the job application "
        "database is implemented."
    )


# ============================================================
# JOB SEEKER AI ASSISTANT
# ============================================================

elif selected_role == "Job Seeker" and page == "AI Career Assistant":

    st.markdown(
        '<div class="section-title">🤖 AI Career Assistant</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Your personal AI career advisor.'
        '</div>',
        unsafe_allow_html=True
    )

    question = st.chat_input(
        "Ask CareerLens AI about your career..."
    )

    if question:

        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            st.write(
                "The CareerLens AI assistant will be connected "
                "to the LLM engine in a later development phase."
            )


# ============================================================
# RECRUITER DASHBOARD
# ============================================================

elif selected_role == "Recruiter" and page == "Dashboard":

    st.markdown(
        """
        <div class="hero">

            <div class="hero-title">
                Recruit Smarter.
                <br>

                <span class="gradient-text">
                    Hire Better.
                </span>
            </div>

            <div class="hero-description">
                CareerLens AI helps recruiters analyze large
                volumes of resumes, identify the strongest
                candidates and build an intelligent shortlist.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    metrics = [
        ("Active Jobs", "0"),
        ("Total Candidates", "0"),
        ("Shortlisted", "0"),
        ("Interviews", "0")
    ]

    for column, (label, value) in zip(
        [c1, c2, c3, c4],
        metrics
    ):

        with column:

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

    st.markdown(
        '<div class="section-title">Recruitment Intelligence</div>',
        unsafe_allow_html=True
    )

    recruiter_features = [
        (
            "📋",
            "Create Job",
            "Define the role, skills, experience and hiring requirements."
        ),
        (
            "📂",
            "Bulk Resume Upload",
            "Upload large batches of candidate resumes."
        ),
        (
            "🧠",
            "AI Candidate Ranking",
            "Automatically score candidates against your job requirements."
        ),
        (
            "🔍",
            "Smart Filters",
            "Filter candidates by skills, experience, education and score."
        ),
        (
            "⚖️",
            "Candidate Comparison",
            "Compare shortlisted candidates side by side."
        ),
        (
            "📊",
            "Hiring Analytics",
            "Understand your recruitment pipeline and candidate pool."
        )
    ]

    columns = st.columns(3)

    for index, feature in enumerate(recruiter_features):

        icon, title, description = feature

        with columns[index % 3]:

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
                        {description}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# CREATE JOB
# ============================================================

elif selected_role == "Recruiter" and page == "Create Job":

    st.markdown(
        '<div class="section-title">📋 Create Job</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Define the requirements that CareerLens AI will use '
        'to rank candidates.'
        '</div>',
        unsafe_allow_html=True
    )

    job_title = st.text_input(
        "Job Title",
        placeholder="Machine Learning Engineer"
    )

    company = st.text_input(
        "Company Name"
    )

    required_skills = st.text_area(
        "Required Skills",
        placeholder="Python, Machine Learning, SQL, NLP..."
    )

    experience = st.number_input(
        "Minimum Experience (years)",
        min_value=0,
        max_value=30,
        value=0
    )

    job_description = st.text_area(
        "Full Job Description",
        height=250
    )

    if st.button(
        "Save Job",
        use_container_width=True
    ):

        if not job_title:

            st.warning(
                "Job title is required."
            )

        else:

            st.success(
                f"Job '{job_title}' created successfully."
            )


# ============================================================
# BULK RESUME UPLOAD
# ============================================================

elif selected_role == "Recruiter" and page == "Bulk Resume Upload":

    st.markdown(
        '<div class="section-title">📂 Bulk Resume Upload</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Upload multiple resumes. CareerLens AI will parse '
        'and analyze them automatically.'
        '</div>',
        unsafe_allow_html=True
    )

    resumes = st.file_uploader(
        "Upload Candidate Resumes",
        type=["pdf", "docx"],
        accept_multiple_files=True
    )

    if resumes:

        st.success(
            f"{len(resumes)} resume(s) uploaded."
        )

        if st.button(
            "Analyze All Resumes",
            use_container_width=True
        ):

            st.info(
                "Bulk resume parsing engine will be connected next."
            )


# ============================================================
# CANDIDATE RANKING
# ============================================================

elif selected_role == "Recruiter" and page == "Candidate Ranking":

    st.markdown(
        '<div class="section-title">🧠 AI Candidate Ranking</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Choose how many top candidates you want CareerLens AI '
        'to shortlist.'
        '</div>',
        unsafe_allow_html=True
    )

    top_n = st.selectbox(
        "Number of candidates to display",
        [
            5,
            10,
            20,
            30,
            50,
            100
        ]
    )

    minimum_score = st.slider(
        "Minimum Match Score",
        min_value=0,
        max_value=100,
        value=60
    )

    st.info(
        f"AI will return the top {top_n} candidates "
        f"with a minimum match score of {minimum_score}%."
    )

    if st.button(
        "Rank Candidates",
        use_container_width=True
    ):

        st.info(
            "Candidate ranking engine will be connected "
            "after the resume parsing and matching models."
        )


# ============================================================
# CANDIDATE COMPARISON
# ============================================================

elif selected_role == "Recruiter" and page == "Candidate Comparison":

    st.markdown(
        '<div class="section-title">⚖️ Candidate Comparison</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Compare shortlisted candidates side by side.'
        '</div>',
        unsafe_allow_html=True
    )

    st.info(
        "Candidate comparison will become available after "
        "the ranking engine is implemented."
    )


# ============================================================
# SHORTLIST
# ============================================================

elif selected_role == "Recruiter" and page == "Shortlist":

    st.markdown(
        '<div class="section-title">⭐ Shortlisted Candidates</div>',
        unsafe_allow_html=True
    )

    st.info(
        "Candidates selected by the recruiter will appear here."
    )


# ============================================================
# RECRUITMENT PIPELINE
# ============================================================

elif selected_role == "Recruiter" and page == "Recruitment Pipeline":

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

    for column, (stage, count) in zip(columns, stages):

        with column:

            st.markdown(
                f"""
                <div class="metric-card">

                    <div class="metric-label">
                        {stage}
                    </div>

                    <div class="metric-value">
                        {count}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# HIRING ANALYTICS
# ============================================================

elif selected_role == "Recruiter" and page == "Hiring Analytics":

    st.markdown(
        '<div class="section-title">📈 Hiring Analytics</div>',
        unsafe_allow_html=True
    )

    st.info(
        "Recruitment analytics will be populated from the "
        "candidate and hiring database."
    )


# ============================================================
# RECRUITER AI
# ============================================================

elif selected_role == "Recruiter" and page == "AI Recruiter Assistant":

    st.markdown(
        '<div class="section-title">🤖 AI Recruiter Assistant</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
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
                "The AI Recruiter Assistant will be connected "
                "to the candidate database and ranking engine."
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

        🎯 <strong>CareerLens AI</strong>

        <br><br>

        AI-Powered Career Intelligence & Recruitment Platform

        <br>

        Final Year Project • AI • ML • NLP

    </div>
    """,
    unsafe_allow_html=True
)
