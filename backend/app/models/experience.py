import uuid

from datetime import date

from pgvector.sqlalchemy import VECTOR

from sqlalchemy import (
    Boolean,
    Date,
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


class Experience(
    TimestampMixin,
    Base
):

    __tablename__ = "experiences"


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


    company: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )


    role: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )


    start_date: Mapped[
        date | None
    ] = mapped_column(
        Date,
        nullable=True
    )


    end_date: Mapped[
        date | None
    ] = mapped_column(
        Date,
        nullable=True
    )


    currently_working: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
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
        back_populates="experiences"
    )