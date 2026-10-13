import uuid

from pydantic import (
    BaseModel,
    Field,
)


class AgentAnalyzeJobRequest(BaseModel):

    job_id: uuid.UUID

    resume_limit: int = Field(
        default=5,
        ge=1,
        le=10
    )


class AgentAnalyzeJobResponse(BaseModel):

    job_id: uuid.UUID

    match_score: int

    recommendation: str

    matched_skills: list[str]

    missing_skills: list[str]

    evidence_count: int

    final_reasoning: str

    llm_provider: str

    used_advanced_reasoning: bool

    status: str