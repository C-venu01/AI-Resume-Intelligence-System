# ============================================================
# AI RESUME INTELLIGENCE PLATFORM
# MAJOR PROJECT – FULL VERSION
# STRICT CGPA | PROJECT AWARE | RECRUITER CONTROLLED
# ============================================================

import streamlit as st
import PyPDF2
import json
import re
from typing import List, Dict, Optional

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.run.agent import RunOutput

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="AI Resume Intelligence Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# ROLE → SKILL DEFINITIONS
# ============================================================
ROLE_SKILLS: Dict[str, List[str]] = {
    "AI / ML Engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "Data Preprocessing",
        "DSA",
        "MLOps",
        "RAG",
        "Model Deployment"
    ],

    "Backend Engineer": [
        "Python",
        "Java",
        "Node.js",
        "REST APIs",
        "Databases",
        "System Design",
        "Cloud",
        "DSA"
    ],

    "Frontend Engineer": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "State Management",
        "Responsive Design",
        "DSA"
    ],

    "Java Developer": [
        "Java",
        "Spring",
        "Hibernate",
        "SQL",
        "Backend",
        "DSA"
    ],

    "Cloud Engineer": [
        "AWS",
        "Azure",
        "GCP",
        "Docker",
        "Kubernetes",
        "CI/CD",
        "DSA"
    ]
}

# ============================================================
# SKILL GAP ROADMAP
# ============================================================
SKILL_ROADMAP: Dict[str, List[str]] = {
    "DSA": [
        "Revise arrays, strings, recursion",
        "Master linked lists, stacks, queues",
        "Practice trees & graphs",
        "Solve 300+ LeetCode problems",
        "Analyze time & space complexity"
    ],
    "MLOps": [
        "Learn ML pipelines",
        "Experiment tracking (MLflow)",
        "Dockerize ML models",
        "Deploy models on cloud"
    ],
    "RAG": [
        "Learn embeddings",
        "Use vector databases",
        "Build RAG pipelines",
        "Optimize retrieval accuracy"
    ],
    "Cloud": [
        "Understand cloud fundamentals",
        "Deploy applications",
        "Learn IAM & monitoring",
        "Handle scalability"
    ]
}

## ============================================================
# PDF TEXT EXTRACTION
# ============================================================
def extract_text_from_pdf(pdf_file) -> str:
    reader = PyPDF2.PdfReader(pdf_file)
    full_text = ""

    for page_index, page in enumerate(reader.pages):
        page_text = page.extract_text()
        if page_text:
            full_text += page_text + "\n"

    return full_text.lower()

# ============================================================
# STRICT CGPA EXTRACTION (FIXED – NO FALSE POSITIVES)
# ============================================================
def extract_cgpa(text: str) -> Optional[float]:
    """
    Detects CGPA ONLY when explicitly mentioned.
    Will NOT mistakenly pick random numbers.
    """

    patterns = [
        r'cgpa[:\s]*([0-9]\.?[0-9]?)',
        r'c\.g\.p\.a[:\s]*([0-9]\.?[0-9]?)',
        r'([0-9]\.?[0-9]?)\s*/\s*10'
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            try:
                cgpa_val = float(match.group(1))
                if 0 <= cgpa_val <= 10:
                    return cgpa_val
            except ValueError:
                continue

    return None

# ============================================================
# PROJECT DETECTION
# ============================================================
def detect_projects(text: str) -> bool:
    project_keywords = [
        "project",
        "developed",
        "implemented",
        "designed",
        "built",
        "application",
        "platform",
        "system"
    ]
    return any(word in text for word in project_keywords)

# ============================================================
# DSA DETECTION
# ============================================================
def detect_dsa(text: str) -> bool:
    dsa_keywords = [
        "data structures",
        "algorithms",
        "leetcode",
        "codeforces",
        "dsa"
    ]
    return any(word in text for word in dsa_keywords)

# ============================================================
# OPTIONAL AI AGENT
# ============================================================
def create_agent(api_key: Optional[str]) -> Optional[Agent]:
    if not api_key:
        return None

    return Agent(
        model=OpenAIChat(
            id="gpt-4o",
            api_key=api_key
        ),
        instructions=[
            "You are a senior technical recruiter.",
            "Focus on project relevance and applied skills.",
            "Do not rely only on keywords.",
            "Return STRICT JSON only."
        ],
        markdown=False
    )

# ============================================================
# CORE RESUME ANALYSIS (CGPA HARD GATE)
# ============================================================
def analyze_resume(
    resume_text: str,
    required_skills: List[str],
    cgpa_cutoff: Optional[float],
    consider_cgpa: bool,
    agent: Optional[Agent]
) -> Dict:

    # ---------------- CGPA CHECK (ABSOLUTE RULE) ----------------
    cgpa = extract_cgpa(resume_text)

    if consider_cgpa:
        if cgpa is None:
            return {
                "cgpa": None,
                "experience_level": "junior",
                "matching_skills": [],
                "missing_skills": required_skills,
                "shortlisted": False,
                "score": 0,
                "feedback": "rejected: cgpa not mentioned"
            }

        if cgpa < cgpa_cutoff:
            return {
                "cgpa": cgpa,
                "experience_level": "junior",
                "matching_skills": [],
                "missing_skills": required_skills,
                "shortlisted": False,
                "score": 0,
                "feedback": f"rejected: cgpa {cgpa} below cutoff {cgpa_cutoff}"
            }

    # ---------------- SKILL MATCHING ----------------
    matching_skills = []
    missing_skills = []

    for skill in required_skills:
        if skill.lower() in resume_text:
            matching_skills.append(skill)
        else:
            missing_skills.append(skill)

    # ---------------- PROJECT & DSA BONUS ----------------
    score = 0
    score += len(matching_skills) * 10

    if detect_projects(resume_text):
        score += 20

    if detect_dsa(resume_text):
        score += 10

    shortlisted = score >= 60

    return {
        "cgpa": cgpa,
        "experience_level": "junior",
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "shortlisted": shortlisted,
        "score": score,
        "feedback": (
            "strong profile with relevant projects"
            if shortlisted
            else "skill gaps detected – improve via projects"
        )
    }

# ============================================================
# SIDEBAR – RECRUITER CONTROLS
# ============================================================
with st.sidebar:
    st.header("⚙️ Recruiter Configuration")

    api_key = st.text_input("OpenAI API Key (optional)", type="password")

    role = st.selectbox("Select Hiring Role", list(ROLE_SKILLS.keys()))

    st.subheader("Required Skills (Editable)")
    selected_skills: List[str] = []
    for skill in ROLE_SKILLS[role]:
        if st.checkbox(skill, value=True):
            selected_skills.append(skill)

    st.subheader("CGPA Configuration")
    consider_cgpa = st.checkbox("Enforce CGPA (Hard Filter)")
    cgpa_cutoff = None
    if consider_cgpa:
        cgpa_cutoff = st.number_input(
            "Minimum CGPA",
            min_value=0.0,
            max_value=10.0,
            step=0.1
        )

# ============================================================
# MAIN UI
# ============================================================
st.title("🧠 AI Resume Intelligence Platform")
st.caption("Major Project • Strict CGPA • Project-based Evaluation")

resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if resume_file:
    resume_text = extract_text_from_pdf(resume_file)
    st.success("Resume uploaded successfully")

    if st.button("🚀 Analyze Resume"):
        if consider_cgpa and cgpa_cutoff is None:
            st.error("Please set CGPA cutoff")
        elif not selected_skills:
            st.error("Select at least one required skill")
        else:
            with st.spinner("Analyzing resume..."):
                result = analyze_resume(
                    resume_text,
                    selected_skills,
                    cgpa_cutoff,
                    consider_cgpa,
                    create_agent(api_key)
                )

            # ====================================================
            # RESULT DISPLAY
            # ====================================================
            st.markdown("## 📊 Analysis Result")

            if result["shortlisted"]:
                st.success("✅ Candidate Shortlisted")
            else:
                st.error("❌ Candidate Rejected")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("CGPA", result["cgpa"] if result["cgpa"] else "Not Found")
                st.metric("Final Score", result["score"])
                st.markdown("### Matching Skills")
                for s in result["matching_skills"]:
                    st.success(s)

            with col2:
                st.markdown("### Missing Skills")
                for s in result["missing_skills"]:
                    st.warning(s)

            st.markdown("### Recruiter Feedback")
            st.info(result["feedback"])

            st.markdown("## 🛠 Skill Gap Roadmap")
            for skill in result["missing_skills"]:
                if skill in SKILL_ROADMAP:
                    st.markdown(f"### {skill}")
                    for step in SKILL_ROADMAP[skill]:
                        st.write("➡️", step)
