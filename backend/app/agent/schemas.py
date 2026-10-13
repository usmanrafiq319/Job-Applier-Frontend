from pydantic import (
    BaseModel,
    Field,
)


class FastAgentReview(BaseModel):

    reasoning: str = Field(
        min_length=10
    )

    confidence: int = Field(
        ge=0,
        le=100
    )

    needs_advanced_reasoning: bool


class AdvancedAgentReview(BaseModel):

    reasoning: str = Field(
        min_length=10
    )

    confidence: int = Field(
        ge=0,
        le=100
    )