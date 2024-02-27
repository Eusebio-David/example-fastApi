"""add column content to post table

Revision ID: bda8c980f66f
Revises: 2ab3bc1d1408
Create Date: 2024-02-22 19:33:43.395404

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bda8c980f66f'
down_revision: Union[str, None] = '2ab3bc1d1408'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.add_column('posts', sa.Column('content_post',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content_post')
    pass
