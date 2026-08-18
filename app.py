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
# CareerLens AI
# AI-Powered Career Intelligence & Recruitment Platform
# ============================================================

st.set_page_config(
    page_title="CareerLens AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# APP THEME
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background: #07111f;
    }

    section[data-testid="stSidebar"] {
        background: #0b1728;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        color: #f8fafc !important;
    }

    p, label, .stCaption {
        color: #b8c5d6 !important;
    }

    div[data-testid="stMetric"] {
        background: #0d1b2e;
        border: 1px solid #20344f;
        border-radius: 14px;
        padding: 18px;
    }

    div[data-testid="stMetricValue"] {
        color: #ffffff !important;
    }

    div[data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #0d1b2e;
        border-radius: 16px;
        border-color: #20344f;
    }

    .brand {
        font-size: 30px;
        font-weight: 800;
        color: white;
        margin-bottom: 2px;
    }

    .brand span {
        color: #7c83ff;
    }

    .brand-subtitle {
        color: #8191a8;
        font-size: 12px;
        letter-spacing: 1.5px;
    }

    .hero {
        background: linear-gradient(
            135deg,
            #0e1d34 0%,
            #101d38 55%,
            #14234a 100%
        );
        border: 1px solid #263d61;
        border-radius: 24px;
        padding: 42px;
        margin: 10px 0 30px 0;
    }

    .hero-small {
        color: #8ea2ff;
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 1.5px;
        margin-bottom: 12px;
    }

    .hero-title {
        color: white;
        font-size: 48px;
        line-height: 1.08;
        font-weight: 800;
        margin-bottom: 18px;
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
        max-width: 760px;
        color: #aebdd0;
        font-size: 16px;
        line-height: 1.7;
    }

    .status {
        color: #45e39b;
        font-weight: 700;
    }

    .feature-title {
        color: white;
        font-size: 19px;
        font-weight: 700;
        margin-top: 10px;
    }

    .feature-text {
        color: #91a2b7;
        line-height: 1.6;
        font-size: 14px;
    }

    .section-note {
        color: #7f91a8;
        margin-top: -10px;
        margin-bottom: 20px;
    }

    .risk-high {
        color: #ff6b6b;
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
# DATA
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
    "Machine Learning": ["machine learning", "machine-learning", "ml"],
    "Deep Learning": ["deep learning", "deep-learning"],
    "NLP": ["nlp", "natural language processing"],
    "Computer Vision": ["computer vision", "opencv"],
    "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch"],
    "Scikit-learn": ["scikit-learn", "sklearn"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Data Analysis": ["data analysis", "data analytics"],
    "Data Science": ["data science"],
    "Power BI": ["power bi", "powerbi"],
    "Tableau": ["tableau"],
    "Excel": ["excel", "microsoft excel"],
    "AWS": ["aws", "amazon web services"],
    "Azure": ["azure", "microsoft azure"],
    "GCP": ["gcp", "google cloud"],
    "Docker": ["docker"],
    "Kubernetes": ["kubernetes", "k8s"],
    "Git": ["git", "github", "gitlab"],
    "Linux": ["linux"],
    "REST API": ["rest api", "restful api", "rest apis"],
    "FastAPI": ["fastapi", "fast api"],
    "Flask": ["flask"],
    "Django": ["django"],
    "Spring Boot": ["spring boot"],
    "C++": ["c++", "cpp"],
    "C#": ["c#", "c sharp"],
    ".NET": [".net", "dotnet"],
    "HTML": ["html", "html5"],
    "CSS": ["css", "css3"],
    "Figma": ["figma"],
    "UI/UX": ["ui/ux", "ui ux"],
    "Agile": ["agile", "scrum"],
    "Communication": ["communication"],
    "Leadership": ["leadership"],
    "Problem Solving": ["problem solving", "problem-solving"],
}

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

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "resume_name" not in st.session_state:
    st.session_state.resume_name = ""

if "resume_analysis" not in st.session_state:
    st.session_state.resume_analysis = None

if "applications" not in st.session_state:
    st.session_state.applications = 0

if "recruiter_results" not in st.session_state:
    st.session_state.recruiter_results = None


# ============================================================
# FUNCTIONS
# ============================================================

def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", str(text).lower()).strip()


def extract_pdf(data: bytes) -> str:
    if PdfReader is None:
        return ""

    try:
        reader = PdfReader(io.BytesIO(data))
        pages = []

        for page in reader.pages:
            pages.append(page.extract_text() or "")

        return "\n".join(pages)

    except Exception:
        return ""


def extract_docx(data: bytes) -> str:
    if Document is None:
        return ""

    try:
        document = Document(io.BytesIO(data))
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

    extension = uploaded_file.name.lower().split(".")[-1]

    if extension == "txt":
        return data.decode("utf-8", errors="ignore")

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

            if re.search(pattern, text):
                detected.append(skill)
                break

    return sorted(set(detected))


def extract_email(text: str) -> str:
    match = re.search(
        r"[\w.+-]+@[\w-]+\.[\w.-]+",
        text
    )

    return match.group(0) if match else "Not detected"


def extract_phone(text: str) -> str:
    matches = re.findall(
        r"(?:\+?\d[\d\s().-]{8,}\d)",
        text
    )

    return matches[0].strip() if matches else "Not detected"


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
            and not re.search(r"\d", line)
            and len(line) < 60
        ):
            return line.title()

    return "Candidate"


def calculate_resume_score(
    text: str,
    skills: List[str]
) -> int:

    score = 0
    lower = normalize(text)

    if len(text.strip()) >= 300:
        score += 15

    if extract_email(text) != "Not detected":
        score += 10

    if extract_phone(text) != "Not detected":
        score += 5

    score += min(len(skills) * 3, 30)

    if any(
        keyword in lower
        for keyword in [
            "b.tech",
            "btech",
            "bachelor",
            "master",
            "degree",
            "computer science",
            "engineering",
        ]
    ):
        score += 15

    if "experience" in lower:
        score += 10

    if "project" in lower:
        score += 5

    if "linkedin" in lower or "github" in lower:
        score += 5

    return min(score, 100)


def calculate_readiness(
    resume_score: int,
    skills: List[str]
) -> int:

    return min(
        100,
        round(
            resume_score * 0.7
            + min(len(skills) * 4, 30)
        ),
    )


def nlp_similarity(
    profile: str,
    job: str
) -> float:

    if not profile.strip() or not job.strip():
        return 0.0

    try:

        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
        )

        matrix = vectorizer.fit_transform(
            [normalize(profile), normalize(job)]
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
    job_skills: List[str]
) -> float:

    if not job_skills:
        return 0.0

    profile = set(profile_skills)
    job = set(job_skills)

    return len(profile & job) / len(job)


def calculate_match(
    profile: str,
    job: str
) -> Tuple[int, int, int]:

    profile_skills = detect_skills(profile)
    job_skills = detect_skills(job)

    nlp_score = nlp_similarity(profile, job)
    skill_score = skill_similarity(
        profile_skills,
        job_skills,
    )

    final_score = (
        nlp_score * 0.55
        + skill_score * 0.45
    )

    return (
        min(round(final_score * 100), 100),
        min(round(nlp_score * 100), 100),
        min(round(skill_score * 100), 100),
    )


def detect_fraud(job_text: str) -> Dict:

    text = normalize(job_text)

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
        100
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
        '<div class="brand">Career<span>Lens</span> AI</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="brand-subtitle">CAREER INTELLIGENCE PLATFORM</div>',
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

    st.success("AI ENGINE ONLINE")

    st.caption(
        "NLP • ML • Recruitment Intelligence"
    )


# ============================================================
# JOB SEEKER DASHBOARD
# ============================================================

if workspace == "👨‍💻 Job Seeker":

    st.markdown(
        """
        <div class="hero">
            <div class="hero-small">
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
                CareerLens AI analyzes your resume,
                evaluates opportunities, detects job-risk
                signals, identifies skill gaps and builds
                a personalized career intelligence profile.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Career Overview")
    st.caption(
        "Your career intelligence at a glance."
    )

    analysis = st.session_state.resume_analysis

    if analysis:

        resume_score = analysis["resume_score"]
        readiness = analysis["readiness"]
        skill_count = len(
            analysis["skills"]
        )

    else:

        resume_score = None
        readiness = None
        skill_count = 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Resume Score",
            "—"
            if resume_score is None
            else f"{resume_score}/100",
        )

    with col2:
        st.metric(
            "Career Readiness",
            "—"
            if readiness is None
            else f"{readiness}%",
        )

    with col3:
        st.metric(
            "Skills Detected",
            skill_count,
        )

    with col4:
        st.metric(
            "Applications",
            st.session_state.applications,
        )

    st.divider()

    # ========================================================
    # RESUME
    # ========================================================

    st.subheader("📄 Resume Intelligence")

    st.write(
        "Upload your resume and let CareerLens AI "
        "extract your professional profile."
    )

    resume = st.file_uploader(
        "Upload Resume",
        type=[
            "pdf",
            "docx",
            "txt",
        ],
    )

    if resume:

        resume_text = extract_file_text(
            resume
        )

        if not resume_text.strip():

            st.error(
                "Unable to extract text from this resume. "
                "Please upload a text-based PDF, DOCX or TXT file."
            )

        else:

            skills = detect_skills(
                resume_text
            )

            score = calculate_resume_score(
                resume_text,
                skills,
            )

            readiness = calculate_readiness(
                score,
                skills,
            )

            st.session_state.resume_text = resume_text
            st.session_state.resume_name = resume.name

            st.session_state.resume_analysis = {
                "name": extract_name(resume_text),
                "email": extract_email(resume_text),
                "phone": extract_phone(resume_text),
                "skills": skills,
                "resume_score": score,
                "readiness": readiness,
            }

            st.success(
                f"Resume analyzed successfully: {resume.name}"
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
                    f"{readiness}%",
                )

            with c:
                st.metric(
                    "Skills",
                    len(skills),
                )

            st.write("### Candidate Profile")

            p1, p2 = st.columns(2)

            with p1:

                st.write(
                    f"**Name:** {extract_name(resume_text)}"
                )

                st.write(
                    f"**Email:** {extract_email(resume_text)}"
                )

            with p2:

                st.write(
                    f"**Phone:** {extract_phone(resume_text)}"
                )

                st.write(
                    f"**Resume:** {resume.name}"
                )

            st.write("### Detected Skills")

            if skills:
                st.write(
                    " • ".join(skills)
                )
            else:
                st.info(
                    "No predefined skills detected."
                )

    st.divider()

    # ========================================================
    # JOB MATCHING
    # ========================================================

    st.subheader("🎯 AI Job Matching")

    st.caption(
        "Compare your resume against a target opportunity."
    )

    job_description = st.text_area(
        "Job Description",
        height=220,
        placeholder=(
            "Paste the job description here..."
        ),
    )

    if st.button(
        "Analyze Job Match",
        type="primary",
        use_container_width=True,
    ):

        if not st.session_state.resume_text:

            st.warning(
                "Please upload a resume first."
            )

        elif not job_description.strip():

            st.warning(
                "Please enter a job description."
            )

        else:

            overall, nlp, skill = calculate_match(
                st.session_state.resume_text,
                job_description,
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

    # ========================================================
    # FRAUD DETECTION
    # ========================================================

    st.subheader("🛡️ Job Fraud Detection")

    st.caption(
        "Analyze suspicious signals in job postings."
    )

    fraud_text = st.text_area(
        "Job Posting",
        height=200,
        placeholder=(
            "Paste a job advertisement here..."
        ),
    )

    if st.button(
        "Run Fraud Detection",
        use_container_width=True,
    ):

        if not fraud_text.strip():

            st.warning(
                "Please enter a job posting."
            )

        else:

            result = detect_fraud(
                fraud_text
            )

            if result["level"] == "HIGH RISK":

                st.error(
                    f"⚠️ {result['level']} "
                    f"— {result['score']}/100"
                )

            elif result["level"] == "MEDIUM RISK":

                st.warning(
                    f"⚠️ {result['level']} "
                    f"— {result['score']}/100"
                )

            else:

                st.success(
                    f"✓ {result['level']} "
                    f"— {result['score']}/100"
                )

            if result["signals"]:

                st.write(
                    "### Suspicious Signals"
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
                    "No predefined suspicious signals detected."
                )

            st.caption(
                "Fraud detection is a screening aid and "
                "does not guarantee that a job is legitimate "
                "or fraudulent."
            )

    st.divider()

    # ========================================================
    # SKILL GAP / ROADMAP
    # ========================================================

    st.subheader("🧩 Skill Gap & Career Roadmap")

    target_role = st.text_input(
        "Target Role",
        placeholder="Example: Machine Learning Engineer",
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
                "Upload a resume first."
            )

        elif not target_job.strip():

            st.warning(
                "Enter a target job description."
            )

        else:

            profile_skills = detect_skills(
                st.session_state.resume_text
            )

            job_skills = detect_skills(
                target_job
            )

            missing = sorted(
                set(job_skills)
                - set(profile_skills)
            )

            left, right = st.columns(2)

            with left:

                st.write(
                    "### Your Skills"
                )

                if profile_skills:
                    st.write(
                        ", ".join(profile_skills)
                    )
                else:
                    st.info(
                        "No skills detected."
                    )

            with right:

                st.write(
                    "### Skill Gaps"
                )

                if missing:
                    st.write(
                        ", ".join(missing)
                    )
                else:
                    st.success(
                        "No major predefined skill gaps."
                    )

            st.write(
                "### 🗺️ Career Roadmap"
            )

            roadmap = [
                f"Choose and focus on your target role: "
                f"{target_role or 'Target Role'}",
                "Strengthen your core technical skills.",
            ]

            if missing:

                roadmap.append(
                    "Prioritize learning: "
                    + ", ".join(missing)
                )

            roadmap.extend(
                [
                    "Build 1–2 strong portfolio projects.",
                    "Improve your resume around the target role.",
                    "Prepare technical and behavioral interviews.",
                    "Apply to relevant opportunities and track results.",
                ]
            )

            for index, step in enumerate(
                roadmap,
                start=1,
            ):

                st.write(
                    f"**{index}.** {step}"
                )

    st.divider()

    # ========================================================
    # FEATURES
    # ========================================================

    st.subheader("Career Intelligence")

    st.caption(
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
            "Compare your profile with opportunities using NLP.",
        ),
        (
            "🛡️",
            "Job Fraud Detection",
            "Identify suspicious payment and urgency signals.",
        ),
        (
            "🧩",
            "Skill Gap Analysis",
            "Discover missing skills for your target role.",
        ),
        (
            "🔎",
            "Job Intelligence",
            "Understand important requirements in job descriptions.",
        ),
        (
            "🗺️",
            "Career Roadmap",
            "Build a structured career development path.",
        ),
    ]

    feature_columns = st.columns(3)

    for index, feature in enumerate(features):

        icon, title, description = feature

        with feature_columns[
            index % 3
        ]:

            with st.container(
                border=True
            ):

                st.markdown(
                    f"### {icon} {title}"
                )

                st.write(
                    description
                )


# ============================================================
# RECRUITER DASHBOARD
# ============================================================

else:

    st.title("🏢 Recruiter Intelligence")

    st.subheader(
        "Screen candidates faster. Shortlist smarter."
    )

    st.write(
        "Upload multiple resumes, provide the job description, "
        "and CareerLens AI will rank candidates using NLP "
        "similarity and skill matching."
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
            "Ranking",
            "NLP + SKILLS",
        )

    with r3:
        st.metric(
            "Recruiter Control",
            "TOP-N",
        )

    st.divider()

    # ========================================================
    # JOB DESCRIPTION
    # ========================================================

    st.subheader(
        "1. Job Requirement"
    )

    recruiter_job = st.text_area(
        "Job Description",
        height=240,
        placeholder=(
            "Paste the complete job description..."
        ),
    )

    if recruiter_job.strip():

        required_skills = detect_skills(
            recruiter_job
        )

        st.write(
            "### Detected Required Skills"
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

    # ========================================================
    # BULK UPLOAD
    # ========================================================

    st.subheader(
        "2. Bulk Candidate Screening"
    )

    candidate_files = st.file_uploader(
        "Upload Candidate Resumes",
        type=[
            "pdf",
            "docx",
            "txt",
        ],
        accept_multiple_files=True,
    )

    top_n = st.number_input(
        "How many candidates should be shortlisted?",
        min_value=1,
        max_value=500,
        value=20,
        step=1,
    )

    st.caption(
        "The recruiter controls the shortlist size."
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

            progress = st.progress(0)

            status = st.empty()

            total = len(candidate_files)

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

                    overall, nlp, skill = calculate_match(
                        text,
                        recruiter_job,
                    )

                    resume_score = calculate_resume_score(
                        text,
                        profile_skills,
                    )

                    missing = sorted(
                        set(job_skills)
                        - set(profile_skills)
                    )

                    candidate_name = extract_name(
                        text
                    )

                    if candidate_name == "Candidate":
                        candidate_name = candidate.name

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
                    len(result_df) + 1
                ),
            )

            shortlist_count = min(
                int(top_n),
                len(result_df),
            )

            shortlist = result_df.head(
                shortlist_count
            ).copy()

            st.session_state.recruiter_results = (
                result_df
            )

            st.session_state.recruiter_shortlist = (
                shortlist
            )

            st.success(
                f"Screening completed. "
                f"{len(result_df)} resumes analyzed."
            )

    # ========================================================
    # RESULTS
    # ========================================================

    if st.session_state.recruiter_results is not None:

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

        st.subheader(
            "3. AI Candidate Ranking"
        )

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(
                "Resumes Screened",
                len(result_df),
            )

        with c2:

            st.metric(
                "Shortlisted",
                len(shortlist),
            )

        with c3:

            best_match = (
                int(
                    result_df.iloc[0][
                        "Overall Match"
                    ]
                )
                if len(result_df)
                else 0
            )

            st.metric(
                "Best Match",
                f"{best_match}%",
            )

        st.write(
            "### 🏆 Shortlisted Candidates"
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

        # ====================================================
        # CANDIDATE DETAILS
        # ====================================================

        st.subheader(
            "4. Candidate Intelligence"
        )

        candidates = shortlist[
            "Candidate"
        ].tolist()

        if candidates:

            selected_candidate = st.selectbox(
                "Select Candidate",
                candidates,
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

            st.write(
                "**Detected Skills**"
            )

            st.write(
                selected["Skills"]
                or "None detected"
            )

            st.write(
                "**Missing Skills**"
            )

            st.write(
                selected["Missing Skills"]
                or "No major predefined skill gaps"
            )

        st.divider()

        # ====================================================
        # EXPORT
        # ====================================================

        st.subheader(
            "5. Export Shortlist"
        )

        csv_data = shortlist.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="⬇️ Download Shortlist CSV",
            data=csv_data,
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
    "& Recruitment Platform • Final Year Project • AI • ML • NLP"
)
