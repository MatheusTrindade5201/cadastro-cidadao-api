"""enable unaccent extension

Revision ID: af290f196186
Revises: 2d9d240bccf4
Create Date: 2025-10-25 10:58:30.771256

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af290f196186'
down_revision = '2d9d240bccf4'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS unaccent;")


def downgrade():
    op.execute("DROP EXTENSION IF EXISTS unaccent;")