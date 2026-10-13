import uuid

from sqlalchemy import String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.base import Base
from app.models.mixins import TimestampMixin


class Profile(
    TimestampMixin,
    Base
):

    __tablename__ = "profiles"


    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )


    full_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )


    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True
    )


    phone: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )


    location: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True
    )


    headline: Mapped[str | None] = mapped_column(
        String(300),
        nullable=True
    )


    professional_summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )


    linkedin_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )


    github_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )


    portfolio_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )


    skill_links = relationship(
        "ProfileSkill",
        back_populates="profile",
        cascade="all, delete-orphan"
    )

    educations = relationship(
        "Education",
        back_populates="profile",
        cascade="all, delete-orphan"
    )

    projects = relationship(
        "Project",
        back_populates="profile",
        cascade="all, delete-orphan"
    )

    experiences = relationship(
        "Experience",
        back_populates="profile",
        cascade="all, delete-orphan"
    )

    resumes = relationship(
        "Resume",
        back_populates="profile",
        cascade="all, delete-orphan"
    )    

    jobs = relationship(
        "Job",
        back_populates="profile"
    )