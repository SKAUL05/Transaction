"""empty message

Revision ID: 2a2795ba6662
Revises: 73cdaa1893b7
Create Date: 2022-02-17 14:07:33.366151

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2a2795ba6662"
down_revision = "73cdaa1893b7"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "transactions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("account_no", sa.BigInteger(), nullable=True),
        sa.Column("details", sa.String(length=500), nullable=True),
        sa.Column("date", sa.Date(), nullable=True),
        sa.Column("withdrawal", sa.Float(), nullable=True),
        sa.Column("deposit", sa.Float(), nullable=True),
        sa.Column("balance", sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("transactions")
    # ### end Alembic commands ###
