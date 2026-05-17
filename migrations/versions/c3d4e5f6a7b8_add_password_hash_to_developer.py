"""add password_hash to api_key_developer

Revision ID: c3d4e5f6a7b8
Revises: be2b4d272ebf
Create Date: 2026-05-17 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'c3d4e5f6a7b8'
down_revision = 'be2b4d272ebf'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'api_key_developer',
        sa.Column('password_hash', sa.String(200), nullable=True),
    )


def downgrade() -> None:
    op.drop_column('api_key_developer', 'password_hash')
