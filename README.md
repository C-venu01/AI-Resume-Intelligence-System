🤖 AI Resume Intelligence Platform – Multi-Resume Batch Analyzer

An intelligent, end-to-end AI-powered resume screening platform that performs batch analysis of resumes, extracts structured candidate information, ranks applicants automatically, and provides quick interviewer-ready insights.

This system uses local NLP processing, regex-based information extraction, and heuristic scoring to deliver fast, accurate, and cost-free resume intelligence without requiring any paid APIs.

📌 Problem Statement

Recruiters and placement coordinators manually screen hundreds of resumes, which is:

Time-consuming

Error-prone

Inconsistent

There is a need for a lightweight automated system that can:

✔ Analyze resumes in bulk
✔ Extract key candidate attributes
✔ Rank candidates objectively
✔ Provide quick summaries for interviewers

🎯 Solution

The AI Resume Intelligence Platform automates resume screening by:

Accepting multiple resume PDFs

Extracting raw text

Performing local NLP-based parsing

Computing a weighted score

Ranking candidates instantly

The platform provides structured, transparent, and explainable results suitable for real-world hiring and campus recruitment.

🚀 Key Features

📂 Upload multiple resume PDFs

🧠 Automatic extraction of:

Name

Email

Phone number

Experience years

Experience level

Specialization / role

Technologies & skills

Projects count

CGPA (if present)

Education

📊 Intelligent scoring (0–100)

🏆 Automatic candidate ranking

📋 Interviewer-ready summaries

📤 Export results as JSON

⚡ Fully offline execution (no paid APIs)

🖥️ Tech Stack
Layer	Technology
Language	Python
Frontend	Streamlit
PDF Parsing	PyPDF2
NLP	Regex + Keyword Matching
Data Format	JSON
🏗️ System Architecture
User Uploads PDFs
        |
        v
PDF Text Extraction (PyPDF2)
        |
        v
Local NLP Processing
(Regex + Keyword Matching)
        |
        v
Feature Extraction
(Name, Skills, Experience, CGPA...)
        |
        v
Scoring Engine
        |
        v
Candidate Ranking
        |
        v
Streamlit Dashboard

🔁 Workflow

User uploads multiple resume PDFs

Text is extracted from each PDF

Resume analyzer extracts fields

Scoring engine assigns score

Candidates sorted by score

Results displayed and exportable

📁 Project Structure
AI-Resume-Intelligence-System/
│
├── app.py              # Main application
├── requirements.txt   # Dependencies
└── README.md

⚙️ Installation & Setup
1️⃣ Clone Repository
git clone https://github.com/C-venu01/AI-Resume-Intelligence-System.git
cd AI-Resume-Intelligence-System

2️⃣ Create Virtual Environment (Optional)
python -m venv venv
venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run Application
streamlit run app.py


Open in browser:

http://localhost:8501

📊 Scoring Methodology
Component	Points
Base Score	50
Each detected technology	+3
Each year of experience	+5
Each achievement	+5
Each project	+2
CGPA > 7	+10
Maximum	100
🧠 Example Candidate Output
Name: Rahul Kumar
Specialization: ML/AI Engineer
Experience: 4 Years
Skills: Python, TensorFlow, SQL
Projects: 5
CGPA: 8.2
Overall Score: 86/100

🎯 Use Cases

Campus placement screening

Internship filtering

HR shortlisting

Hackathons & competitions

Resume quality auditing

🧪 Testing

Tested with resumes in:

PDF text format

Multi-page resumes

Freshers & experienced profiles

⚠️ Limitations

Image-based scanned PDFs not supported

Rule-based skill detection (not semantic)

No database storage (in-memory only)

📈 Future Enhancements

Semantic NLP using embeddings

Role-based scoring profiles

Skill-gap roadmap generation

Resume similarity detection

CSV / Excel export

Database integration

Admin dashboard

🧾 Resume Description (For Your CV)

Built an AI-powered batch resume analysis platform using Python and Streamlit that extracts candidate data, scores resumes, ranks applicants, and generates interviewer-ready insights. Implemented NLP-based parsing, regex extraction, and heuristic scoring achieving automated resume screening without paid APIs.

👨‍💻 Author

Venu Chillale
GitHub: https://github.com/C-venu01
