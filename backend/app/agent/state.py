from typing import TypedDict


class CareerAgentState(
    TypedDict,
    total=False
):

    job_id: str

    resume_limit: int


    match_score: int

    recommendation: str

    matched_skills: list[str]

    missing_skills: list[str]

    evidence_count: int

    analysis_summary: str | None


    fast_reasoning: str

    fast_confidence: int

    needs_advanced_reasoning: bool


    advanced_reasoning: str


    final_reasoning: str

    llm_provider: str

    status: str