🤖 AI Resume Intelligence Platform – Multi-Resume Batch Analyzer

An AI-powered resume screening system that analyzes multiple resumes in batch, extracts key candidate information, ranks candidates automatically, and provides quick interviewer insights — all without requiring paid APIs.

This project focuses on local analysis using NLP techniques, regex, and keyword matching, making it fast, lightweight, and cost-free.

🚀 Features

📂 Upload multiple resume PDFs

🧠 Automatically extract:

Name, Email, Phone

Experience & Experience Level

Specialization / Role

Technologies & Skills

Projects count

CGPA (if available)

Education

📊 Intelligent scoring & ranking (0–100)

🏆 Candidates sorted by overall score

📋 Quick interviewer summary for each candidate

📤 Export results as JSON

⚡ Runs fully offline (no API required)

🖥️ Tech Stack

Python

Streamlit

PyPDF2

Regex (re)

📁 Project Structure
AI-Resume-Intelligence-System/
│
├── app.py
├── requirements.txt
└── README.md

⚙️ Installation
1️⃣ Clone Repository
git clone https://github.com/C-venu01/AI-Resume-Intelligence-System.git
cd AI-Resume-Intelligence-System

2️⃣ Create Virtual Environment (Optional)
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate    # Mac/Linux

3️⃣ Install Dependencies
pip install -r requirements.txt

▶️ Run Application
streamlit run app.py


Open browser at:

http://localhost:8501

📌 How It Works

Upload multiple resume PDFs

System extracts text from each PDF

Local analyzer detects skills, experience, CGPA, and projects

Each resume receives a score (0–100)

Candidates are ranked automatically

Expand any candidate to view full insights

📊 Scoring Logic (Simplified)
Factor	Points
Base Score	50
Each Technology	+3
Experience (per year)	+5
Each Achievement	+5
Each Project	+2
CGPA > 7	+10
Max Score	100
🧠 Example Output

Candidate Name

ML/AI Engineer

4 Years Experience

Skills: Python, ML, TensorFlow, SQL

Projects: 5

CGPA: 8.2

Overall Score: 86/100

🎯 Use Cases

College placement screening

Internship shortlisting

HR recruitment automation

Hackathon & competition evaluations

🔐 No Paid APIs Required

The system uses local rule-based analysis, so:

✔ No OpenAI key needed
✔ No usage limits
✔ No billing

(Optional OpenAI key field exists only for future expansion.)

📈 Future Enhancements

Skill gap recommendations

Role-based filtering

CSV / Excel export

Dashboard analytics

Resume similarity detection

Database storage

👨‍💻 Author

Venu Chillale
GitHub: https://github.com/C-venu01
