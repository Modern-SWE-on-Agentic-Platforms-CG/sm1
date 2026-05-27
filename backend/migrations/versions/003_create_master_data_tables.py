"""create master data tables (tower_master, technology_master, employee_technology_details)

Revision ID: 003
Revises: 002
Create Date: 2026-05-26

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tower_master",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("tower_name", sa.String(100), nullable=False, unique=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "technology_master",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("tech_name", sa.String(100), nullable=False),
        sa.Column("skill_group", sa.String(100)),
        sa.Column("tower_id", sa.Integer(), sa.ForeignKey("tower_master.id")),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("tech_name", "tower_id"),
    )

    op.create_table(
        "employee_technology_details",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column(
            "emp_id", sa.BigInteger(),
            sa.ForeignKey("employee_master.emp_id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column(
            "technology_id", sa.Integer(),
            sa.ForeignKey("technology_master.id"), nullable=False
        ),
        sa.Column("added_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("emp_id", "technology_id"),
    )


def downgrade() -> None:
    op.drop_table("employee_technology_details")
    op.drop_table("technology_master")
    op.drop_table("tower_master")
