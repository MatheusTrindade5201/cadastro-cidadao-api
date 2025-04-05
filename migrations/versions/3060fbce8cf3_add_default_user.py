"""add default user

Revision ID: 3060fbce8cf3
Revises: ff55876fcfef
Create Date: 2025-04-05 08:56:36.940076

"""
from os import getenv

from alembic import op
from sqlalchemy import text

from utils.providers.hash_provider import generate_hash

# revision identifiers, used by Alembic.
revision = '3060fbce8cf3'
down_revision = 'ff55876fcfef'
branch_labels = None
depends_on = None

name = getenv("USER_NAME", default="Admin")
email = getenv("USER_EMAIL", default="Admin@admin.com")
password = getenv("USER_PASSWORD", default="123456789")
zoomer_type = getenv("USER_TYPE", default="ZOOM")

def upgrade() -> None:
    connection = op.get_bind()

    insert_user_query = text(
        """
        INSERT INTO "user" (name, email, password, role, status,  created_at)
        VALUES (:name, :email, :password, :role, 0, NOW())
        RETURNING id;
        """
    ).bindparams(
        name=name,
        email=email,
        password=generate_hash(password),
        role="Zoomer",
    )

    connection.execute(insert_user_query)


def downgrade() -> None:
    connection = op.get_bind()

    op.execute(
        f"""
        DELETE FROM "user" WHERE email = '{email}';
        """
    )
