"""add user table

Revision ID: 83384a9779e0
Revises: bda8c980f66f
Create Date: 2024-02-22 19:48:09.942095

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '83384a9779e0'
down_revision: Union[str, None] = 'bda8c980f66f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('users', 
                    sa.Column('id_user',sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id_user'),
                    sa.UniqueConstraint('email'))

    pass


def downgrade():
    op.drop_table('usuarios')
    pass
