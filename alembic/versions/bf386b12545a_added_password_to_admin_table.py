"""added password to admin table

Revision ID: bf386b12545a
Revises: 2d2cb9dbb154
Create Date: 2025-03-07 13:55:22.621409

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bf386b12545a'
down_revision: Union[str, None] = '2d2cb9dbb154'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
