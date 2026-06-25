from crewai import Task
from tools.models import AtsEvaluation

def get_ats_task(agent, context_tasks: list) -> Task:
    """
    Creates and returns the ATS Evaluation Task.
    """
    return Task(
        description=(
            "Evaluate the ATS compatibility of the candidate's resume.\n\n"
            "Steps:\n"
            "1. Query the knowledge base using the Search Knowledge Base tool for ATS compatibility criteria and formatting rules.\n"
            "2. Read the structured parsed resume from the context.\n"
            "3. Assess the layout and formatting: check for multi-column layouts, tables, images, charts, and potential parsing barriers.\n"
            "4. Scan section headings to ensure they match ATS-friendly standards.\n"
            "5. Evaluate overall readability and compile a detailed list of compatibility issues.\n"
            "6. Calculate an ATS Score (0-100) based on compliance and readability.\n"
            "7. Generate actionable recommendations to resolve all identified issues."
        ),
        expected_output="A structured JSON output matching the AtsEvaluation schema.",
        agent=agent,
        context=context_tasks,
        output_pydantic=AtsEvaluation
    )
