import io
import re
from typing import List, Optional

from docx import Document
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI(title="CareerLens AI API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# SKILL & FRAUD DATABASES
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
    "Artificial Intelligence": ["artificial intelligence", "ai"],
    "NLP": ["nlp", "natural language processing"],
    "Computer Vision": ["computer vision"],
    "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch"],
    "Scikit-learn": ["scikit-learn", "sklearn"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Data Science": ["data science"],
    "Data Analysis": ["data analysis", "data analytics"],
    "Power BI": ["power bi"],
    "Tableau": ["tableau"],
    "AWS": ["aws", "amazon web services"],
    "Azure": ["azure"],
    "Google Cloud": ["gcp", "google cloud"],
    "Docker": ["docker"],
    "Kubernetes": ["kubernetes", "k8s"],
    "Git": ["git"],
    "GitHub": ["github"],
    "Linux": ["linux"],
    "MongoDB": ["mongodb"],
    "PostgreSQL": ["postgresql", "postgres"],
    "MySQL": ["mysql"],
    "REST API": ["rest api", "restful api"],
    "Agile": ["agile"],
    "Communication": ["communication skills"],
    "Leadership": ["leadership"],
    "Problem Solving": ["problem solving", "problem-solving"],
}

FRAUD_PATTERNS = {
    "Financial Requests": [
        "pay a fee",
        "registration fee",
        "processing fee",
        "send money",
        "wire transfer",
        "payment required",
        "deposit",
    ],
    "Urgency": ["act now", "urgent", "immediately", "today only"],
    "Sensitive Information": [
        "bank details",
        "account number",
        "password",
        "otp",
        "social security",
    ],
    "Suspicious Communication": [
        "telegram",
        "whatsapp only",
        "crypto",
        "gift card",
        "bitcoin",
    ],
}

# ============================================================
# PARSING & NLP HELPERS
# ============================================================


def clean_text(text: str) -> str:
  if not text:
    return ""
  text = text.replace("\x00", " ")
  return re.sub(r"\s+", " ", text).strip()


def extract_skills(text: str) -> List[str]:
  text_lower = clean_text(text).lower()
  found = []
  for skill, patterns in SKILLS.items():
    for pattern in patterns:
      if re.search(r"\b" + re.escape(pattern) + r"\b", text_lower):
        found.append(skill)
        break
  return sorted(set(found))


def extract_email(text: str) -> Optional[str]:
  match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text or "")
  return match.group(0) if match else None


def extract_phone(text: str) -> Optional[str]:
  match = re.search(r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text or "")
  return match.group(0).strip() if match else None


def extract_name(raw_text: str) -> str:
  lines = [
      line.strip() for line in (raw_text or "").splitlines() if line.strip()
  ]
  ignored = [
      "resume",
      "curriculum",
      "vitae",
      "profile",
      "objective",
      "email",
      "phone",
      "contact",
      "page",
  ]

  for line in lines[:8]:
    if "@" in line or any(digit in line for digit in "0123456789"):
      continue
    if any(item in line.lower() for item in ignored):
      continue
    cleaned = re.sub(r"[^A-Za-z\s]", "", line).strip()
    words = cleaned.split()
    if 2 <= len(words) <= 4 and all(len(w) > 1 for w in words):
      return cleaned.title()
  return "Candidate"


def parse_file_bytes(data: bytes, filename: str) -> str:
  filename = filename.lower()
  if filename.endswith(".txt"):
    return data.decode("utf-8", errors="ignore")
  if filename.endswith(".pdf"):
    reader = PdfReader(io.BytesIO(data))
    return "\n".join([page.extract_text() or "" for page in reader.pages])
  if filename.endswith(".docx"):
    doc = Document(io.BytesIO(data))
    return "\n".join([p.text for p in doc.paragraphs])
  return ""


def calculate_resume_score(text: str) -> int:
  score = 0
  skills = extract_skills(text)
  score += min(len(skills) * 4, 30)
  if extract_email(text):
    score += 10
  if extract_phone(text):
    score += 10

  sections = ["education", "experience", "projects", "skills", "summary"]
  for s in sections:
    if s in text.lower():
      score += 6

  words = len(text.split())
  if words >= 250:
    score += 10
  if words >= 450:
    score += 10
  return min(100, max(10, score))


def compute_job_match(resume_text: str, job_text: str):
  if not resume_text.strip() or not job_text.strip():
    return {
        "overall": 0,
        "semantic": 0,
        "skill_match": 0,
        "matched": [],
        "missing": [],
    }

  try:
    vectorizer = TfidfVectorizer(
        stop_words="english", ngram_range=(1, 2), max_features=5000
    )
    matrix = vectorizer.fit_transform([resume_text, job_text])
    nlp_score = round(cosine_similarity(matrix[0:1], matrix[1:2])[0][0] * 100)
  except Exception:
    nlp_score = 0

  resume_skills = set(extract_skills(resume_text))
  job_skills = set(extract_skills(job_text))
  matched = sorted(resume_skills & job_skills)
  missing = sorted(job_skills - resume_skills)

  skill_score = (
      round((len(matched) / len(job_skills)) * 100) if job_skills else nlp_score
  )
  overall = round((nlp_score * 0.5) + (skill_score * 0.5))

  return {
      "overall": min(100, overall),
      "semantic": min(100, nlp_score),
      "skill_match": min(100, skill_score),
      "matched": matched,
      "missing": missing,
  }


# ============================================================
# ENDPOINTS
# ============================================================


@app.get("/")
def root():
  return {"status": "online", "message": "CareerLens AI API is running"}


@app.get("/health")
def health():
  return {"status": "healthy", "service": "CareerLens AI"}


@app.post("/api/resume/analyze")
async def analyze_resume(file: UploadFile = File(...)):
  data = await file.read()
  raw_text = parse_file_bytes(data, file.filename or "")
  cleaned = clean_text(raw_text)

  if not cleaned:
    raise HTTPException(
        status_code=400, detail="Could not extract text from document."
    )

  skills = extract_skills(cleaned)
  score = calculate_resume_score(cleaned)
  readiness = min(100, round((score * 0.7) + min(len(skills) * 3, 30)))

  return {
      "name": extract_name(raw_text),
      "email": extract_email(cleaned) or "Not detected",
      "phone": extract_phone(cleaned) or "Not detected",
      "experience": "Identified",
      "resume_score": score,
      "readiness": readiness,
      "skills": skills,
      "extracted_text": cleaned,
  }


class MatchReq(BaseModel):
  resume_text: str
  job_description: str


@app.post("/api/job/match")
def job_match(req: MatchReq):
  return compute_job_match(req.resume_text, req.job_description)


class TextReq(BaseModel):
  text: str


@app.post("/api/job/fraud")
def fraud_detection(req: TextReq):
  text_lower = clean_text(req.text).lower()
  signals = {}
  for cat, patterns in FRAUD_PATTERNS.items():
    matches = [p for p in patterns if p in text_lower]
    if matches:
      signals[cat] = matches

  total_flags = sum(len(v) for v in signals.values())
  risk_score = min(100, total_flags * 20)
  level = (
      "HIGH RISK"
      if risk_score >= 40
      else ("MEDIUM RISK" if risk_score >= 20 else "LOW RISK")
  )
  return {"score": risk_score, "level": level, "signals": total_flags}


class SkillGapReq(BaseModel):
  resume_text: str
  target_job: str


@app.post("/api/skills/gap")
def skill_gap(req: SkillGapReq):
  r_skills = set(extract_skills(req.resume_text))
  j_skills = set(extract_skills(req.target_job))
  return {
      "matched": sorted(r_skills & j_skills),
      "missing": sorted(j_skills - r_skills),
  }


class RoadmapReq(BaseModel):
  resume_text: Optional[str] = ""
  target_role: str


@app.post("/api/career/roadmap")
def roadmap(req: RoadmapReq):
  role = req.target_role.strip()
  return {
      "steps": [
          f"Master core foundations and syntax required for {role}.",
          (
              "Deepen expertise in relevant frameworks, cloud tooling, and"
              " microservices."
          ),
          (
              f"Build 2 end-to-end industry portfolio projects targeting"
              f" {role} challenges."
          ),
          (
              "Refine system design, behavioral storytelling, and technical"
              " interview prep."
          ),
          (
              "Tailor resume keywords and actively network with hiring"
              f" teams in {role} domains."
          ),
      ]
  }


@app.post("/api/recruiter/screen")
async def recruiter_screen(
    job_description: str = Form(...), files: List[UploadFile] = File(...)
):
  candidates = []
  for f in files:
    data = await f.read()
    raw = parse_file_bytes(data, f.filename or "")
    cleaned = clean_text(raw)
    name = extract_name(raw)
    match_data = compute_job_match(cleaned, job_description)
    score = calculate_resume_score(cleaned)

    candidates.append({
        "Candidate": name,
        "File": f.filename,
        "Resume Score": f"{score}/100",
        "Match Score": f"{match_data['overall']}%",
        "Matched Skills": ", ".join(match_data["matched"][:6]) or "None",
        "Missing Skills": ", ".join(match_data["missing"][:4]) or "None",
        "_raw_score": match_data["overall"],
    })

  candidates.sort(key=lambda x: x["_raw_score"], reverse=True)
  for c in candidates:
    del c["_raw_score"]
  return candidates


class ChatMessage(BaseModel):
  role: str
  content: str


class ChatReq(BaseModel):
  messages: List[ChatMessage]
  resume_context: Optional[str] = ""


@app.post("/api/chat/ask")
def chat_assistant(req: ChatReq):
  latest_user_msg = req.messages[-1].content.lower()
  r_context = req.resume_context.lower()

  if "ats" in latest_user_msg or "score" in latest_user_msg:
    return {
        "reply": (
            "To maximize ATS readability: use single-column layouts, standard"
            " headers ('Experience', 'Education', 'Skills'), match phrasing"
            " directly from the job description, and avoid non-standard fonts"
            " or nested tables."
        )
    }
  elif "skill" in latest_user_msg or "gap" in latest_user_msg:
    detected = extract_skills(r_context)
    if detected:
      return {
          "reply": (
              f"I noticed skills like {', '.join(detected[:5])} in your"
              " resume. Focus on pairing these with verifiable project metrics"
              " (e.g., 'reduced latency by 20%')."
          )
      }
    return {
        "reply": (
            "Be sure to categorize skills into 'Programming Languages',"
            " 'Frameworks/Libraries', and 'Cloud/DevOps' for maximum clarity."
        )
    }
  elif "project" in latest_user_msg:
    return {
        "reply": (
            "Standout projects should follow the STAR format (Situation, Task,"
            " Action, Result), include live deployment links or GitHub repos,"
            " and address real-world business metrics."
        )
    }
  return {
      "reply": (
          "I can assist with resume optimization, ATS best practices,"
          " interview questions, or skill roadmaps. What specific topic would"
          " you like to dive into?"
      )
  }


if __name__ == "__main__":
  import uvicorn

  uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
