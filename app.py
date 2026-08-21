import io
import re
from typing import Optional, List, Dict

import pandas as pd
import streamlit as st

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

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
# FASTAPI BACKEND
# ============================================================

api = FastAPI(
    title="CareerLens AI API",
    description="AI-powered career intelligence and recruitment API",
    version="1.0.0",
)

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
        "artificial intelligence"
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
# TEXT PROCESSING
# ============================================================

def clean_text(text: str) -> str:
    if not text:
        return ""

    text = text.replace("\x00", " ")
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_skills(text: str) -> List[str]:

    text = clean_text(text).lower()

    found = []

    for skill, patterns in SKILLS.items():

        for pattern in patterns:

            if pattern in text:
                found.append(skill)
                break

    return sorted(set(found))


def extract_email(text: str) -> Optional[str]:

    match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text or ""
    )

    return match.group(0) if match else None


def extract_phone(text: str) -> Optional[str]:

    match = re.search(
        r"(?:\+?\d[\d\s().-]{7,}\d)",
        text or ""
    )

    return match.group(0).strip() if match else None


def extract_name(text: str) -> str:

    lines = [
        x.strip()
        for x in (text or "").splitlines()
        if x.strip()
    ]

    for line in lines[:10]:

        if "@" in line:
            continue

        if any(
            word in line.lower()
            for word in [
                "resume",
                "curriculum",
                "vitae",
                "profile",
                "objective",
                "email",
                "phone",
            ]
        ):
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
# FILE EXTRACTION
# ============================================================

def extract_file_text(file_bytes: bytes, filename: str) -> str:

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
# RESUME AI
# ============================================================

def resume_score(text: str) -> int:

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

    for section in sections:

        if section in text.lower():
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


def career_readiness(
    score: int,
    skill_count: int
) -> int:

    return max(
        0,
        min(
            100,
            round(
                score * 0.7
                + min(skill_count * 3, 30)
            )
        )
    )


# ============================================================
# NLP JOB MATCHING
# ============================================================

def job_match(
    resume: str,
    job: str
) -> Dict:

    resume = clean_text(resume)
    job = clean_text(job)

    if not resume or not job:

        return {
            "overall_match": 0,
            "nlp_similarity": 0,
            "skill_match": 0,
            "matched_skills": [],
            "missing_skills": [],
        }

    try:

        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=5000
        )

        matrix = vectorizer.fit_transform(
            [resume, job]
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
        extract_skills(resume)
    )

    job_skills = set(
        extract_skills(job)
    )

    matched = sorted(
        resume_skills.intersection(
            job_skills
        )
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
        "overall_match": min(
            100,
            max(0, overall)
        ),
        "nlp_similarity": min(
            100,
            max(0, nlp_score)
        ),
        "skill_match": min(
            100,
            max(0, skill_score)
        ),
        "matched_skills": matched,
        "missing_skills": missing,
    }


# ============================================================
# FRAUD DETECTION
# ============================================================

FRAUD_PATTERNS = {

    "Financial Requests": [
        "pay a fee",
        "registration fee",
        "processing fee",
        "send money",
        "wire transfer",
        "bank account",
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

    "Personal Information": [
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


def fraud_detection(text: str) -> Dict:

    text = clean_text(text).lower()

    signals = {}

    for category, patterns in FRAUD_PATTERNS.items():

        hits = [
            p
            for p in patterns
            if p in text
        ]

        if hits:
            signals[category] = hits

    risk_score = min(
        100,
        sum(
            len(v) * 12
            for v in signals.values()
        )
    )

    if risk_score >= 50:
        level = "HIGH RISK"

    elif risk_score >= 20:
        level = "MEDIUM RISK"

    else:
        level = "LOW RISK"

    return {
        "risk_score": risk_score,
        "risk_level": level,
        "signals": signals,
    }


# ============================================================
# API ROUTES
# ============================================================

@api.get("/")
def root():

    return {
        "application": "CareerLens AI",
        "status": "online",
        "version": "1.0.0",
    }


@api.get("/health")
def health():

    return {
        "status": "healthy",
        "ai_engine": "online",
    }


@api.post("/api/resume/analyze")
async def analyze_resume_api(
    file: UploadFile = File(...)
):

    content = await file.read()

    text = extract_file_text(
        content,
        file.filename or ""
    )

    text = clean_text(text)

    if not text:

        return {
            "success": False,
            "message": "Could not extract text from resume.",
        }

    skills = extract_skills(text)
    score = resume_score(text)

    return {
        "success": True,
        "candidate": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "resume_score": score,
        "career_readiness": career_readiness(
            score,
            len(skills)
        ),
        "skills": skills,
    }


@api.post("/api/job/match")
async def job_match_api(
    resume_text: str = Form(...),
    job_description: str = Form(...)
):

    return {
        "success": True,
        **job_match(
            resume_text,
            job_description
        )
    }


@api.post("/api/job/fraud")
async def fraud_api(
    job_description: str = Form(...)
):

    return {
        "success": True,
        **fraud_detection(
            job_description
        )
    }


@api.post("/api/career/analyze")
async def career_analyze_api(
    resume_text: str = Form(...),
    job_description: str = Form(...)
):

    match = job_match(
        resume_text,
        job_description
    )

    score = resume_score(
        resume_text
    )

    skills = extract_skills(
        resume_text
    )

    return {
        "success": True,
        "resume_score": score,
        "career_readiness": career_readiness(
            score,
            len(skills)
        ),
        "skills": skills,
        "job_match": match,
    }


# ============================================================
# STREAMLIT UI
# ============================================================

def run_streamlit_app():

    st.set_page_config(
        page_title="CareerLens AI",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # --------------------------------------------------------
    # CSS
    # --------------------------------------------------------

    st.markdown(
        """
        <style>

        .stApp {
            background:
                radial-gradient(
                    circle at 10% 0%,
                    rgba(99,102,241,.14),
                    transparent 30%
                ),
                radial-gradient(
                    circle at 90% 10%,
                    rgba(56,189,248,.10),
                    transparent 28%
                ),
                #07101f;
            color: #e5e7eb;
        }

        [data-testid="stSidebar"] {
            background: #091426;
            border-right: 1px solid rgba(148,163,184,.12);
        }

        .block-container {
            max-width: 1450px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        h1,h2,h3,h4 {
            color:#f8fafc !important;
        }

        .brand {
            text-align:center;
            padding:10px 0 22px;
        }

        .brand-icon {
            font-size:48px;
        }

        .brand-name {
            font-size:27px;
            font-weight:800;
            color:#f8fafc;
        }

        .brand-name span {
            color:#7c8cff;
        }

        .brand-subtitle {
            color:#64748b;
            font-size:10px;
            letter-spacing:2px;
        }

        .online {
            color:#4ade80;
            font-size:12px;
            font-weight:700;
            text-align:center;
        }

        .hero {
            padding:42px;
            border-radius:25px;
            border:1px solid rgba(129,140,248,.18);
            background:
                linear-gradient(
                    135deg,
                    rgba(30,41,59,.92),
                    rgba(15,23,42,.72)
                );
            box-shadow:0 25px 70px rgba(0,0,0,.25);
            margin-bottom:30px;
        }

        .hero-label {
            color:#38bdf8;
            font-size:12px;
            font-weight:800;
            letter-spacing:2px;
            margin-bottom:12px;
        }

        .hero-title {
            color:#f8fafc;
            font-size:clamp(34px,5vw,64px);
            font-weight:850;
            line-height:1.05;
            letter-spacing:-3px;
        }

        .hero-gradient {
            background:
                linear-gradient(
                    90deg,
                    #8b7cff,
                    #38bdf8
                );
            -webkit-background-clip:text;
            -webkit-text-fill-color:transparent;
        }

        .hero-text {
            max-width:850px;
            color:#94a3b8;
            font-size:16px;
            line-height:1.8;
            margin-top:18px;
        }

        .card {
            background:rgba(15,23,42,.68);
            border:1px solid rgba(148,163,184,.12);
            border-radius:18px;
            padding:22px;
            min-height:155px;
            margin-bottom:14px;
        }

        .card-icon {
            font-size:30px;
            margin-bottom:12px;
        }

        .card-title {
            color:#f8fafc;
            font-size:17px;
            font-weight:750;
            margin-bottom:8px;
        }

        .card-text {
            color:#94a3b8;
            font-size:13px;
            line-height:1.6;
        }

        .section-title {
            color:#f8fafc;
            font-size:25px;
            font-weight:800;
            margin-top:28px;
        }

        .section-subtitle {
            color:#64748b;
            margin-bottom:18px;
        }

        .stButton > button {
            border-radius:12px;
            border:1px solid rgba(99,102,241,.30);
            background:
                linear-gradient(
                    135deg,
                    rgba(99,102,241,.18),
                    rgba(56,189,248,.10)
                );
            color:#f8fafc;
            font-weight:600;
        }

        [data-testid="stMetric"] {
            background:rgba(15,23,42,.72);
            border:1px solid rgba(148,163,184,.12);
            border-radius:16px;
            padding:18px;
        }

        .footer {
            text-align:center;
            color:#475569;
            padding:35px 0 10px;
            font-size:12px;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # SESSION STATE
    # --------------------------------------------------------

    if "resume_text" not in st.session_state:
        st.session_state.resume_text = ""

    if "resume_score" not in st.session_state:
        st.session_state.resume_score = 0

    if "skills" not in st.session_state:
        st.session_state.skills = []

    if "readiness" not in st.session_state:
        st.session_state.readiness = 0

    if "applications" not in st.session_state:
        st.session_state.applications = 0

    # --------------------------------------------------------
    # SIDEBAR
    # --------------------------------------------------------

    st.sidebar.markdown(
        """
        <div class="brand">
            <div class="brand-icon">🎯</div>

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

    st.sidebar.markdown(
        '<div class="online">● AI ENGINE ONLINE</div>',
        unsafe_allow_html=True,
    )

    st.sidebar.divider()

    workspace = st.sidebar.radio(
        "WORKSPACE",
        [
            "👨‍💻 Job Seeker",
            "🏢 Recruiter",
        ],
    )

    # --------------------------------------------------------
    # JOB SEEKER
    # --------------------------------------------------------

    if workspace == "👨‍💻 Job Seeker":

        module = st.sidebar.radio(
            "JOB SEEKER MODULES",
            [
                "Dashboard",
                "Resume Intelligence",
                "AI Job Matching",
                "Job Fraud Detection",
                "Skill Gap Analysis",
                "Career Roadmap",
            ],
        )

        # ----------------------------------------------------
        # DASHBOARD
        # ----------------------------------------------------

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

                    <div class="hero-text">
                        CareerLens AI brings resume intelligence,
                        job matching, fraud-risk analysis,
                        skill-gap detection and career planning
                        into one professional workspace.
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
                '<div class="section-subtitle">'
                'Your career intelligence at a glance.'
                '</div>',
                unsafe_allow_html=True,
            )

            a, b, c, d = st.columns(4)

            with a:
                st.metric(
                    "Resume Score",
                    (
                        f"{st.session_state.resume_score}/100"
                        if st.session_state.resume_score
                        else "—"
                    )
                )

            with b:
                st.metric(
                    "Career Readiness",
                    (
                        f"{st.session_state.readiness}%"
                        if st.session_state.readiness
                        else "—"
                    )
                )

            with c:
                st.metric(
                    "Skills Detected",
                    len(st.session_state.skills)
                )

            with d:
                st.metric(
                    "Applications",
                    st.session_state.applications
                )

            st.markdown(
                '<div class="section-title">'
                'Career Intelligence'
                '</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                '<div class="section-subtitle">'
                'AI-powered tools for smarter career decisions.'
                '</div>',
                unsafe_allow_html=True,
            )

            cards = [
                (
                    "📄",
                    "Resume Intelligence",
                    "Analyze your resume and extract skills, education, projects and experience."
                ),
                (
                    "🎯",
                    "AI Job Matching",
                    "Compare your profile against job descriptions using NLP and skill matching."
                ),
                (
                    "🛡️",
                    "Job Fraud Detection",
                    "Detect suspicious financial, urgency and communication signals."
                ),
                (
                    "🧩",
                    "Skill Gap Analysis",
                    "Identify missing skills between your profile and target role."
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
                ),
            ]

            columns = st.columns(3)

            for i, card in enumerate(cards):

                icon, title, description = card

                with columns[i % 3]:

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
                        unsafe_allow_html=True,
                    )

        # ----------------------------------------------------
        # RESUME
        # ----------------------------------------------------

        elif module == "Resume Intelligence":

            st.title("📄 Resume Intelligence")

            st.caption(
                "AI-powered resume parsing and career scoring."
            )

            file = st.file_uploader(
                "Upload your resume",
                type=["pdf", "docx", "txt"]
            )

            if st.button(
                "Analyze Resume",
                type="primary",
                use_container_width=True
            ):

                if not file:

                    st.warning(
                        "Please upload a resume first."
                    )

                else:

                    with st.spinner(
                        "AI engine analyzing resume..."
                    ):

                        text = extract_file_text(
                            file.getvalue(),
                            file.name
                        )

                        text = clean_text(text)

                        if not text:

                            st.error(
                                "Unable to extract readable text from this file."
                            )

                        else:

                            skills = extract_skills(text)

                            score = resume_score(text)

                            readiness = career_readiness(
                                score,
                                len(skills)
                            )

                            st.session_state.resume_text = text
                            st.session_state.resume_score = score
                            st.session_state.skills = skills
                            st.session_state.readiness = readiness

                            st.success(
                                "Resume analysis completed."
                            )

            if st.session_state.resume_text:

                st.divider()

                a, b, c = st.columns(3)

                with a:
                    st.metric(
                        "Resume Score",
                        f"{st.session_state.resume_score}/100"
                    )

                with b:
                    st.metric(
                        "Career Readiness",
                        f"{st.session_state.readiness}%"
                    )

                with c:
                    st.metric(
                        "Skills Detected",
                        len(st.session_state.skills)
                    )

                st.subheader("Candidate")

                st.write(
                    extract_name(
                        st.session_state.resume_text
                    )
                )

                st.subheader("Contact")

                x, y = st.columns(2)

                with x:
                    st.write(
                        "Email:",
                        extract_email(
                            st.session_state.resume_text
                        ) or "Not detected"
                    )

                with y:
                    st.write(
                        "Phone:",
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
                        "No recognized skills detected."
                    )

        # ----------------------------------------------------
        # JOB MATCHING
        # ----------------------------------------------------

        elif module == "AI Job Matching":

            st.title("🎯 AI Job Matching")

            job = st.text_area(
                "Paste Job Description",
                height=300
            )

            if st.button(
                "Calculate Match",
                type="primary",
                use_container_width=True
            ):

                if not st.session_state.resume_text:

                    st.warning(
                        "Analyze your resume first."
                    )

                elif not job.strip():

                    st.warning(
                        "Enter a job description."
                    )

                else:

                    result = job_match(
                        st.session_state.resume_text,
                        job
                    )

                    a, b, c = st.columns(3)

                    with a:
                        st.metric(
                            "Overall Match",
                            f"{result['overall_match']}%"
                        )

                    with b:
                        st.metric(
                            "NLP Similarity",
                            f"{result['nlp_similarity']}%"
                        )

                    with c:
                        st.metric(
                            "Skill Match",
                            f"{result['skill_match']}%"
                        )

                    st.subheader(
                        "Matched Skills"
                    )

                    st.write(
                        ", ".join(
                            result["matched_skills"]
                        )
                        or "None"
                    )

                    st.subheader(
                        "Missing Skills"
                    )

                    st.write(
                        ", ".join(
                            result["missing_skills"]
                        )
                        or "None"
                    )

        # ----------------------------------------------------
        # FRAUD
        # ----------------------------------------------------

        elif module == "Job Fraud Detection":

            st.title("🛡️ Job Fraud Detection")

            text = st.text_area(
                "Paste Job Advertisement",
                height=300
            )

            if st.button(
                "Analyze Risk",
                type="primary",
                use_container_width=True
            ):

                if not text.strip():

                    st.warning(
                        "Paste a job advertisement first."
                    )

                else:

                    result = fraud_detection(
                        text
                    )

                    if result["risk_level"] == "HIGH RISK":

                        st.error(
                            f"HIGH RISK — "
                            f"{result['risk_score']}/100"
                        )

                    elif result["risk_level"] == "MEDIUM RISK":

                        st.warning(
                            f"MEDIUM RISK — "
                            f"{result['risk_score']}/100"
                        )

                    else:

                        st.success(
                            f"LOW RISK — "
                            f"{result['risk_score']}/100"
                        )

                    for category, signals in result[
                        "signals"
                    ].items():

                        st.write(
                            f"**{category}:** "
                            + ", ".join(signals)
                        )

        # ----------------------------------------------------
        # SKILL GAP
        # ----------------------------------------------------

        elif module == "Skill Gap Analysis":

            st.title("🧩 Skill Gap Analysis")

            target = st.text_area(
                "Paste Target Job Description",
                height=300
            )

            if st.button(
                "Analyze Skill Gap",
                type="primary",
                use_container_width=True
            ):

                if not st.session_state.resume_text:

                    st.warning(
                        "Analyze your resume first."
                    )

                elif not target.strip():

                    st.warning(
                        "Enter the target job description."
                    )

                else:

                    current = set(
                        st.session_state.skills
                    )

                    required = set(
                        extract_skills(target)
                    )

                    matched = sorted(
                        current & required
                    )

                    missing = sorted(
                        required - current
                    )

                    a, b = st.columns(2)

                    with a:

                        st.subheader(
                            "Your Skills"
                        )

                        st.write(
                            ", ".join(
                                sorted(current)
                            )
                            or "None"
                        )

                    with b:

                        st.subheader(
                            "Missing Skills"
                        )

                        st.write(
                            ", ".join(
                                missing
                            )
                            or "No major skill gaps detected"
                        )

        # ----------------------------------------------------
        # ROADMAP
        # ----------------------------------------------------

        elif module == "Career Roadmap":

            st.title("🗺️ Career Roadmap")

            role = st.text_input(
                "Target Role",
                placeholder="Example: Data Scientist"
            )

            if st.button(
                "Generate Roadmap",
                type="primary",
                use_container_width=True
            ):

                st.success(
                    f"Career roadmap generated for "
                    f"{role or 'your target role'}."
                )

                stages = [
                    (
                        "01",
                        "Foundation",
                        "Strengthen fundamental concepts."
                    ),
                    (
                        "02",
                        "Skill Development",
                        "Learn the highest-priority technical skills."
                    ),
                    (
                        "03",
                        "Projects",
                        "Build practical portfolio projects."
                    ),
                    (
                        "04",
                        "Interview Preparation",
                        "Prepare technical and behavioral interviews."
                    ),
                    (
                        "05",
                        "Career Launch",
                        "Optimize your resume and apply strategically."
                    ),
                ]

                for number, title, description in stages:

                    st.info(
                        f"**{number} — {title}**\n\n"
                        f"{description}"
                    )

    # --------------------------------------------------------
    # RECRUITER
    # --------------------------------------------------------

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

                <div class="hero-text">
                    CareerLens AI helps recruiters compare
                    candidate resumes against a target job,
                    calculate NLP similarity, measure skill
                    alignment and create a recruiter-controlled
                    Top-N shortlist.
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        st.subheader(
            "Bulk Candidate Screening"
        )

        job = st.text_area(
            "Target Job Description",
            height=280
        )

        files = st.file_uploader(
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

            if not job.strip():

                st.warning(
                    "Enter a target job description."
                )

            elif not files:

                st.warning(
                    "Upload candidate resumes."
                )

            else:

                results = []

                progress = st.progress(0)

                for i, file in enumerate(files):

                    text = extract_file_text(
                        file.getvalue(),
                        file.name
                    )

                    text = clean_text(text)

                    result = job_match(
                        text,
                        job
                    )

                    results.append(
                        {
                            "Candidate": extract_name(text),
                            "Email": extract_email(text) or "",
                            "Resume Score": resume_score(text),
                            "NLP Match": result[
                                "nlp_similarity"
                            ],
                            "Skill Match": result[
                                "skill_match"
                            ],
                            "Overall Match": result[
                                "overall_match"
                            ],
                            "Skills": ", ".join(
                                extract_skills(text)
                            ),
                            "Missing Skills": ", ".join(
                                result[
                                    "missing_skills"
                                ]
                            ),
                        }
                    )

                    progress.progress(
                        (i + 1) / len(files)
                    )

                df = pd.DataFrame(
                    results
                )

                df = df.sort_values(
                    "Overall Match",
                    ascending=False
                )

                df.insert(
                    0,
                    "Rank",
                    range(
                        1,
                        len(df) + 1
                    )
                )

                shortlist = df.head(
                    int(top_n)
                )

                st.success(
                    f"Screened {len(df)} candidates."
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
                    "CareerLens_Shortlist.csv",
                    "text/csv",
                    use_container_width=True
                )

    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="footer">
            🎯 CareerLens AI<br>
            AI-Powered Career Intelligence & Recruitment Platform<br>
            Final Year Project · Artificial Intelligence · Machine Learning · NLP
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# STREAMLIT ENTRY POINT
# ============================================================

if __name__ == "__main__":
    run_streamlit_app()
