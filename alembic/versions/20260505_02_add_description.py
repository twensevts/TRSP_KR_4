"""add description to products

Revision ID: 20260505_02
Revises: 20260505_01
Create Date: 2026-05-05 00:00:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260505_02"
down_revision = "20260505_01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "products",
        sa.Column(
            "description",
            sa.String(length=500),
            nullable=False,
            server_default="",
        ),
    )
    
    # Add two sample records as required by task 9.1
    op.execute(
        """
        INSERT INTO products (title, price, count, description) 
        VALUES 
        ('Laptop', 999.99, 5, 'High performance laptop for work and gaming'),
        ('Wireless Mouse', 29.99, 50, 'Ergonomic wireless mouse with USB receiver')
        """
    )


def downgrade() -> None:
    op.drop_column("products", "description")
