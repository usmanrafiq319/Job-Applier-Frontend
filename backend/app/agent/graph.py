from langgraph.graph import (
    END,
    START,
    StateGraph,
)

from app.agent.context import (
    AgentContext,
)

from app.agent.nodes import (
    advanced_review_node,
    analyze_job_node,
    fast_review_node,
    finalize_node,
    route_after_fast_review,
)

from app.agent.state import (
    CareerAgentState,
)


builder = StateGraph(
    CareerAgentState,
    context_schema=AgentContext
)


builder.add_node(
    "analyze_job",
    analyze_job_node
)


builder.add_node(
    "fast_review",
    fast_review_node
)


builder.add_node(
    "advanced_review",
    advanced_review_node
)


builder.add_node(
    "finalize",
    finalize_node
)


builder.add_edge(
    START,
    "analyze_job"
)


builder.add_edge(
    "analyze_job",
    "fast_review"
)


builder.add_conditional_edges(
    "fast_review",
    route_after_fast_review,
    {
        "advanced_review":
            "advanced_review",

        "finalize":
            "finalize",
    }
)


builder.add_edge(
    "advanced_review",
    "finalize"
)


builder.add_edge(
    "finalize",
    END
)


career_agent_graph = (
    builder.compile()
)