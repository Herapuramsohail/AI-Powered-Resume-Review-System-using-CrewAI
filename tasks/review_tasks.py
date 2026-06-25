from crewai import Task
from tools.models import JobMatch, ContentImprovement, FinalReport

def get_job_match_task(agent, job_description: str, context_tasks: list) -> Task:
    """
    Creates and returns the Job Match Task.
    """
    return Task(
        description=(
            "Analyze the alignment between the candidate's history and the job description.\n\n"
            "Job Description:\n"
            "--------------------------------------------------\n"
            f"{job_description}\n"
            "--------------------------------------------------\n\n"
            "Steps:\n"
            "1. Review the parsed resume details from the context.\n"
            "2. Check if the candidate's projects and past roles represent the responsibilities required by the job.\n"
            "3. Determine if the seniority level and scale of previous work matches the target role.\n"
            "4. Identify specific areas where the candidate's background matches the requirements.\n"
            "5. Pinpoint key requirements in the job description that are missing from the resume.\n"
            "6. Calculate a Match Score (0-100) representing semantic alignment."
        ),
        expected_output="A structured JSON output matching the JobMatch schema.",
        agent=agent,
        context=context_tasks,
        output_pydantic=JobMatch
    )

def get_content_improvement_task(agent, context_tasks: list) -> Task:
    """
    Creates and returns the Content Improvement Task.
    """
    return Task(
        description=(
            "Review and optimize the resume's experience descriptions and bullet points.\n\n"
            "Steps:\n"
            "1. Search the knowledge base for 'STAR method' and 'resume writing' guidelines using the Search Knowledge Base tool.\n"
            "2. Read the parsed resume from the context.\n"
            "3. Identify at least 3-5 weak bullet points or descriptions that are duty-oriented rather than achievement-oriented.\n"
            "4. Rewrite these bullet points to start with strong action verbs, use the STAR format, and suggest placing quantifiable metrics.\n"
            "5. Explain the rationale for each rewrite (what was improved, why it is stronger)."
        ),
        expected_output="A structured JSON output matching the ContentImprovement schema.",
        agent=agent,
        context=context_tasks,
        output_pydantic=ContentImprovement
    )

def get_final_review_task(agent, context_tasks: list) -> Task:
    """
    Creates and returns the Final Review Task.
    """
    return Task(
        description=(
            "Compile and synthesize all previous agent reviews into a final cohesive evaluation.\n\n"
            "Steps:\n"
            "1. Read the outputs from all previous tasks (Parsing, ATS check, Skills analysis, Job match, Content rewrites) in the context.\n"
            "2. Write a comprehensive professional Executive Summary of the candidate's candidacy, strengths, and fit.\n"
            "3. Consolidate the ATS Score (0-100) and Job Match Score (0-100) from the previous tasks.\n"
            "4. Identify the top 3 highest-priority, actionable improvements the candidate should make.\n"
            "5. Make a final hiring readiness rating ('Excellent Match', 'Strong Match', 'Moderate Match', 'Low Match', 'Needs Revision').\n\n"
            "The final report must be structured, professional, and ready to be delivered to a job seeker."
        ),
        expected_output="A structured JSON output matching the FinalReport schema.",
        agent=agent,
        context=context_tasks,
        output_pydantic=FinalReport
    )
