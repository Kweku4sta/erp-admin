"""added password to admin table again

Revision ID: 3404d9237680
Revises: bf386b12545a
Create Date: 2025-03-07 13:58:15.847886

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3404d9237680'
down_revision: Union[str, None] = 'bf386b12545a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
