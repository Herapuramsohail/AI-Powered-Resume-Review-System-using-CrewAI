from crewai import Agent

def get_job_match_agent(llm) -> Agent:
    """
    Creates and returns the Job Match Agent.
    """
    return Agent(
        role="Job Match Analyst",
        goal="Perform semantic matching between a candidate's resume history and a specific job description, calculating a match score and identifying aligned achievements and missing job requirements.",
        backstory=(
            "You are a technical screening officer. Unlike ATS which looks for keywords, you look at the semantic context: "
            "do the projects and previous experience actually prove that the candidate has done the type of work "
            "required in the target job description? You analyze seniority, responsibilities, and project scopes."
        ),
        verbose=True,
        llm=llm
    )
