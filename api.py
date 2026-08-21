
from typing import List, Optional
import io
import re

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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
# APP
# ============================================================

app = FastAPI(
    title="CareerLens AI API",
    description="AI-powered Career Intelligence and Recruitment API",
    version="1.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# SKILL DATABASE
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
        "ai",
    ],
    "NLP": [
        "nlp",
        "natural language processing",
    ],
    "Computer Vision": ["computer vision"],
    "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch"],
    "Scikit-learn": [
        "scikit-learn",
        "sklearn",
    ],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Matplotlib": ["matplotlib"],
    "Data Analysis": [
        "data analysis",
        "data analytics",
    ],
    "Data Science": ["data science"],
    "Statistics": ["statistics"],
    "Power BI": ["power bi"],
    "Tableau": ["tableau"],
    "AWS": [
        "aws",
        "amazon web services",
    ],
    "Azure": ["azure"],
    "Google Cloud": [
        "gcp",
        "google cloud",
    ],
    "Docker": ["docker"],
    "Kubernetes": [
        "kubernetes",
        "k8s",
    ],
    "Git": ["git"],
    "GitHub": ["github"],
    "Linux": ["linux"],
    "MongoDB": [
        "mongodb",
        "mongo db",
    ],
    "PostgreSQL": [
        "postgresql",
        "postgres",
    ],
    "MySQL": ["mysql"],
    "Firebase": ["firebase"],
    "REST API": [
        "rest api",
        "restful api",
    ],
    "GraphQL": ["graphql"],
    "Microservices": ["microservices"],
    "System Design": ["system design"],
    "Cybersecurity": [
        "cybersecurity",
        "cyber security",
    ],
    "Networking": [
        "networking",
        "computer networks",
    ],
    "Agile": ["agile"],
    "Scrum": ["scrum"],
    "Communication": [
        "communication skills",
    ],
    "Leadership": ["leadership"],
    "Problem Solving": [
        "problem solving",
        "problem-solving",
    ],
}


# ============================================================
# FRAUD DATABASE
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


# ============================================================
# MODELS
# ============================================================

class TextRequest(BaseModel):
    text: str


class JobMatchRequest(BaseModel):
    resume_text: str
    job_description: str


class SkillGapRequest(BaseModel):
    resume_text: str
    target_job: str


class RoadmapRequest(BaseModel):
    target_role: str
    current_skills: Optional[List[str]] = []


# ============================================================
# HELPERS
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
        text or "",
    )

    return match.group(0) if match else None


def extract_phone(text: str):

    match = re.search(
        r"(?:\+?\d[\d\s().-]{7,}\d)",
        text or "",
    )

    return (
        match.group(0).strip()
        if match
        else None
    )


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

        if any(
            item in lower
            for item in ignored
        ):
            continue

        cleaned = re.sub(
            r"[^A-Za-z .'-]",
            "",
            line,
        ).strip()

        words = cleaned.split()

        if 2 <= len(words) <= 5:
            return cleaned

    return "Candidate"


# ============================================================
# FILE EXTRACTION
# ============================================================

async def extract_uploaded_file(
    file: UploadFile,
) -> str:

    data = await file.read()

    filename = (
        file.filename or ""
    ).lower()

    try:

        if filename.endswith(".txt"):

            return data.decode(
                "utf-8",
                errors="ignore",
            )

        if filename.endswith(".pdf"):

            if PdfReader is None:
                raise HTTPException(
                    status_code=500,
                    detail="PyPDF2 is not installed.",
                )

            reader = PdfReader(
                io.BytesIO(data)
            )

            pages = []

            for page in reader.pages:

                try:
                    pages.append(
                        page.extract_text()
                        or ""
                    )
                except Exception:
                    pass

            return "\n".join(pages)

        if filename.endswith(".docx"):

            if Document is None:
                raise HTTPException(
                    status_code=500,
                    detail="python-docx is not installed.",
                )

            document = Document(
                io.BytesIO(data)
            )

            return "\n".join(
                paragraph.text
                for paragraph in document.paragraphs
            )

    except HTTPException:
        raise

    except Exception as exc:

        raise HTTPException(
            status_code=400,
            detail=f"Unable to read file: {exc}",
        )

    raise HTTPException(
        status_code=400,
        detail="Unsupported file type. Use PDF, DOCX or TXT.",
    )


# ============================================================
# RESUME SCORE
# ============================================================

def calculate_resume_score(
    text: str,
) -> int:

    text = clean_text(text)

    if not text:
        return 0

    score = 0

    skills = extract_skills(text)

    score += min(
        len(skills) * 4,
        30,
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
        min(100, score),
    )


def calculate_readiness(
    resume_score: int,
    skill_count: int,
) -> int:

    return max(
        0,
        min(
            100,
            round(
                resume_score * 0.70
                + min(
                    skill_count * 3,
                    30,
                )
            ),
        ),
    )


# ============================================================
# JOB MATCHING
# ============================================================

def calculate_job_match(
    resume_text: str,
    job_text: str,
):

    resume_text = clean_text(
        resume_text
    )

    job_text = clean_text(
        job_text
    )

    if not resume_text or not job_text:

        return {
            "overall": 0,
            "nlp_similarity": 0,
            "skill_match": 0,
            "matched_skills": [],
            "missing_skills": [],
        }

    nlp_score = 0

    try:

        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=5000,
        )

        matrix = vectorizer.fit_transform(
            [
                resume_text,
                job_text,
            ]
        )

        similarity = cosine_similarity(
            matrix[0:1],
            matrix[1:2],
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
        "overall": min(
            100,
            max(0, overall),
        ),
        "nlp_similarity": min(
            100,
            max(0, nlp_score),
        ),
        "skill_match": min(
            100,
            max(0, skill_score),
        ),
        "matched_skills": matched,
        "missing_skills": missing,
    }


# ============================================================
# FRAUD DETECTION
# ============================================================

def detect_fraud(text: str):

    lower = clean_text(
        text
    ).lower()

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
        ),
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
# HEALTH
# ============================================================

@app.get("/")
def root():

    return {
        "name": "CareerLens AI",
        "status": "online",
        "version": "1.0.0",
        "message": "CareerLens AI API is running.",
    }


@app.get("/health")
def health():

    return {
        "status": "healthy",
        "service": "CareerLens AI",
    }


# ============================================================
# RESUME ANALYSIS
# ============================================================

@app.post("/api/resume/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
):

    text = await extract_uploaded_file(
        file
    )

    text = clean_text(text)

    if not text:

        raise HTTPException(
            status_code=400,
            detail="No readable text found in the resume.",
        )

    skills = extract_skills(text)

    score = calculate_resume_score(
        text
    )

    readiness = calculate_readiness(
        score,
        len(skills),
    )

    return {
        "success": True,
        "candidate": {
            "name": extract_name(text),
            "email": extract_email(text),
            "phone": extract_phone(text),
        },
        "resume_score": score,
        "career_readiness": readiness,
        "skills_detected": len(skills),
        "skills": skills,
        "word_count": len(text.split()),
        "text_preview": text[:1000],
    }


# ============================================================
# SKILLS
# ============================================================

@app.post("/api/resume/skills")
def resume_skills(
    request: TextRequest,
):

    text = clean_text(
        request.text
    )

    skills = extract_skills(
        text
    )

    return {
        "success": True,
        "skills": skills,
        "count": len(skills),
    }


# ============================================================
# JOB MATCH
# ============================================================

@app.post("/api/job/match")
def job_match(
    request: JobMatchRequest,
):

    if not request.resume_text.strip():

        raise HTTPException(
            status_code=400,
            detail="Resume text is required.",
        )

    if not request.job_description.strip():

        raise HTTPException(
            status_code=400,
            detail="Job description is required.",
        )

    result = calculate_job_match(
        request.resume_text,
        request.job_description,
    )

    return {
        "success": True,
        **result,
    }


# ============================================================
# FRAUD
# ============================================================

@app.post("/api/job/fraud")
def job_fraud(
    request: TextRequest,
):

    if not request.text.strip():

        raise HTTPException(
            status_code=400,
            detail="Job advertisement text is required.",
        )

    result = detect_fraud(
        request.text
    )

    return {
        "success": True,
        **result,
    }


# ============================================================
# SKILL GAP
# ============================================================

@app.post("/api/skills/gap")
def skill_gap(
    request: SkillGapRequest,
):

    resume_skills = set(
        extract_skills(
            request.resume_text
        )
    )

    required_skills = set(
        extract_skills(
            request.target_job
        )
    )

    matched = sorted(
        resume_skills
        & required_skills
    )

    missing = sorted(
        required_skills
        - resume_skills
    )

    if required_skills:

        coverage = round(
            len(matched)
            / len(required_skills)
            * 100
        )

    else:

        coverage = 100

    return {
        "success": True,
        "current_skills": sorted(
            resume_skills
        ),
        "required_skills": sorted(
            required_skills
        ),
        "matched_skills": matched,
        "missing_skills": missing,
        "skill_coverage": coverage,
    }


# ============================================================
# CAREER ROADMAP
# ============================================================

@app.post("/api/career/roadmap")
def career_roadmap(
    request: RoadmapRequest,
):

    role = request.target_role.strip()

    if not role:

        raise HTTPException(
            status_code=400,
            detail="Target role is required.",
        )

    current_skills = [
        skill.strip()
        for skill in request.current_skills
        if skill.strip()
    ]

    roadmap = [
        {
            "step": 1,
            "title": "Foundation",
            "description": (
                f"Build the fundamentals required "
                f"for a {role} career."
            ),
        },
        {
            "step": 2,
            "title": "Core Skills",
            "description": (
                "Develop the technical and "
                "professional skills most relevant "
                "to the target role."
            ),
        },
        {
            "step": 3,
            "title": "Portfolio Projects",
            "description": (
                "Create practical projects that "
                "demonstrate your ability to solve "
                "real-world problems."
            ),
        },
        {
            "step": 4,
            "title": "Interview Preparation",
            "description": (
                "Prepare technical, behavioral "
                "and role-specific interview skills."
            ),
        },
        {
            "step": 5,
            "title": "Career Launch",
            "description": (
                "Optimize your resume, portfolio "
                "and job application strategy."
            ),
        },
    ]

    return {
        "success": True,
        "target_role": role,
        "current_skills": current_skills,
        "roadmap": roadmap,
    }


# ============================================================
# BATCH RECRUITER MATCHING
# ============================================================

class Candidate(BaseModel):
    name: str
    resume_text: str


class RecruiterScreenRequest(BaseModel):
    job_description: str
    candidates: List[Candidate]
    top_n: int = 10


@app.post("/api/recruiter/screen")
def recruiter_screen(
    request: RecruiterScreenRequest,
):

    if not request.job_description.strip():

        raise HTTPException(
            status_code=400,
            detail="Job description is required.",
        )

    if not request.candidates:

        raise HTTPException(
            status_code=400,
            detail="At least one candidate is required.",
        )

    top_n = max(
        1,
        min(
            request.top_n,
            len(request.candidates),
        ),
    )

    results = []

    for candidate in request.candidates:

        match = calculate_job_match(
            candidate.resume_text,
            request.job_description,
        )

        resume_score = calculate_resume_score(
            candidate.resume_text
        )

        results.append(
            {
                "name": candidate.name,
                "resume_score": resume_score,
                "nlp_similarity": match[
                    "nlp_similarity"
                ],
                "skill_match": match[
                    "skill_match"
                ],
                "overall_match": match[
                    "overall"
                ],
                "matched_skills": match[
                    "matched_skills"
                ],
                "missing_skills": match[
                    "missing_skills"
                ],
            }
        )

    results.sort(
        key=lambda item: item[
            "overall_match"
        ],
        reverse=True,
    )

    for index, result in enumerate(
        results[:top_n],
        start=1,
    ):

        result["rank"] = index

    return {
        "success": True,
        "total_candidates": len(results),
        "shortlist": results[:top_n],
    }


# ============================================================
# RUN LOCALLY
# ============================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )

