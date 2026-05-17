"""add public api tables

Revision ID: a1b2c3d4e5f6
Revises: 2d9d240bccf4
Create Date: 2026-05-17

"""
from alembic import op
import sqlalchemy as sa

revision = 'a1b2c3d4e5f6'
down_revision = '2d9d240bccf4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'api_key_developer',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=120), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('status', sa.SmallInteger(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
    )

    op.create_table(
        'api_key',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('developer_id', sa.Integer(), nullable=False),
        sa.Column('prefix', sa.String(length=16), nullable=False),
        sa.Column('key_hash', sa.String(length=200), nullable=False),
        sa.Column('status', sa.String(length=10), nullable=False, server_default='active'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('last_used_at', sa.DateTime(), nullable=True),
        sa.Column('revoked_at', sa.DateTime(), nullable=True),
        sa.Column('revoked_by', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['developer_id'], ['api_key_developer.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['revoked_by'], ['user.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_api_key_prefix', 'api_key', ['prefix'])

    op.create_table(
        'api_key_usage_log',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('api_key_id', sa.Integer(), nullable=False),
        sa.Column('endpoint', sa.String(length=200), nullable=False),
        sa.Column('method', sa.String(length=10), nullable=False),
        sa.Column('status_code', sa.Integer(), nullable=False),
        sa.Column('requested_at', sa.DateTime(), nullable=False),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.ForeignKeyConstraint(['api_key_id'], ['api_key.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_api_key_usage_log_api_key_id', 'api_key_usage_log', ['api_key_id'])

    op.create_table(
        'developer_session',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('developer_id', sa.Integer(), nullable=False),
        sa.Column('token_hash', sa.String(length=200), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('used_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['developer_id'], ['api_key_developer.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('token_hash'),
    )


def downgrade() -> None:
    op.drop_table('developer_session')
    op.drop_index('ix_api_key_usage_log_api_key_id', table_name='api_key_usage_log')
    op.drop_table('api_key_usage_log')
    op.drop_index('ix_api_key_prefix', table_name='api_key')
    op.drop_table('api_key')
    op.drop_table('api_key_developer')
