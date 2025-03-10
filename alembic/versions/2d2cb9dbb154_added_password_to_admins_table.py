"""added password to admins table

Revision ID: 2d2cb9dbb154
Revises: 85f0706ce83b
Create Date: 2025-03-07 13:49:29.894387

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2d2cb9dbb154'
down_revision: Union[str, None] = '85f0706ce83b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # add password column to admins table
    op.add_column('admins', sa.Column('password', sa.String(), nullable=True))
    


def downgrade() -> None:
    # drop password column from admins table
    op.drop_column('admins', 'password')
    
