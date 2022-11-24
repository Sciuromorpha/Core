"""Add extension crypto

Revision ID: 2342d5694a7e
Revises: 50f16fff837a
Create Date: 2022-11-09 19:16:23.658636

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2342d5694a7e'
down_revision = '50f16fff837a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto";')


def downgrade() -> None:
    op.execute('DROP EXTENSION IF EXISTS "pgcrypto";')
