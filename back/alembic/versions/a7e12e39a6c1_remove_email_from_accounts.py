"""remove email from accounts

Revision ID: a7e12e39a6c1
Revises: 
Create Date: 2025-12-05 13:06:59.233317
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7e12e39a6c1'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()

    # Drop indexes safely if they exist
    for table, index in [
        ('books', 'ix_books_id'),
        ('persons', 'ix_persons_email'),
        ('persons', 'ix_persons_id'),
        ('accounts', 'ix_accounts_email'),
        ('accounts', 'ix_accounts_id'),
        ('users', 'ix_users_id')
    ]:
        result = conn.execute(
            sa.text(f"SELECT to_regclass('public.{index}')")
        ).scalar()
        if result is not None:
            op.drop_index(index, table_name=table)

    # Drop tables safely using CASCADE for dependent objects
    for table in ['books', 'persons', 'accounts', 'roles', 'permissions', 'role_permissions', 'users']:
        exists = conn.execute(
            sa.text(f"""
                SELECT EXISTS (
                    SELECT 1 FROM information_schema.tables 
                    WHERE table_schema='public' AND table_name='{table}'
                )
            """)
        ).scalar()
        if exists:
            op.execute(sa.text(f'DROP TABLE {table} CASCADE'))


def downgrade() -> None:
    """Downgrade schema."""
    # Recreate tables and indexes exactly as before
    op.create_table('users',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('email_etablissement', sa.VARCHAR(), nullable=False),
        sa.Column('username', sa.VARCHAR(), nullable=False),
        sa.Column('hashed_password', sa.VARCHAR(), nullable=False),
        sa.Column('is_active', sa.BOOLEAN(), nullable=True),
        sa.Column('role_id', sa.INTEGER(), nullable=True),
        sa.Column('person_id', sa.INTEGER(), nullable=True),
        sa.ForeignKeyConstraint(['person_id'], ['persons.id'], name='users_person_id_fkey'),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], name='users_role_id_fkey'),
        sa.PrimaryKeyConstraint('id', name='users_pkey'),
        sa.UniqueConstraint('email_etablissement', name='users_email_etablissement_key'),
        sa.UniqueConstraint('username', name='users_username_key')
    )
    op.create_index('ix_users_id', 'users', ['id'], unique=False)

    op.create_table('role_permissions',
        sa.Column('role_id', sa.INTEGER(), nullable=True),
        sa.Column('permission_id', sa.INTEGER(), nullable=True),
        sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], name='role_permissions_permission_id_fkey'),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], name='role_permissions_role_id_fkey')
    )

    op.create_table('permissions',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('name', sa.VARCHAR(), nullable=False),
        sa.Column('description', sa.VARCHAR(), nullable=True),
        sa.PrimaryKeyConstraint('id', name='permissions_pkey'),
        sa.UniqueConstraint('name', name='permissions_name_key')
    )

    op.create_table('roles',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('name', sa.VARCHAR(), nullable=False),
        sa.Column('description', sa.VARCHAR(), nullable=True),
        sa.PrimaryKeyConstraint('id', name='roles_pkey'),
        sa.UniqueConstraint('name', name='roles_name_key')
    )

    op.create_table('accounts',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('sexe', sa.VARCHAR(), nullable=False),
        sa.Column('nom', sa.VARCHAR(), nullable=False),
        sa.Column('prenom', sa.VARCHAR(), nullable=False),
        sa.Column('etablissement', sa.VARCHAR(), nullable=False),
        sa.Column('numero', sa.VARCHAR(), nullable=True),
        sa.Column('rue', sa.VARCHAR(), nullable=True),
        sa.Column('boite_postale', sa.VARCHAR(), nullable=True),
        sa.Column('code_postal', sa.VARCHAR(), nullable=True),
        sa.Column('ville', sa.VARCHAR(), nullable=True),
        sa.Column('codex_ville', sa.VARCHAR(), nullable=True),
        sa.Column('pays', sa.VARCHAR(), nullable=True),
        sa.Column('email', sa.VARCHAR(), nullable=False),
        sa.Column('telephone', sa.VARCHAR(), nullable=True),
        sa.PrimaryKeyConstraint('id', name='accounts_pkey')
    )
    op.create_index('ix_accounts_id', 'accounts', ['id'], unique=True)
    op.create_index('ix_accounts_email', 'accounts', ['email'], unique=True)

    op.create_table('persons',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('sexe', sa.VARCHAR(), nullable=False),
        sa.Column('nom', sa.VARCHAR(), nullable=False),
        sa.Column('prenom', sa.VARCHAR(), nullable=False),
        sa.Column('etablissement', sa.VARCHAR(), nullable=False),
        sa.Column('numero', sa.VARCHAR(), nullable=True),
        sa.Column('rue', sa.VARCHAR(), nullable=True),
        sa.Column('boite_postale', sa.VARCHAR(), nullable=True),
        sa.Column('code_postal', sa.VARCHAR(), nullable=True),
        sa.Column('ville', sa.VARCHAR(), nullable=True),
        sa.Column('codex_ville', sa.VARCHAR(), nullable=True),
        sa.Column('pays', sa.VARCHAR(), nullable=True),
        sa.Column('email', sa.VARCHAR(), nullable=False),
        sa.Column('telephone', sa.VARCHAR(), nullable=True),
        sa.PrimaryKeyConstraint('id', name='persons_pkey')
    )
    op.create_index('ix_persons_id', 'persons', ['id'], unique=False)
    op.create_index('ix_persons_email', 'persons', ['email'], unique=True)

    op.create_table('books',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('title', sa.VARCHAR(), nullable=False),
        sa.Column('author', sa.VARCHAR(), nullable=True),
        sa.PrimaryKeyConstraint('id', name='books_pkey')
    )
    op.create_index('ix_books_id', 'books', ['id'], unique=False)
