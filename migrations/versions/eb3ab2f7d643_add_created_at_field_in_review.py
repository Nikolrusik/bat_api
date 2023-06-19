"""Add created_at field in Review

Revision ID: eb3ab2f7d643
Revises: 0ffe2f11cda5
Create Date: 2023-06-19 20:47:44.335355

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb3ab2f7d643'
down_revision = '0ffe2f11cda5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('review', sa.Column('created_at', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('review', 'created_at')
    # ### end Alembic commands ###