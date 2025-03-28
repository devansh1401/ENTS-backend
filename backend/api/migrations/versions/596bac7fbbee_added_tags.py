"""added tags

Revision ID: 596bac7fbbee
Revises: 76c91a8730cb
Create Date: 2025-01-21 17:30:36.277304

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "596bac7fbbee"
down_revision = "76c91a8730cb"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "tag",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "cell_tag",
        sa.Column("cell_id", sa.Integer(), nullable=False),
        sa.Column("tag_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["cell_id"],
            ["cell.id"],
        ),
        sa.ForeignKeyConstraint(
            ["tag_id"],
            ["tag.id"],
        ),
        sa.PrimaryKeyConstraint("cell_id", "tag_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("cell_tag")
    op.drop_table("tag")
    # ### end Alembic commands ###
