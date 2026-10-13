import uuid

from datetime import datetime
from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


JobStatus = Literal[
    "FOUND",
    "ANALYZED",
    "HIGH_MATCH",
    "LOW_MATCH",
    "SAVED",
    "REJECTED",
    "APPLIED",
]


class JobCreateRequest(BaseModel):

    title: str = Field(
        min_length=1,
        max_length=250
    )

    company: str = Field(
        min_length=1,
        max_length=250
    )

    location: str | None = Field(
        default=None,
        max_length=200
    )

    job_url: str | None = Field(
        default=None,
        max_length=1000
    )

    description: str = Field(
        min_length=10
    )

    source: str | None = Field(
        default=None,
        max_length=100
    )


class JobStatusUpdateRequest(BaseModel):

    status: JobStatus


class JobResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: uuid.UUID

    title: str

    company: str

    location: str | None

    job_url: str | None

    description: str

    status: str

    source: str | None

    created_at: datetime

    updated_at: datetime