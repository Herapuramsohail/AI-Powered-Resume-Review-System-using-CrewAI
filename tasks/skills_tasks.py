from crewai import Task
from tools.models import SkillsAnalysis

def get_skills_task(agent, job_description: str, context_tasks: list) -> Task:
    """
    Creates and returns the Skills Gap Analysis Task.
    """
    return Task(
        description=(
            "Compare the candidate's skills and experience against the requirements of the target job description.\n\n"
            "Target Job Description:\n"
            "--------------------------------------------------\n"
            f"{job_description}\n"
            "--------------------------------------------------\n\n"
            "Steps:\n"
            "1. Read the parsed resume from the context.\n"
            "2. Map out existing skills that align with the job description.\n"
            "3. Identify key missing technical and soft skills required for the role.\n"
            "4. Query the knowledge base using the Search Knowledge Base tool for recommended training, resources, and certifications "
            "relevant to the target role and missing skills.\n"
            "5. Build a list of recommended courses or certifications including platform names and justifications."
        ),
        expected_output="A structured JSON output matching the SkillsAnalysis schema.",
        agent=agent,
        context=context_tasks,
        output_pydantic=SkillsAnalysis
    )
