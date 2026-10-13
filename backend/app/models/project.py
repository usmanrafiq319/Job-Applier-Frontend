import uuid

from pgvector.sqlalchemy import VECTOR

from sqlalchemy import (
    ForeignKey,
    String,
    Text,
)

from sqlalchemy.dialects.postgresql import (
    ARRAY,
    UUID,
)

from sqlalchemy.ext.mutable import MutableList

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.core.constants import EMBEDDING_DIMENSION
from app.db.base import Base
from app.models.mixins import TimestampMixin


class Project(
    TimestampMixin,
    Base
):

    __tablename__ = "projects"


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
        String(200),
        nullable=False
    )


    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )


    technologies: Mapped[list[str]] = mapped_column(

        MutableList.as_mutable(
            ARRAY(
                String(100)
            )
        ),

        nullable=False,
        default=list
    )


    project_url: Mapped[
        str | None
    ] = mapped_column(
        String(500),
        nullable=True
    )


    github_url: Mapped[
        str | None
    ] = mapped_column(
        String(500),
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


    profile = relationship(
        "Profile",
        back_populates="projects"
    )