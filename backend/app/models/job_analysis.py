import uuid

from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)

from sqlalchemy.dialects.postgresql import (
    ARRAY,
    JSONB,
    UUID,
)

from sqlalchemy.ext.mutable import (
    MutableList,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.base import Base
from app.models.mixins import TimestampMixin


class JobAnalysis(
    TimestampMixin,
    Base
):

    __tablename__ = "job_analyses"


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
        unique=True,
        index=True
    )


    match_score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )


    recommendation: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="LOW_MATCH"
    )


    matched_skills: Mapped[list[str]] = mapped_column(

        MutableList.as_mutable(
            ARRAY(
                String(120)
            )
        ),

        nullable=False,
        default=list
    )


    missing_skills: Mapped[list[str]] = mapped_column(

        MutableList.as_mutable(
            ARRAY(
                String(120)
            )
        ),

        nullable=False,
        default=list
    )


    relevant_experience: Mapped[list] = mapped_column(
        MutableList.as_mutable(
            JSONB
        ),
        nullable=False,
        default=list
    )


    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )


    analyzed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )


    job = relationship(
        "Job",
        back_populates="analysis"
    )