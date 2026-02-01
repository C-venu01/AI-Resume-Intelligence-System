🤖 AI Resume Intelligence Platform – Multi-Resume Batch Analyzer

An AI-powered resume screening system that analyzes multiple resumes, extracts key candidate information, ranks candidates automatically, and provides quick interviewer insights.

Built using local NLP, regex, and keyword matching, making it fast, lightweight, and completely free from paid APIs.

🚀 Features

Upload multiple resume PDFs

Automatic extraction of:

Name, Email, Phone

Experience & Experience Level

Specialization / Role

Skills & Technologies

Projects Count

CGPA (if available)

Education

Intelligent scoring (0–100)

Automatic ranking of candidates

Quick interviewer summary

Export results as JSON

Works fully offline

🖥 Tech Stack

Python

Streamlit

PyPDF2

Regex

📁 Project Structure
AI-Resume-Intelligence-System/
│
├── app.py
├── requirements.txt
└── README.md

⚙️ Installation & Run
git clone https://github.com/C-venu01/AI-Resume-Intelligence-System.git
cd AI-Resume-Intelligence-System
pip install -r requirements.txt
streamlit run app.py


Open in browser:

http://localhost:8501

📌 How It Works

Upload multiple resumes

Text is extracted from PDFs

Local analyzer detects skills, experience, CGPA, and projects

Each resume gets a score (0–100)

Candidates are ranked automatically

📊 Scoring Logic
Factor	Points
Base Score	50
Each Technology	+3
Experience (per year)	+5
Each Achievement	+5
Each Project	+2
CGPA > 7	+10
Max Score	100
🎯 Use Cases

College placement screening

Internship shortlisting

HR recruitment automation

🔐 No Paid APIs

✔ No OpenAI key required
✔ No billing
✔ No usage limits

👨‍💻 Author

Venu Chillale
GitHub: https://github.com/C-venu01
