from crewai import Agent
from tools.rag_tool import SearchKnowledgeBaseTool

def get_ats_agent(llm) -> Agent:
    """
    Creates and returns the ATS Evaluation Agent.
    """
    return Agent(
        role="ATS Evaluation Expert",
        goal="Analyze a parsed resume's formatting, structure, and keyword density against target job descriptions and ATS compliance guidelines, returning an ATS score, list of issues, and recommendations.",
        backstory=(
            "You are a seasoned HR systems architect who has designed and customized major Applicant Tracking Systems (ATS). "
            "You know exactly what causes parsing errors and how resumes are scored. "
            "You use your RAG tool to search for ATS compliance guidelines and compare the input resume's formatting "
            "(like multi-column layouts, tables, visual assets) and text elements to ensure it passes the ATS gates."
        ),
        tools=[SearchKnowledgeBaseTool()],
        verbose=True,
        llm=llm
    )
