

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

============================================================
PAGE CONFIGURATION
============================================================

st.set_page_config(
page_title="CareerLens AI — Career Intelligence & Recruitment",
page_icon="⚡",
layout="wide",
initial_sidebar_state="expanded",
)

============================================================
ULTRA-PREMIUM SAAS DESIGN SYSTEM & CSS
============================================================

st.markdown(
"""<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

{
font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}

code, pre {
font-family: 'JetBrains Mono', monospace !important;
}

.stApp {
background: radial-gradient(circle at 10% 15%, rgba(99, 102, 241, 0.12) 0%, transparent 45%),
radial-gradient(circle at 90% 85%, rgba(168, 85, 247, 0.10) 0%, transparent 45%),
radial-gradient(circle at 50% 50%, rgba(14, 165, 233, 0.05) 0%, transparent 60%),
#050914;
color: #cbd5e1;
}

[data-testid="stSidebar"] {
background: rgba(8, 15, 28, 0.95);
border-right: 1px solid rgba(255, 255, 255, 0.08);
backdrop-filter: blur(20px);
}

.block-container {
max-width: 1420px;
padding-top: 1.5rem;
padding-bottom: 3.5rem;
}

h1, h2, h3, h4 {
color: #f8fafc !important;
font-weight: 700;
letter-spacing: -0.03em;
}

p, label, span {
color: #94a3b8;
}

.hero-container {
position: relative;
background: radial-gradient(circle at top right, rgba(99, 102, 241, 0.18) 0%, transparent 60%),
radial-gradient(circle at bottom left, rgba(168, 85, 247, 0.12) 0%, transparent 50%),
linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(13, 19, 38, 0.95) 100%);
border: 1px solid rgba(129, 140, 248, 0.3);
border-radius: 24px;
padding: 38px 42px;
margin-bottom: 28px;
backdrop-filter: blur(20px);
box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7), inset 0 1px 0 rgba(255, 255, 255, 0.12);
}

.hero-badge-row {
display: flex;
align-items: center;
gap: 10px;
margin-bottom: 14px;
}

.hero-pill {
display: inline-flex;
align-items: center;
gap: 6px;
color: #a5b4fc;
font-size: 11px;
font-weight: 700;
letter-spacing: 1.5px;
text-transform: uppercase;
background: rgba(99, 102, 241, 0.15);
border: 1px solid rgba(99, 102, 241, 0.35);
border-radius: 20px;
padding: 4px 14px;
}

.hero-title {
color: #ffffff;
font-size: 38px;
font-weight: 800;
line-height: 1.15;
margin: 0 0 14px 0;
letter-spacing: -0.03em;
}

.hero-gradient-text {
background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
}

.hero-description {
color: #94a3b8;
font-size: 15px;
line-height: 1.7;
max-width: 860px;
margin: 0 0 26px 0;
}

.hero-features-grid {
display: grid;
grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
gap: 12px;
margin-top: 10px;
}

.hero-mini-card {
background: rgba(255, 255, 255, 0.03);
border: 1px solid rgba(255, 255, 255, 0.08);
border-radius: 14px;
padding: 12px 16px;
display: flex;
align-items: center;
gap: 12px;
transition: all 0.2s ease;
}

.hero-mini-card {
background: rgba(99, 102, 241, 0.08);
border-color: rgba(99, 102, 241, 0.3);
transform: translateY(-2px);
}

.hero-icon-box {
width: 36px;
height: 36px;
border-radius: 10px;
display: flex;
align-items: center;
justify-content: center;
background: rgba(99, 102, 241, 0.15);
border: 1px solid rgba(99, 102, 241, 0.3);
flex-shrink: 0;
}

.hero-card-text h5 {
margin: 0;
color: #f1f5f9;
font-size: 13px;
font-weight: 700;
}

.hero-card-text p {
margin: 0;
color: #64748b;
font-size: 11px;
}

.glass-card {
background: rgba(11, 20, 38, 0.65);
border: 1px solid rgba(255, 255, 255, 0.08);
border-radius: 18px;
padding: 24px;
backdrop-filter: blur(16px);
margin-bottom: 18px;
box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.05);
transition: all 0.25s ease;
}

.glass-card {
border-color: rgba(99, 102, 241, 0.4);
transform: translateY(-2px);
}

.chip {
display: inline-block;
background: rgba(30, 41, 59, 0.85);
color: #e2e8f0;
border: 1px solid rgba(255, 255, 255, 0.12);
border-radius: 20px;
padding: 5px 14px;
font-size: 12px;
font-weight: 600;
margin: 4px 4px 4px 0;
letter-spacing: 0.2px;
box-shadow: 0 2px 6px rgba(0,0,0,0.2);
}

.chip-gap {
background: rgba(239, 68, 68, 0.18);
color: #fca5a5;
border: 1px solid rgba(239, 68, 68, 0.4);
}

.chip-match {
background: rgba(34, 197, 94, 0.18);
color: #86efac;
border: 1px solid rgba(34, 197, 94, 0.4);
}

.badge-low {
background: rgba(34, 197, 94, 0.15);
color: #4ade80;
border: 1px solid rgba(34, 197, 94, 0.4);
padding: 8px 18px;
border-radius: 10px;
font-weight: 800;
font-size: 14px;
display: inline-block;
box-shadow: 0 0 20px rgba(34, 197, 94, 0.2);
}

.badge-medium {
background: rgba(245, 158, 11, 0.15);
color: #fbbf24;
border: 1px solid rgba(245, 158, 11, 0.4);
padding: 8px 18px;
border-radius: 10px;
font-weight: 800;
font-size: 14px;
display: inline-block;
box-shadow: 0 0 20px rgba(245, 158, 11, 0.2);
}

.badge-high {
background: rgba(239, 68, 68, 0.15);
color: #f87171;
border: 1px solid rgba(239, 68, 68, 0.4);
padding: 8px 18px;
border-radius: 10px;
font-weight: 800;
font-size: 14px;
display: inline-block;
box-shadow: 0 0 20px rgba(239, 68, 68, 0.2);
}

.status-pill {
display: inline-flex;
align-items: center;
gap: 8px;
font-size: 11px;
font-weight: 700;
color: #4ade80;
background: rgba(34, 197, 94, 0.12);
border: 1px solid rgba(34, 197, 94, 0.3);
padding: 5px 12px;
border-radius: 20px;
}

.status-dot {
height: 7px;
width: 7px;
background-color: #22c55e;
border-radius: 50%;
box-shadow: 0 0 8px #22c55e;
}

div[data-testid="stMetric"] {
background: rgba(11, 20, 38, 0.7);
border: 1px solid rgba(255, 255, 255, 0.08);
border-radius: 16px;
padding: 18px 22px;
backdrop-filter: blur(12px);
box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

div[data-testid="stMetricValue"] {
color: #ffffff !important;
font-weight: 800;
font-size: 28px !important;
letter-spacing: -0.03em;
}

div[data-testid="stMetricLabel"] {
color: #64748b !important;
font-size: 12px;
font-weight: 700;
text-transform: uppercase;
letter-spacing: 0.6px;
}
</style>""",
unsafe_allow_html=True,
)

============================================================
SKILL TAXONOMY
============================================================

SKILL_ALIASES = {
"Python": ["python", "py"],
"Java": ["java", "jvm"],
"JavaScript": ["javascript", "js", "ecmascript"],
"TypeScript": ["typescript", "ts"],
"C++": ["c++", "cpp"],
"C#": ["c#", "csharp", "c sharp"],
".NET": [".net", "dotnet", "asp.net"],
"Go / Golang": ["golang", "go language"],
"Rust": ["rust", "cargo"],
"React": ["react", "react.js", "reactjs", "next.js", "nextjs"],
"Angular": ["angular", "angularjs"],
"Vue.js": ["vue", "vue.js", "vuejs", "nuxt"],
"Node.js": ["node.js", "nodejs", "node js", "express", "expressjs"],
"FastAPI": ["fastapi", "fast api"],
"Flask": ["flask"],
"Django": ["django"],
"Spring Boot": ["spring boot", "springboot", "spring framework"],
"HTML/CSS": ["html", "html5", "css", "css3", "tailwind", "bootstrap", "sass"],
"SQL": ["sql", "mysql", "postgresql", "postgres", "sqlite", "oracle", "mariadb"],
"MongoDB": ["mongodb", "mongo db", "mongo"],
"Redis": ["redis"],
"GraphQL": ["graphql"],
"REST API": ["rest api", "restful api", "restful", "apis", "api development"],
"Machine Learning": ["machine learning", "machine-learning", "ml", "supervised learning"],
"Deep Learning": ["deep learning", "deep-learning", "dl", "neural networks", "cnn", "rnn", "lstm"],
"NLP": ["nlp", "natural language processing", "text mining", "spacy", "nltk", "transformers", "llm", "genai", "rag"],
"Computer Vision": ["computer vision", "opencv", "yolo", "image processing"],
"TensorFlow": ["tensorflow", "tf"],
"PyTorch": ["pytorch", "torch"],
"Scikit-learn": ["scikit-learn", "sklearn"],
"Pandas": ["pandas"],
"NumPy": ["numpy"],
"Data Analysis": ["data analysis", "data analytics", "eda", "statistical analysis"],
"Data Science": ["data science", "predictive modeling"],
"Power BI": ["power bi", "powerbi"],
"Tableau": ["tableau"],
"Excel": ["excel", "microsoft excel", "spreadsheets", "vlookup"],
"AWS": ["aws", "amazon web services", "ec2", "s3", "lambda", "ecs", "cloudformation"],
"Azure": ["azure", "microsoft azure"],
"GCP": ["gcp", "google cloud", "google cloud platform"],
"Docker": ["docker", "containerization", "docker-compose"],
"Kubernetes": ["kubernetes", "k8s", "helm"],
"Git": ["git", "github", "gitlab", "version control"],
"Linux": ["linux", "unix", "bash", "shell scripting"],
"CI/CD": ["ci/cd", "continuous integration", "github actions", "jenkins"],
"Microservices": ["microservices", "distributed systems", "event-driven"],
"Figma / UI": ["figma", "ui/ux", "ui ux", "wireframing", "prototyping"],
"Agile": ["agile", "scrum", "kanban", "sprint planning"],
"Leadership": ["leadership", "mentoring", "team management", "stakeholder management"],
"Problem Solving": ["problem solving", "analytical thinking", "troubleshooting"],
}

============================================================
FRAUD DETECTION PATTERNS
============================================================

FRAUD_RULES = {
"Financial Demands & Upfront Fees": [
"pay a fee", "registration fee", "processing fee", "training fee",
"security deposit", "send money", "payment required", "upfront payment",
"pay to apply", "application fee", "wire transfer", "cashier check",
"purchase equipment first", "refundable deposit"
],
"Sensitive Banking & ID Requests": [
"bank account", "bank details", "credit card", "debit card",
"otp", "one time password", "crypto", "cryptocurrency", "wallet address",
"social security number", "ssn", "netbanking password", "routing number"
],
"High-Pressure Urgency": [
"act now", "urgent hiring", "immediate joiner today", "within 24 hours",
"limited slots left", "last chance", "today only", "instant offer letter",
"no delay join now"
],
"Unofficial Recruitment Channels": [
"whatsapp only", "telegram only", "contact on telegram", "contact on whatsapp",
"personal gmail", "inbox me directly", "dm on telegram", "no official email"
],
"Unrealistic Employment Guarantees": [
"guaranteed job", "100% placement", "guaranteed placement", "no interview required",
"no experience high salary", "earn $5000 weekly effortless", "guaranteed selection",
"direct hiring without technical round"
]
}

============================================================
SESSION STATE INITIALIZATION
============================================================

defaults = {
"workspace_mode": "Job Seeker",
"active_nav": "Resume Intelligence",
"resume_text": "",
"resume_name": "",
"resume_analysis": None,
"applications": 0,
"recruiter_results": None,
"chat_history": [
{
"role": "assistant",
"content": "👋 Hello! I am your CareerLens Universal AI Advisor.\n\nI can analyze resumes, diagnose skill gaps, formulate career strategies, draft cover letters, simulate technical and behavioral interviews, or clarify any aspect of recruitment and hiring.\n\nWhat would you like assistance with today?"
}
],
}

for key, value in defaults.items():
if key not in st.session_state:
st.session_state[key] = value

============================================================
TEXT EXTRACTION & NLP ENGINES
============================================================

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
match = re.search(r"[\w.+-]+@[\w-]+.[a-zA-Z]{2,}", text)
return match.group(0) if match else "Not detected"

def extract_phone(text: str) -> str:
matches = re.findall(r"(?:+?\d{1,3}[-.\s]?)?(?\d{3})?[-.\s]?\d{3}[-.\s]?\d{4}", text)
return matches[0].strip() if matches else "Not detected"

def extract_name(text: str) -> str:
lines = [line.strip() for line in text.splitlines() if line.strip()]
for line in lines[:10]:
if (
2 <= len(line.split()) <= 4
and "@" not in line
and not re.search(r"\d", line)
and len(line) < 40
and not any(keyword in line.lower() for keyword in ["resume", "curriculum", "cv", "profile", "contact", "email", "phone"])
):
return line.title()
return "Candidate"

def calculate_resume_score(text: str, skills: List[str]) -> int:
score = 0
lower = normalize_text(text)

if len(text.strip()) >= 500:
    score += 15
elif len(text.strip()) >= 250:
    score += 10

if extract_email(text) != "Not detected":
    score += 10
if extract_phone(text) != "Not detected":
    score += 5

score += min(len(skills) * 3, 30)

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

============================================================
COMPREHENSIVE RESPONSIVE AI CHATBOT ENGINE
============================================================

def generate_dynamic_bot_response(prompt: str) -> str:
p = prompt.strip().lower()
profile = st.session_state.resume_analysis
skills = profile["skills"] if profile else []
r_score = profile["resume_score"] if profile else None
name = profile["name"] if profile else "Candidate"

if any(k in p for k in ["hi", "hello", "hey", "who are you", "what can you do"]):
    return (
        f"Hello {name if name != 'Candidate' else 'there'}! I am **CareerLens AI**, your comprehensive career intelligence assistant.\n\n"
        "Here is what I can do for you right now:\n"
        "- **Resume Diagnosis**: Review quality scores, structural signals, and optimization strategies.\n"
        "- **Skill Strategy**: Identify missing technical stacks and design progressive learning roadmaps.\n"
        "- **Interview Prep**: Run mock technical & behavioral (STAR) interview simulations.\n"
        "- **Fraud Shield**: Advise on job offer legitimacy and recruitment red flags.\n"
        "- **Cover Letters & Pitches**: Generate tailored pitch templates and recruiter reach-outs."
    )

if any(k in p for k in ["my resume", "my score", "analyze my", "review my resume", "my profile"]):
    if profile:
        return (
            f"### 📄 Profile Assessment for **{name}**\n"
            f"- **Overall Quality Score**: `{r_score}/100`\n"
            f"- **Career Readiness Index**: `{profile['readiness']}%`\n"
            f"- **Indexed Skills ({len(skills)})**: {', '.join(skills[:8])}{'...' if len(skills) > 8 else ''}\n"
            f"- **Contact Info**: {profile['email']} | {profile['phone']}\n\n"
            "**Top 3 Immediate Recommendations:**\n"
            "1. **Impact Quantifiers**: Replace passive descriptions with data (e.g., *'Decreased query latency by 42% using Redis indexing'*).\n"
            "2. **Portfolio Links**: Ensure live GitHub and LinkedIn hyperlinks are positioned prominently at the top.\n"
            "3. **Skill Dispersion**: Ensure technical terms appear naturally inside work accomplishment bullets, not just in a skills list."
        )
    return (
        "You haven't uploaded a resume yet! Navigate to the **📄 Resume Intelligence** module in the navigation bar above, "
        "upload your PDF or DOCX file, and I will generate your personalized intelligence profile."
    )

if any(k in p for k in ["skill", "stack", "what should i learn", "gap", "technolog"]):
    if skills:
        return (
            f"### 🛠️ Competency Analysis for **{name}**\n"
            f"You currently possess strong signals in: **{', '.join(skills[:6])}**.\n\n"
            "**High-Yield Adjacent Technologies to Learn in 2026:**\n"
            "- **Cloud & Microservices**: Docker, Kubernetes, AWS (ECS/Lambda), CI/CD GitHub Actions.\n"
            "- **Modern Back-End**: FastAPI, Go/Rust microservices, Redis caching, gRPC.\n"
            "- **AI & Data Integration**: Vector databases (Milvus/Pinecone), LangChain/LlamaIndex, Retrieval-Augmented Generation (RAG).\n\n"
            "To see exact deficits against a specific opening, check out the **🗺️ Skill & Roadmap** module!"
        )
    return (
        "To give you custom skill suggestions, please upload your resume. In general, modern technical stacks "
        "demand **Python/TypeScript**, **Cloud Native (Docker/Kubernetes/AWS)**, **FastAPI/Next.js**, and **System Design fundamentals**."
    )

if any(k in p for k in ["interview", "mock", "question", "star method", "behavioral"]):
    role_match = "Software / AI Engineer"
    return (
        f"### 🎯 Interview Preparation Protocol ({role_match})\n\n"
        "**1. Behavioral Question (STAR Method):**\n"
        "> *'Tell me about a time you resolved a major production bottleneck or conflicting architectural decision.'*\n"
        "- **Situation**: Set the engineering problem and constraints.\n"
        "- **Task**: What was your specific responsibility?\n"
        "- **Action**: Concrete technical steps, tools, and compromises made.\n"
        "- **Result**: Measurable business impact (uptime, cost reduction, throughput).\n\n"
        "**2. Technical Architecture Question:**\n"
        "> *'How would you design a rate-limiter for a distributed API handling 100k requests/second?'*\n\n"
        "*Type your answer to either question below and I will critique it!*"
    )

if any(k in p for k in ["fraud", "scam", "fake", "legitimate", "suspicious", "telegram", "whatsapp"]):
    return (
        "### 🛡️ Recruitment Fraud Safeguard Checklist\n"
        "Watch out for these **definite red flags** in job communications:\n"
        "1. **Payment Requests**: Any demand for 'equipment fees', 'processing charges', or 'training deposits'.\n"
        "2. **Unofficial Channels**: Conducting formal hiring solely via Telegram, WhatsApp, or personal `@gmail.com` addresses.\n"
        "3. **No Interview**: Direct employment offers without technical rounds or video calls.\n"
        "4. **Financial Data**: Asking for netbanking credentials, OTPs, or crypto wallets.\n\n"
        "You can paste any suspicious offer text into the **🛡️ Fraud Job Detection** module above for an automated risk score!"
    )

if any(k in p for k in ["cover letter", "pitch", "message", "email to recruiter", "outreach"]):
    return (
        f"### ✉️ High-Response Recruiter Outreach Template\n\n"
        f"**Subject:** Application: [Target Role] — {name} ({', '.join(skills[:3]) if skills else 'Software Engineer'})\n\n"
        "Hi [Hiring Manager / Recruiter Name],\n\n"
        "I have been following [Company Name]'s recent work in [Specific Field/Product] and wanted to reach out regarding the [Job Title] role.\n\n"
        f"With hands-on experience in **{', '.join(skills[:4]) if skills else 'modern full-stack & cloud architectures'}**, "
        "I recently [mention your strongest quantified project or work achievement, e.g., 'scaled backend throughput by 40%']. "
        "I am confident I can bring immediate value to your engineering team.\n\n"
        "I have attached my resume for your review. Would you be open to a brief 10-minute conversation this week?\n\n"
        f"Best regards,\n**{name}**\n[LinkedIn Profile Link] | [GitHub Link]"
    )

if any(k in p for k in ["roadmap", "career plan", "future", "how to become", "steps"]):
    return (
        "### 🗺️ 5-Stage Career Acceleration Framework\n"
        "1. **Competency Benchmarking**: Diagnose technical gaps against tier-1 job listings.\n"
        "2. **Production Portfolio**: Build 2 deployed full-stack / ML applications with CI/CD and public documentation.\n"
        "3. **Metric-First Resume**: Highlight efficiency, scalability, and measurable business outputs.\n"
        "4. **System Design & Algorithm Prep**: Practice LeetCode mediums and distributed system trade-offs.\n"
        "5. **Targeted Outreach**: Direct outreach to engineering managers and recruiters."
    )

return (
    f"### 💡 CareerLens AI Advisory\n\n"
    f"You asked: *\"{prompt}\"*\n\n"
    "Here are key insights regarding your inquiry:\n"
    "- **Strategic Alignment**: Ensure all career and recruitment decisions align with measurable engineering competencies and verified industry standards.\n"
    "- **Best Practice**: Continuously calibrate your technical portfolio, keeping documentation and live deployment links active.\n"
    "- **Action Step**: Use the top navigation bar to explore your **Resume Quality Score**, **Semantic Job Match Index**, or **Fraud Risk Screening**.\n\n"
    "*Feel free to ask for specific code examples, resume bullet rewrites, or technical interview mock questions!*"
)
============================================================
SIDEBAR NAVIGATION & PERSISTENT LOGO
============================================================

with st.sidebar:
st.markdown(
"""<div style="padding: 10px 0 16px 0;">
<div style="display: flex; align-items: center; gap: 10px;">
<span style="font-size: 32px;">⚡</span>
<span style="font-size: 25px; font-weight: 800; color: #fff; letter-spacing: -0.5px;">
Career<span style="background: linear-gradient(135deg, #818cf8 0%, #c084fc 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Lens</span> AI
</span>
</div>
<div style="font-size: 10px; font-weight: 700; color: #818cf8; letter-spacing: 1.5px; margin-top: 4px; text-transform: uppercase;">
Career Intelligence Platform
</div>

</div>""", unsafe_allow_html=True, )

if st.button("🏠 Home / Job Seeker Hub", use_container_width=True):
    st.session_state.workspace_mode = "Job Seeker"
    st.session_state.active_nav = "Resume Intelligence"
    st.rerun()

st.markdown("---")

st.caption("SELECT WORKSPACE")
workspace_choice = st.radio(
    "Workspace Selector",
    ["👨‍💻 Job Seeker Workspace", "🏢 Recruiter Workspace"],
    index=0 if st.session_state.workspace_mode == "Job Seeker" else 1,
    label_visibility="collapsed",
)

if "Job Seeker" in workspace_choice:
    st.session_state.workspace_mode = "Job Seeker"
else:
    st.session_state.workspace_mode = "Recruiter"

st.markdown("---")

st.markdown(
    """<div class="status-pill">
<span class="status-dot"></span>
AI ENGINE ONLINE

</div> <div style="font-size: 11px; color: #64748b; margin-top: 10px; line-height: 1.5;"> NLP • Cosine TF-IDF • Skill Extraction • Fraud Heuristics </div>""", unsafe_allow_html=True, )

============================================================
WORKSPACE 1: JOB SEEKER DASHBOARD
============================================================

if st.session_state.workspace_mode == "Job Seeker":

st.markdown(
    """<div class="hero-container">
<div class="hero-badge-row">
    <div class="hero-pill">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#818cf8" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/>
        </svg>
        AI Career Intelligence
    </div>
    <div class="hero-pill" style="border-color: rgba(56, 189, 248, 0.35); background: rgba(56, 189, 248, 0.1); color: #7dd3fc;">
        Next-Gen Workspace
    </div>
</div>
<div class="hero-title">
    Understand Your Career. <span class="hero-gradient-text">Build Your Future.</span>
</div>
<p class="hero-description">
    CareerLens AI combines deep semantic NLP, precision skill indexing, real-time fraud risk screening, and adaptive career telemetry into a unified intelligence hub.
</p>
<div class="hero-features-grid">
    <div class="hero-mini-card">
        <div class="hero-icon-box">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>
            </svg>
        </div>
        <div class="hero-card-text">
            <h5>Resume Scoring</h5>
            <p>Structural & NLP Audit</p>
        </div>
    </div>
    <div class="hero-mini-card">
        <div class="hero-icon-box">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#818cf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>
            </svg>
        </div>
        <div class="hero-card-text">
            <h5>Semantic Matching</h5>
            <p>TF-IDF & Skill Alignment</p>
        </div>
    </div>
    <div class="hero-mini-card">
        <div class="hero-icon-box">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#f87171" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
            </svg>
        </div>
        <div class="hero-card-text">
            <h5>Fraud Shield</h5>
            <p>Heuristic Risk Detection</p>
        </div>
    </div>
    <div class="hero-mini-card">
        <div class="hero-icon-box">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#c084fc" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
            </svg>
        </div>
        <div class="hero-card-text">
            <h5>Career Advisor</h5>
            <p>Interactive Copilot</p>
        </div>
    </div>
</div>

</div>""", unsafe_allow_html=True, )

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
    st.metric("Skills Detected", skill_count)
with m4:
    st.metric("Applications Tracked", st.session_state.applications)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("#### ⚡ Module Navigation Bar")
nav_c1, nav_c2, nav_c3, nav_c4, nav_c5 = st.columns(5)

with nav_c1:
    if st.button("📄 Resume Intelligence", use_container_width=True, type="primary" if st.session_state.active_nav == "Resume Intelligence" else "secondary"):
        st.session_state.active_nav = "Resume Intelligence"
        st.rerun()

with nav_c2:
    if st.button("🎯 Job Matching", use_container_width=True, type="primary" if st.session_state.active_nav == "Job Matching" else "secondary"):
        st.session_state.active_nav = "Job Matching"
        st.rerun()

with nav_c3:
    if st.button("🛡️ Fraud Job Detection", use_container_width=True, type="primary" if st.session_state.active_nav == "Fraud Job Detection" else "secondary"):
        st.session_state.active_nav = "Fraud Job Detection"
        st.rerun()

with nav_c4:
    if st.button("🗺️ Skill & Roadmap", use_container_width=True, type="primary" if st.session_state.active_nav == "Skill & Roadmap" else "secondary"):
        st.session_state.active_nav = "Skill & Roadmap"
        st.rerun()

with nav_c5:
    if st.button("💬 AI Career Chatbot", use_container_width=True, type="primary" if st.session_state.active_nav == "AI Career Chatbot" else "secondary"):
        st.session_state.active_nav = "AI Career Chatbot"
        st.rerun()

st.markdown("---")

# ----------------------------------------------------
# MODULE 1: RESUME INTELLIGENCE
# ----------------------------------------------------
if st.session_state.active_nav == "Resume Intelligence":
    st.subheader("📄 Resume Intelligence & Profile Parsing")
    st.caption("Upload your resume in PDF, DOCX, or TXT format to evaluate your profile against industry scoring standards.")

    resume_file = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx", "txt"],
        key="js_resume_file",
        label_visibility="collapsed",
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

            st.success("✅ Resume indexed and analyzed successfully!")

            p_col1, p_col2 = st.columns(2)
            with p_col1:
                st.markdown(
                    f"""<div class="glass-card">
<h4 style="margin:0 0 12px 0;">👤 Candidate Profile</h4>
<p style="margin: 4px 0;"><b>Name:</b> {st.session_state.resume_analysis['name']}</p>
<p style="margin: 4px 0;"><b>Email:</b> {st.session_state.resume_analysis['email']}</p>
<p style="margin: 4px 0;"><b>Phone:</b> {st.session_state.resume_analysis['phone']}</p>
<p style="margin: 4px 0;"><b>Document:</b> {resume_file.name}</p>

</div>""", unsafe_allow_html=True, ) with p_col2: st.markdown( f"""<div class="glass-card"> <h4 style="margin:0 0 12px 0;">🛠️ Extracted Skills ({len(detected)})</h4> <div>{render_chips(detected)}</div> </div>""", unsafe_allow_html=True, )

# ----------------------------------------------------
# MODULE 2: JOB MATCHING
# ----------------------------------------------------
elif st.session_state.active_nav == "Job Matching":
    st.subheader("🎯 Semantic Job Matching Engine")
    st.caption("Evaluates semantic context similarity (TF-IDF + Cosine Similarity) blended with exact skill overlap.")

    job_input = st.text_area(
        "Paste Target Job Description",
        height=200,
        placeholder="Paste target job responsibilities, tech stack, and qualifications here...",
        key="match_jd_input",
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
                st.metric("Overall Match Score", f"{overall}%")
            with c2:
                st.metric("NLP Semantic Match", f"{nlp_sim}%")
            with c3:
                st.metric("Skill Alignment", f"{skill_sim}%")

            st.markdown("<br>", unsafe_allow_html=True)
            sc1, sc2 = st.columns(2)
            with sc1:
                st.markdown(
                    f"""<div class="glass-card">
<h4 style="color:#4ade80 !important; margin:0 0 12px 0;">✓ Matched Skills ({len(matched)})</h4>
<div>{render_chips(matched, 'chip chip-match')}</div>

</div>""", unsafe_allow_html=True, ) with sc2: st.markdown( f"""<div class="glass-card"> <h4 style="color:#f87171 !important; margin:0 0 12px 0;">⚠ Skill Gaps ({len(missing)})</h4> <div>{render_chips(missing, 'chip chip-gap')}</div> </div>""", unsafe_allow_html=True, )

# ----------------------------------------------------
# MODULE 3: FRAUD JOB DETECTION
# ----------------------------------------------------
elif st.session_state.active_nav == "Fraud Job Detection":
    st.subheader("🛡️ Job Fraud & Suspicious Signal Screening")
    st.caption("Screens listings for payment demands, banking requests, artificial urgency, and unofficial channels.")

    posting_input = st.text_area(
        "Paste Job Advertisement or Offer",
        height=180,
        placeholder="Paste job description, recruitment email, or offer text...",
        key="fraud_input",
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
                f"""<div style="margin: 15px 0;">
<span class="{badge_class}">{lvl} — RISK INDEX: {scr}/100</span>

</div>""", unsafe_allow_html=True, )

            if fraud_res["signals"]:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("#### Identified Risk Indicators")
                for cat, hits in fraud_res["signals"].items():
                    st.markdown(f"**{cat}:** `{', '.join(hits)}`")
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.success("✓ No common recruitment scam patterns or high-risk phrases detected.")

            st.caption("Advisory Note: AI screening detects statistical risk signals and is not a definitive certification of fraud or authenticity.")

# ----------------------------------------------------
# MODULE 4: SKILL & ROADMAP
# ----------------------------------------------------
elif st.session_state.active_nav == "Skill & Roadmap":
    st.subheader("🗺️ Skill Gap Diagnosis & Career Roadmap")
    st.caption("Transform technical missing links into an actionable step-by-step development strategy.")

    r_role = st.text_input("Target Career Role", placeholder="e.g., Lead Data Engineer, Senior Full-Stack Architect")
    r_jd = st.text_area("Target Job Context", height=150, placeholder="Paste target job qualifications to identify gaps...")

    if st.button("Generate Career Roadmap", use_container_width=True):
        if not st.session_state.resume_text:
            st.warning("⚠️ Please upload your resume in Resume Intelligence first.")
        elif not r_jd.strip():
            st.warning("⚠️ Please provide the target job context.")
        else:
            c_skills = detect_skills(st.session_state.resume_text)
            t_skills = detect_skills(r_jd)
            gaps = sorted(set(t_skills) - set(c_skills))

            st.markdown("#### Skill Deficit Diagnosis")
            st.markdown(f"**Target Role:** `{r_role or 'Target Role'}`")
            st.markdown(f"**Identified Gaps:** {render_chips(gaps, 'chip chip-gap')}", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### Structured 5-Phase Action Plan")

            steps = [
                f"**Phase 1: Core Competency Acquisition** — Prioritize learning: *{', '.join(gaps[:3]) if gaps else 'Advanced System Architecture'}*.",
                f"**Phase 2: Project Engineering** — Build 2 end-to-end applications demonstrating {', '.join(gaps[3:6]) if len(gaps) > 3 else 'high-throughput microservices and automated testing'}.",
                "**Phase 3: Impact-Oriented Resume Calibration** — Highlight quantified performance metrics (e.g., latency reduction, cost optimization) matching role expectations.",
                "**Phase 4: Technical & System Design Prep** — Master system trade-offs, architecture blueprints, and behavioral STAR questions.",
                "**Phase 5: Targeted Application Strategy** — Apply selectively to matching roles and refine resumes based on keyword feedback."
            ]

            for s in steps:
                st.markdown(f"- {s}")

# ----------------------------------------------------
# MODULE 5: RESPONSIVE AI CAREER CHATBOT
# ----------------------------------------------------
elif st.session_state.active_nav == "AI Career Chatbot":
    st.subheader("💬 AI Career Advisor Chatbot")
    st.caption("Ask anything: resume audits, mock interviews, skill roadmaps, tech stack advice, or recruiter cover letters.")

    st.markdown("**Quick Prompts:**")
    qc1, qc2, qc3, qc4 = st.columns(4)
    with qc1:
        if st.button("📊 Audit My Resume", use_container_width=True):
            st.session_state.chat_history.append({"role": "user", "content": "Analyze my resume score and give me improvements."})
            reply = generate_dynamic_bot_response("analyze my resume score and give me improvements")
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()
    with qc2:
        if st.button("🛠️ What Skills To Learn?", use_container_width=True):
            st.session_state.chat_history.append({"role": "user", "content": "What skills should I learn next?"})
            reply = generate_dynamic_bot_response("what skills should i learn next")
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()
    with qc3:
        if st.button("🎯 Mock Interview Question", use_container_width=True):
            st.session_state.chat_history.append({"role": "user", "content": "Give me a mock interview question."})
            reply = generate_dynamic_bot_response("give me an interview question and STAR method")
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()
    with qc4:
        if st.button("✉️ Draft Outreach Pitch", use_container_width=True):
            st.session_state.chat_history.append({"role": "user", "content": "Draft a recruiter outreach message."})
            reply = generate_dynamic_bot_response("draft a recruiter outreach email cover letter")
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask CareerLens AI anything about your career or recruitment..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        reply = generate_dynamic_bot_response(prompt)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)
============================================================
WORKSPACE 2: RECRUITER SCREENING DASHBOARD
============================================================

else:
st.markdown(
"""<div class="hero-banner">
<div class="hero-tag">Enterprise Screening Hub</div>
<div class="hero-heading">Bulk Resume Screening & <span>Candidate Ranking</span></div>
<p class="hero-sub">
Screen large batches of applicants against target job requirements. Compute TF-IDF semantic similarity and skill alignment, select your custom Top-N cohort, and export shortlists.
</p>

</div>""", unsafe_allow_html=True, )

rec_col1, rec_col2 = st.columns([1.2, 0.8])

with rec_col1:
    st.subheader("1. Job Requirements Benchmark")
    recruiter_job_text = st.text_area(
        "Benchmark Job Description",
        height=230,
        placeholder="Paste complete job requirements, responsibilities, and required skill sets...",
        key="rec_jd_box",
    )

with rec_col2:
    st.subheader("2. Shortlist Parameters")
    top_n_val = st.number_input(
        "Shortlist Limit (Top-N)",
        min_value=1,
        max_value=500,
        value=10,
        step=1,
        help="Recruiter decides the exact number of top candidates to shortlist.",
    )
    st.caption("Recruiter-controlled: Select any cohort size from 1 to 500.")

    candidate_batch = st.file_uploader(
        "Upload Batch Resumes (PDF, DOCX, TXT)",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        key="rec_batch_uploader",
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
            status_text.text(f"Analyzing ({i+1}/{total_docs}): {doc_file.name}")
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
                    "Status": "Failed / Unreadable",
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
                    "Status": "Screened",
                })

            bar.progress((i + 1) / total_docs)

        status_text.empty()
        bar.empty()

        df_results = pd.DataFrame(records)
        df_results = df_results.sort_values(
            by=["Overall Match", "Skill Match", "Resume Score"],
            ascending=False,
        ).reset_index(drop=True)

        df_results.insert(0, "Rank", range(1, len(df_results) + 1))
        st.session_state.recruiter_results = df_results
        st.success(f"✓ Screened and ranked {len(df_results)} resumes successfully!")

# Display Recruiter Results
if st.session_state.recruiter_results is not None:
    df_all = st.session_state.recruiter_results
    shortlist_size = min(int(top_n_val), len(df_all))
    df_top = df_all.head(shortlist_size)

    st.markdown("---")
    st.subheader("3. Ranked Candidate Shortlist")

    k1, k2, k3 = st.columns(3)
    with k1:
        st.metric("Total Resumes Screened", len(df_all))
    with k2:
        st.metric("Shortlisted Cohort", len(df_top))
    with k3:
        best_score = df_all.iloc[0]["Overall Match"] if not df_all.empty else 0
        st.metric("Top Candidate Score", f"{best_score}%")

    st.markdown(f"#### 🏆 Top {shortlist_size} Candidates")
    display_cols = ["Rank", "Candidate", "Email", "Resume Score", "NLP Match", "Skill Match", "Overall Match", "Missing Skills", "Status"]
    st.dataframe(df_top[display_cols], use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("4. Candidate Diagnostic Drill-Down")

    candidate_list = df_top["Candidate"].tolist()
    if candidate_list:
        selected_person = st.selectbox("Select Candidate for Diagnostic Analysis", candidate_list)
        row = df_top[df_top["Candidate"] == selected_person].iloc[0]

        cd1, cd2 = st.columns(2)
        with cd1:
            st.markdown(
                f"""<div class="glass-card">
<h4 style="margin:0 0 10px 0;">Candidate: {row['Candidate']}</h4>
<p><b>Email:</b> {row['Email']}</p>
<p><b>Overall Match:</b> {row['Overall Match']}%</p>
<p><b>Resume Quality Score:</b> {row['Resume Score']}/100</p>

</div>""", unsafe_allow_html=True, ) with cd2: st.markdown( f"""<div class="glass-card"> <h4 style="margin:0 0 10px 0;">Match Diagnostic</h4> <p><b>NLP Similarity:</b> {row['NLP Match']}%</p> <p><b>Skill Overlap:</b> {row['Skill Match']}%</p> <p><b>Skill Gaps:</b> {row['Missing Skills'] or 'None'}</p> </div>""", unsafe_allow_html=True, )

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
============================================================
PLATFORM FOOTER
============================================================

st.markdown("---")
st.markdown(
"""<div style="text-align: center; color: #475569; font-size: 12px; padding: 8px 0;">
⚡ <b>CareerLens AI</b> — AI-Powered Career Intelligence & Recruitment Platform | Final Year Project

</div>""", unsafe_allow_html=True, )

Close
