"""Create_Status_Fk

Revision ID: 0a8c158bb3ab
Revises:
Create Date: 2023-05-15 13:41:38.426178

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, uscsed by Alembic.
revision = "0a8c158bb3ab"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Drop the 'status' column from the 'copy' table
    op.drop_column("copy", "status")

    # Add the new 'status' column with foreign key constraint
    op.add_column(
        "copy", sa.Column("status", sa.Integer(), nullable=False, server_default="1")
    )

    # Create the foreign key constraint
    op.create_foreign_key("fk_copy_status", "copy", "status", ["status"], ["id"])


def downgrade():
    # Drop the foreign key constraint
    op.drop_constraint("fk_copy_status", "copy", type_="foreignkey")

    # Drop the 'status' column from the 'copy' table
    op.drop_column("copy", "status")
