import uuid

from pydantic import (
    BaseModel,
    Field,
)


class SkillCreateRequest(BaseModel):

    name: str = Field(
        min_length=1,
        max_length=120
    )

    category: str = Field(
        default="OTHER",
        max_length=50
    )

    level: str = Field(
        default="BEGINNER",
        max_length=30
    )


class SkillUpdateRequest(BaseModel):

    category: str | None = Field(
        default=None,
        max_length=50
    )

    level: str | None = Field(
        default=None,
        max_length=30
    )


class SkillResponse(BaseModel):

    id: uuid.UUID

    name: str

    category: str

    level: str