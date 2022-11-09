"""Added meta/task relationship

Revision ID: 50f16fff837a
Revises: da1cc51f7c3b
Create Date: 2022-11-09 17:07:49.419349

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "50f16fff837a"
down_revision = "da1cc51f7c3b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index(op.f("ix_meta_id"), "meta", ["id"], unique=False)
    op.create_index(op.f("ix_task_id"), "task", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_task_id"), table_name="task")
    op.drop_index(op.f("ix_meta_id"), table_name="meta")
