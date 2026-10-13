import uuid

from pgvector.sqlalchemy import VECTOR

from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)

from sqlalchemy.dialects.postgresql import (
    JSONB,
    UUID,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.core.constants import EMBEDDING_DIMENSION
from app.db.base import Base
from app.models.mixins import TimestampMixin


class ResumeChunk(
    TimestampMixin,
    Base
):

    __tablename__ = "resume_chunks"


    __table_args__ = (

        UniqueConstraint(
            "resume_id",
            "chunk_index",
            name="uq_resume_chunks_resume_chunk_index"
        ),

    )


    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )


    resume_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),

        ForeignKey(
            "resumes.id",
            ondelete="CASCADE"
        ),

        nullable=False,
        index=True
    )


    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )


    chunk_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )


    page_number: Mapped[
        int | None
    ] = mapped_column(
        Integer,
        nullable=True
    )


    chunk_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="TEXT"
    )


    token_count: Mapped[
        int | None
    ] = mapped_column(
        Integer,
        nullable=True
    )


    extra_metadata: Mapped[
        dict | None
    ] = mapped_column(
        JSONB,
        nullable=True
    )


    embedding: Mapped[
        list[float] | None
    ] = mapped_column(

        VECTOR(
            EMBEDDING_DIMENSION
        ),

        nullable=True
    )


    resume = relationship(
        "Resume",
        back_populates="chunks"
    )