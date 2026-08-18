import io
import re
import os
from typing import List, Dict, Tuple

import streamlit as st
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

try:
    from PyPDF2 import PdfReader
except Exception:
    PdfReader = None

try:
    from docx import Document
except Exception:
    Document = None


# ============================================================
# CAREERLENS AI
# Final Year Project
# AI • ML • NLP • Recruitment Intelligence
# ============================================================


# ============================================================
# PAGE CONFIGURATION
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

@import url(
    'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
);

html,
body,
[class*="css"] {
    font-family: "Inter", sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 80% 0%,
            rgba(82, 74, 255, 0.10),
            transparent 30%
        ),
        #070b14;
    color: #f5f7fb;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

.block-container {
    max-width: 1450px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

section[data-testid="stSidebar"] {
    background: #0a101c;
    border-right: 1px solid #1d2940;
}

section[data-testid="stSidebar"] > div {
    padding-top: 1.3rem;
}


/* =========================================================
   BRAND
   ========================================================= */

.brand-container {
    text-align: center;
    padding: 5px 0 18px;
}

.logo-box {
    width: 68px;
    height: 68px;
    margin: auto;

    border-radius: 21px;

    background:
        linear-gradient(
            145deg,
            #7165ff,
            #38bdf8
        );

    display: flex;
    align-items: center;
    justify-content: center;

    box-shadow:
        0 12px 35px rgba(79, 70, 229, 0.35);
}

.logo-symbol {
    position: relative;
    width: 37px;
    height: 37px;
    border: 4px solid white;
    border-radius: 50%;
    box-sizing: border-box;
}

.logo-symbol:before,
.logo-symbol:after {
    content: "";
    position: absolute;
    background: white;
    border-radius: 20px;
}

.logo-symbol:before {
    width: 4px;
    height: 43px;
    left: 12px;
    top: -7px;
}

.logo-symbol:after {
    width: 43px;
    height: 4px;
    left: -7px;
    top: 12px;
}

.brand-name {
    margin-top: 13px;
    font-size: 23px;
    font-weight: 800;
    letter-spacing: -0.7px;
}

.brand-name span {
    background:
        linear-gradient(
            90deg,
            #8b7cff,
            #38bdf8
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.brand-subtitle {
    color: #657894;
    font-size: 10px;
    margin-top: 4px;
    letter-spacing: 0.5px;
}


/* =========================================================
   HERO
   ========================================================= */

.hero {
    position: relative;

    padding: 42px;

    border-radius: 22px;

    border: 1px solid #22324d;

    background:
        radial-gradient(
            circle at 90% 15%,
            rgba(56,189,248,.10),
            transparent 28%
        ),
        radial-gradient(
            circle at 10% 90%,
            rgba(113,101,255,.10),
            transparent 30%
        ),
        #0e1726;

    margin-bottom: 28px;
}

.hero-label {
    color: #8d82ff;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.4px;
    text-transform: uppercase;
}

.hero-title {
    margin-top: 10px;

    font-size: 48px;
    line-height: 1.05;

    font-weight: 800;

    letter-spacing: -2px;
}

.hero-gradient {
    background:
        linear-gradient(
            90deg,
            #8b7cff,
            #38bdf8
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-description {
    max-width: 760px;

    margin-top: 18px;

    color: #8597b0;

    font-size: 15px;
    line-height: 1.7;
}


/* =========================================================
   CARDS
   ========================================================= */

.feature-card {
    background: #0e1726;

    border: 1px solid #1e2d45;

    border-radius: 16px;

    padding: 22px;

    min-height: 175px;

    transition: 0.2s ease;
}

.feature-card:hover {
    border-color: #3b4f72;
    transform: translateY(-2px);
}

.feature-icon {
    font-size: 26px;
    margin-bottom: 10px;
}

.feature-title {
    font-size: 16px;
    font-weight: 700;
}

.feature-description {
    color: #788aa3;
    font-size: 13px;
    line-height: 1.6;
    margin-top: 8px;
}


/* =========================================================
   METRICS
   ========================================================= */

div[data-testid="stMetric"] {
    background: #0e1726;
    border: 1px solid #1e2d45;
    border-radius: 15px;
    padding: 18px;
}

div[data-testid="stMetricLabel"] {
    color: #788aa3;
}

div[data-testid="stMetricValue"] {
    color: #ffffff;
    font-weight: 800;
}


/* =========================================================
   BUTTONS
   ========================================================= */

.stButton > button {
    width: 100%;
    min-height: 43px;

    border-radius: 10px;

    background: #111c2e;

    color: white;

    border: 1px solid #293a58;

    font-weight: 600;
}

.stButton > button:hover {
    border-color: #7165ff;
    color: white;
}


/* =========================================================
   INPUTS
   ========================================================= */

.stTextInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] {
    background-color: #0d1625;
    color: white;
}

section[data-testid="stFileUploaderDropzone"] {
    background: #0d1625;
    border: 1px dashed #344766;
    border-radius: 14px;
}


/* =========================================================
   BADGES
   ========================================================= */

.badge-success {
    padding: 6px 10px;
    border-radius: 8px;

    background: rgba(34,197,94,.10);

    color: #65d98b;

    border: 1px solid rgba(34,197,94,.20);

    font-size: 12px;
    font-weight: 700;
}

.badge-warning {
    padding: 6px 10px;
    border-radius: 8px;

    background: rgba(245,158,11,.10);

    color: #f4bd55;

    border: 1px solid rgba(245,158,11,.20);

    font-size: 12px;
    font-weight: 700;
}

.badge-danger {
    padding: 6px 10px;
    border-radius: 8px;

    background: rgba(239,68,68,.10);

    color: #f47777;

    border: 1px solid rgba(239,68,68,.20);

    font-size: 12px;
    font-weight: 700;
}


/* =========================================================
   FOOTER
   ========================================================= */

.footer {
    text-align: center;
    color: #536680;

    font-size: 11px;

    padding: 40px 0 10px;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SKILL DATABASE
# ============================================================

SKILLS = {
    "python",
    "java",
    "javascript",
    "typescript",
    "c",
    "c++",
    "c#",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "html",
    "css",
    "react",
    "angular",
    "node.js",
    "node",
    "express",
    "django",
    "flask",
    "fastapi",
    "streamlit",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "ai",
    "nlp",
    "natural language processing",
    "computer vision",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "sklearn",
    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",
    "git",
    "github",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "linux",
    "rest api",
    "api",
    "data analysis",
    "data science",
    "excel",
    "power bi",
    "tableau",
    "spark",
    "hadoop",
    "firebase",
    "figma",
    "agile",
    "scrum",
    "communication",
    "leadership",
    "problem solving",
}


# ============================================================
# TEXT EXTRACTION
# ============================================================

def extract_pdf_text(file) -> str:
    if PdfReader is None:
        return ""

    try:
        reader = PdfReader(file)
        pages = []

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pages.append(text)

        return "\n".join(pages)

    except Exception:
        return ""


def extract_docx_text(file) -> str:
    if Document is None:
        return ""

    try:
        data = file.read()
        document = Document(io.BytesIO(data))

        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        return "\n".join(paragraphs)

    except Exception:
        return ""


def extract_text(file) -> str:

    if file is None:
        return ""

    filename = file.name.lower()

    if filename.endswith(".pdf"):
        return extract_pdf_text(file)

    if filename.endswith(".docx"):
        return extract_docx_text(file)

    if filename.endswith(".txt"):
        try:
            return file.read().decode(
                "utf-8",
                errors="ignore",
            )
        except Exception:
            return ""

    return ""


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text: str) -> str:

    if not text:
        return ""

    text = text.lower()

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


# ============================================================
# SKILL EXTRACTION
# ============================================================

def extract_skills(text: str) -> List[str]:

    cleaned = clean_text(text)

    found = []

    for skill in SKILLS:

        pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"

        if re.search(pattern, cleaned):

            found.append(skill)

    return sorted(
        list(set(found))
    )


# ============================================================
# CONTACT EXTRACTION
# ============================================================

def extract_email(text: str):

    match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text,
    )

    if match:
        return match.group(0)

    return "Not detected"


def extract_phone(text: str):

    match = re.search(
        r"(?:\+?\d[\d\s().-]{8,}\d)",
        text,
    )

    if match:
        return match.group(0).strip()

    return "Not detected"


# ============================================================
# RESUME SCORING
# ============================================================

def calculate_resume_score(
    text: str,
    skills: List[str],
) -> int:

    score = 0

    lowered = clean_text(text)

    # Skills
    score += min(
        len(skills) * 4,
        40,
    )

    # Sections
    sections = [
        "education",
        "experience",
        "skills",
        "projects",
        "certifications",
        "summary",
    ]

    section_count = sum(
        1
        for section in sections
        if section in lowered
    )

    score += min(
        section_count * 5,
        30,
    )

    # Contact
    if extract_email(text) != "Not detected":
        score += 10

    if extract_phone(text) != "Not detected":
        score += 5

    # Length
    word_count = len(
        lowered.split()
    )

    if word_count >= 250:
        score += 10

    if word_count >= 500:
        score += 5

    return min(
        score,
        100,
    )


# ============================================================
# JOB MATCHING
# ============================================================

def calculate_similarity(
    resume_text: str,
    job_text: str,
) -> float:

    resume_text = clean_text(resume_text)
    job_text = clean_text(job_text)

    if not resume_text or not job_text:
        return 0.0

    try:

        vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        vectors = vectorizer.fit_transform(
            [
                resume_text,
                job_text,
            ]
        )

        similarity = cosine_similarity(
            vectors[0:1],
            vectors[1:2],
        )[0][0]

        return float(
            round(
                similarity * 100,
                2,
            )
        )

    except Exception:
        return 0.0


def skill_match_score(
    resume_skills: List[str],
    job_skills: List[str],
) -> Tuple[float, List[str], List[str]]:

    if not job_skills:
        return 0.0, [], []

    resume_set = set(
        skill.lower()
        for skill in resume_skills
    )

    job_set = set(
        skill.lower()
        for skill in job_skills
    )

    matched = sorted(
        resume_set.intersection(job_set)
    )

    missing = sorted(
        job_set.difference(resume_set)
    )

    score = (
        len(matched) /
        len(job_set)
    ) * 100

    return (
        round(score, 2),
        matched,
        missing,
    )


def combined_job_score(
    resume_text: str,
    job_text: str,
) -> Dict:

    resume_skills = extract_skills(
        resume_text
    )

    job_skills = extract_skills(
        job_text
    )

    similarity = calculate_similarity(
        resume_text,
        job_text,
    )

    skill_score, matched, missing = (
        skill_match_score(
            resume_skills,
            job_skills,
        )
    )

    final_score = (
        similarity * 0.45
        +
        skill_score * 0.55
    )

    return {
        "similarity": round(
            similarity,
            2,
        ),
        "skill_score": round(
            skill_score,
            2,
        ),
        "final_score": round(
            final_score,
            2,
        ),
        "matched_skills": matched,
        "missing_skills": missing,
    }


# ============================================================
# FRAUD DETECTION
# ============================================================

FRAUD_PATTERNS = {

    "Payment Request": [
        "pay registration fee",
        "registration fee",
        "pay money",
        "processing fee",
        "security deposit",
        "deposit money",
        "pay upfront",
        "payment required",
    ],

    "Financial Information": [
        "bank account",
        "bank details",
        "credit card",
        "debit card",
        "otp",
        "one time password",
        "financial details",
    ],

    "Urgency": [
        "act immediately",
        "urgent",
        "limited seats",
        "today only",
        "respond immediately",
        "immediate joining",
    ],

    "Suspicious Communication": [
        "telegram",
        "whatsapp only",
        "contact via whatsapp",
        "contact via telegram",
        "gmail recruitment",
    ],

    "Unrealistic Offer": [
        "earn $10000",
        "earn 10000",
        "guaranteed income",
        "no experience required",
        "work 1 hour",
        "easy money",
    ],
}


def detect_fraud(
    job_text: str,
) -> Dict:

    text = clean_text(
        job_text
    )

    findings = []

    categories = set()

    for category, patterns in FRAUD_PATTERNS.items():

        for pattern in patterns:

            if pattern in text:

                findings.append(
                    pattern
                )

                categories.add(
                    category
                )

    # Score
    risk_score = min(
        len(findings) * 12,
        100,
    )

    if risk_score >= 60:
        level = "HIGH"

    elif risk_score >= 30:
        level = "MEDIUM"

    else:
        level = "LOW"

    return {
        "risk_score": risk_score,
        "risk_level": level,
        "findings": findings,
        "categories": sorted(
            categories
        ),
    }


# ============================================================
# JOB INTELLIGENCE
# ============================================================

def analyze_job(
    job_text: str,
) -> Dict:

    skills = extract_skills(
        job_text
    )

    fraud = detect_fraud(
        job_text
    )

    words = len(
        clean_text(job_text).split()
    )

    return {
        "skills": skills,
        "skill_count": len(skills),
        "word_count": words,
        "fraud": fraud,
    }


# ============================================================
# CAREER ROADMAP
# ============================================================

def generate_roadmap(
    current_skills: List[str],
    target_skills: List[str],
) -> Dict:

    current = set(
        skill.lower()
        for skill in current_skills
    )

    target = set(
        skill.lower()
        for skill in target_skills
    )

    missing = sorted(
        target.difference(current)
    )

    phases = []

    if missing:

        phases.append(
            {
                "phase": "Phase 1",
                "title": "Build Core Skills",
                "skills": missing[:3],
            }
        )

        if len(missing) > 3:

            phases.append(
                {
                    "phase": "Phase 2",
                    "title": "Develop Advanced Skills",
                    "skills": missing[3:6],
                }
            )

        if len(missing) > 6:

            phases.append(
                {
                    "phase": "Phase 3",
                    "title": "Specialize",
                    "skills": missing[6:],
                }
            )

    else:

        phases.append(
            {
                "phase": "Phase 1",
                "title": "Profile Strengthening",
                "skills": [
                    "Build projects",
                    "Improve portfolio",
                    "Practice interviews",
                ],
            }
        )

    return {
        "missing": missing,
        "phases": phases,
    }


# ============================================================
# FILE NAME
# ============================================================

def candidate_name(
    filename: str,
) -> str:

    name = os.path.splitext(
        filename
    )[0]

    name = re.sub(
        r"[_-]+",
        " ",
        name,
    )

    return name.title()


# ============================================================
# SIDEBAR BRAND
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand-container">

            <div class="logo-box">
                <div class="logo-symbol"></div>
            </div>

            <div class="brand-name">
                Career<span>Lens</span> AI
            </div>

            <div class="brand-subtitle">
                CAREER INTELLIGENCE PLATFORM
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.caption("WORKSPACE")

    workspace = st.radio(
        "Workspace",
        [
            "👨‍💻 Job Seeker",
            "🏢 Recruiter",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    st.success(
        "● AI ENGINE ONLINE"
    )

    st.caption(
        "NLP • ML • Recruitment Intelligence"
    )


# ============================================================
# JOB SEEKER NAVIGATION
# ============================================================

if workspace == "👨‍💻 Job Seeker":

    st.sidebar.divider()

    seeker_module = st.sidebar.radio(
        "JOB SEEKER MODULES",
        [
            "🏠 Dashboard",
            "📄 Resume Intelligence",
            "🎯 AI Job Matching",
            "🛡️ Job Fraud Detection",
            "🧩 Skill Gap Analysis",
            "🔎 Job Intelligence",
            "🗺️ Career Roadmap",
        ],
    )


# ============================================================
# RECRUITER NAVIGATION
# ============================================================

else:

    st.sidebar.divider()

    recruiter_module = st.sidebar.radio(
        "RECRUITER MODULES",
        [
            "🏢 Recruiter Dashboard",
            "📂 Bulk Resume Screening",
            "🧠 AI Candidate Ranking",
            "🎯 Top-N Shortlist",
            "📊 Candidate Comparison",
        ],
    )


# ============================================================
# JOB SEEKER DASHBOARD
# ============================================================

if (
    workspace == "👨‍💻 Job Seeker"
    and seeker_module == "🏠 Dashboard"
):

    st.markdown(
        """
        <div class="hero">

            <div class="hero-label">
                AI CAREER INTELLIGENCE
            </div>

            <div class="hero-title">
                Understand Your Career.
                <br>
                <span class="hero-gradient">
                    Build Your Future.
                </span>
            </div>

            <div class="hero-description">
                CareerLens AI analyzes your resume,
                evaluates opportunities, detects
                job-risk signals, identifies skill
                gaps and builds a personalized
                career intelligence profile.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader(
        "Career Overview"
    )

    st.caption(
        "Your career intelligence at a glance."
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Resume Score",
            "—",
        )

    with c2:
        st.metric(
            "Career Readiness",
            "—",
        )

    with c3:
        st.metric(
            "Skills Detected",
            "0",
        )

    with c4:
        st.metric(
            "Applications",
            "0",
        )

    st.divider()

    st.subheader(
        "Career Intelligence"
    )

    features = [
        (
            "📄",
            "Resume Intelligence",
            "Extract skills, education, projects and experience from your resume.",
        ),
        (
            "🎯",
            "AI Job Matching",
            "Compare your resume with a target job using NLP similarity and skill matching.",
        ),
        (
            "🛡️",
            "Job Fraud Detection",
            "Detect suspicious payment, financial, urgency and communication signals.",
        ),
        (
            "🧩",
            "Skill Gap Analysis",
            "Identify missing skills between your profile and target job.",
        ),
        (
            "🔎",
            "Job Intelligence",
            "Extract important skills and risk signals from job descriptions.",
        ),
        (
            "🗺️",
            "Career Roadmap",
            "Generate a structured path toward your target role.",
        ),
    ]

    row1 = st.columns(3)

    for col, item in zip(
        row1,
        features[:3],
    ):

        icon, title, description = item

        with col:

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
                unsafe_allow_html=True,
            )

    st.write("")

    row2 = st.columns(3)

    for col, item in zip(
        row2,
        features[3:],
    ):

        icon, title, description = item

        with col:

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
                unsafe_allow_html=True,
            )


# ============================================================
# RESUME INTELLIGENCE
# ============================================================

elif (
    workspace == "👨‍💻 Job Seeker"
    and seeker_module == "📄 Resume Intelligence"
):

    st.title(
        "📄 Resume Intelligence"
    )

    st.caption(
        "Upload your resume and let CareerLens AI analyze it."
    )

    uploaded = st.file_uploader(
        "Upload Resume",
        type=[
            "pdf",
            "docx",
            "txt",
        ],
    )

    if uploaded:

        with st.spinner(
            "Analyzing resume..."
        ):

            text = extract_text(
                uploaded
            )

            skills = extract_skills(
                text
            )

            score = calculate_resume_score(
                text,
                skills,
            )

            email = extract_email(
                text
            )

            phone = extract_phone(
                text
            )

        if not text:

            st.error(
                "Could not extract text from this file."
            )

        else:

            st.success(
                "Resume analyzed successfully."
            )

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric(
                    "Resume Score",
                    f"{score}/100",
                )

            with c2:
                st.metric(
                    "Skills Detected",
                    len(skills),
                )

            with c3:
                st.metric(
                    "Words",
                    len(text.split()),
                )

            st.divider()

            st.subheader(
                "Contact Intelligence"
            )

            c1, c2 = st.columns(2)

            with c1:
                st.write(
                    f"**Email:** {email}"
                )

            with c2:
                st.write(
                    f"**Phone:** {phone}"
                )

            st.subheader(
                "Detected Skills"
            )

            if skills:

                st.write(
                    " • ".join(
                        skills
                    )
                )

            else:

                st.warning(
                    "No known skills were detected."
                )

            st.subheader(
                "Resume Preview"
            )

            st.text_area(
                "Extracted resume text",
                text[:10000],
                height=300,
            )


# ============================================================
# AI JOB MATCHING
# ============================================================

elif (
    workspace == "👨‍💻 Job Seeker"
    and seeker_module == "🎯 AI Job Matching"
):

    st.title(
        "🎯 AI Job Matching"
    )

    st.caption(
        "Compare your resume with a target job using NLP and skill intelligence."
    )

    resume_file = st.file_uploader(
        "Upload Resume",
        type=[
            "pdf",
            "docx",
            "txt",
        ],
        key="matching_resume",
    )

    job_description = st.text_area(
        "Paste Job Description",
        height=260,
        placeholder=(
            "Paste the complete job description here..."
        ),
    )

    if st.button(
        "Analyze Job Match",
        type="primary",
    ):

        if not resume_file:

            st.error(
                "Please upload a resume."
            )

        elif not job_description.strip():

            st.error(
                "Please enter a job description."
            )

        else:

            resume_text = extract_text(
                resume_file
            )

            result = combined_job_score(
                resume_text,
                job_description,
            )

            st.success(
                "Job match analysis completed."
            )

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric(
                    "Overall Match",
                    f"{result['final_score']}%",
                )

            with c2:
                st.metric(
                    "NLP Similarity",
                    f"{result['similarity']}%",
                )

            with c3:
                st.metric(
                    "Skill Match",
                    f"{result['skill_score']}%",
                )

            st.divider()

            st.subheader(
                "Matched Skills"
            )

            if result["matched_skills"]:

                st.success(
                    ", ".join(
                        result["matched_skills"]
                    )
                )

            else:

                st.info(
                    "No matching skills detected."
                )

            st.subheader(
                "Skill Gaps"
            )

            if result["missing_skills"]:

                st.warning(
                    ", ".join(
                        result["missing_skills"]
                    )
                )

            else:

                st.success(
                    "No major skill gaps detected."
                )


# ============================================================
# JOB FRAUD DETECTION
# ============================================================

elif (
    workspace == "👨‍💻 Job Seeker"
    and seeker_module == "🛡️ Job Fraud Detection"
):

    st.title(
        "🛡️ Job Fraud Detection"
    )

    st.caption(
        "Analyze a job posting for suspicious risk signals."
    )

    job_text = st.text_area(
        "Paste Job Posting",
        height=320,
        placeholder=(
            "Paste the complete job advertisement here..."
        ),
    )

    if st.button(
        "Scan Job for Risk",
        type="primary",
    ):

        if not job_text.strip():

            st.error(
                "Please enter a job posting."
            )

        else:

            result = detect_fraud(
                job_text
            )

            score = result[
                "risk_score"
            ]

            level = result[
                "risk_level"
            ]

            if level == "HIGH":

                st.error(
                    f"HIGH RISK — {score}/100"
                )

            elif level == "MEDIUM":

                st.warning(
                    f"MEDIUM RISK — {score}/100"
                )

            else:

                st.success(
                    f"LOW RISK — {score}/100"
                )

            st.subheader(
                "Detected Signals"
            )

            if result["categories"]:

                for category in result[
                    "categories"
                ]:

                    st.write(
                        f"⚠️ {category}"
                    )

            else:

                st.success(
                    "No major suspicious categories detected."
                )

            if result["findings"]:

                st.subheader(
                    "Matched Risk Indicators"
                )

                for finding in result[
                    "findings"
                ]:

                    st.write(
                        f"• {finding}"
                    )

            st.info(
                "This is an AI-assisted risk screening system, "
                "not a legal guarantee that a job is legitimate or fraudulent."
            )


# ============================================================
# JOB INTELLIGENCE
# ============================================================

elif (
    workspace == "👨‍💻 Job Seeker"
    and seeker_module == "🔎 Job Intelligence"
):

    st.title(
        "🔎 Job Intelligence"
    )

    st.caption(
        "Understand the requirements hidden inside a job description."
    )

    job_text = st.text_area(
        "Paste Job Description",
        height=320,
    )

    if st.button(
        "Analyze Job",
        type="primary",
    ):

        if not job_text.strip():

            st.error(
                "Please enter a job description."
            )

        else:

            result = analyze_job(
                job_text
            )

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric(
                    "Skills Found",
                    result["skill_count"],
                )

            with c2:
                st.metric(
                    "Description Words",
                    result["word_count"],
                )

            with c3:
                st.metric(
                    "Fraud Risk",
                    f"{result['fraud']['risk_score']}/100",
                )

            st.divider()

            st.subheader(
                "Required Skills"
            )

            if result["skills"]:

                st.write(
                    " • ".join(
                        result["skills"]
                    )
                )

            else:

                st.info(
                    "No known technical skills detected."
                )


# ============================================================
# SKILL GAP ANALYSIS
# ============================================================

elif (
    workspace == "👨‍💻 Job Seeker"
    and seeker_module == "🧩 Skill Gap Analysis"
):

    st.title(
        "🧩 Skill Gap Analysis"
    )

    st.caption(
        "Discover the skills missing for your target opportunity."
    )

    resume_file = st.file_uploader(
        "Upload Resume",
        type=[
            "pdf",
            "docx",
            "txt",
        ],
        key="gap_resume",
    )

    target_job = st.text_area(
        "Paste Target Job Description",
        height=260,
    )

    if st.button(
        "Analyze Skill Gap",
        type="primary",
    ):

        if not resume_file:

            st.error(
                "Upload your resume first."
            )

        elif not target_job.strip():

            st.error(
                "Enter the target job description."
            )

        else:

            resume_text = extract_text(
                resume_file
            )

            current_skills = extract_skills(
                resume_text
            )

            target_skills = extract_skills(
                target_job
            )

            score, matched, missing = (
                skill_match_score(
                    current_skills,
                    target_skills,
                )
            )

            c1, c2 = st.columns(2)

            with c1:
                st.metric(
                    "Skill Match",
                    f"{score}%",
                )

            with c2:
                st.metric(
                    "Missing Skills",
                    len(missing),
                )

            st.subheader(
                "Your Skills"
            )

            st.write(
                ", ".join(
                    current_skills
                )
                if current_skills
                else "None detected"
            )

            st.subheader(
                "Matched Skills"
            )

            st.success(
                ", ".join(
                    matched
                )
                if matched
                else "No matches"
            )

            st.subheader(
                "Skills to Learn"
            )

            st.warning(
                ", ".join(
                    missing
                )
                if missing
                else "No major gaps detected"
            )


# ============================================================
# CAREER ROADMAP
# ============================================================

elif (
    workspace == "👨‍💻 Job Seeker"
    and seeker_module == "🗺️ Career Roadmap"
):

    st.title(
        "🗺️ Career Roadmap"
    )

    st.caption(
        "Build a learning path from your current skills to your target role."
    )

    current = st.text_input(
        "Current Skills",
        placeholder=(
            "Python, SQL, Git, Machine Learning..."
        ),
    )

    target = st.text_input(
        "Target Skills",
        placeholder=(
            "Python, SQL, Machine Learning, Docker, AWS..."
        ),
    )

    if st.button(
        "Generate Roadmap",
        type="primary",
    ):

        current_skills = [
            x.strip().lower()
            for x in current.split(",")
            if x.strip()
        ]

        target_skills = [
            x.strip().lower()
            for x in target.split(",")
            if x.strip()
        ]

        if not target_skills:

            st.error(
                "Enter your target skills."
            )

        else:

            roadmap = generate_roadmap(
                current_skills,
                target_skills,
            )

            st.subheader(
                "Skills to Develop"
            )

            if roadmap["missing"]:

                st.warning(
                    ", ".join(
                        roadmap["missing"]
                    )
                )

            else:

                st.success(
                    "You already cover the target skills."
                )

            st.divider()

            for phase in roadmap[
                "phases"
            ]:

                st.markdown(
                    f"### {phase['phase']} — {phase['title']}"
                )

                for skill in phase[
                    "skills"
                ]:

                    st.write(
                        f"• {skill}"
                    )


# ============================================================
# RECRUITER DASHBOARD
# ============================================================

elif (
    workspace == "🏢 Recruiter"
    and recruiter_module == "🏢 Recruiter Dashboard"
):

    st.markdown(
        """
        <div class="hero">

            <div class="hero-label">
                AI RECRUITMENT INTELLIGENCE
            </div>

            <div class="hero-title">
                Screen Smarter.
                <br>
                <span class="hero-gradient">
                    Hire Better.
                </span>
            </div>

            <div class="hero-description">
                CareerLens AI helps recruiters process
                large resume collections, rank candidates,
                compare skills and create a configurable
                shortlist using NLP and ML-based scoring.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader(
        "Recruiter Intelligence"
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.info(
            "📂 Upload hundreds of resumes"
        )

    with c2:
        st.info(
            "🧠 Automatically rank candidates"
        )

    with c3:
        st.info(
            "🎯 Select your own Top-N"
        )

    st.divider()

    st.subheader(
        "Recruitment Workflow"
    )

    st.write(
        """
        **1. Upload resumes → 2. Enter job description → 
        3. CareerLens analyzes skills → 4. Candidates are ranked → 
        5. Recruiter chooses Top-N → 6. Export shortlist**
        """
    )


# ============================================================
# BULK RESUME SCREENING
# ============================================================

elif (
    workspace == "🏢 Recruiter"
    and recruiter_module == "📂 Bulk Resume Screening"
):

    st.title(
        "📂 Bulk Resume Screening"
    )

    st.caption(
        "Upload multiple resumes and analyze them against a target job."
    )

    job_description = st.text_area(
        "Target Job Description",
        height=220,
        placeholder=(
            "Paste the complete job description here..."
        ),
    )

    resumes = st.file_uploader(
        "Upload Candidate Resumes",
        type=[
            "pdf",
            "docx",
            "txt",
        ],
        accept_multiple_files=True,
    )

    if st.button(
        "Run AI Screening",
        type="primary",
    ):

        if not job_description.strip():

            st.error(
                "Enter the target job description."
            )

        elif not resumes:

            st.error(
                "Upload at least one resume."
            )

        else:

            results = []

            progress = st.progress(
                0
            )

            total = len(
                resumes
            )

            for index, resume in enumerate(
                resumes
            ):

                text = extract_text(
                    resume
                )

                if not text:

                    continue

                skills = extract_skills(
                    text
                )

                result = combined_job_score(
                    text,
                    job_description,
                )

                resume_score = calculate_resume_score(
                    text,
                    skills,
                )

                results.append(
                    {
                        "Candidate": candidate_name(
                            resume.name
                        ),
                        "File": resume.name,
                        "Overall Match": result[
                            "final_score"
                        ],
                        "NLP Similarity": result[
                            "similarity"
                        ],
                        "Skill Match": result[
                            "skill_score"
                        ],
                        "Resume Score": resume_score,
                        "Matched Skills": ", ".join(
                            result[
                                "matched_skills"
                            ]
                        ),
                        "Missing Skills": ", ".join(
                            result[
                                "missing_skills"
                            ]
                        ),
                    }
                )

                progress.progress(
                    (index + 1) / total
                )

            if results:

                df = pd.DataFrame(
                    results
                )

                df = df.sort_values(
                    "Overall Match",
                    ascending=False,
                ).reset_index(
                    drop=True
                )

                df.insert(
                    0,
                    "Rank",
                    range(
                        1,
                        len(df) + 1,
                    ),
                )

                st.session_state[
                    "candidate_results"
                ] = df

                st.success(
                    f"Successfully analyzed {len(df)} candidates."
                )

                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                )

            else:

                st.error(
                    "No readable resumes were found."
                )


# ============================================================
# AI CANDIDATE RANKING
# ============================================================

elif (
    workspace == "🏢 Recruiter"
    and recruiter_module == "🧠 AI Candidate Ranking"
):

    st.title(
        "🧠 AI Candidate Ranking"
    )

    st.caption(
        "Review candidates ranked by NLP similarity and skill compatibility."
    )

    if (
        "candidate_results"
        not in st.session_state
    ):

        st.info(
            "Run Bulk Resume Screening first."
        )

    else:

        df = st.session_state[
            "candidate_results"
        ]

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

        st.divider()

        st.subheader(
            "Top Candidates"
        )

        top_count = min(
            10,
            len(df),
        )

        for index in range(
            top_count
        ):

            row = df.iloc[
                index
            ]

            with st.expander(
                f"#{int(row['Rank'])}  {row['Candidate']}  —  {row['Overall Match']}%"
            ):

                c1, c2, c3 = st.columns(3)

                with c1:
                    st.metric(
                        "Overall Match",
                        f"{row['Overall Match']}%",
                    )

                with c2:
                    st.metric(
                        "Skill Match",
                        f"{row['Skill Match']}%",
                    )

                with c3:
                    st.metric(
                        "Resume Score",
                        f"{row['Resume Score']}/100",
                    )

                st.write(
                    f"**Matched Skills:** "
                    f"{row['Matched Skills'] or 'None'}"
                )

                st.write(
                    f"**Missing Skills:** "
                    f"{row['Missing Skills'] or 'None'}"
                )


# ============================================================
# TOP-N SHORTLIST
# ============================================================

elif (
    workspace == "🏢 Recruiter"
    and recruiter_module == "🎯 Top-N Shortlist"
):

    st.title(
        "🎯 Top-N Candidate Shortlist"
    )

    st.caption(
        "The recruiter decides how many candidates should be shortlisted."
    )

    if (
        "candidate_results"
        not in st.session_state
    ):

        st.info(
            "Run Bulk Resume Screening first."
        )

    else:

        df = st.session_state[
            "candidate_results"
        ]

        max_candidates = len(
            df
        )

        top_n = st.number_input(
            "Number of candidates to shortlist",
            min_value=1,
            max_value=max_candidates,
            value=min(
                10,
                max_candidates,
            ),
            step=1,
        )

        shortlist = df.head(
            top_n
        ).copy()

        st.success(
            f"Top {top_n} candidates selected."
        )

        st.dataframe(
            shortlist,
            use_container_width=True,
            hide_index=True,
        )

        csv = shortlist.to_csv(
            index=False
        ).encode(
            "utf-8"
        )

        st.download_button(
            "⬇️ Download Shortlist CSV",
            csv,
            "CareerLens_shortlist.csv",
            "text/csv",
        )


# ============================================================
# CANDIDATE COMPARISON
# ============================================================

elif (
    workspace == "🏢 Recruiter"
    and recruiter_module == "📊 Candidate Comparison"
):

    st.title(
        "📊 Candidate Comparison"
    )

    st.caption(
        "Compare candidates using the AI screening results."
    )

    if (
        "candidate_results"
        not in st.session_state
    ):

        st.info(
            "Run Bulk Resume Screening first."
        )

    else:

        df = st.session_state[
            "candidate_results"
        ]

        candidate_names = df[
            "Candidate"
        ].tolist()

        selected = st.multiselect(
            "Select candidates",
            candidate_names,
            default=candidate_names[
                :min(3, len(candidate_names))
            ],
        )

        if selected:

            comparison = df[
                df["Candidate"].isin(
                    selected
                )
            ]

            st.dataframe(
                comparison,
                use_container_width=True,
                hide_index=True,
            )

            st.subheader(
                "Comparison"
            )

            cols = st.columns(
                len(comparison)
            )

            for col, (_, row) in zip(
                cols,
                comparison.iterrows(),
            ):

                with col:

                    st.markdown(
                        f"### {row['Candidate']}"
                    )

                    st.metric(
                        "Overall",
                        f"{row['Overall Match']}%",
                    )

                    st.metric(
                        "Skill Match",
                        f"{row['Skill Match']}%",
                    )

                    st.metric(
                        "Resume Score",
                        f"{row['Resume Score']}/100",
                    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div class="footer">

        <b>CareerLens AI</b><br>

        AI-Powered Career Intelligence & Recruitment Platform<br>

        Final Year Project • Artificial Intelligence • Machine Learning • NLP

    </div>
    """,
    unsafe_allow_html=True,
)
