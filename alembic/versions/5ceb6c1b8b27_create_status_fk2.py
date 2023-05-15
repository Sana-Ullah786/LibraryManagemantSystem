"""Create_Status_Fk2

Revision ID: 5ceb6c1b8b27
Revises: b4fe61fdb743
Create Date: 2023-05-15 16:34:14.802013

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "5ceb6c1b8b27"
down_revision = "b4fe61fdb743"
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
