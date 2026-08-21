
import io
import re
from typing import Dict, List

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
# Standalone Streamlit app
# IMPORTANT: This file contains Python only.
# Do not add ```python or ``` around this code in app.py.
# ============================================================

st.set_page_config(
    page_title="CareerLens AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Professional UI
# -----------------------------

st.markdown(
    """
<style>
:root{
    --bg:#07111f;
    --panel:#0d1a2b;
    --panel2:#101f33;
    --border:#213754;
    --text:#f4f7fb;
    --muted:#8fa2ba;
    --purple:#8b7cff;
    --cyan:#38bdf8;
    --green:#4ade80;
    --yellow:#fbbf24;
    --red:#fb7185;
}
.stApp{
    background:
        radial-gradient(circle at 15% 0%,rgba(139,124,255,.14),transparent 28%),
        radial-gradient(circle at 90% 5%,rgba(56,189,248,.10),transparent 25%),
        var(--bg);
}
.block-container{
    max-width:1450px;
    padding:28px 34px 60px;
}
[data-testid="stSidebar"]{
    background:#081526;
    border-right:1px solid #1b304b;
}
h1,h2,h3,h4{
    color:var(--text)!important;
}
p,label,.stMarkdown{
    color:#b8c6d8;
}
.brand{
    font-size:29px;
    font-weight:850;
    color:white;
    letter-spacing:-.7px;
}
.brand span{
    background:linear-gradient(90deg,var(--purple),var(--cyan));
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}
.brand-sub{
    font-size:10px;
    letter-spacing:2px;
    color:#70849e;
    margin-top:3px;
}
.status{
    display:inline-block;
    background:#0b2b20;
    color:var(--green);
    border:1px solid #1e6548;
    border-radius:999px;
    padding:7px 12px;
    font-size:11px;
    font-weight:800;
    letter-spacing:1px;
}
.hero{
    background:
        linear-gradient(135deg,rgba(139,124,255,.12),rgba(56,189,248,.04)),
        linear-gradient(135deg,#0d1d34,#0b1728);
    border:1px solid #28425f;
    border-radius:24px;
    padding:42px;
    margin-bottom:28px;
    box-shadow:0 24px 70px rgba(0,0,0,.20);
}
.kicker{
    color:var(--cyan);
    font-size:12px;
    font-weight:800;
    letter-spacing:2.4px;
}
.hero h1{
    font-size:clamp(38px,5vw,62px);
    line-height:1.05;
    letter-spacing:-2.4px;
    margin:12px 0;
}
.hero h1 span{
    background:linear-gradient(90deg,var(--purple),var(--cyan));
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}
.hero p{
    max-width:820px;
    font-size:16px;
    line-height:1.75;
    color:#a8b9cd;
}
.card{
    background:rgba(13,26,43,.88);
    border:1px solid var(--border);
    border-radius:18px;
    padding:22px;
    min-height:150px;
}
.card-icon{
    font-size:28px;
}
.card-title{
    color:white;
    font-weight:800;
    font-size:17px;
    margin-top:9px;
}
.card-text{
    color:#8fa2ba;
    font-size:13px;
    line-height:1.6;
    margin-top:7px;
}
.panel{
    background:rgba(13,26,43,.82);
    border:1px solid var(--border);
    border-radius:18px;
    padding:22px;
    margin:12px 0;
}
.skill{
    display:inline-block;
    background:rgba(139,124,255,.10);
    color:#d9d4ff;
    border:1px solid rgba(139,124,255,.25);
    border-radius:999px;
    padding:6px 11px;
    margin:3px;
    font-size:12px;
}
.small-label{
    color:#7186a1;
    font-size:11px;
    font-weight:800;
    letter-spacing:1.2px;
    text-transform:uppercase;
}
.footer{
    text-align:center;
    color:#7186a1;
    font-size:12px;
    padding:35px 0 5px;
}
div.stButton > button{
    border-radius:11px;
    font-weight:700;
}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# AI / NLP ENGINE
# ============================================================

SKILLS = {
    "Python":["python"],
    "Java":["java"],
    "JavaScript":["javascript","js"],
    "TypeScript":["typescript","ts"],
    "C++":["c++","cpp"],
    "C#":["c#","c sharp"],
    "SQL":["sql"],
    "HTML":["html"],
    "CSS":["css"],
    "React":["react","reactjs"],
    "Angular":["angular"],
    "Vue":["vue","vuejs"],
    "Node.js":["node.js","nodejs"],
    "Django":["django"],
    "Flask":["flask"],
    "FastAPI":["fastapi"],
    "Spring Boot":["spring boot"],
    "Flutter":["flutter"],
    "Dart":["dart"],
    "Android":["android"],
    "iOS":["ios"],
    "Machine Learning":["machine learning"],
    "Deep Learning":["deep learning"],
    "Artificial Intelligence":["artificial intelligence"],
    "NLP":["nlp","natural language processing"],
    "Computer Vision":["computer vision"],
    "TensorFlow":["tensorflow"],
    "PyTorch":["pytorch"],
    "Scikit-learn":["scikit-learn","sklearn"],
    "Pandas":["pandas"],
    "NumPy":["numpy"],
    "Data Analysis":["data analysis","data analytics"],
    "Data Science":["data science"],
    "Statistics":["statistics"],
    "Power BI":["power bi"],
    "Tableau":["tableau"],
    "AWS":["aws","amazon web services"],
    "Azure":["azure"],
    "Google Cloud":["google cloud","gcp"],
    "Docker":["docker"],
    "Kubernetes":["kubernetes","k8s"],
    "Git":["git"],
    "GitHub":["github"],
    "Linux":["linux"],
    "MongoDB":["mongodb","mongo db"],
    "PostgreSQL":["postgresql","postgres"],
    "MySQL":["mysql"],
    "Firebase":["firebase"],
    "REST API":["rest api","restful api"],
    "GraphQL":["graphql"],
    "Microservices":["microservices"],
    "System Design":["system design"],
    "Cybersecurity":["cybersecurity","cyber security"],
    "Networking":["networking","computer networks"],
    "Agile":["agile"],
    "Scrum":["scrum"],
    "Leadership":["leadership"],
    "Communication":["communication skills"],
    "Problem Solving":["problem solving","problem-solving"],
}

FRAUD_RULES = {
    "Financial request":[
        "pay a fee","registration fee","processing fee","send money",
        "wire transfer","credit card","payment required","deposit"
    ],
    "Urgency":[
        "act now","urgent","immediately","limited time","today only"
    ],
    "Sensitive information":[
        "bank details","account number","password","otp",
        "social security","identity document"
    ],
    "Suspicious communication":[
        "telegram","whatsapp only","crypto","gift card",
        "bitcoin","personal gmail"
    ],
}


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def extract_skills(text: str) -> List[str]:
    lower = normalize(text).lower()
    found = []

    for skill, patterns in SKILLS.items():
        if any(pattern in lower for pattern in patterns):
            found.append(skill)

    return sorted(set(found))


def extract_email(text: str) -> str:
    match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text or "",
    )
    return match.group(0) if match else "Not detected"


def extract_phone(text: str) -> str:
    match = re.search(r"(?:\+?\d[\d\s().-]{7,}\d)", text or "")
    return match.group(0).strip() if match else "Not detected"


def extract_name(text: str) -> str:
    lines = [x.strip() for x in (text or "").splitlines() if x.strip()]

    for line in lines[:12]:
        if "@" in line:
            continue

        cleaned = re.sub(r"[^A-Za-z .'-]", "", line).strip()
        words = cleaned.split()

        if 2 <= len(words) <= 5:
            if not any(
                x in cleaned.lower()
                for x in ["resume", "curriculum", "profile", "objective"]
            ):
                return cleaned

    return "Candidate"


def resume_score(text: str) -> int:
    text = normalize(text)

    if not text:
        return 0

    lower = text.lower()
    score = 0

    score += min(len(extract_skills(text)) * 4, 36)

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
        "skills",
    ]

    score += sum(4 for section in sections if section in lower)

    words = len(text.split())

    if words >= 250:
        score += 8
    if words >= 500:
        score += 5

    return min(score, 100)


def analyze_resume(text: str) -> Dict:
    skills = extract_skills(text)
    score = resume_score(text)

    readiness = min(
        100,
        round(score * 0.70 + min(len(skills) * 3, 30)),
    )

    experience = bool(
        re.search(
            r"\b(experience|internship|worked|developer|engineer|manager)\b",
            text.lower(),
        )
    )

    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "experience": "Detected" if experience else "Not clearly detected",
        "skills": skills,
        "resume_score": score,
        "readiness": readiness,
    }


def extract_text(uploaded_file) -> str:
    name = uploaded_file.name.lower()
    data = uploaded_file.getvalue()

    if name.endswith(".txt"):
        return data.decode("utf-8", errors="ignore")

    if name.endswith(".pdf"):
        if PdfReader is None:
            raise RuntimeError("PyPDF2 is not installed.")
        reader = PdfReader(io.BytesIO(data))
        return "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

    if name.endswith(".docx"):
        if Document is None:
            raise RuntimeError("python-docx is not installed.")
        doc = Document(io.BytesIO(data))
        return "\n".join(p.text for p in doc.paragraphs)

    raise RuntimeError("Unsupported file format.")


def match_profile_to_job(profile: str, job: str) -> Dict:
    profile = normalize(profile)
    job = normalize(job)

    if not profile or not job:
        return {
            "overall": 0,
            "semantic": 0,
            "skill_match": 0,
            "missing": [],
            "matched": [],
        }

    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=6000,
        )

        matrix = vectorizer.fit_transform([profile, job])

        semantic = round(
            float(cosine_similarity(
                matrix[0:1],
                matrix[1:2],
            )[0][0]) * 100
        )
    except Exception:
        semantic = 0

    profile_skills = set(extract_skills(profile))
    required_skills = set(extract_skills(job))

    matched = sorted(profile_skills & required_skills)
    missing = sorted(required_skills - profile_skills)

    if required_skills:
        skill_match = round(
            len(matched) / len(required_skills) * 100
        )
    else:
        skill_match = semantic

    overall = round(
        semantic * 0.55 +
        skill_match * 0.45
    )

    return {
        "overall": min(overall, 100),
        "semantic": min(semantic, 100),
        "skill_match": min(skill_match, 100),
        "missing": missing,
        "matched": matched,
    }


def analyze_job_risk(job: str) -> Dict:
    lower = normalize(job).lower()
    details = {}

    for category, patterns in FRAUD_RULES.items():
        hits = [p for p in patterns if p in lower]
        if hits:
            details[category] = hits

    score = min(
        100,
        sum(len(hits) * 12 for hits in details.values())
    )

    if score >= 50:
        level = "HIGH RISK"
    elif score >= 20:
        level = "MEDIUM RISK"
    else:
        level = "LOW RISK"

    signals = sum(len(x) for x in details.values())

    return {
        "score": score,
        "level": level,
        "signals": signals,
        "details": details,
    }


def skill_gap(profile: str, target: str) -> Dict:
    current = set(extract_skills(profile))
    required = set(extract_skills(target))

    return {
        "current": sorted(current),
        "required": sorted(required),
        "matched": sorted(current & required),
        "missing": sorted(required - current),
    }


def rank_candidates(candidates: List[Dict], job: str) -> pd.DataFrame:
    rows = []

    for candidate in candidates:
        analysis = analyze_resume(candidate["text"])
        match = match_profile_to_job(candidate["text"], job)

        rows.append({
            "Candidate": analysis["name"],
            "Email": analysis["email"],
            "Overall Match": match["overall"],
            "Skill Match": match["skill_match"],
            "Resume Score": analysis["resume_score"],
            "Missing Skills": ", ".join(match["missing"]),
            "File": candidate["filename"],
        })

    df = pd.DataFrame(rows)

    if not df.empty:
        df = df.sort_values(
            ["Overall Match", "Skill Match", "Resume Score"],
            ascending=False,
        ).reset_index(drop=True)

    return df


# ============================================================
# Session state
# ============================================================

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "resume_analysis" not in st.session_state:
    st.session_state.resume_analysis = None

if "applications" not in st.session_state:
    st.session_state.applications = 0

if "recruiter_df" not in st.session_state:
    st.session_state.recruiter_df = None


# ============================================================
# Helper UI
# ============================================================

def metric_row(values):
    columns = st.columns(len(values))

    for column, item in zip(columns, values):
        label, value, help_text = item

        with column:
            st.metric(
                label,
                value,
                help=help_text,
            )


def show_skills(skills):
    if not skills:
        st.caption("No known skills detected.")
        return

    html = "".join(
        f'<span class="skill">{skill}</span>'
        for skill in skills
    )

    st.markdown(
        html,
        unsafe_allow_html=True,
    )


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:
    st.markdown(
        '<div class="brand">Career<span>Lens</span> AI</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="brand-sub">CAREER INTELLIGENCE PLATFORM</div>',
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
        '<span class="status">● AI ENGINE ONLINE</span>',
        unsafe_allow_html=True,
    )

    st.caption("NLP • ML • Recruitment Intelligence")

    st.divider()

    st.caption("CareerLens AI v2.0")
    st.caption("AI-assisted decisions. Human review recommended.")


# ============================================================
# JOB SEEKER
# ============================================================

if workspace == "👨‍💻 Job Seeker":

    st.markdown(
        """
        <section class="hero">
            <div class="kicker">AI CAREER INTELLIGENCE</div>
            <h1>
                Understand Your Career.<br>
                <span>Build Your Future.</span>
            </h1>
            <p>
                CareerLens AI combines resume intelligence,
                semantic job matching, skill-gap analysis,
                job-risk screening and career planning
                in one professional workspace.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    analysis = st.session_state.resume_analysis

    score = (
        f"{analysis['resume_score']}/100"
        if analysis else "—"
    )

    readiness = (
        f"{analysis['readiness']}%"
        if analysis else "—"
    )

    skills = (
        len(analysis["skills"])
        if analysis else 0
    )

    metric_row([
        (
            "Resume Score",
            score,
            "AI-assisted resume quality score",
        ),
        (
            "Career Readiness",
            readiness,
            "Profile readiness estimate",
        ),
        (
            "Skills Detected",
            skills,
            "Skills extracted from the resume",
        ),
        (
            "Applications",
            st.session_state.applications,
            "Tracked applications",
        ),
    ])

    st.divider()

    tabs = st.tabs([
        "📄 Resume Intelligence",
        "🎯 Job Match",
        "🛡️ Fraud Risk",
        "🧩 Skill Gap",
        "🗺️ Career Roadmap",
    ])

    # --------------------------------------------------------
    # Resume
    # --------------------------------------------------------

    with tabs[0]:

        st.subheader("Resume Intelligence")

        st.write(
            "Upload a PDF, DOCX or TXT resume. "
            "CareerLens AI extracts profile information, "
            "skills and quality signals."
        )

        resume_file = st.file_uploader(
            "Resume",
            type=["pdf", "docx", "txt"],
            key="resume_upload",
        )

        if resume_file:

            if st.button(
                "Analyze Resume",
                type="primary",
                use_container_width=True,
            ):
                try:
                    text = extract_text(resume_file)

                    if not text.strip():
                        st.error(
                            "No readable text was found in this file."
                        )
                    else:
                        result = analyze_resume(text)

                        st.session_state.resume_text = text
                        st.session_state.resume_analysis = result

                        st.success(
                            "Resume analyzed successfully."
                        )

                except Exception as exc:
                    st.error(
                        f"Resume analysis failed: {exc}"
                    )

        analysis = st.session_state.resume_analysis

        if analysis:

            metric_row([
                (
                    "Resume Score",
                    f"{analysis['resume_score']}/100",
                    "Composite resume quality score",
                ),
                (
                    "Readiness",
                    f"{analysis['readiness']}%",
                    "Career readiness estimate",
                ),
                (
                    "Skills",
                    len(analysis["skills"]),
                    "Detected skills",
                ),
            ])

            st.subheader("Profile")

            c1, c2 = st.columns(2)

            with c1:
                st.write(
                    "**Name:**",
                    analysis["name"],
                )
                st.write(
                    "**Email:**",
                    analysis["email"],
                )

            with c2:
                st.write(
                    "**Phone:**",
                    analysis["phone"],
                )
                st.write(
                    "**Experience signals:**",
                    analysis["experience"],
                )

            st.subheader("Detected Skills")

            show_skills(analysis["skills"])

            with st.expander("View extracted resume text"):
                st.text_area(
                    "Extracted text",
                    st.session_state.resume_text,
                    height=300,
                    label_visibility="collapsed",
                )

    # --------------------------------------------------------
    # Job Match
    # --------------------------------------------------------

    with tabs[1]:

        st.subheader("Semantic Job Matching")

        job = st.text_area(
            "Paste job description",
            height=240,
            key="jobmatch",
        )

        if st.button(
            "Analyze Match",
            type="primary",
            use_container_width=True,
        ):

            if not st.session_state.resume_text:
                st.warning(
                    "Upload your resume first."
                )

            elif not job.strip():
                st.warning(
                    "Enter a job description."
                )

            else:

                result = match_profile_to_job(
                    st.session_state.resume_text,
                    job,
                )

                metric_row([
                    (
                        "Overall Match",
                        f"{result['overall']}%",
                        "Weighted semantic and skill match",
                    ),
                    (
                        "Semantic Similarity",
                        f"{result['semantic']}%",
                        "TF-IDF NLP similarity",
                    ),
                    (
                        "Skill Match",
                        f"{result['skill_match']}%",
                        "Required skills found in profile",
                    ),
                ])

                st.progress(
                    result["overall"] / 100
                )

                st.subheader("Matched Skills")
                show_skills(result["matched"])

                st.subheader("Missing Skills")
                show_skills(result["missing"])

                if result["missing"]:
                    st.warning(
                        "Skill gaps: " +
                        ", ".join(result["missing"])
                    )
                else:
                    st.success(
                        "No major known skill gaps detected."
                    )

    # --------------------------------------------------------
    # Fraud
    # --------------------------------------------------------

    with tabs[2]:

        st.subheader(
            "Job Fraud Risk Intelligence"
        )

        jobrisk = st.text_area(
            "Paste job advertisement",
            height=240,
            key="risk",
        )

        if st.button(
            "Run Risk Analysis",
            type="primary",
            use_container_width=True,
        ):

            if not jobrisk.strip():
                st.warning(
                    "Enter a job advertisement."
                )
            else:

                result = analyze_job_risk(
                    jobrisk
                )

                metric_row([
                    (
                        "Risk Score",
                        f"{result['score']}/100",
                        "Rule-based risk indicator",
                    ),
                    (
                        "Risk Level",
                        result["level"],
                        "Low/medium/high screening result",
                    ),
                    (
                        "Signals",
                        result["signals"],
                        "Suspicious patterns detected",
                    ),
                ])

                if result["level"] == "HIGH RISK":
                    st.error(
                        "High-risk signals detected. "
                        "Review this job carefully."
                    )

                elif result["level"] == "MEDIUM RISK":
                    st.warning(
                        "Moderate-risk signals detected."
                    )

                else:
                    st.success(
                        "No significant predefined "
                        "risk signals detected."
                    )

                for category, hits in result["details"].items():

                    st.write(
                        f"**{category}:** " +
                        ", ".join(hits)
                    )

                st.caption(
                    "Fraud screening is an assistive signal, "
                    "not proof of fraud."
                )

    # --------------------------------------------------------
    # Skill Gap
    # --------------------------------------------------------

    with tabs[3]:

        st.subheader("Skill Gap Analysis")

        target = st.text_area(
            "Target job description",
            height=220,
            key="gap",
        )

        if st.button(
            "Analyze Skill Gap",
            type="primary",
            use_container_width=True,
        ):

            if not st.session_state.resume_text:
                st.warning(
                    "Upload your resume first."
                )

            elif not target.strip():
                st.warning(
                    "Enter a target job description."
                )

            else:

                result = skill_gap(
                    st.session_state.resume_text,
                    target,
                )

                metric_row([
                    (
                        "Current Skills",
                        len(result["current"]),
                        "Detected profile skills",
                    ),
                    (
                        "Required Skills",
                        len(result["required"]),
                        "Detected target skills",
                    ),
                    (
                        "Missing Skills",
                        len(result["missing"]),
                        "Skills to prioritize",
                    ),
                ])

                st.subheader("Current / Matched Skills")
                show_skills(result["matched"])

                st.subheader("Priority Skill Gaps")
                show_skills(result["missing"])

                if result["missing"]:
                    st.warning(
                        "Prioritize: " +
                        ", ".join(result["missing"])
                    )
                else:
                    st.success(
                        "Your known skills cover "
                        "the detected requirements."
                    )

    # --------------------------------------------------------
    # Roadmap
    # --------------------------------------------------------

    with tabs[4]:

        st.subheader(
            "Personalized Career Roadmap"
        )

        role = st.text_input(
            "Target role",
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
                    "Strengthen the core skills required by your target role.",
                    "Build 2–3 portfolio projects demonstrating measurable outcomes.",
                    "Improve your resume using quantified achievements and relevant keywords.",
                    "Prepare technical, behavioral and project-based interview questions.",
                    "Apply selectively and track outcomes through the CareerLens workflow.",
                ]

                st.info(
                    f"Target role: {role}"
                )

                for index, step in enumerate(
                    steps,
                    start=1,
                ):

                    st.markdown(
                        f"""
                        <div class="panel">
                            <div class="small-label">
                                STEP {index:02d}
                            </div>
                            <div class="card-title">
                                {step}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

    st.divider()

    st.subheader("Career Intelligence")

    features = [
        (
            "📄",
            "Resume Intelligence",
            "Extract and score professional profile information.",
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
            "Compare current and target capabilities.",
        ),
        (
            "🔎",
            "Job Intelligence",
            "Parse requirements and important skills.",
        ),
        (
            "🗺️",
            "Career Roadmap",
            "Turn skill gaps into an actionable development plan.",
        ),
    ]

    columns = st.columns(3)

    for index, (icon, title, description) in enumerate(features):

        with columns[index % 3]:

            st.markdown(
                f"""
                <div class="card">
                    <div class="card-icon">{icon}</div>
                    <div class="card-title">{title}</div>
                    <div class="card-text">{description}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ============================================================
# RECRUITER
# ============================================================

else:

    st.markdown(
        """
        <section class="hero">
            <div class="kicker">
                RECRUITMENT INTELLIGENCE
            </div>
            <h1>
                Screen Smarter.<br>
                <span>Hire with Evidence.</span>
            </h1>
            <p>
                Upload candidate resumes, define the role,
                and let CareerLens AI rank candidates using
                semantic similarity, skill alignment and
                resume quality.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    job = st.text_area(
        "Job Description",
        height=220,
        key="recruiter_job",
    )

    files = st.file_uploader(
        "Candidate Resumes — bulk upload",
        type=["pdf", "docx", "txt"],
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
        "The recruiter controls the final Top-N shortlist."
    )

    if st.button(
        "🚀 Screen & Rank Candidates",
        type="primary",
        use_container_width=True,
    ):

        if not job.strip():
            st.warning(
                "Enter the job description."
            )

        elif not files:
            st.warning(
                "Upload candidate resumes."
            )

        else:

            candidates = []

            with st.spinner(
                "AI engine is analyzing candidates..."
            ):

                for file in files:

                    try:
                        text = extract_text(file)

                        if text.strip():
                            candidates.append({
                                "filename": file.name,
                                "text": text,
                            })

                    except Exception as exc:
                        st.warning(
                            f"{file.name}: {exc}"
                        )

            if candidates:

                dataframe = rank_candidates(
                    candidates,
                    job,
                )

                st.session_state.recruiter_df = dataframe

                st.success(
                    f"Analyzed {len(dataframe)} candidates."
                )

            else:
                st.error(
                    "No readable resumes were found."
                )

    dataframe = st.session_state.recruiter_df

    if dataframe is not None and not dataframe.empty:

        shortlist = dataframe.head(
            int(top_n)
        ).copy()

        best_match = int(
            dataframe.iloc[0]["Overall Match"]
        )

        metric_row([
            (
                "Resumes Screened",
                len(dataframe),
                "Candidates successfully analyzed",
            ),
            (
                "Shortlisted",
                len(shortlist),
                "Recruiter-selected Top-N",
            ),
            (
                "Best Match",
                f"{best_match}%",
                "Highest ranked candidate",
            ),
        ])

        st.subheader(
            f"🏆 Top {len(shortlist)} Candidates"
        )

        st.dataframe(
            shortlist,
            use_container_width=True,
            hide_index=True,
        )

        st.download_button(
            "⬇️ Download Shortlist CSV",
            shortlist.to_csv(
                index=False
            ).encode("utf-8"),
            file_name="careerLens_shortlist.csv",
            mime="text/csv",
            use_container_width=True,
        )

        if not shortlist.empty:

            selected = st.selectbox(
                "Candidate Intelligence",
                shortlist["Candidate"].tolist(),
            )

            row = shortlist[
                shortlist["Candidate"] == selected
            ].iloc[0]

            c1, c2 = st.columns(2)

            with c1:

                st.metric(
                    "Overall Match",
                    f"{int(row['Overall Match'])}%",
                )

                st.write(
                    "**Candidate:**",
                    row["Candidate"],
                )

                st.write(
                    "**Email:**",
                    row["Email"],
                )

            with c2:

                st.metric(
                    "Skill Match",
                    f"{int(row['Skill Match'])}%",
                )

                st.write(
                    "**Resume Score:**",
                    f"{int(row['Resume Score'])}/100",
                )

                st.write(
                    "**Missing Skills:**",
                    row["Missing Skills"]
                    or "None detected",
                )


# ============================================================
# Footer
# ============================================================

st.divider()

st.markdown(
    """
    <div class="footer">
        <b>🎯 CareerLens AI</b><br>
        AI-Powered Career Intelligence & Recruitment Platform<br>
        Final Year Project · AI · ML · NLP
    </div>
    """,
    unsafe_allow_html=True,
)
