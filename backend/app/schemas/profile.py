import uuid

from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class ProfileUpsertRequest(BaseModel):

    full_name: str = Field(
        min_length=2,
        max_length=150
    )

    email: str = Field(
        min_length=3,
        max_length=255
    )

    phone: str | None = None

    location: str | None = None

    headline: str | None = None

    professional_summary: str | None = None

    linkedin_url: str | None = None

    github_url: str | None = None

    portfolio_url: str | None = None


class ProfileResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: uuid.UUID

    full_name: str

    email: str

    phone: str | None

    location: str | None

    headline: str | None

    professional_summary: str | None

    linkedin_url: str | None

    github_url: str | None

    portfolio_url: str | None

    created_at: datetime

    updated_at: datetime