import streamlit as st
import textwrap

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CareerLens AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SAFE HTML RENDERER
# ============================================================

def html(content):
    """
    Safely render custom HTML without Markdown indentation
    turning it into a code block.
    """
    st.markdown(
        textwrap.dedent(content).strip(),
        unsafe_allow_html=True
    )


# ============================================================
# SESSION STATE
# ============================================================

if "workspace" not in st.session_state:
    st.session_state.workspace = "Job Seeker"

if "job_seeker_page" not in st.session_state:
    st.session_state.job_seeker_page = "Dashboard"

if "recruiter_page" not in st.session_state:
    st.session_state.recruiter_page = "Dashboard"


# ============================================================
# CUSTOM CSS
# ============================================================

html("""
<style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    .stApp {
        background: #080d18;
        color: #ffffff;
    }

    .main .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background: #0b1220;
        border-right: 1px solid #202c42;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem;
        padding-left: 1.2rem;
        padding-right: 1.2rem;
    }

    /* ========================================================
       BRAND
       ======================================================== */

    .brand-box {
        text-align: center;
        padding: 8px 0 22px 0;
    }

    .brand-icon {
        font-size: 42px;
        line-height: 1;
        margin-bottom: 10px;
    }

    .brand-name {
        color: #ffffff;
        font-size: 24px;
        font-weight: 800;
        letter-spacing: -0.5px;
    }

    .brand-name span {
        color: #8b7cff;
    }

    .brand-subtitle {
        color: #7f8ba3;
        font-size: 11px;
        margin-top: 6px;
    }

    /* ========================================================
       SIDEBAR LABELS
       ======================================================== */

    .sidebar-label {
        color: #7f8ba3;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    /* ========================================================
       HERO
       ======================================================== */

    .hero-box {
        position: relative;
        overflow: hidden;

        background:
            radial-gradient(
                circle at 85% 15%,
                rgba(139,124,255,0.16),
                transparent 35%
            ),
            linear-gradient(
                135deg,
                #121c31 0%,
                #0d1627 100%
            );

        border: 1px solid #263550;
        border-radius: 24px;

        padding: 48px;

        margin-bottom: 35px;

        box-shadow:
            0 20px 60px rgba(0,0,0,0.28);
    }

    .hero-small {
        color: #9b8cff;
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 13px;
    }

    .hero-title {
        color: #ffffff;
        font-size: 48px;
        font-weight: 850;
        line-height: 1.12;
        letter-spacing: -1.5px;
    }

    .hero-gradient {
        background: linear-gradient(
            90deg,
            #9b8cff,
            #38bdf8
        );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .hero-text {
        color: #9aa7bd;
        font-size: 16px;
        line-height: 1.7;
        max-width: 850px;
        margin-top: 18px;
    }

    /* ========================================================
       SECTION TITLES
       ======================================================== */

    .section-title {
        color: #ffffff;
        font-size: 27px;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-top: 25px;
    }

    .section-subtitle {
        color: #8996ac;
        font-size: 14px;
        margin-top: 5px;
        margin-bottom: 22px;
    }

    /* ========================================================
       METRIC CARDS
       ======================================================== */

    .metric-card {
        background: #101929;

        border: 1px solid #243149;
        border-radius: 18px;

        padding: 22px;

        min-height: 115px;

        text-align: left;

        box-shadow:
            0 10px 30px rgba(0,0,0,0.12);
    }

    .metric-title {
        color: #8996ac;
        font-size: 13px;
        font-weight: 600;
    }

    .metric-number {
        color: #ffffff;
        font-size: 31px;
        font-weight: 850;
        margin-top: 6px;
    }

    .metric-change {
        color: #6ee7b7;
        font-size: 11px;
        margin-top: 5px;
    }

    /* ========================================================
       FEATURE CARDS
       ======================================================== */

    .feature-card {
        background:
            linear-gradient(
                145deg,
                #111c2d,
                #0e1726
            );

        border: 1px solid #243149;
        border-radius: 18px;

        padding: 24px;

        min-height: 175px;

        margin-bottom: 18px;

        box-shadow:
            0 10px 30px rgba(0,0,0,0.12);
    }

    .feature-icon {
        font-size: 29px;
        margin-bottom: 12px;
    }

    .feature-title {
        color: #ffffff;
        font-size: 17px;
        font-weight: 750;
        margin-bottom: 8px;
    }

    .feature-description {
        color: #8d9ab0;
        font-size: 13px;
        line-height: 1.6;
    }

    /* ========================================================
       INFO CARDS
       ======================================================== */

    .info-card {
        background: #101929;
        border: 1px solid #243149;
        border-radius: 18px;
        padding: 25px;
        margin-bottom: 20px;
    }

    .info-title {
        color: #ffffff;
        font-size: 19px;
        font-weight: 750;
        margin-bottom: 8px;
    }

    .info-text {
        color: #8996ac;
        font-size: 14px;
        line-height: 1.6;
    }

    /* ========================================================
       STATUS
       ======================================================== */

    .status-box {
        background: #0d2a20;
        border: 1px solid #1c5943;
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        color: #6ee7b7;
        font-size: 12px;
        font-weight: 600;
    }

    /* ========================================================
       BADGES
       ======================================================== */

    .badge {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        background: #1b2740;
        color: #aeb9cc;
        margin-right: 5px;
    }

    /* ========================================================
       FOOTER
       ======================================================== */

    .footer {
        border-top: 1px solid #202c42;
        margin-top: 55px;
        padding-top: 25px;
        padding-bottom: 20px;

        text-align: center;

        color: #66738a;
        font-size: 12px;
        line-height: 1.8;
    }

    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        border-radius: 10px;
        min-height: 42px;
        font-weight: 700;
    }

    /* ========================================================
       FILE UPLOADER
       ======================================================== */

    [data-testid="stFileUploader"] {
        background: #0e1726;
        border-radius: 14px;
    }

    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 768px) {

        .hero-box {
            padding: 30px;
        }

        .hero-title {
            font-size: 34px;
        }

        .hero-text {
            font-size: 14px;
        }
    }

</style>
""")


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    html("""
    <div class="brand-box">
        <div class="brand-icon">🎯</div>

        <div class="brand-name">
            Career<span>Lens</span> AI
        </div>

        <div class="brand-subtitle">
            Career Intelligence Platform
        </div>
    </div>
    """)

    st.divider()

    html("""
    <div class="sidebar-label">
        Workspace
    </div>
    """)

    workspace = st.radio(
        "Workspace",
        ["Job Seeker", "Recruiter"],
        index=(
            0
            if st.session_state.workspace == "Job Seeker"
            else 1
        ),
        label_visibility="collapsed"
    )

    st.session_state.workspace = workspace

    st.divider()

    # --------------------------------------------------------
    # JOB SEEKER NAVIGATION
    # --------------------------------------------------------

    if workspace == "Job Seeker":

        html("""
        <div class="sidebar-label">
            👨‍💻 Job Seeker
        </div>
        """)

        job_seeker_pages = [
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

        job_seeker_page = st.radio(
            "Job Seeker Navigation",
            job_seeker_pages,
            index=job_seeker_pages.index(
                st.session_state.job_seeker_page
            ),
            label_visibility="collapsed"
        )

        st.session_state.job_seeker_page = job_seeker_page

        current_page = job_seeker_page

    # --------------------------------------------------------
    # RECRUITER NAVIGATION
    # --------------------------------------------------------

    else:

        html("""
        <div class="sidebar-label">
            🧑‍💼 Recruiter
        </div>
        """)

        recruiter_pages = [
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

        recruiter_page = st.radio(
            "Recruiter Navigation",
            recruiter_pages,
            index=recruiter_pages.index(
                st.session_state.recruiter_page
            ),
            label_visibility="collapsed"
        )

        st.session_state.recruiter_page = recruiter_page

        current_page = recruiter_page

    st.divider()

    html("""
    <div class="status-box">
        ● System Online
    </div>
    """)

    st.write("")

    html("""
    <div style="text-align:center;">
        <div style="color:#8996ac;font-size:12px;">
            CareerLens AI
        </div>

        <div style="color:#5f6c82;font-size:10px;margin-top:4px;">
            AI • ML • NLP
        </div>
    </div>
    """)


# ============================================================
# JOB SEEKER DASHBOARD
# ============================================================

if workspace == "Job Seeker" and current_page == "Dashboard":

    html("""
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
            job opportunities, detects potential job risks,
            identifies skill gaps and helps you build a
            personalized career roadmap.
        </div>

    </div>
    """)

    html("""
    <div class="section-title">
        Career Overview
    </div>

    <div class="section-subtitle">
        Your career intelligence at a glance.
    </div>
    """)

    c1, c2, c3, c4 = st.columns(4)

    metric_data = [
        ("Resume Score", "—", "Upload a resume"),
        ("Career Readiness", "—", "Complete your profile"),
        ("Job Matches", "0", "No matches yet"),
        ("Applications", "0", "Start applying")
    ]

    for col, (title, number, change) in zip(
        [c1, c2, c3, c4],
        metric_data
    ):

        with col:

            html(f"""
            <div class="metric-card">

                <div class="metric-title">
                    {title}
                </div>

                <div class="metric-number">
                    {number}
                </div>

                <div class="metric-change">
                    {change}
                </div>

            </div>
            """)

    html("""
    <div class="section-title">
        Career Intelligence
    </div>

    <div class="section-subtitle">
        AI-powered tools designed to help you make better
        career decisions.
    </div>
    """)

    features = [
        (
            "📄",
            "Resume Intelligence",
            "Analyze your resume and extract skills, education, "
            "projects and experience."
        ),
        (
            "🔎",
            "Job Intelligence",
            "Understand job descriptions and identify important "
            "requirements."
        ),
        (
            "🛡️",
            "Job Fraud Detection",
            "Identify suspicious signals and potential risks "
            "in job postings."
        ),
        (
            "🎯",
            "AI Job Matching",
            "Measure how closely your profile matches a "
            "specific opportunity."
        ),
        (
            "🧩",
            "Skill Gap Analysis",
            "Discover the skills you need for your target "
            "career."
        ),
        (
            "🗺️",
            "Career Roadmap",
            "Create a personalized learning and career "
            "development path."
        )
    ]

    cols = st.columns(3)

    for index, (icon, title, description) in enumerate(features):

        with cols[index % 3]:

            html(f"""
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
            """)


# ============================================================
# RESUME ANALYZER
# ============================================================

elif workspace == "Job Seeker" and current_page == "Resume Analyzer":

    html("""
    <div class="section-title">
        📄 Resume Analyzer
    </div>

    <div class="section-subtitle">
        Upload your resume and let CareerLens AI analyze
        your professional profile.
    </div>
    """)

    resume = st.file_uploader(
        "Upload your resume",
        type=["pdf", "docx"],
        help="Supported formats: PDF and DOCX"
    )

    if resume:

        st.success(
            f"Resume uploaded successfully: {resume.name}"
        )

        col1, col2 = st.columns(2)

        with col1:

            html("""
            <div class="info-card">

                <div class="info-title">
                    Resume Intelligence
                </div>

                <div class="info-text">
                    The AI engine will extract your skills,
                    education, projects, experience and
                    other important information.
                </div>

            </div>
            """)

        with col2:

            html("""
            <div class="info-card">

                <div class="info-title">
                    Career Score
                </div>

                <div class="info-text">
                    Your resume will receive an AI-powered
                    score based on structure, skills,
                    relevance and completeness.
                </div>

            </div>
            """)

        if st.button(
            "🚀 Analyze Resume",
            use_container_width=True
        ):

            st.info(
                "Resume AI engine will be connected in the "
                "next development phase."
            )


# ============================================================
# JOB ANALYZER
# ============================================================

elif workspace == "Job Seeker" and current_page == "Job Analyzer":

    html("""
    <div class="section-title">
        🔎 Job Analyzer
    </div>

    <div class="section-subtitle">
        Analyze a job opportunity before applying.
    </div>
    """)

    job_url = st.text_input(
        "Job URL",
        placeholder="https://example.com/job"
    )

    job_description = st.text_area(
        "Job Description",
        height=260,
        placeholder="Paste the complete job description here..."
    )

    if st.button(
        "🔍 Analyze Job",
        use_container_width=True
    ):

        if not job_url and not job_description:

            st.warning(
                "Please provide a job URL or job description."
            )

        else:

            st.info(
                "Job intelligence engine will be connected "
                "in the next development phase."
            )


# ============================================================
# JOB FRAUD DETECTION
# ============================================================

elif workspace == "Job Seeker" and current_page == "Job Fraud Detection":

    html("""
    <div class="section-title">
        🛡️ Job Fraud Detection
    </div>

    <div class="section-subtitle">
        Check a job posting for suspicious characteristics
        before you apply.
    </div>
    """)

    job_text = st.text_area(
        "Job Posting",
        height=300,
        placeholder="Paste the job posting here..."
    )

    if st.button(
        "🛡️ Check Job Safety",
        use_container_width=True
    ):

        if not job_text.strip():

            st.warning(
                "Please paste a job posting first."
            )

        else:

            st.info(
                "Fraud detection ML model will be connected "
                "in the next development phase."
            )


# ============================================================
# JOB MATCHING
# ============================================================

elif workspace == "Job Seeker" and current_page == "Job Matching":

    html("""
    <div class="section-title">
        🎯 AI Job Matching
    </div>

    <div class="section-subtitle">
        Compare your resume and skills against a job
        opportunity.
    </div>
    """)

    job_description = st.text_area(
        "Job Description",
        height=300,
        placeholder="Paste job requirements here..."
    )

    if st.button(
        "🎯 Calculate Match",
        use_container_width=True
    ):

        if not job_description.strip():

            st.warning(
                "Please enter a job description."
            )

        else:

            st.info(
                "Semantic job matching model will be "
                "connected in the next development phase."
            )


# ============================================================
# SKILL GAP ANALYSIS
# ============================================================

elif workspace == "Job Seeker" and current_page == "Skill Gap Analysis":

    html("""
    <div class="section-title">
        🧩 Skill Gap Analysis
    </div>

    <div class="section-subtitle">
        Discover what skills you need to reach your target role.
    </div>
    """)

    current_skills = st.text_area(
        "Your Current Skills",
        placeholder="Python, SQL, HTML, Machine Learning..."
    )

    target_skills = st.text_area(
        "Target Job Requirements",
        placeholder="Python, SQL, NLP, Docker, AWS..."
    )

    if st.button(
        "🧩 Analyze Skill Gap",
        use_container_width=True
    ):

        if not current_skills or not target_skills:

            st.warning(
                "Please enter both current skills and target "
                "requirements."
            )

        else:

            st.info(
                "Skill gap analysis model will be connected "
                "in the next development phase."
            )


# ============================================================
# CAREER ROADMAP
# ============================================================

elif workspace == "Job Seeker" and current_page == "Career Roadmap":

    html("""
    <div class="section-title">
        🗺️ Career Roadmap
    </div>

    <div class="section-subtitle">
        Build a personalized path toward your target career.
    </div>
    """)

    target_role = st.text_input(
        "Target Career",
        placeholder="Machine Learning Engineer"
    )

    if st.button(
        "🗺️ Generate Roadmap",
        use_container_width=True
    ):

        if not target_role:

            st.warning(
                "Please enter your target career."
            )

        else:

            steps = [
                (
                    "01",
                    "Build Foundations",
                    "Strengthen programming, mathematics and "
                    "computer science fundamentals."
                ),
                (
                    "02",
                    "Develop Technical Skills",
                    "Learn the technologies and frameworks "
                    "required for your target role."
                ),
                (
                    "03",
                    "Build Projects",
                    "Create real-world projects that demonstrate "
                    "your practical abilities."
                ),
                (
                    "04",
                    "Build Your Portfolio",
                    "Publish projects and organize your GitHub "
                    "and professional profile."
                ),
                (
                    "05",
                    "Prepare for Interviews",
                    "Practice technical, behavioral and "
                    "role-specific interviews."
                ),
                (
                    "06",
                    "Apply Strategically",
                    "Target relevant opportunities based on "
                    "your skills and career goals."
                )
            ]

            for number, title, description in steps:

                html(f"""
                <div class="feature-card">

                    <div class="feature-title">
                        {number} • {title}
                    </div>

                    <div class="feature-description">
                        {description}
                    </div>

                </div>
                """)


# ============================================================
# APPLICATION TRACKER
# ============================================================

elif workspace == "Job Seeker" and current_page == "Application Tracker":

    html("""
    <div class="section-title">
        📋 Application Tracker
    </div>

    <div class="section-subtitle">
        Track your job applications from application to offer.
    </div>
    """)

    html("""
    <div class="info-card">

        <div class="info-title">
            No Applications Yet
        </div>

        <div class="info-text">
            Once you start applying to jobs, your applications,
            interview status and application history will appear
            here.
        </div>

    </div>
    """)


# ============================================================
# AI CAREER ASSISTANT
# ============================================================

elif workspace == "Job Seeker" and current_page == "AI Career Assistant":

    html("""
    <div class="section-title">
        🤖 AI Career Assistant
    </div>

    <div class="section-subtitle">
        Ask questions about careers, skills, resumes and
        job searching.
    </div>
    """)

    question = st.chat_input(
        "Ask CareerLens AI..."
    )

    if question:

        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            st.write(
                "The AI Career Assistant will be connected "
                "to the language model in the AI integration "
                "phase."
            )


# ============================================================
# RECRUITER DASHBOARD
# ============================================================

elif workspace == "Recruiter" and current_page == "Dashboard":

    html("""
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
            Upload hundreds of resumes, analyze candidate
            profiles, compare skills and experience, and
            create an intelligent shortlist using AI.
        </div>

    </div>
    """)

    c1, c2, c3, c4 = st.columns(4)

    recruiter_metrics = [
        ("Active Jobs", "0", "Create your first job"),
        ("Candidates", "0", "Upload resumes"),
        ("Shortlisted", "0", "AI ranking pending"),
        ("Interviews", "0", "No interviews yet")
    ]

    for col, (title, number, change) in zip(
        [c1, c2, c3, c4],
        recruiter_metrics
    ):

        with col:

            html(f"""
            <div class="metric-card">

                <div class="metric-title">
                    {title}
                </div>

                <div class="metric-number">
                    {number}
                </div>

                <div class="metric-change">
                    {change}
                </div>

            </div>
            """)

    html("""
    <div class="section-title">
        Recruitment Intelligence
    </div>

    <div class="section-subtitle">
        Powerful tools for modern AI-assisted recruitment.
    </div>
    """)

    recruiter_features = [
        (
            "📋",
            "Create Job",
            "Define the role, skills, experience and hiring "
            "requirements."
        ),
        (
            "📂",
            "Bulk Resume Upload",
            "Upload 100 or even hundreds of candidate resumes "
            "at once."
        ),
        (
            "🧠",
            "AI Candidate Ranking",
            "Automatically score candidates against the "
            "selected job."
        ),
        (
            "🔍",
            "Smart Filtering",
            "Filter candidates according to skills, "
            "experience and match score."
        ),
        (
            "⚖️",
            "Candidate Comparison",
            "Compare selected candidates side by side."
        ),
        (
            "📊",
            "Hiring Analytics",
            "Understand recruitment performance through "
            "data and visual analytics."
        )
    ]

    cols = st.columns(3)

    for index, (icon, title, description) in enumerate(
        recruiter_features
    ):

        with cols[index % 3]:

            html(f"""
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
            """)


# ============================================================
# CREATE JOB
# ============================================================

elif workspace == "Recruiter" and current_page == "Create Job":

    html("""
    <div class="section-title">
        📋 Create Job
    </div>

    <div class="section-subtitle">
        Define the requirements that the AI candidate ranking
        engine will use.
    </div>
    """)

    job_title = st.text_input(
        "Job Title",
        placeholder="Machine Learning Engineer"
    )

    company = st.text_input(
        "Company",
        placeholder="Company name"
    )

    required_skills = st.text_area(
        "Required Skills",
        placeholder="Python, SQL, Machine Learning, NLP..."
    )

    experience = st.number_input(
        "Minimum Experience",
        min_value=0,
        max_value=30,
        value=0
    )

    job_description = st.text_area(
        "Job Description",
        height=250
    )

    if st.button(
        "📋 Create Job",
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

elif workspace == "Recruiter" and current_page == "Bulk Resume Upload":

    html("""
    <div class="section-title">
        📂 Bulk Resume Upload
    </div>

    <div class="section-subtitle">
        Upload multiple candidate resumes for AI-powered
        processing.
    </div>
    """)

    resumes = st.file_uploader(
        "Candidate Resumes",
        type=["pdf", "docx"],
        accept_multiple_files=True
    )

    if resumes:

        st.success(
            f"{len(resumes)} resume(s) uploaded successfully."
        )

        if st.button(
            "🧠 Analyze All Candidates",
            use_container_width=True
        ):

            st.info(
                "Bulk resume parsing and candidate analysis "
                "will be connected in the next phase."
            )


# ============================================================
# CANDIDATE RANKING
# ============================================================

elif workspace == "Recruiter" and current_page == "Candidate Ranking":

    html("""
    <div class="section-title">
        🧠 AI Candidate Ranking
    </div>

    <div class="section-subtitle">
        Recruiter-controlled ranking — choose exactly how
        many candidates you want to shortlist.
    </div>
    """)

    top_n = st.selectbox(
        "How many candidates do you want?",
        [
            5,
            10,
            20,
            30,
            50,
            100
        ],
        index=2
    )

    min_score = st.slider(
        "Minimum AI Match Score",
        min_value=0,
        max_value=100,
        value=60
    )

    col1, col2 = st.columns(2)

    with col1:

        html(f"""
        <div class="info-card">

            <div class="info-title">
                Selection
            </div>

            <div class="info-text">
                Top <b>{top_n}</b> candidates
                will be displayed.
            </div>

        </div>
        """)

    with col2:

        html(f"""
        <div class="info-card">

            <div class="info-title">
                Match Threshold
            </div>

            <div class="info-text">
                Candidates below <b>{min_score}%</b>
                can be excluded.
            </div>

        </div>
        """)

    if st.button(
        "🚀 Rank Candidates",
        use_container_width=True
    ):

        st.info(
            f"AI will rank the candidate pool and return "
            f"the Top {top_n} candidates."
        )


# ============================================================
# CANDIDATE COMPARISON
# ============================================================

elif workspace == "Recruiter" and current_page == "Candidate Comparison":

    html("""
    <div class="section-title">
        ⚖️ Candidate Comparison
    </div>

    <div class="section-subtitle">
        Compare shortlisted candidates before making a
        recruitment decision.
    </div>
    """)

    html("""
    <div class="info-card">

        <div class="info-title">
            Candidate Comparison
        </div>

        <div class="info-text">
            AI-ranked candidates will appear here with their
            skills, experience, education, match score and
            strengths.
        </div>

    </div>
    """)


# ============================================================
# SHORTLIST
# ============================================================

elif workspace == "Recruiter" and current_page == "Shortlist":

    html("""
    <div class="section-title">
        ⭐ Shortlisted Candidates
    </div>

    <div class="section-subtitle">
        Manage candidates selected for the next stage.
    </div>
    """)

    html("""
    <div class="info-card">

        <div class="info-title">
            Shortlist
        </div>

        <div class="info-text">
            Candidates selected from the AI ranking system
            will appear here.
        </div>

    </div>
    """)


# ============================================================
# RECRUITMENT PIPELINE
# ============================================================

elif workspace == "Recruiter" and current_page == "Recruitment Pipeline":

    html("""
    <div class="section-title">
        📊 Recruitment Pipeline
    </div>

    <div class="section-subtitle">
        Track candidates through the recruitment process.
    </div>
    """)

    pipeline = st.columns(4)

    stages = [
        ("Applied", "0"),
        ("Shortlisted", "0"),
        ("Interview", "0"),
        ("Selected", "0")
    ]

    for col, (stage, count) in zip(
        pipeline,
        stages
    ):

        with col:

            html(f"""
            <div class="metric-card">

                <div class="metric-title">
                    {stage}
                </div>

                <div class="metric-number">
                    {count}
                </div>

            </div>
            """)


# ============================================================
# HIRING ANALYTICS
# ============================================================

elif workspace == "Recruiter" and current_page == "Hiring Analytics":

    html("""
    <div class="section-title">
        📈 Hiring Analytics
    </div>

    <div class="section-subtitle">
        Recruitment insights and performance metrics.
    </div>
    """)

    html("""
    <div class="info-card">

        <div class="info-title">
            Analytics Dashboard
        </div>

        <div class="info-text">
            Once candidate and recruitment data is connected,
            this dashboard will display hiring trends,
            candidate quality, shortlist rates and
            recruitment performance.
        </div>

    </div>
    """)


# ============================================================
# AI RECRUITER ASSISTANT
# ============================================================

elif workspace == "Recruiter" and current_page == "AI Recruiter Assistant":

    html("""
    <div class="section-title">
        🤖 AI Recruiter Assistant
    </div>

    <div class="section-subtitle">
        Ask questions about your candidate pool and
        recruitment process.
    </div>
    """)

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

html("""
<div class="footer">

    🎯 <b>CareerLens AI</b>
    <br><br>

    AI-Powered Career Intelligence & Recruitment Platform
    <br>

    Final Year Project • AI • ML • NLP

</div>
""")
