import uuid
from datetime import date, datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class ExperienceCreateRequest(BaseModel):

    company: str = Field(
        min_length=1,
        max_length=200
    )

    role: str = Field(
        min_length=1,
        max_length=200
    )

    start_date: date | None = None

    end_date: date | None = None

    currently_working: bool = False

    description: str = Field(
        min_length=1
    )

    technologies: list[str] = Field(
        default_factory=list
    )


class ExperienceUpdateRequest(BaseModel):

    company: str | None = Field(
        default=None,
        min_length=1,
        max_length=200
    )

    role: str | None = Field(
        default=None,
        min_length=1,
        max_length=200
    )

    start_date: date | None = None

    end_date: date | None = None

    currently_working: bool | None = None

    description: str | None = Field(
        default=None,
        min_length=1
    )

    technologies: list[str] | None = None


class ExperienceResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: uuid.UUID

    company: str

    role: str

    start_date: date | None

    end_date: date | None

    currently_working: bool

    description: str

    technologies: list[str]

    created_at: datetime

    updated_at: datetime