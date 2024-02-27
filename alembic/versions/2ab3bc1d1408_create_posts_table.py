"""create posts table

Revision ID: 2ab3bc1d1408
Revises: 
Create Date: 2024-02-22 19:12:23.837170

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2ab3bc1d1408'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
   op.create_table('posts', sa.Column('id_post', sa.Integer(), nullable=False, 
                                      primary_key=True),sa.Column('title_post', sa.String(), nullable=False))


def downgrade():
    op.drop_table('posts')

    pass
