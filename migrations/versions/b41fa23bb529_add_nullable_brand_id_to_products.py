"""Add nullable brand_id to products

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
        # Step 1: Add the column as nullable
        batch_op.add_column(sa.Column('brand_id', sa.Integer(), nullable=True))
        # Step 2: Create the foreign key
        batch_op.create_foreign_key('fk_products_brand_id', 'brands', ['brand_id'], ['id'])

    # Step 3: Populate brand_id for existing rows (set to default brand_id, e.g., 1)
    op.execute("UPDATE products SET brand_id = 1 WHERE brand_id IS NULL")

    # Step 4: Set NOT NULL constraint
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.alter_column('brand_id', nullable=False)

def downgrade():
    with op.batch_alter_table('products', schema=None) as batch_op:
        # Step 1: Drop the NOT NULL constraint
        batch_op.alter_column('brand_id', nullable=True)
        # Step 2: Drop the foreign key
        batch_op.drop_constraint('fk_products_brand_id', type_='foreignkey')
        # Step 3: Drop the column
        batch_op.drop_column('brand_id')