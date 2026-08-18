
import streamlit as st
import pandas as pd
from engine.resume_engine import analyze_resume, extract_text
from engine.matching_engine import match_profile_to_job
from engine.fraud_engine import analyze_job_risk
from engine.recruitment_engine import rank_candidates
from engine.skill_engine import skill_gap

st.set_page_config(
    page_title="CareerLens AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
:root {
    --bg:#07111f; --panel:#0c192b; --panel2:#101f34;
    --border:#203754; --text:#f4f7fb; --muted:#8fa2ba;
    --purple:#8b7cff; --cyan:#38bdf8; --green:#4ade80;
}
.stApp {background:var(--bg);}
.block-container {max-width:1450px;padding:28px 34px 60px;}
[data-testid="stSidebar"] {background:#081526;border-right:1px solid #1b304b;}
[data-testid="stMetric"] {background:var(--panel);border:1px solid var(--border);
border-radius:16px;padding:18px 20px;}
[data-testid="stMetricValue"] {color:var(--text)!important;}
[data-testid="stMetricLabel"] {color:var(--muted)!important;}
h1,h2,h3 {color:var(--text)!important;}
p, label, .stMarkdown {color:#b8c6d8;}
.brand {font-size:29px;font-weight:850;color:white;letter-spacing:-.7px;}
.brand span {color:var(--purple);}
.brand-sub {font-size:10px;letter-spacing:2px;color:#70849e;margin-top:3px;}
.hero {background:linear-gradient(135deg,#0d1d34,#0b1728);
border:1px solid #28425f;border-radius:24px;padding:40px 42px;margin-bottom:28px;}
.kicker {color:var(--cyan);font-size:12px;font-weight:800;letter-spacing:2.4px;}
.hero h1 {font-size:48px;line-height:1.08;margin:12px 0 10px;}
.hero h1 span {color:var(--purple);}
.hero p {max-width:820px;font-size:16px;line-height:1.75;color:#a8b9cd;}
.card {background:var(--panel);border:1px solid var(--border);border-radius:17px;
padding:22px;min-height:145px;}
.card-icon {font-size:27px}.card-title{color:white;font-weight:750;font-size:17px;margin-top:8px}
.card-text{color:#8fa2ba;font-size:13px;line-height:1.55;margin-top:6px}
.status {display:inline-block;background:#0b2b20;color:var(--green);border:1px solid #1e6548;
border-radius:999px;padding:6px 11px;font-size:11px;font-weight:800;letter-spacing:1px;}
.small {color:#7f93ab;font-size:13px;}
div[data-baseweb="tab-list"] {gap:8px;}
button[kind="tab"] {border-radius:10px;}
</style>
""", unsafe_allow_html=True)

if "resume_text" not in st.session_state: st.session_state.resume_text = ""
if "resume_analysis" not in st.session_state: st.session_state.resume_analysis = None
if "applications" not in st.session_state: st.session_state.applications = 0

with st.sidebar:
    st.markdown('<div class="brand">Career<span>Lens</span> AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-sub">CAREER INTELLIGENCE PLATFORM</div>', unsafe_allow_html=True)
    st.divider()
    workspace = st.radio("WORKSPACE", ["👨‍💻 Job Seeker", "🏢 Recruiter"])
    st.divider()
    st.markdown('<span class="status">● AI ENGINE ONLINE</span>', unsafe_allow_html=True)
    st.caption("NLP • ML • Recruitment Intelligence")
    st.divider()
    st.caption("CareerLens AI v2.0")
    st.caption("AI-assisted decisions. Human review recommended.")

def metric_row(values):
    cols = st.columns(len(values))
    for col, (label, value, helptext) in zip(cols, values):
        with col:
            st.metric(label, value, help=helptext)

if workspace == "👨‍💻 Job Seeker":
    st.markdown("""
    <section class="hero">
      <div class="kicker">AI CAREER INTELLIGENCE</div>
      <h1>Understand Your Career.<br><span>Build Your Future.</span></h1>
      <p>CareerLens AI combines resume intelligence, semantic job matching,
      skill-gap analysis, job-risk screening and career planning in one
      professional workspace.</p>
    </section>
    """, unsafe_allow_html=True)

    a = st.session_state.resume_analysis
    score = a["resume_score"] if a else "—"
    readiness = a["readiness"] if a else "—"
    skills = len(a["skills"]) if a else 0
    metric_row([
        ("Resume Score", f"{score}/100" if score != "—" else "—", "AI-assisted resume quality score"),
        ("Career Readiness", f"{readiness}%" if readiness != "—" else "—", "Profile readiness estimate"),
        ("Skills Detected", skills, "Skills extracted from the current resume"),
        ("Applications", st.session_state.applications, "Tracked applications"),
    ])

    st.divider()
    tabs = st.tabs(["📄 Resume Intelligence","🎯 Job Match","🛡️ Fraud Risk","🧩 Skill Gap","🗺️ Career Roadmap"])

    with tabs[0]:
        st.subheader("Resume Intelligence")
        st.write("Upload a PDF, DOCX or TXT resume. The engine extracts profile data and scores the document.")
        f = st.file_uploader("Resume", type=["pdf","docx","txt"], key="resume")
        if f:
            text = extract_text(f)
            if not text.strip():
                st.error("No readable text was found in this file.")
            else:
                result = analyze_resume(text)
                st.session_state.resume_text = text
                st.session_state.resume_analysis = result
                metric_row([
                    ("Resume Score", f"{result['resume_score']}/100", "Composite resume quality score"),
                    ("Readiness", f"{result['readiness']}%", "Career readiness estimate"),
                    ("Skills", len(result["skills"]), "Detected skills"),
                ])
                st.subheader("Profile")
                c1,c2 = st.columns(2)
                with c1:
                    st.write("**Name:**", result["name"])
                    st.write("**Email:**", result["email"])
                with c2:
                    st.write("**Phone:**", result["phone"])
                    st.write("**Experience signals:**", result["experience"])
                st.subheader("Detected Skills")
                st.write(", ".join(result["skills"]) if result["skills"] else "No known skills detected.")

    with tabs[1]:
        st.subheader("Semantic Job Matching")
        job = st.text_area("Paste job description", height=240, key="jobmatch")
        if st.button("Analyze Match", type="primary", use_container_width=True):
            if not st.session_state.resume_text:
                st.warning("Upload your resume first.")
            elif not job.strip():
                st.warning("Enter a job description.")
            else:
                m = match_profile_to_job(st.session_state.resume_text, job)
                metric_row([
                    ("Overall Match", f"{m['overall']}%", "Weighted semantic + skill match"),
                    ("Semantic Similarity", f"{m['semantic']}%", "TF-IDF NLP similarity"),
                    ("Skill Match", f"{m['skill_match']}%", "Required skills found in profile"),
                ])
                if m["missing"]:
                    st.warning("Skill gaps: " + ", ".join(m["missing"]))
                else:
                    st.success("No major known skill gaps detected.")
                st.progress(m["overall"]/100)

    with tabs[2]:
        st.subheader("Job Fraud Risk Intelligence")
        jobrisk = st.text_area("Paste job advertisement", height=240, key="risk")
        if st.button("Run Risk Analysis", use_container_width=True):
            if not jobrisk.strip():
                st.warning("Enter a job advertisement.")
            else:
                r = analyze_job_risk(jobrisk)
                metric_row([
                    ("Risk Score", f"{r['score']}/100", "Rule-based risk indicator"),
                    ("Risk Level", r["level"], "Low/medium/high screening result"),
                    ("Signals", len(r["signals"]), "Suspicious patterns detected"),
                ])
                if r["level"] == "HIGH RISK": st.error("High-risk signals detected. Review carefully.")
                elif r["level"] == "MEDIUM RISK": st.warning("Moderate-risk signals detected.")
                else: st.success("No significant predefined risk signals detected.")
                for category, hits in r["details"].items():
                    st.write(f"**{category}:** " + ", ".join(hits))
                st.caption("Fraud screening is an assistive signal, not proof of fraud.")

    with tabs[3]:
        st.subheader("Skill Gap Analysis")
        target = st.text_area("Target job description", height=220, key="gap")
        if st.button("Analyze Skill Gap", use_container_width=True):
            if not st.session_state.resume_text:
                st.warning("Upload your resume first.")
            elif not target.strip():
                st.warning("Enter a target job description.")
            else:
                g = skill_gap(st.session_state.resume_text, target)
                metric_row([
                    ("Current Skills", len(g["current"]), "Detected profile skills"),
                    ("Required Skills", len(g["required"]), "Detected target skills"),
                    ("Missing Skills", len(g["missing"]), "Skills to prioritize"),
                ])
                if g["missing"]:
                    st.warning(", ".join(g["missing"]))
                else:
                    st.success("Your known skills cover the detected requirements.")

    with tabs[4]:
        st.subheader("Personalized Career Roadmap")
        role = st.text_input("Target role", "Machine Learning Engineer")
        if st.button("Generate Roadmap", type="primary", use_container_width=True):
            if not st.session_state.resume_text:
                st.warning("Upload your resume first.")
            else:
                current = set(analyze_resume(st.session_state.resume_text)["skills"])
                steps = [
                    "Strengthen the core skills required by your target role.",
                    "Build 2–3 portfolio projects demonstrating measurable outcomes.",
                    "Improve your resume using quantified achievements and relevant keywords.",
                    "Prepare technical, behavioral and project-based interview questions.",
                    "Apply selectively and track outcomes through the CareerLens workflow."
                ]
                st.info(f"Target role: {role}")
                for i, step in enumerate(steps, 1):
                    st.write(f"**{i}.** {step}")

    st.divider()
    st.subheader("Career Intelligence")
    features = [
        ("📄","Resume Intelligence","Extract and score professional profile information."),
        ("🎯","AI Job Matching","Combine NLP similarity with skill alignment."),
        ("🛡️","Job Fraud Detection","Identify suspicious payment, urgency and communication signals."),
        ("🧩","Skill Gap Analysis","Compare current and target capabilities."),
        ("🔎","Job Intelligence","Parse requirements and important skills."),
        ("🗺️","Career Roadmap","Turn gaps into an actionable development plan."),
    ]
    cols = st.columns(3)
    for i,(icon,title,desc) in enumerate(features):
        with cols[i%3]:
            st.markdown(f'<div class="card"><div class="card-icon">{icon}</div><div class="card-title">{title}</div><div class="card-text">{desc}</div></div>', unsafe_allow_html=True)

else:
    st.markdown("""
    <section class="hero">
      <div class="kicker">RECRUITMENT INTELLIGENCE</div>
      <h1>Screen Smarter.<br><span>Hire with Evidence.</span></h1>
      <p>Upload a candidate batch, define the role, and let CareerLens AI
      rank candidates using semantic similarity, skill alignment and resume quality.</p>
    </section>
    """, unsafe_allow_html=True)

    job = st.text_area("Job Description", height=220, key="recruiter_job")
    files = st.file_uploader("Candidate Resumes — bulk upload", type=["pdf","docx","txt"], accept_multiple_files=True)
    top_n = st.number_input("Recruiter Shortlist Size", 1, 500, 20, 1)
    st.caption("The recruiter controls the final Top-N shortlist.")

    if st.button("🚀 Screen & Rank Candidates", type="primary", use_container_width=True):
        if not job.strip():
            st.warning("Enter the job description.")
        elif not files:
            st.warning("Upload candidate resumes.")
        else:
            with st.spinner("AI engine is analyzing candidates..."):
                candidates = []
                for f in files:
                    text = extract_text(f)
                    if text.strip():
                        candidates.append({"filename":f.name, "text":text})
            if candidates:
                df = rank_candidates(candidates, job)
                st.session_state["recruiter_df"] = df
                st.success(f"Analyzed {len(df)} candidates.")
            else:
                st.error("No readable resumes were found.")

    if "recruiter_df" in st.session_state:
        df = st.session_state["recruiter_df"]
        shortlist = df.head(int(top_n)).copy()
        metric_row([
            ("Resumes Screened", len(df), "Candidates successfully analyzed"),
            ("Shortlisted", len(shortlist), "Recruiter-selected Top-N"),
            ("Best Match", f"{int(df.iloc[0]['Overall Match'])}%", "Highest ranked candidate"),
        ])
        st.subheader(f"🏆 Top {len(shortlist)} Candidates")
        st.dataframe(shortlist, use_container_width=True, hide_index=True)
        st.download_button(
            "⬇️ Download Shortlist CSV",
            shortlist.to_csv(index=False).encode("utf-8"),
            "careerLens_shortlist.csv",
            "text/csv",
            use_container_width=True,
        )
        if len(shortlist):
            selected = st.selectbox("Candidate Intelligence", shortlist["Candidate"].tolist())
            row = shortlist[shortlist["Candidate"] == selected].iloc[0]
            c1,c2 = st.columns(2)
            with c1:
                st.metric("Overall Match", f"{int(row['Overall Match'])}%")
                st.write("**Candidate:**", row["Candidate"])
                st.write("**Email:**", row["Email"])
            with c2:
                st.metric("Skill Match", f"{int(row['Skill Match'])}%")
                st.write("**Resume Score:**", f"{int(row['Resume Score'])}/100")
                st.write("**Missing Skills:**", row["Missing Skills"] or "None detected")

st.divider()
st.caption("🎯 CareerLens AI • AI-Powered Career Intelligence & Recruitment Platform • AI • ML • NLP")
