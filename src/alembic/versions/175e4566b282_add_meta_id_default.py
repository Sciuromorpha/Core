"""Add meta.id Default

Revision ID: 175e4566b282
Revises: 2342d5694a7e
Create Date: 2022-11-09 19:28:50.999080

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '175e4566b282'
down_revision = '2342d5694a7e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER TABLE IF EXISTS public.meta ALTER COLUMN id SET DEFAULT gen_random_uuid();")


def downgrade() -> None:
    op.execute("ALTER TABLE IF EXISTS public.meta ALTER COLUMN id DROP DEFAULT;")
