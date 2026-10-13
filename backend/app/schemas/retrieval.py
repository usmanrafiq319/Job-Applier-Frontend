import uuid

from pydantic import (
    BaseModel,
    Field,
)


class ResumeSearchRequest(BaseModel):

    query: str = Field(
        min_length=2,
        max_length=1000
    )

    limit: int = Field(
        default=5,
        ge=1,
        le=20
    )


class ResumeChunkSearchResult(BaseModel):

    chunk_id: uuid.UUID

    resume_id: uuid.UUID

    page_number: int | None

    content: str

    similarity: float