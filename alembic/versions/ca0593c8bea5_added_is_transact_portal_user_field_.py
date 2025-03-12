"""added is_transact_portal_user  field from  users table

Revision ID: ca0593c8bea5
Revises: 574f82ec5b09
Create Date: 2025-03-11 13:04:24.300961

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ca0593c8bea5'
down_revision: Union[str, None] = '574f82ec5b09'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('admins', 'reset_password',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('companies', 'transactional_currency',
               existing_type=sa.VARCHAR(length=3),
               nullable=True)
    op.add_column('users', sa.Column('is_transact_portal_user', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_transact_portal_user')
    op.alter_column('companies', 'transactional_currency',
               existing_type=sa.VARCHAR(length=3),
               nullable=True)
    op.alter_column('admins', 'reset_password',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    # ### end Alembic commands ###
