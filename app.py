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
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CareerLens AI — Career Intelligence & Recruitment",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# MODERN SAAS UI STYLING
# ============================================================

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        * {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background-color: #070d18;
            color: #cbd5e1;
        }

        [data-testid="stSidebar"] {
            background-color: #0c1527;
            border-right: 1px solid #1e293b;
        }

        .block-container {
            max-width: 1350px;
            padding-top: 1.8rem;
            padding-bottom: 3rem;
        }

        /* Typography */
        h1, h2, h3, h4 {
            color: #f8fafc !important;
            font-weight: 700;
            letter-spacing: -0.02em;
        }

        p, label, span {
            color: #94a3b8;
        }

        /* Brand Elements */
        .brand-container {
            padding: 10px 0 20px 0;
        }
        .brand-name {
            font-size: 26px;
            font-weight: 800;
            color: #ffffff;
            letter-spacing: -0.5px;
        }
        .brand-accent {
            background: linear-gradient(135deg, #818cf8 0%, #c084fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .brand-badge {
            display: inline-block;
            font-size: 10px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            color: #a5b4fc;
            background: rgba(99, 102, 241, 0.15);
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 6px;
            padding: 2px 8px;
            margin-top: 6px;
        }

        /* Hero Banner */
        .hero-banner {
            background: linear-gradient(135deg, #0f172a 0%, #172554 50%, #1e1b4b 100%);
            border: 1px solid #312e81;
            border-radius: 20px;
            padding: 36px 40px;
            margin-bottom: 28px;
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        }
        .hero-tag {
            color: #a5b4fc;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 2px;
            text-transform: uppercase;
        }
        .hero-heading {
            color: #ffffff;
            font-size: 38px;
            font-weight: 800;
            line-height: 1.15;
            margin: 8px 0 14px 0;
        }
        .hero-heading span {
            background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .hero-sub {
            color: #94a3b8;
            font-size: 15px;
            line-height: 1.6;
            max-width: 800px;
            margin: 0;
        }

        /* Skill Chips */
        .chip {
            display: inline-block;
            background: #1e293b;
            color: #e2e8f0;
            border: 1px solid #334155;
            border-radius: 20px;
            padding: 4px 14px;
            font-size: 12px;
            font-weight: 500;
            margin: 3px 4px 3px 0;
        }
        .chip-gap {
            background: rgba(239, 68, 68, 0.12);
            color: #fca5a5;
            border: 1px solid rgba(239, 68, 68, 0.3);
        }
        .chip-match {
            background: rgba(34, 197, 94, 0.12);
            color: #86efac;
            border: 1px solid rgba(34, 197, 94, 0.3);
        }

        /* Stat & Info Cards */
        .stat-card {
            background-color: #0f172a;
            border: 1px solid #1e293b;
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 15px;
        }
        .feature-card {
            background-color: #0f172a;
            border: 1px solid #1e293b;
            border-radius: 16px;
            padding: 22px;
            min-height: 155px;
            transition: all 0.2s ease-in-out;
        }
        .feature-icon {
            font-size: 26px;
            margin-bottom: 10px;
        }
        .feature-title {
            color: #f1f5f9;
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 6px;
        }
        .feature-desc {
            color: #64748b;
            font-size: 13px;
            line-height: 1.5;
        }

        /* Risk Badges */
        .badge-low {
            background: rgba(34, 197, 94, 0.15);
            color: #4ade80;
            border: 1px solid rgba(34, 197, 94, 0.4);
            padding: 6px 14px;
            border-radius: 8px;
            font-weight: 700;
            display: inline-block;
        }
        .badge-medium {
            background: rgba(245, 158, 11, 0.15);
            color: #fbbf24;
            border: 1px solid rgba(245, 158, 11, 0.4);
            padding: 6px 14px;
            border-radius: 8px;
            font-weight: 700;
            display: inline-block;
        }
        .badge-high {
            background: rgba(239, 68, 68, 0.15);
            color: #f87171;
            border: 1px solid rgba(239, 68, 68, 0.4);
            padding: 6px 14px;
            border-radius: 8px;
            font-weight: 700;
            display: inline-block;
        }

        /* System Status Pill */
        .status-pill {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 12px;
            font-weight: 600;
            color: #4ade80;
            background: rgba(34, 197, 94, 0.08);
            border: 1px solid rgba(34, 197, 94, 0.2);
            padding: 6px 12px;
            border-radius: 8px;
            width: fit-content;
        }
        .status-dot {
            height: 8px;
            width: 8px;
            background-color: #22c55e;
            border-radius: 50%;
            display: inline-block;
        }

        /* Streamlit Native Widget Reskins */
        div[data-testid="stMetric"] {
            background-color: #0f172a;
            border: 1px solid #1e293b;
            border-radius: 12px;
            padding: 16px;
        }
        div[data-testid="stMetricValue"] {
            color: #f8fafc !important;
            font-weight: 700;
        }
        div[data-testid="stMetricLabel"] {
            color: #64748b !important;
            font-size: 13px;
            font-weight: 600;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SKILL TAXONOMY
# ============================================================

SKILL_ALIASES = {
    "Python": ["python", "py"],
    "Java": ["java", "jvm"],
    "JavaScript": ["javascript", "js"],
    "TypeScript": ["typescript", "ts"],
    "C++": ["c++", "cpp"],
    "C#": ["c#", "csharp", "c sharp"],
    ".NET": [".net", "dotnet", "asp.net"],
    "React": ["react", "react.js", "reactjs"],
    "Angular": ["angular", "angularjs"],
    "Vue.js": ["vue", "vue.js", "vuejs"],
    "Node.js": ["node.js", "nodejs", "node js"],
    "FastAPI": ["fastapi", "fast api"],
    "Flask": ["flask"],
    "Django": ["django"],
    "Spring Boot": ["spring boot", "springboot", "spring"],
    "HTML": ["html", "html5"],
    "CSS": ["css", "css3", "tailwind", "bootstrap"],
    "SQL": ["sql", "mysql", "postgresql", "postgres", "sqlite", "oracle"],
    "MongoDB": ["mongodb", "mongo db", "mongo"],
    "Redis": ["redis"],
    "Machine Learning": ["machine learning", "machine-learning", "ml"],
    "Deep Learning": ["deep learning", "deep-learning", "dl", "neural networks"],
    "NLP": ["nlp", "natural language processing", "text mining", "spacy", "nltk"],
    "Computer Vision": ["computer vision", "opencv", "yolo", "image processing"],
    "TensorFlow": ["tensorflow", "tf"],
    "PyTorch": ["pytorch", "torch"],
    "Scikit-learn": ["scikit-learn", "sklearn"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Data Analysis": ["data analysis", "data analytics", "eda"],
    "Data Science": ["data science"],
    "Power BI": ["power bi", "powerbi"],
    "Tableau": ["tableau"],
    "Excel": ["excel", "microsoft excel", "spreadsheets"],
    "AWS": ["aws", "amazon web services", "ec2", "s3", "lambda"],
    "Azure": ["azure", "microsoft azure"],
    "GCP": ["gcp", "google cloud", "google cloud platform"],
    "Docker": ["docker", "containerization"],
    "Kubernetes": ["kubernetes", "k8s"],
    "Git": ["git", "github", "gitlab", "version control"],
    "Linux": ["linux", "unix", "bash", "shell scripting"],
    "REST API": ["rest api", "restful api", "restful", "apis"],
    "GraphQL": ["graphql"],
    "CI/CD": ["ci/cd", "continuous integration", "github actions", "jenkins"],
    "Microservices": ["microservices", "distributed systems"],
    "Figma": ["figma"],
    "UI/UX": ["ui/ux", "ui ux", "user experience", "wireframing"],
    "Agile": ["agile", "scrum", "kanban", "sprint"],
    "Communication": ["communication", "presentation"],
    "Leadership": ["leadership", "mentoring", "team management"],
    "Problem Solving": ["problem solving", "problem-solving", "analytical skills"],
}


# ============================================================
# FRAUD DETECTION PATTERNS
# ============================================================

FRAUD_RULES = {
    "Financial & Payment Demands": [
        "pay a fee", "registration fee", "processing fee", "training fee",
        "security deposit", "send money", "payment required", "upfront payment",
        "pay to apply", "application fee", "wire transfer", "cashier check"
    ],
    "Sensitive Banking Requests": [
        "bank account", "bank details", "credit card", "debit card",
        "otp", "one time password", "crypto", "cryptocurrency", "wallet address",
        "social security number", "ssn", "netbanking"
    ],
    "Artificial Urgency": [
        "act now", "urgent hiring", "immediate joiner today", "within 24 hours",
        "limited slots left", "last chance", "today only", "instant offer"
    ],
    "Unofficial Communication Channels": [
        "whatsapp only", "telegram only", "contact on telegram", "contact on whatsapp",
        "personal gmail", "inbox me directly", "dm on telegram"
    ],
    "Unrealistic Guarantees": [
        "guaranteed job", "100% placement", "guaranteed placement", "no interview required",
        "no experience high salary", "earn $5000 weekly effortless", "guaranteed selection"
    ]
}


# ============================================================
# SESSION STATE INITIALIZATION
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
# TEXT EXTRACTION & NLP ENGINES
# ============================================================

def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", str(text).lower()).strip()


def extract_pdf(data: bytes) -> str:
    if PdfReader is None:
        return ""
    try:
        reader = PdfReader(io.BytesIO(data))
        return "\n".join([page.extract_text() or "" for page in reader.pages])
    except Exception:
        return ""


def extract_docx(data: bytes) -> str:
    if Document is None:
        return ""
    try:
        doc = Document(io.BytesIO(data))
        return "\n".join([p.text for p in doc.paragraphs])
    except Exception:
        return ""


def extract_file_text(uploaded_file) -> str:
    if uploaded_file is None:
        return ""
    try:
        data = uploaded_file.getvalue()
    except Exception:
        return ""

    ext = uploaded_file.name.lower().split(".")[-1]
    if ext == "txt":
        return data.decode("utf-8", errors="ignore")
    if ext == "pdf":
        return extract_pdf(data)
    if ext == "docx":
        return extract_docx(data)
    return ""


def detect_skills(text: str) -> List[str]:
    text_clean = normalize_text(text)
    detected = []
    for skill, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            pattern = r"(?<![a-z0-9])" + re.escape(alias.lower()) + r"(?![a-z0-9])"
            if re.search(pattern, text_clean):
                detected.append(skill)
                break
    return sorted(set(detected))


def extract_email(text: str) -> str:
    match = re.search(r"[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else "Not detected"


def extract_phone(text: str) -> str:
    matches = re.findall(r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text)
    return matches[0].strip() if matches else "Not detected"


def extract_name(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for line in lines[:10]:
        if (
            2 <= len(line.split()) <= 4
            and "@" not in line
            and not re.search(r"\d", line)
            and len(line) < 40
            and not any(keyword in line.lower() for keyword in ["resume", "curriculum", "cv", "profile"])
        ):
            return line.title()
    return "Candidate"


def calculate_resume_score(text: str, skills: List[str]) -> int:
    score = 0
    lower = normalize_text(text)

    # Content length & depth
    if len(text.strip()) >= 500:
        score += 15
    elif len(text.strip()) >= 250:
        score += 10

    # Contact indicators
    if extract_email(text) != "Not detected":
        score += 10
    if extract_phone(text) != "Not detected":
        score += 5

    # Skill footprint (up to 30 pts)
    score += min(len(skills) * 3, 30)

    # Core Structural Sections
    education_markers = ["b.tech", "btech", "bachelor", "master", "degree", "computer science", "engineering", "university", "gpa"]
    if any(m in lower for m in education_markers):
        score += 15

    if any(k in lower for k in ["experience", "employment", "work history", "internship"]):
        score += 10

    if any(k in lower for k in ["project", "portfolio", "capstone", "github.com"]):
        score += 10

    if any(k in lower for k in ["linkedin.com", "github.com", "leetcode", "certifi"]):
        score += 5

    return min(score, 100)


def calculate_readiness(resume_score: int, skills: List[str]) -> int:
    skill_factor = min(len(skills) * 3.5, 30)
    return min(100, round((resume_score * 0.7) + skill_factor))


def nlp_similarity(profile: str, job: str) -> float:
    if not profile.strip() or not job.strip():
        return 0.0
    try:
        vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        matrix = vectorizer.fit_transform([normalize_text(profile), normalize_text(job)])
        return float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])
    except Exception:
        return 0.0


def skill_similarity(profile_skills: List[str], job_skills: List[str]) -> float:
    if not job_skills:
        return 0.0
    return len(set(profile_skills) & set(job_skills)) / len(set(job_skills))


def calculate_match(profile: str, job: str) -> Tuple[int, int, int]:
    profile_skills = detect_skills(profile)
    job_skills = detect_skills(job)

    nlp_score = nlp_similarity(profile, job)
    skill_score = skill_similarity(profile_skills, job_skills)

    # Blended weighting: 50% NLP semantics + 50% explicit skill alignment
    overall = (nlp_score * 0.50) + (skill_score * 0.50)

    return (
        min(round(overall * 100), 100),
        min(round(nlp_score * 100), 100),
        min(round(skill_score * 100), 100),
    )


def detect_fraud(job_text: str) -> Dict:
    text = normalize_text(job_text)
    found = {}

    for category, phrases in FRAUD_RULES.items():
        hits = [phrase for phrase in phrases if phrase in text]
        if hits:
            found[category] = hits

    total_signals = sum(len(v) for v in found.values())
    risk_score = min(total_signals * 20, 100)

    if risk_score >= 50:
        level = "HIGH RISK"
    elif risk_score >= 20:
        level = "MEDIUM RISK"
    else:
        level = "LOW RISK"

    return {
        "level": level,
        "score": risk_score,
        "signals": found,
    }


def render_chips(skills: List[str], chip_class="chip") -> str:
    if not skills:
        return "<span style='color:#64748b; font-size:13px;'>None detected</span>"
    return "".join([f"<span class='{chip_class}'>{s}</span>" for s in skills])


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:
    st.markdown(
        """
        <div class="brand-container">
            <div class="brand-name">Career<span class="brand-accent">Lens</span> AI</div>
            <div class="brand-badge">Enterprise Edition</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    workspace = st.radio(
        "WORKSPACE VIEW",
        ["👨‍💻 Job Seeker Workspace", "🏢 Recruiter Intelligence"],
        index=0,
    )

    st.markdown("---")

    st.markdown(
        """
        <div class="status-pill">
            <span class="status-dot"></span>
            AI ENGINE ONLINE
        </div>
        <div style="font-size: 11px; color: #64748b; margin-top: 8px;">
            TF-IDF • Cosine Similarity • NLP Heuristics
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# WORKSPACE 1: JOB SEEKER
# ============================================================

if workspace == "👨‍💻 Job Seeker Workspace":

    st.markdown(
        """
        <div class="hero-banner">
            <div class="hero-tag">AI Career Intelligence</div>
            <div class="hero-heading">Understand Your Career. <span>Build Your Future.</span></div>
            <p class="hero-sub">
                CareerLens AI provides multidimensional resume scoring, semantic job description matching,
                instant skill-gap diagnosis, and automated job-posting fraud screening.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Top Overview Metrics
    analysis = st.session_state.resume_analysis
    resume_score = analysis["resume_score"] if analysis else None
    readiness = analysis["readiness"] if analysis else None
    skill_count = len(analysis["skills"]) if analysis else 0

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Resume Score", "—" if resume_score is None else f"{resume_score}/100")
    with m2:
        st.metric("Career Readiness", "—" if readiness is None else f"{readiness}%")
    with m3:
        st.metric("Skills Extracted", skill_count)
    with m4:
        st.metric("Target Applications", st.session_state.applications)

    st.markdown("<br>", unsafe_allow_html=True)

    # Modular Tabs for Clean UX
    tab_resume, tab_match, tab_fraud, tab_roadmap = st.tabs([
        "📄 Resume Intelligence",
        "🎯 Semantic Job Match",
        "🛡️ Fraud Risk Screening",
        "🗺️ Skill Gap & Roadmap"
    ])

    # --- TAB 1: RESUME INTELLIGENCE ---
    with tab_resume:
        st.subheader("Upload & Parse Resume")
        st.caption("Supports PDF, DOCX, and TXT files. Evaluated against industry structural benchmarks.")

        resume_file = st.file_uploader(
            "Upload Resume",
            type=["pdf", "docx", "txt"],
            key="js_resume_file",
            label_visibility="collapsed"
        )

        if resume_file:
            text = extract_file_text(resume_file)
            if not text.strip():
                st.error("⚠️ Unable to extract text. Please ensure the document contains selectable text.")
            else:
                detected = detect_skills(text)
                r_score = calculate_resume_score(text, detected)
                readiness_score = calculate_readiness(r_score, detected)

                st.session_state.resume_text = text
                st.session_state.resume_name = resume_file.name
                st.session_state.resume_analysis = {
                    "name": extract_name(text),
                    "email": extract_email(text),
                    "phone": extract_phone(text),
                    "skills": detected,
                    "resume_score": r_score,
                    "readiness": readiness_score,
                }

                st.success("✅ Resume analyzed and indexed successfully!")

                p_col1, p_col2 = st.columns(2)
                with p_col1:
                    st.markdown(
                        f"""
                        <div class="stat-card">
                            <h4 style="margin:0 0 10px 0;">Candidate Identification</h4>
                            <p><b>Name:</b> {st.session_state.resume_analysis['name']}</p>
                            <p><b>Email:</b> {st.session_state.resume_analysis['email']}</p>
                            <p><b>Phone:</b> {st.session_state.resume_analysis['phone']}</p>
                            <p><b>Source File:</b> {resume_file.name}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with p_col2:
                    st.markdown(
                        f"""
                        <div class="stat-card">
                            <h4 style="margin:0 0 10px 0;">Identified Competencies ({len(detected)})</h4>
                            <div>{render_chips(detected)}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

    # --- TAB 2: SEMANTIC JOB MATCH ---
    with tab_match:
        st.subheader("Job Compatibility Engine")
        st.caption("Calculates TF-IDF n-gram cosine similarity paired with explicit skill taxonomy overlap.")

        job_input = st.text_area(
            "Paste Target Job Description",
            height=200,
            placeholder="Paste target job responsibilities, requirements, and qualifications...",
            key="match_jd_input"
        )

        if st.button("Run Compatibility Match", type="primary", use_container_width=True):
            if not st.session_state.resume_text:
                st.warning("⚠️ Please upload your resume in the Resume Intelligence tab first.")
            elif not job_input.strip():
                st.warning("⚠️ Please provide a job description to compare against.")
            else:
                overall, nlp_sim, skill_sim = calculate_match(st.session_state.resume_text, job_input)
                cand_skills = detect_skills(st.session_state.resume_text)
                req_skills = detect_skills(job_input)
                missing = sorted(set(req_skills) - set(cand_skills))
                matched = sorted(set(req_skills) & set(cand_skills))

                st.session_state.applications += 1

                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("Overall Match Index", f"{overall}%")
                with c2:
                    st.metric("Semantic Context Similarity", f"{nlp_sim}%")
                with c3:
                    st.metric("Skill Overlap Ratio", f"{skill_sim}%")

                st.markdown("<br>", unsafe_allow_html=True)
                sc1, sc2 = st.columns(2)
                with sc1:
                    st.markdown(
                        f"""
                        <div class="stat-card">
                            <h4 style="color:#4ade80 !important; margin:0 0 10px 0;">✓ Matched Job Skills ({len(matched)})</h4>
                            <div>{render_chips(matched, 'chip chip-match')}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with sc2:
                    st.markdown(
                        f"""
                        <div class="stat-card">
                            <h4 style="color:#f87171 !important; margin:0 0 10px 0;">⚠ Missing Target Skills ({len(missing)})</h4>
                            <div>{render_chips(missing, 'chip chip-gap')}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

    # --- TAB 3: FRAUD SCREENING ---
    with tab_fraud:
        st.subheader("Job Posting Risk & Fraud Shield")
        st.caption("Evaluates text patterns for payment demands, unofficial communications, and unrealistic guarantees.")

        posting_input = st.text_area(
            "Paste Job Posting or Email Offer",
            height=180,
            placeholder="Paste suspicious job advertisement, recruitment email, or offer letter...",
            key="fraud_input"
        )

        if st.button("Inspect Risk Signals", use_container_width=True):
            if not posting_input.strip():
                st.warning("⚠️ Please provide job advertisement text to screen.")
            else:
                fraud_res = detect_fraud(posting_input)
                lvl = fraud_res["level"]
                scr = fraud_res["score"]

                badge_class = "badge-low" if lvl == "LOW RISK" else ("badge-medium" if lvl == "MEDIUM RISK" else "badge-high")

                st.markdown(
                    f"""
                    <div style="margin: 15px 0;">
                        <span class="{badge_class}">{lvl} — RISK INDEX: {scr}/100</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if fraud_res["signals"]:
                    st.markdown("<div class='stat-card'>", unsafe_allow_html=True)
                    st.markdown("#### Detected Risk Indicators")
                    for cat, hits in fraud_res["signals"].items():
                        st.markdown(f"**{cat}:** `{', '.join(hits)}`")
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.success("✓ No common recruitment risk patterns or red-flag phrases detected.")

                st.caption("Disclaimer: AI screening identifies statistical risk markers and is not absolute legal proof of legitimacy or fraud.")

    # --- TAB 4: SKILL GAP & ROADMAP ---
    with tab_roadmap:
        st.subheader("Career Progression Roadmap")
        st.caption("Transform skill deficits into an actionable step-by-step career development path.")

        r_role = st.text_input("Target Career Role", placeholder="e.g., Senior Machine Learning Engineer, Full Stack Developer")
        r_jd = st.text_area("Target Job Context", height=150, placeholder="Paste target requirements to diagnose specific gaps...")

        if st.button("Generate Development Plan", use_container_width=True):
            if not st.session_state.resume_text:
                st.warning("⚠️ Please upload your resume in the Resume Intelligence tab first.")
            elif not r_jd.strip():
                st.warning("⚠️ Please provide the target job context.")
            else:
                c_skills = detect_skills(st.session_state.resume_text)
                t_skills = detect_skills(r_jd)
                gaps = sorted(set(t_skills) - set(c_skills))

                st.markdown("#### Skill Gap Analysis")
                st.markdown(f"**Target Role:** `{r_role or 'Specified Target Role'}`")
                st.markdown(f"**Identified Gaps:** {render_chips(gaps, 'chip chip-gap')}", unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("#### Personalized Action Plan")

                steps = [
                    f"**Phase 1: Foundation Alignment** — Master missing core competencies: *{', '.join(gaps[:3]) if gaps else 'Advanced Role Architectures'}*.",
                    f"**Phase 2: Project Demonstration** — Build 2 end-to-end production-grade portfolio projects showcasing {', '.join(gaps[3:6]) if len(gaps) > 3 else 'system design & deployment'}.",
                    "**Phase 3: Resume Keyword Calibration** — Quantify impact metrics (latency reduction, revenue impact, accuracy improvement) matching role requirements.",
                    "**Phase 4: Interview Simulation** — Practice technical system architecture rounds and behavioral scenarios.",
                    "**Phase 5: Targeted Pipeline** — Apply to relevant positions and iterate based on screening feedback."
                ]

                for s in steps:
                    st.markdown(f"- {s}")


# ============================================================
# WORKSPACE 2: RECRUITER INTELLIGENCE
# ============================================================

else:
    st.markdown(
        """
        <div class="hero-banner">
            <div class="hero-tag">Enterprise Screening</div>
            <div class="hero-heading">High-Throughput <span>Candidate Intelligence.</span></div>
            <p class="hero-sub">
                Batch screen hundreds of applicants simultaneously. Rank candidates with blended NLP similarity
                and skill extraction metrics, then export recruiter-controlled shortlists in seconds.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    rec_col1, rec_col2 = st.columns([1.2, 0.8])

    with rec_col1:
        st.subheader("1. Job Description & Benchmarks")
        recruiter_job_text = st.text_area(
            "Benchmark Job Description",
            height=230,
            placeholder="Paste role requirements, mandatory tech stack, and responsibilities...",
            key="rec_jd_box"
        )

    with rec_col2:
        st.subheader("2. Target Configuration")
        top_n_val = st.number_input(
            "Shortlist Limit (Top-N)",
            min_value=1,
            max_value=500,
            value=10,
            step=1,
            help="Select the exact number of top candidates you want in the final ranked cohort."
        )
        st.caption("Recruiter-controlled: Select Top 5, 10, 20, 50, or custom bounds.")

        candidate_batch = st.file_uploader(
            "Upload Batch Resumes (PDF, DOCX, TXT)",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=True,
            key="rec_batch_uploader"
        )

    if st.button("🚀 Execute Batch AI Screening", type="primary", use_container_width=True):
        if not recruiter_job_text.strip():
            st.warning("⚠️ Please provide a job description benchmark first.")
        elif not candidate_batch:
            st.warning("⚠️ Please upload at least one candidate resume.")
        else:
            records = []
            bar = st.progress(0)
            status_text = st.empty()
            total_docs = len(candidate_batch)

            target_skills = detect_skills(recruiter_job_text)

            for i, doc_file in enumerate(candidate_batch):
                status_text.text(f"Processing ({i+1}/{total_docs}): {doc_file.name}")
                raw_text = extract_file_text(doc_file)

                if not raw_text.strip():
                    records.append({
                        "Candidate": doc_file.name,
                        "Email": "Unreadable",
                        "Resume Score": 0,
                        "NLP Match": 0,
                        "Skill Match": 0,
                        "Overall Match": 0,
                        "Skills": "",
                        "Missing Skills": "",
                        "Status": "Failed / Unreadable"
                    })
                else:
                    c_skills = detect_skills(raw_text)
                    overall_s, nlp_s, skill_s = calculate_match(raw_text, recruiter_job_text)
                    r_score = calculate_resume_score(raw_text, c_skills)
                    gaps = sorted(set(target_skills) - set(c_skills))
                    c_name = extract_name(raw_text)
                    if c_name == "Candidate":
                        c_name = doc_file.name

                    records.append({
                        "Candidate": c_name,
                        "Email": extract_email(raw_text),
                        "Resume Score": r_score,
                        "NLP Match": nlp_s,
                        "Skill Match": skill_s,
                        "Overall Match": overall_s,
                        "Skills": ", ".join(c_skills),
                        "Missing Skills": ", ".join(gaps),
                        "Status": "Screened"
                    })

                bar.progress((i + 1) / total_docs)

            status_text.empty()
            bar.empty()

            df_results = pd.DataFrame(records)
            df_results = df_results.sort_values(
                by=["Overall Match", "Skill Match", "Resume Score"],
                ascending=False
            ).reset_index(drop=True)

            df_results.insert(0, "Rank", range(1, len(df_results) + 1))
            st.session_state.recruiter_results = df_results
            st.success(f"✓ Successfully screened and ranked {len(df_results)} candidate profiles!")

    # Display Recruiter Results
    if st.session_state.recruiter_results is not None:
        df_all = st.session_state.recruiter_results
        shortlist_size = min(int(top_n_val), len(df_all))
        df_top = df_all.head(shortlist_size)

        st.markdown("---")
        st.subheader("3. Candidate Ranking & Shortlist")

        k1, k2, k3 = st.columns(3)
        with k1:
            st.metric("Total Resumes Screened", len(df_all))
        with k2:
            st.metric("Shortlisted Cohort", len(df_top))
        with k3:
            best_score = df_all.iloc[0]["Overall Match"] if not df_all.empty else 0
            st.metric("Top Candidate Score", f"{best_score}%")

        display_cols = ["Rank", "Candidate", "Email", "Resume Score", "NLP Match", "Skill Match", "Overall Match", "Missing Skills", "Status"]
        st.dataframe(df_top[display_cols], use_container_width=True, hide_index=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("4. Candidate Intelligence Deep-Dive")

        candidate_list = df_top["Candidate"].tolist()
        if candidate_list:
            selected_person = st.selectbox("Select Candidate for Diagnostic Drill-Down", candidate_list)
            row = df_top[df_top["Candidate"] == selected_person].iloc[0]

            cd1, cd2 = st.columns(2)
            with cd1:
                st.markdown(
                    f"""
                    <div class="stat-card">
                        <h4 style="margin:0 0 10px 0;">Candidate: {row['Candidate']}</h4>
                        <p><b>Email:</b> {row['Email']}</p>
                        <p><b>Overall Match Index:</b> {row['Overall Match']}%</p>
                        <p><b>Resume Quality Score:</b> {row['Resume Score']}/100</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with cd2:
                st.markdown(
                    f"""
                    <div class="stat-card">
                        <h4 style="margin:0 0 10px 0;">Match Diagnostic</h4>
                        <p><b>Semantic NLP Match:</b> {row['NLP Match']}%</p>
                        <p><b>Explicit Skill Match:</b> {row['Skill Match']}%</p>
                        <p><b>Skill Gaps:</b> {row['Missing Skills'] or 'None'}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("---")
        st.subheader("5. Export Recruitment Intelligence")

        csv_buffer = df_top.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download Shortlist as CSV",
            data=csv_buffer,
            file_name="CareerLens_Shortlist.csv",
            mime="text/csv",
            type="primary",
            use_container_width=True,
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #475569; font-size: 12px; padding: 10px 0;">
        🎯 <b>CareerLens AI</b> — AI-Powered Career Intelligence & Recruitment Platform | Final Year Project
    </div>
    """,
    unsafe_allow_html=True,
)
