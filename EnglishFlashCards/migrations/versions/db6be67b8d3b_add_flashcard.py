"""Add FlashCard

Revision ID: db6be67b8d3b
Revises: 
Create Date: 2025-03-21 18:11:40.158583

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'db6be67b8d3b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('flash_card', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('flash_card', schema=None) as batch_op:
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###
