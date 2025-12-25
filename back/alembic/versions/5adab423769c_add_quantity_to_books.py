"""add quantity to books

Revision ID: 5adab423769c
Revises: 0faa85c312af
Create Date: 2025-xx-xx
"""

from alembic import op
import sqlalchemy as sa


# === OBLIGATOIRE ===
revision = "5adab423769c"
down_revision = "0faa85c312af"
branch_labels = None
depends_on = None

def upgrade():
    op.add_column(
        'books',
        sa.Column(
            'quantity',
            sa.Integer(),
            nullable=False,
            server_default='1'
        )
    )

    # optionnel mais recommandé : retirer le default après
    op.alter_column('books', 'quantity', server_default=None)


def downgrade():
    op.drop_column('books', 'quantity')
