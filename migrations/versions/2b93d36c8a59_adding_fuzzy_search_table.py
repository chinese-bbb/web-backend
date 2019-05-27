"""adding fuzzy search table

Revision ID: 2b93d36c8a59
Revises: a98114a99a51
Create Date: 2019-05-26 23:17:57.622995

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b93d36c8a59'
down_revision = 'a98114a99a51'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fuzzy_search_raw',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('keyword', sa.String(length=140), nullable=True),
    sa.Column('storage', sa.String(length=10000), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fuzzy_search_raw')
    # ### end Alembic commands ###
