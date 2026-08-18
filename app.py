import io
import re
from typing import Dict, List, Tuple

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
# AI-Powered Career Intelligence & Recruitment Platform
# ============================================================

st.set_page_config(
    page_title="CareerLens AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PROFESSIONAL STREAMLIT THEME
# ============================================================

st.markdown(
    """
    <style>
        .stApp {
            background-color: #07111f;
        }

        [data-testid="stSidebar"] {
            background-color: #0b1728;
        }

        .block-container {
            max-width: 1400px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        h1, h2, h3 {
            color: #f8fafc !important;
        }

        p, label {
            color: #b8c5d6;
        }

        .brand-name {
            font-size: 28px;
            font-weight: 800;
            color: white;
        }

        .brand-accent {
            color: #8b7cff;
        }

        .brand-subtitle {
            font-size: 11px;
            letter-spacing: 2px;
            color: #8091a8;
        }

        .hero-box {
            background-color: #0e1d34;
            border: 1px solid #263d61;
            border-radius: 22px;
            padding: 36px;
            margin-bottom: 28px;
        }

        .hero-label {
            color: #8b7cff;
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 2px;
        }

        .hero-title {
            color: white;
            font-size: 44px;
            line-height: 1.1;
            font-weight: 800;
            margin-top: 12px;
        }

        .hero-accent {
            color: #38bdf8;
        }

        .hero-description {
            color: #aebdd0;
            font-size: 16px;
            line-height: 1.7;
            max-width: 780px;
            margin-top: 15px;
        }

        .section-description {
            color: #8293aa;
            margin-top: -10px;
            margin-bottom: 20px;
        }

        .feature-card {
            background-color: #0d1b2e;
            border: 1px solid #20344f;
            border-radius: 16px;
            padding: 22px;
            min-height: 150px;
        }

        .feature-icon {
            font-size: 28px;
        }

        .feature-title {
            color: white;
            font-size: 17px;
            font-weight: 700;
            margin-top: 8px;
        }

        .feature-description {
            color: #91a2b7;
            font-size: 14px;
            line-height: 1.6;
            margin-top: 6px;
        }

        .online {
            color: #4ade80;
            font-weight: 700;
        }

        div[data-testid="stMetric"] {
            background-color: #0d1b2e;
            border: 1px solid #20344f;
            border-radius: 14px;
            padding: 18px;
        }

        div[data-testid="stMetricValue"] {
            color: white !important;
        }

        div[data-testid="stMetricLabel"] {
            color: #94a3b8 !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SKILL DATABASE
# ============================================================

SKILL_ALIASES = {
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
        "ml",
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
    "Power BI": ["power bi", "powerbi"],
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
    "C++": ["c++", "cpp"],
    "C#": ["c#", "c sharp"],
    ".NET": [".net", "dotnet"],
    "HTML": ["html", "html5"],
    "CSS": ["css", "css3"],
    "Figma": ["figma"],
    "UI/UX": [
        "ui/ux",
        "ui ux",
    ],
    "Agile": [
        "agile",
        "scrum",
    ],
    "Communication": ["communication"],
    "Leadership": ["leadership"],
    "Problem Solving": [
        "problem solving",
        "problem-solving",
    ],
}


# ============================================================
# FRAUD SIGNAL DATABASE
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
        "upfront payment",
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
# SESSION STATE
# ============================================================

defaults = {
    "resume_text": "",
    "resume_name": "",
    "resume_analysis": None,
    "applications": 0,
    "recruiter_results": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def normalize(text: str) -> str:
    return re.sub(
        r"\s+",
        " ",
        str(text).lower(),
    ).strip()


def extract_pdf(data: bytes) -> str:
    if PdfReader is None:
        return ""

    try:
        reader = PdfReader(io.BytesIO(data))

        pages = []

        for page in reader.pages:
            pages.append(
                page.extract_text() or ""
            )

        return "\n".join(pages)

    except Exception:
        return ""


def extract_docx(data: bytes) -> str:
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


def extract_file_text(uploaded_file) -> str:
    if uploaded_file is None:
        return ""

    try:
        data = uploaded_file.getvalue()
    except Exception:
        return ""

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


def detect_skills(text: str) -> List[str]:
    text = normalize(text)

    detected = []

    for skill, aliases in SKILL_ALIASES.items():

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


def extract_email(text: str) -> str:
    match = re.search(
        r"[\w.+-]+@[\w-]+\.[\w.-]+",
        text,
    )

    if match:
        return match.group(0)

    return "Not detected"


def extract_phone(text: str) -> str:
    matches = re.findall(
        r"(?:\+?\d[\d\s().-]{8,}\d)",
        text,
    )

    if matches:
        return matches[0].strip()

    return "Not detected"


def extract_name(text: str) -> str:

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    for line in lines[:10]:

        if (
            2 <= len(line.split()) <= 5
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
    text: str,
    skills: List[str],
) -> int:

    score = 0

    lower = normalize(text)

    if len(text.strip()) >= 300:
        score += 15

    if extract_email(text) != "Not detected":
        score += 10

    if extract_phone(text) != "Not detected":
        score += 5

    score += min(
        len(skills) * 3,
        30,
    )

    education_words = [
        "b.tech",
        "btech",
        "bachelor",
        "master",
        "degree",
        "computer science",
        "engineering",
    ]

    if any(
        word in lower
        for word in education_words
    ):
        score += 15

    if "experience" in lower:
        score += 10

    if "project" in lower:
        score += 5

    if (
        "linkedin" in lower
        or "github" in lower
    ):
        score += 5

    return min(
        score,
        100,
    )


def calculate_readiness(
    resume_score: int,
    skills: List[str],
) -> int:

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


def nlp_similarity(
    profile: str,
    job: str,
) -> float:

    if (
        not profile.strip()
        or not job.strip()
    ):
        return 0.0

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

        return float(similarity)

    except Exception:
        return 0.0


def skill_similarity(
    profile_skills: List[str],
    job_skills: List[str],
) -> float:

    if not job_skills:
        return 0.0

    profile = set(profile_skills)
    job = set(job_skills)

    return (
        len(profile & job)
        / len(job)
    )


def calculate_match(
    profile: str,
    job: str,
) -> Tuple[int, int, int]:

    profile_skills = detect_skills(
        profile
    )

    job_skills = detect_skills(
        job
    )

    nlp_score = nlp_similarity(
        profile,
        job,
    )

    skill_score = skill_similarity(
        profile_skills,
        job_skills,
    )

    final_score = (
        nlp_score * 0.55
        + skill_score * 0.45
    )

    return (
        min(
            round(
                final_score * 100
            ),
            100,
        ),
        min(
            round(
                nlp_score * 100
            ),
            100,
        ),
        min(
            round(
                skill_score * 100
            ),
            100,
        ),
    )


def detect_fraud(
    job_text: str,
) -> Dict:

    text = normalize(
        job_text
    )

    found = {}

    for category, phrases in FRAUD_RULES.items():

        hits = [
            phrase
            for phrase in phrases
            if phrase in text
        ]

        if hits:
            found[category] = hits

    total_signals = sum(
        len(values)
        for values in found.values()
    )

    risk_score = min(
        total_signals * 15,
        100,
    )

    if risk_score >= 60:
        level = "HIGH RISK"

    elif risk_score >= 30:
        level = "MEDIUM RISK"

    else:
        level = "LOW RISK"

    return {
        "level": level,
        "score": risk_score,
        "signals": found,
    }


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="brand-name">'
        'Career<span class="brand-accent">Lens</span> AI'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="brand-subtitle">'
        'CAREER INTELLIGENCE PLATFORM'
        '</div>',
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
        '<p class="online">● AI ENGINE ONLINE</p>',
        unsafe_allow_html=True,
    )

    st.caption(
        "NLP • Machine Learning • "
        "Recruitment Intelligence"
    )


# ============================================================
# JOB SEEKER
# ============================================================

if workspace == "👨‍💻 Job Seeker":

    st.markdown(
        '<div class="hero-box">'
        '<div class="hero-label">'
        'AI CAREER INTELLIGENCE'
        '</div>'
        '<div class="hero-title">'
        'Understand Your Career.'
        '<br>'
        '<span class="hero-accent">'
        'Build Your Future.'
        '</span>'
        '</div>'
        '<div class="hero-description">'
        'CareerLens AI analyzes your resume, '
        'evaluates opportunities, detects job-risk '
        'signals, identifies skill gaps and builds '
        'a personalized career intelligence profile.'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.header(
        "Career Overview"
    )

    st.write(
        "Your career intelligence at a glance."
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

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Resume Score",
            (
                "—"
                if resume_score is None
                else f"{resume_score}/100"
            ),
        )

    with c2:
        st.metric(
            "Career Readiness",
            (
                "—"
                if readiness is None
                else f"{readiness}%"
            ),
        )

    with c3:
        st.metric(
            "Skills Detected",
            skill_count,
        )

    with c4:
        st.metric(
            "Applications",
            st.session_state.applications,
        )

    st.divider()

    # --------------------------------------------------------
    # RESUME INTELLIGENCE
    # --------------------------------------------------------

    st.header(
        "📄 Resume Intelligence"
    )

    st.write(
        "Upload your resume to extract your "
        "professional profile."
    )

    resume = st.file_uploader(
        "Resume File",
        type=[
            "pdf",
            "docx",
            "txt",
        ],
        key="jobseeker_resume",
    )

    if resume:

        resume_text = extract_file_text(
            resume
        )

        if not resume_text.strip():

            st.error(
                "Could not extract text from this file. "
                "Please use a text-based PDF, DOCX or TXT file."
            )

        else:

            skills = detect_skills(
                resume_text
            )

            score = calculate_resume_score(
                resume_text,
                skills,
            )

            readiness_score = (
                calculate_readiness(
                    score,
                    skills,
                )
            )

            st.session_state.resume_text = (
                resume_text
            )

            st.session_state.resume_name = (
                resume.name
            )

            st.session_state.resume_analysis = {
                "name": extract_name(
                    resume_text
                ),
                "email": extract_email(
                    resume_text
                ),
                "phone": extract_phone(
                    resume_text
                ),
                "skills": skills,
                "resume_score": score,
                "readiness": readiness_score,
            }

            st.success(
                "Resume analyzed successfully."
            )

            a, b, c = st.columns(3)

            with a:
                st.metric(
                    "Resume Score",
                    f"{score}/100",
                )

            with b:
                st.metric(
                    "Career Readiness",
                    f"{readiness_score}%",
                )

            with c:
                st.metric(
                    "Skills Detected",
                    len(skills),
                )

            st.subheader(
                "Candidate Profile"
            )

            p1, p2 = st.columns(2)

            with p1:

                st.write(
                    f"**Name:** "
                    f"{extract_name(resume_text)}"
                )

                st.write(
                    f"**Email:** "
                    f"{extract_email(resume_text)}"
                )

            with p2:

                st.write(
                    f"**Phone:** "
                    f"{extract_phone(resume_text)}"
                )

                st.write(
                    f"**File:** "
                    f"{resume.name}"
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
                    "No predefined skills detected."
                )

    st.divider()

    # --------------------------------------------------------
    # JOB MATCHING
    # --------------------------------------------------------

    st.header(
        "🎯 AI Job Matching"
    )

    st.write(
        "Compare your profile against a target job."
    )

    job_description = st.text_area(
        "Job Description",
        height=220,
        placeholder=(
            "Paste the complete job description here..."
        ),
        key="job_match_description",
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

            overall, nlp, skill = (
                calculate_match(
                    st.session_state.resume_text,
                    job_description,
                )
            )

            profile_skills = detect_skills(
                st.session_state.resume_text
            )

            job_skills = detect_skills(
                job_description
            )

            missing = sorted(
                set(job_skills)
                - set(profile_skills)
            )

            m1, m2, m3 = st.columns(3)

            with m1:
                st.metric(
                    "Overall Match",
                    f"{overall}%",
                )

            with m2:
                st.metric(
                    "NLP Similarity",
                    f"{nlp}%",
                )

            with m3:
                st.metric(
                    "Skill Match",
                    f"{skill}%",
                )

            if missing:

                st.warning(
                    "Skill gaps: "
                    + ", ".join(missing)
                )

            else:

                st.success(
                    "No major predefined skill gaps detected."
                )

    st.divider()

    # --------------------------------------------------------
    # FRAUD DETECTION
    # --------------------------------------------------------

    st.header(
        "🛡️ Job Fraud Detection"
    )

    st.write(
        "Screen job advertisements for suspicious signals."
    )

    fraud_text = st.text_area(
        "Job Advertisement",
        height=220,
        placeholder=(
            "Paste a job advertisement here..."
        ),
        key="fraud_description",
    )

    if st.button(
        "Run Fraud Detection",
        use_container_width=True,
    ):

        if not fraud_text.strip():

            st.warning(
                "Enter a job advertisement."
            )

        else:

            fraud_result = detect_fraud(
                fraud_text
            )

            level = fraud_result[
                "level"
            ]

            score = fraud_result[
                "score"
            ]

            if level == "HIGH RISK":

                st.error(
                    f"⚠️ {level} — {score}/100"
                )

            elif level == "MEDIUM RISK":

                st.warning(
                    f"⚠️ {level} — {score}/100"
                )

            else:

                st.success(
                    f"✓ {level} — {score}/100"
                )

            if fraud_result["signals"]:

                st.subheader(
                    "Detected Risk Signals"
                )

                for category, signals in (
                    fraud_result["signals"].items()
                ):

                    st.write(
                        f"**{category}:** "
                        + ", ".join(signals)
                    )

            else:

                st.info(
                    "No predefined suspicious signals detected."
                )

            st.caption(
                "This is an AI-assisted screening tool, "
                "not a guarantee that a job is legitimate "
                "or fraudulent."
            )

    st.divider()

    # --------------------------------------------------------
    # SKILL GAP + ROADMAP
    # --------------------------------------------------------

    st.header(
        "🧩 Skill Gap Analysis"
    )

    target_role = st.text_input(
        "Target Role",
        placeholder=(
            "Example: Machine Learning Engineer"
        ),
    )

    target_job = st.text_area(
        "Target Job Description",
        height=180,
        placeholder=(
            "Paste the target job description..."
        ),
    )

    if st.button(
        "Generate Career Plan",
        use_container_width=True,
    ):

        if not st.session_state.resume_text:

            st.warning(
                "Upload your resume first."
            )

        elif not target_job.strip():

            st.warning(
                "Enter the target job description."
            )

        else:

            profile_skills = detect_skills(
                st.session_state.resume_text
            )

            target_skills = detect_skills(
                target_job
            )

            missing = sorted(
                set(target_skills)
                - set(profile_skills)
            )

            left, right = st.columns(2)

            with left:

                st.subheader(
                    "Your Skills"
                )

                if profile_skills:
                    st.write(
                        ", ".join(profile_skills)
                    )
                else:
                    st.info(
                        "No predefined skills detected."
                    )

            with right:

                st.subheader(
                    "Skill Gaps"
                )

                if missing:
                    st.write(
                        ", ".join(missing)
                    )
                else:
                    st.success(
                        "No major predefined skill gaps."
                    )

            st.subheader(
                "🗺️ Career Roadmap"
            )

            roadmap = [
                (
                    f"Focus on your target role: "
                    f"{target_role or 'Target Role'}"
                ),
                (
                    "Strengthen your core technical "
                    "and professional skills."
                ),
            ]

            if missing:

                roadmap.append(
                    "Prioritize learning: "
                    + ", ".join(missing)
                )

            roadmap.extend(
                [
                    "Build strong portfolio projects.",
                    "Improve your resume for the target role.",
                    "Prepare technical and behavioral interviews.",
                    "Apply to relevant opportunities.",
                ]
            )

            for index, item in enumerate(
                roadmap,
                start=1,
            ):

                st.write(
                    f"**{index}.** {item}"
                )

    st.divider()

    # --------------------------------------------------------
    # FEATURE GRID
    # --------------------------------------------------------

    st.header(
        "Career Intelligence"
    )

    st.write(
        "AI-powered tools for smarter career decisions."
    )

    features = [
        (
            "📄",
            "Resume Intelligence",
            "Extract skills, education, projects and experience.",
        ),
        (
            "🎯",
            "AI Job Matching",
            "Compare your profile with job opportunities.",
        ),
        (
            "🛡️",
            "Job Fraud Detection",
            "Detect suspicious payment, urgency and communication signals.",
        ),
        (
            "🧩",
            "Skill Gap Analysis",
            "Discover missing skills for your target career.",
        ),
        (
            "🔎",
            "Job Intelligence",
            "Understand important job requirements.",
        ),
        (
            "🗺️",
            "Career Roadmap",
            "Build a structured learning and career path.",
        ),
    ]

    feature_cols = st.columns(3)

    for index, (
        icon,
        title,
        description,
    ) in enumerate(features):

        with feature_cols[
            index % 3
        ]:

            st.markdown(
                '<div class="feature-card">'
                f'<div class="feature-icon">{icon}</div>'
                f'<div class="feature-title">{title}</div>'
                f'<div class="feature-description">'
                f'{description}'
                '</div>'
                '</div>',
                unsafe_allow_html=True,
            )


# ============================================================
# RECRUITER DASHBOARD
# ============================================================

else:

    st.title(
        "🏢 Recruiter Intelligence"
    )

    st.write(
        "Screen large resume batches, rank candidates "
        "and create a recruiter-controlled shortlist."
    )

    st.divider()

    r1, r2, r3 = st.columns(3)

    with r1:
        st.metric(
            "AI Engine",
            "ONLINE",
        )

    with r2:
        st.metric(
            "Screening",
            "NLP + SKILLS",
        )

    with r3:
        st.metric(
            "Shortlist",
            "RECRUITER CONTROLLED",
        )

    st.divider()

    # --------------------------------------------------------
    # JOB REQUIREMENTS
    # --------------------------------------------------------

    st.header(
        "1. Job Requirements"
    )

    recruiter_job = st.text_area(
        "Job Description",
        height=240,
        placeholder=(
            "Paste the complete job description..."
        ),
        key="recruiter_job",
    )

    if recruiter_job.strip():

        required_skills = detect_skills(
            recruiter_job
        )

        st.subheader(
            "Required Skills Detected"
        )

        if required_skills:

            st.write(
                " • ".join(required_skills)
            )

        else:

            st.info(
                "No predefined skills detected."
            )

    st.divider()

    # --------------------------------------------------------
    # BULK RESUME UPLOAD
    # --------------------------------------------------------

    st.header(
        "2. Bulk Resume Screening"
    )

    candidate_files = st.file_uploader(
        "Upload Candidate Resumes",
        type=[
            "pdf",
            "docx",
            "txt",
        ],
        accept_multiple_files=True,
        key="candidate_resumes",
    )

    top_n = st.number_input(
        "Shortlist Size",
        min_value=1,
        max_value=500,
        value=20,
        step=1,
        help=(
            "Recruiter decides how many candidates "
            "should be shortlisted."
        ),
    )

    st.info(
        "You can choose Top 5, Top 10, Top 20, "
        "Top 50 or any other number up to 500."
    )

    if st.button(
        "🚀 Screen & Rank Candidates",
        type="primary",
        use_container_width=True,
    ):

        if not recruiter_job.strip():

            st.warning(
                "Enter the job description first."
            )

        elif not candidate_files:

            st.warning(
                "Upload candidate resumes first."
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
                start=1,
            ):

                status.write(
                    f"Analyzing {candidate.name}..."
                )

                text = extract_file_text(
                    candidate
                )

                if not text.strip():

                    results.append(
                        {
                            "Candidate": candidate.name,
                            "Email": "Not detected",
                            "Resume Score": 0,
                            "NLP Match": 0,
                            "Skill Match": 0,
                            "Overall Match": 0,
                            "Skills": "",
                            "Missing Skills": "",
                            "Status": "Unreadable",
                        }
                    )

                else:

                    profile_skills = detect_skills(
                        text
                    )

                    job_skills = detect_skills(
                        recruiter_job
                    )

                    overall, nlp, skill = (
                        calculate_match(
                            text,
                            recruiter_job,
                        )
                    )

                    resume_score = (
                        calculate_resume_score(
                            text,
                            profile_skills,
                        )
                    )

                    missing = sorted(
                        set(job_skills)
                        - set(profile_skills)
                    )

                    candidate_name = (
                        extract_name(text)
                    )

                    if (
                        candidate_name
                        == "Candidate"
                    ):
                        candidate_name = (
                            candidate.name
                        )

                    results.append(
                        {
                            "Candidate": candidate_name,
                            "Email": extract_email(text),
                            "Resume Score": resume_score,
                            "NLP Match": nlp,
                            "Skill Match": skill,
                            "Overall Match": overall,
                            "Skills": ", ".join(
                                profile_skills
                            ),
                            "Missing Skills": ", ".join(
                                missing
                            ),
                            "Status": "Analyzed",
                        }
                    )

                progress.progress(
                    index / total
                )

            status.empty()
            progress.empty()

            result_df = pd.DataFrame(
                results
            )

            result_df = result_df.sort_values(
                by=[
                    "Overall Match",
                    "Skill Match",
                    "Resume Score",
                ],
                ascending=False,
            ).reset_index(
                drop=True
            )

            result_df.insert(
                0,
                "Rank",
                range(
                    1,
                    len(result_df) + 1,
                ),
            )

            st.session_state.recruiter_results = (
                result_df
            )

            st.success(
                f"Completed screening of "
                f"{len(result_df)} resumes."
            )

    # --------------------------------------------------------
    # RANKING RESULTS
    # --------------------------------------------------------

    if (
        st.session_state.recruiter_results
        is not None
    ):

        result_df = (
            st.session_state.recruiter_results
        )

        shortlist_count = min(
            int(top_n),
            len(result_df),
        )

        shortlist = result_df.head(
            shortlist_count
        )

        st.divider()

        st.header(
            "3. AI Candidate Ranking"
        )

        a, b, c = st.columns(3)

        with a:

            st.metric(
                "Resumes Screened",
                len(result_df),
            )

        with b:

            st.metric(
                "Shortlisted",
                len(shortlist),
            )

        with c:

            best = int(
                result_df.iloc[0][
                    "Overall Match"
                ]
            )

            st.metric(
                "Best Match",
                f"{best}%",
            )

        st.subheader(
            f"🏆 Top {shortlist_count} Candidates"
        )

        display_columns = [
            "Rank",
            "Candidate",
            "Email",
            "Resume Score",
            "NLP Match",
            "Skill Match",
            "Overall Match",
            "Missing Skills",
            "Status",
        ]

        st.dataframe(
            shortlist[
                display_columns
            ],
            use_container_width=True,
            hide_index=True,
        )

        st.divider()

        # ----------------------------------------------------
        # CANDIDATE DETAILS
        # ----------------------------------------------------

        st.header(
            "4. Candidate Intelligence"
        )

        candidates = shortlist[
            "Candidate"
        ].tolist()

        if candidates:

            selected_candidate = (
                st.selectbox(
                    "Select Candidate",
                    candidates,
                )
            )

            selected = shortlist[
                shortlist["Candidate"]
                == selected_candidate
            ].iloc[0]

            d1, d2 = st.columns(2)

            with d1:

                st.write(
                    f"**Candidate:** "
                    f"{selected['Candidate']}"
                )

                st.write(
                    f"**Email:** "
                    f"{selected['Email']}"
                )

                st.write(
                    f"**Overall Match:** "
                    f"{selected['Overall Match']}%"
                )

            with d2:

                st.write(
                    f"**Resume Score:** "
                    f"{selected['Resume Score']}/100"
                )

                st.write(
                    f"**NLP Match:** "
                    f"{selected['NLP Match']}%"
                )

                st.write(
                    f"**Skill Match:** "
                    f"{selected['Skill Match']}%"
                )

            st.subheader(
                "Detected Skills"
            )

            st.write(
                selected["Skills"]
                or "None detected"
            )

            st.subheader(
                "Missing Skills"
            )

            st.write(
                selected["Missing Skills"]
                or "No major predefined skill gaps"
            )

        st.divider()

        # ----------------------------------------------------
        # EXPORT
        # ----------------------------------------------------

        st.header(
            "5. Export Shortlist"
        )

        csv_data = shortlist.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "⬇️ Download Shortlist CSV",
            data=csv_data,
            file_name=(
                "careerLens_shortlist.csv"
            ),
            mime="text/csv",
            use_container_width=True,
        )

        st.caption(
            "CareerLens AI provides AI-assisted candidate "
            "screening. Recruiters should review candidates "
            "before making final hiring decisions."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🎯 CareerLens AI | AI-Powered Career Intelligence "
    "& Recruitment Platform | Final Year Project | "
    "Artificial Intelligence • Machine Learning • NLP"
)
