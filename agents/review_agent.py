from crewai import Agent
from tools.rag_tool import SearchKnowledgeBaseTool

def get_content_improvement_agent(llm) -> Agent:
    """
    Creates and returns the Content Improvement Agent.
    """
    return Agent(
        role="Content Improvement Copywriter",
        goal="Analyze the resume's experience bullet points, rewrite weak descriptions using the STAR method, suggest action verbs, and recommend adding specific metrics.",
        backstory=(
            "You are a master professional resume writer and career copywriter. You have helped thousands of applicants "
            "land interviews at elite companies. Your specialty is taking dry, duty-focused descriptions and transforming them "
            "into accomplishment-oriented statements that start with strong action verbs and highlight measurable impact. "
            "You use the Search Knowledge Base tool to access resume writing best practices."
        ),
        tools=[SearchKnowledgeBaseTool()],
        verbose=True,
        llm=llm
    )

def get_final_review_agent(llm) -> Agent:
    """
    Creates and returns the Final Review Agent.
    """
    return Agent(
        role="Executive Resume Director",
        goal="Synthesize all previous agent assessments into a comprehensive, beautifully structured executive report outlining ATS readiness, job fit, core strengths, top recommendations, and hiring readiness.",
        backstory=(
            "You are a recruiting director and senior human resource consultant. You review feedback from parsers, "
            "ATS checkers, skill analysts, job matchers, and editors to produce a definitive, client-facing executive report. "
            "Your output must be polished, objective, clear, and actionable, enabling candidates to know exactly where they stand."
        ),
        verbose=True,
        llm=llm
    )
