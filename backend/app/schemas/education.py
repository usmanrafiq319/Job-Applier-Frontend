import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class EducationCreateRequest(BaseModel):
    degree: str = Field(
        min_length=1,
        max_length=200
    )

    institute: str = Field(
        min_length=1,
        max_length=250
    )

    start_date: date | None = None
    end_date: date | None = None

    cgpa: str | None = Field(
        default=None,
        max_length=30
    )


class EducationUpdateRequest(BaseModel):
    degree: str | None = Field(
        default=None,
        min_length=1,
        max_length=200
    )

    institute: str | None = Field(
        default=None,
        min_length=1,
        max_length=250
    )

    start_date: date | None = None
    end_date: date | None = None

    cgpa: str | None = Field(
        default=None,
        max_length=30
    )


class EducationResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: uuid.UUID
    degree: str
    institute: str
    start_date: date | None
    end_date: date | None
    cgpa: str | None

    created_at: datetime
    updated_at: datetime