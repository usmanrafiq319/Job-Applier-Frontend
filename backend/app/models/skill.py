import uuid

from sqlalchemy import (
    ForeignKey,
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


class Skill(
    TimestampMixin,
    Base
):

    __tablename__ = "skills"


    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )


    name: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        unique=True,
        index=True
    )


    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="OTHER"
    )


    profile_links = relationship(
        "ProfileSkill",
        back_populates="skill",
        cascade="all, delete-orphan"
    )


class ProfileSkill(Base):

    __tablename__ = "profile_skills"


    profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),

        ForeignKey(
            "profiles.id",
            ondelete="CASCADE"
        ),

        primary_key=True
    )


    skill_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),

        ForeignKey(
            "skills.id",
            ondelete="CASCADE"
        ),

        primary_key=True
    )


    level: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="BEGINNER"
    )


    profile = relationship(
        "Profile",
        back_populates="skill_links"
    )


    skill = relationship(
        "Skill",
        back_populates="profile_links"
    )