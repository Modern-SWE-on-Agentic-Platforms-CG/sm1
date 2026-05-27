"""create employee tables

Revision ID: 002
Revises: 001
Create Date: 2026-05-26

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "employee_master",
        sa.Column("emp_id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("emp_name", sa.String(200), nullable=False),
        sa.Column("email_id", sa.String(255), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("location", sa.String(100)),
        sa.Column("grade", sa.String(50)),
        sa.Column("bu", sa.String(100)),
        sa.Column("practice", sa.String(100)),
        sa.Column("market_unit", sa.String(100)),
        sa.Column("account", sa.String(100)),
        sa.Column("organisation", sa.String(100)),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_employee_master_bu", "employee_master", ["bu"])
    op.create_index("ix_employee_master_is_active", "employee_master", ["is_active"])

    op.create_table(
        "employee_role_details",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column(
            "emp_id", sa.BigInteger(),
            sa.ForeignKey("employee_master.emp_id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column("role_id", sa.Integer(), sa.ForeignKey("role_master.id"), nullable=False),
        sa.Column("assigned_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("emp_id", "role_id"),
    )

    op.create_table(
        "employee_tower_details",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column(
            "emp_id", sa.BigInteger(),
            sa.ForeignKey("employee_master.emp_id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column("tower_name", sa.String(100), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("employee_tower_details")
    op.drop_table("employee_role_details")
    op.drop_index("ix_employee_master_is_active", "employee_master")
    op.drop_index("ix_employee_master_bu", "employee_master")
    op.drop_table("employee_master")
