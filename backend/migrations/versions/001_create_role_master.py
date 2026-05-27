"""create role_master table

Revision ID: 001
Revises:
Create Date: 2026-05-26

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

ROLES = [
    "Interviewer", "Recruiter", "PMO", "PracticeLead", "Lead",
    "TowerLead", "SLBULead", "NALead", "RecruiterLead", "BUAdmin",
    "PracticeAdmin", "Admin", "ReferralSPOC", "ReferralUser",
]


def upgrade() -> None:
    op.create_table(
        "role_master",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("role_name", sa.String(100), nullable=False, unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    # Seed roles
    op.bulk_insert(
        sa.table("role_master", sa.column("role_name", sa.String)),
        [{"role_name": r} for r in ROLES],
    )


def downgrade() -> None:
    op.drop_table("role_master")
