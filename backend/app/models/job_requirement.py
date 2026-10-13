import uuid

from sqlalchemy import (
    Boolean,
    ForeignKey,
    String,
    Text,
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.base import Base
from app.models.mixins import TimestampMixin


class JobRequirement(
    TimestampMixin,
    Base
):

    __tablename__ = "job_requirements"


    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )


    job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),

        ForeignKey(
            "jobs.id",
            ondelete="CASCADE"
        ),

        nullable=False,
        index=True
    )


    text: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )


    requirement_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="OTHER"
    )


    skill_name: Mapped[str | None] = mapped_column(
        String(120),
        nullable=True
    )


    is_required: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )


    importance: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="MEDIUM"
    )


    job = relationship(
        "Job",
        back_populates="requirements"
    )