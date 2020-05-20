"""empty message

Revision ID: 3c3d89862429
Revises: 
Create Date: 2020-05-19 18:17:32.658850

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c3d89862429'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('state_collections',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('creator_id', sa.String(length=20), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('team_id', sa.String(length=20), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('state_items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('creator_id', sa.String(length=20), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('collection_id', sa.Integer(), nullable=True),
    sa.Column('team_id', sa.String(length=20), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('value', sa.String(length=100), nullable=True),
    sa.Column('default_value', sa.String(length=100), nullable=True),
    sa.Column('label', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['collection_id'], ['state_collections.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.String(length=20), nullable=False),
    sa.Column('team_id', sa.String(length=20), nullable=False),
    sa.Column('current_state_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['current_state_id'], ['state_collections.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('collection_permissions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('collection_id', sa.Integer(), nullable=True),
    sa.Column('permission', sa.String(length=10), nullable=True),
    sa.ForeignKeyConstraint(['collection_id'], ['state_collections.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('item_permissions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('item_id', sa.Integer(), nullable=True),
    sa.Column('permission', sa.String(length=10), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['state_items.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('item_permissions')
    op.drop_table('collection_permissions')
    op.drop_table('users')
    op.drop_table('state_items')
    op.drop_table('state_collections')
    # ### end Alembic commands ###
