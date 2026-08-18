# ============================================================
# CareerLens AI
# AI-Powered Career Intelligence & Recruitment Platform
# Final Year Project
# ============================================================

import io
import re
import html
from typing import List, Dict, Tuple

import numpy as np
import pandas as pd
import streamlit as st

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from pypdf import PdfReader
from docx import Document


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CareerLens AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 15% 10%, rgba(99,102,241,0.12), transparent 30%),
        radial-gradient(circle at 85% 15%, rgba(14,165,233,0.10), transparent 30%),
        #070b14;
    color: #e8eefc;
}

/* Remove Streamlit top padding */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #0b1220 0%,
            #080e19 100%
        );
    border-right: 1px solid #1d2a42;
}

section[data-testid="stSidebar"] > div {
    padding-top: 1.5rem;
}

/* Sidebar radio */
div[data-testid="stRadio"] label {
    color: #aebbd2 !important;
    font-weight: 500;
}

div[data-testid="stRadio"] label:hover {
    color: #ffffff !important;
}

/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 10px;
    border: 1px solid #2a3a59;
    background: linear-gradient(135deg, #17243b, #101a2d);
    color: #eaf1ff;
    font-weight: 600;
    min-height: 42px;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    border-color: #7c6cff;
    color: white;
    transform: translateY(-1px);
}

/* Primary buttons */
button[kind="primary"] {
    background: linear-gradient(
        135deg,
        #6d5dfc,
        #2ea9e8
    ) !important;
    border: none !important;
}

/* Inputs */
.stTextInput input,
.stTextArea textarea,
.stSelectbox div,
.stMultiSelect div {
    background-color: #0d1626 !important;
    color: #edf4ff !important;
    border-color: #263754 !important;
}

/* File uploader */
section[data-testid="stFileUploaderDropzone"] {
    background: #0c1525;
    border: 1px dashed #344a70;
    border-radius: 14px;
}

/* Metrics */
div[data-testid="stMetric"] {
    background: linear-gradient(
        145deg,
        rgba(19,31,51,0.96),
        rgba(12,20,34,0.96)
    );
    border: 1px solid #233451;
    padding: 18px;
    border-radius: 16px;
}

div[data-testid="stMetricLabel"] {
    color: #91a3c2 !important;
}

div[data-testid="stMetricValue"] {
    color: #f4f7ff !important;
}

/* Dataframes */
div[data-testid="stDataFrame"] {
    border: 1px solid #22334f;
    border-radius: 12px;
    overflow: hidden;
}

/* Divider */
hr {
    border-color: #1e2d46 !important;
}

/* Custom cards */

.cl-card {
    background:
        linear-gradient(
            145deg,
            rgba(17,28,48,0.96),
            rgba(10,18,31,0.96)
        );
    border: 1px solid #223452;
    border-radius: 18px;
    padding: 24px;
    margin-bottom: 18px;
    box-shadow: 0 12px 35px rgba(0,0,0,0.18);
}

.cl-card:hover {
    border-color: #344d77;
}

.cl-small-card {
    background: rgba(14,24,41,0.92);
    border: 1px solid #21334f;
    border-radius: 15px;
    padding: 20px;
    min-height: 150px;
}

.logo-box {
    width: 56px;
    height: 56px;
    border-radius: 17px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #101c30;
    border: 1px solid #293b5c;
    margin-bottom: 14px;
}

.brand-name {
    font-size: 24px;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.5px;
}

.brand-name span {
    background: linear-gradient(90deg, #8b7cff, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.brand-subtitle {
    color: #7284a3;
    font-size: 12px;
    margin-top: 4px;
}

.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 7px 11px;
    border-radius: 100px;
    background: rgba(34,197,94,0.08);
    border: 1px solid rgba(34,197,94,0.20);
    color: #67e59a;
    font-size: 12px;
    font-weight: 700;
}

.hero {
    padding: 38px;
    border-radius: 24px;
    border: 1px solid #263957;
    background:
        radial-gradient(
            circle at 90% 10%,
            rgba(56,189,248,0.12),
            transparent 30%
        ),
        radial-gradient(
            circle at 10% 90%,
            rgba(139,124,255,0.13),
            transparent 30%
        ),
        linear-gradient(
            145deg,
            #101a2c,
            #0a1322
        );
    margin-bottom: 28px;
}

.hero-kicker {
    color: #7fa8ff;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 13px;
}

.hero-title {
    font-size: clamp(36px, 5vw, 68px);
    line-height: 1.04;
    font-weight: 800;
    letter-spacing: -2.8px;
    color: #f7faff;
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

.hero-description {
    max-width: 760px;
    color: #93a5c3;
    font-size: 16px;
    line-height: 1.7;
    margin-top: 20px;
}

.section-title {
    font-size: 27px;
    font-weight: 800;
    color: #f4f7ff;
    margin-top: 20px;
}

.section-subtitle {
    color: #7385a4;
    margin-top: 4px;
    margin-bottom: 20px;
}

.feature-icon {
    font-size: 28px;
    margin-bottom: 12px;
}

.feature-title {
    color: #eef4ff;
    font-size: 17px;
    font-weight: 700;
}

.feature-description {
    color: #7588a7;
    font-size: 13px;
    line-height: 1.6;
    margin-top: 8px;
}

.score-ring {
    font-size: 38px;
    font-weight: 800;
    color: #8b7cff;
}

.tag {
    display: inline-block;
    padding: 5px 9px;
    margin: 3px;
    border-radius: 8px;
    background: #17243a;
    border: 1px solid #2b405f;
    color: #a9baff;
    font-size: 12px;
}

.success-box {
    background: rgba(34,197,94,0.07);
    border: 1px solid rgba(34,197,94,0.20);
    border-radius: 12px;
    padding: 15px;
    color: #8ce9ae;
}

.warning-box {
    background: rgba(245,158,11,0.07);
    border: 1px solid rgba(245,158,11,0.20);
    border-radius: 12px;
    padding: 15px;
    color: #ffd27c;
}

.danger-box {
    background: rgba(239,68,68,0.07);
    border: 1px solid rgba(239,68,68,0.20);
    border-radius: 12px;
    padding: 15px;
    color: #ff9a9a;
}

.info-box {
    background: rgba(56,189,248,0.07);
    border: 1px solid rgba(56,189,248,0.20);
    border-radius: 12px;
    padding: 15px;
    color: #8bdcff;
}

.rank-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 34px;
    height: 34px;
    border-radius: 50%;
    background: linear-gradient(135deg,#6d5dfc,#2ea9e8);
    color: white;
    font-weight: 800;
}

.mini-label {
    color: #6f82a1;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: .8px;
}

.mini-value {
    color: #edf3ff;
    font-size: 20px;
    font-weight: 700;
    margin-top: 4px;
}

.footer {
    text-align: center;
    color: #566984;
    font-size: 12px;
    padding: 30px 0 10px 0;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "resume_analysis" not in st.session_state:
    st.session_state.resume_analysis = None

if "applications" not in st.session_state:
    st.session_state.applications = []

if "job_matches" not in st.session_state:
    st.session_state.job_matches = []

if "recruiter_results" not in st.session_state:
    st.session_state.recruiter_results = None


# ============================================================
# CAREER SKILLS DATABASE
# ============================================================

SKILLS = [
    "python",
    "java",
    "javascript",
    "typescript",
    "c++",
    "c",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "html",
    "css",
    "react",
    "angular",
    "node.js",
    "express",
    "fastapi",
    "flask",
    "django",
    "streamlit",
    "git",
    "github",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "linux",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "natural language processing",
    "nlp",
    "computer vision",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",
    "power bi",
    "tableau",
    "excel",
    "data analysis",
    "data science",
    "statistics",
    "communication",
    "leadership",
    "problem solving",
    "teamwork",
    "agile",
    "scrum",
    "rest api",
    "api",
    "firebase",
    "figma",
    "ui/ux",
    "cybersecurity",
    "ethical hacking",
    "networking",
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clean_text(text: str) -> str:
    """Normalize text for NLP processing."""
    if not text:
        return ""

    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s\+\#\.\-/]", " ", text)
    return text.strip()


def safe_text(text: str) -> str:
    """Escape text before putting it inside custom HTML."""
    return html.escape(str(text))


def extract_text_from_pdf(uploaded_file) -> str:
    """Extract text from PDF."""
    try:
        reader = PdfReader(uploaded_file)
        pages = []

        for page in reader.pages:
            page_text = page.extract_text() or ""
            pages.append(page_text)

        return "\n".join(pages)

    except Exception as e:
        return f"ERROR: Could not read PDF: {e}"


def extract_text_from_docx(uploaded_file) -> str:
    """Extract text from DOCX."""
    try:
        data = uploaded_file.read()
        document = Document(io.BytesIO(data))

        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        return "\n".join(paragraphs)

    except Exception as e:
        return f"ERROR: Could not read DOCX: {e}"


def extract_text_from_upload(uploaded_file) -> str:
    """Extract text from supported file."""
    if uploaded_file is None:
        return ""

    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)

    if filename.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)

    if filename.endswith(".txt"):
        try:
            return uploaded_file.read().decode("utf-8", errors="ignore")
        except Exception:
            return ""

    return ""


def extract_skills(text: str) -> List[str]:
    """Extract known skills from text."""
    normalized = clean_text(text)

    found = []

    for skill in SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"

        if re.search(pattern, normalized):
            found.append(skill)

    return sorted(set(found))


def calculate_resume_score(text: str, skills: List[str]) -> int:
    """Simple explainable resume scoring engine."""

    if not text.strip():
        return 0

    score = 0
    normalized = clean_text(text)

    # Skill component
    score += min(len(skills) * 4, 40)

    # Resume sections
    sections = {
        "education": 8,
        "experience": 12,
        "projects": 10,
        "skills": 8,
        "certification": 5,
        "contact": 5,
        "summary": 4,
    }

    for section, points in sections.items():
        if section in normalized:
            score += points

    # Length quality
    words = len(normalized.split())

    if words >= 250:
        score += 5

    if words >= 500:
        score += 5

    return int(min(score, 100))


def calculate_readiness(score: int, skills: List[str]) -> str:
    if score >= 80 and len(skills) >= 10:
        return "Excellent"

    if score >= 65 and len(skills) >= 7:
        return "Strong"

    if score >= 50:
        return "Developing"

    return "Needs Improvement"


def semantic_similarity(text_a: str, text_b: str) -> float:
    """
    NLP matching engine using TF-IDF + cosine similarity.
    This is lightweight and deployment friendly.
    """

    text_a = clean_text(text_a)
    text_b = clean_text(text_b)

    if not text_a or not text_b:
        return 0.0

    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=5000,
        )

        matrix = vectorizer.fit_transform([text_a, text_b])

        score = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]

        return float(score)

    except Exception:
        return 0.0


def calculate_job_match(
    resume_text: str,
    job_text: str
) -> Tuple[float, List[str], List[str]]:
    """Calculate job compatibility."""

    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_text))

    if job_skills:
        matched = resume_skills.intersection(job_skills)
        missing = job_skills.difference(resume_skills)

        skill_score = len(matched) / len(job_skills)
    else:
        matched = set()
        missing = set()
        skill_score = 0.0

    text_score = semantic_similarity(
        resume_text,
        job_text
    )

    final_score = (
        (skill_score * 0.65) +
        (text_score * 0.35)
    ) * 100

    return (
        round(final_score, 1),
        sorted(matched),
        sorted(missing),
    )


# ============================================================
# FRAUD DETECTION ENGINE
# ============================================================

FRAUD_PATTERNS = {
    "payment_request": [
        "pay registration fee",
        "pay a fee",
        "registration fee",
        "processing fee",
        "security deposit",
        "pay money",
        "send money",
        "make a payment",
    ],

    "financial_request": [
        "bank account",
        "credit card",
        "debit card",
        "otp",
        "one time password",
        "upi payment",
        "wallet transfer",
    ],

    "urgency": [
        "act immediately",
        "urgent",
        "limited seats",
        "within 24 hours",
        "immediately",
        "last chance",
    ],

    "unrealistic_salary": [
        "earn $10000",
        "earn $20000",
        "guaranteed income",
        "guaranteed salary",
        "easy money",
        "make money fast",
    ],

    "suspicious_communication": [
        "telegram",
        "whatsapp only",
        "contact via whatsapp",
        "contact via telegram",
        "send your documents",
    ],
}


def detect_job_fraud(job_text: str) -> Dict:
    """
    Explainable fraud-risk engine.
    This is a prototype risk classifier, not a legal/factual
    determination that a job is fraudulent.
    """

    text = clean_text(job_text)

    score = 0
    signals = []

    weights = {
        "payment_request": 30,
        "financial_request": 25,
        "urgency": 15,
        "unrealistic_salary": 20,
        "suspicious_communication": 15,
    }

    for category, patterns in FRAUD_PATTERNS.items():

        found = []

        for pattern in patterns:
            if pattern in text:
                found.append(pattern)

        if found:
            score += weights[category]

            signals.append(
                {
                    "category": category.replace("_", " ").title(),
                    "matches": found,
                }
            )

    score = min(score, 100)

    if score >= 60:
        level = "High Risk"

    elif score >= 30:
        level = "Medium Risk"

    else:
        level = "Low Risk"

    return {
        "score": score,
        "level": level,
        "signals": signals,
    }


# ============================================================
# RECRUITER AI ENGINE
# ============================================================

def candidate_score(
    resume_text: str,
    job_description: str
) -> Dict:

    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_description))

    matched = resume_skills.intersection(job_skills)
    missing = job_skills.difference(resume_skills)

    if job_skills:
        skill_score = (
            len(matched) / len(job_skills)
        ) * 100
    else:
        skill_score = 0

    text_score = (
        semantic_similarity(
            resume_text,
            job_description
        ) * 100
    )

    experience_bonus = 0

    experience_patterns = [
        r"(\d+)\+?\s+years",
        r"(\d+)\s+years of experience",
    ]

    experience_years = 0

    for pattern in experience_patterns:

        matches = re.findall(
            pattern,
            clean_text(resume_text)
        )

        if matches:
            try:
                experience_years = max(
                    int(x) for x in matches
                )
            except Exception:
                pass

    experience_bonus = min(
        experience_years * 2,
        10
    )

    final = (
        skill_score * 0.55 +
        text_score * 0.35 +
        experience_bonus
    )

    return {
        "score": round(min(final, 100), 1),
        "skills": sorted(resume_skills),
        "matched": sorted(matched),
        "missing": sorted(missing),
        "experience": experience_years,
    }


# ============================================================
# LOGO
# ============================================================

def render_logo():

    svg = """
    <svg width="56" height="56"
         viewBox="0 0 100 100"
         xmlns="http://www.w3.org/2000/svg">

        <defs>
            <linearGradient id="cg"
                x1="0%" y1="0%"
                x2="100%" y2="100%">

                <stop offset="0%"
                    stop-color="#8B7CFF"/>

                <stop offset="100%"
                    stop-color="#38BDF8"/>

            </linearGradient>
        </defs>

        <rect x="4" y="4"
              width="92"
              height="92"
              rx="26"
              fill="#111C30"
              stroke="#293B5C"
              stroke-width="3"/>

        <circle cx="50"
                cy="50"
                r="27"
                fill="none"
                stroke="url(#cg)"
                stroke-width="7"/>

        <path d="M50 24 L50 76"
              stroke="url(#cg)"
              stroke-width="6"
              stroke-linecap="round"/>

        <path d="M24 50 L76 50"
              stroke="url(#cg)"
              stroke-width="6"
              stroke-linecap="round"/>

        <circle cx="50"
                cy="50"
                r="7"
                fill="#FFFFFF"/>
    </svg>
    """

    st.markdown(
        f"""
        <div class="logo-box">
            {svg}
        </div>

        <div class="brand-name">
            Career<span>Lens</span> AI
        </div>

        <div class="brand-subtitle">
            Career Intelligence Platform
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    render_logo()

    st.markdown("---")

    st.markdown(
        """
        <div style="
            color:#657895;
            font-size:11px;
            font-weight:700;
            letter-spacing:1px;
            text-transform:uppercase;
            margin-bottom:8px;">
            Workspace
        </div>
        """,
        unsafe_allow_html=True,
    )

    workspace = st.radio(
        "Workspace",
        [
            "👨‍💻 Job Seeker",
            "🏢 Recruiter",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")

    if workspace == "👨‍💻 Job Seeker":

        st.markdown(
            """
            <div style="
                color:#8295b3;
                font-size:12px;
                margin-bottom:8px;">
                Job Seeker
            </div>
            """,
            unsafe_allow_html=True,
        )

        seeker_page = st.radio(
            "Job Seeker Navigation",
            [
                "Dashboard",
                "Resume Analyzer",
                "Job Matching",
                "Job Fraud Detection",
                "Skill Gap Analysis",
                "Career Roadmap",
            ],
            label_visibility="collapsed",
        )

    else:

        recruiter_page = st.radio(
            "Recruiter Navigation",
            [
                "Recruiter Dashboard",
                "Bulk Resume Screening",
                "Candidate Ranking",
            ],
                label_visibility="collapsed",
        )

    st.markdown("---")

    st.markdown(
        """
        <div class="status-pill">
            <span>●</span>
            AI ENGINE ONLINE
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="
            color:#586c8b;
            font-size:11px;
            margin-top:12px;">
            AI · ML · NLP
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# JOB SEEKER DASHBOARD
# ============================================================

def job_seeker_dashboard():

    analysis = st.session_state.resume_analysis

    st.markdown(
        """
        <div class="hero">

            <div class="hero-kicker">
                AI Career Intelligence
            </div>

            <div class="hero-title">
                Understand Your Career.
                <br>
                <span class="hero-gradient">
                    Build Your Future.
                </span>
            </div>

            <div class="hero-description">
                CareerLens AI analyzes your resume, evaluates
                opportunities, detects job-risk signals,
                identifies skill gaps and helps you build a
                personalized career roadmap.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-title">Career Overview</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">Your career intelligence at a glance.</div>',
        unsafe_allow_html=True,
    )

    if analysis:

        resume_score = analysis["score"]
        readiness = analysis["readiness"]
        skills_count = len(analysis["skills"])

    else:

        resume_score = "—"
        readiness = "—"
        skills_count = 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Resume Score",
            resume_score
        )

    with col2:
        st.metric(
            "Career Readiness",
            readiness
        )

    with col3:
        st.metric(
            "Skills Detected",
            skills_count
        )

    with col4:
        st.metric(
            "Applications",
            len(st.session_state.applications)
        )

    st.markdown(
        '<div class="section-title">Career Intelligence</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">AI-powered tools for smarter career decisions.</div>',
        unsafe_allow_html=True,
    )

    features = [
        (
            "📄",
            "Resume Intelligence",
            "Extract skills, experience, education, projects and profile information from your resume."
        ),
        (
            "🛡️",
            "Job Fraud Detection",
            "Detect suspicious payment, financial, urgency and communication signals."
        ),
        (
            "🎯",
            "AI Job Matching",
            "Compare your profile with job descriptions using NLP similarity and skill matching."
        ),
        (
            "🧩",
            "Skill Gap Analysis",
            "Find missing skills between your current profile and your target career."
        ),
        (
            "🔎",
            "Job Intelligence",
            "Analyze job requirements and understand which skills are important."
        ),
        (
            "🗺️",
            "Career Roadmap",
            "Generate a structured learning and career development path."
        ),
    ]

    cols = st.columns(3)

    for i, feature in enumerate(features):

        icon, title, description = feature

        with cols[i % 3]:

            st.markdown(
                f"""
                <div class="cl-small-card">

                    <div class="feature-icon">
                        {icon}
                    </div>

                    <div class="feature-title">
                        {safe_text(title)}
                    </div>

                    <div class="feature-description">
                        {safe_text(description)}
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        """
        <div class="footer">
            🎯 <b>CareerLens AI</b><br>
            AI-Powered Career Intelligence & Recruitment Platform<br>
            Final Year Project · AI · ML · NLP
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# RESUME ANALYZER
# ============================================================

def resume_analyzer():

    st.markdown(
        '<div class="section-title">Resume Intelligence</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">Upload your resume and let the AI engine analyze your profile.</div>',
        unsafe_allow_html=True,
    )

    uploaded = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx", "txt"],
        help="Supported formats: PDF, DOCX and TXT",
    )

    if uploaded:

        with st.spinner("AI engine analyzing your resume..."):

            text = extract_text_from_upload(uploaded)

            if text.startswith("ERROR:"):

                st.error(text)
                return

            skills = extract_skills(text)

            score = calculate_resume_score(
                text,
                skills
            )

            readiness = calculate_readiness(
                score,
                skills
            )

            st.session_state.resume_text = text

            st.session_state.resume_analysis = {
                "score": score,
                "readiness": readiness,
                "skills": skills,
                "text": text,
                "filename": uploaded.name,
            }

        st.success("Resume analyzed successfully.")

    analysis = st.session_state.resume_analysis

    if not analysis:

        st.markdown(
            """
            <div class="info-box">
                Upload a resume to begin AI analysis.
            </div>
            """,
            unsafe_allow_html=True,
        )

        return

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Resume Score",
            f"{analysis['score']}/100"
        )

    with col2:
        st.metric(
            "Career Readiness",
            analysis["readiness"]
        )

    with col3:
        st.metric(
            "Skills Detected",
            len(analysis["skills"])
        )

    st.markdown("### Detected Skills")

    if analysis["skills"]:

        tags = "".join(
            f'<span class="tag">{safe_text(skill.title())}</span>'
            for skill in analysis["skills"]
        )

        st.markdown(
            tags,
            unsafe_allow_html=True
        )

    else:

        st.warning(
            "No known skills were detected. "
            "Try a resume with a dedicated Skills section."
        )

    st.markdown("### Extracted Resume Text")

    with st.expander("View extracted text"):

        st.text_area(
            "Resume content",
            analysis["text"],
            height=350,
            label_visibility="collapsed",
        )


# ============================================================
# JOB MATCHING
# ============================================================

def job_matching():

    st.markdown(
        '<div class="section-title">AI Job Matching</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">Compare your resume against a job description.</div>',
        unsafe_allow_html=True,
    )

    if not st.session_state.resume_text:

        st.info(
            "First upload your resume from Resume Intelligence."
        )

        return

    job_description = st.text_area(
        "Paste Job Description",
        height=280,
        placeholder=(
            "Paste the complete job description here..."
        ),
    )

    if st.button(
        "🎯 Analyze Job Match",
        type="primary"
    ):

        if not job_description.strip():

            st.warning(
                "Please enter a job description."
            )

            return

        with st.spinner("Running NLP matching engine..."):

            score, matched, missing = calculate_job_match(
                st.session_state.resume_text,
                job_description,
            )

        st.markdown("### Match Result")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Compatibility",
                f"{score}%"
            )

        with c2:
            st.metric(
                "Matching Skills",
                len(matched)
            )

        with c3:
            st.metric(
                "Missing Skills",
                len(missing)
            )

        if score >= 75:

            st.markdown(
                """
                <div class="success-box">
                    Strong match. Your profile aligns well with this opportunity.
                </div>
                """,
                unsafe_allow_html=True,
            )

        elif score >= 50:

            st.markdown(
                """
                <div class="warning-box">
                    Moderate match. Improving the missing skills could increase your compatibility.
                </div>
                """,
                unsafe_allow_html=True,
            )

        else:

            st.markdown(
                """
                <div class="danger-box">
                    Low match. Consider developing the missing skills before applying.
                </div>
                """,
                unsafe_allow_html=True,
            )

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("#### Matching Skills")

            for skill in matched:
                st.markdown(
                    f"✓ {skill.title()}"
                )

        with col2:

            st.markdown("#### Missing Skills")

            for skill in missing:
                st.markdown(
                    f"• {skill.title()}"
                )


# ============================================================
# FRAUD DETECTION
# ============================================================

def fraud_detection():

    st.markdown(
        '<div class="section-title">Job Fraud Detection</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">Analyze a job posting for suspicious risk signals.</div>',
        unsafe_allow_html=True,
    )

    job_text = st.text_area(
        "Paste Job Posting",
        height=320,
        placeholder=(
            "Paste the complete job advertisement here..."
        ),
    )

    if st.button(
        "🛡️ Scan Job Risk",
        type="primary"
    ):

        if not job_text.strip():

            st.warning(
                "Please paste a job posting."
            )

            return

        result = detect_job_fraud(job_text)

        c1, c2 = st.columns(2)

        with c1:
            st.metric(
                "Risk Score",
                f"{result['score']}/100"
            )

        with c2:
            st.metric(
                "Risk Level",
                result["level"]
            )

        if result["level"] == "High Risk":

            st.markdown(
                """
                <div class="danger-box">
                    ⚠️ High-risk signals detected. Carefully verify the employer and job source.
                </div>
                """,
                unsafe_allow_html=True,
            )

        elif result["level"] == "Medium Risk":

            st.markdown(
                """
                <div class="warning-box">
                    ⚠️ Some suspicious signals were detected. Investigate before proceeding.
                </div>
                """,
                unsafe_allow_html=True,
            )

        else:

            st.markdown(
                """
                <div class="success-box">
                    ✓ No major suspicious signals were detected by the current rule engine.
                </div>
                """,
                unsafe_allow_html=True,
            )

        if result["signals"]:

            st.markdown("### Detected Signals")

            for signal in result["signals"]:

                st.markdown(
                    f"""
                    <div class="cl-card">

                        <b>{safe_text(signal['category'])}</b>

                        <br><br>

                        {' '.join(
                            f'<span class="tag">{safe_text(x)}</span>'
                            for x in signal["matches"]
                        )}

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        else:

            st.info(
                "No predefined fraud indicators were detected."
            )

        st.caption(
            "Important: this is an explainable prototype risk detector, "
            "not a definitive determination that a job is fraudulent."
        )


# ============================================================
# SKILL GAP ANALYSIS
# ============================================================

def skill_gap():

    st.markdown(
        '<div class="section-title">Skill Gap Analysis</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">Discover what you need to learn for your target role.</div>',
        unsafe_allow_html=True,
    )

    if not st.session_state.resume_text:

        st.info(
            "Upload your resume first."
        )

        return

    target_job = st.text_area(
        "Target Job Description",
        height=280,
        placeholder=(
            "Paste the job description for your target role..."
        ),
    )

    if st.button(
        "🧩 Analyze Skill Gap",
        type="primary"
    ):

        if not target_job.strip():

            st.warning(
                "Enter a target job description."
            )

            return

        resume_skills = set(
            extract_skills(
                st.session_state.resume_text
            )
        )

        target_skills = set(
            extract_skills(target_job)
        )

        matched = resume_skills.intersection(
            target_skills
        )

        missing = target_skills.difference(
            resume_skills
        )

        c1, c2 = st.columns(2)

        with c1:

            st.metric(
                "Current Skills",
                len(resume_skills)
            )

        with c2:

            st.metric(
                "Skills To Develop",
                len(missing)
            )

        st.markdown("### Skills You Already Have")

        for skill in sorted(matched):

            st.markdown(
                f"✓ **{skill.title()}**"
            )

        st.markdown("### Recommended Skills")

        if missing:

            for skill in sorted(missing):

                st.markdown(
                    f"→ **{skill.title()}**"
                )

        else:

            st.success(
                "No obvious skill gaps were detected."
            )


# ============================================================
# CAREER ROADMAP
# ============================================================

def career_roadmap():

    st.markdown(
        '<div class="section-title">Career Roadmap</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">Create a practical development path toward your target role.</div>',
        unsafe_allow_html=True,
    )

    target = st.text_input(
        "Target Career",
        placeholder="Example: Machine Learning Engineer",
    )

    skills_text = st.text_area(
        "Current Skills",
        placeholder="Example: Python, SQL, Pandas, Machine Learning",
    )

    if st.button(
        "🗺️ Build Career Roadmap",
        type="primary"
    ):

        if not target.strip():

            st.warning(
                "Enter your target career."
            )

            return

        current_skills = extract_skills(
            skills_text
        )

        target_lower = target.lower()

        roadmap = []

        if "machine learning" in target_lower:

            roadmap = [
                ("01", "Python & Data", "Strengthen Python, NumPy, Pandas and data preprocessing."),
                ("02", "Statistics", "Learn probability, statistics and model evaluation."),
                ("03", "Machine Learning", "Master regression, classification, clustering and feature engineering."),
                ("04", "Deep Learning", "Learn neural networks and frameworks such as PyTorch or TensorFlow."),
                ("05", "Projects", "Build 2–3 end-to-end ML projects using real datasets."),
                ("06", "Deployment", "Learn APIs, Streamlit, Docker and cloud deployment."),
            ]

        elif "data scientist" in target_lower:

            roadmap = [
                ("01", "Python", "Strengthen Python, NumPy and Pandas."),
                ("02", "Statistics", "Study probability, statistics and experimentation."),
                ("03", "Data Analysis", "Build strong visualization and exploratory analysis skills."),
                ("04", "Machine Learning", "Learn supervised and unsupervised learning."),
                ("05", "Portfolio", "Build practical data science projects."),
                ("06", "Deployment", "Learn how to deploy models and dashboards."),
            ]

        elif "software" in target_lower or "developer" in target_lower:

            roadmap = [
                ("01", "Programming", "Master one primary programming language."),
                ("02", "DSA", "Practice data structures and algorithms."),
                ("03", "Web Development", "Learn frontend, backend and REST APIs."),
                ("04", "Databases", "Learn SQL and database design."),
                ("05", "Git & Deployment", "Learn Git, Docker and deployment workflows."),
                ("06", "Projects", "Build production-style applications."),
            ]

        else:

            roadmap = [
                ("01", "Foundation", "Strengthen the core knowledge required for the role."),
                ("02", "Technical Skills", "Identify and learn the most important technical skills."),
                ("03", "Projects", "Build practical projects demonstrating those skills."),
                ("04", "Experience", "Work on internships, freelance work or open-source projects."),
                ("05", "Portfolio", "Create a professional portfolio and GitHub profile."),
                ("06", "Interview", "Practice technical, behavioral and role-specific interviews."),
            ]

        for step, title, description in roadmap:

            st.markdown(
                f"""
                <div class="cl-card">

                    <div style="
                        display:flex;
                        gap:18px;
                        align-items:flex-start;">

                        <div class="rank-badge">
                            {step}
                        </div>

                        <div>

                            <div style="
                                color:#f1f5ff;
                                font-size:18px;
                                font-weight:700;">

                                {safe_text(title)}

                            </div>

                            <div style="
                                color:#8092af;
                                margin-top:6px;
                                line-height:1.6;">

                                {safe_text(description)}

                            </div>

                        </div>

                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )


# ============================================================
# RECRUITER DASHBOARD
# ============================================================

def recruiter_dashboard():

    st.markdown(
        """
        <div class="hero">

            <div class="hero-kicker">
                AI Recruitment Intelligence
            </div>

            <div class="hero-title">
                Screen Smarter.
                <br>
                <span class="hero-gradient">
                    Hire Better.
                </span>
            </div>

            <div class="hero-description">
                Upload a large batch of resumes and let CareerLens AI
                rank candidates against your job description using
                skills, NLP similarity and experience signals.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    results = st.session_state.recruiter_results

    if results is not None:

        df = results

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Resumes Screened",
                len(df)
            )

        with col2:
            st.metric(
                "Top Candidate",
                f"{df.iloc[0]['Match Score']}%"
                if len(df)
                else "—"
            )

        with col3:
            st.metric(
                "Average Score",
                f"{df['Match Score'].mean():.1f}%"
                if len(df)
                else "—"
            )

        with col4:
            st.metric(
                "Shortlisted",
                len(df[df["Selected"] == "Yes"])
            )

        st.markdown("### Candidate Ranking")

        display_df = df[
            [
                "Rank",
                "Candidate",
                "Match Score",
                "Skill Match",
                "Experience",
                "Selected",
            ]
        ]

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.markdown(
            """
            <div class="info-box">
                Start by uploading resumes from Bulk Resume Screening.
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# BULK RESUME SCREENING
# ============================================================

def bulk_resume_screening():

    st.markdown(
        '<div class="section-title">Bulk Resume Screening</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">Upload hundreds of resumes and automatically rank the strongest candidates.</div>',
        unsafe_allow_html=True,
    )

    job_description = st.text_area(
        "Job Description",
        height=240,
        placeholder=(
            "Paste the complete job description here..."
        ),
    )

    files = st.file_uploader(
        "Upload Candidate Resumes",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        help="You can upload multiple resumes at once.",
    )

    col1, col2 = st.columns(2)

    with col1:

        top_n = st.number_input(
            "Candidates to shortlist",
            min_value=1,
            max_value=500,
            value=20,
            step=1,
        )

    with col2:

        min_score = st.slider(
            "Minimum match score",
            min_value=0,
            max_value=100,
            value=0,
        )

    if st.button(
        "🚀 Run AI Candidate Screening",
        type="primary"
    ):

        if not job_description.strip():

            st.warning(
                "Please enter a job description."
            )

            return

        if not files:

            st.warning(
                "Please upload at least one resume."
            )

            return

        records = []

        progress = st.progress(0)

        for index, file in enumerate(files):

            text = extract_text_from_upload(file)

            if text.startswith("ERROR:"):

                continue

            result = candidate_score(
                text,
                job_description
            )

            skill_match = 0

            job_skills = set(
                extract_skills(
                    job_description
                )
            )

            if job_skills:

                skill_match = round(
                    len(result["matched"])
                    /
                    len(job_skills)
                    * 100,
                    1
                )

            records.append(
                {
                    "Candidate": file.name,
                    "Match Score": result["score"],
                    "Skill Match": skill_match,
                    "Experience": result["experience"],
                    "Matched Skills": ", ".join(
                        result["matched"]
                    ),
                    "Missing Skills": ", ".join(
                        result["missing"]
                    ),
                    "Resume Text": text,
                }
            )

            progress.progress(
                (index + 1) / len(files)
            )

        if not records:

            st.error(
                "No readable resumes were found."
            )

            return

        df = pd.DataFrame(records)

        df = df[
            df["Match Score"] >= min_score
        ]

        df = df.sort_values(
            by="Match Score",
            ascending=False
        ).reset_index(drop=True)

        df["Rank"] = np.arange(
            1,
            len(df) + 1
        )

        df["Selected"] = np.where(
            df["Rank"] <= top_n,
            "Yes",
            "No"
        )

        st.session_state.recruiter_results = df

        st.success(
            f"Screened {len(files)} resumes and shortlisted the top {min(top_n, len(df))}."
        )

        st.rerun()


# ============================================================
# CANDIDATE RANKING
# ============================================================

def candidate_ranking():

    st.markdown(
        '<div class="section-title">Candidate Ranking</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">Review AI-ranked candidates and inspect individual profiles.</div>',
        unsafe_allow_html=True,
    )

    df = st.session_state.recruiter_results

    if df is None:

        st.info(
            "Run Bulk Resume Screening first."
        )

        return

    # --------------------------------------------------------
    # Top N selector
    # --------------------------------------------------------

    top_n = st.slider(
        "Recruiter shortlist size",
        min_value=1,
        max_value=len(df),
        value=min(20, len(df)),
    )

    shortlisted = df.head(top_n)

    st.markdown(
        f"""
        <div class="success-box">
            AI shortlist currently contains <b>{len(shortlisted)}</b> candidates.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Shortlisted Candidates")

    for _, candidate in shortlisted.iterrows():

        with st.expander(
            f"#{int(candidate['Rank'])}  "
            f"{candidate['Candidate']}  —  "
            f"{candidate['Match Score']}%"
        ):

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric(
                    "Match Score",
                    f"{candidate['Match Score']}%"
                )

            with c2:
                st.metric(
                    "Skill Match",
                    f"{candidate['Skill Match']}%"
                )

            with c3:
                st.metric(
                    "Experience",
                    f"{candidate['Experience']} yrs"
                )

            st.markdown("#### Matching Skills")

            if candidate["Matched Skills"]:

                for skill in candidate[
                    "Matched Skills"
                ].split(", "):

                    if skill:
                        st.markdown(
                            f"✓ {skill.title()}"
                        )

            else:

                st.write("No matching skills detected.")

            st.markdown("#### Missing Skills")

            if candidate["Missing Skills"]:

                for skill in candidate[
                    "Missing Skills"
                ].split(", "):

                    if skill:
                        st.markdown(
                            f"• {skill.title()}"
                        )

            else:

                st.write(
                    "No major missing skills detected."
                )

    st.markdown("### Export Shortlist")

    export_df = shortlisted[
        [
            "Rank",
            "Candidate",
            "Match Score",
            "Skill Match",
            "Experience",
            "Selected",
            "Matched Skills",
            "Missing Skills",
        ]
    ]

    csv = export_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "⬇️ Download Shortlist CSV",
        data=csv,
        file_name="career_lens_shortlist.csv",
        mime="text/csv",
    )


# ============================================================
# ROUTING
# ============================================================

if workspace == "👨‍💻 Job Seeker":

    if seeker_page == "Dashboard":
        job_seeker_dashboard()

    elif seeker_page == "Resume Analyzer":
        resume_analyzer()

    elif seeker_page == "Job Matching":
        job_matching()

    elif seeker_page == "Job Fraud Detection":
        fraud_detection()

    elif seeker_page == "Skill Gap Analysis":
        skill_gap()

    elif seeker_page == "Career Roadmap":
        career_roadmap()

else:

    if recruiter_page == "Recruiter Dashboard":
        recruiter_dashboard()

    elif recruiter_page == "Bulk Resume Screening":
        bulk_resume_screening()

    elif recruiter_page == "Candidate Ranking":
        candidate_ranking()
