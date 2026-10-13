from typing import Literal

from pydantic import (
    BaseModel,
    Field,
)


RequirementType = Literal[
    "SKILL",
    "EXPERIENCE",
    "EDUCATION",
    "RESPONSIBILITY",
    "OTHER",
]


RequirementImportance = Literal[
    "LOW",
    "MEDIUM",
    "HIGH",
]


class ExtractedRequirement(BaseModel):

    text: str = Field(
        min_length=1
    )

    requirement_type: RequirementType

    skill_name: str | None = None

    is_required: bool = True

    importance: RequirementImportance = (
        "MEDIUM"
    )


class RequirementExtractionOutput(
    BaseModel
):

    requirements: list[
        ExtractedRequirement
    ]