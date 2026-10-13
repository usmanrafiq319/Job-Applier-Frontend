import uuid

from datetime import date

from sqlalchemy import (
    Date,
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


class Education(
    TimestampMixin,
    Base
):

    __tablename__ = "educations"


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


    degree: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )


    institute: Mapped[str] = mapped_column(
        String(250),
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


    cgpa: Mapped[
        str | None
    ] = mapped_column(
        String(30),
        nullable=True
    )


    profile = relationship(
        "Profile",
        back_populates="educations"
    )