import io
import re

import pandas as pd
import streamlit as st
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
# CAREERLENS AI
# Single-file AI Career Intelligence & Recruitment Platform
# ============================================================

st.set_page_config(
    page_title="CareerLens AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PROFESSIONAL UI
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background: #07111f;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 30px;
        padding-bottom: 60px;
    }

    [data-testid="stSidebar"] {
        background: #081526;
        border-right: 1px solid #1c3049;
    }

    h1, h2, h3 {
        color: #f8fafc !important;
    }

    p, label {
        color: #aebdd0;
    }

    .brand {
        font-size: 30px;
        font-weight: 800;
        color: white;
        letter-spacing: -1px;
    }

    .brand span {
        color: #8b7cff;
    }

    .brand-subtitle {
        font-size: 10px;
        color: #71849d;
        letter-spacing: 2px;
        margin-top: 3px;
    }

    .status {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 999px;
        background: #09261d;
        border: 1px solid #1c6548;
        color: #4ade80;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1px;
    }

    .hero {
        background: linear-gradient(
            135deg,
            #0e1f37,
            #0b1728
        );
        border: 1px solid #29425f;
        border-radius: 24px;
        padding: 42px;
        margin-bottom: 30px;
    }

    .hero-kicker {
        color: #38bdf8;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 2.5px;
    }

    .hero-title {
        color: white;
        font-size: 48px;
        font-weight: 850;
        line-height: 1.08;
        margin-top: 12px;
    }

    .hero-gradient {
        color: #8b7cff;
    }

    .hero-text {
        color: #aebdd0;
        max-width: 850px;
        font-size: 16px;
        line-height: 1.75;
        margin-top: 15px;
    }

    .feature-card {
        background: #0c192b;
        border: 1px solid #203754;
        border-radius: 17px;
        padding: 22px;
        min-height: 145px;
        margin-bottom: 18px;
    }

    .feature-icon {
        font-size: 27px;
    }

    .feature-title {
        color: white;
        font-size: 17px;
        font-weight: 750;
        margin-top: 8px;
    }

    .feature-text {
        color: #8fa2ba;
        font-size: 13px;
        line-height: 1.55;
        margin-top: 7px;
    }

    div[data-testid="stMetric"] {
        background: #0c192b;
        border: 1px solid #203754;
        border-radius: 16px;
        padding: 18px;
    }

    div[data-testid="stMetricValue"] {
        color: white !important;
    }

    div[data-testid="stMetricLabel"] {
        color: #8fa2ba !important;
    }

    .section-note {
        color: #7f93ab;
        font-size: 13px;
    }

    .risk-high {
        color: #fb7185;
        font-weight: 800;
    }

    .risk-medium {
        color: #fbbf24;
        font-weight: 800;
    }

    .risk-low {
        color: #4ade80;
        font-weight: 800;
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
    st.session_state.applications = 0

if "recruiter_results" not in st.session_state:
    st.session_state.recruiter_results = None


# ============================================================
# SKILL KNOWLEDGE BASE
# ============================================================

SKILLS = {
    "Python": ["python"],
    "Java": ["java"],
    "JavaScript": ["javascript", "js"],
    "TypeScript": ["typescript", "ts"],
    "React": ["react", "react.js", "reactjs"],
    "Node.js": ["node.js", "nodejs", "node js"],
    "SQL": ["sql", "mysql", "postgresql", "postgres"],
    "MongoDB": ["mongodb", "mongo db", "mongo"],
    "Machine Learning": [
        "machine learning",
        "machine-learning",
    ],
    "Deep Learning": [
        "deep learning",
        "deep-learning",
    ],
    "NLP": [
        "nlp",
        "natural language processing",
    ],
    "Computer Vision": [
        "computer vision",
        "opencv",
    ],
    "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch"],
    "Scikit-learn": [
        "scikit-learn",
        "sklearn",
    ],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Data Analysis": [
        "data analysis",
        "data analytics",
    ],
    "Data Science": ["data science"],
    "Power BI": [
        "power bi",
        "powerbi",
    ],
    "Tableau": ["tableau"],
    "Excel": [
        "excel",
        "microsoft excel",
    ],
    "AWS": [
        "aws",
        "amazon web services",
    ],
    "Azure": [
        "azure",
        "microsoft azure",
    ],
    "GCP": [
        "gcp",
        "google cloud",
    ],
    "Docker": ["docker"],
    "Kubernetes": [
        "kubernetes",
        "k8s",
    ],
    "Git": [
        "git",
        "github",
        "gitlab",
    ],
    "Linux": ["linux"],
    "REST API": [
        "rest api",
        "restful api",
        "rest apis",
    ],
    "FastAPI": [
        "fastapi",
        "fast api",
    ],
    "Flask": ["flask"],
    "Django": ["django"],
    "Spring Boot": ["spring boot"],
    "C++": [
        "c++",
        "cpp",
    ],
    "C#": [
        "c#",
        "c sharp",
    ],
    ".NET": [
        ".net",
        "dotnet",
    ],
    "HTML": [
        "html",
        "html5",
    ],
    "CSS": [
        "css",
        "css3",
    ],
    "Figma": ["figma"],
    "UI/UX": [
        "ui/ux",
        "ui ux",
    ],
    "Agile": [
        "agile",
        "scrum",
    ],
    "Communication": [
        "communication",
    ],
    "Leadership": [
        "leadership",
    ],
    "Problem Solving": [
        "problem solving",
        "problem-solving",
    ],
}


# ============================================================
# FRAUD SIGNALS
# ============================================================

FRAUD_RULES = {
    "Payment Request": [
        "pay a fee",
        "registration fee",
        "processing fee",
        "training fee",
        "security deposit",
        "send money",
        "payment required",
        "pay to apply",
    ],
    "Financial Information": [
        "bank account",
        "bank details",
        "credit card",
        "debit card",
        "otp",
        "one time password",
        "wallet",
        "crypto",
        "cryptocurrency",
    ],
    "Urgency Pressure": [
        "act now",
        "urgent",
        "immediately",
        "within 24 hours",
        "limited slots",
        "last chance",
        "today only",
    ],
    "Suspicious Communication": [
        "whatsapp only",
        "telegram only",
        "contact on telegram",
        "contact on whatsapp",
        "personal gmail",
    ],
    "Guaranteed Claims": [
        "guaranteed job",
        "100% placement",
        "guaranteed placement",
        "no interview required",
    ],
}


# ============================================================
# TEXT PROCESSING
# ============================================================

def normalize(text):
    return re.sub(
        r"\s+",
        " ",
        str(text).lower(),
    ).strip()


def extract_pdf(data):
    if PdfReader is None:
        return ""

    try:
        reader = PdfReader(
            io.BytesIO(data)
        )

        pages = []

        for page in reader.pages:
            pages.append(
                page.extract_text() or ""
            )

        return "\n".join(pages)

    except Exception:
        return ""


def extract_docx(data):
    if Document is None:
        return ""

    try:
        document = Document(
            io.BytesIO(data)
        )

        return "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

    except Exception:
        return ""


def extract_text(uploaded_file):

    if uploaded_file is None:
        return ""

    data = uploaded_file.getvalue()

    extension = (
        uploaded_file.name
        .lower()
        .split(".")[-1]
    )

    if extension == "txt":

        return data.decode(
            "utf-8",
            errors="ignore",
        )

    if extension == "pdf":

        return extract_pdf(data)

    if extension == "docx":

        return extract_docx(data)

    return ""


# ============================================================
# AI RESUME ENGINE
# ============================================================

def detect_skills(text):

    text = normalize(text)

    detected = []

    for skill, aliases in SKILLS.items():

        for alias in aliases:

            pattern = (
                r"(?<![a-z0-9])"
                + re.escape(alias.lower())
                + r"(?![a-z0-9])"
            )

            if re.search(
                pattern,
                text,
            ):

                detected.append(skill)
                break

    return sorted(
        set(detected)
    )


def extract_email(text):

    match = re.search(
        r"[\w.+-]+@[\w-]+\.[\w.-]+",
        text,
    )

    if match:
        return match.group(0)

    return "Not detected"


def extract_phone(text):

    match = re.search(
        r"(?:\+?\d[\d\s().-]{8,}\d)",
        text,
    )

    if match:
        return match.group(0).strip()

    return "Not detected"


def extract_name(text):

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    for line in lines[:10]:

        words = line.split()

        if (
            2 <= len(words) <= 5
            and "@" not in line
            and not re.search(
                r"\d",
                line,
            )
            and len(line) < 60
        ):

            return line.title()

    return "Candidate"


def calculate_resume_score(
    text,
    skills,
):

    lower = normalize(text)

    score = 0

    if len(text) >= 300:
        score += 15

    if extract_email(text) != "Not detected":
        score += 10

    if extract_phone(text) != "Not detected":
        score += 5

    score += min(
        len(skills) * 3,
        30,
    )

    education_terms = [
        "b.tech",
        "btech",
        "bachelor",
        "master",
        "degree",
        "engineering",
        "computer science",
    ]

    if any(
        term in lower
        for term in education_terms
    ):
        score += 15

    if "experience" in lower:
        score += 10

    if "project" in lower:
        score += 5

    if (
        "github" in lower
        or "linkedin" in lower
    ):
        score += 5

    return min(
        score,
        100,
    )


def calculate_readiness(
    resume_score,
    skills,
):

    return min(
        100,
        round(
            resume_score * 0.7
            + min(
                len(skills) * 4,
                30,
            )
        ),
    )


# ============================================================
# NLP MATCHING ENGINE
# ============================================================

def calculate_nlp_similarity(
    profile,
    job,
):

    if (
        not profile.strip()
        or not job.strip()
    ):
        return 0

    try:

        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
        )

        matrix = vectorizer.fit_transform(
            [
                normalize(profile),
                normalize(job),
            ]
        )

        similarity = cosine_similarity(
            matrix[0:1],
            matrix[1:2],
        )[0][0]

        return float(
            similarity
        )

    except Exception:

        return 0


def calculate_job_match(
    profile,
    job,
):

    profile_skills = set(
        detect_skills(profile)
    )

    job_skills = set(
        detect_skills(job)
    )

    nlp = calculate_nlp_similarity(
        profile,
        job,
    )

    if job_skills:

        skill_match = (
            len(
                profile_skills
                & job_skills
            )
            / len(job_skills)
        )

    else:

        skill_match = 0

    overall = (
        nlp * 0.55
        + skill_match * 0.45
    )

    return {
        "overall": min(
            round(overall * 100),
            100,
        ),
        "nlp": min(
            round(nlp * 100),
            100,
        ),
        "skill": min(
            round(skill_match * 100),
            100,
        ),
        "missing": sorted(
            job_skills
            - profile_skills
        ),
    }


# ============================================================
# FRAUD ENGINE
# ============================================================

def analyze_fraud(
    job_text,
):

    text = normalize(
        job_text
    )

    details = {}

    for category, phrases in FRAUD_RULES.items():

        matches = [
            phrase
            for phrase in phrases
            if phrase in text
        ]

        if matches:
            details[category] = matches

    signal_count = sum(
        len(values)
        for values in details.values()
    )

    score = min(
        signal_count * 15,
        100,
    )

    if score >= 60:
        level = "HIGH RISK"

    elif score >= 30:
        level = "MEDIUM RISK"

    else:
        level = "LOW RISK"

    return {
        "score": score,
        "level": level,
        "details": details,
    }


# ============================================================
# UI HELPERS
# ============================================================

def metric_cards(items):

    columns = st.columns(
        len(items)
    )

    for column, item in zip(
        columns,
        items,
    ):

        label, value, help_text = item

        with column:

            st.metric(
                label,
                value,
                help=help_text,
            )


def show_feature_cards():

    features = [
        (
            "📄",
            "Resume Intelligence",
            "Extract skills, education, experience and profile signals.",
        ),
        (
            "🎯",
            "AI Job Matching",
            "Combine NLP similarity with skill alignment.",
        ),
        (
            "🛡️",
            "Job Fraud Detection",
            "Identify suspicious payment, urgency and communication signals.",
        ),
        (
            "🧩",
            "Skill Gap Analysis",
            "Discover missing skills for your target opportunity.",
        ),
        (
            "🔎",
            "Job Intelligence",
            "Understand requirements and important capabilities.",
        ),
        (
            "🗺️",
            "Career Roadmap",
            "Turn career gaps into an actionable development path.",
        ),
    ]

    columns = st.columns(3)

    for index, feature in enumerate(
        features
    ):

        icon, title, description = feature

        with columns[
            index % 3
        ]:

            st.markdown(
                f"""
                <div class="feature-card">
                    <div class="feature-icon">
                        {icon}
                    </div>

                    <div class="feature-title">
                        {title}
                    </div>

                    <div class="feature-text">
                        {description}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">
            Career<span>Lens</span> AI
        </div>

        <div class="brand-subtitle">
            CAREER INTELLIGENCE PLATFORM
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    workspace = st.radio(
        "WORKSPACE",
        [
            "👨‍💻 Job Seeker",
            "🏢 Recruiter",
        ],
    )

    st.divider()

    st.markdown(
        """
        <span class="status">
            ● AI ENGINE ONLINE
        </span>
        """,
        unsafe_allow_html=True,
    )

    st.caption(
        "NLP • ML • Recruitment Intelligence"
    )

    st.divider()

    st.caption(
        "CareerLens AI v2.0"
    )


# ============================================================
# JOB SEEKER DASHBOARD
# ============================================================

if workspace == "👨‍💻 Job Seeker":

    st.markdown(
        """
        <div class="hero">

            <div class="hero-kicker">
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
                CareerLens AI combines resume intelligence,
                semantic job matching, skill-gap analysis,
                job-risk screening and career planning
                into one professional workspace.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.header(
        "Career Overview"
    )

    st.markdown(
        '<div class="section-note">'
        "Your career intelligence at a glance."
        "</div>",
        unsafe_allow_html=True,
    )

    analysis = (
        st.session_state.resume_analysis
    )

    if analysis:

        resume_score = analysis[
            "resume_score"
        ]

        readiness = analysis[
            "readiness"
        ]

        skill_count = len(
            analysis["skills"]
        )

    else:

        resume_score = None
        readiness = None
        skill_count = 0

    metric_cards(
        [
            (
                "Resume Score",
                (
                    f"{resume_score}/100"
                    if resume_score is not None
                    else "—"
                ),
                "AI-assisted resume quality score",
            ),
            (
                "Career Readiness",
                (
                    f"{readiness}%"
                    if readiness is not None
                    else "—"
                ),
                "Profile readiness estimate",
            ),
            (
                "Skills Detected",
                skill_count,
                "Skills extracted from resume",
            ),
            (
                "Applications",
                st.session_state.applications,
                "Tracked applications",
            ),
        ]
    )

    st.divider()

    tabs = st.tabs(
        [
            "📄 Resume",
            "🎯 Job Match",
            "🛡️ Fraud Detection",
            "🧩 Skill Gap",
            "🗺️ Roadmap",
        ]
    )

    # --------------------------------------------------------
    # RESUME
    # --------------------------------------------------------

    with tabs[0]:

        st.subheader(
            "Resume Intelligence"
        )

        st.write(
            "Upload your resume and let the AI engine "
            "build your career profile."
        )

        resume = st.file_uploader(
            "Upload Resume",
            type=[
                "pdf",
                "docx",
                "txt",
            ],
            key="jobseeker_resume",
        )

        if resume:

            text = extract_text(
                resume
            )

            if not text.strip():

                st.error(
                    "No readable text was found. "
                    "Please upload a text-based PDF, DOCX or TXT file."
                )

            else:

                skills = detect_skills(
                    text
                )

                score = calculate_resume_score(
                    text,
                    skills,
                )

                readiness_score = (
                    calculate_readiness(
                        score,
                        skills,
                    )
                )

                st.session_state.resume_text = text

                st.session_state.resume_analysis = {
                    "name": extract_name(text),
                    "email": extract_email(text),
                    "phone": extract_phone(text),
                    "skills": skills,
                    "resume_score": score,
                    "readiness": readiness_score,
                }

                st.success(
                    "Resume analyzed successfully."
                )

                metric_cards(
                    [
                        (
                            "Resume Score",
                            f"{score}/100",
                            "Composite resume score",
                        ),
                        (
                            "Career Readiness",
                            f"{readiness_score}%",
                            "Career readiness estimate",
                        ),
                        (
                            "Skills Detected",
                            len(skills),
                            "Extracted skills",
                        ),
                    ]
                )

                st.subheader(
                    "Candidate Profile"
                )

                left, right = st.columns(2)

                with left:

                    st.write(
                        "**Name:**",
                        extract_name(text),
                    )

                    st.write(
                        "**Email:**",
                        extract_email(text),
                    )

                with right:

                    st.write(
                        "**Phone:**",
                        extract_phone(text),
                    )

                    st.write(
                        "**Resume:**",
                        resume.name,
                    )

                st.subheader(
                    "Detected Skills"
                )

                if skills:

                    st.write(
                        " • ".join(skills)
                    )

                else:

                    st.info(
                        "No known skills detected."
                    )

    # --------------------------------------------------------
    # JOB MATCH
    # --------------------------------------------------------

    with tabs[1]:

        st.subheader(
            "🎯 AI Job Matching"
        )

        st.write(
            "Compare your resume with a target opportunity "
            "using NLP similarity and skill alignment."
        )

        job_description = st.text_area(
            "Job Description",
            height=240,
            placeholder=(
                "Paste the complete job description..."
            ),
            key="job_match",
        )

        if st.button(
            "Analyze Job Match",
            type="primary",
            use_container_width=True,
        ):

            if not st.session_state.resume_text:

                st.warning(
                    "Upload your resume first."
                )

            elif not job_description.strip():

                st.warning(
                    "Enter a job description."
                )

            else:

                result = calculate_job_match(
                    st.session_state.resume_text,
                    job_description,
                )

                metric_cards(
                    [
                        (
                            "Overall Match",
                            f"{result['overall']}%",
                            "Weighted NLP + skill score",
                        ),
                        (
                            "NLP Similarity",
                            f"{result['nlp']}%",
                            "TF-IDF semantic similarity",
                        ),
                        (
                            "Skill Match",
                            f"{result['skill']}%",
                            "Required skills found",
                        ),
                    ]
                )

                st.progress(
                    result["overall"] / 100
                )

                if result["missing"]:

                    st.warning(
                        "Skill gaps: "
                        + ", ".join(
                            result["missing"]
                        )
                    )

                else:

                    st.success(
                        "No major known skill gaps detected."
                    )

    # --------------------------------------------------------
    # FRAUD
    # --------------------------------------------------------

    with tabs[2]:

        st.subheader(
            "🛡️ Job Fraud Detection"
        )

        st.write(
            "Screen job advertisements for suspicious "
            "payment, urgency and communication signals."
        )

        fraud_text = st.text_area(
            "Job Advertisement",
            height=240,
            placeholder=(
                "Paste a job advertisement..."
            ),
            key="fraud_job",
        )

        if st.button(
            "Run Fraud Analysis",
            use_container_width=True,
        ):

            if not fraud_text.strip():

                st.warning(
                    "Enter a job advertisement."
                )

            else:

                result = analyze_fraud(
                    fraud_text
                )

                metric_cards(
                    [
                        (
                            "Risk Score",
                            f"{result['score']}/100",
                            "AI-assisted risk indicator",
                        ),
                        (
                            "Risk Level",
                            result["level"],
                            "Screening classification",
                        ),
                        (
                            "Risk Categories",
                            len(result["details"]),
                            "Categories with signals",
                        ),
                    ]
                )

                if result["level"] == "HIGH RISK":

                    st.error(
                        "High-risk signals detected. "
                        "Review this opportunity carefully."
                    )

                elif result["level"] == "MEDIUM RISK":

                    st.warning(
                        "Moderate-risk signals detected."
                    )

                else:

                    st.success(
                        "No significant predefined risk signals detected."
                    )

                for category, signals in (
                    result["details"].items()
                ):

                    st.write(
                        f"**{category}:** "
                        + ", ".join(signals)
                    )

                st.caption(
                    "Fraud detection provides risk signals "
                    "and is not proof that a job is fraudulent."
                )

    # --------------------------------------------------------
    # SKILL GAP
    # --------------------------------------------------------

    with tabs[3]:

        st.subheader(
            "🧩 Skill Gap Analysis"
        )

        target_job = st.text_area(
            "Target Job Description",
            height=220,
            key="target_job",
        )

        if st.button(
            "Analyze Skill Gap",
            use_container_width=True,
        ):

            if not st.session_state.resume_text:

                st.warning(
                    "Upload your resume first."
                )

            elif not target_job.strip():

                st.warning(
                    "Enter a target job description."
                )

            else:

                current = set(
                    detect_skills(
                        st.session_state.resume_text
                    )
                )

                required = set(
                    detect_skills(
                        target_job
                    )
                )

                missing = sorted(
                    required - current
                )

                metric_cards(
                    [
                        (
                            "Current Skills",
                            len(current),
                            "Skills detected in your profile",
                        ),
                        (
                            "Required Skills",
                            len(required),
                            "Skills detected in target role",
                        ),
                        (
                            "Skill Gaps",
                            len(missing),
                            "Skills not currently detected",
                        ),
                    ]
                )

                if missing:

                    st.warning(
                        "Prioritize: "
                        + ", ".join(missing)
                    )

                else:

                    st.success(
                        "Your detected skills cover the requirements."
                    )

    # --------------------------------------------------------
    # ROADMAP
    # --------------------------------------------------------

    with tabs[4]:

        st.subheader(
            "🗺️ Career Roadmap"
        )

        target_role = st.text_input(
            "Target Role",
            "Machine Learning Engineer",
        )

        if st.button(
            "Generate Roadmap",
            type="primary",
            use_container_width=True,
        ):

            if not st.session_state.resume_text:

                st.warning(
                    "Upload your resume first."
                )

            else:

                steps = [
                    "Strengthen the core skills required for your target role.",
                    "Build 2–3 portfolio projects with measurable outcomes.",
                    "Improve your resume with quantified achievements.",
                    "Prepare technical and behavioral interview questions.",
                    "Apply selectively and track application outcomes.",
                ]

                st.info(
                    f"Target role: {target_role}"
                )

                for number, step in enumerate(
                    steps,
                    1,
                ):

                    st.write(
                        f"**{number}.** {step}"
                    )

    st.divider()

    st.header(
        "Career Intelligence"
    )

    show_feature_cards()


# ============================================================
# RECRUITER DASHBOARD
# ============================================================

else:

    st.markdown(
        """
        <div class="hero">

            <div class="hero-kicker">
                RECRUITMENT INTELLIGENCE
            </div>

            <div class="hero-title">
                Screen Smarter.
                <br>
                <span class="hero-gradient">
                    Hire with Evidence.
                </span>
            </div>

            <div class="hero-text">
                Upload a large candidate batch, define
                the role and let CareerLens AI rank
                candidates using resume quality, NLP
                similarity and skill alignment.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.header(
        "Recruiter Workspace"
    )

    st.write(
        "The recruiter controls how many candidates "
        "are shortlisted."
    )

    st.divider()

    job_description = st.text_area(
        "Job Description",
        height=230,
        placeholder=(
            "Paste the complete job description..."
        ),
        key="recruiter_job",
    )

    required_skills = detect_skills(
        job_description
    )

    if job_description.strip():

        st.write(
            "**Detected Requirements:**"
        )

        if required_skills:

            st.write(
                " • ".join(
                    required_skills
                )
            )

        else:

            st.info(
                "No predefined skills detected."
            )

    st.divider()

    st.subheader(
        "Bulk Candidate Screening"
    )

    candidate_files = st.file_uploader(
        "Upload Candidate Resumes",
        type=[
            "pdf",
            "docx",
            "txt",
        ],
        accept_multiple_files=True,
        key="candidate_files",
    )

    top_n = st.number_input(
        "Recruiter Shortlist Size",
        min_value=1,
        max_value=500,
        value=20,
        step=1,
    )

    st.caption(
        "Examples: Top 5, Top 10, Top 20, Top 50 — "
        "the recruiter decides."
    )

    if st.button(
        "🚀 Screen & Rank Candidates",
        type="primary",
        use_container_width=True,
    ):

        if not job_description.strip():

            st.warning(
                "Enter the job description first."
            )

        elif not candidate_files:

            st.warning(
                "Upload candidate resumes."
            )

        else:

            results = []

            progress = st.progress(
                0
            )

            status = st.empty()

            total = len(
                candidate_files
            )

            for index, candidate in enumerate(
                candidate_files,
                1,
            ):

                status.write(
                    f"AI analyzing "
                    f"{candidate.name}..."
                )

                text = extract_text(
                    candidate
                )

                if text.strip():

                    skills = detect_skills(
                        text
                    )

                    resume_score = (
                        calculate_resume_score(
                            text,
                            skills,
                        )
                    )

                    match = calculate_job_match(
                        text,
                        job_description,
                    )

                    results.append(
                        {
                            "Candidate": extract_name(
                                text
                            ),
                            "Email": extract_email(
                                text
                            ),
                            "Resume Score": resume_score,
                            "NLP Match": match["nlp"],
                            "Skill Match": match["skill"],
                            "Overall Match": match["overall"],
                            "Skills": ", ".join(
                                skills
                            ),
                            "Missing Skills": ", ".join(
                                match["missing"]
                            ),
                            "File": candidate.name,
                        }
                    )

                progress.progress(
                    index / total
                )

            progress.empty()
            status.empty()

            if results:

                df = pd.DataFrame(
                    results
                )

                df = df.sort_values(
                    by=[
                        "Overall Match",
                        "Skill Match",
                        "Resume Score",
                    ],
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

                st.session_state.recruiter_results = df

                st.success(
                    f"Successfully analyzed "
                    f"{len(df)} resumes."
                )

            else:

                st.error(
                    "No readable resumes were found."
                )

    # --------------------------------------------------------
    # RECRUITER RESULTS
    # --------------------------------------------------------

    if (
        st.session_state.recruiter_results
        is not None
    ):

        df = (
            st.session_state.recruiter_results
        )

        shortlist_count = min(
            int(top_n),
            len(df),
        )

        shortlist = df.head(
            shortlist_count
        )

        st.divider()

        st.header(
            "🏆 Candidate Ranking"
        )

        best_match = int(
            df.iloc[0][
                "Overall Match"
            ]
        )

        metric_cards(
            [
                (
                    "Resumes Screened",
                    len(df),
                    "Successfully analyzed resumes",
                ),
                (
                    "Shortlisted",
                    len(shortlist),
                    "Recruiter-selected Top-N",
                ),
                (
                    "Best Match",
                    f"{best_match}%",
                    "Highest overall candidate score",
                ),
            ]
        )

        st.subheader(
            f"Top {shortlist_count} Candidates"
        )

        st.dataframe(
            shortlist,
            use_container_width=True,
            hide_index=True,
        )

        st.divider()

        st.subheader(
            "Candidate Intelligence"
        )

        candidates = shortlist[
            "Candidate"
        ].tolist()

        if candidates:

            selected_candidate = st.selectbox(
                "Select Candidate",
                candidates,
            )

            candidate_row = shortlist[
                shortlist["Candidate"]
                == selected_candidate
            ].iloc[0]

            left, right = st.columns(2)

            with left:

                st.metric(
                    "Overall Match",
                    f"{int(candidate_row['Overall Match'])}%",
                )

                st.write(
                    "**Candidate:**",
                    candidate_row["Candidate"],
                )

                st.write(
                    "**Email:**",
                    candidate_row["Email"],
                )

                st.write(
                    "**Resume Score:**",
                    f"{int(candidate_row['Resume Score'])}/100",
                )

            with right:

                st.metric(
                    "Skill Match",
                    f"{int(candidate_row['Skill Match'])}%",
                )

                st.write(
                    "**NLP Match:**",
                    f"{int(candidate_row['NLP Match'])}%",
                )

                st.write(
                    "**Detected Skills:**",
                    candidate_row["Skills"]
                    or "None detected",
                )

                st.write(
                    "**Missing Skills:**",
                    candidate_row["Missing Skills"]
                    or "None detected",
                )

        st.divider()

        st.subheader(
            "Export Recruitment Results"
        )

        csv = shortlist.to_csv(
            index=False
        ).encode(
            "utf-8"
        )

        st.download_button(
            "⬇️ Download Shortlist CSV",
            data=csv,
            file_name="careerLens_shortlist.csv",
            mime="text/csv",
            use_container_width=True,
        )

        st.caption(
            "CareerLens AI provides AI-assisted screening. "
            "Recruiters should review candidates before making "
            "final hiring decisions."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🎯 CareerLens AI • AI-Powered Career Intelligence "
    "& Recruitment Platform • Artificial Intelligence • "
    "Machine Learning • NLP"
)
