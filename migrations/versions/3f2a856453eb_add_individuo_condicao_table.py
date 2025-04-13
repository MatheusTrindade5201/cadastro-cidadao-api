"""add individuo condicao table

Revision ID: 3f2a856453eb
Revises: 99eb71135e74
Create Date: 2025-04-13 14:45:34.298331

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f2a856453eb'
down_revision = '99eb71135e74'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('individuo_condicao',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('individuo_id', sa.Integer(), nullable=True),
                    sa.Column('condicao', sa.String(length=60), nullable=True),
                    sa.ForeignKeyConstraint(['individuo_id'], ['individuo.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('individuo_condicao')
