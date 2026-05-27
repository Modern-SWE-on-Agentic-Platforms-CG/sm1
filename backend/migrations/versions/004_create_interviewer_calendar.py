"""create interviewer_calendar

Revision ID: 004
Revises: 003
Create Date: 2026-05-26

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "004"
down_revision: Union[str, None] = "003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "interviewer_calendar",
        sa.Column("interviewer_calendar_id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column(
            "emp_id", sa.BigInteger(),
            sa.ForeignKey("employee_master.emp_id"), nullable=False
        ),
        sa.Column("skill_id", sa.Integer(), sa.ForeignKey("technology_master.id")),
        sa.Column("slot_date", sa.Date(), nullable=False),
        sa.Column("from_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("to_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "slot_status", sa.String(20), nullable=False, server_default="Available"
        ),
        sa.Column("is_weekend_drive", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_by", sa.String(255)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.CheckConstraint(
            "slot_status IN ('Available','Booked','Interviewed','Pending')",
            name="ck_slot_status",
        ),
    )
    op.create_index("ix_interviewer_calendar_emp_date", "interviewer_calendar", ["emp_id", "slot_date"])
    op.create_index("ix_interviewer_calendar_emp_status", "interviewer_calendar", ["emp_id", "slot_status"])
    op.create_index("ix_interviewer_calendar_skill_id", "interviewer_calendar", ["skill_id"])


def downgrade() -> None:
    op.drop_index("ix_interviewer_calendar_skill_id", "interviewer_calendar")
    op.drop_index("ix_interviewer_calendar_emp_status", "interviewer_calendar")
    op.drop_index("ix_interviewer_calendar_emp_date", "interviewer_calendar")
    op.drop_table("interviewer_calendar")
