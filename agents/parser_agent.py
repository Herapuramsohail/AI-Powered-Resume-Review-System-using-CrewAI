from crewai import Agent

def get_parser_agent(llm) -> Agent:
    """
    Creates and returns the Resume Parsing Agent.
    """
    return Agent(
        role="Resume Parsing Specialist",
        goal="Extract raw text from PDF/DOCX resumes and structure it into a comprehensive, valid JSON format containing all standard resume sections.",
        backstory=(
            "You are an expert data extraction specialist with a background in HR systems and applicant tracking systems. "
            "You possess an excellent eye for detail and can convert unstructured, messy text from resumes "
            "into perfectly formatted JSON structures containing Contact Info, Summary, Skills, Work Experience, "
            "Education, Projects, and Certifications."
        ),
        verbose=True,
        llm=llm
    )
