"""remove email from accounts

Revision ID: ef03c0b05857
Revises: a7e12e39a6c1
Create Date: 2025-12-05 13:09:59.371431

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ef03c0b05857'
down_revision: Union[str, Sequence[str], None] = 'a7e12e39a6c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column('accounts', 'email')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('accounts', sa.Column('email', sa.String(), nullable=False))
