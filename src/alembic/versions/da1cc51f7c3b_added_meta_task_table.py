"""Create meta/task table

Revision ID: da1cc51f7c3b
Revises: 
Create Date: 2022-11-09 10:29:33.523273

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'da1cc51f7c3b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('meta',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('data', postgresql.JSONB(none_as_null=True), nullable=True),
    sa.Column('origin_url', sa.String(), nullable=True),
    sa.Column('process_tag', postgresql.ARRAY(sa.String(), dimensions=1), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('task',
    sa.Column('id', sa.Integer(), sa.Identity(always=False, cycle=True), nullable=False),
    sa.Column('meta_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('worker', sa.String(), nullable=True),
    sa.Column('param', postgresql.BYTEA(), nullable=True),
    sa.Column('status', postgresql.ENUM('pending', 'waiting', 'running', 'success', 'failed', name='task-status'), nullable=True),
    sa.ForeignKeyConstraint(['meta_id'], ['meta.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('task')
    op.drop_table('meta')
