"""added password again

Revision ID: 870894ee9fd1
Revises: 3404d9237680
Create Date: 2025-03-07 14:01:57.499689

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '870894ee9fd1'
down_revision: Union[str, None] = '3404d9237680'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # add password column to admins table
    op.add_column('admins', sa.Column('password', sa.String(), nullable=True))


def downgrade() -> None:
    # drop password column from admins table
    op.drop_column('admins', 'password')
