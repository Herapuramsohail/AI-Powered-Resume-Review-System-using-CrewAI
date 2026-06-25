# AI Resume Review & ATS Optimization Agent

A production-ready, multi-agent AI system built on **CrewAI** that parses resumes (PDF/DOCX), evaluates them for ATS compliance, runs a skills gap analysis against a target job description, calculates semantic job-fit matching, optimizes writing using the STAR method, and generates a downloadable PDF report via an interactive **Streamlit** dashboard.

---

## Architecture & Specialized Agents

The system uses 6 collaborating agents, organized sequentially to review and score resumes:

1. **Resume Parsing Agent**: Parses the raw document text and structures it into standardized sections using a target JSON format.
2. **ATS Evaluation Agent**: Inspects the resume structure and formatting against standard ATS rules (RAG-supported via ChromaDB) and outputs an ATS Score, issues list, and layout adjustments.
3. **Skills Gap Analysis Agent**: Compares the candidate's skills list against the target job description requirements. Finds missing technical and soft skills, querying a database of learning resources and certifications to build an upskilling pathway.
4. **Job Match Agent**: Evaluates the semantic alignment of projects, experience, and scale against the target job description to compute a Job Description Match percentage.
5. **Content Improvement Agent**: Reviews the experience bullet points and rewrites weak, duty-focused descriptions using the STAR method (Situation/Task/Action/Result) and action verbs.
6. **Final Review Agent**: Aggregates all findings into a unified professional consultancy review report, computing the overall hiring readiness rating.

---

## Directory Structure

```
resume-review-agent/
│
├── agents/
│   ├── __init__.py
│   ├── parser_agent.py      # Resume Parser Agent
│   ├── ats_agent.py         # ATS evaluation Agent
│   ├── skills_agent.py      # Skills Gap Analysis Agent
│   ├── job_match_agent.py   # Job Match Agent
│   └── review_agent.py      # Content Improvement & Final Review Agents
│
├── tasks/
│   ├── __init__.py
│   ├── parsing_tasks.py     # Parsing Task
│   ├── ats_tasks.py         # ATS Task
│   ├── skills_tasks.py      # Skills Task
│   └── review_tasks.py      # Job Match, Bullet Rewrite, and Final Review Tasks
│
├── tools/
│   ├── __init__.py
│   ├── pdf_parser.py        # PDF extractor (pdfplumber + PyPDF2 fallback)
│   ├── docx_parser.py       # DOCX extractor (python-docx)
│   ├── rag_tool.py          # ChromaDB search tool for agents
│   └── models.py            # Pydantic schemas for task outputs
│   └── pdf_generator.py     # Custom report generator using FPDF2
│
├── knowledge_base/          # Advice documents for RAG indexing
│   ├── ats_standards.md
│   ├── resumes_best_practices.md
│   └── industry_skills.md
│
├── crew.py                  # Crew config and execution flow
├── main.py                  # CLI application entrypoint
├── app.py                   # Streamlit web dashboard
├── setup_kb.py              # Knowledge base indexing script
├── requirements.txt         # Package dependencies
├── sample_resume.txt        # Mock text resume
├── sample_jd.txt            # Mock job description
└── README.md                # This documentation
```

---

## Environment Setup Guide

### 1. Prerequisites
- **Python**: Version 3.10 to 3.12.7.
- **OpenAI API Key**: Required for GPT models (uses `gpt-4o` by default).

### 2. Installation
Clone the repository or navigate to your project folder, then install the dependencies:

```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables
Create a `.env` file in the root directory (you can copy `.env.example` as a template):

```env
OPENAI_API_KEY=your_actual_openai_api_key
OPENAI_MODEL_NAME=gpt-4o
```

### 4. Build the Local Vector Database (ChromaDB)
The Skills Gap and ATS agents use a RAG tool to query compliance rules and certifications. Build and populate the ChromaDB store by running:

```bash
python setup_kb.py
```
This script reads guidelines from `knowledge_base/`, computes embeddings using `sentence-transformers/all-MiniLM-L6-v2`, and initializes the vector store under `./chroma_db`.

### 5. Generate Test PDF/DOCX Resume Files (Optional)
To create actual PDF and Word documents from the sample text for testing, run:
```bash
python generate_test_files.py
```
This creates `sample_resume.pdf` and `sample_resume.docx` in the root folder.

---

## How to Run

### Option A: Interactive Streamlit Dashboard
Launch the web interface locally:

```bash
streamlit run app.py
```

**Using the Dashboard**:
1. Open the local link (typically `http://localhost:8501`).
2. Input your **OpenAI API Key** in the sidebar (if it is not already loaded from `.env`).
3. Upload `sample_resume.pdf` or `sample_resume.docx` (created by the generator script).
4. Paste the job description from `sample_jd.txt` or select the file upload option.
5. Click **Analyze Resume** and watch the agents collaborate in real-time.
6. Once finished, inspect the score cards and browse specific tabs for **ATS Audit**, **Skills Gap**, and **STAR Rewrites**.
7. Click the **Download Detailed PDF Report** button to download a polished, branded evaluation document.

### Option B: Command Line Interface (CLI)
Run the review command directly in the shell:

```bash
python main.py --resume sample_resume.txt --jd sample_jd.txt
```

**Arguments**:
- `--resume`: Path to the candidate's resume (supports `.txt`, `.pdf`, `.docx`).
- `--jd`: Path to the target job description (supports `.txt`).
- `--model`: (Optional) OpenAI model to use (default: `gpt-4o`).
- `--output`: (Optional) Output path for full JSON results (default: `review_output.json`).

