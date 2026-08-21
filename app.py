
import io
import re
from typing import List, Dict

import streamlit as st
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

try:
    from PyPDF2 import PdfReader
except ImportError:
    PdfReader = None

try:
    from docx import Document
except ImportError:
    Document = None


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
# CAREERLENS AI — GLOBAL STYLES
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- MAIN APP ---------- */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 0%,
                rgba(99, 102, 241, 0.16),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 5%,
                rgba(56, 189, 248, 0.12),
                transparent 28%
            ),
            #07101f;
        color: #e5e7eb;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* ---------- SIDEBAR ---------- */

    [data-testid="stSidebar"] {
        background: #091426;
        border-right: 1px solid rgba(148, 163, 184, 0.12);
    }

    [data-testid="stSidebar"] * {
        color: #e2e8f0;
    }

    /* ---------- BRAND ---------- */

    .brand {
        text-align: center;
        padding: 10px 0 22px;
    }

    .brand-logo {
        width: 70px;
        height: 70px;
        margin: auto;
        border-radius: 22px;

        display: flex;
        align-items: center;
        justify-content: center;

        font-size: 36px;

        background:
            linear-gradient(
                135deg,
                rgba(129, 140, 248, 0.20),
                rgba(56, 189, 248, 0.16)
            );

        border: 1px solid rgba(129, 140, 248, 0.35);

        box-shadow:
            0 10px 35px rgba(56, 189, 248, 0.08);
    }

    .brand-name {
        margin-top: 12px;
        font-size: 27px;
        font-weight: 850;
        color: #f8fafc;
        letter-spacing: -1px;
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
        margin-top: 4px;
        color: #64748b;
        font-size: 9px;
        font-weight: 700;
        letter-spacing: 2px;
    }

    .engine-online {
        text-align: center;
        color: #4ade80;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1px;
        margin-top: 10px;
    }

    /* ---------- HERO ---------- */

    .hero {
        position: relative;
        overflow: hidden;

        padding: 48px;
        border-radius: 28px;

        border: 1px solid rgba(129, 140, 248, 0.18);

        background:
            linear-gradient(
                135deg,
                rgba(30, 41, 59, 0.92),
                rgba(15, 23, 42, 0.78)
            );

        box-shadow:
            0 30px 80px rgba(0, 0, 0, 0.25);

        margin-bottom: 32px;
    }

    .hero::after {
        content: "";
        position: absolute;

        width: 300px;
        height: 300px;

        right: -100px;
        top: -120px;

        border-radius: 50%;

        background:
            radial-gradient(
                circle,
                rgba(99, 102, 241, 0.22),
                transparent 70%
            );
    }

    .hero-label {
        position: relative;
        z-index: 2;

        color: #38bdf8;
        font-size: 11px;
        font-weight: 850;
        letter-spacing: 2.5px;
        margin-bottom: 14px;
    }

    .hero-title {
        position: relative;
        z-index: 2;

        color: #f8fafc;
        font-size: clamp(36px, 5vw, 66px);
        font-weight: 900;
        line-height: 1.02;
        letter-spacing: -3px;
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
        position: relative;
        z-index: 2;

        max-width: 850px;

        margin-top: 20px;

        color: #94a3b8;
        font-size: 15px;
        line-height: 1.8;
    }

    /* ---------- SECTION ---------- */

    .section-title {
        color: #f8fafc;
        font-size: 26px;
        font-weight: 850;
        margin-top: 28px;
    }

    .section-subtitle {
        color: #64748b;
        margin-top: 4px;
        margin-bottom: 20px;
    }

    /* ---------- FEATURE CARDS ---------- */

    .feature-card {
        min-height: 190px;

        padding: 24px;

        border-radius: 20px;

        background:
            linear-gradient(
                145deg,
                rgba(15, 23, 42, 0.82),
                rgba(15, 23, 42, 0.56)
            );

        border: 1px solid rgba(148, 163, 184, 0.11);

        box-shadow:
            0 15px 45px rgba(0, 0, 0, 0.12);

        transition: transform 0.2s ease;
    }

    .feature-icon {
        font-size: 31px;
        margin-bottom: 14px;
    }

    .feature-title {
        color: #f8fafc;
        font-size: 17px;
        font-weight: 800;
        margin-bottom: 9px;
    }

    .feature-description {
        color: #94a3b8;
        font-size: 13px;
        line-height: 1.65;
    }

    /* ---------- METRICS ---------- */

    [data-testid="stMetric"] {
        background:
            rgba(15, 23, 42, 0.75);

        border:
            1px solid rgba(148, 163, 184, 0.12);

        border-radius: 17px;

        padding: 20px;
    }

    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
    }

    [data-testid="stMetricValue"] {
        color: #f8fafc !important;
    }

    /* ---------- BUTTONS ---------- */

    .stButton > button {
        min-height: 44px;

        border-radius: 12px;

        border: 1px solid rgba(129, 140, 248, 0.30);

        background:
            linear-gradient(
                135deg,
                rgba(99, 102, 241, 0.22),
                rgba(56, 189, 248, 0.12)
            );

        color: #f8fafc;

        font-weight: 750;
    }

    .stButton > button:hover {
        border-color: rgba(56, 189, 248, 0.55);
        color: #ffffff;
    }

    /* ---------- INPUTS ---------- */

    textarea,
    input {
        border-radius: 12px !important;
    }

    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;

        color: #475569;

        padding: 40px 0 10px;

        font-size: 12px;

        line-height: 1.8;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# AI SKILL DATABASE
# ============================================================

SKILLS = {
    "Python": ["python"],
    "Java": ["java"],
    "JavaScript": ["javascript", "js"],
    "TypeScript": ["typescript", "ts"],
    "C++": ["c++", "cpp"],
    "C#": ["c#", "c sharp"],
    "SQL": ["sql"],
    "HTML": ["html"],
    "CSS": ["css"],
    "React": ["react", "reactjs"],
    "Angular": ["angular"],
    "Vue": ["vue", "vuejs"],
    "Node.js": ["node.js", "nodejs"],
    "Django": ["django"],
    "Flask": ["flask"],
    "FastAPI": ["fastapi"],
    "Spring Boot": ["spring boot"],
    "Flutter": ["flutter"],
    "Dart": ["dart"],
    "Android": ["android"],
    "iOS": ["ios"],
    "Machine Learning": ["machine learning"],
    "Deep Learning": ["deep learning"],
    "Artificial Intelligence": [
        "artificial intelligence",
        "ai"
    ],
    "NLP": [
        "nlp",
        "natural language processing"
    ],
    "Computer Vision": ["computer vision"],
    "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch"],
    "Scikit-learn": [
        "scikit-learn",
        "sklearn"
    ],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Matplotlib": ["matplotlib"],
    "Data Analysis": [
        "data analysis",
        "data analytics"
    ],
    "Data Science": ["data science"],
    "Statistics": ["statistics"],
    "Power BI": ["power bi"],
    "Tableau": ["tableau"],
    "AWS": [
        "aws",
        "amazon web services"
    ],
    "Azure": ["azure"],
    "Google Cloud": [
        "gcp",
        "google cloud"
    ],
    "Docker": ["docker"],
    "Kubernetes": [
        "kubernetes",
        "k8s"
    ],
    "Git": ["git"],
    "GitHub": ["github"],
    "Linux": ["linux"],
    "MongoDB": [
        "mongodb",
        "mongo db"
    ],
    "PostgreSQL": [
        "postgresql",
        "postgres"
    ],
    "MySQL": ["mysql"],
    "Firebase": ["firebase"],
    "REST API": [
        "rest api",
        "restful api"
    ],
    "GraphQL": ["graphql"],
    "Microservices": ["microservices"],
    "System Design": ["system design"],
    "Cybersecurity": [
        "cybersecurity",
        "cyber security"
    ],
    "Networking": [
        "networking",
        "computer networks"
    ],
    "Agile": ["agile"],
    "Scrum": ["scrum"],
    "Communication": [
        "communication skills"
    ],
    "Leadership": ["leadership"],
    "Problem Solving": [
        "problem solving",
        "problem-solving"
    ],
}


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def clean_text(text: str) -> str:
    if not text:
        return ""

    text = text.replace("\x00", " ")
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_skills(text: str) -> List[str]:
    text_lower = clean_text(text).lower()

    found = []

    for skill, patterns in SKILLS.items():

        for pattern in patterns:

            if pattern in text_lower:
                found.append(skill)
                break

    return sorted(set(found))


def extract_email(text: str):
    match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text or ""
    )

    return match.group(0) if match else None


def extract_phone(text: str):
    match = re.search(
        r"(?:\+?\d[\d\s().-]{7,}\d)",
        text or ""
    )

    return match.group(0).strip() if match else None


def extract_name(text: str) -> str:

    lines = [
        line.strip()
        for line in (text or "").splitlines()
        if line.strip()
    ]

    for line in lines[:10]:

        if "@" in line:
            continue

        lower = line.lower()

        ignored = [
            "resume",
            "curriculum",
            "vitae",
            "profile",
            "objective",
            "email",
            "phone",
        ]

        if any(x in lower for x in ignored):
            continue

        cleaned = re.sub(
            r"[^A-Za-z .'-]",
            "",
            line
        ).strip()

        words = cleaned.split()

        if 2 <= len(words) <= 5:
            return cleaned

    return "Candidate"


# ============================================================
# DOCUMENT EXTRACTION
# ============================================================

def extract_file_text(
    file_bytes: bytes,
    filename: str
) -> str:

    filename = filename.lower()

    try:

        if filename.endswith(".txt"):

            return file_bytes.decode(
                "utf-8",
                errors="ignore"
            )

        if filename.endswith(".pdf"):

            if PdfReader is None:
                return ""

            reader = PdfReader(
                io.BytesIO(file_bytes)
            )

            pages = []

            for page in reader.pages:

                try:
                    pages.append(
                        page.extract_text() or ""
                    )
                except Exception:
                    pass

            return "\n".join(pages)

        if filename.endswith(".docx"):

            if Document is None:
                return ""

            document = Document(
                io.BytesIO(file_bytes)
            )

            return "\n".join(
                paragraph.text
                for paragraph in document.paragraphs
            )

    except Exception:
        return ""

    return ""


# ============================================================
# RESUME AI ENGINE
# ============================================================

def calculate_resume_score(text: str) -> int:

    text = clean_text(text)

    if not text:
        return 0

    score = 0

    skills = extract_skills(text)

    score += min(
        len(skills) * 4,
        30
    )

    if extract_email(text):
        score += 8

    if extract_phone(text):
        score += 5

    sections = [
        "summary",
        "profile",
        "objective",
        "education",
        "experience",
        "projects",
        "certifications",
        "achievements",
    ]

    lower = text.lower()

    for section in sections:

        if section in lower:
            score += 6

    word_count = len(
        text.split()
    )

    if word_count >= 250:
        score += 8

    if word_count >= 500:
        score += 5

    return max(
        0,
        min(100, score)
    )


def calculate_readiness(
    resume_score: int,
    skill_count: int
) -> int:

    return max(
        0,
        min(
            100,
            round(
                resume_score * 0.70
                + min(skill_count * 3, 30)
            )
        )
    )


# ============================================================
# NLP JOB MATCHING
# ============================================================

def calculate_job_match(
    resume_text: str,
    job_text: str
) -> Dict:

    resume_text = clean_text(resume_text)
    job_text = clean_text(job_text)

    if not resume_text or not job_text:

        return {
            "overall": 0,
            "nlp": 0,
            "skills": 0,
            "matched": [],
            "missing": [],
        }

    nlp_score = 0

    try:

        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=5000
        )

        matrix = vectorizer.fit_transform(
            [resume_text, job_text]
        )

        similarity = cosine_similarity(
            matrix[0:1],
            matrix[1:2]
        )[0][0]

        nlp_score = round(
            similarity * 100
        )

    except Exception:
        nlp_score = 0

    resume_skills = set(
        extract_skills(resume_text)
    )

    job_skills = set(
        extract_skills(job_text)
    )

    matched = sorted(
        resume_skills & job_skills
    )

    missing = sorted(
        job_skills - resume_skills
    )

    if job_skills:

        skill_score = round(
            len(matched)
            / len(job_skills)
            * 100
        )

    else:

        skill_score = nlp_score

    overall = round(
        nlp_score * 0.55
        + skill_score * 0.45
    )

    return {
        "overall": min(100, max(0, overall)),
        "nlp": min(100, max(0, nlp_score)),
        "skills": min(100, max(0, skill_score)),
        "matched": matched,
        "missing": missing,
    }


# ============================================================
# JOB FRAUD AI
# ============================================================

FRAUD_PATTERNS = {

    "Financial Requests": [
        "pay a fee",
        "registration fee",
        "processing fee",
        "send money",
        "wire transfer",
        "credit card",
        "payment required",
        "deposit",
    ],

    "Urgency": [
        "act now",
        "urgent",
        "immediately",
        "limited time",
        "today only",
    ],

    "Sensitive Information": [
        "bank details",
        "account number",
        "password",
        "otp",
        "social security",
        "identity document",
    ],

    "Suspicious Communication": [
        "telegram",
        "whatsapp only",
        "crypto",
        "gift card",
        "bitcoin",
        "personal gmail",
    ],
}


def detect_fraud(text: str) -> Dict:

    lower = clean_text(text).lower()

    signals = {}

    for category, patterns in FRAUD_PATTERNS.items():

        matches = [
            pattern
            for pattern in patterns
            if pattern in lower
        ]

        if matches:
            signals[category] = matches

    risk_score = min(
        100,
        sum(
            len(items) * 12
            for items in signals.values()
        )
    )

    if risk_score >= 50:
        level = "HIGH RISK"

    elif risk_score >= 20:
        level = "MEDIUM RISK"

    else:
        level = "LOW RISK"

    return {
        "score": risk_score,
        "level": level,
        "signals": signals,
    }


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "resume_text": "",
    "resume_score": 0,
    "readiness": 0,
    "skills": [],
    "applications": 0,
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">

            <div class="brand-logo">
                🎯
            </div>

            <div class="brand-name">
                Career<span>Lens</span> AI
            </div>

            <div class="brand-subtitle">
                CAREER INTELLIGENCE PLATFORM
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="engine-online">'
        '● AI ENGINE ONLINE'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    workspace = st.radio(
        "WORKSPACE",
        [
            "👨‍💻 Job Seeker",
            "🏢 Recruiter"
        ]
    )


# ============================================================
# JOB SEEKER
# ============================================================

if workspace == "👨‍💻 Job Seeker":

    with st.sidebar:

        module = st.radio(
            "JOB SEEKER MODULES",
            [
                "Dashboard",
                "Resume Intelligence",
                "AI Job Matching",
                "Job Fraud Detection",
                "Skill Gap Analysis",
                "Career Roadmap",
            ]
        )

    # ========================================================
    # DASHBOARD
    # ========================================================

    if module == "Dashboard":

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
                    evaluates opportunities, detects job-risk
                    signals, identifies skill gaps and builds
                    a personalized career intelligence profile.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-title">'
            'Career Overview'
            '</div>',
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
            st.metric(
                "Resume Score",
                (
                    f"{st.session_state.resume_score}/100"
                    if st.session_state.resume_score
                    else "—"
                )
            )

        with c2:
            st.metric(
                "Career Readiness",
                (
                    f"{st.session_state.readiness}%"
                    if st.session_state.readiness
                    else "—"
                )
            )

        with c3:
            st.metric(
                "Skills Detected",
                len(st.session_state.skills)
            )

        with c4:
            st.metric(
                "Applications",
                st.session_state.applications
            )

        st.markdown(
            '<div class="section-title">'
            'Career Intelligence'
            '</div>',
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
                "Extract skills, education, projects and experience from your resume."
            ),
            (
                "🎯",
                "AI Job Matching",
                "Compare your profile with target opportunities using NLP similarity and skill matching."
            ),
            (
                "🛡️",
                "Job Fraud Detection",
                "Detect suspicious financial, urgency and communication signals."
            ),
            (
                "🧩",
                "Skill Gap Analysis",
                "Identify missing skills between your profile and your target career."
            ),
            (
                "🔎",
                "Job Intelligence",
                "Analyze job requirements and identify important skills."
            ),
            (
                "🗺️",
                "Career Roadmap",
                "Create a structured path toward your target role."
            ),
        ]

        columns = st.columns(3)

        for index, feature in enumerate(features):

            icon, title, description = feature

            with columns[index % 3]:

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

    # ========================================================
    # RESUME INTELLIGENCE
    # ========================================================

    elif module == "Resume Intelligence":

        st.title("📄 Resume Intelligence")

        st.caption(
            "AI-powered resume parsing, skill extraction and career scoring."
        )

        uploaded = st.file_uploader(
            "Upload your resume",
            type=["pdf", "docx", "txt"]
        )

        if st.button(
            "Analyze Resume",
            type="primary",
            use_container_width=True
        ):

            if uploaded is None:

                st.warning(
                    "Please upload a resume first."
                )

            else:

                with st.spinner(
                    "CareerLens AI is analyzing your resume..."
                ):

                    text = extract_file_text(
                        uploaded.getvalue(),
                        uploaded.name
                    )

                    text = clean_text(text)

                    if not text:

                        st.error(
                            "No readable text could be extracted from this file."
                        )

                    else:

                        skills = extract_skills(text)

                        score = calculate_resume_score(
                            text
                        )

                        readiness = calculate_readiness(
                            score,
                            len(skills)
                        )

                        st.session_state.resume_text = text
                        st.session_state.resume_score = score
                        st.session_state.readiness = readiness
                        st.session_state.skills = skills

                        st.success(
                            "Resume analysis completed successfully."
                        )

        if st.session_state.resume_text:

            st.divider()

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric(
                    "Resume Score",
                    f"{st.session_state.resume_score}/100"
                )

            with c2:
                st.metric(
                    "Career Readiness",
                    f"{st.session_state.readiness}%"
                )

            with c3:
                st.metric(
                    "Skills Detected",
                    len(st.session_state.skills)
                )

            st.subheader("Candidate Profile")

            st.write(
                extract_name(
                    st.session_state.resume_text
                )
            )

            c1, c2 = st.columns(2)

            with c1:

                st.write(
                    "**Email**"
                )

                st.write(
                    extract_email(
                        st.session_state.resume_text
                    ) or "Not detected"
                )

            with c2:

                st.write(
                    "**Phone**"
                )

                st.write(
                    extract_phone(
                        st.session_state.resume_text
                    ) or "Not detected"
                )

            st.subheader("Detected Skills")

            if st.session_state.skills:

                st.write(
                    " • ".join(
                        st.session_state.skills
                    )
                )

            else:

                st.info(
                    "No recognized skills were detected."
                )

    # ========================================================
    # JOB MATCHING
    # ========================================================

    elif module == "AI Job Matching":

        st.title("🎯 AI Job Matching")

        st.caption(
            "Compare your resume with a target job using NLP and skill alignment."
        )

        job_description = st.text_area(
            "Job Description",
            height=300,
            placeholder="Paste the complete job description here..."
        )

        if st.button(
            "Calculate Match",
            type="primary",
            use_container_width=True
        ):

            if not st.session_state.resume_text:

                st.warning(
                    "Please analyze your resume first."
                )

            elif not job_description.strip():

                st.warning(
                    "Please enter a job description."
                )

            else:

                result = calculate_job_match(
                    st.session_state.resume_text,
                    job_description
                )

                c1, c2, c3 = st.columns(3)

                with c1:
                    st.metric(
                        "Overall Match",
                        f"{result['overall']}%"
                    )

                with c2:
                    st.metric(
                        "NLP Similarity",
                        f"{result['nlp']}%"
                    )

                with c3:
                    st.metric(
                        "Skill Match",
                        f"{result['skills']}%"
                    )

                st.subheader("Matched Skills")

                if result["matched"]:

                    st.success(
                        ", ".join(
                            result["matched"]
                        )
                    )

                else:

                    st.info(
                        "No matching skills detected."
                    )

                st.subheader("Missing Skills")

                if result["missing"]:

                    st.warning(
                        ", ".join(
                            result["missing"]
                        )
                    )

                else:

                    st.success(
                        "No major skill gaps detected."
                    )

    # ========================================================
    # FRAUD DETECTION
    # ========================================================

    elif module == "Job Fraud Detection":

        st.title("🛡️ Job Fraud Detection")

        st.caption(
            "Analyze suspicious signals in job advertisements."
        )

        job_text = st.text_area(
            "Job Advertisement",
            height=320,
            placeholder="Paste the job posting here..."
        )

        if st.button(
            "Analyze Job Risk",
            type="primary",
            use_container_width=True
        ):

            if not job_text.strip():

                st.warning(
                    "Please paste a job advertisement."
                )

            else:

                result = detect_fraud(
                    job_text
                )

                if result["level"] == "HIGH RISK":

                    st.error(
                        f"🚨 HIGH RISK — "
                        f"{result['score']}/100"
                    )

                elif result["level"] == "MEDIUM RISK":

                    st.warning(
                        f"⚠️ MEDIUM RISK — "
                        f"{result['score']}/100"
                    )

                else:

                    st.success(
                        f"✓ LOW RISK — "
                        f"{result['score']}/100"
                    )

                if result["signals"]:

                    st.subheader(
                        "Detected Risk Signals"
                    )

                    for category, signals in result[
                        "signals"
                    ].items():

                        st.write(
                            f"**{category}:** "
                            + ", ".join(signals)
                        )

                else:

                    st.info(
                        "No known high-risk patterns were detected."
                    )

    # ========================================================
    # SKILL GAP
    # ========================================================

    elif module == "Skill Gap Analysis":

        st.title("🧩 Skill Gap Analysis")

        st.caption(
            "Discover what skills you need for your target career."
        )

        target_job = st.text_area(
            "Target Job Description",
            height=300
        )

        if st.button(
            "Analyze Skill Gap",
            type="primary",
            use_container_width=True
        ):

            if not st.session_state.resume_text:

                st.warning(
                    "Please analyze your resume first."
                )

            elif not target_job.strip():

                st.warning(
                    "Please enter a target job description."
                )

            else:

                current = set(
                    st.session_state.skills
                )

                required = set(
                    extract_skills(target_job)
                )

                matched = sorted(
                    current & required
                )

                missing = sorted(
                    required - current
                )

                c1, c2 = st.columns(2)

                with c1:

                    st.subheader(
                        "✓ Current Skills"
                    )

                    if matched:

                        for skill in matched:
                            st.write(
                                f"✓ {skill}"
                            )

                    else:

                        st.info(
                            "No matching skills detected."
                        )

                with c2:

                    st.subheader(
                        "△ Skills to Develop"
                    )

                    if missing:

                        for skill in missing:
                            st.write(
                                f"→ {skill}"
                            )

                    else:

                        st.success(
                            "No major skill gaps detected."
                        )

    # ========================================================
    # CAREER ROADMAP
    # ========================================================

    elif module == "Career Roadmap":

        st.title("🗺️ Career Roadmap")

        st.caption(
            "Build a structured path toward your target role."
        )

        target_role = st.text_input(
            "Target Career",
            placeholder="Example: Data Scientist"
        )

        if st.button(
            "Generate Roadmap",
            type="primary",
            use_container_width=True
        ):

            role = target_role.strip()

            if not role:

                st.warning(
                    "Enter a target career first."
                )

            else:

                st.success(
                    f"Roadmap created for {role}."
                )

                roadmap = [
                    (
                        "01",
                        "Foundation",
                        "Strengthen the fundamentals required for your target role."
                    ),
                    (
                        "02",
                        "Core Skills",
                        "Build the highest-priority technical and professional skills."
                    ),
                    (
                        "03",
                        "Practical Projects",
                        "Create portfolio projects that demonstrate real-world ability."
                    ),
                    (
                        "04",
                        "Interview Preparation",
                        "Prepare technical, behavioral and role-specific interviews."
                    ),
                    (
                        "05",
                        "Career Launch",
                        "Optimize your resume, portfolio and job application strategy."
                    ),
                ]

                for number, title, description in roadmap:

                    st.info(
                        f"**{number} · {title}**\n\n"
                        f"{description}"
                    )


# ============================================================
# RECRUITER WORKSPACE
# ============================================================

else:

    st.markdown(
        """
        <div class="hero">

            <div class="hero-label">
                RECRUITMENT INTELLIGENCE
            </div>

            <div class="hero-title">
                Find the right candidates.
                <br>
                <span class="hero-gradient">
                    Faster and smarter.
                </span>
            </div>

            <div class="hero-description">
                CareerLens AI compares candidate resumes
                against a target job using NLP similarity,
                skill alignment and recruiter-controlled
                Top-N ranking.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.title("🏢 Recruiter Screening")

    job_description = st.text_area(
        "Target Job Description",
        height=280
    )

    resumes = st.file_uploader(
        "Upload Candidate Resumes",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True
    )

    top_n = st.number_input(
        "Recruiter Top-N",
        min_value=1,
        max_value=500,
        value=10
    )

    if st.button(
        "Run AI Screening",
        type="primary",
        use_container_width=True
    ):

        if not job_description.strip():

            st.warning(
                "Enter a target job description."
            )

        elif not resumes:

            st.warning(
                "Upload candidate resumes."
            )

        else:

            results = []

            progress = st.progress(0)

            for index, resume in enumerate(resumes):

                text = extract_file_text(
                    resume.getvalue(),
                    resume.name
                )

                text = clean_text(text)

                match = calculate_job_match(
                    text,
                    job_description
                )

                results.append(
                    {
                        "Candidate": extract_name(text),
                        "Email": extract_email(text) or "",
                        "Resume Score": calculate_resume_score(text),
                        "NLP Match": match["nlp"],
                        "Skill Match": match["skills"],
                        "Overall Match": match["overall"],
                        "Skills": ", ".join(
                            extract_skills(text)
                        ),
                        "Missing Skills": ", ".join(
                            match["missing"]
                        ),
                    }
                )

                progress.progress(
                    (index + 1) / len(resumes)
                )

            dataframe = pd.DataFrame(
                results
            )

            dataframe = dataframe.sort_values(
                "Overall Match",
                ascending=False
            )

            dataframe.insert(
                0,
                "Rank",
                range(
                    1,
                    len(dataframe) + 1
                )
            )

            shortlist = dataframe.head(
                int(top_n)
            )

            st.success(
                f"Screened {len(dataframe)} candidates."
            )

            st.subheader(
                f"Top {len(shortlist)} Candidates"
            )

            st.dataframe(
                shortlist,
                use_container_width=True,
                hide_index=True
            )

            csv = shortlist.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                "Download Shortlist CSV",
                csv,
                "careerlens_shortlist.csv",
                "text/csv",
                use_container_width=True
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        🎯 <b>CareerLens AI</b><br>
        AI-Powered Career Intelligence & Recruitment Platform<br>
        Final Year Project · Artificial Intelligence · Machine Learning · NLP
    </div>
    """,
    unsafe_allow_html=True
)
```
