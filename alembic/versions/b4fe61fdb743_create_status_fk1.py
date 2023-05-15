"""Create_Status_Fk1

Revision ID: b4fe61fdb743
Revises: 0a8c158bb3ab
Create Date: 2023-05-15 16:26:51.085155

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "b4fe61fdb743"
down_revision = "0a8c158bb3ab"
branch_labels = None
depends_on = None


def upgrade():
    # Drop the 'status' column from the 'copy' table
    op.drop_column("copy", "status")

    # Add the new 'status' column with foreign key constraint
    op.add_column(
        "copy",
        sa.Column(
            "status",
            sa.Integer,
            sa.ForeignKey("status.id", name="fk_copy_status"),
            nullable=False,
            server_default="1",
        ),
    )


def downgrade():
    # Drop the foreign key constraint
    op.drop_constraint("fk_copy_status", "copy", type_="foreignkey")

    # Drop the 'status' column from the 'copy' table
    op.drop_column("copy", "status")
