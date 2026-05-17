"""merge public api and unaccent heads

Revision ID: be2b4d272ebf
Revises: a1b2c3d4e5f6, af290f196186
Create Date: 2026-05-17 09:47:36.035507

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be2b4d272ebf'
down_revision = ('a1b2c3d4e5f6', 'af290f196186')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
