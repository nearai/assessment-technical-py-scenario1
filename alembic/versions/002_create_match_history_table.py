"""Create match_history table

Revision ID: 002
Revises: 001
Create Date: 2023-11-01

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create match_history table
    op.create_table(
        'match_history',
        sa.Column('id', UUID(), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('query_id', sa.Text(), nullable=False),
        sa.Column('agent_id', UUID(), nullable=False),
        sa.Column('rank', sa.Integer(), nullable=False),
        sa.Column('selected', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('timestamp', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()'))
    )
    
    # Create foreign key constraint
    op.create_foreign_key(
        'fk_match_history_agent_id',
        'match_history', 'agents',
        ['agent_id'], ['id']
    )
    
    # Create indexes for faster lookups
    op.create_index('idx_match_history_query_id', 'match_history', ['query_id'])
    op.create_index('idx_match_history_agent_id', 'match_history', ['agent_id'])


def downgrade() -> None:
    # Drop match_history table
    op.drop_table('match_history')