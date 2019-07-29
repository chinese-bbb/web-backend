"""add is_founder field to Users table

Revision ID: f87268b0584c
Revises: 4e78392ab360
Create Date: 2019-07-25 10:54:58.548030

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f87268b0584c'
down_revision = '4e78392ab360'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_founder', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'is_founder')
    # ### end Alembic commands ###
