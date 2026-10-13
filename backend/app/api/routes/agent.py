from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.agent.context import (
    AgentContext,
)

from app.agent.graph import (
    career_agent_graph,
)

from app.db.session import get_db

from app.schemas.agent import (
    AgentAnalyzeJobRequest,
    AgentAnalyzeJobResponse,
)


router = APIRouter(
    prefix="/agent",
    tags=["Agent"]
)


@router.post(
    "/analyze-job",
    response_model=AgentAnalyzeJobResponse
)
async def analyze_job_with_agent(
    payload: AgentAnalyzeJobRequest,
    db: AsyncSession = Depends(get_db)
):

    result = await career_agent_graph.ainvoke(

        {
            "job_id":
                str(payload.job_id),

            "resume_limit":
                payload.resume_limit,

            "status":
                "STARTED",
        },

        context=AgentContext(
            db=db
        )
    )


    return AgentAnalyzeJobResponse(

        job_id=payload.job_id,

        match_score=result[
            "match_score"
        ],

        recommendation=result[
            "recommendation"
        ],

        matched_skills=result[
            "matched_skills"
        ],

        missing_skills=result[
            "missing_skills"
        ],

        evidence_count=result[
            "evidence_count"
        ],

        final_reasoning=result[
            "final_reasoning"
        ],

        llm_provider=result[
            "llm_provider"
        ],

        used_advanced_reasoning=(
            bool(
                result.get(
                    "advanced_reasoning"
                )
            )
        ),

        status=result[
            "status"
        ],
    )