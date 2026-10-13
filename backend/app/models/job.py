import uuid

from sqlalchemy import (
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


class Job(
    TimestampMixin,
    Base
):

    __tablename__ = "jobs"


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


    title: Mapped[str] = mapped_column(
        String(250),
        nullable=False
    )


    company: Mapped[str] = mapped_column(
        String(250),
        nullable=False
    )


    location: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True
    )


    job_url: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True
    )


    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )


    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="FOUND",
        index=True
    )


    source: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )


    profile = relationship(
        "Profile",
        back_populates="jobs"
    )


    requirements = relationship(
        "JobRequirement",
        back_populates="job",
        cascade="all, delete-orphan"
    )


    analysis = relationship(
        "JobAnalysis",
        back_populates="job",
        cascade="all, delete-orphan",
        uselist=False
    )

    profile = relationship(
        "Profile",
        back_populates="jobs"
    )