import io
from typing import Dict, List
import pandas as pd
import requests
import streamlit as st

API_BASE_URL = "https://careerlens-ai-9dx8.onrender.com"

st.set_page_config(
    page_title="CareerLens AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
:root{
    --bg:#07111f;
    --panel:#0d1a2b;
    --border:#213754;
    --text:#f4f7fb;
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
.card-icon{ font-size:28px; }
.card-title{ color:white; font-weight:800; font-size:17px; margin-top:9px; }
.card-text{ color:#8fa2ba; font-size:13px; line-height:1.6; margin-top:7px; }
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
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# API CALLS
# ============================================================


def api_analyze_resume(file) -> Dict:
  files = {"file": (file.name, file.getvalue(), file.type)}
  res = requests.post(
      f"{API_BASE_URL}/api/resume/analyze", files=files, timeout=60
  )
  res.raise_for_status()
  return res.json()


def api_match_job(resume_text: str, job_description: str) -> Dict:
  payload = {"resume_text": resume_text, "job_description": job_description}
  res = requests.post(f"{API_BASE_URL}/api/job/match", json=payload, timeout=30)
  res.raise_for_status()
  return res.json()


def api_detect_fraud(job_text: str) -> Dict:
  payload = {"text": job_text}
  res = requests.post(f"{API_BASE_URL}/api/job/fraud", json=payload, timeout=30)
  res.raise_for_status()
  return res.json()


def api_skill_gap(resume_text: str, target_job: str) -> Dict:
  payload = {"resume_text": resume_text, "target_job": target_job}
  res = requests.post(
      f"{API_BASE_URL}/api/skills/gap", json=payload, timeout=30
  )
  res.raise_for_status()
  return res.json()


def api_career_roadmap(resume_text: str, target_role: str) -> Dict:
  payload = {"resume_text": resume_text, "target_role": target_role}
  res = requests.post(
      f"{API_BASE_URL}/api/career/roadmap", json=payload, timeout=30
  )
  res.raise_for_status()
  return res.json()


def api_screen_candidates(files: List, job_description: str) -> List[Dict]:
  file_payload = [("files", (f.name, f.getvalue(), f.type)) for f in files]
  data_payload = {"job_description": job_description}
  res = requests.post(
      f"{API_BASE_URL}/api/recruiter/screen",
      files=file_payload,
      data=data_payload,
      timeout=120,
  )
  res.raise_for_status()
  return res.json()


def api_chat_assistant(messages: List[Dict], resume_context: str = "") -> str:
  payload = {"messages": messages, "resume_context": resume_context}
  try:
    res = requests.post(
        f"{API_BASE_URL}/api/chat/ask", json=payload, timeout=30
    )
    if res.status_code == 200:
      return res.json().get(
          "reply", "I am ready to help optimize your career path."
      )
  except Exception:
    pass
  return "Focus on quantifiable achievements, matching core job description keywords, and maintaining clean ATS formatting."


# ============================================================
# STATE & HELPERS
# ============================================================

if "resume_text" not in st.session_state:
  st.session_state.resume_text = ""
if "resume_analysis" not in st.session_state:
  st.session_state.resume_analysis = None
if "applications" not in st.session_state:
  st.session_state.applications = 0
if "recruiter_df" not in st.session_state:
  st.session_state.recruiter_df = None


def metric_row(values):
  columns = st.columns(len(values))
  for column, (label, value, help_text) in zip(columns, values):
    with column:
      st.metric(label, value, help=help_text)


def show_skills(skills):
  if not skills:
    st.caption("No skills detected.")
    return
  html = "".join(f'<span class="skill">{skill}</span>' for skill in skills)
  st.markdown(html, unsafe_allow_html=True)


# ============================================================
# SIDEBAR
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

  workspace = st.radio("WORKSPACE", ["👨‍💻 Job Seeker", "🏢 Recruiter"])
  st.divider()

  try:
    health_check = requests.get(f"{API_BASE_URL}/health", timeout=3)
    if health_check.status_code == 200:
      st.markdown(
          '<span class="status">● BACKEND CONNECTED</span>',
          unsafe_allow_html=True,
      )
    else:
      st.warning("⚠️ Backend Degraded")
  except Exception:
    st.error("❌ Backend Offline")

  st.caption("NLP • ML • FastAPI Microservice")
  st.divider()
  st.caption("CareerLens AI v2.0")


# ============================================================
# JOB SEEKER
# ============================================================

if workspace == "👨‍💻 Job Seeker":

  st.markdown(
      """
        <section class="hero">
            <div class="kicker">AI CAREER INTELLIGENCE</div>
            <h1>Understand Your Career.<br><span>Build Your Future.</span></h1>
            <p>CareerLens AI connects to our cloud ML engine for resume parsing, semantic matching, fraud detection, and roadmap generation.</p>
        </section>
        """,
      unsafe_allow_html=True,
  )

  analysis = st.session_state.resume_analysis
  score = f"{analysis.get('resume_score', '—')}/100" if analysis else "—"
  readiness = f"{analysis.get('readiness', '—')}%" if analysis else "—"
  skills_count = len(analysis.get("skills", [])) if analysis else 0

  metric_row([
      ("Resume Score", score, "AI-assisted resume quality score"),
      ("Career Readiness", readiness, "Profile readiness estimate"),
      ("Skills Detected", skills_count, "Skills extracted by AI backend"),
      ("Applications", st.session_state.applications, "Tracked applications"),
  ])

  st.divider()

  tabs = st.tabs([
      "📄 Resume Intelligence",
      "🎯 Job Match",
      "🛡️ Fraud Risk",
      "🧩 Skill Gap",
      "🗺️ Career Roadmap",
      "💬 AI Career Assistant",
  ])

  # 1. Resume Intelligence
  with tabs[0]:
    st.subheader("Resume Intelligence")
    resume_file = st.file_uploader(
        "Upload Resume", type=["pdf", "docx", "txt"], key="resume_upload"
    )

    if resume_file and st.button(
        "Analyze Resume via API", type="primary", use_container_width=True
    ):
      with st.spinner("Connecting to Render backend..."):
        try:
          result = api_analyze_resume(resume_file)
          st.session_state.resume_analysis = result
          st.session_state.resume_text = result.get("extracted_text", "")
          st.success("Resume processed successfully!")
        except Exception as exc:
          st.error(f"Backend API error: {exc}")

    if st.session_state.resume_analysis:
      res = st.session_state.resume_analysis
      c1, c2 = st.columns(2)
      with c1:
        st.write("**Name:**", res.get("name", "Candidate"))
        st.write("**Email:**", res.get("email", "Not detected"))
      with c2:
        st.write("**Phone:**", res.get("phone", "Not detected"))
        st.write("**Experience:**", res.get("experience", "Identified"))

      st.subheader("Detected Skills")
      show_skills(res.get("skills", []))

  # 2. Job Match
  with tabs[1]:
    st.subheader("Semantic Job Matching")
    job_desc = st.text_area("Paste job description", height=200, key="jobmatch")

    if st.button(
        "Analyze Match via API", type="primary", use_container_width=True
    ):
      if not st.session_state.resume_text:
        st.warning("Please upload and analyze your resume first.")
      elif not job_desc.strip():
        st.warning("Please enter a job description.")
      else:
        with st.spinner("Running semantic matching model..."):
          try:
            result = api_match_job(st.session_state.resume_text, job_desc)
            metric_row([
                (
                    "Overall Match",
                    f"{result.get('overall', 0)}%",
                    "Weighted alignment",
                ),
                (
                    "Semantic Similarity",
                    f"{result.get('semantic', 0)}%",
                    "NLP Cosine match",
                ),
                (
                    "Skill Match",
                    f"{result.get('skill_match', 0)}%",
                    "Overlap percentage",
                ),
            ])
            st.progress(result.get("overall", 0) / 100)
            st.subheader("Matched Skills")
            show_skills(result.get("matched", []))
            st.subheader("Missing Skills")
            show_skills(result.get("missing", []))
          except Exception as exc:
            st.error(f"API Error: {exc}")

  # 3. Fraud Risk
  with tabs[2]:
    st.subheader("Job Fraud Risk Intelligence")
    jobrisk = st.text_area("Paste job advertisement", height=200, key="risk")

    if st.button(
        "Run Risk Analysis via API", type="primary", use_container_width=True
    ):
      if not jobrisk.strip():
        st.warning("Enter a job advertisement to evaluate.")
      else:
        with st.spinner("Evaluating scam signals..."):
          try:
            res = api_detect_fraud(jobrisk)
            metric_row([
                (
                    "Risk Score",
                    f"{res.get('score', 0)}/100",
                    "Heuristic fraud probability",
                ),
                (
                    "Risk Level",
                    res.get("level", "LOW RISK"),
                    "Screening verdict",
                ),
                (
                    "Signals Detected",
                    res.get("signals", 0),
                    "Triggered flags",
                ),
            ])
            if res.get("level") == "HIGH RISK":
              st.error("⚠️ High risk patterns detected.")
            else:
              st.success("✅ Low risk detected.")
          except Exception as exc:
            st.error(f"API Error: {exc}")

  # 4. Skill Gap
  with tabs[3]:
    st.subheader("Skill Gap Analysis")
    target_job = st.text_area("Target job description", height=200, key="gap")

    if st.button(
        "Analyze Skill Gap via API", type="primary", use_container_width=True
    ):
      if not st.session_state.resume_text:
        st.warning("Upload your resume first.")
      elif not target_job.strip():
        st.warning("Enter target job requirements.")
      else:
        with st.spinner("Calculating skill matrix..."):
          try:
            res = api_skill_gap(st.session_state.resume_text, target_job)
            st.subheader("Matched Skills")
            show_skills(res.get("matched", []))
            st.subheader("Missing Skills to Prioritize")
            show_skills(res.get("missing", []))
          except Exception as exc:
            st.error(f"API Error: {exc}")

  # 5. Career Roadmap
  with tabs[4]:
    st.subheader("Personalized Career Roadmap")
    role = st.text_input("Target role", "Machine Learning Engineer")

    if st.button(
        "Generate Roadmap via API", type="primary", use_container_width=True
    ):
      with st.spinner("Generating personalized development plan..."):
        try:
          res = api_career_roadmap(st.session_state.resume_text, role)
          steps = res.get("steps", [])
          for idx, step in enumerate(steps, 1):
            st.markdown(
                f"""
                            <div class="panel">
                                <div class="small-label">STEP {idx:02d}</div>
                                <div class="card-title">{step}</div>
                            </div>
                            """,
                unsafe_allow_html=True,
            )
        except Exception as exc:
          st.error(f"API Error: {exc}")

  # 6. Chatbot
  with tabs[5]:
    st.subheader("CareerLens AI Assistant")

    if "chat_messages" not in st.session_state:
      st.session_state.chat_messages = [{
          "role": "assistant",
          "content": (
              "Hello! Ask me anything about resume optimization, ATS keywords,"
              " interview preparation, or skill roadmaps."
          ),
      }]

    st.caption("Quick Questions:")
    q_cols = st.columns(3)
    faqs = [
        "How do I optimize my resume for ATS?",
        "How do I present my technical skills?",
        "What makes a project stand out?",
    ]

    chosen_faq = None
    for i, faq in enumerate(faqs):
      if q_cols[i].button(faq, key=f"btn_faq_{i}", use_container_width=True):
        chosen_faq = faq

    for msg in st.session_state.chat_messages:
      with st.chat_message(msg["role"]):
        st.write(msg["content"])

    user_input = st.chat_input("Ask a question about your resume or career...")
    active_prompt = chosen_faq or user_input

    if active_prompt:
      st.session_state.chat_messages.append(
          {"role": "user", "content": active_prompt}
      )
      with st.chat_message("user"):
        st.write(active_prompt)

      with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
          ans = api_chat_assistant(
              st.session_state.chat_messages,
              resume_context=st.session_state.resume_text,
          )
          st.write(ans)
      st.session_state.chat_messages.append(
          {"role": "assistant", "content": ans}
      )
      st.rerun()

# ============================================================
# RECRUITER WORKSPACE
# ============================================================

else:
  st.markdown(
      """
        <section class="hero">
            <div class="kicker">RECRUITMENT INTELLIGENCE</div>
            <h1>Screen Smarter.<br><span>Hire with Evidence.</span></h1>
            <p>Bulk upload candidate resumes to rank them through the Render ML backend.</p>
        </section>
        """,
      unsafe_allow_html=True,
  )

  recruiter_job = st.text_area(
      "Job Description", height=200, key="recruiter_job"
  )
  recruiter_files = st.file_uploader(
      "Candidate Resumes",
      type=["pdf", "docx", "txt"],
      accept_multiple_files=True,
      key="candidate_files",
  )
  top_n = st.number_input(
      "Shortlist Size", min_value=1, max_value=100, value=10
  )

  if st.button(
      "🚀 Screen Candidates via Backend API",
      type="primary",
      use_container_width=True,
  ):
    if not recruiter_job.strip() or not recruiter_files:
      st.warning("Please provide a job description and candidate resumes.")
    else:
      with st.spinner("Backend is ranking candidate pool..."):
        try:
          candidates_data = api_screen_candidates(
              recruiter_files, recruiter_job
          )
          st.session_state.recruiter_df = pd.DataFrame(candidates_data)
          st.success(f"Successfully ranked {len(candidates_data)} candidates!")
        except Exception as exc:
          st.error(f"Screening failed: {exc}")

  if (
      st.session_state.recruiter_df is not None
      and not st.session_state.recruiter_df.empty
  ):
    df = st.session_state.recruiter_df.head(int(top_n))
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.download_button(
        "⬇️ Download CSV",
        df.to_csv(index=False).encode("utf-8"),
        file_name="shortlist.csv",
        mime="text/csv",
        use_container_width=True,
    )

# ============================================================
# FOOTER
# ============================================================
st.divider()
st.markdown(
    """
    <div class="footer">
        <b>🎯 CareerLens AI</b><br>
        Connected to Render Backend (Python/FastAPI)
    </div>
    """,
    unsafe_allow_html=True,
)
