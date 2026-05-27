"""create export history index and additional constraints

Revision ID: 011
Revises: 010
Create Date: 2024-01-12
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "011"
down_revision: Union[str, None] = "010"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    from alembic import op as _op
    from sqlalchemy import inspect
    from sqlalchemy.engine import Connection

    bind = op.get_bind()
    inspector = inspect(bind)
    existing = [idx['name'] for idx in inspector.get_indexes('export_history')]

    if 'ix_export_history_created_by' not in existing:
        op.create_index('ix_export_history_created_by', 'export_history', ['created_by'], unique=False)
    if 'ix_export_history_created_at' not in existing:
        op.create_index('ix_export_history_created_at', 'export_history', ['created_at'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_export_history_created_at', table_name='export_history')
    op.drop_index('ix_export_history_created_by', table_name='export_history')
