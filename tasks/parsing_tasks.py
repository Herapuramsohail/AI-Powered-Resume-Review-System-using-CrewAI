from crewai import Task
from tools.models import ParsedResume

def get_parsing_task(agent, resume_text: str) -> Task:
    """
    Creates and returns the Resume Parsing Task.
    """
    return Task(
        description=(
            "Analyze the following raw text extracted from a candidate's resume.\n\n"
            "Raw Resume Text:\n"
            "--------------------------------------------------\n"
            f"{resume_text}\n"
            "--------------------------------------------------\n\n"
            "Extract and organize all information into standard resume sections: "
            "Contact Info (name, email, phone, location, links), Summary/Objective, "
            "Skills list, Experience (company, role, duration, achievements/descriptions), "
            "Education history, Projects, and Certifications.\n"
            "Ensure that no information is lost, and non-standard text is classified "
            "under the most logical section. Return a clean, structured output."
        ),
        expected_output="A structured JSON output matching the ParsedResume schema.",
        agent=agent,
        output_pydantic=ParsedResume
    )
