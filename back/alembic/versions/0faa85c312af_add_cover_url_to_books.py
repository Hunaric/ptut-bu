"""add cover_url to books

Revision ID: 0faa85c312af
Revises: d0340a6ce2ae
Create Date: 2025-12-22 10:10:57.544544
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0faa85c312af"
down_revision = "d0340a6ce2ae"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "books",
        sa.Column("cover_url", sa.String(length=500), nullable=True)
    )


def downgrade():
    op.drop_column("books", "cover_url")
