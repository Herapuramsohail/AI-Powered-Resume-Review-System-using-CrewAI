from pydantic import BaseModel, Field
from typing import List, Optional, Dict

# ================= Parser Models =================

class ContactInfo(BaseModel):
    name: str = Field(..., description="Candidate's full name.")
    email: Optional[str] = Field(None, description="Candidate's email address.")
    phone: Optional[str] = Field(None, description="Candidate's phone number.")
    location: Optional[str] = Field(None, description="Candidate's city and state/country.")
    links: List[str] = Field(default_factory=list, description="List of professional links (e.g. LinkedIn, GitHub, Portfolio).")

class WorkExperience(BaseModel):
    company: str = Field(..., description="Name of the company or organization.")
    role: str = Field(..., description="Job title.")
    duration: str = Field(..., description="Employment dates or duration (e.g. June 2021 - Present).")
    description: List[str] = Field(..., description="List of accomplishments or responsibilities as bullet points.")

class Education(BaseModel):
    institution: str = Field(..., description="Name of the university, college, or school.")
    degree: str = Field(..., description="Degree obtained and field of study.")
    duration: Optional[str] = Field(None, description="Dates attended.")

class Project(BaseModel):
    title: str = Field(..., description="Name of the project.")
    description: str = Field(..., description="Brief description of the project, including technologies used and outcomes.")

class ParsedResume(BaseModel):
    contact_info: ContactInfo = Field(..., description="Contact details extracted from the resume.")
    summary: Optional[str] = Field(None, description="Candidate's professional summary or objective.")
    skills: List[str] = Field(default_factory=list, description="List of technical and soft skills extracted.")
    experience: List[WorkExperience] = Field(default_factory=list, description="Candidate's job history.")
    education: List[Education] = Field(default_factory=list, description="Candidate's educational background.")
    projects: List[Project] = Field(default_factory=list, description="Candidate's projects.")
    certifications: List[str] = Field(default_factory=list, description="List of licenses, credentials, or certifications.")


# ================= ATS Models =================

class AtsEvaluation(BaseModel):
    ats_score: int = Field(..., description="ATS compatibility score from 0 to 100 based on structure, formatting, and content.")
    ats_issues: List[str] = Field(..., description="List of specific ATS compatibility issues (e.g., tables, graphics, poor fonts).")
    ats_recommendations: List[str] = Field(..., description="List of action items to fix the ATS compatibility issues.")


# ================= Skills Models =================

class CourseOrCert(BaseModel):
    name: str = Field(..., description="Name of recommended course or certification.")
    platform_or_provider: str = Field(..., description="Where to take it (e.g. Coursera, Udemy, AWS).")
    why_recommended: str = Field(..., description="Brief justification explaining which skill gap it addresses.")

class SkillsAnalysis(BaseModel):
    existing_skills: List[str] = Field(..., description="Skills from the resume that match or align with the job description.")
    missing_skills: List[str] = Field(..., description="Required skills from the job description that are missing from the resume.")
    recommended_learning_path: List[CourseOrCert] = Field(default_factory=list, description="List of recommended upskilling paths.")


# ================= Job Match Models =================

class JobMatch(BaseModel):
    match_score: int = Field(..., description="Match percentage from 0 to 100 between the resume and the job description.")
    matching_skills_and_experience: List[str] = Field(..., description="Aspects of experience and skills that closely match the job.")
    missing_requirements: List[str] = Field(..., description="Critical requirements or experience levels mentioned in the job post that are missing.")


# ================= Content Improvement Models =================

class BulletRewrite(BaseModel):
    original: str = Field(..., description="The original bullet point from the resume.")
    rewritten: str = Field(..., description="The rewritten bullet point using the STAR method and strong action verbs.")
    rationale: str = Field(..., description="Explanation of what was changed and why (e.g. added metrics, replaced weak verb).")

class ContentImprovement(BaseModel):
    weak_descriptions: List[str] = Field(..., description="List of weak descriptions or duty-heavy phrases found in the resume.")
    improved_bullets: List[BulletRewrite] = Field(..., description="List of rewritten bullet points with explanation.")


# ================= Final Review Models =================

class FinalReport(BaseModel):
    executive_summary: str = Field(..., description="High-level professional overview of the candidate's profile and match.")
    ats_score: int = Field(..., description="ATS compatibility score (0-100).")
    job_match_score: int = Field(..., description="Job description alignment score (0-100).")
    top_improvements: List[str] = Field(..., description="Top 3 high-impact improvement recommendations for the candidate.")
    hiring_readiness_rating: str = Field(..., description="Hiring readiness assessment: 'Excellent Match', 'Strong Match', 'Moderate Match', 'Low Match', or 'Needs Revision'.")
