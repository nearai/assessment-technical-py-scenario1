"""Create agents table

Revision ID: 001
Revises: 
Create Date: 2023-11-01

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create extension for UUID generation if it doesn't exist
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    
    # Create agents table
    op.create_table(
        'agents',
        sa.Column('id', UUID(), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('capabilities', sa.Text(), nullable=False),
        sa.Column('historical_performance', sa.Float(), nullable=False, server_default=sa.text('0.5')),
        sa.Column('availability', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('image_url', sa.Text(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()'))
    )


def downgrade() -> None:
    # Drop agents table
    op.drop_table('agents')