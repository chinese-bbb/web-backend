"""adding new complaint table

Revision ID: 526870fd6eb2
Revises: 1caea2fe0b66
Create Date: 2019-06-07 13:02:49.651052

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '526870fd6eb2'
down_revision = '1caea2fe0b66'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('complaint',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('complaint_body', sa.String(length=2000), nullable=True),
    sa.Column('expected_solution_body', sa.String(length=2000), nullable=True),
    sa.Column('complain_type', sa.String(length=140), nullable=True),
    sa.Column('complain_timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('if_negotiated_by_merchant', sa.Boolean(), nullable=True),
    sa.Column('negotiate_timestamp', sa.DateTime(), nullable=True),
    sa.Column('allow_public', sa.Boolean(), nullable=True),
    sa.Column('allow_contact_by_merchant', sa.Boolean(), nullable=True),
    sa.Column('allow_press', sa.Boolean(), nullable=True),
    sa.Column('item_price', sa.String(length=200), nullable=True),
    sa.Column('item_model', sa.String(length=200), nullable=True),
    sa.Column('trade_info', sa.String(length=2000), nullable=True),
    sa.Column('relatedProducts', sa.String(length=200), nullable=True),
    sa.Column('purchase_timestamp', sa.DateTime(), nullable=True),
    sa.Column('invoce_files', sa.String(length=2000), nullable=True),
    sa.Column('id_files', sa.String(length=2000), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_complaint_complain_timestamp'), 'complaint', ['complain_timestamp'], unique=False)
    op.create_index(op.f('ix_complaint_negotiate_timestamp'), 'complaint', ['negotiate_timestamp'], unique=False)
    op.create_index(op.f('ix_complaint_purchase_timestamp'), 'complaint', ['purchase_timestamp'], unique=False)
    op.create_index(op.f('ix_complaint_user_id'), 'complaint', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_complaint_user_id'), table_name='complaint')
    op.drop_index(op.f('ix_complaint_purchase_timestamp'), table_name='complaint')
    op.drop_index(op.f('ix_complaint_negotiate_timestamp'), table_name='complaint')
    op.drop_index(op.f('ix_complaint_complain_timestamp'), table_name='complaint')
    op.drop_table('complaint')
    # ### end Alembic commands ###