import streamlit as st

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="CareerLens AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# PROFESSIONAL THEME
# ---------------------------------------------------------

st.markdown("""
<style>

@import url(
    'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
);

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #070b14;
    color: #f5f7fb;
}

/* Remove Streamlit branding */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

/* Main container */
.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background: #0a101c;
    border-right: 1px solid #1b2940;
}

section[data-testid="stSidebar"] > div {
    padding: 1.5rem 1rem;
}

/* Sidebar text */

section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label {
    color: #aab8ce !important;
}

/* Radio */

div[data-testid="stRadio"] > div {
    gap: 8px;
}

div[data-testid="stRadio"] label {
    background: transparent;
    border-radius: 10px;
    padding: 8px 10px;
}

div[data-testid="stRadio"] label:hover {
    background: #111c2e;
}

/* Buttons */

.stButton > button {
    width: 100%;
    min-height: 42px;
    border-radius: 10px;
    border: 1px solid #293b57;
    background: #101a2b;
    color: #eaf0fa;
    font-weight: 600;
}

.stButton > button:hover {
    border-color: #6d63ff;
    color: white;
}

/* Primary button */

.stButton > button[kind="primary"] {
    background: linear-gradient(
        135deg,
        #7165ff,
        #27a9e8
    );
    border: none;
}

/* Cards */

.card {
    background: #0d1625;
    border: 1px solid #1d2c43;
    border-radius: 16px;
    padding: 22px;
    height: 100%;
}

.card:hover {
    border-color: #334b70;
}

.card-icon {
    font-size: 28px;
    margin-bottom: 14px;
}

.card-title {
    font-size: 16px;
    font-weight: 700;
    color: #f1f5fc;
    margin-bottom: 8px;
}

.card-text {
    color: #8192aa;
    font-size: 13px;
    line-height: 1.6;
}

/* Hero */

.hero {
    background:
        radial-gradient(
            circle at 90% 20%,
            rgba(50,170,235,.12),
            transparent 30%
        ),
        radial-gradient(
            circle at 10% 80%,
            rgba(113,101,255,.12),
            transparent 30%
        ),
        #0d1625;

    border: 1px solid #20324d;
    border-radius: 22px;
    padding: 42px;
    margin-bottom: 30px;
}

.hero-label {
    color: #7f8cff;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 12px;
}

.hero-title {
    font-size: 52px;
    line-height: 1.05;
    font-weight: 800;
    letter-spacing: -2px;
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
    max-width: 720px;
    margin-top: 18px;
    color: #899ab2;
    line-height: 1.7;
    font-size: 15px;
}

/* Section */

.section-title {
    font-size: 25px;
    font-weight: 800;
    margin-top: 28px;
    margin-bottom: 4px;
}

.section-subtitle {
    color: #71839e;
    margin-bottom: 20px;
}

/* Brand */

.brand {
    text-align: center;
    padding: 5px 0 18px;
}

.logo {
    width: 58px;
    height: 58px;
    margin: auto;
    border-radius: 18px;

    background: linear-gradient(
        135deg,
        #7165ff,
        #25a9e8
    );

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 27px;
    font-weight: 800;

    box-shadow:
        0 10px 30px rgba(85,90,255,.25);
}

.brand-name {
    margin-top: 12px;
    font-size: 22px;
    font-weight: 800;
}

.brand-name span {
    color: #6f8cff;
}

.brand-subtitle {
    color: #687b98;
    font-size: 11px;
    margin-top: 3px;
}

/* Status */

.status {
    margin-top: 15px;
    padding: 8px 10px;
    text-align: center;

    background: rgba(34,197,94,.07);
    border: 1px solid rgba(34,197,94,.18);

    color: #69db91;
    border-radius: 9px;

    font-size: 11px;
    font-weight: 700;
}

/* Metric */

.metric {
    background: #0d1625;
    border: 1px solid #1d2c43;
    border-radius: 15px;
    padding: 20px;
}

.metric-label {
    color: #71839d;
    font-size: 12px;
}

.metric-value {
    font-size: 30px;
    font-weight: 800;
    margin-top: 8px;
}

.metric-description {
    color: #5f718b;
    font-size: 11px;
    margin-top: 5px;
}

/* Footer */

.footer {
    text-align: center;
    color: #536680;
    font-size: 11px;
    padding: 40px 0 10px;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# SIDEBAR BRAND
# ---------------------------------------------------------

with st.sidebar:

    st.markdown("""
    <div class="brand">

        <div class="logo">
            🎯
        </div>

        <div class="brand-name">
            Career<span>Lens</span> AI
        </div>

        <div class="brand-subtitle">
            Career Intelligence Platform
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.caption("WORKSPACE")

    workspace = st.radio(
        "Select workspace",
        [
            "👨‍💻 Job Seeker",
            "🏢 Recruiter"
        ],
        label_visibility="collapsed"
    )

    st.markdown("""
    <div class="status">
        ● AI ENGINE ONLINE
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------
# JOB SEEKER
# ---------------------------------------------------------

if workspace == "👨‍💻 Job Seeker":

    st.markdown("""
    <div class="hero">

        <div class="hero-label">
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
            CareerLens AI brings resume intelligence,
            job matching, fraud-risk analysis,
            skill-gap detection and career planning
            into one professional workspace.
        </div>

    </div>
    """, unsafe_allow_html=True)

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
        st.markdown("""
        <div class="metric">
            <div class="metric-label">
                RESUME SCORE
            </div>
            <div class="metric-value">
                —
            </div>
            <div class="metric-description">
                AI resume analysis
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="metric">
            <div class="metric-label">
                CAREER READINESS
            </div>
            <div class="metric-value">
                —
            </div>
            <div class="metric-description">
                Profile readiness
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="metric">
            <div class="metric-label">
                SKILLS DETECTED
            </div>
            <div class="metric-value">
                0
            </div>
            <div class="metric-description">
                Extracted from resume
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="metric">
            <div class="metric-label">
                APPLICATIONS
            </div>
            <div class="metric-value">
                0
            </div>
            <div class="metric-description">
                Tracked applications
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">Career Intelligence</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'AI-powered tools for smarter career decisions.'
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
            "🎯",
            "AI Job Matching",
            "Measure how closely your profile matches a specific opportunity."
        ),
        (
            "🛡️",
            "Job Fraud Detection",
            "Identify suspicious payment, financial, urgency and communication signals."
        ),
        (
            "🧩",
            "Skill Gap Analysis",
            "Discover the skills you need for your target career."
        ),
        (
            "🔎",
            "Job Intelligence",
            "Understand job requirements and identify important skills."
        ),
        (
            "🗺️",
            "Career Roadmap",
            "Create a structured path toward your target career."
        )
    ]

    rows = [
        features[:3],
        features[3:]
    ]

    for row in rows:

        cols = st.columns(3)

        for col, feature in zip(cols, row):

            icon, title, description = feature

            with col:

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

    st.markdown("""
    <div class="footer">
        🎯 CareerLens AI
        <br>
        AI-Powered Career Intelligence & Recruitment Platform
        <br>
        Final Year Project · AI · ML · NLP
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------
# RECRUITER
# ---------------------------------------------------------

else:

    st.markdown("""
    <div class="hero">

        <div class="hero-label">
            AI Recruitment Intelligence
        </div>

        <div class="hero-title">
            Screen Smarter.
            <br>
            <span class="hero-gradient">
                Hire Better.
            </span>
        </div>

        <div class="hero-text">
            CareerLens AI helps recruiters analyze large
            resume pools, compare candidates against job
            requirements and create an intelligent shortlist.
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">Recruiter Overview</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Your recruitment intelligence workspace.'
        '</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("RESUMES SCREENED", "0")

    with c2:
        st.metric("CANDIDATES RANKED", "0")

    with c3:
        st.metric("SHORTLISTED", "0")

    with c4:
        st.metric("AVG. MATCH", "—")

    st.markdown(
        '<div class="section-title">Recruitment Intelligence</div>',
        unsafe_allow_html=True
    )

    features = [
        (
            "📂",
            "Bulk Resume Screening",
            "Upload a large batch of resumes and process them together."
        ),
        (
            "🧠",
            "AI Candidate Ranking",
            "Rank candidates using skills, experience and NLP similarity."
        ),
        (
            "🎯",
            "Top-N Shortlisting",
            "Recruiters decide whether they want the top 5, 10, 20, 50 or more."
        ),
        (
            "📊",
            "Candidate Comparison",
            "Compare candidates using consistent scoring criteria."
        ),
        (
            "🔍",
            "Skill Intelligence",
            "See matched and missing skills for every candidate."
        ),
        (
            "⬇️",
            "Shortlist Export",
            "Export the final candidate shortlist as CSV."
        )
    ]

    rows = [
        features[:3],
        features[3:]
    ]

    for row in rows:

        cols = st.columns(3)

        for col, feature in zip(cols, row):

            icon, title, description = feature

            with col:

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

    st.markdown("""
    <div class="footer">
        🎯 CareerLens AI
        <br>
        AI-Powered Recruitment Intelligence
        <br>
        Final Year Project · AI · ML · NLP
    </div>
    """, unsafe_allow_html=True)
