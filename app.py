"""
AI Resume Intelligence Platform - Multi-Resume Batch Analysis
Analyzes multiple resumes, ranks candidates, and provides quick interviewer insights
Generic analysis - not tied to specific roles
CLEAN VERSION - All functions properly defined
"""

from typing import Dict, Optional, List
import PyPDF2
import streamlit as st
import json
from datetime import datetime
import time
import re

# ==================== CONFIGURATION ====================

ANALYSIS_PROMPT = """Analyze this resume and extract key information. Return ONLY a JSON object with no markdown, no backticks, no extra text.

{resume_text}

Return JSON (nothing else):
{{"candidate_name": "name", "email": "email", "phone": "phone", "experience_years": 0, "experience_level": "Fresher|Junior|Mid-level|Senior|Lead", "specialization": "role", "key_strength": "strength", "technologies": ["tech1", "tech2"], "notable_achievements": ["achievement1", "achievement2"], "projects_count": 0, "education": "degree", "cgpa": null, "candidate_summary": "summary", "overall_score": 75}}"""


# ==================== PDF EXTRACTION ====================

def extract_text_from_pdf(pdf_file) -> Optional[str]:
    """Extract text from uploaded PDF file."""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            try:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            except Exception:
                continue
        
        text = text.strip()
        return text if len(text) >= 50 else None
    except Exception:
        return None


# ==================== LOCAL ANALYSIS ====================

def analyze_resume_locally(resume_text: str, file_name: str) -> Dict:
    """
    Local resume analysis without API calls - avoids quota issues.
    Uses keyword matching and pattern detection.
    """
    try:
        text_lower = resume_text.lower()
        
        # Extract basic info
        lines = resume_text.split('\n')
        candidate_name = lines[0].strip() if lines else "Not Found"
        
        # Extract email
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', resume_text)
        email = email_match.group() if email_match else "Not provided"
        
        # Extract phone
        phone_match = re.search(r'[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}', resume_text)
        phone = phone_match.group() if phone_match else "Not provided"
        
        # Estimate experience
        experience_years = 0
        if "10+ years" in text_lower or "10 years" in text_lower:
            experience_years = 12
        elif "5-10 years" in text_lower or "5+ years" in text_lower:
            experience_years = 7
        elif "3-5 years" in text_lower:
            experience_years = 4
        elif "1-3 years" in text_lower or "2 years" in text_lower:
            experience_years = 2
        elif "fresher" in text_lower or "0 years" in text_lower:
            experience_years = 0
        else:
            year_matches = re.findall(r'20\d{2}', resume_text)
            if len(year_matches) >= 2:
                try:
                    experience_years = int(year_matches[-1]) - int(year_matches[0])
                except ValueError:
                    pass
        
        # Determine experience level
        if "senior" in text_lower or "lead" in text_lower:
            experience_level = "Senior"
        elif "mid" in text_lower or experience_years >= 5:
            experience_level = "Mid-level"
        elif experience_years >= 3:
            experience_level = "Junior"
        else:
            experience_level = "Fresher"
        
        # Detect technologies
        tech_keywords = {
            "Python": ["python"],
            "JavaScript": ["javascript", "js"],
            "React": ["react", "reactjs"],
            "Node.js": ["node.js", "nodejs"],
            "Java": ["java"],
            "C++": ["c++"],
            "Docker": ["docker"],
            "AWS": ["aws"],
            "Machine Learning": ["machine learning", "ml", "tensorflow", "pytorch"],
            "Data Science": ["data science", "pandas", "numpy"],
            "SQL": ["sql", "mysql", "postgresql"],
            "Git": ["git", "github"],
            "Linux": ["linux", "unix"],
            "REST API": ["rest api", "restful"],
            "MongoDB": ["mongodb"],
            "DevOps": ["devops", "ci/cd"],
            "Kubernetes": ["kubernetes", "k8s"],
        }
        
        technologies = []
        for tech, keywords in tech_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    technologies.append(tech)
                    break
        
        # Extract CGPA
        cgpa = None
        cgpa_match = re.search(r'(?:cgpa|gpa|c\.gpa)\s*[:=]?\s*(\d+\.?\d*)', resume_text, re.IGNORECASE)
        if cgpa_match:
            try:
                cgpa = float(cgpa_match.group(1))
            except ValueError:
                pass
        
        # Count projects and achievements
        projects_count = text_lower.count("project")
        achievement_keywords = ["developed", "implemented", "designed", "built", "created", "led", "managed"]
        notable_achievements = []
        for line in resume_text.split('\n'):
            if any(keyword in line.lower() for keyword in achievement_keywords) and len(line) > 20:
                notable_achievements.append(line.strip())
                if len(notable_achievements) >= 3:
                    break
        
        # Detect specialization
        specialization = "General Developer"
        if "machine learning" in text_lower or "ai" in text_lower or "pytorch" in text_lower:
            specialization = "ML/AI Engineer"
        elif "react" in text_lower or "frontend" in text_lower or "vue" in text_lower:
            specialization = "Frontend Engineer"
        elif "backend" in text_lower or "node" in text_lower or "java" in text_lower:
            specialization = "Backend Engineer"
        elif "devops" in text_lower or "docker" in text_lower or "kubernetes" in text_lower:
            specialization = "DevOps Engineer"
        elif "data" in text_lower:
            specialization = "Data Engineer"
        
        # Calculate score
        score = 50  # base score
        score += len(technologies) * 3  # tech diversity
        score += min(experience_years * 5, 20)  # experience
        score += len(notable_achievements) * 5  # achievements
        score += projects_count * 2  # projects
        if cgpa and cgpa > 7:
            score += 10
        score = min(score, 100)
        
        # Generate summary
        candidate_summary = f"{candidate_name} is a {experience_level.lower()} {specialization.lower()} with {experience_years} years of experience. Skilled in {', '.join(technologies[:3]) if technologies else 'multiple technologies'}."
        
        # Extract education
        education = "Not specified"
        if "b.tech" in text_lower or "bachelor" in text_lower:
            education = "B.Tech"
        elif "b.e" in text_lower:
            education = "B.E"
        elif "m.tech" in text_lower or "master" in text_lower:
            education = "M.Tech"
        
        return {
            "candidate_name": candidate_name,
            "email": email,
            "phone": phone,
            "experience_years": experience_years,
            "experience_level": experience_level,
            "specialization": specialization,
            "key_strength": notable_achievements[0] if notable_achievements else specialization,
            "technologies": list(set(technologies)),
            "notable_achievements": notable_achievements[:3] if notable_achievements else [specialization],
            "projects_count": projects_count,
            "education": education,
            "cgpa": cgpa,
            "candidate_summary": candidate_summary,
            "overall_score": int(score),
            "filename": file_name
        }
    
    except Exception as e:
        return {
            "candidate_name": "Analysis Error",
            "email": "N/A",
            "phone": "N/A",
            "experience_years": 0,
            "experience_level": "Unknown",
            "specialization": "Unknown",
            "key_strength": "Error in analysis",
            "technologies": [],
            "notable_achievements": [],
            "projects_count": 0,
            "education": "N/A",
            "cgpa": None,
            "candidate_summary": "Could not process resume",
            "overall_score": 0,
            "filename": file_name
        }


# ==================== ANALYSIS FUNCTIONS ====================

def analyze_single_resume(resume_text: str, api_key: str, file_name: str = "", use_api: bool = False) -> Optional[Dict]:
    """Analyze a single resume using local analysis by default."""
    return analyze_resume_locally(resume_text, file_name)


# ==================== SESSION STATE ====================

def init_session_state() -> None:
    """Initialize session state."""
    defaults = {
        'api_key': "",
        'analysis_complete': False,
        'candidates': [],
        'ranked_candidates': []
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ==================== MAIN APP ====================

def main():
    """Main Streamlit app."""
    st.set_page_config(
        page_title="AI Batch Resume Analyzer",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 AI Batch Resume Analyzer")
    st.markdown("Upload multiple resumes, analyze candidates, and rank them by experience & skills")
    
    init_session_state()
    
    # ========== SIDEBAR ==========
    with st.sidebar:
        st.header("⚙️ Setup")
        api_key = st.text_input("OpenAI API Key", type="password", value=st.session_state.api_key, help="Optional")
        st.session_state.api_key = api_key
        st.markdown("---")
        st.info("💡 **How it works:**\n1. Upload PDFs\n2. AI analyzes resumes\n3. Ranked by score")
    
    # ========== MAIN CONTENT ==========
    col1, col2 = st.columns([3, 1])
    with col1:
        st.header("📤 Batch Upload Resumes")
    with col2:
        if st.button("🔄 Clear All", use_container_width=True):
            st.session_state.analysis_complete = False
            st.session_state.candidates = []
            st.session_state.ranked_candidates = []
            st.rerun()
    
    st.markdown("### Upload Multiple Resume PDFs")
    uploaded_files = st.file_uploader("Choose PDF files", type=["pdf"], accept_multiple_files=True)
    
    if uploaded_files:
        st.markdown(f"**{len(uploaded_files)} file(s) selected**")
        
        if not st.session_state.analysis_complete:
            if st.button("🚀 Analyze All Resumes", use_container_width=True, type="primary"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                candidates = []
                
                for idx, file in enumerate(uploaded_files):
                    status_text.text(f"📖 Extracting: {file.name}")
                    resume_text = extract_text_from_pdf(file)
                    
                    if not resume_text:
                        st.warning(f"⚠️ Could not extract {file.name}")
                        continue
                    
                    status_text.text(f"🧠 Analyzing: {file.name}")
                    result = analyze_single_resume(resume_text, st.session_state.api_key, file.name)
                    
                    if result:
                        result["filename"] = file.name
                        candidates.append(result)
                        st.success(f"✅ {file.name}")
                    
                    progress_bar.progress((idx + 1) / len(uploaded_files))
                    if idx < len(uploaded_files) - 1:
                        time.sleep(0.3)
                
                if candidates:
                    ranked = sorted(candidates, key=lambda x: x.get("overall_score", 0), reverse=True)
                    st.session_state.candidates = candidates
                    st.session_state.ranked_candidates = ranked
                    st.session_state.analysis_complete = True
                    status_text.text(f"✅ Analysis complete! {len(ranked)} candidate(s) ranked.")
                    progress_bar.progress(1.0)
                    st.rerun()
                else:
                    st.error("❌ Could not analyze any resumes. Please try again.")
        
        # ========== RESULTS DISPLAY ==========
        if st.session_state.analysis_complete and st.session_state.ranked_candidates:
            ranked = st.session_state.ranked_candidates
            
            st.markdown("---")
            st.markdown(f"## 📊 Results: {len(ranked)} Candidate(s) Ranked")
            
            # Summary stats
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                avg_score = sum(c.get("overall_score", 0) for c in ranked) / len(ranked)
                st.metric("📈 Avg Score", f"{avg_score:.0f}")
            with col2:
                st.metric("👥 Total Candidates", len(ranked))
            with col3:
                senior_count = sum(1 for c in ranked if "Senior" in c.get("experience_level", ""))
                st.metric("🎯 Senior+ Candidates", senior_count)
            with col4:
                avg_exp = sum(c.get("experience_years", 0) for c in ranked) / len(ranked)
                st.metric("📅 Avg Experience (yrs)", f"{avg_exp:.1f}")
            
            st.markdown("---")
            st.markdown("### 🏆 Candidates Ranked by Overall Score")
            
            for rank, candidate in enumerate(ranked, 1):
                score = candidate.get("overall_score", 0)
                if score >= 80:
                    color = "🟢"
                elif score >= 60:
                    color = "🟡"
                else:
                    color = "🔴"
                
                header = f"{color} **#{rank}** | {candidate.get('candidate_name', 'Unknown')} | Score: {score} | {candidate.get('experience_level', 'Unknown')}"
                
                with st.expander(header, expanded=(rank == 1)):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**📌 Specialization:** {candidate.get('specialization', 'Not specified')}")
                        st.markdown(f"**💼 Experience:** {candidate.get('experience_years', 0)} years")
                        st.markdown(f"**🎓 Education:** {candidate.get('education', 'Not specified')}")
                        if candidate.get('cgpa'):
                            st.markdown(f"**📊 CGPA:** {candidate.get('cgpa')}")
                        st.markdown(f"**💪 Key Strength:** {candidate.get('key_strength', 'N/A')}")
                    
                    with col2:
                        st.metric("Overall Score", f"{score}/100")
                        st.metric("Projects", candidate.get("projects_count", 0))
                    
                    st.markdown("---")
                    st.markdown("### 📋 Quick Interviewer Summary")
                    st.info(candidate.get('candidate_summary', 'No summary available'))
                    st.markdown("---")
                    
                    # Technologies
                    st.markdown("### 🛠️ Technologies & Skills")
                    techs = candidate.get("technologies", [])
                    if techs:
                        cols = st.columns(len(techs) if len(techs) <= 5 else 5)
                        for i, tech in enumerate(techs[:5]):
                            with cols[i % 5]:
                                st.write(f"• {tech}")
                        if len(techs) > 5:
                            st.write(f"+ {len(techs) - 5} more")
                    
                    st.markdown("---")
                    
                    # Achievements
                    achievements = candidate.get("notable_achievements", [])
                    if achievements:
                        st.markdown("### 🏅 Notable Achievements")
                        for achievement in achievements:
                            st.markdown(f"✅ {achievement}")
                    
                    st.markdown("---")
                    st.markdown("### 📧 Contact Information")
                    st.markdown(f"**Email:** {candidate.get('email', 'Not provided')}")
                    st.markdown(f"**Phone:** {candidate.get('phone', 'Not provided')}")
                    st.markdown(f"**From:** {candidate.get('filename', 'Unknown')}")
            
            st.markdown("---")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📥 Export Results (JSON)", use_container_width=True):
                    export = {
                        "analysis_date": datetime.now().isoformat(),
                        "total_candidates": len(ranked),
                        "candidates": ranked
                    }
                    st.download_button(
                        label="Download JSON",
                        data=json.dumps(export, indent=2),
                        file_name=f"batch_resume_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
            
            with col2:
                if st.button("🔄 Analyze More Resumes", use_container_width=True):
                    st.session_state.analysis_complete = False
                    st.session_state.candidates = []
                    st.session_state.ranked_candidates = []
                    st.rerun()


if __name__ == "__main__":
    main()
