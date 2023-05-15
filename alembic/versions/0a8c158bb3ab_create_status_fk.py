"""Create_Status_Fk

Revision ID: 0a8c158bb3ab
Revises:
Create Date: 2023-05-15 13:41:38.426178

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "0a8c158bb3ab"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add the "status" column to the "copy" table
    op.add_column("copy", sa.Column("status", sa.String(length=50), nullable=True))

    # Create the foreign key relationship
    op.create_foreign_key("fk_copy_status", "copy", "status", ["status"], ["id"])

    pass


def downgrade() -> None:
    # Remove the foreign key relationship
    op.drop_constraint("fk_copy_status", "copy", type_="foreignkey")

    # Remove the "status" column from the "copy" table
    op.drop_column("copy", "status")
    pass
