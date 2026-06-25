"""
Single combined output model for the 1-agent, 1-task crew.
All analysis fields + report fields in ONE schema.
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class WorkExperience(BaseModel):
    company: str
    role: str
    duration: str
    description: List[str]


class Education(BaseModel):
    institution: str
    degree: str
    duration: Optional[str] = None


class Project(BaseModel):
    title: str
    description: str


class CourseOrCert(BaseModel):
    name: str
    platform_or_provider: str
    why_recommended: str


class BulletRewrite(BaseModel):
    original: str
    rewritten: str
    rationale: str


class FullAnalysis(BaseModel):
    # Parsed resume
    candidate_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    summary: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    experience: List[WorkExperience] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)
    projects: List[Project] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)

    # ATS
    ats_score: int = Field(..., description="ATS compatibility score 0-100.")
    ats_issues: List[str] = Field(default_factory=list)
    ats_recommendations: List[str] = Field(default_factory=list)

    # Skills gap
    existing_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    recommended_learning_path: List[CourseOrCert] = Field(default_factory=list)

    # Job match
    job_match_score: int = Field(..., description="Job match score 0-100.")
    matching_skills_and_experience: List[str] = Field(default_factory=list)
    missing_requirements: List[str] = Field(default_factory=list)

    # STAR rewrites
    weak_descriptions: List[str] = Field(default_factory=list)
    improved_bullets: List[BulletRewrite] = Field(default_factory=list)

    # Executive report (merged - no separate Report Agent needed)
    executive_summary: str = Field(default="", description="3-sentence executive summary.")
    hiring_readiness_rating: str = Field(
        default="Needs Revision",
        description="One of: Excellent Match, Strong Match, Moderate Match, Low Match, Needs Revision."
    )
    top_improvements: List[str] = Field(
        default_factory=list,
        description="Top 3 highest-impact improvement recommendations."
    )


# Keep FinalReport for backward compat (unused by new crew)
class FinalReport(BaseModel):
    executive_summary: str
    ats_score: int
    job_match_score: int
    top_improvements: List[str]
    hiring_readiness_rating: str
