"""Add brand_id to products

Revision ID: b41fa23bb529
Revises: 8e8cf978208f
Create Date: 2025-07-29 21:47:29.706093
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'b41fa23bb529'
down_revision = '8e8cf978208f'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('products', schema=None) as batch_op:
        # Add the brand_id column as non-nullable and create the foreign key
        batch_op.add_column(sa.Column('brand_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key('fk_products_brand_id', 'brands', ['brand_id'], ['id'])

def downgrade():
    with op.batch_alter_table('products', schema=None) as batch_op:
        # Drop the foreign key
        batch_op.drop_constraint('fk_products_brand_id', type_='foreignkey')
        # Drop the brand_id column
        batch_op.drop_column('brand_id')