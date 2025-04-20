"""add unique on individual

Revision ID: 2d9d240bccf4
Revises: 3f2a856453eb
Create Date: 2025-04-20 12:39:15.046985

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2d9d240bccf4'
down_revision = '3f2a856453eb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('individuo', 'domicilio',
               existing_type=sa.VARCHAR(length=60),
               nullable=False)
    op.alter_column('individuo', 'sexo',
               existing_type=sa.VARCHAR(length=1),
               nullable=False)
    op.alter_column('individuo', 'raca_cor',
               existing_type=sa.VARCHAR(length=60),
               nullable=False)
    op.alter_column('individuo', 'etnia',
               existing_type=sa.VARCHAR(length=60),
               nullable=False)
    op.alter_column('individuo', 'celular',
               existing_type=sa.VARCHAR(length=15),
               nullable=False)
    op.alter_column('individuo', 'email',
               existing_type=sa.VARCHAR(length=60),
               nullable=False)
    op.alter_column('individuo', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.create_unique_constraint(None, 'individuo', ['cns'])
    op.create_unique_constraint(None, 'individuo', ['cpf'])


def downgrade() -> None:
    op.drop_constraint(None, 'individuo', type_='unique')
    op.drop_constraint(None, 'individuo', type_='unique')
    op.alter_column('individuo', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('individuo', 'email',
               existing_type=sa.VARCHAR(length=60),
               nullable=True)
    op.alter_column('individuo', 'celular',
               existing_type=sa.VARCHAR(length=15),
               nullable=True)
    op.alter_column('individuo', 'etnia',
               existing_type=sa.VARCHAR(length=60),
               nullable=True)
    op.alter_column('individuo', 'raca_cor',
               existing_type=sa.VARCHAR(length=60),
               nullable=True)
    op.alter_column('individuo', 'sexo',
               existing_type=sa.VARCHAR(length=1),
               nullable=True)
    op.alter_column('individuo', 'domicilio',
               existing_type=sa.VARCHAR(length=60),
               nullable=True)
