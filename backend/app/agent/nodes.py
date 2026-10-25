import uuid

from langgraph.runtime import Runtime

from app.agent.context import (
    AgentContext,
)

from app.agent.schemas import (
    AdvancedAgentReview,
    FastAgentReview,
)

from app.agent.state import (
    CareerAgentState,
)

from app.integrations.llm.llm_router import (
    LLMMode,
    LLMRouter,
)

from app.schemas.job_analysis import (
    JobAnalyzeRequest,
)

from app.services.job_analysis_service import (
    JobAnalysisService,
)


analysis_service = JobAnalysisService()

llm_router = LLMRouter()

async def analyze_job_node(
    state: CareerAgentState,
    runtime: Runtime[AgentContext]
) -> dict:

    job_id = uuid.UUID(
        state["job_id"]
    )


    result = await analysis_service.analyze_job(
        runtime.context.db,

        JobAnalyzeRequest(
            job_id=job_id,
            resume_limit=state.get(
                "resume_limit",
                5
            )
        )
    )


    return {

        "match_score":
            result.match_score,

        "recommendation":
            result.recommendation,

        "matched_skills":
            result.matched_skills,

        "missing_skills":
            result.missing_skills,

        "evidence_count":
            len(
                result.relevant_experience
            ),

        "analysis_summary":
            result.summary,

        "status":
            "ANALYZED",
    }

async def fast_review_node(
    
    state: CareerAgentState
) -> dict:

    prompt = f"""
Review this job/profile analysis.

Match score:
{state["match_score"]}

Recommendation:
{state["recommendation"]}

Matched skills:
{", ".join(state["matched_skills"]) or "None"}

Missing skills:
{", ".join(state["missing_skills"]) or "None"}

Relevant evidence count:
{state["evidence_count"]}

Existing deterministic summary:
{state.get("analysis_summary") or "None"}

Your task:

1. Explain briefly why this candidate is or is not
   a good match.

2. Do not invent skills, experience, education,
   or evidence.

3. Mark needs_advanced_reasoning=true only when
   the available evidence is ambiguous, conflicting,
   incomplete, or the decision genuinely needs
   deeper interpretation.

4. Do not automatically request advanced reasoning
   just because the candidate has missing skills.

Keep the reasoning concise.
""".strip()


    review = await llm_router.generate_structured(

        prompt=prompt,

        schema=FastAgentReview,

        system_prompt=(
            "You are a careful technical job "
            "matching assistant. Base every conclusion "
            "only on the supplied evidence."
        ),

        mode=LLMMode.FAST
    )


    return {

        "fast_reasoning":
            review.reasoning,

        "fast_confidence":
            review.confidence,

        "needs_advanced_reasoning":
            review.needs_advanced_reasoning,

        "status":
            "FAST_REVIEW_COMPLETE",
            
    }

def route_after_fast_review(
    state: CareerAgentState
) -> str:

    if state.get(
        "needs_advanced_reasoning",
        False
    ):

        return "advanced_review"


    return "finalize"

async def advanced_review_node(
    state: CareerAgentState
) -> dict:

    prompt = f"""
Perform a deeper review of this technical
job/candidate match.

Match score:
{state["match_score"]}

Recommendation:
{state["recommendation"]}

Matched skills:
{", ".join(state["matched_skills"]) or "None"}

Missing skills:
{", ".join(state["missing_skills"]) or "None"}

Relevant evidence count:
{state["evidence_count"]}

Deterministic summary:
{state.get("analysis_summary") or "None"}

Initial Groq review:
{state.get("fast_reasoning") or "None"}

Initial confidence:
{state.get("fast_confidence", 0)}

Determine whether the deterministic score and
initial reasoning are reasonable.

Explain important strengths, meaningful gaps,
and uncertainty.

Do not invent any candidate experience or skills.
""".strip()


    review = await llm_router.generate_structured(

        prompt=prompt,

        schema=AdvancedAgentReview,

        system_prompt=(
            "You are the advanced reasoning layer "
            "of an AI career matching system. "
            "Use only supplied evidence."
        ),

        mode=LLMMode.ADVANCED
    )


    return {

        "advanced_reasoning":
            review.reasoning,

        "status":
            "ADVANCED_REVIEW_COMPLETE",
    }

async def finalize_node(
    state: CareerAgentState
) -> dict:

    advanced = state.get(
        "advanced_reasoning"
    )


    if advanced:

        final_reasoning = advanced

        provider = "gemini"

    else:

        final_reasoning = state.get(
            "fast_reasoning",
            ""
        )

        provider = "groq"


    return {

        "final_reasoning":
            final_reasoning,

        "llm_provider":
            provider,

        "status":
            "COMPLETED",
    }