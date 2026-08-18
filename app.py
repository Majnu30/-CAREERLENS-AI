import streamlit as st

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="CareerLens AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# CSS ONLY
# =========================================================

st.markdown(
    """
    <style>

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    .stApp {
        background-color: #080c16;
    }

    section[data-testid="stSidebar"] {
        background-color: #0c1220;
        border-right: 1px solid #1d2940;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* Buttons */

    .stButton > button {
        border-radius: 10px;
        border: 1px solid #293752;
        background-color: #111a2b;
        color: #ffffff;
        font-weight: 600;
    }

    .stButton > button:hover {
        border-color: #7c6cff;
        color: #ffffff;
    }

    /* Metrics */

    div[data-testid="stMetric"] {
        background-color: #101827;
        border: 1px solid #1e2d45;
        border-radius: 14px;
        padding: 18px;
    }

    div[data-testid="stMetricLabel"] {
        color: #8291a9;
    }

    div[data-testid="stMetricValue"] {
        color: #ffffff;
    }

    /* File uploader */

    section[data-testid="stFileUploaderDropzone"] {
        background-color: #0e1726;
        border: 1px dashed #344766;
        border-radius: 14px;
    }

    /* Inputs */

    .stTextInput input,
    .stTextArea textarea {
        background-color: #0e1726;
        color: white;
        border: 1px solid #293752;
        border-radius: 10px;
    }

    /* Cards */

    .feature-card {
        background-color: #101827;
        border: 1px solid #1e2d45;
        border-radius: 14px;
        padding: 20px;
        min-height: 170px;
    }

    .feature-card:hover {
        border-color: #405579;
    }

    .hero-card {
        background-color: #101827;
        border: 1px solid #253654;
        border-radius: 20px;
        padding: 40px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🎯 CareerLens AI")

    st.caption("Career Intelligence Platform")

    st.divider()

    st.caption("WORKSPACE")

    workspace = st.radio(
        "Choose workspace",
        [
            "👨‍💻 Job Seeker",
            "🏢 Recruiter",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    st.success("AI ENGINE ONLINE")

    st.caption("AI • ML • NLP")


# =========================================================
# JOB SEEKER
# =========================================================

if workspace == "👨‍💻 Job Seeker":

    st.markdown(
        '<div class="hero-card">',
        unsafe_allow_html=True,
    )

    st.caption("AI CAREER INTELLIGENCE")

    st.title("Understand Your Career.")

    st.header("Build Your Future.")

    st.write(
        """
        CareerLens AI brings resume intelligence,
        job matching, fraud-risk analysis,
        skill-gap detection and career planning
        into one professional workspace.
        """
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )

    st.divider()

    st.subheader("Career Overview")

    st.caption(
        "Your career intelligence at a glance."
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Resume Score",
            "—",
            "AI resume analysis",
        )

    with col2:
        st.metric(
            "Career Readiness",
            "—",
            "Profile readiness",
        )

    with col3:
        st.metric(
            "Skills Detected",
            "0",
            "Extracted from resume",
        )

    with col4:
        st.metric(
            "Applications",
            "0",
            "Tracked applications",
        )

    st.divider()

    st.subheader("Career Intelligence")

    st.caption(
        "AI-powered tools for smarter career decisions."
    )

    # -----------------------------------------------------
    # ROW 1
    # -----------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            '<div class="feature-card">',
            unsafe_allow_html=True,
        )

        st.markdown("### 📄 Resume Intelligence")

        st.write(
            "Analyze your resume and extract "
            "skills, education, projects and experience."
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            '<div class="feature-card">',
            unsafe_allow_html=True,
        )

        st.markdown("### 🎯 AI Job Matching")

        st.write(
            "Measure how closely your profile "
            "matches a specific opportunity."
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )

    with col3:

        st.markdown(
            '<div class="feature-card">',
            unsafe_allow_html=True,
        )

        st.markdown("### 🛡️ Job Fraud Detection")

        st.write(
            "Identify suspicious payment, "
            "financial, urgency and communication signals."
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )

    st.write("")

    # -----------------------------------------------------
    # ROW 2
    # -----------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            '<div class="feature-card">',
            unsafe_allow_html=True,
        )

        st.markdown("### 🧩 Skill Gap Analysis")

        st.write(
            "Discover the skills you need "
            "for your target career."
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            '<div class="feature-card">',
            unsafe_allow_html=True,
        )

        st.markdown("### 🔎 Job Intelligence")

        st.write(
            "Understand job requirements "
            "and identify important skills."
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )

    with col3:

        st.markdown(
            '<div class="feature-card">',
            unsafe_allow_html=True,
        )

        st.markdown("### 🗺️ Career Roadmap")

        st.write(
            "Create a structured path "
            "toward your target career."
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )

    st.divider()

    st.caption(
        "🎯 CareerLens AI  •  "
        "AI-Powered Career Intelligence & Recruitment Platform"
    )

    st.caption(
        "Final Year Project • AI • ML • NLP"
    )


# =========================================================
# RECRUITER
# =========================================================

else:

    st.markdown(
        '<div class="hero-card">',
        unsafe_allow_html=True,
    )

    st.caption("AI RECRUITMENT INTELLIGENCE")

    st.title("Screen Smarter.")

    st.header("Hire Better.")

    st.write(
        """
        CareerLens AI helps recruiters analyze large
        resume pools, compare candidates against job
        requirements and create an intelligent shortlist.
        """
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )

    st.divider()

    st.subheader("Recruiter Overview")

    st.caption(
        "Your recruitment intelligence at a glance."
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Resumes Screened",
            "0",
        )

    with col2:
        st.metric(
            "Candidates Ranked",
            "0",
        )

    with col3:
        st.metric(
            "Shortlisted",
            "0",
        )

    with col4:
        st.metric(
            "Average Match",
            "—",
        )

    st.divider()

    st.subheader("Recruitment Intelligence")

    st.caption(
        "Professional tools for high-volume recruitment."
    )

    # -----------------------------------------------------
    # RECRUITER ROW 1
    # -----------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            '<div class="feature-card">',
            unsafe_allow_html=True,
        )

        st.markdown("### 📂 Bulk Resume Screening")

        st.write(
            "Upload a large collection of resumes "
            "and process them together."
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            '<div class="feature-card">',
            unsafe_allow_html=True,
        )

        st.markdown("### 🧠 AI Candidate Ranking")

        st.write(
            "Rank candidates using skills, "
            "experience and NLP similarity."
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )

    with col3:

        st.markdown(
            '<div class="feature-card">',
            unsafe_allow_html=True,
        )

        st.markdown("### 🎯 Top-N Shortlisting")

        st.write(
            "Recruiters decide whether they want "
            "the top 5, 10, 20, 50 or more candidates."
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )

    st.write("")

    # -----------------------------------------------------
    # RECRUITER ROW 2
    # -----------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            '<div class="feature-card">',
            unsafe_allow_html=True,
        )

        st.markdown("### 📊 Candidate Comparison")

        st.write(
            "Compare candidates using "
            "consistent evaluation criteria."
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            '<div class="feature-card">',
            unsafe_allow_html=True,
        )

        st.markdown("### 🔍 Skill Intelligence")

        st.write(
            "See matched and missing skills "
            "for every candidate."
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )

    with col3:

        st.markdown(
            '<div class="feature-card">',
            unsafe_allow_html=True,
        )

        st.markdown("### ⬇️ Shortlist Export")

        st.write(
            "Export the final candidate "
            "shortlist as CSV."
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )

    st.divider()

    st.caption(
        "🎯 CareerLens AI  •  "
        "AI-Powered Recruitment Intelligence"
    )

    st.caption(
        "Final Year Project • AI • ML • NLP"
    )
