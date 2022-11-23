"""Add meta.origin_url index

Revision ID: 612b76967a81
Revises: 175e4566b282
Create Date: 2022-11-23 16:35:30.670976

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "612b76967a81"
down_revision = "175e4566b282"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index(op.f("ix_meta_origin_url"), "meta", ["origin_url"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_meta_origin_url"), table_name="meta")
