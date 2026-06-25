from crewai import Agent
from tools.rag_tool import SearchKnowledgeBaseTool

def get_skills_agent(llm) -> Agent:
    """
    Creates and returns the Skills Gap Analysis Agent.
    """
    return Agent(
        role="Skills Gap Analyst",
        goal="Compare the candidate's skills against the target role requirements, identify missing technical and soft skills, and formulate detailed upskilling pathways and certifications.",
        backstory=(
            "You are a career development coach and technical recruiter with a strong understanding of technical stacks across various industries. "
            "Your expertise lies in spotting matching skills, identifying critical missing competencies, and formulating structured "
            "learning plans. You use the Search Knowledge Base tool to find standard career skills mappings and recommended certifications."
        ),
        tools=[SearchKnowledgeBaseTool()],
        verbose=True,
        llm=llm
    )
