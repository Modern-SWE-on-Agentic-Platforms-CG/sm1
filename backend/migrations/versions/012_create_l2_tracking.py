"""create l2 tracking tables

Revision ID: 012
Revises: 011
Create Date: 2024-01-12
"""
from alembic import op
import sqlalchemy as sa

revision = '012'
down_revision = '011'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'l2_select_data',
        sa.Column('l2_select_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('candidate_detail_id', sa.Integer, sa.ForeignKey('candidate_detail.candidate_detail_id', ondelete='CASCADE'), nullable=False),
        sa.Column('l2_interviewer_id', sa.Integer, sa.ForeignKey('employee_master.emp_id', ondelete='SET NULL'), nullable=True),
        sa.Column('l2_interview_date', sa.Date, nullable=True),
        sa.Column('l2_feedback', sa.Text, nullable=True),
        sa.Column('l2_recommendation', sa.String(50), nullable=True),
        sa.Column('l2_status', sa.String(50), nullable=True, server_default='Pending'),
        sa.Column('aging_days', sa.Integer, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    op.create_index('ix_l2_select_data_candidate', 'l2_select_data', ['candidate_detail_id'])
    op.create_index('ix_l2_select_data_status', 'l2_select_data', ['l2_status'])


def downgrade() -> None:
    op.drop_index('ix_l2_select_data_status', 'l2_select_data')
    op.drop_index('ix_l2_select_data_candidate', 'l2_select_data')
    op.drop_table('l2_select_data')
