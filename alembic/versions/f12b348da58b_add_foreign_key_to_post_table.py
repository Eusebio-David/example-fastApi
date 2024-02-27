"""add foreign-key to post table

Revision ID: f12b348da58b
Revises: 83384a9779e0
Create Date: 2024-02-26 16:16:44.188367

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f12b348da58b'
down_revision: Union[str, None] = '83384a9779e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users',
                          local_cols=['owner_id'], remote_cols=['id_user'], ondelete="CASCADE")

    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')

    pass
