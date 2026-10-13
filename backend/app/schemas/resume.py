import uuid

from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
)


class ResumeResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: uuid.UUID

    original_file_name: str

    mime_type: str | None

    file_size: int | None

    status: str

    is_active: bool

    chunk_count: int

    processed_at: datetime | None

    created_at: datetime

    updated_at: datetime