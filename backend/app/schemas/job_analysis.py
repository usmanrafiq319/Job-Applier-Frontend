import uuid

from datetime import datetime

from pydantic import (
    BaseModel,
    Field,
)


class JobAnalyzeRequest(BaseModel):

    job_id: uuid.UUID

    resume_limit: int = Field(
        default=5,
        ge=1,
        le=10
    )


class JobRequirementResponse(BaseModel):

    id: uuid.UUID

    text: str

    requirement_type: str

    skill_name: str | None

    is_required: bool

    importance: str


class RelevantEvidence(BaseModel):

    source: str

    source_id: str

    title: str

    content: str

    relevance: float


class JobAnalysisResponse(BaseModel):

    id: uuid.UUID

    job_id: uuid.UUID

    match_score: int

    recommendation: str

    matched_skills: list[str]

    missing_skills: list[str]

    relevant_experience: list[
        RelevantEvidence
    ]

    summary: str | None

    analyzed_at: datetime

    requirements: list[
        JobRequirementResponse
    ]