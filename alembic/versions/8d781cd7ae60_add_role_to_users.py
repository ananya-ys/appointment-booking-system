"""add role to users

Revision ID: 8d781cd7ae60
Revises: f911befc7374
Create Date: 2026-02-02 17:16:18.561242

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8d781cd7ae60'
down_revision: Union[str, Sequence[str], None] = 'f911befc7374'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 1. Add column with a DEFAULT so existing rows get a value
    op.add_column(
        'users',
        sa.Column(
            'role',
            sa.String(),
            nullable=False,
            server_default='customer'
        )
    )

    # 2. (Optional but clean) Remove the server default after backfill
    op.alter_column(
        'users',
        'role',
        server_default=None
    )

def downgrade() -> None:
    op.drop_column('users', 'role')

