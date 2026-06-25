"""
Single-agent, single-task crew.
All knowledge (ATS rules, STAR method) is embedded directly in the prompt.
No RAG tool calls = NO extra LLM round-trips.
Total LLM calls: 1  (vs 3-4 before).
"""
import os, time, json
from dotenv import load_dotenv
load_dotenv()

from crewai import Crew, Process, LLM, Agent, Task
from tools.combined_models import FullAnalysis, FinalReport

# Embedded knowledge (replaces RAG tool calls)
EMBEDDED_KNOWLEDGE = """
=== ATS COMPLIANCE RULES ===
- Use single-column layout. No tables or text boxes for important text.
- Standard section headers: Professional Experience, Skills, Education, Projects, Certifications.
- Contact info in body text, not header/footer.
- Use standard PDF or DOCX. No images, HTML, or graphics.
- Keyword density: mirror exact phrases from the job description.
- No special characters, graphics, or fancy fonts.

=== STAR METHOD FOR BULLET POINTS ===
Each bullet = Situation/Task + Action + Result (quantified).
Strong verbs: Developed, Architected, Reduced, Increased, Led, Automated, Deployed, Optimized.
Example weak: "Worked on backend APIs."
Example strong: "Architected 12 RESTful microservices using FastAPI, reducing average response latency by 38% and supporting 50K daily active users."

=== SKILLS GAP ANALYSIS ===
Compare resume skills directly against job description requirements.
Recommend specific courses: Coursera, Udemy, AWS Training, Google Cloud Skills Boost, LinkedIn Learning.
"""


def run_resume_review_crew(
    resume_text: str,
    job_description: str,
    api_key: str,
    model_name: str = "gemini/gemini-2.5-flash"
) -> dict:
    if not api_key:
        raise ValueError("API key must be provided.")

    if model_name.startswith("gemini/"):
        os.environ["GEMINI_API_KEY"] = api_key
    elif model_name.startswith("anthropic/"):
        os.environ["ANTHROPIC_API_KEY"] = api_key
    else:
        os.environ["OPENAI_API_KEY"] = api_key

    llm = LLM(model=model_name, temperature=0.2, api_key=api_key, timeout=180)

    agent = Agent(
        role="Senior Resume Analysis Expert",
        goal="Perform a complete, accurate resume analysis in one response.",
        backstory=(
            "You are an elite career coach and ATS specialist with 15 years of experience. "
            "You deliver fast, precise, structured resume evaluations."
        ),
        tools=[],
        verbose=False,
        llm=llm,
        max_iter=2,
        max_retry_limit=3,
    )

    task = Task(
        description=(
            "Analyse the resume against the job description. "
            "Use the embedded guidelines below. Return ONE JSON object.\n\n"
            f"{EMBEDDED_KNOWLEDGE}\n\n"
            "=== RESUME ===\n"
            f"{resume_text}\n"
            "=== END RESUME ===\n\n"
            "=== JOB DESCRIPTION ===\n"
            f"{job_description}\n"
            "=== END JOB DESCRIPTION ===\n\n"
            "Instructions:\n"
            "1. PARSE: Extract candidate_name, email, phone, location, summary, skills, "
            "   experience (company/role/duration/description list), education, projects, certifications.\n"
            "2. ATS SCORE (0-100): Check formatting, section headers, keyword density using the ATS rules above.\n"
            "3. SKILLS GAP: existing_skills vs job requirements -> missing_skills and recommended_learning_path.\n"
            "4. JOB MATCH SCORE (0-100): alignment of experience + seniority + projects with JD.\n"
            "5. STAR REWRITES: Find 3 weak bullets, rewrite each using the STAR method above.\n"
            "6. EXECUTIVE SUMMARY: 3-sentence summary of candidate fit.\n"
            "7. HIRING READINESS: one of Excellent Match / Strong Match / Moderate Match / Low Match / Needs Revision.\n"
            "8. TOP 3 IMPROVEMENTS: highest-impact actionable steps.\n\n"
            "Return a single JSON object matching the FullAnalysis schema exactly."
        ),
        expected_output="A valid JSON object matching the FullAnalysis Pydantic schema.",
        agent=agent,
        output_pydantic=FullAnalysis,
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=False,
        max_rpm=4,
        memory=False,
    )

    print("Starting single-agent resume review...")
    max_retries = 4
    retry_delays = [20, 40, 60, 90]
    last_error = None

    for attempt in range(max_retries):
        try:
            crew_output = crew.kickoff()
            break
        except Exception as e:
            err = str(e)
            is_retryable = any(c in err for c in ["503","429","UNAVAILABLE","RESOURCE_EXHAUSTED","high demand","quota"])
            if is_retryable and attempt < max_retries - 1:
                wait = retry_delays[attempt]
                print(f"[Retry {attempt+1}/{max_retries}] API error. Waiting {wait}s...")
                time.sleep(wait)
                last_error = e
            else:
                raise
    else:
        raise RuntimeError(f"Failed after {max_retries} retries. Last: {last_error}")

    # Extract result
    fa = {}
    tasks_output = getattr(crew_output, "tasks_output", None)
    if tasks_output:
        t = tasks_output[0]
        if hasattr(t, "pydantic") and t.pydantic:
            fa = t.pydantic.model_dump() if hasattr(t.pydantic, "model_dump") else dict(t.pydantic)
        elif hasattr(t, "json_dict") and t.json_dict:
            fa = t.json_dict
        else:
            try:
                fa = json.loads(t.raw)
            except Exception:
                fa = {"raw": t.raw}
    else:
        try:
            fa = json.loads(crew_output.raw)
        except Exception:
            fa = {"raw": str(crew_output)}

    # Shape to the dict app.py expects
    return {
        "parsed_resume": {
            "contact_info": {
                "name":  fa.get("candidate_name", ""),
                "email": fa.get("email", ""),
                "phone": fa.get("phone", ""),
                "location": fa.get("location", ""),
                "links": [],
            },
            "summary":        fa.get("summary", ""),
            "skills":         fa.get("skills", []),
            "experience":     fa.get("experience", []),
            "education":      fa.get("education", []),
            "projects":       fa.get("projects", []),
            "certifications": fa.get("certifications", []),
        },
        "ats_evaluation": {
            "ats_score":           fa.get("ats_score", 0),
            "ats_issues":          fa.get("ats_issues", []),
            "ats_recommendations": fa.get("ats_recommendations", []),
        },
        "skills_analysis": {
            "existing_skills":          fa.get("existing_skills", fa.get("skills", [])),
            "missing_skills":           fa.get("missing_skills", []),
            "recommended_learning_path": fa.get("recommended_learning_path", []),
        },
        "job_match": {
            "match_score":                    fa.get("job_match_score", 0),
            "matching_skills_and_experience": fa.get("matching_skills_and_experience", []),
            "missing_requirements":           fa.get("missing_requirements", []),
        },
        "content_improvement": {
            "weak_descriptions": fa.get("weak_descriptions", []),
            "improved_bullets":  fa.get("improved_bullets", []),
        },
        "final_report": {
            "executive_summary":      fa.get("executive_summary", ""),
            "ats_score":              fa.get("ats_score", 0),
            "job_match_score":        fa.get("job_match_score", 0),
            "top_improvements":       fa.get("top_improvements", []),
            "hiring_readiness_rating": fa.get("hiring_readiness_rating", "Needs Revision"),
        },
    }
