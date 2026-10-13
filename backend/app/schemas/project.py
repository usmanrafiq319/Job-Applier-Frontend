import uuid
from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class ProjectCreateRequest(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=200
    )

    description: str = Field(
        min_length=1
    )

    technologies: list[str] = Field(
        default_factory=list
    )

    project_url: str | None = Field(
        default=None,
        max_length=500
    )

    github_url: str | None = Field(
        default=None,
        max_length=500
    )


class ProjectUpdateRequest(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200
    )

    description: str | None = Field(
        default=None,
        min_length=1
    )

    technologies: list[str] | None = None

    project_url: str | None = Field(
        default=None,
        max_length=500
    )

    github_url: str | None = Field(
        default=None,
        max_length=500
    )


class ProjectResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: uuid.UUID
    title: str
    description: str
    technologies: list[str]

    project_url: str | None
    github_url: str | None

    created_at: datetime
    updated_at: datetime