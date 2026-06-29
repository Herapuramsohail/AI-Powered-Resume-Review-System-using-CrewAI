# 🚀 AI Resume Review & ATS Optimization Agent

A production-ready **Multi-Agent AI Resume Review System** built with **CrewAI**, **Google Gemini API**, **ChromaDB (RAG)**, and **Streamlit**.

The application analyzes resumes against a target job description, evaluates ATS compatibility, identifies skill gaps, calculates semantic job matching, rewrites resume content using the STAR method, and generates a professional downloadable PDF report.

---

## 🌐 Live Demo

👉 **Try the Application Here**

**https://ai-powered-resume-review-system-using-crewai-gbphhdab6nh5y3rxy.streamlit.app/**

---

# 📌 Features

✅ Resume Parsing (PDF, DOCX & TXT)

✅ ATS Compliance Analysis

✅ Skills Gap Analysis

✅ Semantic Job Match Score

✅ STAR Method Resume Improvement

✅ AI Resume Suggestions

✅ Downloadable PDF Report

✅ Retrieval-Augmented Generation (RAG)

✅ Multi-Agent Collaboration using CrewAI

---

# 🏗️ System Architecture

```
                    Resume
                       │
                       ▼
        Resume Parsing Agent
                       │
                       ▼
         ATS Evaluation Agent
                       │
                       ▼
       Skills Gap Analysis Agent
                       │
                       ▼
          Job Match Agent
                       │
                       ▼
      STAR Rewrite Agent
                       │
                       ▼
         Final Review Agent
                       │
                       ▼
     Professional PDF Report
```

---

# 🤖 AI Agents

### 1️⃣ Resume Parsing Agent

- Parses PDF, DOCX and TXT resumes.
- Extracts structured resume information.
- Converts resume into a standardized JSON format.

---

### 2️⃣ ATS Evaluation Agent

- Evaluates ATS compatibility.
- Detects formatting issues.
- Provides ATS Score.
- Suggests improvements using a RAG knowledge base.

---

### 3️⃣ Skills Gap Analysis Agent

- Compares resume skills with Job Description.
- Finds missing technical and soft skills.
- Suggests learning resources and certifications.

---

### 4️⃣ Job Match Agent

- Computes semantic similarity between Resume and Job Description.
- Generates Job Match Percentage.
- Highlights matching and missing requirements.

---

### 5️⃣ Content Improvement Agent

- Improves weak resume bullet points.
- Converts them into STAR format.
- Uses action verbs and quantified achievements.

---

### 6️⃣ Final Review Agent

- Aggregates all agent outputs.
- Computes Hiring Readiness Score.
- Generates a professional PDF report.

---

# 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| AI Framework | CrewAI |
| LLM | Google Gemini API |
| Frontend | Streamlit |
| Vector Database | ChromaDB |
| Embeddings | Sentence Transformers |
| PDF Parsing | pdfplumber, PyPDF2 |
| DOCX Parsing | python-docx |
| Data Models | Pydantic |
| PDF Reports | FPDF2 |

---

# 📂 Project Structure

```
resume-review-agent/
│
├── agents/
│   ├── parser_agent.py
│   ├── ats_agent.py
│   ├── skills_agent.py
│   ├── job_match_agent.py
│   └── review_agent.py
│
├── tasks/
│   ├── parsing_tasks.py
│   ├── ats_tasks.py
│   ├── skills_tasks.py
│   └── review_tasks.py
│
├── tools/
│   ├── pdf_parser.py
│   ├── docx_parser.py
│   ├── rag_tool.py
│   ├── models.py
│   └── pdf_generator.py
│
├── knowledge_base/
│   ├── ats_standards.md
│   ├── resumes_best_practices.md
│   └── industry_skills.md
│
├── crew.py
├── app.py
├── main.py
├── setup_kb.py
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git

cd YOUR_REPOSITORY
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file.

```env
GEMINI_API_KEY=your_gemini_api_key
```

---

# 📚 Build the Knowledge Base

The ATS and Skills Gap agents use a Retrieval-Augmented Generation (RAG) pipeline backed by ChromaDB.

Initialize the vector database:

```bash
python setup_kb.py
```

This indexes the documents inside the `knowledge_base/` directory.

---

# ▶️ Run the Application

Start the Streamlit app:

```bash
streamlit run app.py
```

Open:

```
http://localhost:8501
```

---

# 💻 Command Line Usage

```bash
python main.py --resume sample_resume.pdf --jd sample_jd.txt
```

Optional arguments:

```
--resume

--jd

--output

--model
```

---

# 📊 Workflow

```
Upload Resume
        │
        ▼
Upload Job Description
        │
        ▼
Resume Parsing
        │
        ▼
ATS Evaluation
        │
        ▼
Skills Gap Analysis
        │
        ▼
Job Match Score
        │
        ▼
STAR Rewrite
        │
        ▼
Final AI Review
        │
        ▼
Download PDF Report
```

---

# 🎯 Key Highlights

- Multi-Agent AI System
- Resume Parsing
- ATS Score Calculation
- Resume vs JD Matching
- Skills Gap Detection
- STAR Bullet Rewriting
- RAG using ChromaDB
- Professional PDF Report Generation
- Streamlit Web Dashboard
- Powered by Google Gemini API

---

# 🚀 Future Enhancements

- Authentication & User Accounts
- Resume History Dashboard
- Multiple Resume Comparison
- Support for Multiple LLMs (Gemini, OpenAI, Claude)
- Cloud Database Integration
- Resume Version Tracking
- Interview Question Generator
- Cover Letter Generator
- AI Career Recommendations

---

# 📸 Screenshots

> Add screenshots here after uploading them.

Example:

```
screenshots/

dashboard.png

ats_score.png

skills_gap.png

pdf_report.png
```

---

# 🤝 Contributing

Contributions are welcome!

Feel free to fork the repository, improve features, and submit a pull request.

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Mohammad Sohail**

GitHub: https://github.com/YOUR_GITHUB_USERNAME

LinkedIn: https://www.linkedin.com/in/YOUR_LINKEDIN/

---

⭐ If you found this project useful, don't forget to **Star** this repository!
