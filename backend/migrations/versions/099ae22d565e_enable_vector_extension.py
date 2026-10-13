"""enable vector extension

Revision ID: 099ae22d565e
Revises: c5b4a4936ee4
Create Date: 2026-10-12 03:04:05.706228

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '099ae22d565e'
down_revision: Union[str, Sequence[str], None] = 'c5b4a4936ee4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass