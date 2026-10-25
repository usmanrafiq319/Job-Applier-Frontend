# This defines the common SQLAlchemy model base class.	Every database model inherits from Base, allowing SQLAlchemy/Alembic to discover the application's tables.

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass