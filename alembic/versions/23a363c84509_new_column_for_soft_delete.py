"""New column for soft delete

Revision ID: 23a363c84509
Revises: 94a2bc55b61f
Create Date: 2023-05-22 19:37:26.940284

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "23a363c84509"
down_revision = "94a2bc55b61f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "user",
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default="False"),
    )
    op.add_column(
        "status",
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default="False"),
    )
    op.add_column(
        "language",
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default="False"),
    )
    op.add_column(
        "genre",
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default="False"),
    )
    op.add_column(
        "copy",
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default="False"),
    )
    op.add_column(
        "borrowed",
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default="False"),
    )
    op.add_column(
        "book_genre",
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default="False"),
    )
    op.add_column(
        "book_author",
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default="False"),
    )
    op.add_column(
        "book",
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default="False"),
    )
    op.add_column(
        "author",
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default="False"),
    )


def downgrade() -> None:
    op.drop_column("user", "is_deleted")
    op.drop_column("status", "is_deleted")
    op.drop_column("language", "is_deleted")
    op.drop_column("genre", "is_deleted")
    op.drop_column("copy", "is_deleted")
    op.drop_column("borrowed", "is_deleted")
    op.drop_column("book_genre", "is_deleted")
    op.drop_column("book_author", "is_deleted")
    op.drop_column("book", "is_deleted")
    op.drop_column("author", "is_deleted")
