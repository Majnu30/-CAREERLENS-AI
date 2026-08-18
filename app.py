import io
import re
import html as html_lib
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

from pypdf import PdfReader
from docx import Document

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


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
# SESSION STATE
# ============================================================

DEFAULTS = {
    "workspace": "Job Seeker",
    "seeker_page": "Dashboard",
    "recruiter_page": "Dashboard",
    "resume_profile": None,
    "job_analysis": None,
    "job_text": "",
    "job_title": "",
    "candidate_df": None,
    "shortlisted": [],
    "applications": [],
    "created_jobs": [],
    "selected_candidates": [],
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# SAFE HTML HELPER
# ============================================================

def render_html(content: str):
    """
    Prevents Streamlit from treating indented HTML as Markdown
    code blocks.
    """
    st.markdown(
        content.strip(),
        unsafe_allow_html=True
    )


# ============================================================
# SVG LOGO
# ============================================================

def logo_svg(size=48):
    return f"""
    <svg width="{size}" height="{size}" viewBox="0 0 100 100"
         xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="cg" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#8B7CFF"/>
                <stop offset="100%" stop-color="#38BDF8"/>
            </linearGradient>
        </defs>

        <rect x="4" y="4" width="92" height="92" rx="26"
              fill="#111C30"
              stroke="#293B5C"
              stroke-width="3"/>

        <circle cx="50" cy="50" r="27"
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

        <circle cx="50" cy="50" r="7"
                fill="#FFFFFF"/>
    </svg>
    """


# ============================================================
# GLOBAL CSS
# ============================================================

render_html("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 80% 0%,
            rgba(99, 102, 241, 0.08),
            transparent 30%
        ),
        #070B14;
    color: #F8FAFC;
}

.main .block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

[data-testid="stHeader"] {
    background: transparent;
}

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #0B1220 0%,
            #080E19 100%
        );
    border-right: 1px solid #1D2A40;
}

section[data-testid="stSidebar"] .block-container {
    padding: 1.5rem 1.1rem;
}

hr {
    border-color: #1D2A40 !important;
}

.brand {
    text-align: center;
    padding: 8px 0 20px;
}

.brand-logo {
    margin-bottom: 12px;
}

.brand-name {
    font-size: 25px;
    font-weight: 800;
    letter-spacing: -0.8px;
}

.brand-name span {
    background:
        linear-gradient(
            90deg,
            #9B8CFF,
            #38BDF8
        );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.brand-subtitle {
    color: #75839B;
    font-size: 10px;
    margin-top: 6px;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.sidebar-heading {
    color: #64748B;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.4px;
    text-transform: uppercase;
    margin: 12px 0 8px;
}

.hero {
    position: relative;
    overflow: hidden;

    background:
        radial-gradient(
            circle at 90% 15%,
            rgba(139,124,255,.18),
            transparent 32%
        ),
        radial-gradient(
            circle at 70% 100%,
            rgba(56,189,248,.08),
            transparent 35%
        ),
        linear-gradient(
            135deg,
            #111C30,
            #0B1322
        );

    border: 1px solid #253652;
    border-radius: 26px;

    padding: 50px;

    margin-bottom: 30px;

    box-shadow:
        0 25px 70px rgba(0,0,0,.28);
}

.hero-kicker {
    color: #A79BFF;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    margin-bottom: 13px;
}

.hero-title {
    font-size: 48px;
    line-height: 1.08;
    font-weight: 850;
    letter-spacing: -2px;
}

.gradient {
    background:
        linear-gradient(
            90deg,
            #A99BFF,
            #38BDF8
        );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-description {
    color: #94A3B8;
    max-width: 850px;
    font-size: 15px;
    line-height: 1.8;
    margin-top: 20px;
}

.section-title {
    color: #F8FAFC;
    font-size: 27px;
    font-weight: 800;
    letter-spacing: -.6px;
    margin-top: 25px;
}

.section-subtitle {
    color: #718096;
    font-size: 13px;
    margin: 5px 0 20px;
}

.metric {
    background:
        linear-gradient(
            145deg,
            #111C2D,
            #0D1625
        );

    border: 1px solid #23334D;
    border-radius: 18px;

    padding: 22px;

    min-height: 125px;

    box-shadow:
        0 12px 35px rgba(0,0,0,.16);
}

.metric-label {
    color: #7E8CA4;
    font-size: 12px;
    font-weight: 600;
}

.metric-value {
    color: #F8FAFC;
    font-size: 31px;
    font-weight: 850;
    margin-top: 8px;
}

.metric-note {
    color: #5EE7B7;
    font-size: 10px;
    margin-top: 6px;
}

.card {
    background:
        linear-gradient(
            145deg,
            #101A2B,
            #0D1625
        );

    border: 1px solid #22324B;
    border-radius: 18px;

    padding: 23px;

    margin-bottom: 18px;

    box-shadow:
        0 12px 35px rgba(0,0,0,.12);
}

.card-title {
    color: #F8FAFC;
    font-size: 17px;
    font-weight: 750;
    margin-bottom: 7px;
}

.card-text {
    color: #8C9AB0;
    font-size: 13px;
    line-height: 1.65;
}

.feature {
    background:
        linear-gradient(
            145deg,
            #101A2B,
            #0C1422
        );

    border: 1px solid #22324B;
    border-radius: 18px;

    padding: 24px;

    min-height: 180px;

    margin-bottom: 18px;

    transition: all .2s ease;
}

.feature:hover {
    border-color: #52658B;
    transform: translateY(-2px);
}

.feature-icon {
    font-size: 30px;
    margin-bottom: 13px;
}

.feature-title {
    font-size: 16px;
    font-weight: 750;
    color: #F8FAFC;
    margin-bottom: 8px;
}

.feature-text {
    color: #8491A7;
    font-size: 12px;
    line-height: 1.65;
}

.badge {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 99px;
    background: #19253A;
    color: #AAB7CA;
    font-size: 10px;
    font-weight: 700;
    margin: 3px;
}

.badge-good {
    background: #0D3024;
    color: #5EE7B7;
}

.badge-warn {
    background: #332A0D;
    color: #FACC15;
}

.badge-danger {
    background: #35151A;
    color: #FB7185;
}

.status-online {
    text-align: center;
    color: #5EE7B7;
    background: #0B261D;
    border: 1px solid #194F3C;
    border-radius: 10px;
    padding: 9px;
    font-size: 11px;
    font-weight: 700;
}

.score-circle {
    text-align: center;
    background:
        radial-gradient(
            circle,
            #18253B,
            #0E1727
        );
    border: 1px solid #314563;
    border-radius: 50%;
    width: 150px;
    height: 150px;
    padding-top: 38px;
    margin: auto;
}

.score-number {
    color: #F8FAFC;
    font-size: 38px;
    font-weight: 850;
}

.score-label {
    color: #8290A5;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.warning-box {
    background: #281F0A;
    border: 1px solid #625019;
    border-radius: 14px;
    padding: 17px;
    color: #FDE68A;
    font-size: 13px;
    line-height: 1.6;
}

.success-box {
    background: #09241B;
    border: 1px solid #1A5841;
    border-radius: 14px;
    padding: 17px;
    color: #6EE7B7;
    font-size: 13px;
}

.danger-box {
    background: #2A1015;
    border: 1px solid #692530;
    border-radius: 14px;
    padding: 17px;
    color: #FDA4AF;
    font-size: 13px;
}

.info-box {
    background: #101C30;
    border: 1px solid #243A5B;
    border-radius: 14px;
    padding: 17px;
    color: #93C5FD;
    font-size: 13px;
    line-height: 1.6;
}

.footer {
    border-top: 1px solid #1C293D;
    margin-top: 60px;
    padding: 25px 0;
    text-align: center;
    color: #59677D;
    font-size: 11px;
    line-height: 1.8;
}

.stButton > button {
    border-radius: 11px;
    min-height: 43px;
    font-weight: 700;
    border: 1px solid #2A3B59;
    background: #111C2E;
    color: #F8FAFC;
}

.stButton > button:hover {
    border-color: #8B7CFF;
    color: #FFFFFF;
}

[data-testid="stFileUploader"] {
    background: #0D1727;
    border: 1px dashed #314563;
    border-radius: 14px;
}

input, textarea {
    border-radius: 10px !important;
}

@media (max-width: 800px) {
    .hero {
        padding: 30px;
    }

    .hero-title {
        font-size: 34px;
    }
}

</style>
""")


# ============================================================
# DATA / NLP ENGINE
# ============================================================

SKILL_LIBRARY = {
    "Python": ["python"],
    "Java": ["java"],
    "C": [r"\bc\b"],
    "C++": ["c++", "cpp"],
    "JavaScript": ["javascript", "js"],
    "TypeScript": ["typescript"],
    "HTML": ["html"],
    "CSS": ["css"],
    "React": ["react", "reactjs"],
    "Node.js": ["node.js", "nodejs"],
    "SQL": ["sql", "mysql", "postgresql", "postgres"],
    "MongoDB": ["mongodb", "mongo db"],
    "Git": ["git", "github", "gitlab"],
    "Docker": ["docker", "containerization"],
    "Kubernetes": ["kubernetes", "k8s"],
    "AWS": ["aws", "amazon web services"],
    "Azure": ["azure"],
    "GCP": ["google cloud", "gcp"],
    "Machine Learning": [
        "machine learning",
        "machine-learning"
    ],
    "Deep Learning": [
        "deep learning",
        "deep-learning"
    ],
    "Artificial Intelligence": [
        "artificial intelligence",
        "artificial intelligence"
    ],
    "NLP": [
        "natural language processing",
        "nlp"
    ],
    "Computer Vision": [
        "computer vision",
        "opencv"
    ],
    "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch"],
    "Scikit-learn": [
        "scikit-learn",
        "sklearn"
    ],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Power BI": ["power bi"],
    "Tableau": ["tableau"],
    "Excel": ["excel", "microsoft excel"],
    "Figma": ["figma"],
    "UI/UX": ["ui/ux", "user experience"],
    "REST API": [
        "rest api",
        "restful api"
    ],
    "FastAPI": ["fastapi"],
    "Flask": ["flask"],
    "Django": ["django"],
    "Spring Boot": ["spring boot"],
    "Data Analysis": [
        "data analysis",
        "data analytics"
    ],
    "Data Science": ["data science"],
    "Statistics": [
        "statistics",
        "statistical analysis"
    ],
    "Agile": ["agile", "scrum"],
    "Communication": ["communication"],
    "Leadership": ["leadership"],
    "Problem Solving": [
        "problem solving",
        "problem-solving"
    ],
}


def normalize_text(text):
    if not text:
        return ""

    text = text.replace("\x00", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_pdf_text(file_bytes):
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        pages = []

        for page in reader.pages:
            text = page.extract_text() or ""
            pages.append(text)

        return normalize_text("\n".join(pages))

    except Exception as exc:
        return f"[PDF extraction error: {exc}]"


def extract_docx_text(file_bytes):
    try:
        document = Document(io.BytesIO(file_bytes))

        parts = []

        for paragraph in document.paragraphs:
            if paragraph.text:
                parts.append(paragraph.text)

        for table in document.tables:
            for row in table.rows:
                parts.append(
                    " ".join(
                        cell.text
                        for cell in row.cells
                    )
                )

        return normalize_text("\n".join(parts))

    except Exception as exc:
        return f"[DOCX extraction error: {exc}]"


def extract_text_from_file(uploaded_file):
    if uploaded_file is None:
        return ""

    suffix = Path(uploaded_file.name).suffix.lower()
    data = uploaded_file.getvalue()

    if suffix == ".pdf":
        return extract_pdf_text(data)

    if suffix == ".docx":
        return extract_docx_text(data)

    if suffix == ".txt":
        try:
            return normalize_text(
                data.decode(
                    "utf-8",
                    errors="ignore"
                )
            )
        except Exception:
            return ""

    return ""


def extract_skills(text):
    text_lower = text.lower()
    found = []

    for skill, patterns in SKILL_LIBRARY.items():

        for pattern in patterns:

            try:
                if re.search(
                    pattern,
                    text_lower,
                    flags=re.IGNORECASE
                ):
                    found.append(skill)
                    break

            except re.error:
                if pattern.lower() in text_lower:
                    found.append(skill)
                    break

    return sorted(
        set(found),
        key=lambda x: x.lower()
    )


def extract_email(text):
    match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    return match.group(0) if match else ""


def extract_phone(text):
    match = re.search(
        r"(?:\+?\d[\d\s().-]{7,}\d)",
        text
    )

    return match.group(0).strip() if match else ""


def extract_experience_years(text):
    patterns = [
        r"(\d+(?:\.\d+)?)\+?\s*(?:years|year)\s+(?:of\s+)?experience",
        r"experience\s*[:\-]?\s*(\d+(?:\.\d+)?)\+?\s*(?:years|year)",
    ]

    values = []

    for pattern in patterns:
        matches = re.findall(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        for value in matches:
            try:
                values.append(float(value))
            except ValueError:
                pass

    return max(values) if values else 0.0


def extract_education(text):
    education_keywords = [
        "b.tech",
        "btech",
        "b.e.",
        "be ",
        "bachelor",
        "m.tech",
        "mtech",
        "master",
        "mca",
        "mba",
        "phd",
        "computer science",
        "information technology",
        "engineering",
    ]

    lower = text.lower()

    return [
        keyword
        for keyword in education_keywords
        if keyword in lower
    ]


def section_presence(text):
    lower = text.lower()

    sections = {
        "summary": [
            "summary",
            "profile",
            "objective"
        ],
        "experience": [
            "experience",
            "employment",
            "work history"
        ],
        "education": [
            "education",
            "academic"
        ],
        "skills": [
            "skills",
            "technical skills",
            "technologies"
        ],
        "projects": [
            "projects",
            "project experience"
        ],
        "certifications": [
            "certification",
            "certifications"
        ],
    }

    result = {}

    for name, keywords in sections.items():
        result[name] = any(
            keyword in lower
            for keyword in keywords
        )

    return result


def calculate_resume_score(text, skills):
    if not text:
        return 0

    sections = section_presence(text)

    score = 0

    # Contact information
    if extract_email(text):
        score += 10

    if extract_phone(text):
        score += 5

    # Skills
    score += min(
        len(skills) * 2,
        25
    )

    # Sections
    for value in sections.values():
        if value:
            score += 5

    # Experience
    if extract_experience_years(text) > 0:
        score += 5

    # Reasonable content length
    word_count = len(text.split())

    if word_count >= 250:
        score += 5

    if word_count >= 500:
        score += 5

    return int(
        min(score, 100)
    )


def analyze_resume(file_name, text):
    skills = extract_skills(text)

    sections = section_presence(text)

    score = calculate_resume_score(
        text,
        skills
    )

    return {
        "name": Path(file_name).stem.replace(
            "_",
            " "
        ),
        "file_name": file_name,
        "text": text,
        "skills": skills,
        "email": extract_email(text),
        "phone": extract_phone(text),
        "experience_years": extract_experience_years(text),
        "education": extract_education(text),
        "sections": sections,
        "score": score,
        "word_count": len(text.split()),
    }


# ============================================================
# JOB MATCHING ENGINE
# ============================================================

def calculate_text_similarity(text_a, text_b):

    if not text_a.strip() or not text_b.strip():
        return 0.0

    try:

        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=7000,
        )

        matrix = vectorizer.fit_transform(
            [text_a, text_b]
        )

        similarity = cosine_similarity(
            matrix[0:1],
            matrix[1:2]
        )[0][0]

        return float(
            max(
                0,
                min(
                    similarity * 100,
                    100
                )
            )
        )

    except Exception:
        return 0.0


def skill_match(resume_skills, job_text):

    job_skills = extract_skills(
        job_text
    )

    resume_set = set(
        skill.lower()
        for skill in resume_skills
    )

    job_set = set(
        skill.lower()
        for skill in job_skills
    )

    if not job_set:
        return 0.0, [], []

    matched = sorted(
        resume_set.intersection(job_set)
    )

    missing = sorted(
        job_set.difference(resume_set)
    )

    percentage = (
        len(matched) /
        len(job_set)
    ) * 100

    return (
        percentage,
        matched,
        missing
    )


def calculate_match(resume_text, job_text):

    resume_skills = extract_skills(
        resume_text
    )

    text_score = calculate_text_similarity(
        resume_text,
        job_text
    )

    skill_score, matched, missing = skill_match(
        resume_skills,
        job_text
    )

    # Weighted NLP score
    final_score = (
        text_score * 0.55
        +
        skill_score * 0.45
    )

    return {
        "match_score": round(
            final_score,
            1
        ),
        "text_similarity": round(
            text_score,
            1
        ),
        "skill_match": round(
            skill_score,
            1
        ),
        "matched_skills": matched,
        "missing_skills": missing,
    }


# ============================================================
# FRAUD DETECTION ENGINE
# ============================================================

FRAUD_RULES = [
    (
        "payment",
        [
            "pay a fee",
            "registration fee",
            "processing fee",
            "pay money",
            "deposit money",
            "security deposit",
            "training fee",
        ],
        25,
        "The posting asks the applicant for money."
    ),
    (
        "financial",
        [
            "bank account",
            "bank details",
            "credit card",
            "debit card",
            "otp",
            "one time password",
        ],
        20,
        "The posting requests sensitive financial information."
    ),
    (
        "crypto",
        [
            "bitcoin",
            "cryptocurrency",
            "crypto payment",
            "usdt",
            "ethereum",
        ],
        20,
        "The posting contains cryptocurrency-related payment signals."
    ),
    (
        "gift_card",
        [
            "gift card",
            "gift cards",
            "itunes card",
            "google play card",
        ],
        20,
        "The posting mentions gift-card transactions."
    ),
    (
        "urgency",
        [
            "act immediately",
            "urgent hiring",
            "limited slots",
            "apply immediately",
            "respond immediately",
        ],
        10,
        "The posting uses strong urgency language."
    ),
    (
        "messaging",
        [
            "telegram",
            "whatsapp",
            "signal app",
            "contact me on",
        ],
        10,
        "The recruitment process relies heavily on external messaging."
    ),
    (
        "unrealistic",
        [
            "earn $5000 per week",
            "earn 10000 per week",
            "guaranteed income",
            "guaranteed salary",
            "no experience needed",
            "easy money",
        ],
        15,
        "The posting contains potentially unrealistic employment claims."
    ),
]


def fraud_detection(text):

    lower = text.lower()

    score = 0
    signals = []

    for (
        category,
        keywords,
        points,
        reason
    ) in FRAUD_RULES:

        matched = [
            keyword
            for keyword in keywords
            if keyword in lower
        ]

        if matched:

            score += points

            signals.append({
                "category": category,
                "matched": matched,
                "reason": reason,
                "points": points,
            })

    # Generic email warning
    emails = re.findall(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    for email in emails:

        free_domains = [
            "gmail.com",
            "yahoo.com",
            "hotmail.com",
            "outlook.com",
        ]

        if any(
            domain in email.lower()
            for domain in free_domains
        ):

            score += 8

            signals.append({
                "category": "email",
                "matched": [email],
                "reason": (
                    "The recruiter appears to use a free email "
                    "domain rather than a company domain."
                ),
                "points": 8,
            })

            break

    score = min(
        score,
        100
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
        "signals": signals,
    }


# ============================================================
# CANDIDATE RANKING
# ============================================================

def rank_candidates(
    candidate_profiles,
    job_text,
    top_n
):

    rows = []

    for candidate in candidate_profiles:

        match = calculate_match(
            candidate["text"],
            job_text
        )

        final_score = (
            match["match_score"] * 0.65
            +
            candidate["score"] * 0.20
            +
            min(
                candidate["experience_years"] * 3,
                15
            )
        )

        rows.append({
            "Candidate": candidate["name"],
            "Resume Score": candidate["score"],
            "Match Score": match["match_score"],
            "Skill Match": match["skill_match"],
            "Experience": candidate["experience_years"],
            "Skills": ", ".join(
                candidate["skills"]
            ),
            "Matched Skills": ", ".join(
                match["matched_skills"]
            ),
            "Missing Skills": ", ".join(
                match["missing_skills"]
            ),
            "Final Score": round(
                final_score,
                1
            ),
            "Email": candidate["email"],
            "File": candidate["file_name"],
        })

    dataframe = pd.DataFrame(rows)

    if dataframe.empty:
        return dataframe

    dataframe = dataframe.sort_values(
        "Final Score",
        ascending=False
    ).reset_index(
        drop=True
    )

    dataframe.insert(
        0,
        "Rank",
        range(
            1,
            len(dataframe) + 1
        )
    )

    dataframe["Decision"] = np.where(
        dataframe["Rank"] <= top_n,
        "SHORTLIST",
        "REVIEW"
    )

    return dataframe


# ============================================================
# HELPER UI FUNCTIONS
# ============================================================

def metric_card(label, value, note=""):
    return f"""
    <div class="metric">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-note">{note}</div>
    </div>
    """


def feature_card(icon, title, description):
    return f"""
    <div class="feature">
        <div class="feature-icon">{icon}</div>
        <div class="feature-title">{title}</div>
        <div class="feature-text">{description}</div>
    </div>
    """


def badge(text, style=""):
    safe = html_lib.escape(str(text))
    return (
        f'<span class="badge {style}">{safe}</span>'
    )


def score_color_class(score):
    if score >= 75:
        return "good"
    if score >= 50:
        return "warn"
    return "danger"


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    render_html(
        f"""
        <div class="brand">
            <div class="brand-logo">
                {logo_svg(54)}
            </div>

            <div class="brand-name">
                Career<span>Lens</span> AI
            </div>

            <div class="brand-subtitle">
                Career Intelligence Platform
            </div>
        </div>
        """
    )

    st.divider()

    render_html(
        '<div class="sidebar-heading">Workspace</div>'
    )

    workspace = st.radio(
        "Workspace",
        [
            "Job Seeker",
            "Recruiter"
        ],
        index=(
            0
            if st.session_state.workspace
            == "Job Seeker"
            else 1
        ),
        label_visibility="collapsed",
    )

    st.session_state.workspace = workspace

    st.divider()

    if workspace == "Job Seeker":

        render_html(
            '<div class="sidebar-heading">👨‍💻 Job Seeker</div>'
        )

        pages = [
            "Dashboard",
            "Resume Analyzer",
            "Job Analyzer",
            "Job Fraud Detection",
            "Job Matching",
            "Skill Gap Analysis",
            "Career Roadmap",
            "Application Tracker",
            "AI Career Assistant",
        ]

        page = st.radio(
            "Navigation",
            pages,
            index=pages.index(
                st.session_state.seeker_page
            ),
            label_visibility="collapsed",
        )

        st.session_state.seeker_page = page

    else:

        render_html(
            '<div class="sidebar-heading">🧑‍💼 Recruiter</div>'
        )

        pages = [
            "Dashboard",
            "Create Job",
            "Bulk Resume Upload",
            "Candidate Ranking",
            "Candidate Comparison",
            "Shortlist",
            "Recruitment Pipeline",
            "Hiring Analytics",
            "AI Recruiter Assistant",
        ]

        page = st.radio(
            "Navigation",
            pages,
            index=pages.index(
                st.session_state.recruiter_page
            ),
            label_visibility="collapsed",
        )

        st.session_state.recruiter_page = page

    st.divider()

    render_html(
        """
        <div class="status-online">
            ● AI ENGINE ONLINE
        </div>
        """
    )


# ============================================================
# JOB SEEKER — DASHBOARD
# ============================================================

if workspace == "Job Seeker" and page == "Dashboard":

    render_html(
        """
        <div class="hero">

            <div class="hero-kicker">
                AI Career Intelligence
            </div>

            <div class="hero-title">
                Understand Your Career.
                <br>
                <span class="gradient">
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
        """
    )

    profile = st.session_state.resume_profile

    resume_score = (
        profile["score"]
        if profile
        else "—"
    )

    skill_count = (
        len(profile["skills"])
        if profile
        else 0
    )

    render_html(
        """
        <div class="section-title">
            Career Overview
        </div>

        <div class="section-subtitle">
            Your career intelligence at a glance.
        </div>
        """
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        render_html(
            metric_card(
                "Resume Score",
                resume_score,
                "AI resume analysis"
            )
        )

    with c2:
        readiness = (
            min(
                100,
                resume_score
            )
            if isinstance(
                resume_score,
                int
            )
            else "—"
        )

        render_html(
            metric_card(
                "Career Readiness",
                readiness,
                "Based on current profile"
            )
        )

    with c3:
        render_html(
            metric_card(
                "Skills Detected",
                skill_count,
                "Extracted from resume"
            )
        )

    with c4:
        render_html(
            metric_card(
                "Applications",
                len(
                    st.session_state.applications
                ),
                "Tracked applications"
            )
        )

    render_html(
        """
        <div class="section-title">
            Career Intelligence
        </div>

        <div class="section-subtitle">
            AI-powered tools for smarter career decisions.
        </div>
        """
    )

    features = [
        (
            "📄",
            "Resume Intelligence",
            "Extract skills, experience, education, projects "
            "and contact information from your resume."
        ),
        (
            "🎯",
            "AI Job Matching",
            "Compare your profile with job descriptions using "
            "NLP similarity and skill matching."
        ),
        (
            "🔎",
            "Job Intelligence",
            "Analyze job requirements and understand which "
            "skills are important."
        ),
        (
            "🛡️",
            "Job Fraud Detection",
            "Detect suspicious payment, financial, urgency and "
            "communication signals."
        ),
        (
            "🧩",
            "Skill Gap Analysis",
            "Find missing skills between your profile and "
            "your target job."
        ),
        (
            "🗺️",
            "Career Roadmap",
            "Generate a structured path toward your target "
            "career."
        ),
    ]

    cols = st.columns(3)

    for i, feature in enumerate(features):

        with cols[i % 3]:
            render_html(
                feature_card(*feature)
            )


# ============================================================
# JOB SEEKER — RESUME ANALYZER
# ============================================================

elif workspace == "Job Seeker" and page == "Resume Analyzer":

    render_html(
        """
        <div class="section-title">
            📄 Resume Intelligence
        </div>

        <div class="section-subtitle">
            Upload your resume and let the NLP engine build
            your professional profile.
        </div>
        """
    )

    uploaded = st.file_uploader(
        "Upload Resume",
        type=[
            "pdf",
            "docx",
            "txt"
        ],
        help="PDF, DOCX and TXT are supported."
    )

    if uploaded:

        with st.spinner(
            "CareerLens AI is reading your resume..."
        ):

            text = extract_text_from_file(
                uploaded
            )

            profile = analyze_resume(
                uploaded.name,
                text
            )

            st.session_state.resume_profile = profile

        if text.startswith("["):

            st.error(text)

        elif len(text) < 50:

            st.warning(
                "Very little text could be extracted. "
                "If this is a scanned PDF, OCR will be needed "
                "for a future version."
            )

        else:

            st.success(
                "Resume successfully analyzed."
            )

            c1, c2, c3 = st.columns(3)

            with c1:
                render_html(
                    metric_card(
                        "Resume Score",
                        f"{profile['score']}/100",
                        "Overall profile quality"
                    )
                )

            with c2:
                render_html(
                    metric_card(
                        "Skills",
                        len(profile["skills"]),
                        "Detected skills"
                    )
                )

            with c3:
                render_html(
                    metric_card(
                        "Experience",
                        f"{profile['experience_years']:.1f} yrs",
                        "Detected experience"
                    )
                )

            st.write("")

            left, right = st.columns(
                [1, 1]
            )

            with left:

                render_html(
                    """
                    <div class="card">
                        <div class="card-title">
                            🧠 Detected Skills
                        </div>
                    </div>
                    """
                )

                if profile["skills"]:

                    skill_html = "".join(
                        badge(
                            skill,
                            "badge-good"
                        )
                        for skill in profile["skills"]
                    )

                    render_html(
                        f'<div>{skill_html}</div>'
                    )

                else:

                    st.info(
                        "No skills were detected from the "
                        "current skill library."
                    )

            with right:

                render_html(
                    """
                    <div class="card">
                        <div class="card-title">
                            👤 Profile Information
                        </div>
                    </div>
                    """
                )

                st.write(
                    f"**Name:** {profile['name']}"
                )

                st.write(
                    f"**Email:** {profile['email'] or 'Not detected'}"
                )

                st.write(
                    f"**Phone:** {profile['phone'] or 'Not detected'}"
                )

                st.write(
                    f"**Words:** {profile['word_count']}"
                )

            render_html(
                """
                <div class="section-title">
                    Resume Structure
                </div>
                """
            )

            structure = profile["sections"]

            structure_df = pd.DataFrame({
                "Section": [
                    name.title()
                    for name in structure
                ],
                "Detected": [
                    "Yes"
                    if value
                    else "No"
                    for value in structure.values()
                ],
            })

            st.dataframe(
                structure_df,
                use_container_width=True,
                hide_index=True,
            )

            render_html(
                """
                <div class="section-title">
                    Extracted Education Signals
                </div>
                """
            )

            if profile["education"]:

                for item in profile["education"]:
                    render_html(
                        badge(
                            item.upper(),
                            "badge-good"
                        )
                    )

            else:

                st.info(
                    "No education keywords were detected."
                )


# ============================================================
# JOB SEEKER — JOB ANALYZER
# ============================================================

elif workspace == "Job Seeker" and page == "Job Analyzer":

    render_html(
        """
        <div class="section-title">
            🔎 Job Intelligence
        </div>

        <div class="section-subtitle">
            Understand the requirements of a job before applying.
        </div>
        """
    )

    job_title = st.text_input(
        "Job Title",
        placeholder="Machine Learning Engineer"
    )

    job_text = st.text_area(
        "Job Description",
        height=300,
        placeholder=(
            "Paste the complete job description here..."
        )
    )

    if st.button(
        "🔍 Analyze Job",
        use_container_width=True
    ):

        if len(job_text.strip()) < 30:

            st.warning(
                "Please provide a more complete job description."
            )

        else:

            skills = extract_skills(
                job_text
            )

            fraud = fraud_detection(
                job_text
            )

            st.session_state.job_text = job_text
            st.session_state.job_title = job_title
            st.session_state.job_analysis = {
                "skills": skills,
                "fraud": fraud,
            }

            c1, c2, c3 = st.columns(3)

            with c1:
                render_html(
                    metric_card(
                        "Skills Required",
                        len(skills),
                        "Detected by NLP"
                    )
                )

            with c2:
                render_html(
                    metric_card(
                        "Risk Score",
                        fraud["score"],
                        fraud["level"]
                    )
                )

            with c3:
                render_html(
                    metric_card(
                        "Text Length",
                        len(job_text.split()),
                        "Words analyzed"
                    )
                )

            render_html(
                """
                <div class="section-title">
                    Required Skills
                </div>
                """
            )

            if skills:

                render_html(
                    "".join(
                        badge(
                            skill,
                            "badge-good"
                        )
                        for skill in skills
                    )
                )

            else:

                st.info(
                    "No known skills were detected."
                )

            render_html(
                """
                <div class="section-title">
                    Job Risk Assessment
                </div>
                """
            )

            fraud = fraud["score"]

            if fraud >= 60:

                render_html(
                    """
                    <div class="danger-box">
                        🚨 High-risk signals detected.
                        Review the posting carefully before
                        sharing personal information or making
                        payments.
                    </div>
                    """
                )

            elif fraud >= 30:

                render_html(
                    """
                    <div class="warning-box">
                        ⚠️ Some suspicious signals were detected.
                        Perform additional verification before
                        applying.
                    </div>
                    """
                )

            else:

                render_html(
                    """
                    <div class="success-box">
                        ✓ No major predefined fraud signals
                        were detected by the current engine.
                    </div>
                    """
                )


# ============================================================
# JOB SEEKER — FRAUD DETECTION
# ============================================================

elif workspace == "Job Seeker" and page == "Job Fraud Detection":

    render_html(
        """
        <div class="section-title">
            🛡️ Job Fraud Detection
        </div>

        <div class="section-subtitle">
            Analyze suspicious signals in a job posting.
        </div>
        """
    )

    fraud_text = st.text_area(
        "Paste Job Posting",
        height=320,
        placeholder="Paste the complete job posting here..."
    )

    if st.button(
        "🛡️ Scan For Fraud Signals",
        use_container_width=True
    ):

        if len(fraud_text.strip()) < 30:

            st.warning(
                "Please provide the job posting."
            )

        else:

            result = fraud_detection(
                fraud_text
            )

            c1, c2 = st.columns(2)

            with c1:

                render_html(
                    f"""
                    <div class="score-circle">
                        <div class="score-number">
                            {result['score']}
                        </div>
                        <div class="score-label">
                            Risk Score
                        </div>
                    </div>
                    """
                )

            with c2:

                if result["level"] == "HIGH RISK":

                    render_html(
                        """
                        <div class="danger-box">
                            <b>HIGH RISK</b><br><br>
                            Multiple suspicious indicators
                            were detected.
                        </div>
                        """
                    )

                elif result["level"] == "MEDIUM RISK":

                    render_html(
                        """
                        <div class="warning-box">
                            <b>MEDIUM RISK</b><br><br>
                            Some suspicious indicators
                            were detected.
                        </div>
                        """
                    )

                else:

                    render_html(
                        """
                        <div class="success-box">
                            <b>LOW RISK</b><br><br>
                            No major predefined suspicious
                            indicators were detected.
                        </div>
                        """
                    )

            render_html(
                """
                <div class="section-title">
                    🔍 Detection Explanation
                </div>
                """
            )

            if not result["signals"]:

                st.success(
                    "No predefined suspicious signals detected."
                )

            else:

                for signal in result["signals"]:

                    render_html(
                        f"""
                        <div class="card">
                            <div class="card-title">
                                {html_lib.escape(
                                    signal["category"].upper()
                                )}
                            </div>

                            <div class="card-text">
                                {html_lib.escape(
                                    signal["reason"]
                                )}
                                <br><br>
                                <b>Matched:</b>
                                {html_lib.escape(
                                    ", ".join(
                                        signal["matched"]
                                    )
                                )}
                            </div>
                        </div>
                        """
                    )

            st.caption(
                "This is a risk-screening system, not a guarantee "
                "that a job is legitimate or fraudulent."
            )


# ============================================================
# JOB SEEKER — JOB MATCHING
# ============================================================

elif workspace == "Job Seeker" and page == "Job Matching":

    render_html(
        """
        <div class="section-title">
            🎯 AI Job Matching
        </div>

        <div class="section-subtitle">
            Compare your resume against a target opportunity.
        </div>
        """
    )

    profile = st.session_state.resume_profile

    if not profile:

        st.warning(
            "Upload and analyze your resume first."
        )

    else:

        job = st.text_area(
            "Target Job Description",
            height=320,
            placeholder="Paste the target job description..."
        )

        if st.button(
            "🎯 Calculate AI Match",
            use_container_width=True
        ):

            if len(job.strip()) < 30:

                st.warning(
                    "Please provide a job description."
                )

            else:

                result = calculate_match(
                    profile["text"],
                    job
                )

                st.session_state.job_text = job

                c1, c2, c3 = st.columns(3)

                with c1:
                    render_html(
                        metric_card(
                            "Overall Match",
                            f"{result['match_score']}%",
                            "Weighted NLP score"
                        )
                    )

                with c2:
                    render_html(
                        metric_card(
                            "Skill Match",
                            f"{result['skill_match']}%",
                            "Required skills"
                        )
                    )

                with c3:
                    render_html(
                        metric_card(
                            "Text Similarity",
                            f"{result['text_similarity']}%",
                            "TF-IDF similarity"
                        )
                    )

                render_html(
                    """
                    <div class="section-title">
                        Matching Skills
                    </div>
                    """
                )

                if result["matched_skills"]:

                    render_html(
                        "".join(
                            badge(
                                skill,
                                "badge-good"
                            )
                            for skill
                            in result["matched_skills"]
                        )
                    )

                else:

                    st.info(
                        "No direct skill matches detected."
                    )

                render_html(
                    """
                    <div class="section-title">
                        🧩 Skill Gaps
                    </div>
                    """
                )

                if result["missing_skills"]:

                    render_html(
                        "".join(
                            badge(
                                skill,
                                "badge-warn"
                            )
                            for skill
                            in result["missing_skills"]
                        )
                    )

                else:

                    st.success(
                        "No missing skills were detected from "
                        "the current skill library."
                    )


# ============================================================
# JOB SEEKER — SKILL GAP
# ============================================================

elif workspace == "Job Seeker" and page == "Skill Gap Analysis":

    render_html(
        """
        <div class="section-title">
            🧩 Skill Gap Analysis
        </div>

        <div class="section-subtitle">
            Discover what you need to learn for your target role.
        </div>
        """
    )

    profile = st.session_state.resume_profile

    current = ""

    if profile:
        current = ", ".join(
            profile["skills"]
        )

    current_skills = st.text_area(
        "Current Skills",
        value=current,
        height=150
    )

    target_skills = st.text_area(
        "Target Job / Required Skills",
        height=220,
        placeholder=(
            "Python, Machine Learning, NLP, SQL, Docker..."
        )
    )

    if st.button(
        "🧩 Analyze Skill Gap",
        use_container_width=True
    ):

        if not target_skills:

            st.warning(
                "Please enter target requirements."
            )

        else:

            current_set = set(
                extract_skills(
                    current_skills
                )
            )

            target_set = set(
                extract_skills(
                    target_skills
                )
            )

            matched = sorted(
                current_set.intersection(
                    target_set
                )
            )

            missing = sorted(
                target_set.difference(
                    current_set
                )
            )

            coverage = (
                len(matched) /
                len(target_set) *
                100
            ) if target_set else 0

            render_html(
                metric_card(
                    "Skill Coverage",
                    f"{coverage:.1f}%",
                    "Target skill coverage"
                )
            )

            render_html(
                """
                <div class="section-title">
                    Already Have
                </div>
                """
            )

            if matched:

                render_html(
                    "".join(
                        badge(
                            skill,
                            "badge-good"
                        )
                        for skill in matched
                    )
                )

            else:

                st.info(
                    "No matching skills detected."
                )

            render_html(
                """
                <div class="section-title">
                    Skills To Develop
                </div>
                """
            )

            if missing:

                render_html(
                    "".join(
                        badge(
                            skill,
                            "badge-warn"
                        )
                        for skill in missing
                    )
                )

            else:

                st.success(
                    "Excellent — no skill gaps detected."
                )


# ============================================================
# JOB SEEKER — CAREER ROADMAP
# ============================================================

elif workspace == "Job Seeker" and page == "Career Roadmap":

    render_html(
        """
        <div class="section-title">
            🗺️ Career Roadmap
        </div>

        <div class="section-subtitle">
            Build a practical roadmap for your target career.
        </div>
        """
    )

    target = st.text_input(
        "Target Career",
        placeholder="AI Engineer"
    )

    profile = st.session_state.resume_profile

    if profile:
        render_html(
            f"""
            <div class="info-box">
                Current profile contains
                <b>{len(profile['skills'])}</b>
                detected skills.
            </div>
            """
        )

    if st.button(
        "🗺️ Generate Roadmap",
        use_container_width=True
    ):

        if not target:

            st.warning(
                "Enter a target career."
            )

        else:

            steps = [
                (
                    "01",
                    "Foundation",
                    "Strengthen programming, computer science, "
                    "mathematics and communication fundamentals."
                ),
                (
                    "02",
                    "Core Technology",
                    f"Learn the core tools and technologies "
                    f"used in {target}."
                ),
                (
                    "03",
                    "Practical Projects",
                    "Build 2–4 meaningful projects that solve "
                    "real problems."
                ),
                (
                    "04",
                    "Portfolio",
                    "Publish your work on GitHub and create "
                    "a professional portfolio."
                ),
                (
                    "05",
                    "Interview Preparation",
                    "Practice technical, behavioral and "
                    "role-specific interviews."
                ),
                (
                    "06",
                    "Targeted Applications",
                    "Apply to roles that align with your "
                    "skills and demonstrated projects."
                ),
            ]

            for number, title, description in steps:

                render_html(
                    f"""
                    <div class="card">
                        <div class="card-title">
                            {number} · {title}
                        </div>
                        <div class="card-text">
                            {description}
                        </div>
                    </div>
                    """
                )


# ============================================================
# JOB SEEKER — APPLICATION TRACKER
# ============================================================

elif workspace == "Job Seeker" and page == "Application Tracker":

    render_html(
        """
        <div class="section-title">
            📋 Application Tracker
        </div>

        <div class="section-subtitle">
            Manage your job applications.
        </div>
        """
    )

    with st.form(
        "application_form",
        clear_on_submit=True
    ):

        company = st.text_input(
            "Company"
        )

        role = st.text_input(
            "Role"
        )

        status = st.selectbox(
            "Status",
            [
                "Applied",
                "Screening",
                "Interview",
                "Offer",
                "Rejected"
            ]
        )

        submitted = st.form_submit_button(
            "➕ Add Application",
            use_container_width=True
        )

        if submitted:

            if company and role:

                st.session_state.applications.append({
                    "Company": company,
                    "Role": role,
                    "Status": status,
                })

                st.success(
                    "Application added."
                )

            else:

                st.warning(
                    "Company and role are required."
                )

    if st.session_state.applications:

        df = pd.DataFrame(
            st.session_state.applications
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# JOB SEEKER — AI ASSISTANT
# ============================================================

elif workspace == "Job Seeker" and page == "AI Career Assistant":

    render_html(
        """
        <div class="section-title">
            🤖 AI Career Assistant
        </div>

        <div class="section-subtitle">
            Ask CareerLens AI about your profile and job search.
        </div>
        """
    )

    question = st.chat_input(
        "Ask about your career..."
    )

    if question:

        lower = question.lower()

        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):

            profile = st.session_state.resume_profile

            if profile and (
                "skill" in lower
                or "resume" in lower
            ):

                st.write(
                    f"Your current resume analysis contains "
                    f"{len(profile['skills'])} detected skills: "
                    f"{', '.join(profile['skills'][:12])}."
                )

            elif "fraud" in lower:

                st.write(
                    "Paste a job posting into Job Fraud Detection. "
                    "CareerLens will examine predefined risk signals "
                    "such as payment requests, sensitive financial "
                    "information and suspicious urgency."
                )

            elif "match" in lower:

                st.write(
                    "Use AI Job Matching to compare your resume "
                    "against a specific job description using "
                    "TF-IDF text similarity and skill overlap."
                )

            else:

                st.write(
                    "I can help you with resume analysis, job "
                    "matching, skill gaps, fraud-risk screening "
                    "and career planning. Choose a module from "
                    "the sidebar for a detailed analysis."
                )


# ============================================================
# RECRUITER — DASHBOARD
# ============================================================

elif workspace == "Recruiter" and page == "Dashboard":

    render_html(
        """
        <div class="hero">

            <div class="hero-kicker">
                AI Recruitment Intelligence
            </div>

            <div class="hero-title">
                Recruit Smarter.
                <br>
                <span class="gradient">
                    Hire Better.
                </span>
            </div>

            <div class="hero-description">
                Upload large batches of resumes, analyze
                candidate profiles, compare skills and
                experience, and let CareerLens AI rank the
                strongest candidates for your role.
            </div>

        </div>
        """
    )

    candidate_df = st.session_state.candidate_df

    total_candidates = (
        len(candidate_df)
        if candidate_df is not None
        else 0
    )

    shortlisted = len(
        st.session_state.shortlisted
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        render_html(
            metric_card(
                "Active Jobs",
                len(
                    st.session_state.created_jobs
                ),
                "Recruitment positions"
            )
        )

    with c2:
        render_html(
            metric_card(
                "Candidates",
                total_candidates,
                "Resumes processed"
            )
        )

    with c3:
        render_html(
            metric_card(
                "Shortlisted",
                shortlisted,
                "AI / recruiter selection"
            )
        )

    with c4:
        render_html(
            metric_card(
                "Interviews",
                sum(
                    1
                    for app in st.session_state.applications
                    if app.get("Status")
                    == "Interview"
                ),
                "Current pipeline"
            )
        )

    render_html(
        """
        <div class="section-title">
            Recruiter Intelligence
        </div>

        <div class="section-subtitle">
            A professional AI-assisted recruitment workflow.
        </div>
        """
    )

    features = [
        (
            "📋",
            "Create Job",
            "Define role, skills, experience and requirements."
        ),
        (
            "📂",
            "Bulk Resume Upload",
            "Process 10, 50, 100 or more resumes together."
        ),
        (
            "🧠",
            "AI Candidate Ranking",
            "Rank candidates using NLP and skill similarity."
        ),
        (
            "⚖️",
            "Candidate Comparison",
            "Compare top candidates side by side."
        ),
        (
            "⭐",
            "Shortlisting",
            "Recruiter controls exactly how many candidates "
            "to shortlist."
        ),
        (
            "📈",
            "Hiring Analytics",
            "Visualize candidate quality and recruitment data."
        ),
    ]

    cols = st.columns(3)

    for i, feature in enumerate(features):

        with cols[i % 3]:

            render_html(
                feature_card(*feature)
            )


# ============================================================
# RECRUITER — CREATE JOB
# ============================================================

elif workspace == "Recruiter" and page == "Create Job":

    render_html(
        """
        <div class="section-title">
            📋 Create Recruitment Job
        </div>

        <div class="section-subtitle">
            Define the job that CareerLens AI will use for
            candidate matching.
        </div>
        """
    )

    with st.form(
        "create_job_form"
    ):

        title = st.text_input(
            "Job Title",
            placeholder="Machine Learning Engineer"
        )

        company = st.text_input(
            "Company",
            placeholder="Your company"
        )

        minimum_experience = st.number_input(
            "Minimum Experience",
            min_value=0,
            max_value=30,
            value=0
        )

        description = st.text_area(
            "Complete Job Description",
            height=280,
            placeholder=(
                "Responsibilities, required skills, "
                "qualifications..."
            )
        )

        submit = st.form_submit_button(
            "💾 Save Job",
            use_container_width=True
        )

        if submit:

            if not title or not description:

                st.warning(
                    "Job title and description are required."
                )

            else:

                job = {
                    "title": title,
                    "company": company,
                    "experience": minimum_experience,
                    "description": description,
                    "skills": extract_skills(
                        description
                    ),
                }

                st.session_state.created_jobs.append(
                    job
                )

                st.session_state.job_text = description
                st.session_state.job_title = title

                st.success(
                    f"{title} is ready for candidate ranking."
                )

    if st.session_state.created_jobs:

        render_html(
            """
            <div class="section-title">
                Saved Jobs
            </div>
            """
        )

        for job in st.session_state.created_jobs:

            render_html(
                f"""
                <div class="card">
                    <div class="card-title">
                        {html_lib.escape(job['title'])}
                    </div>

                    <div class="card-text">
                        {html_lib.escape(job['company'])}
                        ·
                        {job['experience']}+ years
                        <br><br>
                        Skills:
                        {html_lib.escape(
                            ", ".join(job["skills"])
                        )}
                    </div>
                </div>
                """
            )


# ============================================================
# RECRUITER — BULK RESUME UPLOAD
# ============================================================

elif workspace == "Recruiter" and page == "Bulk Resume Upload":

    render_html(
        """
        <div class="section-title">
            📂 Bulk Candidate Processing
        </div>

        <div class="section-subtitle">
            Upload multiple resumes and build a searchable
            candidate pool.
        </div>
        """
    )

    resumes = st.file_uploader(
        "Upload Candidate Resumes",
        type=[
            "pdf",
            "docx",
            "txt"
        ],
        accept_multiple_files=True,
        help="Upload resumes in PDF, DOCX or TXT format."
    )

    if resumes:

        if st.button(
            "🧠 Process All Resumes",
            use_container_width=True
        ):

            profiles = []

            progress = st.progress(
                0
            )

            for i, resume in enumerate(
                resumes
            ):

                text = extract_text_from_file(
                    resume
                )

                if len(text) >= 20:

                    profiles.append(
                        analyze_resume(
                            resume.name,
                            text
                        )
                    )

                progress.progress(
                    (i + 1) /
                    len(resumes)
                )

            st.session_state.candidate_df = pd.DataFrame(
                profiles
            )

            st.success(
                f"{len(profiles)} candidates processed."
            )

    candidate_df = st.session_state.candidate_df

    if candidate_df is not None and not candidate_df.empty:

        preview = candidate_df[
            [
                "name",
                "score",
                "experience_years",
                "skills",
                "email"
            ]
        ].copy()

        preview.columns = [
            "Candidate",
            "Resume Score",
            "Experience",
            "Skills",
            "Email"
        ]

        st.dataframe(
            preview,
            use_container_width=True,
            hide_index=True
        )

        csv = preview.to_csv(
            index=False
        ).encode(
            "utf-8"
        )

        st.download_button(
            "⬇️ Export Candidate Pool CSV",
            csv,
            "candidate_pool.csv",
            "text/csv",
            use_container_width=True
        )


# ============================================================
# RECRUITER — CANDIDATE RANKING
# ============================================================

elif workspace == "Recruiter" and page == "Candidate Ranking":

    render_html(
        """
        <div class="section-title">
            🧠 AI Candidate Ranking
        </div>

        <div class="section-subtitle">
            Recruiter-controlled Top-N selection from a bulk
            candidate pool.
        </div>
        """
    )

    candidate_df = st.session_state.candidate_df

    if candidate_df is None or candidate_df.empty:

        st.warning(
            "Upload candidate resumes first."
        )

    else:

        saved_jobs = st.session_state.created_jobs

        if saved_jobs:

            job_options = [
                job["title"]
                for job in saved_jobs
            ]

            selected_job = st.selectbox(
                "Select Job",
                job_options
            )

            selected = next(
                job
                for job in saved_jobs
                if job["title"]
                == selected_job
            )

            job_text = selected["description"]

        else:

            job_text = st.text_area(
                "Job Description",
                value=st.session_state.job_text,
                height=220,
                placeholder="Paste job description..."
            )

        top_n = st.selectbox(
            "How many candidates should be shortlisted?",
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

        minimum_score = st.slider(
            "Minimum final score",
            0,
            100,
            50
        )

        if st.button(
            "🚀 Run AI Ranking",
            use_container_width=True
        ):

            if len(job_text.strip()) < 30:

                st.warning(
                    "A complete job description is required."
                )

            else:

                profiles = (
                    candidate_df
                    .to_dict("records")
                )

                ranking = rank_candidates(
                    profiles,
                    job_text,
                    top_n
                )

                ranking = ranking[
                    ranking["Final Score"]
                    >= minimum_score
                ].copy()

                st.session_state.ranked_df = ranking

                st.success(
                    f"AI ranking completed. "
                    f"Showing the strongest candidates."
                )

        ranking = st.session_state.get(
            "ranked_df"
        )

        if ranking is not None and not ranking.empty:

            render_html(
                """
                <div class="section-title">
                    🏆 Candidate Leaderboard
                </div>
                """
            )

            display_columns = [
                "Rank",
                "Candidate",
                "Resume Score",
                "Match Score",
                "Skill Match",
                "Experience",
                "Final Score",
                "Decision",
            ]

            st.dataframe(
                ranking[display_columns],
                use_container_width=True,
                hide_index=True
            )

            csv = ranking.to_csv(
                index=False
            ).encode(
                "utf-8"
            )

            st.download_button(
                "⬇️ Download AI Ranking",
                csv,
                "candidate_ranking.csv",
                "text/csv",
                use_container_width=True
            )


# ============================================================
# RECRUITER — COMPARISON
# ============================================================

elif workspace == "Recruiter" and page == "Candidate Comparison":

    render_html(
        """
        <div class="section-title">
            ⚖️ Candidate Comparison
        </div>

        <div class="section-subtitle">
            Compare your strongest candidates before making
            the final decision.
        </div>
        """
    )

    ranking = st.session_state.get(
        "ranked_df"
    )

    if ranking is None or ranking.empty:

        st.info(
            "Run AI Candidate Ranking first."
        )

    else:

        candidates = ranking[
            "Candidate"
        ].tolist()

        selected = st.multiselect(
            "Select candidates to compare",
            candidates,
            default=candidates[:min(3, len(candidates))]
        )

        if selected:

            comparison = ranking[
                ranking["Candidate"].isin(
                    selected
                )
            ][
                [
                    "Candidate",
                    "Resume Score",
                    "Match Score",
                    "Skill Match",
                    "Experience",
                    "Final Score",
                    "Matched Skills",
                    "Missing Skills"
                ]
            ]

            st.dataframe(
                comparison,
                use_container_width=True,
                hide_index=True
            )

            chart = px.bar(
                comparison,
                x="Candidate",
                y="Final Score",
                title="Candidate Final Scores",
                template="plotly_dark"
            )

            chart.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )

            st.plotly_chart(
                chart,
                use_container_width=True
            )


# ============================================================
# RECRUITER — SHORTLIST
# ============================================================

elif workspace == "Recruiter" and page == "Shortlist":

    render_html(
        """
        <div class="section-title">
            ⭐ Shortlist Management
        </div>

        <div class="section-subtitle">
            Recruiter has the final control over candidate
            selection.
        </div>
        """
    )

    ranking = st.session_state.get(
        "ranked_df"
    )

    if ranking is None or ranking.empty:

        st.info(
            "Run candidate ranking first."
        )

    else:

        candidates = ranking[
            "Candidate"
        ].tolist()

        selected = st.multiselect(
            "Select final shortlist",
            candidates
        )

        if st.button(
            "⭐ Save Shortlist",
            use_container_width=True
        ):

            st.session_state.shortlisted = selected

            st.success(
                f"{len(selected)} candidates shortlisted."
            )

        if st.session_state.shortlisted:

            render_html(
                """
                <div class="section-title">
                    Final Shortlist
                </div>
                """
            )

            for name in st.session_state.shortlisted:

                render_html(
                    f"""
                    <div class="success-box">
                        ⭐ {html_lib.escape(name)}
                    </div>
                    """
                )


# ============================================================
# RECRUITER — PIPELINE
# ============================================================

elif workspace == "Recruiter" and page == "Recruitment Pipeline":

    render_html(
        """
        <div class="section-title">
            📊 Recruitment Pipeline
        </div>

        <div class="section-subtitle">
            Move candidates through the hiring lifecycle.
        </div>
        """
    )

    shortlisted = st.session_state.shortlisted

    if not shortlisted:

        st.info(
            "Your shortlist is empty."
        )

    else:

        for name in shortlisted:

            status = st.selectbox(
                name,
                [
                    "Shortlisted",
                    "HR Screening",
                    "Technical Interview",
                    "Final Interview",
                    "Offer",
                    "Rejected"
                ],
                key=f"pipeline_{name}"
            )

            st.caption(
                f"Current stage: {status}"
            )


# ============================================================
# RECRUITER — ANALYTICS
# ============================================================

elif workspace == "Recruiter" and page == "Hiring Analytics":

    render_html(
        """
        <div class="section-title">
            📈 Hiring Analytics
        </div>

        <div class="section-subtitle">
            Understand the quality and distribution of your
            candidate pool.
        </div>
        """
    )

    ranking = st.session_state.get(
        "ranked_df"
    )

    if ranking is None or ranking.empty:

        st.info(
            "Run candidate ranking to generate analytics."
        )

    else:

        c1, c2, c3 = st.columns(3)

        with c1:
            render_html(
                metric_card(
                    "Candidates",
                    len(ranking),
                    "Ranked candidates"
                )
            )

        with c2:
            render_html(
                metric_card(
                    "Average Score",
                    f"{ranking['Final Score'].mean():.1f}",
                    "Average AI score"
                )
            )

        with c3:
            render_html(
                metric_card(
                    "Top Score",
                    f"{ranking['Final Score'].max():.1f}",
                    "Highest candidate"
                )
            )

        chart = px.histogram(
            ranking,
            x="Final Score",
            nbins=10,
            title="Candidate Score Distribution",
            template="plotly_dark"
        )

        chart.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            chart,
            use_container_width=True
        )


# ============================================================
# RECRUITER — AI ASSISTANT
# ============================================================

elif workspace == "Recruiter" and page == "AI Recruiter Assistant":

    render_html(
        """
        <div class="section-title">
            🤖 AI Recruiter Assistant
        </div>

        <div class="section-subtitle">
            Ask questions about your candidate pool.
        </div>
        """
    )

    question = st.chat_input(
        "Example: Who are my strongest candidates?"
    )

    if question:

        ranking = st.session_state.get(
            "ranked_df"
        )

        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):

            if ranking is None or ranking.empty:

                st.write(
                    "Run candidate ranking first so I can "
                    "analyze the candidate pool."
                )

            else:

                lower = question.lower()

                if (
                    "top"
                    in lower
                    or "strongest"
                    in lower
                    or "best"
                    in lower
                ):

                    top = ranking.head(5)

                    response = []

                    for _, row in top.iterrows():

                        response.append(
                            f"**{row['Candidate']}** — "
                            f"{row['Final Score']}/100"
                        )

                    st.markdown(
                        "\n\n".join(
                            response
                        )
                    )

                elif "python" in lower:

                    matches = ranking[
                        ranking["Skills"]
                        .str.contains(
                            "Python",
                            case=False,
                            na=False
                        )
                    ]

                    if matches.empty:

                        st.write(
                            "No Python candidates were detected."
                        )

                    else:

                        st.write(
                            "Candidates with Python detected:"
                        )

                        st.dataframe(
                            matches[
                                [
                                    "Candidate",
                                    "Final Score",
                                    "Experience"
                                ]
                            ],
                            hide_index=True,
                            use_container_width=True
                        )

                else:

                    st.write(
                        "I can summarize top candidates, inspect "
                        "skills, compare scores and help review "
                        "the ranked candidate pool."
                    )


# ============================================================
# FOOTER
# ============================================================

render_html(
    """
    <div class="footer">

        🎯 <b>CareerLens AI</b>
        <br>
        AI-Powered Career Intelligence & Recruitment Platform
        <br>
        Final Year Project · AI · ML · NLP

    </div>
    """
)
