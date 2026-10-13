import uuid

from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.base import Base
from app.models.mixins import TimestampMixin


class Resume(
    TimestampMixin,
    Base
):

    __tablename__ = "resumes"


    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )


    profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),

        ForeignKey(
            "profiles.id",
            ondelete="CASCADE"
        ),

        nullable=False,
        index=True
    )


    original_file_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )


    storage_path: Mapped[
        str | None
    ] = mapped_column(
        String(1000),
        nullable=True
    )


    mime_type: Mapped[
        str | None
    ] = mapped_column(
        String(100),
        nullable=True
    )


    file_size: Mapped[
        int | None
    ] = mapped_column(
        Integer,
        nullable=True
    )


    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="UPLOADED"
    )


    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )


    chunk_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )


    processed_at: Mapped[
        datetime | None
    ] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )


    profile = relationship(
        "Profile",
        back_populates="resumes"
    )


    chunks = relationship(
        "ResumeChunk",
        back_populates="resume",
        cascade="all, delete-orphan"
    )