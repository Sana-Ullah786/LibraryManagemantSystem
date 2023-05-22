"""Create_Status_Fk4

Revision ID: 94a2bc55b61f
Revises: 5ceb6c1b8b27
Create Date: 2023-05-15 16:58:11.687387

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "94a2bc55b61f"
down_revision = "5ceb6c1b8b27"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("copy", "status", nullable=False, new_column_name="status_id")
    pass


def downgrade() -> None:
    op.alter_column("copy", "status_id", nullable=False, new_column_name="status")
    pass
