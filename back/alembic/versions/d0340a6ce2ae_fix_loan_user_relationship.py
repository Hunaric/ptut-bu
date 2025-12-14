from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = 'd0340a6ce2ae'
down_revision = 'f2d8610a5d7d'
branch_labels = None
depends_on = None

def upgrade():
    # Supprimer la colonne loan_id de users
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_column("loan_id")

    # Modifier le type de user_id dans loans pour qu'il soit UUID
    with op.batch_alter_table("loans") as batch_op:
        batch_op.alter_column(
            "user_id",
            existing_type=sa.INTEGER(),
            type_=postgresql.UUID(),
            existing_nullable=False
        )

def downgrade():
    # Rollback si besoin
    with op.batch_alter_table("loans") as batch_op:
        batch_op.alter_column(
            "user_id",
            existing_type=postgresql.UUID(),
            type_=sa.INTEGER(),
            existing_nullable=False
        )
    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(sa.Column("loan_id", sa.INTEGER(), nullable=True))
